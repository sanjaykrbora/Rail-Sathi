# Rail Sathi

Smart Railway Workshop Management System for N.F. Railway Mechanical Workshop, Dibrugarh.

## Tech Stack

- Python 3.11+
- Streamlit
- SQLite
- Pandas and Plotly

## Project Structure

- app.py
- configuration.py
- requirement.txt
- css/style.css
- assets/
- databases/
  - database.py
  - init_db.py
  - seed_data.py
- pages/
- utils/
  - authentication/

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirement.txt
```

3. Initialize the database:

```bash
python databases/init_db.py
python databases/seed_data.py
```

4. Run the app:

```bash
streamlit run app.py
```

## Environment Variables

Set the following environment variables when using AI features:

- GEMINI_API_KEY

You can store them in a .env file in the project root.
