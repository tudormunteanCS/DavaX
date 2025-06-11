/*
I have a task at a Database Management systems training that implies this: designing a data base to with core functionality for employees to track time worked per week. This is the flow: The employee(employee table) must complete a form which includes the following:
1.Project code he is working on (table with project codes)
2.Task Details (one of 7 options)
3.Time type (one of 8 options)
4.Location (one of 4 options)
5.Relocated Country (a country so needed country table)
6.Selected Dates(a maximum one week period)
7.Quantity (a number describing the number of hours worked per day)
*/

-- Creating the database
CREATE DATABASE employee_timesheet;
USE employee_timesheet

--Creating Tables

CREATE TABLE Employees(
	employee_id INT IDENTITY(1,1) PRIMARY KEY,
	employee_first_name VARCHAR(100) NOT NULL,
	employee_last_name VARCHAR(100) NOT NULL,
	employee_email VARCHAR(100) NOT NULL UNIQUE
)

CREATE TABLE Projects(
	project_id INT IDENTITY(1,1) PRIMARY KEY,
	project_code VARCHAR(100) NOT NULL UNIQUE
)

CREATE TABLE Tasks(
	task_id INT IDENTITY(1,1) PRIMARY KEY,
	task_name VARCHAR(100) NOT NULL
)

CREATE TABLE TimeTypes(
	time_type_id INT IDENTITY(1,1) PRIMARY KEY,
	time_type_name VARCHAR(100) NOT NULL
)

CREATE TABLE Locations(
	location_id INT IDENTITY(1,1) PRIMARY KEY,
	location_name VARCHAR(100) NOT NULL
)

CREATE TABLE Countries(
	country_id INT IDENTITY(1,1) PRIMARY KEY,
	country_name VARCHAR(100) NOT NULL
)

--Task assigned to project many to many mapping
CREATE TABLE ProjectTasks(
	project_id INT,
	task_id INT,
	PRIMARY KEY (project_id,task_id),
	FOREIGN KEY (project_id) REFERENCES Projects(project_id),
	FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
)

