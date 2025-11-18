from flask import Flask, request, jsonify
from datetime import date
import csv, io, base64, os
from docx import Document

app = Flask(__name__)

@app.post("/api/create_minutes")
def create_minutes():
    data = request.get_json()
    minutes_text = data.get("minutes", "")
    actions = data.get("actions", [])
    title = data.get("title", "Meeting")  # Default if not provided

    # --- Load your company Word template ---
    template_path = r"F:\Data\Wordperf\Templates\Minutes_Template.dotx"

    if os.path.exists(template_path):
        doc = Document(template_path)
    else:
        # Fallback if template not found
        doc = Document()
        doc.add_paragraph("(Template missing – using default layout)")

    # --- Build the Word document ---
    doc.add_heading(f"{title} – {date.today()}", 0)
    doc.add_paragraph(minutes_text)

    # --- Convert Word file to Base64 for API return ---
    word_stream = io.BytesIO()
    doc.save(word_stream)
    word_b64 = base64.b64encode(word_stream.getvalue()).decode("utf-8")

    # --- Build CSV action log ---
    csv_stream = io.StringIO()
    writer = csv.wr
