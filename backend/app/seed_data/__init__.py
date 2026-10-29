from __future__ import annotations

from ..models import Guide
from .github import GUIDE as GITHUB
from .google_calendar import GUIDE as GCAL
from .slack import GUIDE as SLACK
from .hubspot import GUIDE as HUBSPOT
from .notion import GUIDE as NOTION
from .salesforce import GUIDE as SALESFORCE

SEED_GUIDES: list[Guide] = [GITHUB, GCAL, SLACK, HUBSPOT, NOTION, SALESFORCE]
