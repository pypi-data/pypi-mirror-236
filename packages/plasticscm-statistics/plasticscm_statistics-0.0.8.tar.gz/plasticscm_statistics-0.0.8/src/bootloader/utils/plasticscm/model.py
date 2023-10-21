# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import re
from os import PathLike
from pathlib import Path
from typing import Any

from majormode.perseus.model.date import ISO8601DateTime
from majormode.perseus.utils import cast


class Changeset:
    """
    A changeset describes the exact differences between two successive
    versions in the version control system's repository of changes.
    Changesets are typically treated as an atomic unit, an indivisible set,
    by version control systems.
    """
    CSV_FIELD_INDEX_OWNER = 0
    CSV_FIELD_INDEX_DATE = 1
    CSV_FIELD_INDEX_CHANGESET_ID = 2

    # REGEX_PATTERN_PLASTIC_SCM_TIMESTAMP = r'^(?P<month>[1-9]|1[0-9])\/(?P<day>[1-9]|[1-2][0-9]|3[01])\/(?P<year>2[0-9]{3})\s(?P<hour>[0-9]|1[0-2]):(?P<minute>[0-5][0-9]):(?P<second>[0-5][0-9])(?P<meridiem>AM|PM)$'
    REGEX_PATTERN_PLASTIC_SCM_TIMESTAMP = r'^(?P<month>\d{1,2})\/(?P<day>\d{1,2})\/(?P<year>\d{4})\s(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})(?P<meridiem>AM|PM)?$'
    REGEX_PLASTIC_SCM_TIMESTAMP = re.compile(REGEX_PATTERN_PLASTIC_SCM_TIMESTAMP)

    @classmethod
    def __cast_stringified_timestamp_to_iso8601(cls, timestamp: str) -> ISO8601DateTime:
        """
        10/18/2023

        :param timestamp:

        :return:
        """
        match = cls.REGEX_PLASTIC_SCM_TIMESTAMP.match(timestamp)
        if match is None:
            raise ValueError(f"Invalid timestamp '{timestamp}'")

        day = match.group('day')
        month = match.group('month')
        year = match.group('year')

        hours = int(match.group('hour'))
        minutes = match.group('minute')
        seconds = match.group('second')

        meridiem = match.group('meridiem')

        if meridiem == 'AM' and hours == 12:
            hours = '0'
        elif meridiem == 'PM' and hours < 12:
            hours = str(int(hours) + 12)

        stringified_iso_8601_timestamp = f'{year}-{month:>02}-{day:>02}T{hours:>02}:{minutes}:{seconds}'

        return cast.string_to_timestamp(stringified_iso_8601_timestamp)

    def __init__(
            self,
            repository_name: str,
            owner: str,
            date: ISO8601DateTime,
            changeset_id: int):
        self.__repository_name = repository_name
        self.__owner = owner
        self.__date = date
        self.__changeset_id = changeset_id
        self.__details = None

    @property
    def changeset_id(self) -> int:
        return self.__changeset_id

    @property
    def date(self) -> ISO8601DateTime:
        return self.__date

    @property
    def details(self) -> ChangesetDetail:
        return self.__details

    @details.setter
    def details(self, details: ChangesetDetail) -> None:
        if self.__details is not None:
            raise ValueError(f"The changeset {self.__changeset_id} has already details defined")
        self.__details = details

    @classmethod
    def from_csv(cls, repository_name: str, payload: Any) -> Changeset or None:
        return payload and Changeset(
            repository_name,
            payload[cls.CSV_FIELD_INDEX_OWNER],
            # cls.__cast_stringified_timestamp_to_iso8601(payload[cls.CSV_FIELD_INDEX_DATE]),
            cast.string_to_timestamp(payload[cls.CSV_FIELD_INDEX_DATE]),
            int(payload[cls.CSV_FIELD_INDEX_CHANGESET_ID])
        )

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def repository_name(self) -> str:
        return self.__repository_name


class ChangesetDetail:
    CSV_FIELD_INDEX_FILE_PATH = 0
    CSV_FIELD_INDEX_FILE_TYPE = 1
    CSV_FIELD_INDEX_FILE_SIZE = 2

    def __init__(
            self,
            file_path: PathLike,
            file_type: str,
            file_size: int
    ):
        self.__file_path = file_path
        self.__file_type = file_type
        self.__file_size = file_size

    @property
    def file_path(self) -> PathLike:
        return self.__file_path

    @property
    def file_size(self) -> int:
        return self.__file_size

    @property
    def file_type(self) -> str:
        return self.__file_type

    @classmethod
    def from_csv(cls, payload: Any) -> ChangesetDetail:
        return payload and ChangesetDetail(
            Path(payload[cls.CSV_FIELD_INDEX_FILE_PATH]),
            payload[cls.CSV_FIELD_INDEX_FILE_TYPE],
            int(payload[cls.CSV_FIELD_INDEX_FILE_SIZE])
        )
