---
title: "ServiceNowモダン開発環境 To-Be提案: 品質ゲート・自動テスト"
created: 2026-06-04
updated: 2026-06-22
type: proposal
status: draft
tags:
  - servicenow
  - modern-development-environment
  - to-be-proposal
  - obsidian
aliases:
  - "品質ゲート・自動テスト"
related:
  - "[[03-material-flows]]"
  - "[[05-github-operations]]"
---
# ServiceNowモダン開発環境 To-Be提案: 品質ゲート・自動テスト

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[03-material-flows|前へ]] / [[05-github-operations|次へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 6. 標準パイプラインと品質ゲート

### 6.1 Deployment Requestの必須メタデータ

- 要求／ストーリー／不具合ID
- 対象アプリ、スコープ、アプリバージョン、GitHubリポジトリ、コミットSHA、Pull Request
- 更新セットIDおよび親子関係
- 変更影響、対象CI／サービス、データ移行有無、停止有無
- ATF結果、AutomatePro結果、Instance Scan結果、Deployment Analyzer結果
- 実施手順、Runbook task、ロールバック／復旧手順
- セキュリティ・個人情報・国外チームに関する確認結果

### 6.2 段階別ゲート

| 段階 | 自動ゲート | 人手ゲート | Exit criteria |
|---|---|---|---|
| 開発完了 | 開発者ATF、AutomateProスモーク、Instance Scan、アプリ／更新セット整合性 | Peer Review、PR承認 | 重大エラーなし、資材固定、追跡情報完備 |
| 検証入場 | Deployment Analyzer、スモークATF、AutomatePro対象スイート起動可否 | リリース管理者が競合・依存関係確認 | 入場条件を満たし、検証枠を確保 |
| 検証完了 | 回帰ATF、AutomatePro E2E/統合回帰、Instance Scan、外部連携確認 | UAT承認、欠陥判定 | Critical/High欠陥なし、または正式な例外承認 |
| 任意Pre-Prodリハーサル | 本番同等Playbook、ATF＋AutomatePro必要範囲回帰、事後確認のリハーサル | 運用・リリース・変更管理承認 | 大型・高リスク変更のみ実施。所要時間、手順、復旧、監視を確認済み |
| 本番 | 変更窓、事前チェック、順序制御 | 職務分離された承認 | 同一成果物を予定時間内に適用 |
| 本番後 | スモークATF、AutomatePro本番後許可シナリオ、監視、エラー確認 | 業務確認、Release closure | 成功基準達成、証跡保存、差分なし |

ReleaseOpsのDeployment Analyzerは更新セットを対象環境の現状と比較し、ルールとATFコードカバレッジを使って判断できる。初期値として公式の既定動作に合わせてカバレッジ70%未満を要対応とし、アプリ種別ごとに段階的に閾値を引き上げる。ただし、単純なカバレッジ率だけで品質を判定しない。

### 6.3 リリース方式

- **定期リリース列車:** 通常変更を週次または隔週でまとめ、検証環境の競合と承認負荷を抑える。
- **オンデマンドリリース:** 独立性が高く、テストと承認が完了した低リスク変更に使用する。
- **緊急リリース:** 最小限の専用Playbookを用意し、事後レビューと開発環境へのバックポートを必須にする。
- **大型アプリ／複数チーム:** 依存関係と投入順をReleaseOpsのリリース・Playbook・Runbookで明示する。
- **Pre-Prod任意リハーサル:** Pre-Prodは通常変更の必須ステージにしない。リリース管理者がリスク判定し、大型・高リスク変更だけ本番同等リハーサルとして追加する。

### 6.3.1 先行リリースが発生した場合のゲート

要件Aが検証中で、同一アプリの要件Bを先行リリースする場合は、品質ゲートを「環境に入っている変更一式」ではなく「リリース候補として固定した成果物」に対して再実行する。

| 確認観点 | 必須対応 |
|---|---|
| 成果物固定 | 要件Bだけを含むGitタグ、Application Repositoryバージョン、Deployment Requestを作成する。 |
| 独立性確認 | 要件Bが要件Aのテーブル変更、Script Include、Flow、ACL、データ移行に依存していないことを確認する。 |
| 検証環境の清浄性 | 要件Aが残った検証環境の結果をBの合格証跡にしない。B候補を再Installする、環境を戻す、または別検証枠で確認する。 |
| 回帰範囲 | Bの直接機能、Aとの接点、共通部品、権限、外部連携のスモーク／回帰を再実行する。 |
| Aの再整合 | Bリリース後、要件Aを最新本番ベースへ取り込み直し、Aのテスト結果を再取得する。 |

このゲートにより、検証環境で先に進んだ要件Aが本番候補へ紛れ込むことを防ぎ、要件Bの先行リリースを監査可能な形で実施できる。

### 6.4 ATFとAutomateProの組み合わせ方

本提案では、ServiceNow OTBのATFだけでなく、AutomatePro AutoTestも自動テスト基盤として採用する。AutomateProはServiceNow向けに提供されている自動テスト／DevOps製品群であり、公式サイトではAutoTestについて、手動テストをスケールさせるためのテスト自動化、実ユーザーの振る舞いを模したテスト、AIによるテスト作成、再利用可能なブロック、Visual playback、複数ServiceNowインスタンス横断の結果確認などを訴求している。

ATFとAutomateProは競合ではなく、次のように責務を分けて併用する。

| テスト領域 | 主担当 | 理由 |
|---|---|---|
| サーバーサイドロジック、フォーム、Flow、Service CatalogなどServiceNow内で完結する基本回帰 | ATF | ServiceNow標準機能であり、AEMC/ReleaseOpsの品質ゲートへ組み込みやすい。 |
| ITSM/ITOM業務プロセスのE2E、外部連携を含む画面操作、実ユーザーアカウントでの確認 | AutomatePro AutoTest | 実ユーザー視点のテスト、統合先を含むシナリオ、Visual playbackによる失敗解析に向く。 |
| アップグレード回帰、検証環境・Pre-Prod横断の大規模回帰 | ATF + AutomatePro | ATFでServiceNow内部品質を押さえ、AutomateProで業務シナリオと統合動作を補完する。 |
| 証跡・監査資料 | ReleaseOps + AutomatePro/ATF結果 | ReleaseOpsのDeployment Requestに両方の結果URL、実行ID、証跡ファイルを添付する。 |

AutomateProは本リポジトリ内のAustraliaリリース文書に含まれるServiceNow OTB機能ではない。そのため、AEMCやReleaseOpsのパイプラインに自動で組み込める前提にはせず、次の連携設計をPhase 0～2で確立する。

1. **呼び出し方式の確認:** AutomatePro側で利用可能なAPI、Webhook、スケジューラー、CLI、ServiceNow内アプリの起動方法をベンダー資料・PoCで確認する。
2. **ReleaseOps Runbook task化:** API連携が未確定の間は、AutomateProテストスイート実行、結果確認、証跡添付をRunbook taskとして標準化する。
3. **自動ゲート化:** APIまたはWebhookで結果を取得できる場合は、ReleaseOps Deployment Requestにテスト実行ID、結果URL、Pass/Fail、失敗シナリオ数を連携し、Critical/High失敗時は昇格停止にする。
4. **PR連携:** Pull RequestテンプレートにAutomatePro対象スイート、実行結果、失敗時の例外承認を記載する。GitHub Actionsから直接実行する場合も、本番デプロイ経路はReleaseOpsに集約する。
5. **証跡保管:** Visual playback、実行ログ、スクリーンショット、テスト実行レポートはDeployment Requestまたは関連チケットから辿れるようにする。


## 8. 追加導入を推奨するServiceNow製品・機能

### 8.1 優先度A: ATF、AutomatePro、Instance Scan、Deployment Analyzer

最初に導入すべき品質基盤である。AEMCではATFとInstance Scan suiteをデプロイ試験へ追加でき、ReleaseOpsはDeployment AnalyzerとATFコードカバレッジを評価に利用できる。AutomateProはOTBのAEMC/ReleaseOpsゲートではないため、まずRunbook taskで実行・証跡添付を標準化し、API/Webhook等で自動実行と結果取得が可能な範囲からゲート化する。現行プロセスの手動確認を先に可視化・標準化し、その後ゲート化する。

### 8.2 優先度A: AutomatePro連携基盤（権利・API確認後）

AutomatePro AutoTestは、ATFを補完するE2E・統合回帰・実ユーザー視点のテスト基盤として扱う。導入時には、テストスイート命名、環境別実行アカウント、実行トリガー、結果取得、証跡保管、失敗時の昇格停止条件を定義する。AutoDeploy等のAutomatePro製品群を利用する場合でも、ServiceNow資材の本番昇格統制はReleaseOpsに寄せ、二重のリリース正本を作らない。

### 8.3 優先度A: Developer Sandboxes（権利・制約確認後）

Developer Sandboxesは共有開発インスタンスを基準に、オンデマンドの分離環境で並行開発・安全な試験を可能にする。最大30 sandbox/instanceで、Gitブランチ、更新セット、ServiceNow IDE等を利用できる。これによりDev2～Dev5で、大型機能、緊急修正、複数開発者の競合を減らせる。

ただし、incoming integrationのURL調整、clone後の再作成、upgrade時の作業、Build Agent未対応等の制約をPoCで確認する。導入後も顧客別のデータ・統合・契約上の分離が必要なら、基準開発インスタンス自体は統合しない。

### 8.4 優先度B: DevOps Change Velocity

GitHub等の計画・コード・テスト・オーケストレーション情報とServiceNow Change Managementを結び、変更の自動作成、データに基づく自動承認／却下／手動承認、証跡、DevOps Insightsを提供する。ReleaseOpsで安定したDeployment Requestと品質データが取れるようになってから導入すると効果が高い。

ReleaseOpsとDevOps Change Velocityの責務を分ける。

- ReleaseOps: ServiceNow資材をインスタンス間で安全に昇格する。
- DevOps Change Velocity: エンドツーエンドのDevOps証跡と変更管理判断を自動化する。

### 8.5 優先度C: CICD Spoke / CICD API

CICD SpokeはApplication RepositoryからのPublish/Install、ATF、Instance Scan等を自動化できる。GitHub Actionsからの補助処理や既存外部パイプライン連携が必要な場合だけ採用する。ReleaseOpsの標準Playbookで満たせる処理を二重実装しない。
