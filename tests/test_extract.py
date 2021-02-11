import pytest
import pandas as pd
from final_project.broken_extract import *

extract = Extract()


def test_df():
    assert isinstance(extract.academy_df, pd.DataFrame)
    assert isinstance(extract.talent_df, pd.DataFrame)
    assert isinstance(extract.applicant_df, pd.DataFrame)
    assert isinstance(extract.sparta_day_df, pd.DataFrame)


def test_file_names_in_correct_list():
    assert bool(extract.items_in_bucket) == True
    assert bool(extract.file_names_list) == True


def test_columns_are_added():
    assert 'original_file_name' and 'course_start_date' and 'course_end_date' and 'course_name' in extract.academy_df.columns
    assert 'original_file_name' in extract.talent_df.columns
    assert 'original_file_name' in extract.applicant_df.columns
    assert 'original_file_name' and 'academy' and 'date' and 'name' and 'psychometrics' and 'presentation' in extract.sparta_day_df.columns


