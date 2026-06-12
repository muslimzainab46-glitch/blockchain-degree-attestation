import traceback
from backend import attestor

try:
    print("Testing attestation...")
    tx_hash = attestor.broadcast_degree_to_blockchain(
        degree_hash="2f6551c6b3d230e9131aa74179a7be19581080af3a4593299dc89352c3d22aee",
        student_id="42101-9988776-5",
        student_name="Ali Hassan",
        degree_program="BSCS"
    )
    print(f"Attestation successful! TX Hash: {tx_hash}")
except Exception as e:
    traceback.print_exc()
