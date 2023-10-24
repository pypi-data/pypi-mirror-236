import json
from confluent_kafka import (
    Consumer,
    KafkaError,
    TopicPartition,
    OFFSET_BEGINNING,
    OFFSET_END,
)

import datetime
import logging
import pandas as pd
import sys

project_path = "qurix/kafka/utils/"

# Add the project path to the PYTHONPATH
sys.path.insert(0, project_path)
from qurix.kafka.utils.offset_enum import Offset

logging.basicConfig(level=logging.INFO)


class GenericConsumer:
    def __init__(self, topic: str, consumer_config: dict, offset: Offset = None):
        self.consumer = Consumer(consumer_config)
        self.topic = topic
        self.offset = offset.value if offset is not None else None

    def set_offset(self, partition: int, offset_option: Offset = Offset.EXPLICIT, offset_value: int = 0, timestamp_dt: datetime = None) -> None:

        self.partition = partition
        if offset_option == Offset.EARLIEST:
            self.offset = OFFSET_BEGINNING
        elif offset_option == Offset.LATEST:
            self.offset = OFFSET_END
        elif offset_option == Offset.LAST:
            watermark_offsets = self.consumer.get_watermark_offsets(TopicPartition(topic=self.topic, partition=partition))
            if watermark_offsets:
                self.offset = watermark_offsets[1] - 1
                logging.info(f"Last Offset for Partition {partition}: {self.offset}")
            else:
                logging.info(f"No watermarks found for Partition {partition}")
        elif offset_option == Offset.TIMESTAMP:
            unix_timestamp = int(timestamp_dt.timestamp()) * 1000
            tp = TopicPartition(self.topic, partition, unix_timestamp)
            offset_info = self.consumer.offsets_for_times([tp])
            offset = offset_info[0].offset if offset_info else None
            logging.info(f"Timestamp: {timestamp_dt}, Offset: {offset}")
            self.offset = offset
        else:
            self.offset = offset_value
        tp = TopicPartition(topic=self.topic, partition=partition, offset=self.offset)
        self.consumer.assign([tp])
        self.consumer.commit(offsets=[tp])

    def read_messages(
        self,
        num_messages=-1,
    ) -> pd.DataFrame:
        if self.offset is None:
            self.consumer.subscribe(
                [self.topic]
            )  # Subscribe to the topic when offset is not set

        d_messages = {
            "Partition": [],
            "Offset": [],
            "Timestamp": [],
            "Len": [],
            "Key": [],
            "Header": [],
            "Value": [],
        }

        read = num_messages

        while read:
            msg = self.consumer.poll(10.0)
            if msg is None:
                logging.debug("No further data in topic")
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.debug(
                        "Reached end of partition, waiting for new messages..."
                    )
                    break  # Exit the loop if no new messages to consume
                logging.debug(msg.error())
            else:
                d_messages["Partition"].append(msg.partition())
                d_messages["Offset"].append(msg.offset())
                d_messages["Timestamp"].append(
                    datetime.datetime.fromtimestamp(msg.timestamp()[1] / 1000)
                )
                d_messages["Len"].append(len(msg.value()))
                d_messages["Key"].append(msg.key())
                d_messages["Header"].append(msg.headers())
                d_messages["Value"].append(msg.value())
                read = read - 1
                logging.debug(f"Remaining to read: {read}")
                if read == 0:  # Check if all desired messages are consumed
                    break
        df = pd.DataFrame(d_messages)
        self.consumer.close()
        return df

    def extend_df_with_header(self, df: pd.DataFrame) -> pd.DataFrame:
        df_extended = df.copy()
        df_extended['Header'] = df_extended['Header'].apply(lambda x: dict(x))

        for index, row in df_extended.iterrows():
            header = row['Header']
            for key, value in header.items():
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                new_column_name = 'h_' + key
                df_extended.at[index, new_column_name] = value if value is not None else None

        df_extended.drop(columns=['Header'], inplace=True)
        return df_extended

    def extract_json_value(self, df: pd.DataFrame, column: str) -> list:
        def process_json(json_data):
            data = json.loads(json_data)

            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                return pd.json_normalize(data)
            else:
                raise ValueError("Invalid JSON structure")

        df2 = df[column].apply(process_json)
        return pd.concat(df2.to_list(), ignore_index=True)
