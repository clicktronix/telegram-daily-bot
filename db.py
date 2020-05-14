"""Connect database."""
import sys
import logging
import psycopg2
from psycopg2.extras import DictCursor


class Database:
    """PostgreSQL Database class."""

    def __init__(self, config):
        """
        A database connection that can be safely instantiated once, and then
        passed around inside a class or between functions.
        """
        self.host = config.DATABASE_HOST
        self.username = config.DATABASE_USERNAME
        self.password = config.DATABASE_PASSWORD
        self.port = config.DATABASE_PORT
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a postgres database"""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                )
                self.init_tables()
            except psycopg2.DatabaseError as error:
                logging.error(error)
                sys.exit()
            finally:
                logging.info("Connection to database opened successfully.")

    def init_tables(self):
        """Tables initializing"""
        with self.conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS chatIds (id integer PRIMARY KEY);")
        cur.close()
        return

    def select_rows(self, query):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
        cur.close()
        return records

    def select_rows_dict_cursor(self, query):
        """Run a SQL query to select rows from table and return dictionaries."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def update_rows(self, query, args):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, args)
            self.conn.commit()
            cur.close()
