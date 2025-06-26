# Pull Request Inspector

## Overview
The **Pull Request Inspector** is a Python-based tool designed to automate the retrieval, analysis, and storage of GitHub pull request data. It integrates with the GitHub API to fetch pull request metadata and file changes, stores the information in a MongoDB database, and leverages the FastMCP framework for processing. This tool is useful for developers and teams who need to monitor, analyze, and archive pull request details efficiently.

## Features
- **GitHub Integration**: Fetches pull request metadata (title, description, author, timestamps, etc.) and file changes (additions, deletions, diffs) using the GitHub API.
- **MongoDB Storage**: Archives pull request data in a MongoDB database for persistent storage and querying.
- **FastMCP Integration**: Utilizes the FastMCP framework for extensible pull request evaluation and processing.
- **Environment Configuration**: Uses environment variables for secure configuration of API tokens and database URIs.
- **Logging**: Comprehensive logging for debugging and monitoring operations.

## Project Structure
- **`main.py`**: Entry point for running the Pull Request Inspector.
- **`github_fetch.py`**: Handles interactions with the GitHub API to retrieve pull request data and file changes.
- **`mongodb_client.py`**: Manages MongoDB database connections and collection setup.
- **`code_analyzer.py`**: Core logic for the Pull Request Inspector, integrating GitHub data fetching, database storage, and FastMCP processing.
- **`requirements.txt`**: Lists project dependencies.
- **`.env` (not included)**: Stores environment variables like `GITHUB_TOKEN` and `MONGO_URI`.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **MongoDB**: A running MongoDB instance (local or remote).
- **GitHub API Token**: A valid GitHub personal access token with repository read permissions.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root with the following:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   MONGO_URI=your_mongodb_connection_string
   ```
   Replace `your_github_personal_access_token` with your GitHub API token and `your_mongodb_connection_string` with your MongoDB URI (e.g., `mongodb://localhost:27017/` for a local instance).

## Usage
1. **Run the Application**:
   ```bash
   python main.py
   ```
   This starts the Pull Request Inspector, which initializes the FastMCP agent server for processing pull requests.

2. **Interact with the Inspector**:
   The tool uses the FastMCP framework to process commands. You can interact with it via Claude Desktop to fetch and analyze pull requests. Example workflow:
   - Fetch pull request data from a GitHub repository.
   - Store the retrieved data in MongoDB.
   - Use FastMCP tools to evaluate or process the data further.

## Dependencies
- `anthropic`: For potential AI-driven analysis (not explicitly used in the provided code but listed as a dependency).
- `pymongo`: For MongoDB database interactions.
- `mcp[cli]`: FastMCP framework for agent-based processing.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `requests`: For making HTTP requests to the GitHub API.

## Configuration
- **GitHub API Token**: Ensure the `GITHUB_TOKEN` environment variable is set with a valid token. Generate one at [GitHub Settings](https://github.com/settings/tokens) with appropriate permissions.
- **MongoDB URI**: Set the `MONGO_URI` environment variable to point to your MongoDB instance. The default is `mongodb://localhost:27017/`.
- **Logging**: The application logs at the `INFO` level by default. Modify the logging level in `code_analyzer.py` or `mongodb_client.py` if needed.

## Database Schema
The MongoDB database (`pr_analysis_db`) contains a collection (`pr_analysis_collection`) that stores pull request data with the following structure:
```json
{
  "pr_title": "Pull request title",
  "pr_description": "Pull request description",
  "pr_author": "GitHub username",
  "created_timestamp": "ISO timestamp",
  "updated_timestamp": "ISO timestamp",
  "pr_state": "open/closed/merged",
  "files_changed_count": Number,
  "file_diffs": [
    {
      "file_path": "path/to/file",
      "file_status": "added/modified/deleted",
      "lines_added": Number,
      "lines_removed": Number,
      "total_modifications": Number,
      "diff_patch": "Git diff string",
      "source_url": "URL to raw file",
      "api_contents_url": "URL to file contents via API"
    }
  ]
}
```

## Logging
- Logs are output to the console with timestamps and log levels.
- Errors and critical failures are logged with detailed stack traces (at the `DEBUG` level).

