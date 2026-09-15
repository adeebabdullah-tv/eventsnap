from datetime import date, datetime, time, timedelta

from dateutil import parser

from app.event import Event, NormalizedEvent


def normalize_date(date_text, reference_date):
    if not date_text:
        return None

    text = date_text.lower().strip()

    if text == "today":
        return reference_date

    if text == "tomorrow":
        return reference_date + timedelta(days=1)

    if text == "day after tomorrow":
        return reference_date + timedelta(days=2)

    parsed = parser.parse(
        date_text,
        default=datetime.combine(reference_date, time.min)
    )

    return parsed.date()


def normalize_time(time_text):
    if not time_text:
        return None

    parsed = parser.parse(time_text)

    return parsed.time()


def normalize_event(event: Event, reference_date: date) -> NormalizedEvent:
    return NormalizedEvent(
        title=event.title,
        date=normalize_date(event.date, reference_date),
        start_time=normalize_time(event.start_time),
        end_time=normalize_time(event.end_time),
        location=event.location,
        description=event.description,
        organizer=event.organizer,
        registration_url=event.registration_url,
        registration_deadline=normalize_date(
            event.registration_deadline,
            reference_date
        ),
    )