import hashlib
import io

import pandas as pd
from sqlalchemy.orm import Session

from app.models.core import StagingActivity, SyncRun

# Sheets treated as sensitive by default until an admin reclassifies them.
# See PRD v1.2 §39.1 (Data Classes) and §37.2 (Prohibited Patterns).
SENSITIVE_SHEET_HINTS = ("PATIENT", "THERAPY", "PASIEN", "TERAPI")


def row_hash(sheet: str, row_index: int, values: dict) -> str:
    payload = f"{sheet}|{row_index}|{sorted(values.items())}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def import_workbook(db: Session, filename: str, content: bytes) -> SyncRun:
    """Reads every sheet in the uploaded workbook into stg_activities.
    Nothing here writes to `tasks` directly — import always lands in
    staging for review, per PRD v1.2 §38 (Migration and Cutover Plan)."""

    xls = pd.ExcelFile(io.BytesIO(content), engine="openpyxl")

    inserted = updated = duplicate = review = blocked = 0

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        is_sensitive = any(h in sheet_name.upper() for h in SENSITIVE_SHEET_HINTS)

        for idx, row in df.iterrows():
            values = row.fillna("").to_dict()
            h = row_hash(sheet_name, idx, values)

            existing = (
                db.query(StagingActivity)
                .filter_by(source_sheet=sheet_name, source_row=idx, source_hash=h)
                .first()
            )
            if existing:
                duplicate += 1
                continue

            status_value = str(values.get("status", "")).upper()
            sync_status = "BLOCKED" if status_value == "BLOCKED" else "REVIEW"

            record = StagingActivity(
                source_workbook=filename,
                source_sheet=sheet_name,
                source_row=int(idx),
                source_hash=h,
                sync_status=sync_status,
                privacy_sensitive=is_sensitive,
                ai_allowed=not is_sensitive,
                source_payload=str(values),
            )
            db.add(record)

            inserted += 1
            if sync_status == "BLOCKED":
                blocked += 1
            else:
                review += 1

    run = SyncRun(
        source_file=filename,
        inserted=inserted,
        updated=updated,
        duplicate=duplicate,
        review=review,
        blocked=blocked,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run
