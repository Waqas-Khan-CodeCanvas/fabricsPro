you are a databasse engineer design database for a tailor shop a complete tailor managment system using sqlite with offline first aproach and RBAC admin and staff , users , customers , orders , this is going to be used in a desktop application a production grade application , ready to implement database , industry standards , follow best practices , and also before diving into codeing first tell me what is you plane what how many tables which fields , relationships , and all these like things



this is a desktop application sqlite3 + customtkiner used on single pc at a time only admin , and staff roles













import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = "tailor_shop.db"
BACKUP_DIR = "backups"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.enable_pragmas()
        self.create_tables()

    # -----------------------------
    # PRAGMA SETTINGS (IMPORTANT)
    # -----------------------------
    def enable_pragmas(self):
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        self.conn.commit()

    # -----------------------------
    # TABLE CREATION
    # -----------------------------
    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin','staff')),
            phone TEXT,
            is_active INTEGER DEFAULT 1,
            is_deleted INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT UNIQUE,
            address TEXT,
            gender TEXT,
            notes TEXT,
            is_deleted INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS customer_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            measurements_json TEXT NOT NULL,
            created_by INTEGER,
            is_deleted INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            status TEXT DEFAULT 'created',
            total_amount REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            delivery_date DATE,
            is_deleted INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            design_notes TEXT,
            measurement_snapshot TEXT,
            price REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            is_deleted INTEGER DEFAULT 0,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT DEFAULT 'cash',
            received_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(received_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            entity_id INTEGER,
            details TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        """)

        self.conn.commit()

    # -----------------------------
    # GENERIC QUERY METHODS
    # -----------------------------
    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    # -----------------------------
    # SOFT DELETE HELPERS
    # -----------------------------
    def soft_delete(self, table, record_id):
        self.execute(
            f"UPDATE {table} SET is_deleted = 1 WHERE id = ?",
            (record_id,)
        )

    # -----------------------------
    # AUDIT LOG
    # -----------------------------
    def log_action(self, user_id, action, entity, entity_id, details=""):
        self.execute("""
            INSERT INTO audit_logs (user_id, action, entity, entity_id, details)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, action, entity, entity_id, details))

    # -----------------------------
    # BACKUP SYSTEM
    # -----------------------------
    def create_backup(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = f"{BACKUP_DIR}/backup_{timestamp}.db"

        self.conn.commit()
        shutil.copy2(DB_PATH, backup_file)

        self.cleanup_backups()
        return backup_file

    def cleanup_backups(self, keep_last=7):
        files = sorted(
            [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")],
            key=lambda x: os.path.getmtime(os.path.join(BACKUP_DIR, x))
        )

        if len(files) > keep_last:
            for f in files[:-keep_last]:
                os.remove(os.path.join(BACKUP_DIR, f))

    # -----------------------------
    # ORDER NUMBER GENERATOR
    # -----------------------------
    def generate_order_number(self):
        row = self.fetch_one("SELECT COUNT(*) as count FROM orders")
        count = row["count"] + 1
        return f"ORD-{count:05d}"






🏪 SHOP shop_name phone address currency 🧾 INVOICE invoice_prefix tax_percent invoice_footer 💰 BILLING advance_required default_discount 🧵 TAILORING default_delivery_days fitting_required 💾 BACKUP auto_backup backup_interval_hours keep_backups 🔐 SYSTEM theme language












customer_measurements [icon: ruler, color: orange] {
  id integer pk
  customer_id integer
  item_type string
  measurements_json string
  created_by integer
  is_deleted boolean
  created_at timestamp
}


why customer mearments in json


Good question — this is exactly the kind of design decision that matters in real systems.

You’re basically asking:

Why store measurements_json instead of separate columns like chest, waist, sleeve?

Let’s break it properly.

🧠 WHY JSON IS USED FOR customer_measurements

Because tailoring measurements are:

❗ NOT fixed schema data

They change depending on:

shirt
pant
coat
waistcoat
kids clothing
custom designs

So the structure is not stable.

📏 PROBLEM WITH FIXED COLUMNS

If you design like this:
chest
waist
sleeve
shoulder
inseam

❌ Issues:
Shirt needs chest + sleeve
Pants don’t need chest
Coat needs extra fields
Kids wear different measurements
New designs = ALTER TABLE every time

👉 That becomes a maintenance nightmare.

✅ WHY JSON IS BETTER HERE

Instead:
measurements_json = {
  "chest": 40,
  "waist": 32,
  "sleeve": 24,
  "shoulder": 18
}

✔ Benefits:
Fully flexible
No schema changes needed
Supports ANY garment type
Easy to extend
Works perfectly in SQLite for desktop apps
🧵 REAL TAILOR EXAMPLE
Shirt:
{ "chest": 40, "waist": 34, "sleeve": 25 }

Pant:
{ "waist": 32, "length": 40, "hip": 38 }

Coat:
{ "chest": 42, "shoulder": 19, "sleeve": 26, "length": 30 }

👉 Same column, different structure — this is the key idea.

⚖️ JSON vs NORMALIZED TABLE
Option A: Separate columns (BAD here)
chest	waist	sleeve	inseam
❌ rigid	❌ limited	❌ breaks flexibility	
Option B: JSON (GOOD here)
measurements_json
flexible object
🧠 IMPORTANT RULE (REAL WORLD DESIGN)
✔ Use JSON when:
Data structure changes per type
No fixed schema exists
Flexibility is more important than strict querying
❌ Avoid JSON when:
You need heavy filtering (SQL WHERE on fields)
Financial/accounting data
Reporting-heavy analytics
⚡ IN YOUR CASE (TAILOR SYSTEM)

JSON is PERFECT because:

✔ Measurements vary per garment
✔ You rarely filter by chest/waist in SQL
✔ Data is mostly displayed, not queried mathematically
✔ Desktop app (SQLite) handles JSON fine

🚀 PROFESSIONAL UPGRADE (OPTIONAL)

If you want a more advanced system later, you can evolve to:

Hybrid model:
JSON for full flexibility
AND key indexed fields for search

Example:
item_type = "shirt"
measurements_json = {...}
chest = 40   <-- optional indexed field
But for now → NOT needed.

🧭 FINAL VERDICT
👉 Using JSON in customer_measurements is:
✔ Correct
✔ Industry acceptable
✔ Best for desktop SQLite apps
✔ Future-proof for tailoring system

💡 SIMPLE WAY TO REMEMBER

Fixed columns = rigid system
JSON = flexible real-world tailoring system


If you want next step, I can help you design:
🔹 Measurement input UI (CustomTkinter form)
🔹 Measurement templates per garment type
🔹 Validation system for JSON fields
🔹 Print-ready measurement sheet (PDF)
Just tell me 👍


okay but in frontend ui i will be having a fixed form for shalwar kamees , shirt , coat , pant etc


Good — that actually clarifies the design direction a lot.

What you’re describing is:

🧵 Fixed UI forms per garment type + flexible backend storage

That combination is exactly how real tailoring/ERP systems are built.

So JSON is still correct — but now we design it smarter.

🧠 KEY IDEA (IMPORTANT)

You are NOT storing UI in the database.

You are storing:

“structured data that comes from different fixed forms”

So:

UI = fixed (Shalwar Kameez, Shirt, Pant, Coat)
Database = flexible (JSON)
📏 WHY THIS IS STILL THE RIGHT DESIGN

Even though UI is fixed, backend still needs flexibility because:

1. Different garments have different fields
Shirt form:
chest
collar
sleeve
shoulder
Pant form:
waist
length
hip
thigh
Coat form:
chest
shoulder
sleeve
length
back width

👉 These are NOT the same structure.

2. You don’t want 5 tables

If you avoid JSON, you’d need:

shirt_measurements
pant_measurements
coat_measurements
shalwar_measurements
etc...

❌ This becomes messy and unscalable.

✅ BEST PRACTICAL DESIGN (YOUR CASE)
Keep ONE table:

customer_measurements {
  id
  customer_id
  item_type
  measurements_json
  created_by
  is_deleted
  created_at
}

🧠 HOW IT WORKS WITH YOUR FIXED UI
UI Layer (CustomTkinter)

You do:

Shirt Form
Chest: [ 40 ]
Sleeve: [ 24 ]
Collar: [ 15 ]

Pant Form
Waist: [ 32 ]
Length: [ 40 ]
Thigh: [ 22 ]


Backend conversion
Shirt submit → JSON
{
  "chest": 40,
  "sleeve": 24,
  "collar": 15
}
Pant submit → JSON
{
  "waist": 32,
  "length": 40,
  "thigh": 22
}
🔄 IMPORTANT DESIGN PATTERN (THIS IS PRO LEVEL)

You are building:

🧩 “FORM → JSON → DATABASE” system

NOT:

fixed schema system
🧠 WHY THIS IS INDUSTRY STANDARD

This is how systems like:

Shopify product variants
ERP clothing modules
POS systems
Tailoring software

work internally:

UI is structured
DB is flexible

⚡ OPTIONAL UPGRADE (VERY POWERFUL IDEA)

You can improve this later with:

🔹 measurement_templates table
measurement_templates {
  id
  item_type
  fields_json
}

Example:

{
  "shirt": ["chest", "collar", "sleeve", "shoulder"],
  "pant": ["waist", "length", "thigh"]
}

👉 Then UI auto-generates forms (advanced level)

🚀 FINAL VERDICT
✔ Your approach is CORRECT:
Fixed UI forms
JSON storage backend
✔ This is BEST PRACTICE because:
UI is clean
DB is flexible
No schema explosion
Easy to extend new garment types
💡 SIMPLE MENTAL MODEL

Think like this:

🖥️ UI = “Form Designer”
🗄️ DB = “Flexible storage container”













orders [icon: shopping-bag, color: purple] {
  id integer pk
  order_number string
  customer_id integer
  status string
  total_amount float
  paid_amount float
  delivery_date date
  is_deleted boolean
  created_by integer
  created_at timestamp
}

here is one more thing why id , and order_id


Good question — this is one of those “why do databases feel repetitive?” moments, but it actually has a very important reason behind it.

Let’s clear it properly.

🧠 WHY BOTH id AND order_number EXIST

They are NOT the same thing and serve different purposes.

🔑 1. id (Primary Key — Internal System Identity)
id INTEGER PRIMARY KEY
Purpose:
Internal database identity
Used for relationships (foreign keys)
Never changes
Fast indexing
Guaranteed uniqueness
Example:
orders.id = 17
🧾 2. order_number (Business / Human-Friendly ID)
order_number = ORD-00017
Purpose:
Shown to users
Printed on invoices
Used in search
Can include formatting
Example:
ORD-00017
TAILOR-2026-001
INV-1045
⚖️ SIMPLE DIFFERENCE
Type	id	order_number
Purpose	system	user/business
Visible to user	❌ no	✅ yes
Can change	❌ never	⚠️ theoretically yes
Format	number	formatted string
Speed	very fast	slower






order_items [icon: layers, color: purple] { id integer pk order_id integer item_type string design_notes string measurement_snapshot string price float status string is_deleted boolean } explain this each field

Let’s go field by field and connect it to how a real tailor shop actually works. This table is basically the heart of your production workflow, so every field has a purpose.

🧵 order_items TABLE EXPLAINED

This table represents:

👉 Each individual garment inside an order

Example:
One order = 2 shirts + 1 pant → 3 rows in order_items

🧾 1. id (Primary Key)
id integer pk
Meaning:
Unique identity of each garment record
Auto-generated by SQLite
Why needed:
Used internally for updates/deletes
Used in joins with other tables
Example:
1, 2, 3, 4…
🔗 2. order_id (Foreign Key)
order_id integer
Meaning:
Links item to its parent order
Example:
Order #10 contains:
Shirt → order_id = 10
Pant → order_id = 10
Why important:

Builds relationship:

one order → many items

👕 3. item_type
item_type string
Meaning:

Type of garment

Examples:
shirt
pant
coat
shalwar kameez
waistcoat
Why important:
Drives UI form selection
Controls measurement fields
Helps pricing rules
✏️ 4. design_notes
design_notes string
Meaning:

Special instructions for stitching

Examples:
“Slim fit”
“Add pocket on left side”
“Golden buttons”
“Embroidery on collar”
Why important:
Tailor-specific instructions
Custom customer requirements
📏 5. measurement_snapshot
measurement_snapshot string
Meaning:

Frozen copy of measurements at order time

Usually stored as JSON:

{
  "chest": 40,
  "waist": 32,
  "sleeve": 24
}
Why important:

This is VERY critical:

👉 Even if customer changes measurements later
👉 This order must remain unchanged

So snapshot ensures:

✔ historical accuracy
✔ no data corruption
✔ invoice consistency

💰 6. price
price float
Meaning:

Cost of this specific garment

Example:
Shirt = 2000
Pant = 1500
Why important:
Enables item-level billing
Supports discounts per item
Allows partial pricing
🔄 7. status
status string
Meaning:

Current stage of THIS garment

Example values:
pending
cutting
stitching
fitting
completed
delivered
Why important:

Because each garment may move differently:

Example:

Shirt → completed
Pant → still stitching

👉 This cannot be handled at order level only

🗑️ 8. is_deleted
is_deleted boolean
Meaning:

Soft delete flag

Values:
0 = active
1 = deleted
Why important:
Prevents permanent data loss
Allows recovery
Keeps audit history intact
🧠 FULL REAL-WORLD SUMMARY

This table answers:

“What exactly is being stitched?”

Each row = one garment with:

Concept	Meaning
id	system identity
order_id	which order it belongs to
item_type	what garment it is
design_notes	how to stitch it
measurement_snapshot	body data at that time
price	cost of that garment
status	progress of stitching
is_deleted	soft delete control
🧵 SIMPLE ANALOGY

Think of:

🧾 order = bill
🧵 order_items = items on bill

Like:

Shirt → 2000
Pant → 1500
Coat → 3000

Each item has its own lifecycle.

🚀 WHY THIS DESIGN IS STRONG

✔ supports multiple garments per order
✔ supports independent tracking
✔ supports per-item pricing
✔ supports real tailoring workflow
✔ used in ERP/POS systems

💡 KEY INSIGHT

Order = “customer request”
Order_item = “actual work unit”















here is one an othre problem that in orders , order_item having same field status , and mearments and order_item having same fields item_type


Good — this is exactly the kind of “duplication feeling” that shows you’re thinking like a real system designer.

But this is not actually a problem in your design. It just needs correct responsibility separation.

Let’s fix your confusion clearly.

🧠 1. Why status exists in BOTH orders and order_items

They are NOT duplicates. They represent two different levels of tracking.

🧾 orders.status = OVERALL ORDER STATUS

This is the big picture status

Meaning:

“What is the state of the whole order?”

Example:
created
in_progress
ready
delivered
Example scenario:
Order #10 → in_progress

Even if some items are done, the order is still “in_progress”.

🧵 order_items.status = ITEM LEVEL STATUS

This is per garment tracking

Meaning:

“What is the state of THIS specific item?”

Example:
Shirt → completed
Pant → stitching
Coat → cutting
⚖️ SIMPLE RULE
Level	Meaning
orders.status	overall progress
order_items.status	individual garment progress
🧠 REAL-LIFE ANALOGY

Think of a school:

🏫 School = order
📚 Students = order_items
School status = “session ongoing”
Student status = “passed / failed / exam pending”

Same idea.

🧵 2. Why item_type exists in BOTH tables (or seems repeated)

You noticed:

orders
order_items
measurements

all somehow relate to item_type

But again — they serve DIFFERENT purposes.

🧾 A) In order_items.item_type
Purpose:

What garment is being made?

Example:
shirt
pant
coat

This is the WORK UNIT TYPE

📏 B) In customer_measurements.item_type
Purpose:

