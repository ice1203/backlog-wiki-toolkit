# Backlog Wiki Management Toolkit

> ⚠️ **免責事項**  
> このツールキットは無保証で提供されます。利用により生じた一切の損害について、開発者は責任を負いません。  
> 本番環境での使用前に十分なテストを実施し、バックアップを取得してください。  
> 各自の責任でご利用ください。

Backlog WikiとGitHubリポジトリ間の双方向同期を実現するツールキットです。

## 🚀 特徴

- **完全自動同期**: PRマージ時にBacklog Wikiへ自動反映

## 📋 システム概要

### 主要コンポーネント

| コンポーネント | 機能 | 使用場面 |
|---------------|------|----------|
| **GitHub Actions** | PRマージ時の自動同期 | 日常運用（推奨） |
| **backlog_wiki_manager.py** | Wiki CRUD操作 | 手動操作・緊急対応 |
| **extract_wiki_info.py** | 変更ファイル情報抽出 | Actions内部処理 |

## 🛠 必要なファイル

このツールキットをプロジェクトに導入するには、以下のファイルが必要です：

### 必須ファイル
- `.github/workflows/backlog-sync.yml` - 自動同期ワークフロー
- `scripts/backlog_wiki_manager.py` - Wiki管理ツール
- `scripts/extract_wiki_info.py` - Wiki情報抽出ツール
- `CLAUDE.md` - Claude Code向けプロジェクト指示書
- `ドキュメント管理運用ルール.md` - ワークフロー定義

### プロジェクト固有で作成が必要
- `.env` - Backlog APIキー
- `.mcp.json` - MCP設定（Claude Code使用時）

## 🎯 セットアップ手順

### 1. ファイルコピー

```bash
# 本リポジトリから必要ファイルをコピー
cp .github/workflows/backlog-sync.yml your-project/.github/workflows/
cp scripts/* your-project/scripts/
cp CLAUDE.md ドキュメント管理運用ルール.md .gitignore your-project/
```

### 2. 設定ファイル作成

#### `.env`
```bash
BACKLOG_API_KEY=your_backlog_api_key_here
```

#### `wiki/backlog-settings.json`
```json
{
  "domain": "yourcompany.backlog.jp",
  "folderType": "wiki",
  "outputDir": "/path/to/your/project/wiki",
  "projectIdOrKey": "YOUR_PROJECT_KEY",
  "lastUpdated": "2025-01-01T00:00:00.000Z"
}
```

### 3. GitHub設定

```bash
# GitHubリポジトリでSecrets設定
# Settings > Secrets and variables > Actions
# BACKLOG_API_KEY を追加
```

### 4. 動作確認

```bash
# テストドキュメント作成
echo "# テスト" > wiki/test.md
git add . && git commit -m "Initial setup"

# PR作成・マージで自動同期をテスト
```

## 🔧 手動操作

### Wiki操作

```bash
# 新規Wiki作成
python3 scripts/backlog_wiki_manager.py create PROJECT_ID "Wiki名" content.md

# Wiki更新
python3 scripts/backlog_wiki_manager.py update WIKI_ID "Wiki名" content.md

# Wiki削除
python3 scripts/backlog_wiki_manager.py delete WIKI_ID
```

## 📖 運用方法

詳細な運用方法は `ドキュメント管理運用ルール.md` を参照してください。

### 基本ワークフロー

1. **新規作成**: ブランチ作成 → ドキュメント編集 → PR → マージ → 自動同期
2. **更新**: 既存ファイル編集 → PR → マージ → 自動同期
3. **緊急対応**: 手動ツール使用 → 後でGitHub反映

## 🔍 技術仕様

### 対応環境
- **Python**: 3.8+

### API制限
- Backlog API: レート制限あり（通常使用で問題なし）
- GitHub API: Actions実行時の制限内で動作

### セキュリティ
- APIキーの環境変数管理
- `.gitignore`による機密情報除外
- 最小権限でのBacklogアクセス

