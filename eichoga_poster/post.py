import os
import json
import datetime
from notion_client import Client

# --- 設定 ---
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_PAGE_ID = os.environ.get("NOTION_PAGE_ID")
BASE_IMAGE_URL = "https://ittekiou.github.io/notion/eichoga_poster/images"
METADATA_DIR = "metadata"
LAST_POSTED_FILE = ".last_posted"

notion = Client(auth=NOTION_TOKEN)

def load_last_posted():
    if os.path.exists(LAST_POSTED_FILE):
        with open(LAST_POSTED_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_posted(filename):
    with open(LAST_POSTED_FILE, "w") as f:
        f.write(filename)

def get_latest_json_file():
    files = [f for f in os.listdir(METADATA_DIR) if f.endswith(".json")]
    if not files:
        return None
    return sorted(files)[-1]  # 一番新しいファイル（名前ベースでソート）

def post_to_notion():
    latest_file = get_latest_json_file()
    if not latest_file:
        print("❌ JSONファイルが見つかりません")
        return

    last_posted = load_last_posted()
    if last_posted == latest_file:
        print(f"✅ 最新ファイル（{latest_file}）はすでに投稿済みです")
        return

    with open(os.path.join(METADATA_DIR, latest_file), "r") as f:
        data = json.load(f)

    title = data["title"]
    poem = data["poem"]
    memo = data.get("memo", "")
    image_url = BASE_IMAGE_URL + "/" + data["image"].split("/")[-1]
    date = data["date"]

    children = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"text": [{"type": "text", "text": {"content": title}}]},
        },
        {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": image_url},
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"text": [{"type": "text", "text": {"content": poem}}]},
        },
    ]

    if memo:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"text": [{"type": "text", "text": {"content": memo}}]},
        })

    block = {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": [{"type": "text", "text": {"content": title}}],
        },
        "children": children,
    }

    try:
        notion.pages.create(**block)
        print(f"✅ Notionに投稿完了: {title}")
        save_last_posted(latest_file)
    except Exception as e:
        print(f"❌ 投稿失敗: {e}")

if __name__ == "__main__":
    post_to_notion()
