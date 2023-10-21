import pandas as pd
from datetime import datetime
import sys
sys.path.insert(0, "")
if True:
    from qurix.kafka.utils.anonymizer import DataframeAnonymizer


def test_anonymize_dataframe():
    df = pd.DataFrame({
        'float_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'int_col': [1, 2, 3, 4, 5],
        'str_col': ['a', 'b', 'c', 'd', 'e'],
        'date_col': [datetime(2021, 1, 1), datetime(2021, 1, 2), datetime(2021, 1, 3), datetime(2021, 1, 4), datetime(2021, 1, 5)]
    })

    anonymizer = DataframeAnonymizer(df, {2: 'gender'})
    anonymized_df = anonymizer.anonymize_dataframe()

    # Check that the anonymized dataframe has the same shape as the original dataframe
    assert anonymized_df.shape == df.shape

    # Check that the anonymized dataframe has the same data types as the original dataframe
    assert anonymized_df.dtypes.equals(df.dtypes)

    # Check that the anonymized dataframe has different values than the original dataframe
    assert not anonymized_df.equals(df)

    # Check that the anonymized dataframe has the same column names as the original dataframe
    assert list(anonymized_df.columns) == list(df.columns)

    # Check that the anonymized dataframe has the same index as the original dataframe
    assert anonymized_df.index.equals(df.index)

    # Check that the anonymized dataframe has different values than the original dataframe
    assert not anonymized_df.equals(df)
