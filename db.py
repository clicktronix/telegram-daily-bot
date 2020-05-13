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
                    dbname="taskbot",
                    user="clicktronix",
                    password="23031994",
                    host="localhost",
                    port="5432",
                )
            except psycopg2.DatabaseError as error:
                logging.error(error)
                sys.exit()
            finally:
                logging.info("Connection to database opened successfully.")

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

    def update_rows(self, query):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected."
