# Internship Tracker API

A backend REST API for managing internship applications.

## Features

- Add internship applications
- View all internships
- View a single internship
- Update internship details
- Delete internship applications
- SQLite database for data storage

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /internships | Add internship |
| GET | /internships | Get all internships |
| GET | /internships/{id} | Get one internship |
| PUT | /internships/{id} | Update internship |
| DELETE | /internships/{id} | Delete internship |

## How to Run

1. Create virtual environment:

```bash
python -m venv venv