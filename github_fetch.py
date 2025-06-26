import os
import requests
import logging
from dotenv import load_dotenv

# Initialize environment configuration
load_dotenv()
GITHUB_API_TOKEN = os.getenv('GITHUB_TOKEN')

# Confirm GITHUB_TOKEN is present
if not GITHUB_API_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is missing")

def retrieve_pull_request_data(owner: str, repository: str, number: int) -> dict:
    """
    Obtain information and file modifications from a GitHub pull request.
    Returns a dictionary with pull request metadata and file diffs, or None if an error occurs.
    """
    pull_url = f"https://api.github.com/repos/{owner}/{repository}/pulls/{number}"
    changed_files_url = f"{pull_url}/files"
    headers = {'Authorization': f'token {GITHUB_API_TOKEN}'}
    logging.info(f"Requesting pull request data for {owner}/{repository}#{number}")
    try:
        with requests.Session() as http_session:
            http_session.headers.update(headers)
            pr_resp = http_session.get(pull_url)
            pr_resp.raise_for_status()
            pr_metadata = pr_resp.json()
            files_resp = http_session.get(changed_files_url)
            files_resp.raise_for_status()
            files_metadata = files_resp.json()
        file_diffs = [
            {
                'file_path': file['filename'],
                'file_status': file['status'],
                'lines_added': file['additions'],
                'lines_removed': file['deletions'],
                'total_modifications': file['changes'],
                'diff_patch': file.get('patch', ''),
                'source_url': file.get('raw_url', ''),
                'api_contents_url': file.get('contents_url', '')
            }
            for file in files_metadata
        ]
        pull_request_info = {
            'pr_title': pr_metadata.get('title', ''),
            'pr_description': pr_metadata.get('body', ''),
            'pr_author': pr_metadata.get('user', {}).get('login', ''),
            'created_timestamp': pr_metadata.get('created_at', ''),
            'updated_timestamp': pr_metadata.get('updated_at', ''),
            'pr_state': pr_metadata.get('state', ''),
            'files_changed_count': len(file_diffs),
            'file_diffs': file_diffs
        }
        logging.info(f"Successfully obtained {len(file_diffs)} file diffs")
        return pull_request_info
    except Exception as error:
        logging.error(f"Failed to obtain pull request data: {error}")
        return None
