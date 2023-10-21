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

import json
import logging
import subprocess
from collections import defaultdict

from majormode.perseus.model.date import ISO8601DateTime

from src.bootloader.utils.plasticscm.model import Changeset, ChangesetDetail


def get_cm_version() -> str:
    command_line = ['cm', 'version']

    logging.debug(f"Running the command line '{' '.join(command_line)}'...")
    result = subprocess.run(
        command_line,
        capture_output=True,
        text=True
    )

    if result.returncode > 0:
        raise Exception(result.stderr)

    return result.stdout.strip()


def get_available_repositories(server_address: str = None) -> list[str]:
    """
    Return the list of available repositories.

    The Plastic SCM server address is also known as the "repository server
    spec" (``repserverspec``).  It can be represented with the string
    ``repserver:name:port``. For examples:

    ```text
    repserver:skull:8084
    skull:8084
    ```

    Plastic SCM call it "repository server spec", instead of just "server
    spec" for historical reasons.  Long ago, they had separate workspace
    and repository servers, and the naming survived.


    :param server_address The hostname and port of the Plastic SCM server
        to connect to and return the list of available repositories.  When
        not defined, the default server is used, i.e., the server
        configured in the configuration wizard and is written in the local
        ``client.conf`` file.


    :return: An array of the names of available repositories.
    """
    command_line = ['cm', 'repository', 'list']
    if server_address is not None:
        command_line.append(server_address)

    logging.debug(f"Running the command line '{' '.join(command_line)}'...")
    result = subprocess.run(
        command_line,
        capture_output=True,
        text=True
    )

    if result.returncode > 0:
        raise Exception(result.stderr)

    return result.stdout.strip().split('\n')


# Fetch commit history
def get_changeset_history(
        repository_name: str,
        end_date: ISO8601DateTime = None,
        include_details: bool = False,
        start_date: ISO8601DateTime = None,
) -> list[(str, str, str)]:
    """
    Return a history of changesets from the specified repository.


    :param repository_name: The name of the Plastic SCM repository to
        return the changeset history.

    :param end_date: The latest date of changesets to return.  This date
        is exclusive, so changesets that were made at this date are not
        returned.

    :param include_details: Indicate to return the details of each
        changeset.

    :param start_date: The earliest date of changesets to return.  This
        date is inclusive, so changesets that were made at this date are
        returned.


    :return: A list of tuple ``(owner, date, changeset_id)``.
    """
    command_line = ['cm', 'find', 'changeset']

    if start_date or end_date:
        filters = []
        if start_date:
            filters.append(f"date >= '{start_date}'")
        if end_date:
            filters.append(f"date < '{end_date}'")

        where_section = f"where {' and '.join(filters)}"
        command_line.append(where_section)

    command_line.extend(['on', 'repository', f"'{repository_name}'"])
    command_line.append('--format={owner};{date};{changesetid}')
    # command_line.append('--dateformat="yyyy-MM-dd HH:mm:ss"')
    command_line.append('--nototal')

    shell_command_line = ' '.join(command_line)
    logging.debug(f"Running the command line '{shell_command_line}'...")

    result = subprocess.run(
        command_line,
        capture_output=True,
        text=True
    )

    if result.returncode > 0:
        raise Exception(result.stderr)

    changeset_records = result.stdout.strip().split('\n')

    changesets = [
        Changeset.from_csv(
            repository_name,
            record.replace('"', '').split(';')
        )
        for record in changeset_records
    ]

    if include_details:
        for changeset in changesets:
            changeset.details = get_changeset_details(changeset)

    return changesets


# Fetch changed files and lines in a commit
def get_changeset_details(changeset: Changeset):
    command_line = ['cm', 'find', 'revisions']
    command_line.append(f"where changeset={changeset.changeset_id} and type!='dir'")
    command_line.extend(['on', 'repository', f"'{changeset.repository_name}'"])
    command_line.append('--format={item};{type};{size}')
    command_line.append('--nototal')

    logging.debug(f"Running the command line '{' '.join(command_line)}'...")
    result = subprocess.run(
        command_line,
        capture_output=True,
        text=True
    )

    if result.returncode > 0:
        raise Exception(result.stderr)

    changeset_detail_records = result.stdout.strip().split('\n')

    changeset_details = [
        ChangesetDetail.from_csv(record.split(';'))
        for record in changeset_detail_records
        if record != ''
    ]

    return changeset_details


# Main script starts here
if __name__ == '__main__':
    commits = get_changeset_history()
    dev_stats = defaultdict(list)

    for commit in commits:
        owner, date, changeset_id = commit.split(';')
        date = date.split(' ')[0]  # Only keep the date part, remove time
        changeset_id = int(changeset_id)

        commit_details = get_changeset_details(changeset_id)

        file_changes = []
        for detail in commit_details:
            if detail:
                data = json.loads(detail)
                file_changes.append({'file': data['Path'], 'lines_changed': data['Added'] + data['Deleted']})

        dev_stats[owner].append({'date': date, 'files': file_changes})

    # Output the stats
    for dev, commits in dev_stats.items():
        print(f"Developer: {dev}")
        for commit in commits:
            print(f"  Date: {commit['date']}")
            for file_change in commit['files']:
                print(f"    File: {file_change['file']}, Lines Changed: {file_change['lines_changed']}")

