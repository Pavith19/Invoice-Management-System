-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS INVOICES;

-- Switch to the INVOICES database
USE INVOICES;

-- Create the invoices_list table
CREATE TABLE invoices_list (
  INVOICE_NO INT(11) AUTO_INCREMENT PRIMARY KEY,  
  CUSTOMER_NAME VARCHAR(24),                     
  PHONE_NUMBER VARCHAR(15),                      
  DATE DATE,                                     
  INVOICE_TOTAL FLOAT                           
);
