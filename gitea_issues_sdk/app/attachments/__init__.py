"""
Attachments module for the Gitea Issues SDK.

This module provides functionality for working with attachments on issues and comments in Gitea repositories.
"""

from .api import AttachmentsAPI
from .models import Attachment, EditAttachmentOption

__all__ = ["AttachmentsAPI", "Attachment", "EditAttachmentOption"]
