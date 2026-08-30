import os
import httpx
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"


class MondayAPIError(Exception):
    pass


class MondayClient:

    def __init__(self):
        self.token = os.getenv("MONDAY_API_TOKEN")

        if not self.token:
            raise ValueError("MONDAY_API_TOKEN is not configured")

        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

    async def execute(self, query: str, variables=None):

        payload = {"query": query}

        if variables:
            payload["variables"] = variables

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                MONDAY_API_URL,
                json=payload,
                headers=self.headers
            )

        if response.status_code != 200:
            raise MondayAPIError(
                f"HTTP {response.status_code}: {response.text}"
            )

        data = response.json()

        if "errors" in data:
            raise MondayAPIError(str(data["errors"]))

        return data["data"]

    async def get_boards(self, board_ids):

        query = """
        query ($boardIds: [ID!]) {
            boards(ids: $boardIds) {
                id
                name
            }
        }
        """

        return await self.execute(
            query,
            {"boardIds": board_ids}
        )

    async def get_board_items(self, board_id):

        all_items = []
        cursor = None

        while True:

            query = """
            query ($boardId: ID!, $cursor: String) {

                boards(ids: [$boardId]) {

                    items_page(
                        limit: 500,
                        cursor: $cursor
                    ) {

                        cursor

                        items {
                            id
                            name

                            column_values {
                                id
                                text
                                value
                            }
                        }
                    }
                }
            }
            """

            variables = {
                "boardId": board_id,
                "cursor": cursor
            }

            data = await self.execute(query, variables)

            page = data["boards"][0]["items_page"]

            items = page["items"]

            all_items.extend(items)

            cursor = page["cursor"]

            if not cursor:
                break

        return all_items
    async def get_boards_with_columns(self, board_ids):
        query = """
        query ($boardIds: [ID!]) {
        boards(ids: $boardIds) {
            id
            name
            columns {
                id
                title
                type
            }
        }
        }
        """

        return await self.execute(query,
        {"boardIds": board_ids}
    )