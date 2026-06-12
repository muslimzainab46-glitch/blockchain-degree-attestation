import json
from web3 import Web3

def main():
    # 1. Connect to the local node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    
    if not w3.is_connected():
        print("Failed to connect to local blockchain node.")
        return
        
    print("Connected to blockchain node successfully.")
    print(f"Block number: {w3.eth.block_number}")
    
    # 2. Load the contract ABI
    with open('artifacts/contracts/DegreeContract.sol/DegreeContract.json', 'r') as f:
        artifact = json.load(f)
        abi = artifact['abi']
        
    # 3. Contract address (from deploy script output)
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    
    # 4. Instantiate the contract
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # 5. Call owner() function
    owner = contract.functions.owner().call()
    print(f"Contract owner: {owner}")

if __name__ == '__main__':
    main()
