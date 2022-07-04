from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network

import pytest


def test_can_add_judge(judge_selection_vrf):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()

    judge_selection_vrf.addJudge(account, {"from": account})

    assert judge_selection_vrf.judges(0) == account


def test_can_end_lottery(judge_selection_vrf):

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    judge_selection_vrf.addJudge(account, {"from": account})
    fund_with_link(judge_selection_vrf)
    case_number = 42
    judge_selection_vrf.selectJudge(case_number, {"from": account})
    assert judge_selection_vrf.recentCase() == 42


def test_can_pick_judge_correctly(judge_selection_vrf):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    judge_selection_vrf.addJudge(account, {"from": account})
    judge_selection_vrf.addJudge(get_account(index=1), {"from": account})
    judge_selection_vrf.addJudge(get_account(index=2), {"from": account})

    fund_with_link(judge_selection_vrf)
    case_number = 42
    transaction = judge_selection_vrf.selectJudge(case_number, {"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 69
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, judge_selection_vrf.address, {"from": account}
    )
    # 69 % 3 = 0
    print(judge_selection_vrf.recentJudge())
    assert judge_selection_vrf.recentJudge() == account
