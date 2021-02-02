import csv
import json
import pandas as pd
import numpy as np
import pytest

from transform import Transform_csv

def test_df_shape():
    t = Transform_csv()
    assert len(t.academy_df.columns) == 50

def test_add_columns():
    t = Transform_csv()
    t.add_columns()
    assert len(t.academy_df.columns) == 51

def test_active_nulls():
    t = Transform_csv()
    t.active_nulls()
    assert t.academy_df["Analytic_W8"][0] == 99.0

def test_null_rename():
    t = Transform_csv()
    t.add_columns()
    t.active_nulls()
    t.null_rename()
    assert t.academy_df["Active"][0] == "N"

def test_floats_to_ints():
    t = Transform_csv()
    t.add_columns()
    t.active_nulls()
    t.null_rename()
    assert t.academy_df["Analytic_W8"].dtype == float
    t.floats_to_ints()
    assert t.academy_df["Analytic_W8"].dtype == int