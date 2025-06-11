import os
import json
from notion_client import Client
from datetime import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
BASE_IMAGE_URL = "https://ittekiou.github.io/notion/eichoga_poster/images"

notion = Client(auth=NOTION_TOKEN)

def load_metadata(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def create_notion_block(meta, image_url):
    return {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": [{"text": {"content": meta["title"]}}],
        },
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": image_url}
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": meta["poem"]}}]
                }
            }
        ]
    }

def post_to_notion():
    for file in os.listdir("metadata"):
        if file.endswith(".json"):
            meta = load_metadata(f"metadata/{file}")
            date = meta["date"]
            image_file = file.replace(".json", ".png")
            image_url = f"{BASE_IMAGE_URL}/{image_file}"
            block = create_notion_block(meta, image_url)
            notion.pages.create(**block)

if __name__ == "__main__":
    post_to_notion()
