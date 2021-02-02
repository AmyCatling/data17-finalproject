import pytest
import pandas as pd
from final_project.extract import Extract


extract = Extract()
# def test_academy_is_df():
#
#     assert isinstance(extract.self.academy_df, pd.DataFrame)
#
# def test_talent_is_df(self.talent_df):
#     assert isinstance(self.talent_df, pd.DataFrame)


def test_csv_file_names_in_list():
    assert len(extract.csv_file_names_list) > 0
    for file in extract.csv_file_names_list:
        assert 'csv' in file


def test_json_file_name_in_list():
    assert len(extract.json_file_names_list) > 0
    for file in extract.json_file_names_list:
        assert 'json' in file






