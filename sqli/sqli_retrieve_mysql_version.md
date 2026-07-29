# SQL Injection Attack, Querying the Database Type and Version on MySQL and Microsoft

**Difficulty:** Practitioner
**Status:** Solved
**Category:** SQL Injection (UNION attack)

## Lab Description

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

**Objective:** Display the database version string.

**Hint:** Useful payloads can be found on the PortSwigger SQL injection cheat sheet.

## Vulnerability

The category filter takes user input (via the `category` parameter) and inserts it directly into a SQL query used to filter products, without sanitization. Because the response reflects data from the query back into the page, a **UNION-based SQL injection** can be used to append an attacker-controlled `SELECT` statement and have its results displayed alongside the normal product listing.

A typical vulnerable query looks like:

```sql
SELECT name, description FROM products WHERE category = '<category>' AND released = 1
```

## Steps to Solve

1. Open Burp Suite and browse the shop application, clicking into a product category so the `category` parameter request can be captured.
2. Send the request to **Repeater**.
3. **Determine the number of columns** returned by the original query. This can be done incrementally with `ORDER BY`, or directly with a UNION payload guessing two text columns:

   ```
   '+UNION+SELECT+'abc','def'#
   ```

   If the category page reflects `abc` and `def` in the listing, the query returns two columns, and both accept text data.

4. **Retrieve the database version** by replacing one of the dummy values with `@@version`:

   ```
   '+UNION+SELECT+@@version,+NULL#
   ```

5. In this solve, the following URL-encoded payload was submitted in the `category` parameter:

   ```
   %27%20UNION%20SELECT%20@@version,NULL--%20
   ```

   Decoded, this is:

   ```
   ' UNION SELECT @@version,NULL-- 
   ```

6. The resulting query on the backend becomes:

   ```sql
   SELECT name, description FROM products
   WHERE category = '' UNION SELECT @@version, NULL-- ' AND released = 1
   ```

   The trailing `--` (followed by a space) comments out the rest of the original query, and the `UNION SELECT` appends a row containing the database version string in place of a product name.

7. The response displays the database version (e.g. `8.0.x-MySQL` or a Microsoft SQL Server version string) in place of a product listing entry, confirming the injection point and column count.
8. The lab is marked as solved once the version string is successfully displayed on the page.

## Root Cause

- User-controlled input (`category`) is concatenated directly into the SQL query.
- No parameterization or input validation/escaping is applied.
- The application reflects query results back into the response, making it possible to exfiltrate arbitrary data via UNION-based injection once the column count and data types are known.

## Key SQLi Techniques Demonstrated

- **Column count / type discovery** using `UNION SELECT 'abc','def'`.
- **Comment termination** (`--` or `#`) to neutralize the remainder of the original query.
- **Database fingerprinting** via `@@version` (MySQL / Microsoft SQL Server) to retrieve the DBMS version string directly through the injected UNION query.

## Remediation

- **Use parameterized queries / prepared statements** for all database access — never concatenate user input into SQL strings.
- Apply the principle of least privilege to the database account used by the application.
- Avoid reflecting raw query output directly into HTML responses without proper encoding.
- Implement a Web Application Firewall (WAF) and input validation as defense-in-depth (not a substitute for parameterized queries).
- Disable detailed database error messages in production to reduce information leakage.

## Payload Used

```
URL-encoded: %27%20UNION%20SELECT%20@@version,NULL--%20
Decoded:     ' UNION SELECT @@version,NULL-- 
```

## Reference

- PortSwigger Web Security Academy: SQL injection attack, querying the database type and version on MySQL and Microsoft
- Related topic: [SQL injection UNION attacks](https://portswigger.net/web-security/sql-injection/union-attacks)
- [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