CREATE TABLE TimesheetEntries(
	entry_id INT IDENTITY(1,1) PRIMARY KEY,
	employee_id INT NOT NULL,
	project_id INT NOT NULL,
    task_id INT NOT NULL,
    time_type_id INT NOT NULL,
    location_id INT NOT NULL,
	country_id INT NOT NULL,
	entry_date DATE NOT NULL, -- singe day entry, easier for querying time worked per week/month and checking hour constraints
	hours_worked DECIMAL(4,2) NOT NULL CHECK (hours_worked >= 0 AND hours_worked <=24),
	approval_status VARCHAR(20) DEFAULT 'pending',
	metadata NVARCHAR(400), -- here we will store the json, could be submitted via (PC,iPhone,Other mobile device,etc) /
	created_at DATETIME2 DEFAULT SYSDATETIME(),
    updated_at DATETIME2,

	FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
    FOREIGN KEY (time_type_id) REFERENCES TimeTypes(time_type_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
)
-- Indexes for performance (non PK/FK)
CREATE INDEX idx_entry_date ON TimesheetEntries(entry_date);
CREATE INDEX idx_approval_status ON TimesheetEntries(approval_status);

-- Insert into Employees
INSERT INTO Employees(employee_first_name, employee_last_name, employee_email)
VALUES
('John', 'Doe', 'john.doe@example.com'),
('Jane', 'Smith', 'jane.smith@example.com'),
('Alice', 'Brown', 'alice.brown@example.com');

-- Insert into Projects
INSERT INTO Projects(project_code)
VALUES
('PRJ001'),
('PRJ002'),
('PRJ003');

-- Insert into Tasks
INSERT INTO Tasks(task_name)
VALUES
('Development'),
('Testing'),
('Documentation');

-- Insert into TimeTypes
INSERT INTO TimeTypes(time_type_name)
VALUES
('Regular'),
('Overtime'),
('Vacation');

-- Insert into Locations
INSERT INTO Locations(location_name)
VALUES
('Headquarters'),
('Remote'),
('Client Site');

-- Insert into Countries
INSERT INTO Countries(country_name)
VALUES
('United States'),
('Canada'),
('Germany');

-- Insert into ProjectTasks (many-to-many relationship)
INSERT INTO ProjectTasks(project_id, task_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

-- Insert into TimesheetEntries
INSERT INTO TimesheetEntries(employee_id, project_id, task_id, time_type_id, location_id, country_id, entry_date, hours_worked, approval_status, metadata)
VALUES
(1, 1, 1, 1, 1, 1, '2023-06-01', 8.00, 'pending', '{"device": "PC", "timezone": "UTC-5""}'),
(2, 2, 2, 2, 2, 2, '2023-06-02', 8.00, 'pending', '{"device": "iPhone"}'),
(3, 3, 3, 3, 3, 3, '2023-06-03', 4.00, 'pending', '{"device": "Android"}');

INSERT INTO TimesheetEntries(employee_id, project_id, task_id, time_type_id, location_id, country_id, entry_date, hours_worked, approval_status, metadata)
VALUES
(1, 1, 1, 1, 1, 1, '2023-06-01', 8.00, 'pending', '{"device": "PC", "timezone": "UTC-5""}'),
(1, 1, 2, 1, 1, 1, '2023-06-02', 8.00, 'pending', '{"device": "Laptop", "timezone": "UTC-5""}')

go;
--View - selectarea tuturor orelor lucrate pe proiectul PRJ001 a angajatului John Doe

CREATE VIEW TotalHours_PRJ001_JohnDoe
AS
SELECT
    E.employee_first_name,
    E.employee_last_name,
    E.employee_email,
    P.project_code,
    SUM(TSE.hours_worked) AS total_hours_worked
FROM
    TimesheetEntries AS TSE
JOIN
    Employees AS E ON TSE.employee_id = E.employee_id
JOIN
    Projects AS P ON TSE.project_id = P.project_id
WHERE
    E.employee_email = 'john.doe@example.com'
    AND P.project_code = 'PRJ001'
GROUP BY
    E.employee_first_name,
    E.employee_last_name,
    E.employee_email,
    P.project_code;

--View generic pentru selectarea tuturor orelor lucrate pe un anumit proiect al unui anumit angajat
go;

CREATE VIEW EmployeeProjectHours
AS
SELECT
    E.employee_first_name,
    E.employee_last_name,
    E.employee_email,
    P.project_code,
    SUM(TSE.hours_worked) AS total_hours_worked
FROM
    TimesheetEntries AS TSE
JOIN
    Employees AS E ON TSE.employee_id = E.employee_id
JOIN
    Projects AS P ON TSE.project_id = P.project_id
GROUP BY
    E.employee_first_name,
    E.employee_last_name,
    E.employee_email,
    P.project_code;

 go;
SELECT *
FROM EmployeeProjectHours
WHERE employee_email = 'jane.smith@example.com'
  AND project_code = 'PRJ002';

  
  -- o alta varianta mult mai usoara ar fi sa folosim proceduri stocate in care pasam parametri doriti
 

  --Materialized View pentru a vedea numarul total de ore raportat pe un anumit proiect 
SET QUOTED_IDENTIFIER ON;
GO

-- 1. Creează View-ul cu SCHEMABINDING și funcții agregate
CREATE VIEW dbo.ProjectTotalHours_MV
WITH SCHEMABINDING -- -- blocheaza schema tabelelor de baza - nu se poate adauga/modifica/sterge coloane, tipuri de date a tabelelor din indexed view fara a sterge view-ul
AS
SELECT
    P.project_id,
    P.project_code,
    SUM(TSE.hours_worked) AS TotalHoursWorked,
    COUNT_BIG(*) AS NumberOfEntries -- Necesara pentru a putea crea un index clusterizat
FROM
    dbo.Projects AS P
JOIN
    dbo.TimesheetEntries AS TSE ON P.project_id = TSE.project_id
GROUP BY
    P.project_id,
    P.project_code;
GO

-- 2. Creează un Index Unic Clusterizat pe View pentru a-l materializa
CREATE UNIQUE CLUSTERED INDEX IX_ProjectTotalHours_MV_ProjectId
ON dbo.ProjectTotalHours_MV (project_id);
GO


SELECT *
FROM dbo.ProjectTotalHours_MV
WHERE project_code = 'PRJ001'; -- Poți filtra direct pe el


--left join
-- Selectarea tuturor angajatilor care nu au pontari in sistem
SELECT
    Employees.employee_id,
    Employees.employee_first_name,
    Employees.employee_last_name
FROM
    Employees
LEFT JOIN
    TimesheetEntries ON Employees.employee_id = TimesheetEntries.employee_id
where TimesheetEntries.entry_id is NULL


--sa existe cel putin un select asupra structurii cu o functie analitica alta decat row_numb

--suma cumulatiav a orelor lucrate de fiecare angajat pe fiecare proiect.
SELECT
    E.employee_first_name,
    E.employee_last_name,
    P.project_code,
    TSE.entry_date,
    TSE.hours_worked,
    SUM(TSE.hours_worked) OVER (PARTITION BY E.employee_id, P.project_id ORDER BY TSE.entry_date) AS CumulativeHoursForProject
FROM
    Employees AS E
JOIN
    TimesheetEntries AS TSE ON E.employee_id = TSE.employee_id
JOIN
    Projects AS P ON TSE.project_id = P.project_id
ORDER BY
    CumulativeHoursForProject;














