""" Test fixtures for bugzilla2fedmsg.relay.

Authors:    Adam Williamson <awilliam@redhat.com>

"""

import pytest

from .samples import (
    ATTACHMENT_CREATE_MESSAGE_BZ4,
    ATTACHMENT_CREATE_MESSAGE_NOBZ4,
    ATTACHMENT_MODIFY_MESSAGE_BZ4,
    ATTACHMENT_MODIFY_MESSAGE_NO_BZ4,
    BUG_CREATE_MESSAGE_BZ4,
    BUG_CREATE_MESSAGE_NO_BZ4,
    BUG_MODIFY_FOUR_CHANGES_MESSAGE_BZ4,
    BUG_MODIFY_FOUR_CHANGES_MESSAGE_NO_BZ4,
    BUG_MODIFY_MESSAGE_BZ4,
    BUG_MODIFY_MESSAGE_NO_BZ4,
    BUG_MODIFY_TWO_CHANGES_MESSAGE_BZ4,
    BUG_MODIFY_TWO_CHANGES_MESSAGE_NO_BZ4,
    COMMENT_CREATE_MESSAGE_BZ4,
    COMMENT_CREATE_MESSAGE_NO_BZ4,
)


@pytest.fixture(params=[BUG_CREATE_MESSAGE_NO_BZ4, BUG_CREATE_MESSAGE_BZ4])
def bug_create_message(request):
    return request.param


@pytest.fixture(params=[BUG_MODIFY_MESSAGE_NO_BZ4, BUG_MODIFY_MESSAGE_BZ4])
def bug_modify_message(request):
    return request.param


@pytest.fixture(
    params=[BUG_MODIFY_FOUR_CHANGES_MESSAGE_NO_BZ4, BUG_MODIFY_FOUR_CHANGES_MESSAGE_BZ4]
)
def bug_modify_four_changes_message(request):
    return request.param


@pytest.fixture(params=[BUG_MODIFY_TWO_CHANGES_MESSAGE_NO_BZ4, BUG_MODIFY_TWO_CHANGES_MESSAGE_BZ4])
def bug_modify_two_changes_message(request):
    return request.param


@pytest.fixture(params=[COMMENT_CREATE_MESSAGE_NO_BZ4, COMMENT_CREATE_MESSAGE_BZ4])
def comment_create_message(request):
    return request.param


@pytest.fixture(params=[ATTACHMENT_CREATE_MESSAGE_NOBZ4, ATTACHMENT_CREATE_MESSAGE_BZ4])
def attachment_create_message(request):
    return request.param


@pytest.fixture(params=[ATTACHMENT_MODIFY_MESSAGE_NO_BZ4, ATTACHMENT_MODIFY_MESSAGE_BZ4])
def attachment_modify_message(request):
    return request.param
