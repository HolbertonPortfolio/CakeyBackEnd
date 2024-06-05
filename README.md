# Cakey API

This project is a FastAPI application that manages pastries, ingredients, and recipes. The API allows you to create, read, update, and delete pastries, as well as search for pastries by ingredients.

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL
- Git

### Clone the Repository

```bash
git clone https://github.com/HolbertonPortfolio/CakeyBackEnd.git
cd CakeyBackEnd
```


### Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Set Up the Database
    
1. Make sure MySQL is running on your machine.
2. Create a new database:

```sql
CREATE DATABASE cakey_test;
```

3. Update the database connection details in the `config/db.py` file:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/cakey_test"
```

Replace `username` and `password` with your MySQL credentials.



### Run the Application

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

