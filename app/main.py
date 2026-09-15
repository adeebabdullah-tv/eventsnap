from datetime import date
import re
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.ocr import extract_text_from_image
from app.extractor import extract_event, extract_event_from_image
from app.image_processor import prepare_image
from app.normalizer import normalize_event
from app.calendar import create_calendar_event
from app.event import NormalizedEvent
app = FastAPI(title="EventSnap")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


def has_date(text):
    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b",
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\b",
    ]

    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def has_time(text):
    pattern = r"\b\d{1,2}(:\d{2})?\s*(AM|PM)\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


def has_title(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]
    return len(lines) > 0


@app.post("/extract")
async def extract(image: UploadFile = File(...)):
    suffix = Path(image.filename or "").suffix or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        contents = await image.read()
        temp_file.write(contents)
        image_path = Path(temp_file.name)

    optimized_path = None

    try:
        ocr_text = extract_text_from_image(image_path)

        print("\nOCR RESULT:")
        print(ocr_text)

        title_found = has_title(ocr_text)
        date_found = has_date(ocr_text)
        time_found = has_time(ocr_text)

        print("\nOCR CHECK:")
        print("Title:", "YES" if title_found else "NO")
        print("Date:", "YES" if date_found else "NO")
        print("Time:", "YES" if time_found else "NO")

        today = date.today()

        if title_found and date_found and time_found:
            print("\nUsing OCR text -> Gemini")

            event = extract_event(
                ocr_text,
                today,
            )
        else:
            print("\nUsing Gemini Vision fallback")

            optimized_path = image_path.parent / "eventsnap_optimized.jpg"

            optimized_image = prepare_image(
                image_path,
                optimized_path,
            )

            event = extract_event_from_image(
                optimized_image,
                today,
            )

        normalized_event = normalize_event(
            event,
            today,
        )

        print("\nFINAL EVENT:")
        print(normalized_event)

        return normalized_event.model_dump(mode="json")

    finally:
        if image_path.exists():
            image_path.unlink()

        if optimized_path and optimized_path.exists():
            optimized_path.unlink()

@app.post("/calendar")
async def add_to_calendar(event_data: dict):

    event = NormalizedEvent.model_validate(event_data)

    created_event = create_calendar_event(event)

    return {
        "message": "Event added to Google Calendar",
        "calendar_url": created_event.get("htmlLink"),
    }
