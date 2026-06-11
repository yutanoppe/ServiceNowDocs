# ServiceNowモダン開発環境 To-Be提案: To-Be全体像

- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 4. To-Be全体像

```text
要求・アプリ受付 / 開発者統制
          AEMC（本番コントローラー）
                    |
                    v
GitHub: Issue/PR/Commit/Tag -----> スコープアプリのソース正本
                    |
                    v
Dev1～Dev5 または Developer Sandbox
  |  開発者テスト / ATF / AutomatePro / Instance Scan / Peer Review
  |  Application RepositoryへバージョンPublish（スコープアプリ）
  |  完了更新セットを固定（グローバル変更）
  v
ReleaseOps Deployment Request（本番コントローラーで統制）
  |  Deployment Analyzer / ATF / AutomatePro / Instance Scan / 承認 / Runbook
  v
検証（結合・回帰・UAT） -> Pre-Prod（本番同等リハーサル） -> 本番
                    |
                    v
DevOps Change Velocity / Change Management（段階導入）
```

### 4.1 製品・ツールごとの責務

| 製品・機能 | To-Beでの責務 | 導入優先度 |
|---|---|---|
| **AEMC** | アプリ受付、開発権限・コラボレーション、カスタムアプリの可視化、Deployment Requestの入口 | 必須・Phase 1 |
| **ReleaseOps** | 更新セットとアプリの昇格、リリース列車、承認、Playbook、Deployment Analyzer、Runbook task、証跡 | 必須・Phase 1～2 |
| **GitHub** | 1アプリ1リポジトリ、Pull Requestレビュー、ブランチ保護、タグ、CODEOWNERS、Issue/作業追跡連携 | 必須・Phase 1 |
| **Application Repository** | Gitでレビュー済みのスコープアプリバージョンを後続環境へ配布するServiceNowネイティブ経路 | 継続利用 |
| **ATF + Instance Scan** | ServiceNow OTBの自動テストと設定・コード品質ゲート。AEMC/ReleaseOpsで扱いやすい標準ゲートとして採用する | 必須・Phase 1 |
| **AutomatePro AutoTest** | ATFだけでは補いにくいE2E、実ユーザー視点、統合先を含む回帰、自動テスト作成・実行・証跡管理を担う。OTB連携ではないため、ReleaseOps/AEMCから呼び出す連携方式を設計する | 必須・Phase 1～2 |
| **Developer Sandboxes** | 共有開発インスタンス上に、開発者・ストーリー単位の分離環境をオンデマンド提供 | 推奨・Phase 3、権利確認後 |
| **DevOps Change Velocity** | GitHub等のDevOpsデータと変更管理を接続し、変更作成、リスクベース承認、証跡、メトリクスを自動化 | 推奨・Phase 3 |
| **ServiceNow IDE** | 大規模・プロコード開発の生産性向上。App Engine Studioと用途を分ける | 選択導入 |
| **CICD Spoke / CICD API** | ReleaseOps外の補助自動化が必要な場合に、アプリPublish/Install、ATF、Instance Scan等を自動化 | 条件付き。ReleaseOpsと重複させない |

> **重要:** AEMCの旧Pipelines and DeploymentsとReleaseOpsを二重のリリース基盤として長期運用しない。AEMC 28.2.1以降はReleaseOps統合・移行が可能なため、AEMCをガバナンス画面、ReleaseOpsを背後のデプロイ実行基盤とする。

### 4.2 インスタンスのTo-Be役割

| 環境 | To-Be役割 |
|---|---|
| 本番 | **AEMC/ReleaseOpsコントローラー**。全非本番をManaged Instanceとして管理し、Deployment Request、承認、リリース、監査証跡を保持する。通常の開発はしない。 |
| Dev1 | ITSM/ITOM・グローバル変更の基準開発環境。更新セット命名、親子更新セット、Instance Scan、ATFを標準化する。 |
| Dev2 | 共通App Engine部品の基準開発環境。A社専用資材を別スコープ・別リポジトリへ分離する。 |
| Dev3～Dev5 | 顧客別アプリの基準開発環境。顧客／アプリ単位のスコープ・GitHubリポジトリ・所有者を明確化する。 |
| Dev6 | Phase 0～2のPoC・ReleaseOpsパイプライン検証環境。方式確立後は破壊的検証、アップグレード事前調査、教育用途へ戻す。 |
| 検証 | 自動回帰、外部結合、UAT。ReleaseOpsのTest環境として、入場条件を満たした変更だけを受け入れる。 |
| Pre-Prod | 本番同等構成でのリリースリハーサル、性能・運用確認、アップグレード検証。原則として本番と同じPlaybook・同じ成果物を使う。 |

ReleaseOpsでは本番をコントローラーとし、すべての非本番をManaged Instanceにする。Dev6上で先にパイロットしても、正式運用時の制御・承認記録は本番コントローラーへ移す。
