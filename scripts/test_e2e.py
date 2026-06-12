import os
import random
import requests

API_URL = "http://127.0.0.1:8000"

def main():
    print("=== STARTING END-TO-END SYSTEM INTEGRATION TEST ===")
    
    # Clean previous SQLite database to ensure fresh role assignment
    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chaincred.db")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attestation_requests")
            cursor.execute("DELETE FROM profiles")
            cursor.execute("DELETE FROM users")
            conn.commit()
            conn.close()
            print("Cleared existing chaincred.db tables for fresh initialization.")
        except Exception as e:
            print(f"Warning: could not clear database tables: {e}")

    # 1. Clean previous SQLite db if needed, or register new credentials
    # Use random email to avoid duplicate user constraints on repeat runs
    rand_suffix = random.randint(1000, 9999)
    admin_email = f"admin_node_{rand_suffix}@iqra.edu.pk"
    student_email = f"student_ali_{rand_suffix}@iqra.edu.pk"
    password = "password123"

    # Helper to register
    def register_and_verify(email):
        print(f"\nRegistering {email}...")
        res = requests.post(f"{API_URL}/api/auth/register", data={
            "email": email,
            "password": password
        })
        if res.status_code != 200:
            print(f"Signup info: {res.json()}")
            # If already exists, we will proceed
            return
        print("Registration successful.")

    register_and_verify(admin_email) # First user registered becomes Admin
    register_and_verify(student_email)

    # 2. Login Student
    print("\nLogging in student...")
    login_res = requests.post(f"{API_URL}/api/auth/login", data={
        "email": student_email,
        "password": password
    })
    assert login_res.status_code == 200
    student_token = login_res.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    print("Student login successful.")

    # 3. Create Student Profile
    print("\nCreating student profile...")
    prof_res = requests.post(f"{API_URL}/api/profile", headers=student_headers, data={
        "first_name": "Ali",
        "last_name": "Hassan",
        "cnic_number": f"42101-{random.randint(1000000, 9999999)}-5",
        "dob": "2001-11-20"
    })
    assert prof_res.status_code == 200
    print("Student profile created.")

    # 4. Upload Documents
    # Create mock files
    print("\nCreating mock document files...")
    mock_files = ["cnic_f.jpg", "cnic_b.jpg", "matric.jpg", "inter.jpg", "receipt.jpg"]
    for f in mock_files:
        with open(f, "wb") as fh:
            fh.write(b"MOCK_IMAGE_DATA")

    print("Uploading student documents...")
    with open("cnic_f.jpg", "rb") as cf, open("cnic_b.jpg", "rb") as cb, open("matric.jpg", "rb") as m, open("inter.jpg", "rb") as i:
        files = {
            "cnic_front": cf,
            "cnic_back": cb,
            "matric_marksheet": m,
            "inter_marksheet": i
        }
        upload_res = requests.post(
            f"{API_URL}/api/attestation/upload",
            headers=student_headers,
            data={"degree_program": "BSCS"},
            files=files
        )
    assert upload_res.status_code == 200
    print("Student documents uploaded successfully.")

    # 5. Submit Payment Screenshot
    print("\nSubmitting payment receipt...")
    with open("receipt.jpg", "rb") as rec:
        pay_res = requests.post(
            f"{API_URL}/api/attestation/payment",
            headers=student_headers,
            data={"payment_method": "crypto"},
            files={"screenshot": rec}
        )
    assert pay_res.status_code == 200
    print("Payment receipt submitted.")

    # Check Student Status
    status_res = requests.get(f"{API_URL}/api/attestation/status", headers=student_headers)
    assert status_res.json()["status"] == "pending_verification"
    print(f"Current request state: {status_res.json()['status']}")

    # 6. Login Admin
    print("\nLogging in admin...")
    admin_login_res = requests.post(f"{API_URL}/api/auth/login", data={
        "email": admin_email,
        "password": password
    })
    assert admin_login_res.status_code == 200
    admin_token = admin_login_res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("Admin login successful.")

    # Get Pending Requests
    requests_res = requests.get(f"{API_URL}/api/admin/requests", headers=admin_headers)
    assert len(requests_res.json()) > 0
    pending_req = requests_res.json()[-1] # Get latest request
    request_id = pending_req["id"]
    print(f"Latest pending request ID: {request_id}")

    # 7. Admin Verify and Attest on Blockchain
    print("\nAdmin running OCR verification and attestation...")
    verify_res = requests.post(f"{API_URL}/api/admin/verify/{request_id}", headers=admin_headers)
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["status"] == "approved"
    
    degree_hash = verify_data["degree_hash"]
    tx_hash = verify_data["tx_hash"]
    print(f"Verification approved!")
    print(f"Attested Degree Hash: {degree_hash}")
    print(f"Blockchain TX Hash: {tx_hash}")

    # 8. Verify Publicly on Blockchain Ledger
    print("\nQuerying public blockchain verification route...")
    pub_verify_res = requests.get(f"{API_URL}/api/verify/{degree_hash}")
    assert pub_verify_res.status_code == 200
    verify_info = pub_verify_res.json()
    assert verify_info["valid"] is True
    print("Verification result: DEGREE IS VALID!")
    print(f"Stored Name: {verify_info['student_name']}")
    print(f"Stored Program: {verify_info['degree_program']}")
    
    # Clean up mock files
    for f in mock_files:
        try:
            os.remove(f)
        except Exception:
            pass

    print("\n=== SYSTEM INTEGRATION TEST COMPLETED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