What garment these measurements belong to?

Example:
shirt measurements
pant measurements

This is the BODY DATA TYPE

🧠 KEY DIFFERENCE
Table	Meaning of item_type
order_items	what is being stitched
measurements	what body data belongs to
orders	❌ should NOT have item_type
❗ IMPORTANT INSIGHT

You are NOT duplicating data.

You are modeling:

🔹 same concept in different contexts

🧠 WHY THIS IS ACTUALLY GOOD DESIGN

Because tailoring system has 3 layers:

🧾 1. ORDER (business level)
customer
total bill
overall status
🧵 2. ORDER_ITEMS (work level)
shirt/pant/coat
price
stitching status
📏 3. MEASUREMENTS (body data level)
chest
waist
sleeve
⚠️ WHAT WOULD BE A BAD DESIGN

If you REMOVE these separations:

❌ Everything inside orders:
no item tracking
no per-garment status
no flexibility
❌ Everything duplicated everywhere:
messy updates
inconsistent data
hard to scale
🚀 FINAL CLEAN RULE (VERY IMPORTANT)

Each table should represent ONE responsibility only.

✔ orders

“What did customer order?”

✔ order_items

“What are we stitching?”

✔ measurements

“What are the body dimensions?”

🧠 SIMPLE MEMORY TRICK

