// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract DegreeContract {
    address public owner;

    struct DegreeInfo {
        string studentId;
        string studentName;
        string degreeProgram;
        uint256 timestamp;
        bool isValid;
    }

    // Maps degree hash (SHA-256) to its corresponding degree info structure
    mapping(bytes32 => DegreeInfo) public degrees;

    event DegreeIssued(bytes32 indexed degreeHash, string studentId, string studentName, string degreeProgram);
    event DegreeRevoked(bytes32 indexed degreeHash);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can execute this action");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Register/Issue a degree attestation hash on the blockchain.
     */
    function issueDegree(
        bytes32 degreeHash,
        string memory studentId,
        string memory studentName,
        string memory degreeProgram
    ) public onlyOwner {
        require(degreeHash != bytes32(0), "Invalid degree hash");
        require(!degrees[degreeHash].isValid, "Degree hash already issued");

        degrees[degreeHash] = DegreeInfo({
            studentId: studentId,
            studentName: studentName,
            degreeProgram: degreeProgram,
            timestamp: block.timestamp,
            isValid: true
        });

        emit DegreeIssued(degreeHash, studentId, studentName, degreeProgram);
    }

    /**
     * @dev Revoke an issued degree hash (e.g. in case of fraud or academic misconduct).
     */
    function revokeDegree(bytes32 degreeHash) public onlyOwner {
        require(degrees[degreeHash].isValid, "Degree hash not found or already invalid");
        
        degrees[degreeHash].isValid = false;
        
        emit DegreeRevoked(degreeHash);
    }

    /**
     * @dev Public verification function to check if a degree hash is valid and retrieve its details.
     */
    function verifyDegree(bytes32 degreeHash) public view returns (
        string memory studentId,
        string memory studentName,
        string memory degreeProgram,
        uint256 timestamp,
        bool isValid
    ) {
        DegreeInfo memory info = degrees[degreeHash];
        require(info.isValid, "Degree hash is invalid or not registered");
        return (info.studentId, info.studentName, info.degreeProgram, info.timestamp, info.isValid);
    }
}
