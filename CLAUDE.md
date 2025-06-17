# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this Backlog Wiki Management Toolkit.

## Repository Overview

This is a Backlog Wiki management toolkit that enables seamless integration between GitHub repositories and Backlog Wiki through Claude Code. The toolkit provides automated synchronization and manual management capabilities for Backlog Wiki pages.

## Core Features

- **Automatic GitHub to Backlog Wiki synchronization**: GitHub Actions workflow for PR-based updates
- **Manual Wiki CRUD operations**: Python scripts for direct Wiki management
- **Claude Code integration**: Seamless editing workflow with proper validation and error handling

## Common Operations

**Content Management:**
```bash
# Create new Wiki page
python3 scripts/backlog_wiki_manager.py create <project_id> "<page_name>" <content_file>

# Update existing Wiki page
python3 scripts/backlog_wiki_manager.py update <wiki_id> "<page_name>" <content_file>

# Get Wiki information
python3 scripts/backlog_wiki_manager.py get <wiki_id>
```

## Backlog Integration

**Configuration:**
- `backlog-settings.json` - Wiki export settings ([DOMAIN].backlog.jp/[PROJECT_KEY])
- `backlog-update.log` - Synchronization history

**Document Format:**
- Each `.md` file includes Backlog Wiki Link reference
- Standard heading structure with clear sections
- Includes practical command examples and JSON configurations
- Screenshots referenced as `![image][id]`

**Backlog Wiki Manager (Alternative Tool):**
- **Location**: `scripts/backlog_wiki_manager.py`
- **Features**: Full CRUD operations (Create, Read, Update, Delete)
- **Usage**:
  ```bash
  python3 backlog_wiki_manager.py create <project_id> "<hierarchical_name>" <content_file>
  python3 backlog_wiki_manager.py update <wiki_id> "<name>" <content_file>
  python3 backlog_wiki_manager.py delete <wiki_id>
  python3 backlog_wiki_manager.py get <wiki_id>
  ```
- **Advantages**: More detailed error handling, JSON responses, hierarchical naming support

## Document Management Workflow - MANDATORY RULES

**CRITICAL: Claude Code MUST follow the established document management workflow**

### NEVER Start Document Work Without These Steps

**MANDATORY PRE-WORK CHECKLIST:**

1. **ALWAYS check workflow FIRST**
   - **MUST** read @ドキュメント管理運用ルール.md
   - **MUST** identify: New creation OR Existing modification
   - **MUST** create Todo list from workflow steps

2. **NEVER skip the first step**
   - For modifications: **ALWAYS** run `backlog-exporter差分同期` FIRST
   - For new documents: **ALWAYS** use `backlog_wiki_manager.py create` FIRST

3. **STOP immediately if workflow unclear**
   - **NEVER** proceed without workflow confirmation
   - **ALWAYS** ask user for clarification

**VIOLATIONS (NEVER DO THIS):**
- ❌ User: "OU構成設計書を修正したい" → Immediate editing
- ✅ User: "OU構成設計書を修正したい" → Check workflow → Sync → Edit

**REMEMBER: @references are MANDATORY, NOT optional**

詳細なワークフローと手順:
@ドキュメント管理運用ルール.md

### 要点（Claude向け）

**データ管理ルール**:
- **マスターデータ**: GitHub（全ての編集はここで実施）
- **パブリッシュ先**: Backlog（顧客連携・表示専用）
- **Backlogでの直接編集は原則禁止**（緊急時のみ例外）

**使用ツール**:
- **全体同期**: `backlog-exporter` （差分同期で高速）
- **Wiki操作**: `backlog_wiki_manager.py` （階層指定・フルCRUD・統一ツール）
- **緊急対応**: Backlog直接編集（事後GitHub反映必須）

**NEVER deviate from this workflow** - it prevents critical synchronization issues and ensures data integrity.

**Backlog-Exporter File Structure Rules:**
- **CRITICAL**: Backlog-exporterで同期されたファイルは、Backlogでの実際のWiki構造を反映しています
- **File Location Preservation**: ファイルの場所を変更せずに、内容を充実させます
- **Wiki ID Mapping**: Each exported file maintains its original Backlog Wiki ID and hierarchical structure
- **No Manual Restructuring**: Never move or reorganize files exported by backlog-exporter - this breaks Wiki ID linkage
- **Content-Only Modifications**: Focus on content enhancement while preserving the exported file structure

