# -*- coding: UTF-8 -*-

import qanty.common.models as models


def test_get_branches(qanty):
    response = qanty.get_branches()
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, models.Branch)


def test_get_deleted_branches(qanty):
    response = qanty.get_branches(get_deleted=True)
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, models.Branch)


def test_get_branches_with_filters(qanty):
    response = qanty.get_branches(filters={"branch_groups": ["group1", "group2"]})
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, models.Branch)
