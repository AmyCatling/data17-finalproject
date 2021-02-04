-- ALL FOUR TABLES COMBINED
-- APPLICANT ID IS FOREIGN KEY FOR EACH TABLE

CREATE DATABASE Sparta_Db;
USE Sparta_Db;

-- DROP TABLE Applicants
-- DROP TABLE Tests 
-- DROP TABLE Talent
-- DROP TABLE Academy

CREATE TABLE Applicants (
    applicant_id INT NOT NULL IDENTITY PRIMARY KEY,
    applicant_name VARCHAR(100),
    gender CHAR(1),
    dob DATE,
    email VARCHAR(320),
    city VARCHAR(100),
    applicant_address VARCHAR(MAX),
    postcode VARCHAR(4),
    phone VARCHAR(20),
    university VARCHAR(MAX),
    degree VARCHAR(5),
    invited_date INT,
    month_year VARCHAR(10),
    invited_by VARCHAR(100)
);


CREATE TABLE Tests (
    name VARCHAR(100),
    psychometric_score_100 INT,
    presentation_score_32 INT,
    academy VARCHAR(20),
    test_date DATE,
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id)

);

CREATE TABLE Talent(
talent_id INT NOT NULL IDENTITY PRIMARY KEY,
talent_name VARCHAR(100) NOT NULL,
assessment_day DATE,
known_technologies VARCHAR(100),
strengths VARCHAR(100),
weaknesses VARCHAR(100),
self_development BIT,
geo_flexible BIT,
financial_support_self BIT,
result BIT,
course_interest VARCHAR(100),
applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id)
)
 
CREATE TABLE Academy(
    student_id INT NOT NULL IDENTITY PRIMARY KEY,
    trainer VARCHAR(100),
    analytical_w1 INT,
    independent_w1 INT,
    determined_w1 INT,
    professional_w1 INT,
    studious_w1 INT,
    imaginative_w1 INT,
    analytical_w2 INT,
    independent_w2 INT,
    determined_w2 INT,
    professional_w2 INT,
    studious_w2 INT,
    imaginative_w2 INT,
    analytical_w3 INT,
    independent_w3 INT,
    determined_w3 INT,
    professional_w3 INT,
    studious_w3 INT,
    imaginative_w3 INT,
    analytical_w4 INT,
    independent_w4 INT,
    determined_w4 INT,
    professional_w4 INT,
    studious_w4 INT,
    imaginative_w4 INT,
    analytical_w5 INT,
    independent_w5 INT,
    determined_w5 INT,
    professional_w5 INT,
    studious_w5 INT,
    imaginative_w5 INT,
    analytical_w6 INT,
    independent_w6 INT,
    determined_w6 INT,
    professional_w6 INT,
    studious_w6 INT,
    imaginative_w6 INT,
    analytical_w7 INT,
    independent_w7 INT,
    determined_w7 INT,
    professional_w7 INT,
    studious_w7 INT,
    imaginative_w7 INT,
     analytical_w8 INT,
    independent_w8 INT,
    determined_w8 INT,
    professional_w8 INT,
    studious_w8 INT,
    imaginative_w8 INT,
     analytical_w9 INT,
    independent_w9 INT,
    determined_w9 INT,
    professional_w9 INT,
    studious_w9 INT,
    imaginative_w9 INT,
     analytical_w10 INT,
    independent_w10 INT,
    determined_w10 INT,
    professional_w10 INT,
    studious_w10 INT,
    imaginative_w10 INT,
    course_name VARCHAR(100),
    active BIT,
    applicant_id INT FOREIGN KEY REFERENCES Applicants(applicant_id)
 
)
 

-- SELECT * FROM Applicants;
-- SELECT * FROM Tests; 
-- SELECT * FROM Talent;
-- SELECT * FROM Academy;