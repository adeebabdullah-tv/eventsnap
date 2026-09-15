const form = document.getElementById("upload-form");
const status = document.getElementById("status");
const result = document.getElementById("result");

form.addEventListener("submit", async function (event) {
event.preventDefault();


const fileInput = document.getElementById("image");

if (!fileInput.files || fileInput.files.length === 0) {
    status.textContent = "❌ Please select an image first.";
    return;
}

const formData = new FormData();
formData.append("image", fileInput.files[0]);

status.textContent = "🔍 Extracting event...";
result.classList.add("hidden");

try {
    const response = await fetch("/extract", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Extraction failed.");
    }

    document.getElementById("title").value = data.title || "";
    document.getElementById("date").value = data.date || "";
    document.getElementById("start-time").value = data.start_time || "";
    document.getElementById("end-time").value = data.end_time || "";
    document.getElementById("location").value = data.location || "";
    document.getElementById("organizer").value = data.organizer || "";
    document.getElementById("description").value = data.description || "";

    status.textContent = "✅ Event extracted!";
    result.classList.remove("hidden");

} catch (error) {
    console.error(error);
    status.textContent = "❌ " + error.message;
}


});

const calendarButton = document.getElementById("calendar-button");

calendarButton.addEventListener("click", async function () {

    const eventData = {
        title: document.getElementById("title").value,
        date: document.getElementById("date").value,
        start_time: document.getElementById("start-time").value,
        end_time: document.getElementById("end-time").value || null,
        location: document.getElementById("location").value || null,
        organizer: document.getElementById("organizer").value || null,
        description: document.getElementById("description").value || null
    };

    status.textContent = "📅 Adding to Google Calendar...";

    try {

        const response = await fetch("/calendar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(eventData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Could not add event."
            );
        }

        status.textContent = "✅ Added to Google Calendar!";

        if (data.calendar_url) {
            window.open(data.calendar_url, "_blank");
        }

    } catch (error) {

        console.error(error);

        status.textContent = "❌ " + error.message;
    }
});