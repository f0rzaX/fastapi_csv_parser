# CSV Uploader FastAPI Application

This project is a CSV file uploader built using FastAPI. It uses a MySQL database, Redis, and Celery for asynchronous processing.

## Getting Started

### Prerequisites

-   Python 3.10
-   Docker and Docker Compose (for Docker setup)
-   MySQL and Redis (for local setup)

### 1. Clone the Repository

1. Open a terminal and run the following command to clone the repository:

```bash
git clone https://github.com/f0rzaX/fastapi_csv_parser
cd fastapi_csv_parser
```


### 2(a). Running the Application  - using Docker

#### Step 1: Build and Start the Containers

1. Make sure Docker is running on your machine.
2. Open a terminal and navigate to the project directory.
3. Run the following commands:

```bash
docker-compose build
docker-compose up -d
```

This will start three containers:

-   **MySQL** (with the database 'test_db')
-   **Redis** (for Celery task queue)
-   **FastAPI app** (running on port 8000)

#### Step 2: Verify the Setup

-   Access the FastAPI application at: [http://localhost:8000](http://localhost:8000).
-   If everything is working, you should see the FastAPI interface.
-   Use the `/` endpoint to load the form page for uploading CSV files.

#### Step 3: Stopping the Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

### 2(b). Running the Application - Locally

#### Step 1: Set up the Virtual Environment

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    On Windows:

    ```bash
    venv\Scripts\activate
    ```

    On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

#### Step 2: Set up MySQL and Redis

-   **Start MySQL**: You can use Docker or install MySQL locally. For Docker:

    ```bash
    docker run --name vani-mysql -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=test_db -e MYSQL_USER=user -e MYSQL_PASSWORD=password -p 3306:3306 -d mysql:latest
    ```

-   **Start Redis**: You can use Docker or install Redis locally. For Docker:

    ```bash
    docker run --name vani-redis -d -p 6379:6379 redis
    ```

#### Step 3: Set Environment Variables

Create a `.env` file in the root of the project with the following variables:

```plaintext
DB_HOST = your_db_host
DB_PORT = your_db_port
DB_USER = your_db_user
DB_PASSWORD = your_db_password
DB_NAME = your_db_name
REDIS_URL = your_redis_url
UPLOAD_DIR  = your_upload_directory
ERROR_DIR = your_error_directory
```

#### Step 4: Run the FastAPI Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will be available at [http://localhost:8000](http://localhost:8000).

#### Step 5: Start the Celery Worker

In a new terminal, with the virtual environment activated, start the Celery worker:

```bash
celery -A celery_worker worker --loglevel=info
```

#### Step 6: Verify the Setup

-   Access the FastAPI application at: [http://localhost:8000](http://localhost:8000).
-   If everything is working, you should see the FastAPI interface.
-   Use the `/` endpoint to load the form page for uploading CSV files.

### Troubleshooting

-   **Database Connection Issues**: Ensure MySQL and Redis containers/services are running and the environment variables are set correctly.
-   **Docker Build Issues**: Run `docker-compose build --no-cache` to rebuild the images if there are errors.
-   **Missing Dependencies**: If the app fails to start, run `pip install -r requirements.txt` to ensure all dependencies are installed.

### 3. Application Flow

1. **User Interface**:

    - The user accesses the form page at `/`, where they can select and upload a CSV file.
    - The CSV file is uploaded to the `/uploadFile` endpoint.

2. **File Upload and Storage**:

    - The `/uploadFile` endpoint receives the file and saves it to the `storage/upload` directory.
    - Upon successful upload, a 200 response is returned to the user.

3. **Asynchronous Processing**:

    - Once the file is saved, the FastAPI app triggers a Celery task (`process_file`) to process the CSV asynchronously.
    - Celery reads the file, validates each row, and adds valid rows to the database.
    - If a row is invalid, it is saved to an error CSV file in the `storage/error` directory, along with an error message explaining the issue.

4. **Database Interaction**:

    - The app uses SQLAlchemy to interact with the MySQL database.
    - Valid records are stored in the `csv_records` table.

5. **Error Handling**:
    - The app checks for common errors, such as missing fields or incorrect data types.
    - If an error is encountered during parsing or validation, it is logged to an error CSV file.

### Endpoints

-   **/**: Form page to upload CSV files.
-   **/uploadFile**: Endpoint to upload CSV files for processing.
