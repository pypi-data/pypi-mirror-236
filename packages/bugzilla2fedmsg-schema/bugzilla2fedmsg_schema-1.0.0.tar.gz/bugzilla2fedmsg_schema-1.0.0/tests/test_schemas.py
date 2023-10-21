""" Tests for bugzilla2fedmsg_schemas.

Authors:    Adam Williamson <awilliam@redhat.com>

"""


from jsonschema.exceptions import ValidationError

from bugzilla2fedmsg_schema import MessageV1BZ4


class TestSchemas:
    def test_bug_create_schema(self, bug_create_message):
        """Check bug.create message schema bits."""
        message = bug_create_message
        message.validate()
        assert message.assigned_to_email == "lvrabec@redhat.com"
        assert message.component_name == "selinux-policy"
        assert message.product_name == "Fedora"
        assert (
            message.summary
            == "dgunchev@gmail.com filed a new bug RHBZ#1701391 'SELinux is preventing touch from 'write'...'"
        )
        assert (
            str(message)
            == "dgunchev@gmail.com filed a new bug RHBZ#1701391 'SELinux is preventing touch from 'write'...'"
        )
        assert message.url == "https://bugzilla.redhat.com/show_bug.cgi?id=1701391"
        assert (
            message.app_icon
            == "https://bugzilla.redhat.com/extensions/RedHat/web/css/favicon.ico?v=0"
        )
        assert message.agent_name == "Doncho Gunchev"
        assert message.app_name == "bugzilla2fedmsg"
        # broken till we can do email2fas
        assert message.usernames == []
        assert message.packages == ["selinux-policy"]
        assert (
            message.agent_avatar
            == "https://seccdn.libravatar.org/avatar/d4bfc5ec5260361c930aad299c8e14fe03af45109ea88e880a191851b8c83e7f?s=64&d=retro"
        )
        assert message._primary_email == "dgunchev@gmail.com"
        assert message._all_emails == ["dgunchev@gmail.com", "lvrabec@redhat.com"]

    def test_bug_modify_schema(self, bug_modify_message):
        """Check bug.modify message schema bits."""
        message = bug_modify_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "mhroncok@redhat.com updated 'cc' on RHBZ#1699203 'python-pyramid-1.10.4 is available'"
        )
        # here we test both picking up an address from a 'cc' change
        # event, and filtering out lists.fedoraproject.org addresses
        assert message._all_emails == [
            "awilliam@redhat.com",
            "mhroncok@redhat.com",
            "upstream-release-monitoring@fedoraproject.org",
        ]
        # here we test that we can at least derive usernames from
        # fedoraproject.org email addresses
        assert message.usernames == ["upstream-release-monitoring"]

    def test_bug_modify_four_changes_schema(self, bug_modify_four_changes_message):
        """Check bug.modify message schema bits when the message
        includes four changes (this exercises comma_join).
        """
        message = bug_modify_four_changes_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "zebob.m@gmail.com updated 'assigned_to', 'bug_status', 'cc', and 'flag.needinfo' on RHBZ#1702701 'Review Request: perl-Class-AutoClass - D...'"
        )
        # this tests gathering an address from a 'needinfo' change
        assert message._all_emails == [
            "ppisar@redhat.com",
            "rob@boberts.com",
            "zebob.m@gmail.com",
        ]

    def test_bug_modify_two_changes_schema(self, bug_modify_two_changes_message):
        """Check bug.modify message schema bits when the message
        includes two changes (this exercises a slightly different
        comma_join path).
        """
        message = bug_modify_two_changes_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "zebob.m@gmail.com updated 'assigned_to' and 'bug_status' on RHBZ#1702701 'Review Request: perl-Class-AutoClass - D...'"
        )

    def test_bug_modify_no_changes_schema(self, bug_modify_message):
        """Check bug.modify message schema bits when event is missing
        'changes' - we often get messages like this, for some reason.
        """
        message = bug_modify_message
        # wipe the 'changes' dict from the sample message, to simulate
        # one of these broken messages
        del message.body["event"]["changes"]
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "mhroncok@redhat.com updated something unknown on RHBZ#1699203 'python-pyramid-1.10.4 is available'"
        )
        assert message._all_emails == [
            "mhroncok@redhat.com",
            "upstream-release-monitoring@fedoraproject.org",
        ]

    def test_comment_create_schema(self, comment_create_message):
        """Check comment.create message schema bits."""
        message = comment_create_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "smooge@redhat.com added comment on RHBZ#1691487 'openQA transient test failure as duplica...'"
        )

    def test_attachment_create_schema(self, attachment_create_message):
        """Check attachment.create message schema bits."""
        message = attachment_create_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "peter@sonniger-tag.eu added attachment on RHBZ#1701353 '[abrt] gnome-software: gtk_widget_unpare...'"
        )

    def test_attachment_modify_schema(self, attachment_modify_message):
        """Check attachment.modify message schema bits."""
        message = attachment_modify_message
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "joequant@gmail.com updated 'isobsolete' for attachment on RHBZ#1701766 'I2C_HID_QUIRK_NO_IRQ_AFTER_RESET caused ...'"
        )

    def test_attachment_modify_no_changes_schema(self, attachment_modify_message):
        """Check attachment.modify message schema bits when event is
        missing 'changes' - unlike the bug.modify case I have not
        actually seen a message like this in the wild, but we do
        handle it just in case.
        """
        message = attachment_modify_message
        # wipe the 'changes' dict from the sample message, to simulate
        # one of these broken messages
        del message.body["event"]["changes"]
        # this should not raise an exception
        message.validate()
        assert (
            message.summary
            == "joequant@gmail.com updated something unknown for attachment on RHBZ#1701766 'I2C_HID_QUIRK_NO_IRQ_AFTER_RESET caused ...'"
        )

    def test_component_not_package_schema(self, bug_create_message):
        """Check we filter out components that aren't packages."""
        # adjust the component in the sample message to one we should
        # filter out
        message = bug_create_message
        if isinstance(message, MessageV1BZ4):
            message.body["bug"]["component"] = "distribution"
        else:
            message.body["bug"]["component"]["name"] = "distribution"
        # this should not raise an exception
        message.validate()
        assert message.packages == []

    def test_bug_no_qa_contact(self, bug_create_message):
        """Check bug.create message schema bits when qa_contact is None."""
        message = bug_create_message
        message.body["bug"]["qa_contact"] = None
        # this should not raise an exception
        try:
            message.validate()
        except ValidationError as e:
            raise AssertionError(e) from e
        assert message.bug["qa_contact"] is None
