import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from ingestion_service.database import SessionLocal
from ingestion_service.ingestor import ingest_sources
from ingestion_service.models import ApiRecord

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def load_config(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file '{path}' not found.")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class IngestionHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=4, default=str).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    # -------------------- GET --------------------

    def do_GET(self):
        print("GET Request:", self.path)

        if self.path == "/health":
            self.send_json({"status": "ok"})
            return

        elif self.path == "/sources":
            config = load_config("config.json")
            self.send_json(config)
            return

        elif self.path == "/records":
            print("Inside /records endpoint")

            session = SessionLocal()

            try:
                rows = session.query(ApiRecord).all()

                result = []

                for row in rows:
                    result.append({
                        "id": row.id,
                        "source": row.source,
                        "endpoint": row.endpoint,
                        "data": row.data,
                        "created_at": str(row.created_at)
                    })

                self.send_json(result)

            finally:
                session.close()

            return

        else:
            self.send_json({"error": "Endpoint not found"}, 404)

    # -------------------- POST --------------------

    def do_POST(self):

        logger.info(f"POST {self.path}")

        if self.path != "/ingest":
            self.send_json({"error": "Endpoint not found"}, 404)
            return

        try:

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")

            if body:

                try:
                    payload = json.loads(body)
                except json.JSONDecodeError:
                    self.send_json(
                        {"error": "Invalid JSON body"},
                        400
                    )
                    return

            else:
                payload = {}

            config = payload.get("config")

            if config is None:
                config_path = payload.get("config_path", "config.json")
                config = load_config(config_path)

            logger.info("Starting ingestion...")

            result = ingest_sources(config)

            logger.info("Ingestion completed successfully.")

            self.send_json(result)

        except Exception as e:

            logger.exception("Ingestion failed")

            self.send_json(
                {
                    "status": "failed",
                    "error": str(e)
                },
                500
            )

    # Disable default console logging
    def log_message(self, format: str, *args: Any):
        return


def run():

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))

    server = ThreadingHTTPServer(
        (host, port),
        IngestionHandler
    )

    print("=" * 60)
    print(f"Server running at : http://localhost:{port}")
    print("=" * 60)
    print("Available Endpoints:")
    print("GET  /health")
    print("GET  /sources")
    print("GET  /records")
    print("POST /ingest")
    print("=" * 60)

    server.serve_forever()


if __name__ == "__main__":
    run()