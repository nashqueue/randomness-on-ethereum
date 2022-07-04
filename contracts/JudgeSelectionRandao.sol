// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/access/Ownable.sol";

contract JudgeSelectionRandao is Ownable {
    address[] public judges;
    mapping(uint256 => address) public caseToJudge;
    mapping(address => bytes32) public judgeToCommitment;
    mapping(address => uint256) public judgeToBalance;
    address public recentJudge;
    uint256 public randomness;
    uint256 public recentCase;
    uint256 public committmentCount;
    uint256 public secretCount;
    uint256 public blockNumber;
    uint256 public stakeAmount = 10**18;
    enum SELECTION_STATE {
        OPEN,
        COMMITHASH,
        REVEALSECRET
    }
    SELECTION_STATE public selection_state = SELECTION_STATE.OPEN;

    function addJudge(address judge) public onlyOwner {
        require(selection_state == SELECTION_STATE.OPEN);
        judges.push(judge);
    }

    function addBalance() public payable {
        require(selection_state == SELECTION_STATE.OPEN);
        require(
            msg.value + judgeToBalance[msg.sender] >= stakeAmount,
            "Not enough ETH!"
        );
        judgeToBalance[msg.sender] += msg.value;
    }

    function removeBalance() public payable {
        require(selection_state == SELECTION_STATE.OPEN);
        uint256 balance = judgeToBalance[msg.sender];
        judgeToBalance[msg.sender] = 0;
        msg.sender.transfer(judgeToBalance[msg.sender]);
    }

    function selectJudge(uint256 caseNumber) public onlyOwner {
        require(selection_state == SELECTION_STATE.OPEN);
        selection_state = SELECTION_STATE.COMMITHASH;
        recentCase = caseNumber;
        blockNumber = block.number;
    }

    function commitCommitment(bytes32 commitment) public {
        require(selection_state == SELECTION_STATE.COMMITHASH);
        require(judgeToCommitment[msg.sender] == "0");
        require(judgeToBalance[msg.sender] >= stakeAmount);
        judgeToCommitment[msg.sender] = commitment;
        committmentCount++;
    }

    function startReveal() public onlyOwner {
        require(selection_state == SELECTION_STATE.COMMITHASH);
        selection_state = SELECTION_STATE.REVEALSECRET;
        require(committmentCount >= 2);
    }

    function revealSecret(uint256 secret) public {
        require(selection_state == SELECTION_STATE.REVEALSECRET);
        require(judgeToCommitment[msg.sender] != 0);
        require(judgeToBalance[msg.sender] >= stakeAmount);
        require(
            keccak256(abi.encodePacked(secret)) == judgeToCommitment[msg.sender]
        );
        judgeToCommitment[msg.sender] == "0";
        randomness ^= secret;
        secretCount++;
    }

    function stopselection() public onlyOwner {
        require(selection_state == SELECTION_STATE.REVEALSECRET);
        if (block.number - blockNumber > 200) {
            //Slashing TODO
        }
        require(secretCount == committmentCount);
        uint256 indexOfJudge = randomness % judges.length;
        recentJudge = judges[indexOfJudge];
        caseToJudge[recentCase] = recentJudge;

        selection_state = SELECTION_STATE.OPEN;
        secretCount = 0;
        committmentCount = 0;
    }
}
