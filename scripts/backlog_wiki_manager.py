#!/usr/bin/env python3
"""
Backlog Wiki Manager
Simple CRUD operations for Backlog Wiki pages

Usage:
    python backlog_wiki_manager.py create <project_id> <name> <content_file>
    python backlog_wiki_manager.py update <wiki_id> <name> <content_file>
    python backlog_wiki_manager.py delete <wiki_id>
    python backlog_wiki_manager.py get <wiki_id>

Examples:
    python backlog_wiki_manager.py create [PROJECT_ID] "Test Wiki" content.md
    python backlog_wiki_manager.py update [WIKI_ID] "Updated Wiki" content.md
    python backlog_wiki_manager.py delete [WIKI_ID]
    python backlog_wiki_manager.py get [WIKI_ID]
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict, Any

# =====================================================
# プロジェクト固有設定 - 必ず変更してください
# =====================================================
# 🚨 重要: 使用前に以下の値を実際のプロジェクト情報に変更してください
ALLOWED_PROJECT_ID = "[PROJECT_ID]"  # 例: "1234567890"
BACKLOG_DOMAIN = "[DOMAIN]"           # 例: "yourcompany"

# プロジェクト保護設定
ENABLE_PROJECT_PROTECTION = True  # Falseにするとプロジェクト制限を無効化（非推奨）


class BacklogWikiManager:
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        
        # ベースURLの構築（ドメインの設定チェック）
        if base_url is None:
            if BACKLOG_DOMAIN == "[DOMAIN]":
                raise ValueError(
                    "❌ エラー: BACKLOG_DOMAINが設定されていません。\n"
                    "スクリプト上部のBACKLOG_DOMAINを実際のドメインに変更してください。\n"
                    "例: BACKLOG_DOMAIN = \"yourcompany\""
                )
            base_url = f"https://{BACKLOG_DOMAIN}.backlog.jp/api/v2"
        
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "BacklogWikiManager/1.0"
        })
    
    def _validate_project_id(self, project_id: str) -> None:
        """プロジェクトID検証"""
        if not ENABLE_PROJECT_PROTECTION:
            return
        
        if ALLOWED_PROJECT_ID == "[PROJECT_ID]":
            raise ValueError(
                "❌ エラー: ALLOWED_PROJECT_IDが設定されていません。\n"
                "スクリプト上部のALLOWED_PROJECT_IDを実際のプロジェクトIDに変更してください。\n"
                "例: ALLOWED_PROJECT_ID = \"1234567890\""
            )
        
        if str(project_id) != str(ALLOWED_PROJECT_ID):
            raise ValueError(
                f"❌ エラー: 許可されていないプロジェクトです。\n"
                f"指定されたプロジェクトID: {project_id}\n"
                f"許可されているプロジェクトID: {ALLOWED_PROJECT_ID}\n"
                f"異なるプロジェクトでの操作を防ぐため、処理を中止します。"
            )

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[Any, Any]:
        """共通のAPI呼び出し処理"""
        url = f"{self.base_url}{endpoint}"
        params = {"apiKey": self.api_key}
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, data=data, timeout=30)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, params=params, data=data, timeout=30)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params, data=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Request failed: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"❌ Error details: {json.dumps(error_detail, indent=2, ensure_ascii=False)}", file=sys.stderr)
                except:
                    print(f"❌ Response text: {e.response.text}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}", file=sys.stderr)
            sys.exit(1)

    def create_wiki(self, project_id: int, name: str, content: str, mail_notify: bool = False) -> Dict[Any, Any]:
        """Wiki新規作成"""
        # プロジェクトID検証
        self._validate_project_id(project_id)
        
        print(f"🆕 Creating new wiki: {name}")
        print(f"🎯 Project ID: {project_id} (検証済み)")
        
        data = {
            "projectId": project_id,
            "name": name,
            "content": content,
            "mailNotify": "true" if mail_notify else "false"
        }
        
        result = self._make_request("POST", "/wikis", data)
        print(f"✅ Wiki created successfully")
        print(f"🆔 Wiki ID: {result['id']}")
        print(f"📝 Wiki Name: {result['name']}")
        return result

    def update_wiki(self, wiki_id: int, name: str, content: str, mail_notify: bool = False) -> Dict[Any, Any]:
        """Wiki更新"""
        print(f"🔄 Updating wiki ID: {wiki_id}")
        
        data = {
            "name": name,
            "content": content,
            "mailNotify": "true" if mail_notify else "false"
        }
        
        result = self._make_request("PATCH", f"/wikis/{wiki_id}", data)
        print(f"✅ Wiki updated successfully")
        print(f"🆔 Wiki ID: {result['id']}")
        print(f"📝 Wiki Name: {result['name']}")
        return result

    def delete_wiki(self, wiki_id: int, mail_notify: bool = False) -> Dict[Any, Any]:
        """Wiki削除"""
        print(f"🗑️  Deleting wiki ID: {wiki_id}")
        
        # 確認のため、削除前にWiki情報を取得
        wiki_info = self.get_wiki(wiki_id)
        print(f"📝 Wiki to delete: {wiki_info['name']}")
        
        data = {
            "mailNotify": "true" if mail_notify else "false"
        }
        
        result = self._make_request("DELETE", f"/wikis/{wiki_id}", data)
        print(f"✅ Wiki deleted successfully")
        return result

    def get_wiki(self, wiki_id: int) -> Dict[Any, Any]:
        """Wiki情報取得"""
        print(f"📖 Getting wiki ID: {wiki_id}")
        
        result = self._make_request("GET", f"/wikis/{wiki_id}")
        print(f"📝 Wiki Name: {result['name']}")
        print(f"📁 Project ID: {result['projectId']}")
        
        # 取得後にプロジェクトID検証（警告のみ）
        if ENABLE_PROJECT_PROTECTION and str(result['projectId']) != str(ALLOWED_PROJECT_ID):
            print(f"⚠️  警告: このWikiは許可されていないプロジェクト（{result['projectId']}）のものです")
        
        return result

    def read_content_file(self, file_path: str) -> str:
        """コンテンツファイルの読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 最初の3行をスキップ（タイトルとBacklog Wiki Link）
            if len(lines) >= 4:
                content = ''.join(lines[3:])
            else:
                content = ''.join(lines)
            
            return content.strip()
            
        except FileNotFoundError:
            print(f"❌ Content file not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to read content file: {e}", file=sys.stderr)
            sys.exit(1)


