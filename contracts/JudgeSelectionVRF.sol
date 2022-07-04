// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract JudgeSelectionVRF is VRFConsumerBase, Ownable {
    address[] public judges;
    mapping(uint256 => address) public caseToAddress;
    address public recentJudge;
    uint256 public randomness;
    uint256 public recentCase;
    enum SELECTION_STATE {
        OPEN,
        SELECTING_WINNER
    }
    SELECTION_STATE public selection_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        selection_state = SELECTION_STATE.OPEN;
        fee = _fee;
        keyhash = _keyhash;
    }

    function addJudge(address judge) public onlyOwner {
        require(selection_state == SELECTION_STATE.OPEN);
        judges.push(judge);
    }

    function selectJudge(uint256 caseNumber) public onlyOwner {
        require(selection_state == SELECTION_STATE.OPEN);
        selection_state = SELECTION_STATE.SELECTING_WINNER;
        recentCase = caseNumber;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            selection_state == SELECTION_STATE.SELECTING_WINNER,
            "You aren't there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indexOfJudge = _randomness % judges.length;
        recentJudge = judges[indexOfJudge];
        caseToAddress[recentCase] = recentJudge;

        selection_state = SELECTION_STATE.OPEN;
        randomness = _randomness;
    }
}
