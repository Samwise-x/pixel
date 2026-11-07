#!/usr/bin/env python3
"""Bind verified cloud/device receipts to the EXISTING SAMWISE append-only ledger.

No new supervisor, daemon, database, secret store, or event-log format.
Only the existing samwise.py make_event/write_ledger functions write ledger bytes.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

PROTOCOL = "samwise.accumulation/v1"
REPO = "Samwise-x/pixel"
DRIVE_FOLDER = "1dmMV-67c-daoTEftPbGqWcCgPo-UDbcs"
PROJECT_ID = "PVT_kwHODwj8G84BqjDS"

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def source_module(path):
    spec = importlib.util.spec_from_file_location("samwise_existing_ledger", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("SAMWISE_LEDGER_WRITER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "make_event", None)) or not callable(getattr(module, "write_ledger", None)):
        raise RuntimeError("SAMWISE_LEDGER_WRITER_MISSING_METHODS")
    return module

def validated_receipt(raw):
    obj = json.loads(raw.decode("utf-8"))
    required = {"schema", "target", "github", "drive", "device", "verification"}
    if set(obj) != required:
        raise ValueError("RECEIPT_FIELD_MISMATCH")
    if obj["schema"] != PROTOCOL or not isinstance(obj["target"], str) or not obj["target"].strip():
        raise ValueError("RECEIPT_SCHEMA_OR_TARGET")
    gh, drive, device, proof = (obj[k] for k in ("github", "drive", "device", "verification"))
    if (gh.get("repo") != REPO or gh.get("repository_id") != 1416236181
        or gh.get("project_node_id") != PROJECT_ID or gh.get("repo_readback") is not True
        or gh.get("project_readback") is not True):
        raise ValueError("GITHUB_IDENTITY_UNVERIFIED")
    if (drive.get("folder_id") != DRIVE_FOLDER or drive.get("folder_readback") is not True
        ):
        raise ValueError("DRIVE_IDENTITY_UNVERIFIED")
    if (not isinstance(device, dict) or not isinstance(device.get("observed_model"), str)
        or not isinstance(device.get("execution_proof"), str) or len(device["execution_proof"]) < 8
        or proof != "PASS"):
        raise ValueError("DEVICE_EXECUTION_UNVERIFIED")
    # The receipt comes from a fully observed, independently checked connector pass.
    return obj

def run(path, writer, action, receipt_drive_id):
    raw = path.read_bytes()
    receipt = validated_receipt(raw)
    mod = source_module(writer)
    assert getattr(mod, "ENV", None) == "samwise://pixel11", "UNEXPECTED_LEDGER_OWNER"
    if not (isinstance(receipt_drive_id, str) and len(receipt_drive_id) >= 15 and receipt_drive_id.isascii() and all(x.isalnum() or x in "-_" for x in receipt_drive_id)):
        raise ValueError("RECEIPT_DRIVE_ID_INVALID")
    evidence_url = "https://drive.google.com/file/d/" + receipt_drive_id + "/view"
    payload = {
        "target": receipt["target"], "observed_model": receipt["device"]["observed_model"],
        "github_repo": REPO, "project_node_id": PROJECT_ID, "drive_folder_id": DRIVE_FOLDER,
        "receipt_sha256": digest(raw), "receipt_google_drive_file_id": receipt_drive_id
    }
    event = mod.make_event(
        "samwise://bootstrap/accumulation-v1",
        "samwise://target/" + digest(receipt["target"].encode())[:24],
        "bootstrap.bound", "OBSERVED", "VERIFICATION: PASS", payload, evidence_url
    )
    ledger_path = Path(mod.LEDGER)
    existed = False
    if ledger_path.is_file():
        with ledger_path.open("r", encoding="utf-8") as f:
            existed = any(json.loads(line).get("event_id") == event["event_id"] for line in f if line.strip())
    if action == "verify":
        return {"result": "VERIFIED" if existed else "ACTION_REQUIRED", "event_id": event["event_id"],
                "existing_event": existed, "ledger_path": str(ledger_path)}
    cursor = mod.write_ledger([event])
    with ledger_path.open("r", encoding="utf-8") as f:
        matches = sum(json.loads(line).get("event_id") == event["event_id"] for line in f if line.strip())
    if matches != 1:
        raise RuntimeError("LEDGER_EVENT_CARDINALITY_FAILURE")
    return {"result": "UNCHANGED" if existed else "VERIFIED", "event_id": event["event_id"],
            "existing_event": existed, "ledger_cursor": cursor,
            "ledger_sha256": digest(ledger_path.read_bytes()), "receipt_sha256": digest(raw)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=("verify", "apply"))
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--receipt-drive-id", required=True)
    p.add_argument("--writer", type=Path, default=Path.home() / "dev/scripts/samwise.py")
    args = p.parse_args()
    try:
        print(json.dumps(run(args.receipt, args.writer, args.action, args.receipt_drive_id), sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, AssertionError) as exc:
        print(json.dumps({"result": "FAILED", "reason": str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
