# -*- coding: UTF-8 -*-

import datetime

import qanty.common.models as models


def test_list_day_appointments_schedule(qanty):
    branches = qanty.get_branches()
    assert isinstance(branches, list)
    if len(branches) > 0:
        for branch in branches:
            lines = qanty.get_lines(branch_id=branch.id, get_deleted=True)
            assert isinstance(lines, list)
            if len(lines) == 0:
                continue

            for line in lines:
                if len(line.appointment_settings.sets) == 0:
                    continue

                appointments = qanty.list_day_appointments_schedule(
                    branch_id=branch.id,
                    line_id=line.id,
                    day=datetime.datetime.now().strftime("%Y-%m-%d"),
                )
                assert isinstance(appointments, list)

                break
            
            break
