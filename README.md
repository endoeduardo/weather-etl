# Weather ETL Pipeline

This repository contains a data pipeline built with [Dagster](https://dagster.io/) for educational purposes. The pipeline extracts, transforms, and loads (ETL) weather data from the [OpenWeatherMap API](https://openweathermap.org/api).

## Features

- **Data Extraction:** Fetches weather data from OpenWeatherMap.
- **Data Transformation:** Cleans and processes raw weather data.
- **Data Loading:** Stores processed data for analysis or further use.
- **Orchestration:** Uses Dagster for workflow management and monitoring.

## Getting Started

### Prerequisites

- Python 3.8+
- [Dagster](https://docs.dagster.io/getting-started)
- OpenWeatherMap API key

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/weather-etl.git
cd weather-etl
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root and add your OpenWeatherMap API key:

```
WEATHER_API_KEY=your_api_key_here
```

### Running the Pipeline

Start the Dagster development UI:

```bash
dagster dev
```

Trigger the pipeline from the Dagster UI or CLI as needed.

## Project Structure

```
weather-etl/
├── README.md
├── requirements.txt
└── weather_dagster/
    ├── assets.py
    ├── definitions.py
    └── ...
```

## License

This project is for educational purposes only.