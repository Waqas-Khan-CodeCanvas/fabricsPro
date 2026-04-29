from database.database import Database
import json

db = Database()


# =========================
# HELP MENU
# =========================
def show_menu():
    print("\n" + "=" * 50)
    print("🏪 TAILOR SHOP SYSTEM - CLI TESTER")
    print("=" * 50)

    print("""
1. Add Customer
2. View Customers
3. Create Order
4. View Orders
5. Add Order Item
6. Add Payment
7. View Payments
8. View Order Items
9. Add Measurement
10. View Audit Logs
0. Exit
""")


# =========================
# CUSTOMER
# =========================
def add_customer():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    address = input("Address: ")

    db.execute("""
        INSERT INTO customers (name, phone, email, address, gender, notes, is_deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, '', '', 0, datetime('now'), datetime('now'))
    """, (name, phone, email, address))

    print("✅ Customer added")


def view_customers():
    rows = db.fetch_all("SELECT * FROM customers WHERE is_deleted = 0")
    for r in rows:
        print(dict(r))


# =========================
# ORDER
# =========================
def create_order():
    customer_id = input("Customer ID: ")
    total = float(input("Total Amount: "))
    paid = float(input("Paid Amount: "))
    delivery = input("Delivery Date (YYYY-MM-DD): ")

    order_no = db.generate_order_number()

    db.execute("""
        INSERT INTO orders (order_number, customer_id, status, total_amount, paid_amount, delivery_date, is_deleted, created_by, created_at, updated_at)
        VALUES (?, ?, 'created', ?, ?, ?, 0, 1, datetime('now'), datetime('now'))
    """, (order_no, customer_id, total, paid, delivery))

    print(f"✅ Order created: {order_no}")


def view_orders():
    rows = db.fetch_all("SELECT * FROM orders WHERE is_deleted = 0")
    for r in rows:
        print(dict(r))


# =========================
# ORDER ITEMS
# =========================
def add_order_item():
    order_id = input("Order ID: ")
    item_type = input("Item Type (shirt/pant/etc): ")
    price = float(input("Price: "))
    notes = input("Design Notes: ")

    measurements = input("Measurement JSON: ")

    db.execute("""
        INSERT INTO order_items (order_id, item_type, design_notes, measurement_snapshot, price, status, is_deleted)
        VALUES (?, ?, ?, ?, ?, 'pending', 0)
    """, (order_id, item_type, notes, measurements, price))

    print("✅ Order item added")


def view_order_items():
    rows = db.fetch_all("SELECT * FROM order_items WHERE is_deleted = 0")
    for r in rows:
        print(dict(r))


# =========================
# PAYMENTS
# =========================
def add_payment():
    order_id = input("Order ID: ")
    amount = float(input("Amount: "))
    method = input("Method (cash/card/etc): ")

    db.execute("""
        INSERT INTO payments (order_id, amount, method, received_by, created_at)
        VALUES (?, ?, ?, 1, datetime('now'))
    """, (order_id, amount, method))

    print("✅ Payment recorded")


def view_payments():
    rows = db.fetch_all("SELECT * FROM payments")
    for r in rows:
        print(dict(r))


# =========================
# MEASUREMENTS
# =========================
def add_measurement():
    customer_id = input("Customer ID: ")
    item_type = input("Item Type: ")
    data = input("Measurement JSON: ")

    db.execute("""
        INSERT INTO customer_measurements (customer_id, item_type, measurements_json, created_by, created_at, updated_at)
        VALUES (?, ?, ?, 1, datetime('now'), datetime('now'))
    """, (customer_id, item_type, data))

    print("✅ Measurement added")


# =========================
# AUDIT LOGS
# =========================
def view_logs():
    rows = db.fetch_all("SELECT * FROM audit_logs ORDER BY created_at DESC")
    for r in rows:
        print(dict(r))


# =========================
# MAIN LOOP
# =========================
while True:
    show_menu()
    choice = input("Select option: ")

    if choice == "1":
        add_customer()

    elif choice == "2":
        view_customers()

    elif choice == "3":
        create_order()

    elif choice == "4":
        view_orders()

    elif choice == "5":
        add_order_item()

    elif choice == "6":
        add_payment()

    elif choice == "7":
        view_payments()

    elif choice == "8":
        view_order_items()

    elif choice == "9":
        add_measurement()

    elif choice == "10":
        view_logs()

    elif choice == "0":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid option")