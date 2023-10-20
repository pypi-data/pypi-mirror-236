# -*- coding: UTF-8 -*-


def test_qanty(qanty):
    assert isinstance(qanty.company_id, str)
    assert isinstance(qanty.client.headers.get("Authorization"), str)
