import sys
import os
import logging
import traceback
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from github_fetch import retrieve_pull_request_data
from dotenv import load_dotenv
from mongodb_client import ProjectDatabaseHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class PullRequestInspector:
    def __init__(self):
        load_dotenv()
        self.agent = FastMCP("pull_request_inspection")
        self.db_handler = ProjectDatabaseHandler()
        self.pr_collection = self.db_handler.pr_collection
        self._setup_tools()

    def _setup_tools(self):
        """Attach MCP tools for pull request evaluation."""
        self.agent.tool()(self._get_pull_request)
        self.agent.tool()(self._archive_to_database)

    async def _get_pull_request(self, owner: str, repository: str, number: int) -> Dict[str, Any]:
        """Obtain details from a GitHub pull request."""
        logging.info(f"Retrieving PR #{number} from {owner}/{repository}")
        try:
            pr_details = retrieve_pull_request_data(owner, repository, number)
            if pr_details is None:
                logging.warning("No data received from retrieve_pull_request_data")
                return {}
            logging.info("Pull request data successfully retrieved")
            return pr_details
        except Exception as exc:
            logging.error(f"Failed to retrieve PR: {exc}")
            logging.debug(traceback.format_exc())
            return {}

    async def _archive_to_database(self, pr_title: str, pr_data: Dict[str, Any]) -> str:
        """Store pull request review in the database."""
        logging.info(f"Archiving PR review to database: {pr_title}")
        try:
            pr_data["pr_title"] = pr_title
            result = self.pr_collection.insert_one(pr_data)
            message = f"Pull request review for '{pr_title}' archived with ID: {result.inserted_id}"
            logging.info(message)
            return message
        except Exception as exc:
            logging.error(f"Database archiving error: {exc}")
            logging.debug(traceback.format_exc())
            return f"Database archiving error: {exc}"

    def launch_agent_server(self):
        try:
            logging.info("Starting MCP Agent Server")
            self.agent.run(transport="stdio")
        except Exception as exc:
            logging.critical(f"Critical failure in MCP Agent Server: {exc}")
            logging.debug(traceback.format_exc())
            sys.exit(1)

if __name__ == "__main__":
    inspector = PullRequestInspector()
    inspector.launch_agent_server() 
