from sqlalchemy import inspect, text

from app.database import Base, _upgrade_contacts_schema, engine


def test_upgrade_contacts_schema_adds_photo_to_existing_table():
    Base.metadata.drop_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE contacts (id INTEGER PRIMARY KEY)"))
        connection.execute(text("INSERT INTO contacts (id) VALUES (1)"))

    _upgrade_contacts_schema()
    _upgrade_contacts_schema()

    columns = {column["name"] for column in inspect(engine).get_columns("contacts")}
    assert "photo" in columns
    with engine.connect() as connection:
        assert connection.execute(text("SELECT id FROM contacts")).scalar_one() == 1
