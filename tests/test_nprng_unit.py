from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network
from web3 import Web3
import pytest

# =================================================================================================================
def test_can_add_judge(judge_selection_nprng):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()

    judge_selection_nprng.addJudge(account, {"from": account})

    assert judge_selection_nprng.judges(0) == account


def test_can_pick_judge_correctly(judge_selection_nprng):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    judge_selection_nprng.addJudge(account, {"from": account})
    judge_selection_nprng.addJudge(get_account(index=1), {"from": account})
    judge_selection_nprng.addJudge(get_account(index=2), {"from": account})

    case_number = 42
    blockhash = Web3.eth.get_block("latest")["hash"]
    result = Web3.soliditySha3(
        ["uint256", "address", "address"], [case_number, account, blockhash]
    )
    print(blockhash)
    judge_selection_nprng.selectJudge(case_number, {"from": account})
    print(judge_selection_nprng.randomness())
    assert judge_selection_nprng.randomness() == result


#
