import os
import json
import hashlib
import qrcode
from web3 import Web3
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration
RPC_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
OWNER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
OWNER_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# Directories
DEGREES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "attested_degrees")
os.makedirs(DEGREES_DIR, exist_ok=True)
TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def compute_degree_hash(student_id: str, program: str, date: str, university: str) -> str:
    """
    Computes deterministic SHA-256 hash: SHA-256(studentId + program + date + university)
    """
    input_str = f"{student_id}{program}{date}{university}"
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()

def broadcast_degree_to_blockchain(degree_hash: str, student_id: str, student_name: str, degree_program: str) -> str:
    """
    Mints/Registers the degree attestation on the local private Hardhat node.
    Returns: transaction hash
    """
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise Exception("Unable to connect to local blockchain node")

    # Load compiled ABI
    config_dir = os.path.dirname(os.path.dirname(__file__))
    abi_path = os.path.join(config_dir, "artifacts", "contracts", "DegreeContract.sol", "DegreeContract.json")
    with open(abi_path, "r") as f:
        artifact = json.load(f)
        abi = artifact["abi"]

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    
    # Check if already issued
    try:
        _, _, _, _, is_valid = contract.functions.verifyDegree(Web3.to_bytes(hexstr=degree_hash)).call()
        if is_valid:
            raise Exception("This degree attestation hash has already been registered on-chain.")
    except Exception:
        # Expected revert if not found, which is what we want
        pass

    # Build Transaction
    nonce = w3.eth.get_transaction_count(OWNER_ADDRESS)
    tx = contract.functions.issueDegree(
        Web3.to_bytes(hexstr=degree_hash),
        student_id,
        student_name,
        degree_program
    ).build_transaction({
        'from': OWNER_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce,
    })

    # Sign Transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=OWNER_PRIVATE_KEY)
    
    # Broadcast Transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    # Wait for receipt
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return w3.to_hex(tx_hash)

def generate_degree_pdf(student_id: str, student_name: str, degree_program: str, passing_date: str, degree_hash: str, tx_hash: str) -> str:
    """
    Generates a high-quality PDF degree certificate containing student metadata
    and an embedded verification QR code linking back to the blockchain hash.
    """
    pdf_filename = f"{degree_hash}.pdf"
    pdf_path = os.path.join(DEGREES_DIR, pdf_filename)
    
    # 1. Generate QR Code
    # Local verification landing page url
    verify_url = f"http://127.0.0.1:8000/?hash={degree_hash}"
    qr = qrcode.QRCode(version=1, box_size=3, border=1)
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_path = os.path.join(TEMP_DIR, f"qr_{degree_hash}.png")
    qr_img.save(qr_path)

    # 2. Build PDF Document (Landscape Certificate style)
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []

    # Custom styling
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor('#10b981'), # Sea Green
        alignment=1 # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CertSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#6b7280'),
        alignment=1 # Center
    )
    
    name_style = ParagraphStyle(
        'CertName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#1f2937'),
        alignment=1 # Center
    )
    
    body_style = ParagraphStyle(
        'CertBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=20,
        textColor=colors.HexColor('#4b5563'),
        alignment=1 # Center
    )
    
    meta_style = ParagraphStyle(
        'CertMeta',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4b5563')
    )

    story.append(Spacer(1, 20))
    story.append(Paragraph("IQRA UNIVERSITY", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("DEGREE ATTESTATION & CREDENTIAL CERTIFICATE", subtitle_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("This is to certify that", body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(student_name, name_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"has successfully completed all requirements for the degree program:", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>{degree_program}</b>", body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"Graduation Date: <b>{passing_date}</b> | Student ID: <b>{student_id}</b>", body_style))
    story.append(Spacer(1, 30))
    
    # 3. Add verification details and QR Code side-by-side using a layout table
    # We will build a simple table to keep QR code on right and block details on left
    from reportlab.platypus import Table, TableStyle
    
    meta_text = (
        f"<b>BLOCKCHAIN SECURED ATTESTATION</b><br/>"
        f"Network: Private Ethereum Localnet (Chain ID 1337)<br/>"
        f"Contract: {CONTRACT_ADDRESS}<br/>"
        f"Degree Hash: {degree_hash}<br/>"
        f"TX Hash: {tx_hash}<br/>"
        f"Scan QR code to verify credential authenticity instantly on-chain."
    )
    
    left_p = Paragraph(meta_text, meta_style)
    right_img = Image(qr_path, width=80, height=80)
    
    table_data = [[left_p, right_img]]
    t = Table(table_data, colWidths=[520, 100])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,0), 15),
    ]))
    
    story.append(t)
    
    # Build
    doc.build(story)
    
    # Cleanup temp QR image
    try:
        os.remove(qr_path)
    except Exception:
        pass
        
    return pdf_path
