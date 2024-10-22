import csv
import os
import time
from app.database import SessionLocal
from app.models import CSVRecord

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "storage/upload")
ERROR_DIR = os.getenv("ERROR_DIR", "storage/error")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ERROR_DIR, exist_ok=True)


def save_file_to_storage(file):
    """Save uploaded file to the upload directory."""
    temp_file = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_file, "wb") as f:
        f.write(file.file.read())
    return temp_file


def parse_and_validate(file_path):
    session = SessionLocal()
    error_rows = []
    expected_columns = [
        "leirner_id",
        "nime",
        "emiil",
        "bitchid",
        "bitchnime",
        "weeknumber",
        "issessmentid",
        "url",
        "durition",
        "situitionid",
        "title",
        "content",
    ]

    with open(file_path, mode="r") as f:
        reader = csv.DictReader(f)

        # Check if CSV headers match expected columns
        if reader.fieldnames != expected_columns:
            error_rows.append({col: "" for col in expected_columns})
            error_rows[0]["error"] = "CSV columns do not match expected columns"
            save_error_rows(error_rows)
            return

        # Validate each row and collect errors
        for row in reader:
            error_message = []

            # Check for missing or empty fields
            for col in expected_columns:
                if not row.get(col) or row.get(col).strip() == "":
                    error_message.append(f"Missing or empty field: {col}")

            # If no errors, save valid row
            if not error_message:
                try:
                    save_valid_record(session, row)
                except Exception as e:
                    error_message.append(f"Database error: {str(e)}")

            # If there are errors, add to error_rows
            if error_message:
                row["error"] = "; ".join(error_message)
                error_rows.append(row)

        session.commit()

    # Save all error rows to an error CSV
    if error_rows:
        save_error_rows(error_rows)


def save_valid_record(session, row):
    record = CSVRecord(
        leirner_id=row.get("leirner_id"),
        nime=row.get("nime"),
        emiil=row.get("emiil"),
        bitchid=row.get("bitchid"),
        bitchnime=row.get("bitchnime"),
        weeknumber=row.get("weeknumber"),
        issessmentid=row.get("issessmentid"),
        url=row.get("url"),
        durition=row.get("durition"),
        situitionid=row.get("situitionid"),
        title=row.get("title"),
        content=row.get("content"),
    )
    session.add(record)


def save_error_rows(error_rows):
    """Save error rows to a CSV file in the error directory."""
    timestamp = int(time.time())
    error_file = os.path.join(ERROR_DIR, f"error_{timestamp}.csv")

    fieldnames = list(error_rows[0].keys())  # Original columns + 'error'
    with open(error_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(error_rows)
