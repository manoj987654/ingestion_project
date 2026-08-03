from ingestion_service.client import fetch_data
from ingestion_service.pagination import build_params
from ingestion_service.storage import save_records


def ingest_sources(config):

    summary = []

    total_records = 0

    for source in config["sources"]:

        name = source["name"]
        url = source["url"]
        pagination = source.get("pagination")
        record_path = source.get("record_path")

        page = 0
        records_saved = 0

        while True:

            params = build_params(pagination, page)

            response = fetch_data(url, params=params)

            if record_path:
                records = response.get(record_path, [])
            else:
                records = response

            if not records:
                break

            save_records(name, url, records)

            records_saved += len(records)

            page += 1

            if pagination and page >= pagination.get("max_pages", 1):
                break

        total_records += records_saved

        summary.append({
            "source": name,
            "records_ingested": records_saved,
            "pages_processed": page
        })

    return {
        "status": "success",
        "summary": summary,
        "total_records": total_records
    }