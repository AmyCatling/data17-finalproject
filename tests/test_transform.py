import csv
import json
import pandas as pd
import numpy as np
import datetime
import pytest
# Tests are run on a certain csv, need to make sure we know which one it is tested on
from final_project.transform import Transform_academy_csv, Transform_json, Transform_applicant_csv

# def test_df_shape():
#     t = Transform_csv()
#     assert len(t.academy_df.columns) == 62
#
# def test_add_columns():
#     t = Transform_csv()
#     t.add_columns()
#     assert len(t.academy_df.columns) == 63
#
# def test_active_nulls():
#     t = Transform_csv()
#     t.active_nulls()
#     assert t.academy_df["Analytic_W8"][5] == 99.0
#
# def test_null_rename():
#     t = Transform_csv()
#     t.add_columns()
#     t.active_nulls()
#     t.null_rename()
#     assert t.academy_df["Active"][5] == "N"
#
# def test_floats_to_ints():
#     t = Transform_csv()
#     t.add_columns()
#     t.active_nulls()
#     t.null_rename()
#     assert t.academy_df["Analytic_W8"].dtype == float
#     t.floats_to_ints()
#     assert t.academy_df["Analytic_W8"].dtype == int
#
# def test_deactive_nulls():
#     t = Transform_csv()
#     t.active_nulls()
#     t.deactive_nulls()
#     assert t.academy_df["Analytic_W8"][5] == 0
#
# def test_json_shape():
#     j = Transform_json()
#     assert len(j.talent_df.columns) == 10
#
# def test_json_active_bit():
#     j = Transform_json()
#     j.active_bits()
#     assert j.talent_df['geo_flex'][0] == 1
#     assert j.talent_df.loc['geo_flex'][0].dtype == bin
#
# def test_json_date_changed():
#     j = Transform_json()
#     j.date_types_changed()
#     assert j.talent_df["date"].dtype == np.datetime64
#
#
#
def test_applicants_dob_format():
    test = Transform_applicant_csv('df')
    test.fix_dob_format()
    date_test = datetime.date(1994,8,4)
    assert test.applicant_df['dob'][0] == date_test

def test_applicants_invite_date_format():
    test = Transform_applicant_csv()
    test.fix_applicants_invite_format()
    date_test = datetime.date(2019, 4, 10)
    assert test.applicant_df['invited_date'][0] == date_test


def test_fix_nulls_applicants():
    test = Transform_applicant_csv()
    test.fix_nulls_applicants()
    assert test.applicant_df['address'][12] == 'Unknown'

def test_applicant_format_phones():
    test = Transform_applicant_csv('df')
    test.format_phones()
    assert test.applicant_df['phone_number'][0] == '+442957830228'