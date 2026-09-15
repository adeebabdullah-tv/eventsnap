# EventSnap

EventSnap is an open-source event extraction tool for students.

Upload an event poster or announcement, and EventSnap extracts the important details such as:

- Event title
- Date
- Start and end time
- Location
- Organizer
- Description
- Registration deadline

The extracted information can then be reviewed and edited before being added directly to Google Calendar.

## How It Works

Screenshot / Event Poster
        ↓
     OCR
        ↓
  Gemini AI
        ↓
 Structured Event
        ↓
 Review & Edit
        ↓
 Google Calendar

## Features

- 🖼️ Extract events from screenshots and posters
- 🔎 OCR using Tesseract
- 🤖 AI-powered event extraction using Gemini
- 📅 Add events directly to Google Calendar
- ✏️ Review and edit extracted information
- 🧠 Handles relative dates such as "tomorrow"
- 🔐 Uses your own API credentials
- 🌱 Open source

## Tech Stack

- Python
- FastAPI
- Pydantic
- Google Gemini API
- Tesseract OCR
- Google Calendar API
- HTML / CSS / JavaScript

## Prerequisites

Before installing EventSnap, make sure you have:

- Python 3.10+
- Tesseract OCR
- A Gemini API key
- Google Calendar API credentials

### Tesseract OCR

EventSnap uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
to extract text from event posters.

`pytesseract` is the Python wrapper, but the actual Tesseract OCR
program must also be installed separately.

### Windows

1. Install Tesseract OCR for Windows.
2. The default installation location is usually:

```text
C:\Program Files\Tesseract-OCR
```
3. Add the Tesseract installation directory to your Windows PATH.
4. Open a new terminal and verify the installation:
    tesseract --version

If the installation was successful, the command will display the
installed Tesseract version.

EventSnap currently expects Tesseract at:
    C:\Program Files\Tesseract-OCR\tesseract.exe
If Tesseract is installed elsewhere, update the tesseract_cmd
path in app/ocr.py.

For more information, visit the
Tesseract OCR GitHub repository.


Installation
1. Clone the repository
git clone https://github.com/adeebabdullah-tv/eventsnap.git
cd eventsnap
2. Create a virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1
3. Install Python dependencies
pip install -r requirements.txt
Configuration
Gemini API

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Do not commit your .env file or API key to GitHub.

A .env.example file is included as a template.

Google Calendar

To enable Google Calendar integration:

Create a Google Cloud project.
Enable the Google Calendar API.
Configure OAuth consent screen.
Create OAuth credentials for a Desktop application.
Download the credentials file.
Rename it to:
credentials.json
Place it in the project root.

Do not commit credentials.json or token.json.

Running EventSnap

Start the FastAPI server:

uvicorn app.main:app --reload

Then open:

http://127.0.0.1:8000

Upload an event poster and EventSnap will extract the event information.

Project Structure
eventsnap/
├── app/
│   ├── main.py
│   ├── event.py
│   ├── extractor.py
│   ├── normalizer.py
│   ├── ocr.py
│   ├── image_processor.py
│   ├── calendar.py
│   ├── test_normalizer.py
│   ├── static/
│   └── templates/
├── .env.example
├── .gitignore
├── credentials.json       # local only
├── token.json             # generated locally
├── LICENSE
├── README.md
└── requirements.txt
Security

Never commit the following files:

.env
credentials.json
token.json

These files may contain API keys, OAuth credentials, or access tokens.

Future Plans
💬 WhatsApp integration
📱 Mobile-friendly interface
🔗 Share event messages directly with EventSnap
🗓️ Support for multiple calendar providers
🌐 Hosted version
🔐 User authentication
🧪 More automated tests
🎨 Improved UI/UX
License

EventSnap is open source and available under the MIT License.