Think like a factory:

orders = customer invoice
order_items = production units
measurements = raw material specs
🧭 FINAL VERDICT

✔ status duplication = NOT a problem (different levels)
✔ item_type repetition = correct (different contexts)
✔ your design = actually professional and scalable






payments [icon: credit-card, color: yellow] {
  id integer pk
  order_id integer
  amount float
  method string
  received_by integer
  created_at timestamp
}


This table is your payments module, and it’s actually one of the most important parts of a real business system because it controls money flow.

Let’s break it properly field by field.

💰 payments TABLE EXPLAINED

This table stores:

👉 Every payment made against an order (can be full or partial)

🧾 1. id (Primary Key)
id integer pk
Meaning:
Unique identifier for each payment record
Auto-generated
Why important:
Used internally for updates, deletes, tracking
Never shown to user
🔗 2. order_id (Foreign Key)
order_id integer
Meaning:

Links payment to a specific order

Example:
Order #10 → Payment 1
Order #10 → Payment 2 (advance + remaining)
Why important:
One order can have multiple payments
Supports partial payments system
💵 3. amount
amount float
Meaning:

Money received in this transaction

Example:
1000 (advance)
2000 (final payment)
Why important:
Tracks total money flow
Used to calculate remaining balance
💳 4. method
method string
Meaning:

