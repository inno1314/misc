import sqlite3


class DBHandler:
    def __init__(self, db_path="connections.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY,
                    src_ip TEXT,
                    src_port INTEGER,
                    dst_ip TEXT,
                    dst_port INTEGER,
                    protocol TEXT,
                    domain TEXT,
                    timestamp TEXT
                )
            """)

    def save(self, src_ip, src_port, dst_ip, dst_port, protocol, domain, timestamp):
        with self._connect() as c:
            c.execute(
                """
                INSERT INTO connections
                (src_ip, src_port, dst_ip, dst_port, protocol, domain, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (src_ip, src_port, dst_ip, dst_port, protocol, domain, timestamp),
            )
