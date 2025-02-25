Real-Time Health Data Ingestion & Analytics Service
This project implements a mini real-time ingestion and analytics service for wearable health data. It receives simulated health metrics (such as heart rate, steps, and calories) in real time, stores them in a PostgreSQL database, and provides an API endpoint to retrieve aggregated statistics (like average heart rate, total steps, and total calories) over a specified time range.

Table of Contents
Overview
Installation
Configuring PostgreSQL
Running the Application
Testing the Endpoints
Design Explanation
Additional Notes
Overview
The service is built using FastAPI, leveraging asynchronous capabilities for high performance and non-blocking operations. It uses SQLAlchemy with async support and the asyncpg driver to interact with a PostgreSQL database. The database schema is straightforward—a single table (health_metrics) stores user data along with timestamps, heart rate, steps, and calories, making it ideal for time-series data aggregation.

Installation
Clone the Repository:

bash
Copy
git clone <your-repository-url>
cd health_metrics_service
Create and Activate a Virtual Environment:

bash
Copy
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Configuring PostgreSQL
Set Up PostgreSQL:

Make sure PostgreSQL is installed and running on your machine.
Create a new database (e.g., healthdb).
Update the Connection String:

Open main.py and modify the DATABASE_URL variable with your PostgreSQL credentials. For example:

python
Copy
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/healthdb"
Database Initialization:

The application automatically creates the necessary tables when it starts.
Running the Application
Start the FastAPI server by running:

bash
Copy
uvicorn main:app --reload
The service will be accessible at http://127.0.0.1:8000.

Testing the Endpoints
Ingestion Endpoint
Endpoint: POST /ingest

Description: Accepts a JSON array of wearable health metric records.

Example Request Body:

json
Copy
[
  {
    "user_id": 101,
    "timestamp": "2025-01-01T09:30:00Z",
    "heart_rate": 78,
    "steps": 150,
    "calories": 6.5
  },
  {
    "user_id": 101,
    "timestamp": "2025-01-01T09:45:00Z",
    "heart_rate": 82,
    "steps": 300,
    "calories": 13
  },
  {
    "user_id": 202,
    "timestamp": "2025-01-01T10:00:00Z",
    "heart_rate": 90,
    "steps": 500,
    "calories": 22.5
  },
  {
    "user_id": 101,
    "timestamp": "2025-01-01T10:15:00Z",
    "heart_rate": 85,
    "steps": 200,
    "calories": 9.1
  }
]
How to Test:

Open the Swagger UI at http://127.0.0.1:8000/docs.
Navigate to the POST /ingest endpoint, paste the JSON payload into the request body, and click Execute.
You should receive a confirmation message indicating the number of records ingested.
Aggregation Endpoint
Endpoint: GET /metrics

Description: Retrieves aggregated statistics for a specified user and time range.

Query Parameters:

user_id: e.g., 101
start: e.g., 2025-01-01T00:00:00Z
end: e.g., 2025-01-02T00:00:00Z
Example Request:

sql
Copy
GET /metrics?user_id=101&start=2025-01-01T00:00:00Z&end=2025-01-02T00:00:00Z
How to Test:

Use Swagger UI or a tool like Postman to send the above GET request.
The response should include the aggregated average heart rate, total steps, and total calories for the given parameters.
Design Explanation
This service was developed using FastAPI, which is well-suited for building high-performance, asynchronous web applications. The choice of FastAPI, in combination with SQLAlchemy's async capabilities and the asyncpg driver, allows the service to efficiently handle multiple simultaneous requests, making it ideal for real-time data ingestion scenarios.

The database schema features a single table (health_metrics) designed to store time-series data, including user identifiers, timezone-aware timestamps, heart rates, steps, and calories. This design facilitates straightforward aggregation queries over arbitrary time ranges. Handling timezone-aware timestamps ensures that the data remains consistent and reliable, regardless of the geographic location of the data source.

Additional Notes
Error Handling: Basic error handling is implemented. For instance, if no records are found for a specified query, the API returns a 404 error.
Future Enhancements: Additional improvements may include integrating a message queue (like RabbitMQ or Kafka) for more advanced real-time ingestion, enhanced logging, and containerization with Docker.
Contributions: Contributions, issues, and suggestions are welcome. Please feel free to open an issue or submit a pull request.
