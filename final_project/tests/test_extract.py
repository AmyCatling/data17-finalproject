import pytest
import pandas as pd
from final_project.extract import *

def test_academy_is_df(self.academy_df):
    assert isinstance(self.academy_df, pd.DataFrame)

def test_talent_is_df(self.talent_df):
    assert isinstance(self.talent_df, pd.DataFrame)

def test_csv_file_names_in_list():
    assert len(self.csv_file_names_list) > 0
    for file in self.csv_file_names_list:
        assert 'csv' in file

def test_json_file_name_in_list():
    assert len(self.json_file_names_list) > 0
    for file in self.json_file_names_list:
        assert 'json' in file








