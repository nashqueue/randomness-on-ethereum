// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/access/Ownable.sol";

contract JudgeSelectionNprng is Ownable {
    address[] public judges;
    mapping(uint256 => address) public caseToAddress;
    address public recentJudge;
    uint256 public randomness;
    uint256 public recentCase;

    function addJudge(address judge) public onlyOwner {
        judges.push(judge);
    }

    function selectJudge(uint256 caseNumber) public onlyOwner {
        recentCase = caseNumber;

        randomness = uint256(
            keccak256(
                abi.encodePacked(
                    caseNumber, // is preditable
                    msg.sender, //stays the same
                    blockhash(block.number - 1) // is preditable
                )
            )
        );

        uint256 indexOfJudge = randomness % judges.length;
        recentJudge = judges[indexOfJudge];
        caseToAddress[recentCase] = recentJudge;
    }
}
