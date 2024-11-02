
# Report Viewer Project

This project is a web-based report viewer designed to upload, manage, and view HTML report files stored in a structured format. The system consists of a simple Flask server and a frontend interface that displays an organized index of uploaded reports. Reports are organized by tag, year, month, day, and time.

## Features
- **Upload reports** via POST requests
- **View reports** in a hierarchical structure by navigating through tags, years, months, and days
- **Serve reports** outside the container with uploads stored externally on the host machine

## Project Structure

- `server.py`: Flask server to manage file uploads, serve report index, and deliver files.
- `Dockerfile`: Docker configuration to create a containerized environment for the server.
- `docker-compose.yml`: Configures the container to use an external folder for uploads and manage the server.
- `templates/index.html`: Basic frontend with dynamic navigation for the report index.
- `uploads/`: External directory for storing report files, mounted from the host.

## API Endpoints

### 1. Upload a Report
- **Endpoint**: `/upload`
- **Method**: `POST`
- **Parameters**:
  - `tag_run` (string, required): Tag to organize reports, specifying their category.
  - `file` (file, required): The HTML report file to upload.
- **Response**: Returns a JSON message indicating success or error.

**Example**:

```bash
curl -X POST -F "tag_run=my_tag" -F "file=@path/to/report.html" http://localhost/upload
```

### 2. Fetch Report Index
- **Endpoint**: `/api/index`
- **Method**: `GET`
- **Response**: JSON representing the hierarchy of uploaded reports.

### 3. Serve Uploaded Reports
- **Endpoint**: `/<BASE_UPLOAD_FOLDER>/<path:filename>`
- **Method**: `GET`
- **Description**: Serves uploaded HTML report files located in the `uploads` folder.
  
**Example**:
```
http://localhost/uploads/my_tag/2024/11/02/15.30/report.html
```

## JSON Structure for Report Index

The `/api/index` route generates a JSON response containing the structure of uploaded reports, as follows:

```json
{
  "tag": {
    "year": {
      "month_number-month_name": {
        "day": {
          "hour.minute": "uploads/tag/year/month/day/hour.minute/report.html"
        }
      }
    }
  }
}
```

- **tag**: Category for the report, specified by the user upon upload.
- **year**: Year of the upload.
- **month_number-month_name**: Month of the upload, formatted as "MM - MonthName" (e.g., "11-November").
- **day**: Day of the month.
- **hour.minute**: Time of upload, formatted as `HH.MM`.

### Example JSON

```json
{
  "my_tag": {
    "2024": {
      "11-November": {
        "02": {
          "15.30": "uploads/my_tag/2024/11/02/15.30/report.html"
        }
      }
    }
  }
}
```

## Technologies and Libraries Used

- **Flask**: Backend server framework to handle API routes and serve files.
- **Bootstrap 4.3.1**: CSS framework used for styling the frontend.
- **JavaScript**: Used in the frontend for dynamic rendering of breadcrumb navigation and report links.

## Running the Project with Docker

To run this project with Docker, follow these steps:

1. **Build the Docker image**:

   ```bash
   docker build -t report-viewer .
   ```

2. **Run the container with Docker Compose**:

   ```bash
   docker-compose up -d
   ```

   This command starts the container, exposing the Flask server on port 80 of the host machine and mounting the `uploads` folder for persistent report storage.

## Folder Structure

- **uploads/**: Folder to store report files, mounted from the host machine to persist data outside the container.
  
## Notes

- **External Folder**: The `uploads` folder is shared between the host and container, ensuring files remain available after container shutdown or updates.

