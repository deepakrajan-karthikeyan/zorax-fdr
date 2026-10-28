"""Small, dependency-free demo worker for FDR extraction and validation.

Production adapters can replace parse_document with an approved OCR/VLM provider.
This module intentionally returns DEMO results and never claims bank verification.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class Extraction:
    instrument_type: str
    reference_number: str
    issuing_bank: str
    amount_minor: int
    maturity_date: str
    confidence: float
    requires_human_review: bool
    model_mode: str = "DEMO"


def _amount(value: str) -> int:
    return int(re.sub(r"[^\d]", "", value))


def parse_document(text: str) -> Extraction:
    """Extract the supported demo fields from OCR text using conservative patterns."""
    reference = re.search(r"(?:FDR|Reference)\s*(?:No\.?|Number)?\s*[:#-]?\s*([A-Z0-9/-]+)", text, re.I)
    bank = re.search(r"(?:Bank|Issuing Bank)\s*[:#-]?\s*([A-Za-z .&]+?)(?=\s+Amount\b|$)", text, re.I)
    amount = re.search(r"(?:Amount|Deposit)\s*[:#-]?\s*(?:INR|Rs\.?|₹)?\s*([\d,]+)", text, re.I)
    maturity = re.search(r"(?:Maturity|Maturity Date)\s*[:#-]?\s*(\d{4}-\d{2}-\d{2})", text, re.I)
    fields = [reference, bank, amount, maturity]
    confidence = round(sum(item is not None for item in fields) / len(fields), 2)
    if not all(fields):
        raise ValueError("Required FDR fields could not be extracted")
    maturity_date = maturity.group(1)
    if date.fromisoformat(maturity_date) <= date.today():
        raise ValueError("Maturity date must be in the future")
    return Extraction(
        instrument_type="FDR",
        reference_number=reference.group(1).upper(),
        issuing_bank=bank.group(1).strip(),
        amount_minor=_amount(amount.group(1)),
        maturity_date=maturity_date,
        confidence=confidence,
        requires_human_review=confidence < 0.85,
    )


def hash_audit_event(event: dict[str, Any], previous_hash: str) -> str:
    payload = json.dumps({"event": event, "previousHash": previous_hash}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    sample = "FDR No: SBI/FDR/824190 Bank: State Bank of India Amount: INR 2500000 Maturity Date: 2099-03-12"
    result = parse_document(sample)
    print(json.dumps(asdict(result), indent=2))
