from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # "user" or "admin"
    is_verified = Column(Boolean, default=False) # 2FA/Email verification state
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    requests = relationship("AttestationRequest", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    cnic_number = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    passport = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")

class AttestationRequest(Base):
    __tablename__ = "attestation_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    degree_program = Column(String, nullable=False)
    
    # Document file paths
    cnic_front_path = Column(String, nullable=True)
    cnic_back_path = Column(String, nullable=True)
    matric_marksheet_path = Column(String, nullable=True)
    inter_marksheet_path = Column(String, nullable=True)
    
    # Payment info
    payment_method = Column(String, nullable=True) # "crypto" or "1link"
    payment_screenshot_path = Column(String, nullable=True)
    crypto_tx_hash = Column(String, nullable=True)
    
    # Status
    status = Column(String, default="pending_documents") # "pending_documents", "pending_payment", "pending_verification", "approved", "rejected"
    rejection_reason = Column(String, nullable=True)
    
    # Attestation outcome
    tx_hash = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="requests")
