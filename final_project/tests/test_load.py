from final_project.load import LoadData
import pytest

def test_connection():
    loading = LoadData()
    assert loading == '<pyodbc.Connection object at 0x07CD4EA8>'


def test_import_talent_data():
    pass


def test_import_academy_data():
    pass