import pytest
import pandas as pd
from final_project.extract import *

extract = Extract()


def test_df():
    assert isinstance(extract.academy_df, pd.DataFrame)
    assert isinstance(extract.talent_df, pd.DataFrame)
    assert isinstance(extract.applicant_df, pd.DataFrame)
    assert isinstance(extract.sparta_day_df, pd.DataFrame)


def test_file_names_in_correct_list():
    assert len(extract.academy_csv_file_names_list) > 0
    for file in extract.academy_csv_file_names_list:
        assert 'csv' in file

    assert len(extract.json_file_names_list) > 0
    for file in extract.json_file_names_list:
        assert 'json' in file

    assert len(extract.applicant_csv_file_names_list) > 0
    for file in extract.applicant_csv_file_names_list:
        assert 'Applicants.csv' in file

    assert len(extract.txt_file_names_list) > 0
    for file in extract.txt_file_names_list:
        assert 'txt' in file


def test_columns_are_added():
    assert 'original_file_name' and 'date' and 'course_name' in extract.academy_df.columns
    assert 'original_file_name' in extract.talent_df.columns
    assert 'original_file_name' in extract.applicant_df.columns
    assert 'original_file_name' and 'academy' and 'date' and 'name' and 'psychometrics' and 'presentation' in extract.sparta_day_df.columns


