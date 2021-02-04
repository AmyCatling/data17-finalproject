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