How payment was received

Example:
cash
card
bank transfer
jazzcash / easypaisa
Why important:
Financial reporting
Payment tracking
Audit purposes
👤 5. received_by
received_by integer
Meaning:

Which staff/admin received the money

Example:
Admin collected payment
Staff took cash
Why important:
Accountability
Fraud prevention
Staff performance tracking

👉 This links to users.id

⏰ 6. created_at
created_at timestamp
Meaning:

When the payment was recorded in system

Why important:
Daily sales reports
Financial tracking
Audit logs
🧠 HOW THIS TABLE WORKS IN REAL LIFE
Example Order:
Order	Total
ORD-001	5000
Payments:
Payment	Amount
Advance	2000
Remaining	3000

So table becomes:

order_id | amount | method | received_by
-----------------------------------------
1        | 2000   | cash   | admin
1        | 3000   | cash   | staff
⚖️ WHY THIS TABLE EXISTS (VERY IMPORTANT)

You might think:

“Why not just store paid_amount in orders?”

You already have:

paid_amount float
Answer:

Because:

❌ orders.paid_amount = summary only
✅ payments table = detailed history
🧠 DIFFERENCE
Field	Purpose
orders.paid_amount	total received (calculated)
payments table	detailed transaction history
🚀 WHY THIS IS INDUSTRY STANDARD

