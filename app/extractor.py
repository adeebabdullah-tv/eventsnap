import os
import base64

from dotenv import load_dotenv
from google import genai

from app.event import Event


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_event(text, reference_date):
    prompt = f"""
Extract the event information from the following announcement.
Reference date: {reference_date}

Important rules:
- Extract only information that is actually present.
- Do not invent missing information.
- Put the main purpose, topic, or summary of the event into the description field when it is clearly stated.
- Ignore decorative text, emojis, slogans, and promotional wording unless it contains useful event information.
- Preserve dates and times as they appear for now.
- Return the result according to the Event schema.
Announcement:
{text}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Event.model_json_schema(),
        },
    )

    return Event.model_validate_json(interaction.output_text)


def extract_event_from_image(image_path, reference_date):
    prompt = f"""
Extract the event information from this event poster.

Reference date: {reference_date}

Important rules:
- Read the information directly from the image.
- Do not guess or invent information.
- Extract the event title, date, start time, end time, location,
  description, organizer, registration URL, and registration deadline
  when they are visible.
- Pay special attention to small text.
- If information is not visible, leave that field empty.
- Return the result according to the Event schema.
"""

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    image_data = base64.b64encode(image_bytes).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=[
            {
                "type": "image",
                "data": image_data,
                "mime_type": "image/jpeg",
            },
            {
                "type": "text",
                "text": prompt,
            },
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Event.model_json_schema(),
        },
    )

    return Event.model_validate_json(interaction.output_text)