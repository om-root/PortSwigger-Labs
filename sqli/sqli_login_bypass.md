# SQL Injection Vulnerability Allowing Login Bypass

**Difficulty:** Apprentice
**Status:** Solved
**Category:** SQL Injection

## Lab Description

This lab contains a SQL injection vulnerability in the login function.

**Objective:** Perform a SQL injection attack that logs in to the application as the `administrator` user.

## Vulnerability

The login function builds a SQL query by directly concatenating the submitted `username` and `password` parameters, without sanitization. This allows an attacker to inject SQL syntax that alters the logic of the query.

A typical vulnerable query looks like:

```sql
SELECT * FROM users WHERE username = '<username>' AND password = '<password>'
```

By injecting SQL comment syntax into the `username` field, the password check can be commented out entirely, allowing authentication as any user without knowing their password.

## Steps to Solve

1. Open Burp Suite and ensure the browser is proxied through it (Burp's browser or a configured proxy).
2. Go to the lab login page and submit the login form with any username and password (e.g. `admin` / `password`).
3. In Burp Suite, switch to **Proxy > HTTP history** and locate the intercepted `POST` request to `/login`.
4. Send the request to **Repeater** (or intercept it live).
5. Modify the `username` parameter to:

   ```
   administrator'--
   ```

   Leave the `password` parameter as any value (it will be ignored due to the comment).

6. Forward/send the modified request.
7. The resulting query on the backend effectively becomes:

   ```sql
   SELECT * FROM users WHERE username = 'administrator'--' AND password = '<anything>'
   ```

   The `--` comments out the rest of the query, so the password check is never evaluated.
8. The application authenticates the request as the `administrator` user, and the session is granted admin access.
9. Load the account page / lab banner to confirm the lab shows as solved.

## Root Cause

- User input is concatenated directly into a SQL query string instead of being parameterized.
- No input validation or escaping is performed on the `username` or `password` fields.
- SQL comment sequences (`--`, `#`, `/* */` depending on DBMS) allow an attacker to truncate the intended query logic.

## Remediation

- **Use parameterized queries / prepared statements** for all database access — never concatenate user input into SQL strings.
- Apply the principle of least privilege to the database account used by the application.
- Use an ORM or query builder that safely handles parameter binding by default.
- Implement input validation as a defense-in-depth measure (not a substitute for parameterization).
- Enable logging/alerting for anomalous login attempts containing SQL metacharacters.

## Payload Used

```
Username: administrator'--
Password: anything
```

## Reference

- PortSwigger Web Security Academy: SQL injection vulnerability allowing login bypass
- Related topic: [SQL injection](https://portswigger.net/web-security/sql-injection)
