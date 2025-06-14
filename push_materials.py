import subprocess
import datetime
import os
import sys

# エラーハンドリング付きの実行関数
def run_cmd(cmd, desc):
    print(f"🔧 {desc}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ {desc}に失敗しました")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)

# カレントディレクトリをスクリプトのある場所に変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 今日の日付を取得してメッセージに使う
today = datetime.date.today().isoformat()
commit_message = f"Add 詠眺画素材 {today}"

# Git操作（追加 → コミット → プッシュ）
run_cmd(["git", "add", "eichoga_poster/images", "eichoga_poster/metadata"], "変更ファイルの追加")
run_cmd(["git", "commit", "-m", commit_message], "コミット")
run_cmd(["git", "push", "origin", "main"], "GitHubへのプッシュ")

print("✅ 詠眺画素材、GitHubに放流完了！")
