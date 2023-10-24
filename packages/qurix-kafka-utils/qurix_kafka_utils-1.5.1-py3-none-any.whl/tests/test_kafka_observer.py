from unittest.mock import MagicMock
import sys
sys.path.insert(0, "")
if True:
    from qurix.kafka.utils.kafka_observer import KafkaObserver


def test_get_topic_info():
    # Set up mock data for the admin client
    mock_topics = {
        'topic1': MagicMock(partitions={
            0: MagicMock(replicas=[1, 2]),
            1: MagicMock(replicas=[2, 2])
        }),
        'topic2': MagicMock(partitions={
            0: MagicMock(replicas=[1, 2]),
            1: MagicMock(replicas=[2, 2])
        })
    }

    mock_admin_client = MagicMock()
    mock_admin_client.list_topics.return_value.topics = mock_topics

    # Create the observer and set the mock admin client
    observer = KafkaObserver({'bootstrap.servers': 'localhost:9092'})
    observer.admin_client = mock_admin_client

    # Call the method and check the result
    result = observer.get_topic_info()

    assert len(result) == 4
    assert set(result['Topic']) == set(['topic1', 'topic2'])
    assert set(result['Partition']) == set([0, 1])
    assert set(result['Replication Factor']) == set([2, 2])


def test_get_consumer_groups():
    # Set up mock data for the admin client
    mock_consumer_groups = MagicMock(valid=[
        MagicMock(group_id='group1'),
        MagicMock(group_id='group2')
    ], errors=[])

    mock_admin_client = MagicMock()
    mock_admin_client.list_consumer_groups.return_value.result.return_value = mock_consumer_groups

    # Create the observer and set the mock admin client
    observer = KafkaObserver({'bootstrap.servers': 'localhost:9092'})
    observer.admin_client = mock_admin_client

    # Call the method and check the result
    result = observer.get_consumer_groups()

    assert len(result) == 2
    assert result.iloc[0]['Group_ID'] == 'group1'
    assert result.iloc[1]['Group_ID'] == 'group2'


def test_get_consumer_group_offsets():
    # Set up mock data for the admin client
    mock_offsets = {
        'group1': MagicMock(),
        'group2': MagicMock()
    }

    mock_result1 = MagicMock()
    mock_result1.topic_partitions = [
        MagicMock(topic='topic1', partition=0, offset=100),
        MagicMock(topic='topic1', partition=1, offset=200),
        MagicMock(topic='topic2', partition=0, offset=300),
        MagicMock(topic='topic2', partition=1, offset=400)
    ]
    mock_offsets['group1'].result.return_value = mock_result1

    mock_result2 = MagicMock()
    mock_result2.topic_partitions = [
        MagicMock(topic='topic1', partition=0, offset=500),
        MagicMock(topic='topic1', partition=1, offset=600),
        MagicMock(topic='topic2', partition=0, offset=700),
        MagicMock(topic='topic2', partition=1, offset=800)
    ]
    mock_offsets['group2'].result.return_value = mock_result2
