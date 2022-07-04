from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time
from brownie import network
import pytest


def test_can_select_judge(judge_selection_vrf):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    judge_selection_vrf.addJudge(account, {"from": account})

    fund_with_link(judge_selection_vrf)
    case_number = 42
    judge_selection_vrf.selectJudge(case_number, {"from": account})
    time.sleep(1)
    assert judge_selection_vrf.recentWinner() == account
