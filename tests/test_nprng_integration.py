from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time
from brownie import network
import pytest


def test_can_select_judge(judge_selection_nprng):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    judge_selection_nprng.addJudge(account, {"from": account})

    case_number = 1337
    judge_selection_nprng.selectJudge(case_number, {"from": account})
    time.sleep(1)
    assert judge_selection_nprng.recentWinner() == account
