#!/usr/bin/env python3
"""
Wiki Information Extractor for GitHub Actions
Markdownファイルから Backlog Wiki ID と名前を抽出
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Optional


def extract_wiki_id_from_url(url: str) -> Optional[str]:
    """
    Backlog Wiki URLからWiki IDを抽出
    例: https://[DOMAIN].backlog.jp/alias/wiki/[WIKI_ID] → [WIKI_ID]
    """
    match = re.search(r'/wiki/(\d+)', url)
    return match.group(1) if match else None


def extract_wiki_info_from_file(file_path: str) -> Optional[Dict[str, str]]:
    """
    Markdownファイルから Wiki ID と名前を抽出
    """
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️ File not found: {file_path}", file=sys.stderr)
            return None
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backlog Wiki Linkパターンを検索
        # 例: [Backlog Wiki Link](https://[DOMAIN].backlog.jp/alias/wiki/[WIKI_ID])
        wiki_link_match = re.search(
            r'\[Backlog Wiki Link\]\(([^)]+)\)', 
            content
        )
        
        if not wiki_link_match:
            print(f"⚠️ No Backlog Wiki Link found in: {file_path}", file=sys.stderr)
            return None
            
        wiki_url = wiki_link_match.group(1)
        wiki_id = extract_wiki_id_from_url(wiki_url)
        
        if not wiki_id:
            print(f"⚠️ Could not extract Wiki ID from URL: {wiki_url}", file=sys.stderr)
            return None
        
        # ファイル名から Wiki 名を推定（最初の見出しから取得）
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            wiki_name = title_match.group(1).strip()
        else:
            # フォールバック: ファイルパスから名前を生成
            wiki_name = str(path.stem)
        
        return {
            'wiki_id': wiki_id,
            'wiki_name': wiki_name,
            'file_path': file_path,
            'wiki_url': wiki_url
        }
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    """
    メイン処理：変更されたファイルリストからWiki情報を抽出してJSONで出力
    """
    if len(sys.argv) < 2:
        print("Usage: python extract_wiki_info.py <files>", file=sys.stderr)
        sys.exit(1)
    
    # 引数で渡されたファイルリストを処理（複数の個別引数として受け取り）
    files = sys.argv[1:]
    
    if not files:
        print("No files to process", file=sys.stderr)
        sys.exit(0)
    
    print(f"Processing {len(files)} files...")
    
    wiki_updates = []
    
    for file_path in files:
        print(f"Processing: {file_path}")
        wiki_info = extract_wiki_info_from_file(file_path)
        
        if wiki_info:
            wiki_updates.append(wiki_info)
            print(f"✅ Extracted: Wiki ID {wiki_info['wiki_id']} - {wiki_info['wiki_name']}")
        else:
            print(f"❌ Failed to extract info from: {file_path}")
    
    # JSON形式で出力（GitHub Actionsで読み取り可能な形式）
    output_file = "wiki_updates.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        for update in wiki_updates:
            f.write(json.dumps(update, ensure_ascii=False) + '\n')
    
    print(f"\n=== Summary ===")
    print(f"Total files processed: {len(files)}")
    print(f"Wiki info extracted: {len(wiki_updates)}")
    print(f"Output written to: {output_file}")
    
    if len(wiki_updates) != len(files):
        missing_count = len(files) - len(wiki_updates)
        print(f"⚠️ {missing_count} files could not be processed")
        
        # 処理できなかったファイルをリスト表示
        processed_files = {info['file_path'] for info in wiki_updates}
        missing_files = [f for f in files if f not in processed_files]
        
        print("Missing files:")
        for missing in missing_files:
            print(f"  - {missing}")


if __name__ == "__main__":
    main()