## Working Rules

### Language and Content Standards
1. **Japanese Language**: All documentation must be in Japanese - maintain consistency
2. **Professional Tone**: Use formal business Japanese (敬語) appropriate for enterprise consulting
3. **Technical Accuracy**: Verify AWS service names, parameters, and procedures against official documentation
4. **Consistent Terminology**: Use standardized AWS terms in Japanese as per AWS official translations

### Content Organization Rules
1. **Hierarchical Structure**: Follow the established directory structure - never create files outside designated areas
2. **Version Control**: All active work goes under `[CURRENT_PHASE]/` - avoid modifying historical documents
3. **Cross-References**: When referencing other documents, use relative paths within the wiki structure
4. **Template Consistency**: Follow existing document templates and formatting patterns
5. **Design Document Structure**: Maintain clear separation between conceptual design (01_概念設計) and detailed design (02_詳細設計)
6. **Parameter Sheet Focus**: Detailed design documents should focus on implementation parameters, not operational procedures or testing details

### Security and Compliance
1. **No Sensitive Data**: Never include actual AWS account IDs, access keys, or production IP addresses in examples
2. **Sanitized Examples**: Use placeholder values like `123456789012` for account IDs, `example.com` for domains
3. **IAM Role References**: Use generic role names in examples, refer to project documentation for actual role mappings
4. **Audit Trail**: Document all configuration changes with rationale and approval status

### Technical Documentation Standards
1. **Executable Commands**: Provide complete, tested AWS CLI commands with proper escaping
2. **JSON Validation**: Ensure all JSON configurations are syntactically valid
3. **Step-by-Step**: Break complex procedures into numbered, actionable steps
4. **Prerequisites**: Always list required permissions, dependencies, and pre-conditions
5. **Validation Steps**: Include verification commands to confirm successful implementation
6. **AWS Documentation Verification**: Use AWS Documentation MCP server to verify technical accuracy of AWS service behaviors and API specifications
7. **No Emoji Usage**: NEVER use emojis in enterprise documentation - use text-based status indicators instead
   - BAD: "✅ 実装済み"
8. **Temporary File Cleanup**: Always remove temporary test files and content after verification
   - Clean up test content files like `test_content.md` after testing tools
   - Remove debug output files and temporary scripts
   - Ensure git repository remains clean of development artifacts 
   - GOOD: "実装済み" or "[実装済み]" or "Status: 実装済み"
   - Use clear Japanese text labels for status indication
   - CRITICAL: Emojis cause encoding errors in Backlog API calls
9. **Branch Management**: Always delete merged branches to maintain repository cleanliness
   - Delete local merged branches: `git branch -d branch-name`
   - Delete remote merged branches: `git push origin --delete branch-name`
   - Keep only active development branches
   - Maintain clean branch history for better project management

### Project-Specific Guidelines
1. **Current Engagement Focus**: Prioritize `[CURRENT_PHASE]/` for all active documentation
2. **Historical Context**: Reference `[HISTORICAL_PHASE]/` for background but don't modify
3. **Enterprise Standards**: Follow enterprise security patterns - multi-layer approval, least privilege
4. **Scalability Considerations**: Document solutions that work across multiple AWS accounts and regions
5. **Cost Optimization**: Include cost implications and optimization recommendations where relevant

### Quality Assurance
1. **Peer Review**: Indicate when content should be reviewed by senior consultants
2. **Testing Status**: Mark procedures as tested/untested and in which environment
3. **Update Frequency**: Note when documents should be reviewed for updates (e.g., quarterly)
4. **Deprecation Tracking**: Flag outdated procedures or services

## Project Context

This is an active consulting engagement between [PROVIDER_NAME] and [CLIENT_NAME] for AWS multi-account architecture implementation. The project emphasizes enterprise-grade security, governance, and operational excellence across multiple AWS accounts.

### Key Stakeholders
- **Client**: [CLIENT_NAME]
- **Provider**: [PROVIDER_NAME]
- **Platform**: Backlog Wiki ([DOMAIN].backlog.jp/[PROJECT_KEY])
- **Timeline**: [PROJECT_TIMELINE]

