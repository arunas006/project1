
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import structlog
from config.settings import settings


IST = ZoneInfo("Asia/Kolkata")


def add_severity(logger, method_name, event_dict):
    level = event_dict.get("level")

    if level:
        event_dict["severity"] = level.upper()

    return event_dict


class CustomLogger:
    def __init__(self):
        # Store logs in backend/logs/
        log_dir = Path(__file__).resolve().parents[2] / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create a unique filename using IST
        timestamp = timestamp = datetime.now(IST).strftime("%Y%m%d_%H%M")

        self.log_file = log_dir / f"{timestamp}.jsonl"
        self._uploaded = False

        # Configure console and file logging
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    self.log_file,
                    mode="a",
                    encoding="utf-8",
                ),
            ],
            format="%(message)s",
            force=True,
        )

        # Configure structured JSON logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(
                    fmt="iso",
                    utc=False,
                    key="timestamp",
                ),
                structlog.stdlib.add_log_level,
                add_severity,
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self, name=None):
        return structlog.get_logger(name)

    def flush_to_gcs(self):
        if self._uploaded or not self.log_file.exists():
            return

        if not settings.GCS_BUCKET_NAME:
            return

        try:
            from google.cloud import storage

            client = storage.Client(
                project=settings.GCP_PROJECT or None
            )

            bucket = client.bucket(settings.GCS_BUCKET_NAME)
            blob = bucket.blob(f"logs/{self.log_file.name}")

            blob.upload_from_filename(
                str(self.log_file),
                content_type="application/x-ndjson",
            )

            self._uploaded = True

        except Exception:
            logging.getLogger(__name__).exception(
                "GCS log upload failed"
            )


# Initialize once per application process
logger_manager = CustomLogger()
logger = logger_manager.get_logger("application")


if __name__ == "__main__":
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("This is an error")
