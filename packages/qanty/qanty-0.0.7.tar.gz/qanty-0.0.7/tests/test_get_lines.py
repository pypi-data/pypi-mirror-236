# -*- coding: UTF-8 -*-
import random

import qanty.common.models as models


def test_get_branch_lines(qanty):
    branches = qanty.get_branches()
    assert isinstance(branches, list)
    if len(branches) > 0:
        random_branch = random.choice(branches)
        lines = qanty.get_lines(branch_id=random_branch.id)
        assert isinstance(lines, list)
        if len(lines) > 0:
            for line in lines:
                assert isinstance(line, models.Line)


def test_get_deleted_lines(qanty):
    branches = qanty.get_branches()
    assert isinstance(branches, list)
    if len(branches) > 0:
        random_branch = random.choice(branches)
        lines = qanty.get_lines(branch_id=random_branch.id, get_deleted=True)
        assert isinstance(lines, list)
        if len(lines) > 0:
            for line in lines:
                assert isinstance(line, models.Line)


# def test_get_custom_branch_lines(qanty):
#     response = qanty.get_lines(custom_branch_id="custom_branch_id")
#     assert isinstance(response, list)


# def test_get_deleted_lines(qanty):
#     response = qanty.get_lines(get_deleted=True)
#     assert isinstance(response, list)
