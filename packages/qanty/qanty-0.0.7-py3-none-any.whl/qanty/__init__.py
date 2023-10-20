# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

import httpx
from dateutil.parser import parse

import qanty.common.models as models


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Qanty:
    __url = "https://qanty.com/api"

    def __init__(self, auth_token: str, company_id: str) -> None:
        headers = {"Authorization": auth_token}
        self.client = httpx.Client(http2=True, headers=headers)
        self.company_id = company_id

    def __del__(self) -> None:
        self.client.close()

    def get_branches(self, filters: Optional[dict] = None, get_deleted: Optional[bool] = False) -> Optional[List[models.Branch]]:
        """
        Retrieves a list of branches for the company associated with this Qanty instance.

        :param filters: A dictionary of filters to apply to the branch list. Optional.
        :param get_deleted: Whether to include deleted branches in the list. Optional.
        :return: A list of Branch objects representing the branches for the company, or None if an error occurred.
        """
        url = f"{self.__url}/company/get_branches"
        try:
            response = self.client.post(url, json={"company_id": self.company_id, "filters": filters, "get_deleted": get_deleted})
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        sites = data.get("sites", [])
        output: List[models.Branch] = [models.Branch.model_validate(item) for item in sites]
        return output

    def get_lines(
        self, branch_id: str, custom_branch_id: Optional[str] = None, get_deleted: Optional[bool] = False
    ) -> Optional[List[models.Line]]:
        """
        Retrieves a list of lines for a given branch ID.

        Args:
            branch_id (str): The ID of the branch to retrieve lines for.
            custom_branch_id (Optional[str], optional): The custom ID of the branch to retrieve lines for. Defaults to None.
            get_deleted (Optional[bool], optional): Whether to include deleted lines in the response. Defaults to False.

        Returns:
            Optional[List[models.Line]]: A list of Line objects representing the lines in the branch, or None if an error occurred.
        """
        url = f"{self.__url}/branches/get_lines"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "custom_branch_id": custom_branch_id,
                    "get_deleted": get_deleted,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            logger.error(f"Error retrieving lines for branch {branch_id}: {data.get('msg')}")
            return None

        lines = data.get("lines", [])
        output: List[models.Line] = [models.Line.model_validate(item) for item in lines]
        return output

    def list_day_appointments_schedule(
        self, branch_id: str, line_id: str, day: str, custom_branch_id: Optional[str] = None
    ) -> Optional[List[models.AppointmentDaySchedule]]:
        """
        Retrieve the day schedule for a given branch and line on a specific day.

        Args:
            branch_id (str): The ID of the branch to retrieve the schedule for.
            line_id (str): The ID of the line to retrieve the schedule for.
            day (str): The day to retrieve the schedule for, in the format "YYYY-MM-DD".
            custom_branch_id (Optional[str], optional): The ID of a custom branch to retrieve the schedule for. Defaults to None.

        Returns:
            Optional[List[models.DaySchedule]]: A list of DaySchedule objects representing the appointments scheduled for the given branch and line on the given day, or None if an error occurred.
        """
        url = f"{self.__url}/appointments/list_day_schedule"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "line_id": line_id,
                    "day": day,
                    "custom_branch_id": custom_branch_id,
                },
            )
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        if data.get("success") is False:
            logger.error(f"Error retrieving day schedule for branch '{branch_id}' and line '{line_id}': {data.get('msg')}")
            return None

        appointments = data.get("appointments", {})

        output: List[models.AppointmentDaySchedule] = []
        for date, slots in appointments.items():
            entry = {"date_time": parse(date), "slots": []}
            for index, details in slots.items():
                entry["slots"].append({"index": index, **details})
                try:
                    output.append(models.AppointmentDaySchedule.model_validate(entry))
                except Exception:
                    logger.error(f"Error validating appointment day schedule entry: {entry}")
                    continue

        return output

    def list_day_orders_schedule(
        self, branch_id: str, line_id: str, day: str, custom_branch_id: Optional[str] = None
    ) -> Optional[List[models.AppointmentDaySchedule]]:
        pass
