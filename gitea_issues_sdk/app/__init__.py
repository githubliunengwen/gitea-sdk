"""
App module for the Gitea Issues SDK.

This module contains the core functionality for interacting with the Gitea Issues API.
"""

from .issues import IssuesAPI, Issue, EditIssueOption
from .comments import CommentsAPI, Comment, EditCommentOption
from .labels import LabelsAPI, Label, EditLabelOption
from .milestones import MilestonesAPI, Milestone, EditMilestoneOption
from .reactions import ReactionsAPI, Reaction, EditReactionOption
from .attachments import AttachmentsAPI, Attachment, EditAttachmentOption
from .blocks import BlocksAPI, IssueMeta
from .subscriptions import SubscriptionsAPI
from .timeline import TimelineAPI, TimelineEvent
from .stopwatch import StopwatchAPI, TrackedTime
from .pinned import PinnedAPI

__all__ = [
    "IssuesAPI", "Issue", "EditIssueOption",
    "CommentsAPI", "Comment", "EditCommentOption",
    "LabelsAPI", "Label", "EditLabelOption",
    "MilestonesAPI", "Milestone", "EditMilestoneOption",
    "ReactionsAPI", "Reaction", "EditReactionOption",
    "AttachmentsAPI", "Attachment", "EditAttachmentOption",
    "BlocksAPI", "IssueMeta",
    "SubscriptionsAPI",
    "TimelineAPI", "TimelineEvent",
    "StopwatchAPI", "TrackedTime",
    "PinnedAPI",
]