### Critical Success Factors
1. **Security First**: All recommendations must meet enterprise security standards
2. **Compliance Ready**: Solutions should support audit and compliance requirements
3. **Operational Excellence**: Focus on automation, monitoring, and incident response
4. **Cost Effectiveness**: Balance security with cost optimization
5. **Knowledge Transfer**: Document everything for client team handover

## File Exclusions

The following directories are excluded from version control:
- `issues/` - Backlog issue exports (contains sensitive client data)

Always check `.gitignore` before adding new file types to ensure sensitive information is not accidentally committed.

## MCP Server Integration

**Available MCP Servers:**
- **AWS Documentation MCP**: Use for verifying AWS service behaviors, API specifications, and technical accuracy
- **AWS CloudFormation MCP**: Resource management and template operations
- **AWS Cost Analysis MCP**: Cost estimation and optimization recommendations

**Best Practices for MCP Usage:**
1. **Technical Verification**: Always use AWS Documentation MCP to verify technical claims about AWS services
2. **API Behavior Confirmation**: When documenting SCP conditions or API restrictions, verify against official AWS documentation
3. **Multiple Source Validation**: Cross-reference multiple documentation sources for complex technical scenarios

## Document Quality Management Rules

**MANDATORY: After any document modification, Claude Code MUST perform the following quality checks:**

### Post-Modification Quality Assurance
1. **Consistency Check**: Verify logical consistency throughout the document
   - Check for contradictory statements
   - Ensure workflow steps align with stated principles
   - Verify tool usage matches described strategies

2. **Content Optimization**: Remove redundant and unnecessary content
   - Delete duplicate information
   - Eliminate verbose explanations that don't add value
   - Consolidate repetitive sections

3. **Structural Integrity**: Ensure document structure is logical
   - Verify step numbering is correct and sequential
   - Check that headings accurately reflect content
   - Ensure examples match described procedures

4. **Technical Accuracy**: Validate all technical information
   - Verify command syntax and parameters
   - Check that tool names and functions are correct
   - Ensure workflow diagrams match actual procedures

### Quality Control Checklist
- [ ] No contradictory statements exist
- [ ] All workflow steps are logically consistent
- [ ] Redundant content has been removed
- [ ] Technical details are accurate and current
- [ ] Document structure is clear and logical
- [ ] Examples match described procedures

**This quality management process MUST be applied to ALL document modifications without exception.**

### Team Document Quality Standards

#### 2. 文書作成標準

**文章品質基準**:
- 敬語使用：「〜します」「〜いたします」で統一、「〜である」調は避ける
- 専門用語統一：「有効化」vs「設定」「アカウント」vs「アカウント」（全角・半角統一）
- 読みやすさ：一文60文字以内、箇条書き活用、結論先出し
- 曖昧表現の使い分け：断定的な記述を基本とし、「要確認」「検討が必要」など明確な理由がある場合のみ曖昧表現を使用

**構成テンプレートの遵守**:
- **Security Hub/GuardDuty/IAM Access Analyzer等のセキュリティサービス設計書**：
  1. サービス概要 2. 目的 3. 管理方針 4. 適用範囲 5. 設定方針 6. 検知レベルの方針 7. 抑制ルール適用方針 8. サービス統合方針
- **SCP/要件定義/計画書**：
  1. 目的 2. 適用範囲 3. 基本方針 4. 要件詳細/禁止操作のカテゴリ 5. 制約事項/既存制御 6. 更新プロセス
- **詳細設計/パラメータシート**：
  1. 前提条件 2. 設定手順 3. 検証方法 4. トラブルシューティング
