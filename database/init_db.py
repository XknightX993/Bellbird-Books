from database import get_connection


def init_database():
    connection = get_connection()

    with open("database/schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()
