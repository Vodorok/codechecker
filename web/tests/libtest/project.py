# -----------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -----------------------------------------------------------------------------
"""
Test project helpers.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import fnmatch
import json
import os
import shlex
import shutil
import subprocess
from . import env, plist_test


def prepare(test_project_path, temporary_test_path):
    """Prepare test project and report files for the tests.

    Copy the test project to the temporary test dir.
    Modify the report files to point to the source files in the
    temporary test dir.

    Returns a dict with the path to created temporary project
    and report directories.
    """
    shutil.copytree(test_project_path,
                    os.path.join(temporary_test_path, "project"))

    test_project = os.path.join(temporary_test_path, "project")
    test_reports = os.path.join(temporary_test_path, "project", "reports")

    for root, _, filenames in os.walk(test_reports):
        for filename in fnmatch.filter(filenames, '*.plist'):
            plist_test.prefix_file_path(os.path.join(root, filename),
                                        test_project)
    test_project_data = {
        "test_project_path": test_project,
        "test_project_reports": test_reports
    }

    return test_project_data


def get_info(test_project):
    test_proj_cfg = os.path.join(os.path.realpath(path(test_project)),
                                 'project_info.json')
    project_info = \
        json.load(open(test_proj_cfg))
    return project_info


def path(test_project):
    return os.path.join(env.test_proj_root(), test_project)


def get_build_cmd(test_project):
    return get_info(test_project)['build_cmd']


def get_clean_cmd(test_project):
    try:
        return get_info(test_project)['clean_cmd']
    except KeyError:
        return ""


def clean(test_project, environment=None):
    """Clean the test project."""
    project_path = path(test_project)
    clean_cmd = get_clean_cmd(project_path)
    if not clean_cmd:
        # If the clean command is missing do nothing.
        return 0
    try:
        print(clean_cmd)
        proc = subprocess.Popen(shlex.split(clean_cmd),
                                cwd=project_path,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=environment)
        _, _ = proc.communicate()
        return 0
    except subprocess.CalledProcessError as cerr:
        return cerr.returncode


def insert_suppression(source_file_name):
    """Insert a suppression comment to a source file.

    An insert_suppress_here comment in the source file will be replaced
    by a suppress comment.
    """
    with open(source_file_name, 'r') as f:
        content = f.read()
    content = content.replace("insert_suppress_here",
                              "codechecker_suppress [all] test suppression!")
    with open(source_file_name, 'w') as f:
        f.write(content)