This design is used in:

ERP systems
Accounting software
POS systems
Banking apps

Because money systems require:

✔ traceability
✔ transparency
✔ audit history

🔥 REAL INSIGHT

Without this table:

You cannot explain WHERE money came from.

With this table:

You can reconstruct every payment step-by-step.

🧭 FINAL SUMMARY

This table enables:

💰 Payment tracking
📊 Sales reports
👤 Staff accountability
🔁 Partial payments
📜 Financial audit trail
💡 SIMPLE MENTAL MODEL

Think like this:

🧾 orders = “what customer owes”
💰 payments = “what customer paid”


























final code 


Perfect — this is a clean, production-level ER design. Now I’ll convert it into a real SQLite + Python production-ready database layer.

This will be structured like a real backend system used in desktop ERP apps.

🏭 WHAT YOU ARE GETTING

You will get a ready-to-copy database.py with:

✅ Production features
SQLite connection manager
WAL mode (crash-safe)
Foreign keys ON
Auto table creation
Clean schema execution
🔐 Business logic helpers
Soft delete pattern support
Order number generator
Audit log function
Safe query methods
⚡ Best practices
No raw SQL in UI
Reusable DB layer
Clean architecture
Scalable design
📦 FINAL PRODUCTION CODE (COPY PASTE


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



🧠 WHY THIS IS PRODUCTION-READY
🔐 1. Safe SQLite setup


WAL mode enabled


foreign keys enforced


stable performance



🧱 2. Clean architecture


single DB class


no SQL in UI layer


reusable methods



📜 3. Audit system included


full traceability of actions



🗑️ 4. Soft delete supported


safe data handling



⚡ 5. Scalable structure


ready for expansion (invoice, reports, analytics)



🚀 WHAT YOU HAVE NOW
You now have a:

🏭 REAL production-grade tailor shop database backend

This is already:


ERP-level structure


desktop-app ready


scalable for future features



👉 NEXT STEP (HIGHLY RECOMMENDED)
Now you should move to:
🔹 1. CustomTkinter UI integration layer
🔹 2. Login system (RBAC enforcement)
🔹 3. Order workflow engine (status automation)
🔹 4. Invoice generator (PDF printing system)
🔹 5. Dashboard (sales + pending orders)

If you want, I can next build:
👉 Full backend service layer (clean architecture version)
👉 or Complete CustomTkinter screens connected to this DB
👉 or Invoice PDF system (professional billing)










audit_logs [icon: file-text, color: red] {
  id integer pk
  user_id integer
  action string
  entity string
  entity_id integer
  details string
  created_at timestamp
}


Good — this is one of the most important “production-grade” tables in your entire system. Many beginners skip it, but real ERP / POS systems always include it.

Let’s break it properly.

📜 audit_logs TABLE EXPLAINED

This table stores:

👉 “Who did what, when, and on which record”

It is your system memory of actions.

🧾 1. id (Primary Key)
id integer pk
Meaning:
Unique identifier for each log entry
Auto-incremented
Why important:
Helps track each action separately
Used for searching logs
👤 2. user_id
user_id integer
Meaning:

The user (admin or staff) who performed the action

Example:
Admin created order
Staff updated measurement
Why important:
Accountability
Security tracking
Staff monitoring

👉 Links to users.id

⚡ 3. action
action string
Meaning:

What action was performed

Examples:
CREATE_ORDER
UPDATE_ORDER
DELETE_CUSTOMER
ADD_PAYMENT
LOGIN
UPDATE_MEASUREMENT
Why important:
Core activity tracking
Used in reports
Used in debugging
📦 4. entity
entity string
Meaning:

Which table/module was affected

Examples:
orders
customers
payments
order_items
Why important:
Helps categorize logs
Used for filtering history
🔗 5. entity_id
entity_id integer
Meaning:

ID of the affected record

Example:
Order ID = 15
Customer ID = 3
Why important:
Connects log to actual data
Enables traceability
📝 6. details
details string
Meaning:

Extra information about what changed

Examples:
Changed status from 'pending' to 'completed'
Added payment of 2000 via cash
Updated phone number from 0300... to 0312...
Why important:
Human-readable explanation
Debugging support
Audit transparency
⏰ 7. created_at
created_at timestamp
Meaning:

When the action happened

Why important:
Timeline tracking
Reports
Security audits
🧠 HOW THIS WORKS IN REAL SYSTEM
Example Flow:
Admin updates order:
User: Admin
Action: UPDATE_ORDER
Entity: orders
Entity ID: 10
Details: status changed from stitching to completed
Time: 10:30 AM
Staff adds payment:
User: Staff
Action: ADD_PAYMENT
Entity: payments
Entity ID: 5
Details: received 2000 cash
🔥 WHY THIS TABLE IS VERY IMPORTANT

Without audit logs:

❌ No idea who changed data
❌ No debugging history
❌ No fraud tracking
❌ No accountability

With audit logs:

✔ Full system traceability
✔ Debugging becomes easy
✔ Staff accountability
✔ Business transparency

🧠 SIMPLE ANALOGY

Think like CCTV for your database:

📜 audit_logs = “security camera of your system”

Everything is recorded.

⚖️ INDUSTRY USE

This pattern is used in:

Banking systems
ERP systems
Hospital systems
POS systems
Government software

Because:

“If it matters, it must be logged.”

🚀 OPTIONAL UPGRADE (VERY USEFUL LATER)

You can enhance this table with:

🔹 before_value / after_value (advanced tracking)
old_value TEXT
new_value TEXT
🔹 ip_address (if networked later)
ip_address TEXT
🔹 module_name (UI grouping)
module TEXT
🧭 FINAL SUMMARY

This table gives you:

🔐 Security
📊 Activity tracking
🧾 Change history
🐞 Debugging power
👥 User accountability
💡 SIMPLE MEMORY RULE

If data can change → log it
If money is involved → log it
If users act → log it