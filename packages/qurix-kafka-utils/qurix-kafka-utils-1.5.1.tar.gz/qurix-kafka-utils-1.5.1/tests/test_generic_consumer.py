import pandas as pd
import pytest
import sys
import datetime
from unittest.mock import Mock
project_path = "qurix/kafka/utils/"
sys.path.insert(0, project_path)
from qurix.kafka.utils.generic_consumer import GenericConsumer
from qurix.kafka.utils.offset_enum import Offset


consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest"}


# Mock the Kafka Consumer
class MockConsumer:
    def __init__(self):
        self.consumer = Mock()
        self.consumer.error.return_value = None

    def poll(self):
        mock_message = Mock()
        mock_message.error.return_value = None
        mock_message.partition.return_value = 0
        mock_message.offset.return_value = 0
        mock_message.timestamp.return_value = (int(datetime.datetime.now().timestamp() * 1000), 0)
        mock_message.value.return_value = b'mock_message'
        mock_message.key.return_value = b'key'
        mock_message.headers.return_value = []

        messages = [mock_message]
        return messages

    def close(self):
        pass


# Mock the GenericConsumer
@pytest.fixture(scope="function")
def kafka_consumer():
    return GenericConsumer(topic="my_topic", consumer_config=consumer_config)


def test_consumer_reads_messages(kafka_consumer):
    messages = kafka_consumer.read_messages()
    assert len(messages["Value"]) == 0


def test_consumer_with_partition_offset(kafka_consumer):
    kafka_consumer.set_offset(0, offset_value=1000, offset_option=Offset.EXPLICIT)
    messages = kafka_consumer.read_messages()
    assert len(messages["Value"]) == 0


@pytest.fixture
def sample_dataframe():
    data = {
        'Header': [
            [('source', b'Testdriver'), ('target', b'Confluent_kafka')],
            [('source', b'AnotherSource'), ('target', b'AnotherTarget')],
        ]
    }
    return pd.DataFrame(data)


def test_extend_df_with_header(kafka_consumer, sample_dataframe):
    extended_df = kafka_consumer.extend_df_with_header(sample_dataframe)
    assert 'Header' not in extended_df.columns
    assert 'h_source' in extended_df.columns
    assert 'h_target' in extended_df.columns
    assert extended_df['h_source'].tolist() == ['Testdriver', 'AnotherSource']
    assert extended_df['h_target'].tolist() == ['Confluent_kafka', 'AnotherTarget']


def test_extract_json_value(kafka_consumer, sample_dataframe):
    sample_dataframe['JsonColumn'] = [
        '{"key": "value"}',
        '{"key": "value2"}'
    ]
    concatenated_df = pd.concat([sample_dataframe, sample_dataframe], ignore_index=True)
    result_df = kafka_consumer.extract_json_value(concatenated_df, 'JsonColumn')
    assert result_df.shape == (4, 1)
    assert result_df['key'].tolist() == ['value', 'value2', 'value', 'value2']
