import os
import json
from notion_client import Client

# === 環境変数から認証情報を取得 ===
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

# === 設定 ===
BASE_IMAGE_URL = "https://ittekiou.github.io/notion/eichoga_poster/images"
METADATA_DIR = "metadata"
LAST_POSTED_FILE = ".last_posted"

notion = Client(auth=NOTION_TOKEN)

# === 投稿済みファイルの読み書き ===
def load_last_posted():
    if os.path.exists(LAST_POSTED_FILE):
        with open(LAST_POSTED_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_last_posted(filename):
    with open(LAST_POSTED_FILE, "w", encoding="utf-8") as f:
        f.write(filename)

# === 最新JSONファイルを取得（ファイル名で判定） ===
def get_latest_json_file():
    files = [f for f in os.listdir(METADATA_DIR) if f.endswith(".json")]
    if not files:
        return None
<<<<<<< Updated upstream
    files.sort()  # アルファベット順 → ISO日付で正しく並ぶ
    latest = files[-1]
    print(f"📄 最新のJSONファイル: {latest}")
    return latest


# === JSONメタデータの読み込み ===
def load_metadata(filepath):
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)

# === Notionに貼る画像URLの構築 ===
def build_image_url(json_filename, meta):
    if "image" in meta and meta["image"]:
        return f"{BASE_IMAGE_URL}/{meta['image'].split('/')[-1]}"
    image_file = json_filename.replace(".json", ".png")
    return f"{BASE_IMAGE_URL}/{image_file}"

# === Notion用の投稿データ構築 ===
=======
    return sorted(files)[-1]  # アルファベット順で最新を選ぶ

def load_metadata(filepath):
    with open(filepath, 'r', encoding="utf-8") as f:
        return json.load(f)

def build_image_url(json_filename, meta):
    # 優先：JSONにimageフィールドがある場合
    if "image" in meta and meta["image"]:
        return f"{BASE_IMAGE_URL}/{meta['image'].split('/')[-1]}"
    # なければファイル名から生成
    image_file = json_filename.replace(".json", ".png")
    return f"{BASE_IMAGE_URL}/{image_file}"

>>>>>>> Stashed changes
def create_notion_payload(meta, image_url):
    title = meta["title"]
    poem = meta["poem"]
    memo = meta.get("memo", "")

    children = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        },
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
                "rich_text": [{"type": "text", "text": {"content": poem}}]
            }
        }
    ]

    if memo:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": memo}}]
            }
        })

    return {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": [{"type": "text", "text": {"content": title}}]
        },
        "children": children
    }

<<<<<<< Updated upstream
# === Notionへの投稿処理 ===
=======
>>>>>>> Stashed changes
def post_to_notion():
    json_file = get_latest_json_file()
    if not json_file:
        print("❌ metadataディレクトリにJSONファイルが見つかりません")
        return

    if json_file == load_last_posted():
        print(f"✅ すでに投稿済み: {json_file}")
        return

    full_path = os.path.join(METADATA_DIR, json_file)
    meta = load_metadata(full_path)
    image_url = build_image_url(json_file, meta)
    block = create_notion_payload(meta, image_url)

    try:
        notion.pages.create(**block)
        save_last_posted(json_file)
        print(f"✅ Notionページを作成しました: {meta['title']}")
    except Exception as e:
        print(f"❌ Notionページ作成に失敗しました: {e}")

# === 実行 ===
if __name__ == "__main__":
    post_to_notion()
