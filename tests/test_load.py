from final_project.load import LoadData

def test_connection():
    loading = LoadData()
    assert "pyodbc.Connection" in str(loading.conn)

def test_import_talent_data():
    loading = LoadData()
    df = loading.talent_df
    df_row_one = df.iloc[0]
    assert loading.conn.execute("SELECT * FROM Talent LIMIT 1").fetchone() == df_row_one

def test_import_academy_data():
    loading = LoadData()
    df = loading.academy_df
    df_row_one = df.iloc[0]
    assert loading.conn.execute("SELECT * FROM Academy LIMIT 1").fetchone() == df_row_one

def test_update_academy_data():
    loading = LoadData()
    old_course_name = " "
    new_course_name = " "
    assert loading.conn.execute("SELECT course_name FROM table WHERE course_name = ? LIMIT 1",
                                old_course_name).fetchone() == old_course_name
    assert loading.conn.execute("SELECT course_name FROM table WHERE course_name = ? LIMIT 1",
                                new_course_name).fetchone() == new_course_name