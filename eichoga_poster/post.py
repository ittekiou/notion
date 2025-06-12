import os
import json
from notion_client import Client

# --- 設定 ---
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_PAGE_ID")  # 実際はデータベースID
BASE_IMAGE_URL = "https://ittekiou.github.io/notion/eichoga_poster/images"
METADATA_DIR = "metadata"
POSTED_LOG = ".posted_files.json"

notion = Client(auth=NOTION_TOKEN)

def load_posted_files():
    if os.path.exists(POSTED_LOG):
        with open(POSTED_LOG, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_posted_files(posted):
    with open(POSTED_LOG, "w", encoding="utf-8") as f:
        json.dump(sorted(list(posted)), f, ensure_ascii=False, indent=2)

def post_to_notion():
    posted = load_posted_files()
    files = sorted(f for f in os.listdir(METADATA_DIR) if f.endswith(".json"))

    for filename in files:
        if filename in posted:
            continue

        filepath = os.path.join(METADATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            title = data["title"]
            poem = data["poem"]
            memo = data.get("memo", "")
            image_filename = data["image"].split("/")[-1]
            image_url = f"{BASE_IMAGE_URL}/{image_filename}"

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

            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "title": {
                        "title": [{"type": "text", "text": {"content": title}}]
                    }
                },
                children=children
            )

            print(f"✅ 投稿成功: {filename}")
            posted.add(filename)
            save_posted_files(posted)

        except KeyError as e:
            print(f"❌ JSONキーエラー: {filename} - {e}")
        except Exception as e:
            print(f"❌ 投稿失敗: {filename} - {e}")

if __name__ == "__main__":
    post_to_notion()
