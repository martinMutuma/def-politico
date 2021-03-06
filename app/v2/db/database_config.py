import psycopg2
from instance.config import app_config
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
import sys
import os


class Database:
    """ This class will handle all our database logic """

    def __init__(self, config_type='development'):
        self.config_type = config_type

    def init_connection(self):
        """ create a connection and a cursor  to access db """

        config = app_config[self.config_type]
        database_url = config.DATABASE_URL
        self.admin_email = config.ADMIN_EMAIL
        self.admin_password = config.ADMIN_PASSWORD

        try:
            global conn, cur

            conn = psycopg2.connect(database_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            return True
        except Exception as error:
            print('Error. Unable to establish Database connection')
            print(error)

            return False

    def create_db(self):
        """ Creates all the tables for the database """

        for query in table_queries:
            cur.execute(query)

        conn.commit()

    def drop_db(self):
        """ Drops all tables """

        for table in table_names:
            cur.execute('DROP TABLE IF EXISTS {} CASCADE'.format(table))

        conn.commit()

    def create_super_user(self):
        """ creates a default user who is an admin """

        query = "SELECT * FROM users WHERE email = 'bedank6@gmail.com'"
        cur.execute(query)
        user = cur.fetchone()

        if not user:
            cur.execute("""INSERT INTO users (firstname, lastname, phonenumber,
            email, password, passport_url, admin) VALUES ('Bedan', 'Kimani',
            '0712068754', '{}', '{}',
            'https://cdn2.iconfinder.com/data/icons/avatar-2/512/kan_boy-512.png',
            True)
            """.format(
                self.admin_email, generate_password_hash(self.admin_password)))
            conn.commit()

    def insert(self, query):
        """ Add new item in the db """

        cur.execute(query)
        data = cur.fetchone()
        conn.commit()
        return data

    def get_one(self, query):
        """ Get one item form the db """

        cur.execute(query)
        data = cur.fetchone()
        return data

    def get_all(self, query):
        """ Get all items from the db """

        cur.execute(query)
        data = cur.fetchall()
        return data

    def execute(self, query):
        """ Execute any other query """

        cur.execute(query)
        conn.commit()

    def truncate(self):
        """ Clear all database table """

        cur.execute('TRUNCATE TABLE ' + ','.join(table_names) + ' CASCADE')
        conn.commit()


table_queries = [
    """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(250) NOT NULL,
        lastname VARCHAR(250) NOT NULL,
        othername VARCHAR(250) NULL,
        email VARCHAR(250) NOT NULL,
        phonenumber VARCHAR(250) NULL,
        password VARCHAR(250) NOT NULL,
        passport_url VARCHAR(250) NOT NULL DEFAULT 'https://cdn2.iconfinder.com/data/icons/avatar-2/512/kan_boy-512.png',
        admin BOOLEAN NOT NULL DEFAULT FALSE,
        UNIQUE(email)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS parties(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(250) NOT NULL,
        hq_address VARCHAR(250) NOT NULL,
        logo_url VARCHAR(250) NULL,
        slogan VARCHAR(250) NOT NULL,
        manifesto VARCHAR(250) NOT NULL,
        UNIQUE(name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS offices(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(250) NOT NULL,
        type VARCHAR(250) NOT NULL,
        UNIQUE(name, type)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS candidates(
        id SERIAL NOT NULL,
        party INTEGER NOT NULL DEFAULT 0,
        office INTEGER NOT NULL DEFAULT 0,
        candidate INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (candidate, office),
        UNIQUE(candidate),
        FOREIGN KEY (party) REFERENCES parties(id) ON DELETE CASCADE,
        FOREIGN KEY (office) REFERENCES offices(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate) REFERENCES users(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS votes(
        id SERIAL NOT NULL,
        createdby INTEGER NOT NULL DEFAULT 0,
        office INTEGER NOT NULL DEFAULT 0,
        candidate INTEGER NOT NULL DEFAULT 0,
        createdOn  TIMESTAMP WITHOUT TIME ZONE \
        DEFAULT (NOW() AT TIME ZONE 'utc'),
        PRIMARY KEY (createdby, office),
        FOREIGN KEY (createdby) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (office) REFERENCES offices(id) ON DELETE CASCADE,
        FOREIGN KEY (candidate) REFERENCES candidates(candidate) ON DELETE CASCADE
    )
    """
]


table_names = [
    'users',
    'parties',
    'offices',
    'candidates',
    'votes'
]
