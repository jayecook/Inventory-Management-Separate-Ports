# Inventory App - Three Port Setup

This project separates the inventory system into three runnable parts:

| Part | Folder | Port | Purpose |
|---|---|---:|---|
| FastAPI REST API | `backend` | 8000 | JSON CRUD API for products |
| React app | `react_app` | 3000 | React frontend that calls the API |
| Product table app | `table_app` | 5000 | Server-rendered product table/admin page |

Both Python apps use the same PostgreSQL database.

## 1. Create the PostgreSQL database

Open pgAdmin or psql and create this database:

```sql
CREATE DATABASE inventory_db;
```

## 2. Set up the FastAPI REST API on port 8000

Open VS Code terminal:

```bash
cd backend
python -m venv .venv
cp .env.example .env
pip install -r requirements.txt
copy .env.example .env
python init_db.py
python -m uvicorn api_app:app --reload --port 8000
```

Open `backend/.env` and make sure this matches your PostgreSQL password:

```txt
DATABASE_URL=postgresql://postgres:admin123@localhost/inventory_db
```

Create the tables and starter products:

```bash
python init_db.py
```

Run the REST API:

```bash
python -m uvicorn api_app:app --reload --port 8000
```

Open:

```txt
http://localhost:8000
http://localhost:8000/docs
```

## 3. Set up the React app on port 3000

Open a second VS Code terminal:

```bash
cd react_app
npm install
cp .env.example .env
npm run dev
```

Open:

```txt
http://localhost:3000
```

## 4. Set up the separate product table app on port 5000

Open a third VS Code terminal:

```bash
cd table_app
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env

or

cd ~/Documents/inventory_three_port_app/table_app
cp .env.example .env
python -m pip install -r requirements.txt
python -m uvicorn table_app:app --reload --port 5000
```

Make sure `table_app/.env` has the same database URL as the backend.

Run the product table web app:

```bash
python -m uvicorn table_app:app --reload --port 5000
```

Open:

```txt
http://localhost:5000
```

Admin login:

```txt
username: admin
password: admin123
```

## Important port summary

Keep three terminals open at the same time:

```bash
# Terminal 1
cd backend
.venv\Scripts\activate
python -m uvicorn api_app:app --reload --port 8000

# Terminal 2
cd react_app
npm run dev

# Terminal 3
cd table_app
.venv\Scripts\activate
python -m uvicorn table_app:app --reload --port 5000
```

## Troubleshooting

If PowerShell blocks `.venv\Scripts\activate`, use this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If port 3000, 5000, or 8000 is already being used, stop the old terminal with `CTRL + C`.

If the app says the database does not exist, create `inventory_db` first in PostgreSQL.

If password authentication fails, update `DATABASE_URL` in both `.env` files to match your real PostgreSQL password.
# Inventory-Management-Separate-Ports
