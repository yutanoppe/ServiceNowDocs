# ServiceNow Modern Development Environment To-Be Proposal

- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

このフォルダーは、ServiceNowモダン開発環境化の提案を読みやすい単位に分割して管理する。元の単一Markdownは情報量が多いため、目的別に以下のファイルへ分割した。

## 分割ファイル

| ファイル | 内容 |
|---|---|
| [01-executive-summary.md](./01-executive-summary.md) | エグゼクティブサマリー、As-Is評価、設計原則 |
| [02-target-architecture.md](./02-target-architecture.md) | To-Be全体像、製品・ツール責務、インスタンス役割 |
| [03-material-flows.md](./03-material-flows.md) | スコープアプリ、ITSM/ITOM・グローバル変更、XML資材の標準フロー |
| [04-quality-gates-and-testing.md](./04-quality-gates-and-testing.md) | Deployment Requestメタデータ、品質ゲート、ATFとAutomateProの組み合わせ、追加製品・機能 |
| [05-github-operations.md](./05-github-operations.md) | GitHub連携の意義、PRレビュー方針、リポジトリ・ブランチ運用、国外チーム対応 |
| [06-migration-roadmap.md](./06-migration-roadmap.md) | Phase 0〜4の移行ロードマップ。AutomatePro連携のPoC・導入フェーズを含む |
| [07-raci-kpi-and-references.md](./07-raci-kpi-and-references.md) | RACI、KPI、最初に決めるべき事項、リポジトリ内／外部Webの設計根拠 |
| [visual-overview.html](./visual-overview.html) | ブラウザだけで閲覧できる、提案全体のビジュアルHTML版 |

## 読み方

1. 方針と論点を短時間で確認する場合は、[01-executive-summary.md](./01-executive-summary.md) から読む。
2. AEMC、ReleaseOps、GitHub、Application Repositoryの役割分担を確認する場合は、[02-target-architecture.md](./02-target-architecture.md) を読む。
3. XML資材、マスター系データ、Runbook taskの扱いを確認する場合は、[03-material-flows.md](./03-material-flows.md) を読む。
4. ATFとAutomateProを組み合わせた自動テスト計画を確認する場合は、[04-quality-gates-and-testing.md](./04-quality-gates-and-testing.md) と [06-migration-roadmap.md](./06-migration-roadmap.md) を読む。
5. 顧客説明やレビュー会では、[visual-overview.html](./visual-overview.html) をブラウザで開く。
