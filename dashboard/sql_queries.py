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



