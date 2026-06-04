-- ============================================================
-- SafeGuard Insurance – Database Validation SQL Queries
-- Tool: DB Browser for SQLite
-- Database: instance/insurance.db
-- Author: Sahil
-- Date: 2025-06-01
-- ============================================================


-- ============================================================
-- SECTION 1: CUSTOMER TABLE VALIDATION
-- ============================================================

-- SQL-001: View all registered customers
-- Purpose: Verify all registered customers exist in the database
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    is_admin,
    created_at
FROM customers
ORDER BY customer_id;


-- SQL-002: Count total customers (excluding admin)
-- Purpose: Verify customer count matches what admin dashboard shows
SELECT COUNT(*) AS total_customers
FROM customers
WHERE is_admin = 0;


-- SQL-003: Check for duplicate emails
-- Purpose: Verify email uniqueness constraint is working
SELECT email, COUNT(*) AS count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;


-- SQL-004: Find admin accounts
-- Purpose: Verify only intended accounts have admin privileges
SELECT customer_id, first_name, last_name, email, is_admin
FROM customers
WHERE is_admin = 1;


-- SQL-005: Check for customers with missing required fields
-- Purpose: Verify no NULL values exist in required columns
SELECT customer_id, email
FROM customers
WHERE first_name IS NULL
   OR last_name  IS NULL
   OR email      IS NULL
   OR password_hash IS NULL;


-- SQL-006: Find customers registered in the last 7 days
-- Purpose: Verify new registrations are being recorded correctly
SELECT customer_id, first_name, last_name, email, created_at
FROM customers
WHERE created_at >= DATE('now', '-7 days')
ORDER BY created_at DESC;


-- ============================================================
-- SECTION 2: POLICY TABLE VALIDATION
-- ============================================================

-- SQL-007: View all policies with customer details
-- Purpose: Verify policies are correctly linked to customers
SELECT
    p.policy_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    p.policy_type,
    p.coverage_amount,
    p.premium_amount,
    p.start_date,
    p.end_date,
    p.status
FROM policies p
JOIN customers c ON p.customer_id = c.customer_id
ORDER BY p.policy_id;


-- SQL-008: Count policies by type
-- Purpose: Verify distribution of policy types
SELECT
    policy_type,
    COUNT(*) AS total_policies,
    AVG(premium_amount) AS avg_premium,
    SUM(coverage_amount) AS total_coverage
FROM policies
GROUP BY policy_type
ORDER BY total_policies DESC;


-- SQL-009: Find policies with end date in the past (should be Expired)
-- Purpose: THIS IS BUG-001 VALIDATION
-- Expected: All policies where end_date < today should show status = 'Expired'
-- Actual Bug: They still show 'Active'
SELECT
    policy_id,
    policy_type,
    end_date,
    status,
    CASE
        WHEN end_date < DATE('now') THEN 'Should be Expired'
        ELSE 'Valid'
    END AS expected_status
FROM policies
WHERE end_date < DATE('now');


-- SQL-010: Find policies where end date is before start date (BUG-009)
-- Purpose: Validate BUG-009 - impossible date ranges
SELECT
    policy_id,
    policy_type,
    start_date,
    end_date,
    status
FROM policies
WHERE end_date < start_date;


-- SQL-011: Find policies with zero or negative premium (BUG-006)
-- Purpose: Validate BUG-006 - $0 premium for coverage under $1000
SELECT
    policy_id,
    policy_type,
    coverage_amount,
    premium_amount,
    status
FROM policies
WHERE premium_amount <= 0;


-- SQL-012: Verify premium calculation accuracy
-- Purpose: Cross-check that stored premium matches expected formula
-- Formula: coverage * rate * (1 + max(0, age-25) * 0.01)
-- Note: age not stored in policies table, this checks for obvious anomalies
SELECT
    policy_id,
    policy_type,
    coverage_amount,
    premium_amount,
    ROUND(coverage_amount * 0.03, 2) AS expected_auto_min_premium
FROM policies
WHERE policy_type = 'Auto'
  AND premium_amount < ROUND(coverage_amount * 0.03, 2);


-- ============================================================
-- SECTION 3: CLAIMS TABLE VALIDATION
-- ============================================================

-- SQL-013: View all claims with policy and customer details
-- Purpose: Full claims audit - verify all data is correctly stored
SELECT
    cl.claim_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.policy_type,
    p.coverage_amount,
    cl.claim_amount,
    cl.claim_reason,
    cl.status,
    cl.created_at,
    cl.updated_at
FROM claims cl
JOIN policies p  ON cl.policy_id   = p.policy_id
JOIN customers c ON p.customer_id  = c.customer_id
ORDER BY cl.claim_id;


-- SQL-014: Count claims by status
-- Purpose: Verify counts match what admin dashboard shows
SELECT
    status,
    COUNT(*) AS total_claims
