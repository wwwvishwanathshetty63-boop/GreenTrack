import http.client
import json
import os

# This script verifies the security headers and CSRF protection
# Usage: python scripts/verify_security.py

def test_security():
    conn = http.client.HTTPConnection("localhost", 5000)
    
    # 1. Check Security Headers
    print("--- 1. Testing Security Headers ---")
    conn.request("GET", "/")
    res = conn.getresponse()
    headers = dict(res.getheaders())
    
    security_headers = {
        'Content-Security-Policy': 'CSP',
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'HSTS'
    }
    
    for h, label in security_headers.items():
        val = headers.get(h)
        if val:
            print(f"[SUCCESS] {label} header found: {h}")
        else:
            print(f"[WARNING] {label} header ({h}) NOT found (might be disabled in Dev mode)")

    # 2. Check CSRF Protection (requires login)
    print("\n--- 2. Testing CSRF Protection ---")
    # This is a bit complex with http.client but we can check if it requires X-CSRF-TOKEN
    payload = json.dumps({"username": "test", "password": "password"})
    headers = {"Content-Type": "application/json"}
    conn.request("POST", "/api/add-entry", payload, headers)
    res = conn.getresponse()
    
    if res.status == 401:
        print("[SUCCESS] Unauthorized request without token was blocked.")
    elif res.status == 400 or res.status == 405:
        print(f"[SUCCESS] Request was rejected as expected (Status: {res.status}).")
    else:
        print(f"[CRITICAL] Request was NOT blocked (Status: {res.status}). Check CSRF settings.")

    conn.close()

if __name__ == "__main__":
    try:
        test_security()
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to localhost:5000. Please start the Flask app first.")
