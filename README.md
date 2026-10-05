# CodeAlpha_SecureCodingReview
Secure coding review and vulnerability remediation using Python and Bandit.
# Secure Coding Review

## Project Overview

This project demonstrates a secure coding review of a simple Python user registration and login application.

The review focused on identifying common security vulnerabilities, performing static analysis, and applying secure coding practices to remediate the identified issues.

## Technologies Used

- Python
- SQLite
- Bandit
- PBKDF2-HMAC-SHA256
- GitHub

## Project Structure

```text
CodeAlpha_SecureCodingReview/
├── reports/
│   └── security_review.md
├── secure_app/
│   └── app.py
├── vulnerable_app/
│   └── app.py
├── .gitignore
├──README.md
├──requirements.txt
└── screenshots/
│   └── secure_password_hash.png

Security Issues Identified
The initial vulnerable application contained:

1. SQL Injection
User input was directly inserted into SQL queries using string formatting.
This was identified through
Manual code review
Bandit static analysis

2. Plaintext Password Storage
The vulnerable application stored user passwords directly in the database.
This was identified during manual code inspection.

Remediation
The secure version addresses the identified issues by:
Using parameterised SQL queries
Using SQLite placeholders instead of string-based SQL construction
Hashing passwords using PBKDF2-HMAC-SHA256
Generating a unique random salt for each password
Storing the salt together with the derived password hash
Enforcing unique usernames
Security Testing

The vulnerable application was scanned using Bandit and reported two SQL injection-related issues.
The remediated application was then scanned using:
py -m bandit -r secure_app

Final result:
No issues identified.
Final Bandit Results
Severity	Issues
High	0
Medium	0
Low	0
Total	0
Testing

The secure application was tested by:
Registering a test user.
Logging in with the correct credentials.
Verifying that login was successful.
Inspecting the database to confirm that the password was not stored in plaintext.
Running Bandit against the secure application.
Documentation

Detailed findings, risks, recommendations, and remediation steps are available in:
reports/security_review.md

Conclusion
This project demonstrates how manual code review and static analysis can identify security weaknesses and improve application security through secure coding practices.