FROM claims
GROUP BY status
ORDER BY total_claims DESC;


-- SQL-015: Find claims where amount exceeds policy coverage (data integrity)
-- Purpose: Verify no claims exist that exceed their policy coverage
SELECT
    cl.claim_id,
    cl.claim_amount,
    p.coverage_amount,
    cl.claim_amount - p.coverage_amount AS overage
FROM claims cl
JOIN policies p ON cl.policy_id = p.policy_id
WHERE cl.claim_amount > p.coverage_amount;


-- SQL-016: Find claims with very short reason (BUG-004 validation)
-- Purpose: Validate BUG-004 - claim reason under 10 characters accepted
SELECT
    claim_id,
    claim_reason,
    LENGTH(claim_reason) AS reason_length
FROM claims
WHERE LENGTH(claim_reason) < 10;


-- SQL-017: Find claims submitted against expired policies (BUG-001 validation)
-- Purpose: Validate BUG-001 - claims accepted on expired policies
SELECT
    cl.claim_id,
    cl.claim_amount,
    cl.status AS claim_status,
    p.policy_id,
    p.end_date,
    p.status AS policy_status,
    CASE
        WHEN p.end_date < DATE('now') THEN '⚠ CLAIM ON EXPIRED POLICY'
        ELSE 'OK'
    END AS validation_result
FROM claims cl
JOIN policies p ON cl.policy_id = p.policy_id
WHERE p.end_date < DATE('now');


-- SQL-018: Claims submitted today
-- Purpose: Verify real-time claim submission is recorded correctly
SELECT
    claim_id,
    policy_id,
    claim_amount,
    claim_reason,
    status,
    created_at
FROM claims
WHERE DATE(created_at) = DATE('now')
ORDER BY created_at DESC;


-- ============================================================
-- SECTION 4: QUOTES TABLE VALIDATION
-- ============================================================

-- SQL-019: View all quotes
-- Purpose: Verify quote generation is stored correctly
SELECT
    q.quote_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    q.policy_type,
    q.coverage_amount,
    q.quote_amount,
    q.age,
    q.created_at
FROM quotes q
JOIN customers c ON q.customer_id = c.customer_id
ORDER BY q.quote_id;


-- SQL-020: Find quotes with invalid age (BUG-003 validation)
-- Purpose: Validate BUG-003 - quotes generated with age 0 or negative
SELECT
    quote_id,
    policy_type,
    coverage_amount,
    quote_amount,
    age
FROM quotes
WHERE age < 18 OR age > 100;


-- SQL-021: Find quotes with zero premium (BUG-006 validation)
-- Purpose: Validate BUG-006 - $0 premium for coverage under $1000
SELECT
    quote_id,
    policy_type,
    coverage_amount,
    quote_amount AS premium
FROM quotes
WHERE quote_amount = 0;


-- SQL-022: Quotes that were converted to policies
-- Purpose: Verify quote-to-policy conversion rate
SELECT
    q.quote_id,
    q.policy_type,
    q.coverage_amount,
    q.quote_amount,
    CASE
        WHEN p.policy_id IS NOT NULL THEN 'Converted'
        ELSE 'Not Purchased'
    END AS converted
FROM quotes q
LEFT JOIN policies p
    ON q.customer_id   = p.customer_id
   AND q.policy_type   = p.policy_type
   AND q.coverage_amount = p.coverage_amount
ORDER BY q.quote_id;


-- ============================================================
-- SECTION 5: CROSS-TABLE / INTEGRITY CHECKS
-- ============================================================

-- SQL-023: Full customer summary report
-- Purpose: High-level overview of each customer's activity
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(DISTINCT p.policy_id) AS total_policies,
    COUNT(DISTINCT cl.claim_id) AS total_claims,
    COALESCE(SUM(p.premium_amount), 0) AS total_premiums,
    COALESCE(SUM(cl.claim_amount), 0)  AS total_claimed
FROM customers c
LEFT JOIN policies p  ON c.customer_id = p.customer_id
LEFT JOIN claims  cl  ON p.policy_id   = cl.policy_id
WHERE c.is_admin = 0
GROUP BY c.customer_id
ORDER BY total_policies DESC;


-- SQL-024: Find orphaned claims (claims with no matching policy)
-- Purpose: Referential integrity check
SELECT cl.claim_id, cl.policy_id, cl.claim_amount
FROM claims cl
LEFT JOIN policies p ON cl.policy_id = p.policy_id
WHERE p.policy_id IS NULL;


-- SQL-025: Find orphaned policies (policies with no matching customer)
-- Purpose: Referential integrity check
SELECT p.policy_id, p.customer_id, p.policy_type
FROM policies p
LEFT JOIN customers c ON p.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- ============================================================
-- END OF VALIDATION QUERIES
-- Total Queries: 25
-- ============================================================
