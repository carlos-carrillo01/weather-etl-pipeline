# Weather Mini Pipeline

Python ETL pipeline that extracts weather data from Open-Meteo for multiple cities,
transforms and validates it with pandas, and loads it into a PostgreSQL database running on Docker.

## Architecture

```text
Open-Meteo API
      ↓ extract.py
data/raw/*_weather_raw.json
      ↓ transform.py
data/processed/weather_clean.csv
      ↓ load.py
PostgreSQL (Docker)
      ↓ SQL
Analytical queries
```

## Technologies

- Python
- pandas
- requests
- PostgreSQL
- Docker Compose
- SQLAlchemy
- python-dotenv
- pytest
- Git

## How to run it

### 1. Clone the repository

```bash
git clone https://github.com/carlos-carrillo01/weather-etl-pipeline.git
cd weather-mini-pipeline
```

### 2. Create the virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
POSTGRES_USER=data_engineer
POSTGRES_PASSWORD=your_password
POSTGRES_DB=weather_db
CITIES=Mexico City,Guadalajara
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Run the full pipeline

```bash
python main.py
```

### 6. Run the tests

```bash
pytest
```

### 7. Query the data

```bash
docker compose exec postgres psql -U data_engineer -d weather_db
```

```sql
SELECT
    city,
    COUNT(*) AS records
FROM weather
GROUP BY city
ORDER BY city;
```

## Data Model

Table: `weather`

| Column | Type | Description |
|---|---|---|
| city | text | City name |
| date | timestamp | Forecast date |
| temp_max_c | float | Maximum temperature in °C |
| temp_min_c | float | Minimum temperature in °C |
| precipitation_mm | float | Accumulated precipitation in mm |

## Data Quality Validations

The pipeline validates that:

- Dates are valid.
- There are no duplicate dates per city.
- There are no null values in required fields.
- Maximum temperature is not lower than minimum temperature.
- Precipitation is not negative.

Records with null dates or missing required values are dropped before loading.

## Logs

Each run generates messages in the terminal and in `pipeline.log`:

```text
INFO | extract | Extracting data for: Mexico City
INFO | transform | Transforming data for: Mexico City
INFO | load | Loaded 14 records into table 'weather'.
```

## Future Improvements

- Automatic city geocoding.
- Incremental loading instead of replacing the table.
- Daily scheduling with Airflow or cron.
- dbt for SQL transformations.
- Cloud deployment.
