import pandas as pd
import numpy as np
from mimesis import Generic, Person, Address
from mimesis.locales import Locale
from datetime import timedelta
import random


class DataframeAnonymizer:

    def __init__(self, df: pd.DataFrame, value: dict = None):
        self.df = df
        self.value = value
        self.params = self._df_params()

    def _df_params(self):
        """
        Returns a dictionary with the column names as keys and a dictionary of
        their descriptive statistics as values.
        """

        describ_obj = self.df.describe(include='all').to_dict()

        result = [{'col': col,
                   'top': describ_obj[col].get('top', None),
                   'min': describ_obj[col].get('min', None),
                   'max': describ_obj[col].get('max', None),
                   'freq': describ_obj[col].get('freq', None),
                   'unique': describ_obj[col].get('unique', None),
                   'count': describ_obj[col].get('count', None),
                   'mean': describ_obj[col].get('mean', None),
                   'std': describ_obj[col].get('std', None)}
                  for col in self.df.columns]

        dtypes_list = self.df.dtypes.to_list()

        # iterate over the dictionaries and data types simultaneously
        for d, dtype in zip(result, dtypes_list):
            d['dtype'] = str(dtype)

        # add value to list of dictionarys
        for index, item in enumerate(result):
            if self.value is not None and index in self.value:
                result[index]['value'] = self.value[index]
            else:
                result[index]['value'] = None

        return result

    def _anonymize_float(self, mean, std, count, min, max):
        result = np.random.default_rng().normal(mean, std, int(count))
        sorted_result = np.sort(result)
        sorted_result[0] = min
        sorted_result[-1] = max
        np.random.shuffle(sorted_result)
        return sorted_result.astype(float)

    def _anonymize_int(self, mean, std, count, min, max):
        floats = np.random.normal(mean, std, int(count))
        ints = np.round(floats).astype(int)
        sorted_ints = np.sort(ints)
        sorted_ints[0] = min
        sorted_ints[-1] = max
        np.random.shuffle(sorted_ints)
        return sorted_ints.astype(int)

    def _anonymize_str(self, top, count, unique, freq, value):
        # prob_max = int(freq) / int(count)
        generic = Generic(locale=Locale.DE)
        person = Person(locale=Locale.DE)
        address = Address(locale=Locale.DE)
        providers = {
            None: lambda nb: [generic.text.word() for _ in range(nb)],
            'gender': lambda nb: [person.gender() for _ in range(nb)],
            'address': lambda nb: [address.address() for _ in range(nb)],
            'person': lambda nb: [person.full_name() for _ in range(nb)]
        }
        string_list = providers[value](unique)
        random_strings = []
        i = 0
        while len(random_strings) < count:
            random_strings.append(string_list[i])
            i = (i + 1) % len(string_list)
        random.shuffle(random_strings)
        return random_strings

    def _anonymize_date(self, start_date, end_date, count):
        date_list = []
        for i in range(count):
            random_days = random.randint(0, (end_date - start_date).days)
            random_date = start_date + timedelta(days=random_days)
            date_list.append(random_date)
        return date_list

    def _anonymize_column(self, col_dict: dict):
        col_dtype = col_dict['dtype']
        col_count = col_dict['count']
        if col_dtype == 'float64':
            col_mean = col_dict['mean']
            col_std = col_dict['std']
            col_min = col_dict['min']
            col_max = col_dict['max']
            return self._anonymize_float(col_mean, col_std, col_count, col_min, col_max)
        elif col_dtype == 'int64':
            col_mean = col_dict['mean']
            col_std = col_dict['std']
            col_min = col_dict['min']
            col_max = col_dict['max']
            return self._anonymize_int(col_mean, col_std, col_count, col_min, col_max)
        elif col_dtype == 'object':
            col_top = col_dict['top']
            col_unique = col_dict['unique']
            col_freq = col_dict['freq']
            col_value = col_dict['value']
            return self._anonymize_str(col_top, col_count, col_unique, col_freq, col_value)
        elif col_dtype == 'datetime64[ns]':
            col_min = col_dict['min']
            col_max = col_dict['max']
            return self._anonymize_date(col_min, col_max, col_count)
        else:
            return None

    def anonymize_dataframe(self) -> pd.DataFrame:
        anonymized_df = self.df.copy()
        for col_dict in self.params:
            col_name = col_dict['col']
            col_anon = self._anonymize_column(col_dict)
            if col_anon is not None:
                anonymized_df[col_name] = col_anon
        return anonymized_df
