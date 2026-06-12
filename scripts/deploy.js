import hre from "hardhat";

async function main() {
  const connection = await hre.network.connect("localhost");
  const DegreeContract = await connection.ethers.getContractFactory("DegreeContract");
  const contract = await DegreeContract.deploy();

  await contract.waitForDeployment();

  console.log("DegreeContract deployed to:", contract.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
