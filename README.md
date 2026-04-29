# 🧵 Tailor Shop Management System (Desktop App)

A **modern, offline-first Tailor Shop Management System** built with **Python (CustomTkinter) + SQLite3**, designed for small to medium tailoring businesses to manage customers, orders, measurements, payments, and staff efficiently.

---

## 🚀 Features

### 👤 User Management (RBAC)
- Admin & Staff roles
- Secure login system
- Role-based permissions

### 👥 Customer Management
- Add / edit / delete customers
- Store contact details & notes
- Soft delete support

### 🧵 Order Management
- Create multiple orders per customer
- Track order status (pending, stitching, completed, delivered)
- Auto-generated order numbers

### 📏 Measurement System
- Store customer measurements per garment type
- JSON-based flexible measurement storage
- Measurement history tracking

### 🧵 Order Items System
- Multiple garments per order
- Design notes per item
- Individual item status tracking
- Frozen measurement snapshot per item

### 💰 Payments System
- Partial & full payments support
- Multiple payment methods (cash, card, etc.)
- Payment history tracking

### 📊 Audit Logs
- Track all system actions
- User activity monitoring
- Full traceability for security

### ⚙️ Settings System
- Shop configuration (name, phone, currency)
- Invoice settings
- Backup settings
- System preferences

### 💾 Offline-First Architecture
- Fully functional without internet
- Local SQLite database
- Fast & lightweight performance

---

## 🏗️ Tech Stack

- **Python 3.x**
- **SQLite3** (local database)
- **CustomTkinter** (modern UI)
- **OOP Architecture**
- **Offline-first design**

---

## 🧠 Database Architecture

The system is built on a **relational database design**:

- users → RBAC system
- customers → client data
- orders → main transactions
- order_items → garments per order
- payments → financial tracking
- customer_measurements → body data storage (JSON)
- audit_logs → system activity tracking
- settings → application configuration

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/tailor-shop-system.git
cd tailor-shop-system
2. Install Requirements
pip install customtkinter
3. Run Application
python main.py
🧪 Testing (CLI Mode)

You can test backend without UI using CLI:

python main.py

Features available:

Add/View Customers
Create Orders
Add Order Items
Record Payments
View Audit Logs
Manage Measurements
🗂️ Project Structure
tailor-shop-system/
│
├── database.py          # SQLite database layer
├── main.py              # CLI testing system
├── seed_data.py         # Dummy data generator
├── ui/                  # CustomTkinter UI (future)
│
├── tailor_shop.db       # SQLite database
└── README.md
📊 System Workflow
Customer → Order → Order Items → Measurements → Payments
                     ↓
                Audit Logs
🔐 Security Features
Soft delete system (no permanent data loss)
Role-based access control (RBAC)
Audit logging for all actions
Foreign key constraints enabled
💾 Offline First Approach

This system is designed to work:

Without internet connection
On single desktop machine
With fast local SQLite storage
No external dependencies required
🚀 Future Enhancements
📄 Invoice PDF generation
📊 Dashboard analytics (sales, profit)
🧾 Barcode / QR code system
☁️ Cloud backup sync
📱 Mobile companion app
🧵 Dynamic measurement templates (Phase 2)
🖼️ UI Preview (Coming Soon)

Modern CustomTkinter-based desktop UI will be added in next phase.

👨‍💻 Developer Notes

This project follows:

Clean architecture principles
Modular database design
Scalable ERP-style structure
Production-ready SQLite setup
📜 License

This project is for educational and commercial use. Customize freely for your business needs.

⭐ Support

If you like this project:

⭐ Star the repository
🧵 Share with tailors & developers
🚀 Contribute improvements
