# Get list of all students on a selected course
"""
SELECT name
FROM Applicants
WHERE Course.course_name = 'selected course'
INNER JOIN Student ON Student.applicant_id = Applicants.applicant_id
INNER JOIN Course ON Course.course_id = Student.course_id
"""

# Get results for one person (specified by name)
# DF of applicant name, behaviour name, score (maybe we don't need to show the applicant name?)
"""
SELECT Applicants.name, Behaviour.behaviour_name, Weekly_Results.week_number, Weekly_Results.score 
FROM Weekly_Results 
WHERE Applicants.name = 'selected name' 
INNER JOIN Applicants ON Applicants.applicant_id = Weekly_Results.applicant_id
INNER JOIN Behaviour ON Behaviour.behaviour_id = Weekly_Results.behaviour_id
"""


# two tables
# one personal info - name address etc
# another for, strengths weaknesses, how they did in qualitative tests
#
# table 1:
"""
SELECT Applicants.name AS "Trainee", Applicants.email, University_Details.university_name, 
Degree_Grade.classification, Staff.staff_name AS "Trainer"
FROM Applicants
INNER JOIN University_Details ON University_Details.university_id = Applicants.university_id
INNER JOIN Degree_Grade ON Degree_Grade.degree_grade_id = Applicants.degree_grade_id
INNER JOIN Staff ON Staff.staff_id = Applicants.staff_id
"""

# table 2:

# 1. get strengths list
list(pd.read_sql("""
SELECT strength FROM Strengths
INNER JOIN Strengths_junction_table ON Strengths.strength_id = Strengths_junction_table.strength_id
INNER JOIN Applicants ON Strengths_junction_table.applicant_id = Applicants.applicant_id
WHERE Applicants.name = {self.chosen_student}
""", self.docker)['strength'])
list(pd.read_sql('''
                                                SELECT behaviour_name FROM Behaviours
                                                ''', self.docker)['behaviour_name'])
