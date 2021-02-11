CREATE DATABASE Sparta_Db;
USE Sparta_Db;

CREATE TABLE Behaviours (
    behaviour_id INT NOT NULL IDENTITY PRIMARY KEY,
    behaviour_name VARCHAR(20)
);

CREATE TABLE Academies (
    academy_id INT NOT NULL IDENTITY PRIMARY KEY,
    academy_location VARCHAR(20)
);

CREATE TABLE Technologies (
    technology_id INT NOT NULL IDENTITY PRIMARY KEY,
    skill_name VARCHAR(20)
);

CREATE TABLE Strengths (
    strength_id INT NOT NULL IDENTITY PRIMARY KEY,
    strength_name VARCHAR(50)
);

CREATE TABLE Weaknesses (
    weakness_id INT NOT NULL IDENTITY PRIMARY KEY,
    weakness_name VARCHAR(50)
);

CREATE TABLE Gender (
    gender_id INT NOT NULL IDENTITY PRIMARY KEY,
    gender VARCHAR(10)
);

CREATE TABLE City (
    city_id INT NOT NULL IDENTITY PRIMARY KEY,
    city_name VARCHAR(50)
);

CREATE TABLE University_Details (
    university_id INT NOT NULL IDENTITY PRIMARY KEY,
    university_name VARCHAR(100)
);

CREATE TABLE Degree_Grade (
    degree_grade_id INT NOT NULL IDENTITY PRIMARY KEY,
    classification VARCHAR(20)

);

CREATE TABLE Staff (
    staff_id INT NOT NULL IDENTITY PRIMARY KEY,
    staff_name VARCHAR(100) NOT NULL
);

CREATE TABLE Applicants (
    applicant_id INT NOT NULL IDENTITY PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    gender_id INT FOREIGN KEY REFERENCES Gender(gender_id),
    dob DATE,
    email VARCHAR(320),
    city_id INT FOREIGN KEY REFERENCES City(city_id),
    address VARCHAR(MAX),

    postcode_area VARCHAR(10),
    phone_number VARCHAR(30),

    university_id INT FOREIGN KEY REFERENCES University_Details(university_id),
    degree_grade_id INT FOREIGN KEY REFERENCES Degree_Grade(degree_grade_id),
    staff_id INT FOREIGN KEY REFERENCES Staff(staff_id)
);

CREATE TABLE Weekly_Results (
    Composite INT IDENTITY PRIMARY KEY,
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id),
    behaviour_id INT FOREIGN KEY REFERENCES Behaviours(behaviour_id),
    week_number INT,
    score INT
);

--CREATE TABLE Courses (
--    course_id INT NOT NULL IDENTITY PRIMARY KEY,
--    course_name VARCHAR(20),
--    stream_id INT FOREIGN KEY REFERENCES Streams(stream_id),
--    staff_id INT FOREIGN KEY REFERENCES Staff(staff_id)
--);


CREATE TABLE Student (
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id),
--    course_id INT FOREIGN KEY REFERENCES Courses(course_id)
    graduated CHAR(1)
);

CREATE TABLE Sparta_Day_Interview (
    sparta_day_interview_id INT NOT NULL IDENTITY PRIMARY KEY,
    self_development BIT,
    geo_flexible BIT,
    financial_support_self BIT,
    result BIT,
--    course_id INT FOREIGN KEY REFERENCES Courses(course_id),
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id)
);

CREATE TABLE Sparta_Day_Assessment (
    sparta_day_assessment_id INT NOT NULL IDENTITY PRIMARY KEY,
    sparta_day_date DATE,
    psychometric_score INT,
    presentation_score INT,
    academy_id INT FOREIGN KEY REFERENCES Academies(academy_id),
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id)
);

CREATE TABLE Strength_junction_table (
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id),
    strength_id INT FOREIGN KEY REFERENCES Strengths(strength_id)
);

CREATE TABLE Weakness_junction_table (
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id),
    weakness_id INT FOREIGN KEY REFERENCES Weaknesses(weakness_id)
);


CREATE TABLE Talent_Technologies_junction (
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id),
    technology_id INT FOREIGN KEY REFERENCES Technologies(technology_id),
    self_grade INT
);


TRUNCATE TABLE Talent_Technologies_junction; 
TRUNCATE TABLE Weakness_junction_table;
TRUNCATE TABLE Strength_junction_table;
TRUNCATE TABLE Sparta_Day_Assessment;
TRUNCATE TABLE Sparta_Day_Interview; 
TRUNCATE TABLE Student;
TRUNCATE TABLE Courses;
TRUNCATE TABLE Weekly_Results;
TRUNCATE TABLE Applicants;
TRUNCATE TABLE Staff;
TRUNCATE TABLE Degree_Grade;
TRUNCATE TABLE University_Details;
TRUNCATE TABLE City;
TRUNCATE TABLE Gender;
TRUNCATE TABLE Weaknesses;
TRUNCATE TABLE Strengths;
TRUNCATE TABLE Technologies;
TRUNCATE TABLE Academies;
TRUNCATE TABLE Behaviours;

SELECT * FROM Weekly_Results;
SELECT * FROM Behaviours;
SELECT * FROM Student;
SELECT * FROM Applicants;
SELECT * FROM Gender;
SELECT * FROM City;
SELECT * FROM University_Details;
SELECT * FROM Degree_Grade;
SELECT * FROM Staff; 
SELECT * FROM Courses;
SELECT * FROM Sparta_Day_Interview; 
SELECT * FROM Sparta_Day_Assessment; 
SELECT * FROM Academies;
SELECT * FROM Strengths;
SELECT * FROM Weaknesses;
SELECT * FROM Strength_junction_table
SELECT * FROM Weakness_junction_table;
SELECT * FROM Talent_Technologies_junction; 
SELECT * FROM Technologies;