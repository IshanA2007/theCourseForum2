"""Pagination helpers and section-time field map.

Kept separate from ``utils`` so model modules can import these without pulling in
``utils`` (which references models in ``browsable_course_queryset``).
"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# SectionTime weekday flags (forms / advanced search / Course.filter_by_time).
SECTION_DAY_CODE_TO_SECTIONTIME_FIELD = {
    "MON": "monday",
    "TUE": "tuesday",
    "WED": "wednesday",
    "THU": "thursday",
    "FRI": "friday",
}


def paginate(items, page_number, per_page=10):
    """Paginate a queryset or list. Returns a Page object.

    The ``try``/``except`` block guards against out-of-range ``page_number``
    values coming from user-supplied query params:

    - ``PageNotAnInteger`` (e.g. ``?page=abc`` or a missing value) falls back to
      the first page.
    - ``EmptyPage`` (a number past the end, e.g. ``?page=999``) falls back to the
      last available page.

    This keeps the view from raising on malformed pagination input.
    """
    paginator = Paginator(items, per_page)
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
