---
title: "ServiceNowモダン開発環境 To-Be提案: 段階的移行ロードマップ"
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
  - "段階的移行ロードマップ"
related:
  - "[[05-github-operations]]"
  - "[[07-raci-kpi-and-references]]"
---
# ServiceNowモダン開発環境 To-Be提案: 段階的移行ロードマップ

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[05-github-operations|前へ]] / [[07-raci-kpi-and-references|次へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 9. 段階的移行ロードマップ

### Phase 0: 可視化と設計（4～6週間）

**目的:** 移行対象と成功基準を確定し、現行リリースを壊さずに標準を作る。

- 全アプリ、スコープ、更新セット、XML、依存関係、所有者、開発環境、リリース頻度、ATF有無、AutomatePro既存資産・契約・実行環境有無を棚卸しする。
- XMLを「アプリ化」「更新セット化」「標準手順化」「手動例外」に分類する。
- アプリ命名、スコープ、GitHubリポジトリ、ブランチ、PR、更新セット、バージョン、Deployment Requestの標準を定義する。
- KPIのベースラインを測る: リードタイム、検証待ち時間、手動作業数、失敗率、緊急変更率、ロールバック率、ATFカバレッジ、AutomatePro自動化率。
- Dev6を使い、AEMC、ReleaseOps、GitHub接続、ATF、AutomatePro、Instance Scanを技術検証する。
- 本番コントローラー化に必要なセキュリティ、Multi-Instance Management、OAuth、運用権限を設計する。
- AutomateProについて、利用モジュール、API/Webhook/スケジューラー等の起動方式、テスト結果取得方式、実行アカウント、証跡保管先を確認する。

**Exit criteria:** 対象台帳、資材分類、標準、RACI、パイロット対象、KPIが承認済み。

### Phase 1: 小さなスコープアプリでパイロット（6～10週間）

**対象候補:** Dev2の共通部品のうち依存が少ない1アプリ、またはDev3/Dev4の独立した小規模アプリ。

- AEMCで受付・所有者・開発者・Deployment Requestを管理する。
- 1アプリ1GitHubリポジトリ、PR必須、タグとアプリバージョンの対応を導入する。
- Application Repositoryの同一バージョンをReleaseOpsで検証→本番まで昇格する。Pre-Prodは標準ステージにせず、必要な高リスク変更だけ任意リハーサルとして実施する。
- ATF、AutomateProスモークテスト、Instance Scan、Runbook taskをパイプラインに組み込む。
- 本番リリースは現行承認も並行させ、結果を比較する。
- AutomateProはまずRunbook taskで起動・結果確認・証跡添付を標準化し、自動API連携が可能か評価する。

**Exit criteria:** 2～3回の本番リリース成功、同一成果物の昇格、ATF/AutomatePro証跡欠落なし、現行比で手動作業・リードタイムが悪化していない。

### Phase 2: ReleaseOpsを標準リリース経路にする（8～16週間）

- 本番を正式なAEMC/ReleaseOpsコントローラーとし、全非本番をManaged Instanceとして構成する。
- Dev3～Dev5のスコープアプリを順次移行する。
- Dev1の更新セットをReleaseOps Deployment Requestへ統合する。
- 通常、オンデマンド、緊急の3 Playbookを標準化し、それぞれにATFとAutomateProの実行条件を組み込む。
- 検証環境の予約、入場条件、リリース列車、依存関係管理を導入する。
- XML手動ImportをRunbook taskへ移し、毎リリース削減目標を設定する。
- AEMC旧Pipelines and Deploymentsと独自リリース台帳の新規利用を停止する。
- AutomatePro結果をReleaseOps Deployment Requestへ自動または半自動で登録し、Pass/Failに応じた昇格停止ルールを運用開始する。

**Exit criteria:** 本番変更の大半がReleaseOps経由、無管理XMLなし、全Deployment Requestにテスト・承認・復旧証跡あり。

### Phase 3: 開発分離と変更管理自動化（3～6か月）

- Developer SandboxesをDev2～Dev5の一部チームでPoCし、競合削減と費用対効果を評価する。
- DevOps Change VelocityをGitHub、AutomatePro結果、およびChange Managementと接続し、低リスク変更から自動承認を開始する。
- CICD Spoke/APIやGitHub Actionsは、ReleaseOpsからAutomateProを呼び出す補助自動化など、ReleaseOpsで不足する処理に限定して導入する。
- メトリクスに基づき、検証環境の追加、開発環境統合、Dev6用途、リリース頻度を再設計する。

**Exit criteria:** 変更証跡とATF/AutomatePro結果の自動収集、低リスク変更の承認時間短縮、共有開発競合の減少がKPIで確認できる。

### Phase 4: 継続最適化

- ATFカバレッジ、AutomatePro E2Eカバレッジ、品質ゲートをアプリのリスク別に引き上げる。
- XML例外を四半期ごとに見直し、Import Set化、同期化、アプリ／更新セット化できるものから削減する。
- 緊急変更、失敗変更、ロールバックを振り返り、Playbookとテストへ反映する。
- アップグレード時など高リスク変更では、標準パイプライン外のPre-Prodで同じReleaseOps Playbook、回帰ATF、AutomatePro全回帰を使い、アプリ互換性と業務シナリオを確認する。
