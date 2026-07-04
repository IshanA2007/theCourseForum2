"""Inject extra context to TCF templates."""

from django.conf import settings

from tcf_website.models import Semester


def base(request) -> dict:
    """Inject user + latest semester info into the template context."""
    return {
        "DEBUG": settings.DEBUG,
        "USER": request.user,
        "LATEST_SEMESTER": Semester.latest(),
    }
