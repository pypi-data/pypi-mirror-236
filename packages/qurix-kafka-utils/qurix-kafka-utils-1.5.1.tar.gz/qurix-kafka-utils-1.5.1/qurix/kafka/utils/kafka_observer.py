import pandas as pd
from confluent_kafka.admin import AdminClient, ConfigResource
from confluent_kafka import ConsumerGroupTopicPartitions, TopicPartition
from confluent_kafka import Consumer


class KafkaObserver:
    def __init__(self, conf: dict):
        self.conf = conf
        self.admin_client = AdminClient(self.conf)

    def _getConsumerConfig(self, consumer_group: str = "kcc", offset: str = 'earliest'):
        conf = self.conf
        conf["group.id"] = consumer_group
        conf["auto.offset.reset"] = offset
        return conf

    def get_topic_info(self, extended: bool = False, selected_topics: list = None) -> pd.DataFrame:
        topics = self.admin_client.list_topics().topics

        if selected_topics is not None:
            topics = {key: value for key, value in topics.items() if key in selected_topics}

        topic_list = []
        partition_list = []
        replication_factor_list = []

        for topic_name, topic in topics.items():
            for partition_id, partition in topic.partitions.items():
                topic_list.append(topic_name)
                partition_list.append(partition_id)
                replication_factor_list.append(len(partition.replicas))

        df = pd.DataFrame({
            'Topic': topic_list,
            'Partition': partition_list,
            'Replication Factor': replication_factor_list
        })

        if extended:

            consumer_conf = self._getConsumerConfig()
            df_extended_1 = pd.DataFrame(columns=['Topic', 'Partition', 'CommitedOffset', 'CurrentOffset', 'CalculatedOffset', 'LowWatermark', 'HighWatermark'])
            df_extended_2 = pd.DataFrame(columns=['Topic', 'Retention Time', 'Retention Size', 'Cleanup Policy'])

            for topic in set(topic_list):
                # Offsets and Watermarks
                consumer = Consumer(consumer_conf)
                extended_information = self.get_offset_status(consumer, [topic], 'earliest')
                extended_information['Topic'] = topic
                df_extended_1 = pd.concat([df_extended_1, extended_information], ignore_index=True)
                consumer.close()
                # Retention Period and Cleanup Policy
                resource = ConfigResource('topic', topic)
                result = self.admin_client.describe_configs([resource])
                value_list = list(result.values())[0].result()
                data = {'Topic': topic, 'Retention Time': [value_list['retention.ms'].value], 'Retention Size': [value_list['retention.bytes'].value], 'Cleanup Policy': [value_list['cleanup.policy'].value]}
                df_extended_2 = pd.concat([df_extended_2, pd.DataFrame(data)], ignore_index=True)

            df = pd.merge(df, df_extended_1, on=['Topic', 'Partition'])
            df = pd.merge(df, df_extended_2, on=['Topic'])

        return df

    def get_consumer_groups(self) -> pd.DataFrame:
        # Rufe die Liste der Consumer-Gruppen ab
        consumer_groups = self.admin_client.list_consumer_groups().result()

        # Überprüfe, ob die Abfrage erfolgreich war
        if len(consumer_groups.errors) > 0:
            print(
                f"Fehler beim Abrufen der Consumer-Gruppen: {consumer_groups.errors}")
            return

        # Erstelle ein leeres Dataframe
        df = pd.DataFrame(columns=['Group_ID'])

        # Erstelle eine leere Liste für die Daten
        data = []

        # Iteriere über alle Consumer-Gruppen
        for group in consumer_groups.valid:
            group_id = group.group_id
            data.append({'Group_ID': group_id})

        # Erstelle ein neues Dataframe mit den Informationen
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

        return df

    def get_consumer_group_offsets(self, group_id: str) -> pd.DataFrame:
        # Erstelle eine Liste von ConsumerGroupTopicPartitions-Objekten
        consumer_group_offsets_request = [
            ConsumerGroupTopicPartitions(group_id=group_id)
        ]

        # Rufe die Methode list_consumer_group_offsets auf
        offsets = self.admin_client.list_consumer_group_offsets(
            consumer_group_offsets_request, require_stable=True, request_timeout=10.0)

        # Erstelle ein leeres Dataframe
        df = pd.DataFrame(columns=['Group_ID', 'Topic', 'Partition', 'Offset'])

        # Verarbeite die zurückgegebenen Offset-Informationen
        for group_id, future in offsets.items():
            # Warte auf das Ergebnis der Future
            result = future.result()

            for consumer_group_topic_partition in result.topic_partitions:
                topic = consumer_group_topic_partition.topic
                partition = consumer_group_topic_partition.partition
                offset = consumer_group_topic_partition.offset

                # Füge die Informationen dem Dataframe hinzu
                # df = df.append({'Group_ID': group_id, 'Topic': topic, 'Partition': partition, 'Offset': offset},
                #               ignore_index=True)
                data = [{'Group_ID': group_id, 'Topic': topic,
                         'Partition': partition, 'Offset': offset}]
                df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

        return df

    def get_consumer_groups_with_offsets(self) -> pd.DataFrame:
        # Rufe die Liste der Consumer-Gruppen ab
        consumer_groups = self.admin_client.list_consumer_groups().result()

        # Überprüfe, ob die Abfrage erfolgreich war
        if len(consumer_groups.errors) > 0:
            print(
                f"Fehler beim Abrufen der Consumer-Gruppen: {consumer_groups.errors}")
            return

        # Erstelle ein leeres Dataframe
        df = pd.DataFrame(columns=['Group_ID', 'Topic', 'Partition', 'Offset'])

        # Iteriere über alle Consumer-Gruppen und füge sie dem Dataframe hinzu
        for group in consumer_groups.valid:
            group_id = group.group_id

            # Rufe die Offset-Informationen für die Consumer-Gruppe ab
            offsets_df = self.get_consumer_group_offsets(group_id)

            # Füge die Offset-Informationen dem Dataframe hinzu
            # df = df.append(offsets_df, ignore_index=True)
            df = pd.concat([df, offsets_df], ignore_index=True)

        return df

    def get_offset_status(self, consumer, topic: str, auto_offset: str) -> pd.DataFrame:
        c_data = {"Partition": [], "CommitedOffset": [], "CurrentOffset": [
        ], "CalculatedOffset": [], "LowWatermark": [], "HighWatermark": []}
        tp = []
        committed = []
        com_o = -1001

        # Liste der Topics und Anzahl Partitions abrufen
        t = consumer.list_topics()
        p = len(t.topics[topic[0]].partitions)
        for i in range(p):
            tp.append(TopicPartition(topic[0], i))

        # Offsets abrufen
        offset = consumer.position(tp)
        try:
            committed = consumer.committed(tp, timeout=2)
        except ConnectionError:
            print("Timeout")

        for o in offset:
            wm = consumer.get_watermark_offsets(tp[o.partition])

            c_data["Partition"].append(o.partition)
            if len(committed) > 0:
                com_o = committed[o.partition].offset
                c_data["CommitedOffset"].append(com_o)
            else:
                c_data["CommitedOffset"].append(-1001)
            c_data["CurrentOffset"].append(o.offset)
            co = o.offset
            if co == -1001:
                co = com_o
                if co == -1001:
                    if auto_offset == "earliest":
                        co = wm[0]
                    else:
                        co = wm[1]

            c_data["CalculatedOffset"].append(co)
            c_data["LowWatermark"].append(wm[0])
            c_data["HighWatermark"].append(wm[1])

            # print(f"Partition: {o.partition}, Commited Offset {com_o}
            #  Current Offset: {o.offset}, Calculated Offset {co}
            # Low Watermark: {wm[0]}, High Watermark {wm[1]}
            # Messages in Queue: {wm[1] - co}")

        df = pd.DataFrame(c_data)
        return df

    def plot_offset_status(self, consumer):
        df = self.get_offset_status(consumer)
        df.plot(kind="bar", y=["LowWatermark",
                "CalculatedOffset", "HighWatermark"])
