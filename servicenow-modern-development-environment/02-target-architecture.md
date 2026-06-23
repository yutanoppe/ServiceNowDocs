---
title: "ServiceNowモダン開発環境 To-Be提案: To-Be全体像"
created: 2026-06-04
updated: 2026-06-23
type: proposal
status: draft
tags:
  - servicenow
  - modern-development-environment
  - to-be-proposal
  - obsidian
aliases:
  - "To-Be全体像"
related:
  - "[[01-executive-summary]]"
  - "[[03-material-flows]]"
---
# ServiceNowモダン開発環境 To-Be提案: To-Be全体像

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[01-executive-summary|前へ]] / [[03-material-flows|次へ]]


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
検証（結合・回帰・UAT） -> 本番
  ※Pre-Prodは標準パイプライン外の任意リハーサル環境
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
| Pre-Prod | **標準リリースパイプラインには置かない任意リハーサル環境**。大型リリース、基盤変更、アップグレード、性能・運用確認など、本番同等確認が必要な場合だけ、検証済みの同一成果物・同一Playbookで実施する。通常変更の必須ゲートにはしない。 |

ReleaseOpsでは本番をコントローラーとし、すべての非本番をManaged Instanceにする。Dev6上で先にパイロットしても、正式運用時の制御・承認記録は本番コントローラーへ移す。

### 4.3 Pre-Prodを標準パイプライン外に置く方針

通常の昇格経路は **Dev／Developer Sandbox → 検証 → 本番** とし、Pre-ProdはReleaseOpsの標準ステージに組み込まない。理由は、すべての変更にPre-Prodを必須化するとリードタイムが伸び、環境待ちがボトルネック化し、軽微なアプリ変更でも本番同等環境の調整コストが発生するためである。

ただし、Pre-Prodを廃止するのではなく、次の条件に該当する場合の**任意リハーサル／リスク低減環境**として残す。

- 複数アプリ・複数更新セット・データ移行を伴う大型リリース
- 本番停止、性能劣化、外部連携先切替、権限変更などの運用影響が大きい変更
- ファミリーアップグレード、プラグイン導入、Store app更新、基盤設定変更
- 本番手順の所要時間、監視、切戻し、Runbook taskのリハーサルが必要な変更

Pre-Prodを使う場合でも、Pre-Prodで新たに開発・修正して別成果物を作らない。検証で承認されたGitタグ、Application Repositoryバージョン、更新セット、Deployment Requestをそのまま適用し、差分が出た場合は開発環境へ戻して再作成・再検証する。

### 4.4 To-Be構成でのクローニング方式ベストプラクティス

To-Be構成では、GitHub、Application Repository、ReleaseOps Deployment Requestがリリース成果物の正本になる。したがって、クローニングは「開発成果物を配布する手段」ではなく、**非本番環境を本番相当データ・設定へ戻し、検証の信頼性を回復する保守作業**として扱う。

#### 4.4.1 基本方針

| 観点 | 推奨方針 |
|---|---|
| Clone方向 | 原則は本番→非本番。非本番→本番、検証→本番、開発→本番のCloneは禁止する。 |
| Clone対象 | Dev、検証、任意Pre-Prodを用途別にCloneする。Developer Sandboxは短命環境として、必要に応じて再作成を優先する。 |
| 正本 | アプリ資材の正本はGitHubとApplication Repository、リリース証跡の正本はReleaseOpsとする。Clone後に環境差分を手修正して正本化しない。 |
| 頻度 | 検証はリリースサイクル前または月次、Devは四半期または大規模データモデル変更後、Pre-Prodは大型リハーサル・アップグレード前に限定する。 |
| 予約 | リリース列車、UAT、AutomatePro回帰、外部結合試験の期間を避け、Clone freeze期間を事前告知する。 |

#### 4.4.2 Clone前チェック

1. **作業中資材の退避:** 未完了更新セット、未Publishアプリ、未マージPR、ローカルATF修正、テストデータを棚卸しし、必要なものはGitHub、Application Repository、更新セットExport、またはチケット添付へ退避する。
2. **Clone除外・保持設定の確認:** Git資格情報、MID Server設定、OAuth/SAML/SSO、外部連携エンドポイント、メール送信設定、Credential/Connection Alias、環境固有System Property、AutomatePro実行アカウント、監視WebhookなどをClone profileで除外またはPost-cloneで再設定する。
3. **AEMC/ReleaseOpsの安全化:** 本番をAEMC/ReleaseOpsコントローラーにするため、本番由来のコントローラー設定・Deployment Request履歴・承認状態が非本番で誤作動しないよう、対象テーブルの除外、無効化、またはPost-cloneリセット手順を定義する。
4. **個人情報・機密情報対策:** 非本番利用に不要な個人情報、メールアドレス、トークン、連携先URLはマスキング、置換、無効化する。国外チームが使う環境ではデータ持ち出し条件も確認する。

#### 4.4.3 Clone後チェック

- Outbound email、通知、スケジュールジョブ、外部連携、Webhook、MID Server、IntegrationHub接続を非本番用に無効化または切替する。
- GitHub接続、Application Repository接続、AEMC Managed Instance登録、ReleaseOps対象環境設定を非本番として再確認する。
- ATF、AutomateProスモーク、Instance Scan、主要ログイン方式、代表業務フローを実行し、Clone後の利用開始条件を満たすことを確認する。
- Clone後に必要な環境固有データパッチやテストユーザー作成は、手作業ではなくRunbook taskまたは冪等スクリプトで実施し、実行結果を記録する。

#### 4.4.4 運用上の禁止事項

- Cloneで消えることを前提に、非本番だけへ恒久設定や未管理データを作り込まない。
- Clone直後の非本番で直接修正した内容を、GitHub・更新セット・Application Repositoryを経由せず本番候補にしない。
- 本番由来の通知・連携・承認・スケジュールジョブを有効なまま非本番で稼働させない。
- Cloneをリリース失敗時のロールバック手段として扱わない。本番ロールバックはDeployment Requestの復旧手順で管理する。
