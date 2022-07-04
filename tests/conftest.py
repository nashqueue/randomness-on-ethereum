from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network
from scripts.deploy_judge_selection import (
    deploy_judge_selection_vrf,
    deploy_judge_selection_nprng,
)
import pytest


@pytest.fixture()
def judge_selection_vrf():
    return deploy_judge_selection_vrf()


@pytest.fixture()
def judge_selection_nprng():
    return deploy_judge_selection_nprng()
