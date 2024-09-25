CREATE DATABASE PizzaProject;
USE PizzaProject;
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(40),
    LastName NVARCHAR(40),
    Gender CHAR(1),
    Birthdate DATE,
    Phone NVARCHAR(15),
    AccountID INT FOREIGN KEY 
);
