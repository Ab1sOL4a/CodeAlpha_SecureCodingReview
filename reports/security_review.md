# Secure Coding Review

## 1. Project Overview

This project performs a security review of a simple Python-based user registration and login application.

The purpose of the review is to identify security vulnerabilities through manual code inspection and static analysis, document the risks, and recommend appropriate remediation measures.

**Programming Language:** Python
**Application:** Simple User Registration and Login System
**Database:** SQLite
**Static Analysis Tool:** Bandit

---

## 2. Security Review Methodology

The application was reviewed using two approaches:

1. **Manual Code Review** — Source code was inspected to identify insecure coding practices and potential vulnerabilities.
2. **Static Analysis** — Bandit was used to scan the Python source code for common security issues automatically.

The vulnerable application was tested to confirm that its basic registration and login functionality worked before remediation.

---

## 3. Findings Summary

| ID    | Vulnerability                 | Severity | Detection Method       |
| ----- | ----------------------------- | -------- | ---------------------- |
| SC-01 | SQL Injection in Registration | High     | Manual Review + Bandit |
| SC-02 | SQL Injection in Login        | Critical | Manual Review + Bandit |
| SC-03 | Plaintext Password Storage    | Critical | Manual Review          |

---

## 4. Detailed Findings

### SC-01 — SQL Injection in Registration

**Severity:** High

**Affected Location:** `vulnerable\_app/app.py:29`

**Detection:** Manual Code Review and Bandit

The registration function constructs an SQL query using an f-string:

```python

query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"

cursor.execute(query)

```

User-controlled values are directly inserted into the SQL statement.

### Risk

An attacker may provide specially crafted input that changes the intended SQL query. This could potentially allow unauthorised database operations or manipulation of stored data.

### Bandit Result

Bandit reported:

```text

B608: hardcoded\_sql\_expressions

Possible SQL injection vector through string-based query construction.

```

Bandit assigned **Medium severity** and **Low confidence** to the finding.

### Recommendation

Use parameterised SQL queries instead of directly inserting user input into SQL statements.

---

### SC-02 — SQL Injection in Login

**Severity:** Critical

**Affected Location:** `vulnerable\_app/app.py:45`

**Detection:** Manual Code Review and Bandit

The login function constructs an SQL query using an f-string:

```python

query = f"SELECT \* FROM users WHERE username = '{username}' AND password = '{password}'"

cursor.execute(query)

```

Both the username and password are directly inserted into the SQL statement.

### Risk

An attacker may manipulate the SQL query through specially crafted input. In an authentication system, this could potentially result in authentication bypass or unauthorized access to database records.

### Bandit Result

Bandit reported:

```text

B608: hardcoded\_sql\_expressions

Possible SQL injection vector through string-based query construction.

```

Bandit assigned **Medium severity** and **Low confidence**.

### Recommendation

Use parameterized queries so that user input is treated as data rather than executable SQL syntax.

---

### SC-03 — Plaintext Password Storage

**Severity:** Critical

**Affected Location:** `vulnerable\_app/app.py`

**Detection:** Manual Code Review

The application stores passwords directly in the SQLite database without applying password hashing.

The database schema contains:

```python

password TEXT

```

The registration function also directly stores the supplied password.

### Risk

If the database is accessed by an unauthorized person, users' actual passwords could be exposed. Users may also reuse passwords on other services, increasing the potential impact of a database compromise.

### Recommendation

Passwords should never be stored as plaintext.

A secure password-hashing algorithm such as **Argon2id, bcrypt, or scrypt** should be used. Passwords should be hashed before storage and verified using the appropriate password-verification function during login.

---

## 5. Remediation Plan

The following changes will be implemented in the secure version of the application:

### SQL Injection

Replace string-based SQL queries with parameterized queries.

**Vulnerable:**

```python

query = f"SELECT \* FROM users WHERE username = '{username}' AND password = '{password}'"

cursor.execute(query)

```

**Secure approach:**

```python

query = "SELECT \* FROM users WHERE username = ? AND password = ?"

cursor.execute(query, (username, password))

```

### Password Storage

Replace plaintext password storage with secure password hashing.

The secure version will hash passwords before storing them and verify the supplied password against the stored hash during authentication.

---

## 6. Security Best Practices

The following secure coding practices are recommended:

* Use parameterised queries for database operations.
* Never store passwords in plaintext.
* Use established password-hashing algorithms.
* Validate user
* input.
* Follow the principle of least privilege for database access.
* Avoid exposing sensitive information in error messages.
* Keep dependencies updated.
* Perform regular static and manual security reviews.
* Test security controls after implementing remediation.

---

## 7. Conclusion

The security review identified multiple vulnerabilities in the intentionally vulnerable Python application.

Bandit identified two potential SQL injection vectors caused by string-based SQL query construction. Manual code review additionally identified plaintext password storage.

The next stage of the project is to remediate these vulnerabilities, create a secure version of the application, and retest the application to verify that the security issues have been addressed.

## Remediation Verification

The vulnerable application was modified to address the identified security issues.

### SQL Injection Remediation

The vulnerable application used string-based SQL queries that allowed user input to be directly inserted into SQL statements.

The secure version uses parameterised SQL queries with SQLite placeholders (`?`). User input is passed separately from the SQL statement, reducing the risk of SQL injection.

### Password Storage Remediation

The vulnerable application stored user passwords in plaintext.

The secure version stores passwords using PBKDF2-HMAC-SHA256 with a randomly generated 16-byte salt. The stored value contains the salt and derived password hash rather than the original password.

### Final Static Analysis

Bandit was run against the secure application using:

`py -m bandit -r secure_app`

Result:

- High severity issues: 0
- Medium severity issues: 0
- Low severity issues: 0
- Total issues: 0
- Result: **No issues identified**

The successful scan confirms that Bandit did not identify the previously detected SQL injection patterns in the remediated application.

### Limitations

Static analysis does not guarantee that an application is completely free from security vulnerabilities. Manual code review and appropriate security testing should also be performed as part of a complete secure development process.
