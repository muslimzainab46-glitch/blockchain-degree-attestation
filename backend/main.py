import os
import shutil
import json
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

from .database import engine, get_db, Base
from . import models, auth, verifier, attestor

# Initialize tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChainCred Backend API", version="1.0.0")

# Setup CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload paths
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
DEGREES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "attested_degrees")
os.makedirs(DEGREES_DIR, exist_ok=True)

# 1. AUTHENTICATION ENDPOINTS

@app.post("/api/auth/register")
def register(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Email domain validation
    if not email.endswith("@iqra.edu.pk"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is restricted to @iqra.edu.pk email domains."
        )
        
    # Check duplicate
    user_exists = db.query(models.User).filter(models.User.email == email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this email already exists."
        )

    # First user registered, any email containing 'admin', or 'zainab@iqra.edu.pk' gets Admin role for testing convenience
    count = db.query(models.User).count()
    if count == 0 or "admin" in email.lower() or email.lower() == "zainab@iqra.edu.pk":
        role = "admin"
    else:
        role = "user"

    hashed_pw = auth.get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed_pw, role=role, is_verified=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": f"Account created successfully as {role}.", "role": role}

@app.post("/api/auth/verify-2fa")
def verify_2fa(code: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    # Simulate a validation code
    if code != "123456":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 2FA/verification code."
        )
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    user.is_verified = True
    db.commit()
    return {"message": "Email/2FA verified successfully."}

@app.post("/api/auth/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "email": user.email}

# 2. STUDENT PROFILE & UPLOAD ENDPOINTS

@app.get("/api/profile")
def get_profile(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        return {"has_profile": False}
    return {
        "has_profile": True,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "cnic_number": profile.cnic_number,
        "dob": profile.dob,
        "passport": profile.passport
    }

@app.post("/api/profile")
def create_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    cnic_number: str = Form(...),
    dob: str = Form(...),
    passport: str = Form(None),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if profile:
        profile.first_name = first_name
        profile.last_name = last_name
        profile.cnic_number = cnic_number
        profile.dob = dob
        profile.passport = passport
    else:
        profile = models.Profile(
            user_id=current_user.id,
            first_name=first_name,
            last_name=last_name,
            cnic_number=cnic_number,
            dob=dob,
            passport=passport
        )
        db.add(profile)
    db.commit()
    return {"message": "Profile updated successfully."}

@app.post("/api/attestation/upload")
async def upload_documents(
    degree_program: str = Form(...),
    cnic_front: UploadFile = File(...),
    cnic_back: UploadFile = File(...),
    matric_marksheet: UploadFile = File(...),
    inter_marksheet: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Check profile exists
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your personal profile first before uploading documents."
        )

    # Save files helper
    def save_file(uploaded_file: UploadFile, prefix: str) -> str:
        ext = os.path.splitext(uploaded_file.filename)[1]
        filename = f"{current_user.id}_{prefix}{ext}"
        dest_path = os.path.join(UPLOAD_DIR, filename)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(uploaded_file.file, f)
        return filename

    fn_cnic_front = save_file(cnic_front, "cnic_front")
    fn_cnic_back = save_file(cnic_back, "cnic_back")
    fn_matric = save_file(matric_marksheet, "matric")
    fn_inter = save_file(inter_marksheet, "inter")

    # Save Request
    req = db.query(models.AttestationRequest).filter(
        models.AttestationRequest.user_id == current_user.id,
        models.AttestationRequest.status.in_(["pending_documents", "pending_payment", "rejected"])
    ).first()

    if not req:
        req = models.AttestationRequest(user_id=current_user.id)
        db.add(req)

    req.degree_program = degree_program
    req.cnic_front_path = fn_cnic_front
    req.cnic_back_path = fn_cnic_back
    req.matric_marksheet_path = fn_matric
    req.inter_marksheet_path = fn_inter
    req.status = "pending_payment"
    req.rejection_reason = None
    
    db.commit()
    return {"message": "Documents uploaded successfully. Awaiting fee payment."}

@app.post("/api/attestation/payment")
async def submit_payment(
    payment_method: str = Form(...),
    screenshot: UploadFile = File(...),
    crypto_tx_hash: Optional[str] = Form(None),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(models.AttestationRequest).filter(
        models.AttestationRequest.user_id == current_user.id,
        models.AttestationRequest.status == "pending_payment"
    ).first()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No attestation request waiting for payment."
        )

    # Save screenshot
    ext = os.path.splitext(screenshot.filename)[1]
    filename = f"{current_user.id}_payment{ext}"
    dest_path = os.path.join(UPLOAD_DIR, filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(screenshot.file, f)

    req.payment_method = payment_method
    req.payment_screenshot_path = filename
    if crypto_tx_hash:
        req.crypto_tx_hash = crypto_tx_hash
    req.status = "pending_verification"
    db.commit()
    
    return {"message": "Payment receipt submitted successfully. Your request is now in queue for verification."}

@app.get("/api/attestation/status")
def get_status(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    req = db.query(models.AttestationRequest).filter(models.AttestationRequest.user_id == current_user.id).order_by(models.AttestationRequest.created_at.desc()).first()
    if not req:
        return {"has_request": False}
        
    return {
        "has_request": True,
        "degree_program": req.degree_program,
        "status": req.status,
        "rejection_reason": req.rejection_reason,
        "tx_hash": req.tx_hash,
        "pdf_name": os.path.basename(req.pdf_path) if req.pdf_path else None,
        "created_at": req.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

# 3. ADMIN MANAGEMENT ENDPOINTS

@app.get("/api/admin/requests")
def list_pending_requests(admin: models.User = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    requests = db.query(models.AttestationRequest).all()
    out = []
    for r in requests:
        prof = db.query(models.Profile).filter(models.Profile.user_id == r.user_id).first()
        name = f"{prof.first_name} {prof.last_name}" if prof else "Unknown User"
        out.append({
            "id": r.id,
            "student_name": name,
            "degree_program": r.degree_program,
            "status": r.status,
            "payment_method": r.payment_method,
            "cnic_front": r.cnic_front_path,
            "cnic_back": r.cnic_back_path,
            "matric_marksheet": r.matric_marksheet_path,
            "inter_marksheet": r.inter_marksheet_path,
            "payment_screenshot": r.payment_screenshot_path,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return out

@app.post("/api/admin/verify/{request_id}")
def verify_and_attest(request_id: int, admin: models.User = Depends(auth.get_current_admin), db: Session = Depends(get_db)):
    req = db.query(models.AttestationRequest).filter(models.AttestationRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")
    if req.status != "pending_verification":
        raise HTTPException(status_code=400, detail="Request is not ready for verification.")

    prof = db.query(models.Profile).filter(models.Profile.user_id == req.user_id).first()
    if not prof:
        raise HTTPException(status_code=400, detail="Student profile is missing.")

    # 1. OCR verification
    cnic_full_path = os.path.join(UPLOAD_DIR, req.cnic_front_path)
    inter_full_path = os.path.join(UPLOAD_DIR, req.inter_marksheet_path)
    
    is_valid, reason = verifier.verify_documents(cnic_full_path, inter_full_path)
    
    if not is_valid:
        req.status = "rejected"
        req.rejection_reason = reason
        db.commit()
        return {"status": "rejected", "detail": reason}

    # 2. Valid - Attest on Blockchain
    # Compute Hash
    today_str = datetime.now().strftime("%Y-%m-%d")
    deg_hash = attestor.compute_degree_hash(
        student_id=prof.cnic_number, # using CNIC as ID
        program=req.degree_program,
        date=today_str,
        university="Iqra University"
    )

    try:
        # Broadcast Hash to Contract
        student_fullname = f"{prof.first_name} {prof.last_name}"
        tx_hash = attestor.broadcast_degree_to_blockchain(
            degree_hash=deg_hash,
            student_id=prof.cnic_number,
            student_name=student_fullname,
            degree_program=req.degree_program
        )
        
        # 3. Generate PDF + QR Code
        pdf_path = attestor.generate_degree_pdf(
            student_id=prof.cnic_number,
            student_name=student_fullname,
            degree_program=req.degree_program,
            passing_date=today_str,
            degree_hash=deg_hash,
            tx_hash=tx_hash
        )

        req.status = "approved"
        req.tx_hash = tx_hash
        req.pdf_path = pdf_path
        db.commit()
        
        return {
            "status": "approved",
            "detail": "Documents verified successfully and degree attested on-chain.",
            "tx_hash": tx_hash,
            "degree_hash": deg_hash
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Blockchain attestation failed: {str(e)}")

# 4. PUBLIC VERIFICATION ROUTE

@app.get("/api/verify/{degree_hash}")
def verify_hash_public(degree_hash: str):
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider(attestor.RPC_URL))
    if not w3.is_connected():
        raise HTTPException(status_code=500, detail="Cannot connect to blockchain ledger.")

    # Load ABI
    config_dir = os.path.dirname(os.path.dirname(__file__))
    abi_path = os.path.join(config_dir, "artifacts", "contracts", "DegreeContract.sol", "DegreeContract.json")
    with open(abi_path, "r") as f:
        artifact = json.load(f)
        abi = artifact["abi"]

    contract = w3.eth.contract(address=attestor.CONTRACT_ADDRESS, abi=abi)
    
    try:
        student_id, student_name, degree_program, timestamp, is_valid = contract.functions.verifyDegree(
            Web3.to_bytes(hexstr=degree_hash)
        ).call()
        
        if not is_valid:
            return {"valid": False, "status": "revoked"}
            
        dt_object = datetime.fromtimestamp(timestamp)
        date_str = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "valid": True,
            "status": "valid",
            "student_id": student_id,
            "student_name": student_name,
            "degree_program": degree_program,
            "attested_at": date_str
        }
    except Exception:
        return {"valid": False, "status": "not_found"}

# Serve Frontend Website
@app.get("/")
def serve_frontend():
    config_dir = os.path.dirname(os.path.dirname(__file__))
    html_path = os.path.join(config_dir, "blockchain_degree_attestation_website.html")
    return FileResponse(html_path)



# Mount Static Folders
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/degrees", StaticFiles(directory=DEGREES_DIR), name="degrees")
