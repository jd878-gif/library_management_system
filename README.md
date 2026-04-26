# 📚 Library Management System

## 🔍 Overview
A complete Library Management System built from scratch showing 
full progression from basic Python to production-ready application.

## 🚀 Project Evolution
| Stage | Technology | Description |
|-------|-----------|-------------|
| 1 | Python Functions | Basic library operations |
| 2 | OOP | Classes for Book and Member |
| 3 | SQLite | Local database storage |
| 4 | MySQL | Production database |
| 5 | Flask REST API | Full API with endpoints |
| 6 | Pandas | Data analysis and visualization |
| 7 | ETL Pipeline | Extract, Transform, Load |
| 8 | Docker | Containerized entire application |
| 9 | Apache Airflow | Automated ETL pipeline scheduling |

## 🛠️ Tech Stack
- **Language:** Python 3
- **API Framework:** Flask
- **Database:** MySQL, SQLite
- **Data Analysis:** Pandas, Matplotlib
- **ORM:** SQLAlchemy
- **API Testing:** Postman
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git
- **Workflow Orchestration:** Apache Airflow

## 📁 Project Structure
library_management_system/
├── airflow/
│   ├── dags/
│   │   └── library_etl.py
│   └── docker-compose.yaml
├── app_using_docker/
│   ├── app_using_mysql.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env
├── library_application.py
├── library_application_using_OOP.py
├── app_using_sqlite.py
├── app_using_mysql.py
├── app_using_mysql_pandas.py
├── ETL-pipeline.py
├── sql_connector.py
├── .gitignore
├── requirements.txt
└── README.md

## 🔗 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /books | Get all books |
| GET | /books/\<isbn_no\> | Search book by ID |
| GET | /books/search?title= | Search book by title |
| GET | /books/search?author= | Search book by author |
| POST | /books | Insert book |
| DELETE | /books/\<isbn_no\> | Delete book |
| PUT | /books/\<isbn_no\>/borrow | Borrow book |
| PUT | /books/\<isbn_no\>/return | Return book |
| GET | /members | Get all members |
| GET | /members/\<member_id\> | Search member |
| POST | /members | Insert member |
| DELETE | /members/\<member_id\> | Delete member |

## 📊 Data Analysis
- Books borrowed vs available
- Books by publisher and author
- Member borrowing patterns
- Borrowing rate percentage

## 🐳 Docker Setup
Run the entire application with a single command!

### Prerequisites
- Docker Desktop installed and running

### Run with Docker
```bash
docker-compose up --build
```
This automatically starts both Flask API and MySQL in containers!

### Stop containers
```bash
docker-compose down
```

## ⚙️ How to Run

### Option 1 — Docker (Recommended)
```bash
# Clone the repo
git clone https://github.com/jd878-gif/library_management_system

# Navigate to project
cd library_management_system/app_using_docker

# Run with Docker
docker-compose up --build
```

### Option 2 — Local Setup
1. Clone the repo
2. Create `.env` file with database credentials:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=library_db
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run API:
```bash
python app_using_mysql.py
```
5. Run Analysis:
```bash
python app_using_mysql_pandas.py
```
6. Run ETL Pipeline:
```bash
python ETL-pipeline.py
```

## Airflow Setup
Run the automated ETL pipeline:

```bash
cd airflow
docker compose up -d
```
Access Airflow UI at `http://localhost:8080`
- Username: `airflow`
- Password: `airflow`

## 👨‍💻 Author
**Jeet Dave**
[GitHub](https://github.com/jd878-gif/)
