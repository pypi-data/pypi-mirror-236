import psycopg2


def generate_dummy_data():
    data = [
        ("Alice", 25, "alice@example.com", "123 Main St"),
        ("Bob", 30, "bob@example.com", "456 Elm St"),
        ("Charlie", 22, "charlie@example.com", "789 Oak St"),
        ("David", 35, "david@example.com", "101 Maple Ave"),
        ("Eva", 28, "eva@example.com", "202 Pine Rd"),
        ("Frank", 40, "frank@example.com", "123 Main St"),
        ("Grace", 29, "grace@example.com", "456 Elm St"),
        ("Hank", 27, "hank@example.com", "789 Oak St"),
        ("Ivy", 32, "ivy@example.com", "101 Maple Ave"),
        ("Jack", 26, "jack@example.com", "202 Pine Rd"),
    ]

    return data


def create_table(url):

    while True:
        try:
            connection = psycopg2.connect(url)
        except psycopg2.OperationalError:
            continue
        break
    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS dummy_data (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INTEGER,
            email VARCHAR(100),
            address VARCHAR(200)
        )
    '''

    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def insert_data(url):

    connection = psycopg2.connect(url)
    cursor = connection.cursor()

    data = generate_dummy_data()

    insert_query = "INSERT INTO dummy_data (name, age, email, address) VALUES (%s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    USER = "pgsqldev"
    PASSWORD = "Welcome4$"
    DB = "testdb"
    db_url = f"postgresql://{USER}:{PASSWORD}@localhost:5432/{DB}"
    create_table(url=db_url)
    print("table created")
    insert_data(url=db_url)
    print("data inserted")
