from ingestion_service.database import SessionLocal
from ingestion_service.models import ApiRecord


def save_records(source, endpoint, records):

    session = SessionLocal()

    try:

        inserted = 0
        skipped = 0

        for record in records:

            external_id = record.get("id")

            existing = (
                session.query(ApiRecord)
                .filter_by(
                    source=source,
                    external_id=external_id
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            session.add(
                ApiRecord(
                    source=source,
                    external_id=external_id,
                    endpoint=endpoint,
                    data=record
                )
            )

            inserted += 1

        session.commit()

        print(f"Inserted: {inserted}, Skipped: {skipped}")

    except Exception as e:

        session.rollback()
        print(e)
        raise

    finally:
        session.close()