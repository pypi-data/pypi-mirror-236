# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl workflow attachments handling part"""

from typing import List, Tuple, NoReturn

import os
import sys

from opentf.tools.ctlcommons import _error, _is_command, _ensure_options, _ensure_uuid
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import _localstore, _get_file
from opentf.tools.ctlworkflows import _get_workflows

########################################################################
# Constants

UUID_LENGTH = 36


########################################################################
# Help messages

CP_HELP = '''Get a local copy of a workflow attachment

Examples:

  # Get a local copy of a workflow attachment
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:39e68299-8995-4915-9367-1df1ff642159 /target/dir/output_file.ext

Usage:
  opentf-ctl cp WORKFLOW_ID:ATTACHMENT_ID DESTINATION_FILEPATH
'''

########################################################################
# Helpers


def _fatal(*msg) -> NoReturn:
    _error(*msg)
    sys.exit(2)


def _get_options(options: List[str]) -> Tuple[str, str, str]:
    workflow_id, _, attachment_id = options[0].partition(':')
    if not workflow_id or not attachment_id or len(options) != 2:
        _error(
            'Invalid parameters. Expected WORKFLOW_ID:ATTACHMENT_ID DESTINATION_FILEPATH, got %s.',
            ' '.join(options),
        )
        sys.exit(1)
    _ensure_uuid(attachment_id[:-2]) if attachment_id.strip().endswith(
        ('_a', '_e')
    ) else _ensure_uuid(attachment_id)
    return (
        _ensure_uuid(workflow_id, _get_workflows),
        attachment_id,
        options[1],
    )


def _get_attachment_filename(headers, attachment_id: str) -> str:
    _, _, name_with_uuid = headers.get('Content-Disposition', '').partition('name=')
    if name_with_uuid.startswith(attachment_id):
        return name_with_uuid[UUID_LENGTH + 1 :]
    return 'untitled'


########################################################################
# Handle attachments


def _get_attachment(workflow_id: str, attachment_id: str):
    msg = f'Failed to get attachment {attachment_id} from localstore'
    response = _get_file(
        _localstore(),
        f'/workflows/{workflow_id}/files/{attachment_id}',
        msg=msg,
        statuses=(200, 404, 403),
    )

    if response.status_code != 200:
        _fatal(
            '%s. Error code: %d, message: "%s"',
            msg,
            response.status_code,
            response.json().get('message'),
        )

    return response


def _save_attachment(response, attachment_id, filepath):
    with open(os.path.normpath(filepath), 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(
        f'Attachment {_get_attachment_filename(response.headers, attachment_id)} ({attachment_id}) is downloaded as {filepath}.'
    )


def download_attachment(workflow_id: str, attachment_id: str, filepath: str) -> None:
    try:
        response = _get_attachment(workflow_id, attachment_id)
        _save_attachment(response, attachment_id, filepath)
    except Exception as err:
        _fatal(
            'Failed to download attachment %s as %s: %s.',
            attachment_id,
            filepath,
            str(err),
        )


########################################################################
# Exposed functions


def print_attachments_help(args: List[str]):
    """Display help."""
    if _is_command('cp', args):
        print(CP_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def attachments_cmd():
    """Interact with attachments."""
    if _is_command('cp _', sys.argv):
        options = _ensure_options('cp *', sys.argv[1:])
        read_configuration()
        download_attachment(*_get_options(options))
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
