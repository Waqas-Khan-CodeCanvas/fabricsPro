import sqlite3
from datetime import datetime

DB_NAME = "tailor_shop.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed():
    conn = connect()
    cur = conn.cursor()

    now = datetime.now().isoformat()

    # =========================
    # USERS
    # =========================
    cur.executemany("""
        INSERT INTO users (username, password, role, phone, email, is_active, is_deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("admin", "admin123", "admin", "03001111111", "admin@tailor.com", 1, 0, now, now),
        ("staff1", "staff123", "staff", "03002222222", "staff1@tailor.com", 1, 0, now, now),
    ])

    # =========================
    # CUSTOMERS
    # =========================
    cur.executemany("""
        INSERT INTO customers (name, phone, email, address, gender, notes, is_deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("Ali Khan", "03001234567", "ali@gmail.com", "Peshawar Saddar", "male", "Regular customer", 0, now, now),
        ("Ahmed Ali", "03007654321", "ahmed@gmail.com", "Hayatabad", "male", "VIP customer", 0, now, now),
    ])

    # =========================
    # CUSTOMER MEASUREMENTS
    # =========================
    cur.executemany("""
        INSERT INTO customer_measurements (customer_id, item_type, measurements_json, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "shirt", '{"chest":40,"waist":34,"sleeve":24,"shoulder":18}', 1, now, now),
        (1, "pant", '{"waist":32,"length":40,"thigh":22}', 1, now, now),
        (2, "shalwar_kameez", '{"chest":42,"waist":36,"sleeve":25}', 2, now, now),
    ])

    # =========================
    # ORDERS
    # =========================
    cur.executemany("""
        INSERT INTO orders (order_number, customer_id, status, total_amount, paid_amount, delivery_date, is_deleted, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("ORD-00001", 1, "in_progress", 5000, 2000, "2026-05-05", 0, 1, now, now),
        ("ORD-00002", 2, "created", 8000, 0, "2026-05-10", 0, 2, now, now),
    ])

    # =========================
    # ORDER ITEMS
    # =========================
    cur.executemany("""
        INSERT INTO order_items (order_id, item_type, design_notes, measurement_snapshot, price, status, is_deleted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, "shirt", "Slim fit, white color", '{"chest":40,"waist":34,"sleeve":24}', 2000, "stitching", 0),
        (1, "pant", "Black straight fit", '{"waist":32,"length":40}', 1500, "pending", 0),
        (2, "shalwar_kameez", "Wedding embroidery", '{"chest":42,"waist":36}', 4500, "cutting", 0),
    ])

    # =========================
    # PAYMENTS
    # =========================
    cur.executemany("""
        INSERT INTO payments (order_id, amount, method, received_by, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 2000, "cash", 1, now),
        (2, 1000, "card", 2, now),
    ])

    # =========================
    # AUDIT LOGS
    # =========================
    cur.executemany("""
        INSERT INTO audit_logs (user_id, action, entity, entity_id, details, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "CREATE_ORDER", "orders", 1, "Created order ORD-00001", now),
        (2, "ADD_PAYMENT", "payments", 2, "Received 1000 via card", now),
        (1, "UPDATE_ORDER", "orders", 1, "Status updated", now),
    ])

    # =========================
    # SETTINGS
    # =========================
    cur.executemany("""
        INSERT INTO settings (key, value, data_type, category, description, is_editable, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("shop_name", "Al Noor Tailors", "string", "shop", "Shop name", 1, now, now),
        ("phone", "03001111111", "string", "shop", "Contact number", 1, now, now),
        ("currency", "PKR", "string", "shop", "Currency", 1, now, now),

        ("invoice_prefix", "ORD", "string", "invoice", "Order prefix", 1, now, now),
        ("tax_percent", "0", "number", "invoice", "Tax", 1, now, now),

        ("auto_backup", "true", "boolean", "backup", "Auto backup", 1, now, now),
        ("backup_interval_hours", "6", "number", "backup", "Backup interval", 1, now, now),

        ("theme", "dark", "string", "system", "UI theme", 1, now, now),
    ])

    conn.commit()
    conn.close()

    print("✅ Dummy data inserted successfully!")


if __name__ == "__main__":
    seed()