# AI ERP Assistant

An AI-powered Enterprise Resource Planning (ERP) system designed to help small and medium-sized businesses manage their daily operations and make better business decisions using data-driven insights.

## 📌 About the Project

Traditional ERP systems store important business information, but users often need to navigate multiple reports and dashboards to understand their business performance.

The **AI ERP Assistant** aims to combine core ERP functionality with Artificial Intelligence and Machine Learning to make business information easier to access, understand, and analyze.

Users will be able to manage products, customers, sales, and inventory while asking questions in natural language to receive useful business insights and recommendations.

This project is being developed as a 7th-semester Computer Engineering project.

## 🎯 Project Objectives

- Develop a centralized system for managing business operations.
- Manage products, customers, sales, and inventory.
- Generate useful sales and inventory reports.
- Integrate an AI assistant that can answer questions about business data.
- Provide data-driven insights and recommendations to support decision-making.

## ✨ Planned Features

### Core ERP Features
- User authentication and role-based access control
- Product management
- Customer management
- Sales management
- Inventory and stock management
- Business dashboard and reports

### AI Features
- Natural-language queries about business data
- Automated sales summaries
- Inventory insights and low-stock analysis
- Business recommendations based on ERP data

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development and AI/ML |
| FastAPI | REST API development |
| PostgreSQL | Relational database |
| SQL | Database queries and reporting |
| React | Planned frontend development |
| Machine Learning / LLMs | Planned intelligent analysis and AI assistance |
| Git and GitHub | Version control |

*Some technologies and features are planned and may not yet be implemented.*

## 🏗️ Project Structure

```text
AI-ERP-Assistant/
├── backend/
│   └── app/
│       ├── database.py
│       └── main.py
├── datasets/
├── docs/
├── frontend/
├── notebooks/
├── screenshots/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python version supported by the project environment
- PostgreSQL
- Git
- `uv` Python package and project manager

### 1. Clone the repository

```bash
git clone https://github.com/kajal209/AI-ERP-Assistant.git
cd AI-ERP-Assistant
```

### 2. Create and activate a virtual environment

```bash
uv venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install project dependencies

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the database connection settings expected by `backend/app/database.py`.

Do not commit `.env` or share database passwords publicly.

### 5. Set up the database

Create a PostgreSQL database named `ai_erp` and configure its connection details in `.env`.

Create the required database tables using the SQL schema provided in the project documentation or database setup scripts.

### 6. Run the backend

```bash
uv run uvicorn backend.app.main:app --reload
```

Open the following URLs in your browser:

- API: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs

*Database setup instructions may be refined as the project develops.*

## 🗺️ Development Roadmap

- [x] Initial FastAPI backend setup
- [x] PostgreSQL database connection
- [x] Product management API
- [x] Sales management API
- [x] Sales and inventory reporting endpoints
- [ ] User authentication and role-based access
- [ ] Complete ERP modules and frontend
- [ ] AI assistant for natural-language business queries
- [ ] AI-generated business insights and recommendations
- [ ] Testing, documentation, and deployment

## 🔮 Future Scope

- Demand forecasting using historical sales data
- Intelligent inventory replenishment suggestions
- Sales trend analysis
- Automated business reports
- More advanced AI-powered decision support

## 🎓 Project Information

**Project Name:** AI ERP Assistant  
**Project Type:** Academic / 7th-Semester Computer Engineering Project  
**Domain:** Artificial Intelligence, Machine Learning, and Enterprise Resource Planning

## 👩‍💻 Author

**Kajal Mandal**

Computer Engineering Student

## 📄 License

A license can be selected when the project is ready for public distribution.
