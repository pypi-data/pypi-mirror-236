#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import argparse

from majormode.perseus.constant.logging import LOGGING_LEVEL_LITERAL_STRINGS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.model.date import ISO8601DateTime
from majormode.perseus.utils.logging import DEFAULT_LOGGING_FORMATTER
from majormode.perseus.utils.logging import cast_string_to_logging_level
from majormode.perseus.utils.logging import set_up_logger

from src.bootloader.utils.plasticscm import reporting


def parse_arguments() -> argparse.Namespace:
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: An instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description="Plastic SCM repository activities reporting")

    parser.add_argument(
        '--server',
        dest='plasticscm_server_address',
        metavar='NAME',
        required=False,
        help="specify the Plastic SCM server to connect to"
    )

    parser.add_argument(
        '--logging-level',
        dest='logging_level',
        metavar='LEVEL',
        required=False,
        default=str(LoggingLevelLiteral.info),
        type=cast_string_to_logging_level,
        help=f"specify the logging level ({', '.join(LOGGING_LEVEL_LITERAL_STRINGS)})"
    )

    return parser.parse_args()


def run():
    arguments = parse_arguments()

    set_up_logger(
        logging_formatter=DEFAULT_LOGGING_FORMATTER,
        logging_level=arguments.logging_level
    )

    plastic_scm_version = reporting.get_cm_version()
    print(plastic_scm_version)

    available_repositories = reporting.get_available_repositories(
        server_address=arguments.plasticscm_server_address
    )

    for repository_name in available_repositories:
        changesets = reporting.get_changeset_history(
            repository_name,
            end_date=ISO8601DateTime.now(),
            include_details=True
        )

