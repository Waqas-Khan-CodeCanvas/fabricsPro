import sqlite3
import os
from datetime import datetime

DB_NAME = "tailor_shop.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._configure_db()
        self._create_tables()

    # =========================
    # DB CONFIGURATION
    # =========================
    def _configure_db(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute("PRAGMA journal_mode = WAL;")
        self.cursor.execute("PRAGMA synchronous = NORMAL;")
        self.conn.commit()

    # =========================
    # TABLE CREATION
    # =========================
    def _create_tables(self):

        self.cursor.executescript("""

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT,
            phone TEXT,
            email TEXT,
            is_active INTEGER DEFAULT 1,
            is_deleted INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            gender TEXT,
            notes TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS customer_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            item_type TEXT,
            measurements_json TEXT,
            created_by INTEGER,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE,
            customer_id INTEGER,
            status TEXT,
            total_amount REAL,
            paid_amount REAL,
            delivery_date TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_type TEXT,
            design_notes TEXT,
            measurement_snapshot TEXT,
            price REAL,
            status TEXT,
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            amount REAL,
            method TEXT,
            received_by INTEGER,
            created_at TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(received_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            entity TEXT,
            entity_id INTEGER,
            details TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            data_type TEXT,
            category TEXT,
            description TEXT,
            is_editable INTEGER DEFAULT 1,
            created_at TEXT,
            updated_at TEXT
        );

        """)

        self.conn.commit()

    # =========================
    # BASIC QUERY METHODS
    # =========================
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    # =========================
    # ORDER NUMBER GENERATOR
    # =========================
    def generate_order_number(self):
        self.cursor.execute("SELECT COUNT(*) FROM orders")
        count = self.cursor.fetchone()[0] + 1
        return f"ORD-{count:05d}"

    # =========================
    # SOFT DELETE HELPERS
    # =========================
    def soft_delete(self, table, record_id):
        self.execute(
            f"UPDATE {table} SET is_deleted = 1 WHERE id = ?",
            (record_id,)
        )

    # =========================
    # AUDIT LOG
    # =========================
    def log_action(self, user_id, action, entity, entity_id, details=""):
        self.execute("""
            INSERT INTO audit_logs
            (user_id, action, entity, entity_id, details, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            action,
            entity,
            entity_id,
            details,
            datetime.now().isoformat()
        ))

    # =========================
    # CLOSE CONNECTION
    # =========================
    def close(self):
        self.conn.close()