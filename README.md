# TaskFlow Lite

A lightweight, full-stack task management web application built with React, Vite, FastAPI, and SQLite.

## Features

- **Clean Dashboard**: Modern, responsive interface with a beautiful gradient design
- **Task Management**: Add, view, update, and delete tasks
- **Status Tracking**: Toggle tasks between "Pending" and "Completed"
- **Task Statistics**: Real-time counts for total, pending, and completed tasks
- **Sample Data**: Pre-populated with fictional tasks for immediate demo
- **Input Validation**: Form validation with error handling
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

### Frontend
- React 18
- Vite 5
- Modern CSS with gradient backgrounds

### Backend
- FastAPI 0.104
- SQLAlchemy 2.0
- SQLite (local database)
- Pydantic for data validation

## Project Structure

```
taskflow-lite/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # HTML entry point
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration with API proxy
│   └── src/
│       ├── main.jsx         # React entry point
│       ├── App.jsx          # Main React component
│       ├── App.css          # Component styles
│       └── index.css        # Global styles
├── .gitignore               # Git ignore rules
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mayankraj179/taskflow-lite.git
cd taskflow-lite
```

### 2. Backend Setup

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd ../frontend
npm install
```

## Running the Application

### Start the Backend

In a terminal, from the backend directory (with virtual environment activated):

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

### Start the Frontend

In a separate terminal, from the frontend directory:

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### Access the Application

Open your browser and navigate to: `http://localhost:5173`

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{id}` - Get a specific task
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `GET /api/tasks/stats` - Get task statistics

## Database

The application uses SQLite for data storage. The database file (`tasks.db`) is automatically created in the backend directory on first run. Sample data is populated automatically when the database is empty.

## Development

### Backend Development

The FastAPI backend includes auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Development

The Vite dev server provides hot module replacement for fast development.

## Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

### Backend Production

For production deployment, consider using:
- Gunicorn or Uvicorn with multiple workers
- Environment variables for configuration
- A production-grade database (PostgreSQL, MySQL)

## License

This project is open source and available under the MIT License.
