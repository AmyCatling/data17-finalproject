import pytest
import pandas as pd
from final_project.extract import *

extract = Extract()


def test_academy_is_df():
    assert isinstance(extract.academy_df, pd.DataFrame)


def test_talent_is_df():
    assert isinstance(extract.talent_df, pd.DataFrame)


def test_csv_file_names_in_list():
    assert len(extract.csv_file_names_list) > 0
    for file in extract.csv_file_names_list:
        assert 'csv' in file


def test_json_file_name_in_list():
    assert len(extract.json_file_names_list) > 0
    for file in extract.json_file_names_list:
        assert 'json' in file


def test_columns_are_added():
    assert 'original_file_name' in extract.academy_df.columns
    assert 'date' in extract.academy_df.columns
    assert 'course_name' in extract.academy_df.columns
    assert 'original_file_name' in extract.talent_df.columns






