from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import JudgeSelectionVRF, network, config, JudgeSelectionNprng
import time

# ====================================================================================================
def deploy_judge_selection_nprng():
    account = get_account()
    judge_selection_nprng = JudgeSelectionNprng.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    time.sleep(1)
    print("Deployed JudgeSeletion NPRNG!")
    return judge_selection_nprng


def enter_judge_selection_nprng():
    account = get_account()
    judge_selection_nprng = JudgeSelectionNprng[-1]
    tx = judge_selection_nprng.addJudge(account, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_nprng.judges(0)} entered the judge_selection!")
    account1 = get_account(1)
    tx = judge_selection_nprng.addJudge(account1, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_nprng.judges(1)} entered the judge_selection!")
    account2 = get_account(2)
    tx = judge_selection_nprng.addJudge(account2, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_nprng.judges(2)} entered the judge_selection!")


def end_judge_selection_nprng():
    account = get_account()
    judge_selection_nprng = JudgeSelectionNprng[-1]

    caseNumber = 1337
    ending_transaction = judge_selection_nprng.selectJudge(
        caseNumber, {"from": account}
    )
    ending_transaction.wait(1)
    time.sleep(1)
    print(
        f"{judge_selection_nprng.recentJudge()} is the new judge for {judge_selection_nprng.recentCase()} !"
    )


# ====================================================================================================


def deploy_judge_selection_vrf():
    account = get_account()
    judge_selection_vrf = JudgeSelectionVRF.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    time.sleep(1)
    print("Deployed JudgeSeletion VRF!")
    return judge_selection_vrf


def enter_judge_selection_vrf():
    account = get_account()
    judge_selection_vrf = JudgeSelectionVRF[-1]
    tx = judge_selection_vrf.addJudge(account, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_vrf.judges(0)} entered the judge_selection!")
    account1 = get_account(1)
    tx = judge_selection_vrf.addJudge(account1, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_vrf.judges(1)} entered the judge_selection!")
    account2 = get_account(2)
    tx = judge_selection_vrf.addJudge(account2, {"from": account})
    tx.wait(1)
    print(f"{judge_selection_vrf.judges(2)} entered the judge_selection!")


def end_judge_selection_vrf():
    account = get_account()
    judge_selection_vrf = JudgeSelectionVRF[-1]
    # fund the contract
    # then end the judge_selection
    tx = fund_with_link(judge_selection_vrf.address)
    tx.wait(1)
    caseNumber = 1
    ending_transaction = judge_selection_vrf.selectJudge(caseNumber, {"from": account})
    ending_transaction.wait(1)
    time.sleep(1)
    print(
        f"{judge_selection_vrf.recentJudge()} is the new judge for {judge_selection_vrf.recentCase()} !"
    )


def main():
    deploy_judge_selection_nprng()
    enter_judge_selection_nprng()
    end_judge_selection_nprng()
    deploy_judge_selection_vrf()
    enter_judge_selection_vrf()
    end_judge_selection_vrf()
