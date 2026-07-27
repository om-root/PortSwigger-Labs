# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

**Difficulty:** APPRENTICE

## Description

This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:

```sql
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

**Goal:** Perform a SQL injection attack that causes the application to display one or more unreleased products.

## Solution

1. Use Burp Suite to intercept and modify the request that sets the product category filter.
2. Modify the `category` parameter, giving it the value:

   ```
   '+OR+1=1--
   ```

3. Submit the request, and verify that the response now contains one or more unreleased products.

## How it works

The original query filters on both `category` and `released = 1`, so unreleased products are normally hidden. Injecting `' OR 1=1--` transforms the query into:

```sql
SELECT * FROM products WHERE category = '' OR 1=1--' AND released = 1
```

- `OR 1=1` makes the `WHERE` clause always evaluate to true, so every row in the `products` table matches, regardless of category.
- `--` comments out the rest of the original query (`AND released = 1`), removing the restriction that only released products be shown.

As a result, the query returns **all products, including unreleased ones**, solving the lab.

## Key takeaway

Never build SQL queries by concatenating untrusted user input directly into the query string. Use parameterized queries (prepared statements) so that user input is always treated as data, not executable SQL code.