def load_api_key() -> str:
    """環境変数またはDOTENVファイルからAPIキーを読み込み"""
    import os
    
    # 環境変数を優先的にチェック（GitHub Actions対応）
    api_key = os.getenv('BACKLOG_API_KEY')
    if api_key:
        return api_key
    
    # 環境変数にない場合は.envファイルから読み込み（ローカル開発対応）
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    env_file = project_dir / ".env"
    
    if not env_file.exists():
        print(f"❌ BACKLOG_API_KEY environment variable not set and .env file not found at {env_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('BACKLOG_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    if api_key:
                        return api_key
        
        print("❌ BACKLOG_API_KEY not found in environment variable or .env file", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Failed to read .env file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Backlog Wiki Manager - Simple CRUD operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create [PROJECT_ID] "Test Wiki" content.md
  %(prog)s update [WIKI_ID] "Updated Wiki" content.md  
  %(prog)s delete [WIKI_ID]
  %(prog)s get [WIKI_ID]
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new wiki page')
    create_parser.add_argument('project_id', type=int, help='Project ID')
    create_parser.add_argument('name', help='Wiki page name')
    create_parser.add_argument('content_file', help='Content file path')
    create_parser.add_argument('--notify', action='store_true', help='Send email notification')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update existing wiki page')
    update_parser.add_argument('wiki_id', type=int, help='Wiki ID')
    update_parser.add_argument('name', help='Wiki page name')
    update_parser.add_argument('content_file', help='Content file path')
    update_parser.add_argument('--notify', action='store_true', help='Send email notification')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete wiki page')
    delete_parser.add_argument('wiki_id', type=int, help='Wiki ID')
    delete_parser.add_argument('--notify', action='store_true', help='Send email notification')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get wiki page info')
    get_parser.add_argument('wiki_id', type=int, help='Wiki ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load API key
    api_key = load_api_key()
    
    # Initialize manager
    manager = BacklogWikiManager(api_key)
    
    try:
        if args.command == 'create':
            content = manager.read_content_file(args.content_file)
            result = manager.create_wiki(args.project_id, args.name, content, args.notify)
            print(f"\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.command == 'update':
            content = manager.read_content_file(args.content_file)
            result = manager.update_wiki(args.wiki_id, args.name, content, args.notify)
            print(f"\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.command == 'delete':
            result = manager.delete_wiki(args.wiki_id, args.notify)
            print(f"\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.command == 'get':
            result = manager.get_wiki(args.wiki_id)
            print(f"\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()