- **見出しレベル**: H1(#)はタイトルのみ、H2(##)で大項目、H3(###)で中項目まで
- **必須セクション**: 全文書に「目的」「適用範囲」「参考資料」を含める

**図表・スクリーンショットの品質基準**:
- ファイル形式：PNG推奨、JPEGは写真のみ、GIFは禁止
- 解像度：最低1920x1080、文字が読める品質を保持
- キャプション：「図X：説明文」形式、図番号は連番
- 更新日付：スクリーンショットには作成日をファイル名に含める

**参考資料・引用の記載ルール**:
- URL有効性：記載前に必ずリンク確認、アクセス不可の場合は削除
- アクセス日記載：外部リンクには「(2025年6月時点)」を併記
- 内部リンク：Backlog wiki内は相対パス、外部は絶対URL
- AWS公式ドキュメント：必ずMCP serverで最新性を確認

#### 3. 技術的正確性の担保

**AWS公式ドキュメントとの整合性確認**:
- 新規記載時：AWS Documentation MCP serverで該当サービスの最新情報を確認
- 設定値記載時：公式ドキュメントのパラメータ仕様と照合
- API仕様記載時：複数の公式ソースで仕様変更がないことを確認
- サービス名称：AWS公式の日本語表記に統一（例：Amazon S3、AWS Lambda）

**コマンド・設定値の動作検証要求**:
- AWS CLIコマンド：[TEST_ENV]またはSandbox環境での実行確認必須
- JSON設定：JSONバリデータによる構文チェック実施
- 設定パラメータ：有効な値の範囲、制約事項を公式ドキュメントで確認
- 検証結果記録：「検証済み(2025/06/16 [TEST_ENV])」などの記載

**前提条件・制約事項の明記義務**:
- 権限要件：必要なIAMポリシー、ロールを具体的に記載
- 依存関係：前提となるサービス設定、リソース状態を明記
- 環境制約：対象AWS リージョン、アカウント種別の制限を記載
- リスク事項：「データ損失の可能性」など重要な注意点を強調表示

**バージョン依存情報の更新ルール**:
- 記載フォーマット：「AWS CLI v2.x系対応」「Terraform v1.5.x検証済み」
- 更新タイミング：四半期ごと、または依存ツールの major バージョンアップ時
- 互換性情報：新旧バージョンでの動作差異、移行時の注意点を記載
- 廃止予定機能：AWS公式の廃止スケジュールを定期確認し事前周知

#### 4. 一貫性・整合性チェック

**他ドキュメントとの矛盾確認**:
- チェック方法：キーワード検索「暗号化」「OU構成」「SCP」等で関連記述を抽出
- 対象ドキュメント：同一プロジェクト内の設計書、要件定義、手順書
- 矛盾発見時：両方のドキュメントを確認し、より新しい情報で統一
- 定期確認：月次で主要設計事項の整合性を一括チェック

**用語集・略語集との整合性**:
- 用語確認：新規用語使用前に既存用語集での定義有無を確認
- 新規用語追加：定義と使用例を含めて用語集に追記
- 略語使用ルール：初出時は「Service Control Policy (SCP)」形式で記載
- 統一性確保：同義語の使い分けルールを明確化（例：「停止」vs「無効化」）

**設計書間の依存関係確認**:
- 相互参照チェック：概念設計の変更時は詳細設計への影響を必ず確認
- セキュリティ設定変更：運用手順、監視設定への影響を確認
- 設計変更履歴：依存関係のある文書に変更理由と影響範囲を記録

**変更影響範囲の評価**:
- チェックリスト：変更対象の設計要素から影響する可能性のある文書を洗い出し
- 影響度評価：軽微（誤字修正）、中程度（設定値変更）、重大（アーキテクチャ変更）で分類
- 関連文書更新：影響度に応じて同時更新または後続タスクとしてスケジュール
- 利用者影響：利用者向け資料、運用手順への影響有無を必ず確認

#### 5. 利用者視点での品質確保

**利用者理解度に応じた説明レベル調整**:
- 技術レベル別記述：
  - 管理者向け：AWS CLI、JSON設定の詳細まで記載
  - 運用担当者向け：GUI操作中心、必要最低限のCLI
  - 経営陣向け：ビジネスメリット、リスク、コスト中心
- 避けるべき表現：専門用語の羅列、前提知識を要求する記述
- 必須要素：用語説明、図解、具体例を組み合わせた説明

**実装手順の実行可能性確認**:
- テスト実行：記載した手順を実際にテスト環境で最初から最後まで実行
- 所要時間記載：各手順の実行時間目安を記載（例：「約5分」）
- 権限確認：手順実行に必要な権限を事前に確認・記載
- エラーパターン：よくある失敗例と対処方法を事前に検証

**トラブルシューティング情報の充実**:
- 必須記載項目：
  - よくあるエラーメッセージと原因
  - 権限不足時の具体的な対処方法
  - 設定値間違い時の確認ポイント
  - ロールバック手順
- 問題パターン：過去の問い合わせ事例をもとにした予防的な記載
- 連絡先情報：エスカレーション先、サポート窓口の明記
