---
title: "ServiceNowモダン開発環境 To-Be提案: RACI・KPI・設計根拠"
created: 2026-06-04
updated: 2026-06-19
type: proposal
status: draft
tags:
  - servicenow
  - modern-development-environment
  - to-be-proposal
  - obsidian
aliases:
  - "RACI・KPI・設計根拠"
related:
  - "[[06-migration-roadmap]]"
---
# ServiceNowモダン開発環境 To-Be提案: RACI・KPI・設計根拠

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[06-migration-roadmap|前へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 10. RACIのたたき台

以下のRACIは、**PFO（Platform Owner）が個別アプリの実装責任まで背負わない**ことを前提に見直したたたき台である。  
PFOは、個別機能の実装判断・業務仕様の最終責任者ではなく、**ServiceNowプラットフォーム全体の標準、権限、リリース統制、例外管理、アーキテクチャ整合性に対してAccountable**となる。

| 活動 | Product/App Owner | Tech Lead | 開発者 | QA/UAT | Release Manager | Change Manager | Platform Owner |
|---|---|---|---|---|---|---|---|
| AEMCアプリ受付・優先度 | A/R | C | C | C | C | I | C |
| アプリ設計・スコープ設計・依存関係整理 | A | R | C | C | I | I | C |
| GitHub PR・実装 | A | R | R | C | I | I | C |
| PRレビュー・コード品質確認 | A | R | C | C | I | I | C |
| ATF/AutomatePro/Instance Scan整備 | A | R | R | R | I | I | C |
| Deployment Request作成 | C | R | R | C | A | I | C |
| 検証/UAT承認 | A | C | C | R | I | I | I |
| リリース計画・実行 | I | C | C | C | A/R | C | C |
| 本番変更承認 | C | I | I | C | R | A | C |
| リリース方式・品質ゲート・例外運用の標準化 | C | C | I | C | R | C | A |
| 標準・権限・基盤運用 | I | C | C | C | C | C | A/R |
| アーキテクチャ整合性・プラットフォーム影響レビュー | C | R | C | I | C | I | A |

**RACI見直しの考え方:**

- **Product/App Owner** は、対象アプリの業務価値、優先度、UAT承認、個別アプリとしての最終責任を持つ。
- **Tech Lead** は、個別アプリの技術設計、PRレビュー、実装品質、依存関係整理の実務責任を持つ。
- **開発者** は、実装、単体確認、ATF/Instance Scan対応、Deployment Requestに必要な技術情報の準備を担う。
- **QA/UAT** は、テスト観点、UAT実施、受入判定、品質確認を担う。
- **Release Manager** は、Deployment Request、リリース計画、投入順序、Runbook、ReleaseOps上の実行統制に責任を持つ。
- **Change Manager** は、本番変更承認、変更リスク判断、変更管理プロセスとの整合性に責任を持つ。
- **Platform Owner** は、個別実装のAccountableではなく、プラットフォーム標準、権限設計、品質ゲート、例外運用、アーキテクチャ整合性、ServiceNow全体影響の統制に責任を持つ。

国外チームは開発とPR提出をRとできるが、本番承認・本番資格情報・Release実行は国内の職務分離された担当をA/Rとする。  
また、国外チームが関与する場合でも、Product/App Owner、Tech Lead、Release Manager、Change Manager、Platform Ownerの責任分界は上記RACIに従う。

## 11. KPI

| 観点 | KPI例 | 最初の目標例 |
|---|---|---|
| スピード | PR mergeから本番までのリードタイム | ベースライン比20%短縮 |
| 待ち時間 | 検証環境入場待ち時間 | ベースライン比30%短縮 |
| 品質 | 変更失敗率、リリース起因障害、ロールバック率 | 継続的低下 |
| 自動化 | ATF/AutomatePro/Instance Scan自動実行率 | 対象リリース100% |
| 追跡性 | Git commit/PR/アプリ版/更新セット/Deployment Request/Changeの相互参照率 | 100% |
| 手動作業 | 管理外XML Import件数 | 0件 |
| ガバナンス | ReleaseOps外の本番変更率 | 緊急例外を除き0% |
| テスト | リスク別ATFカバレッジ、AutomatePro E2Eカバレッジ | 初期70%を目安に段階向上 |

数値目標はPhase 0のベースライン測定後に確定する。

## 12. 最初に決めるべき事項

以下は実装前に関係者で決定する必要があるが、提案全体を止める不明点ではない。

1. 各アプリのスコープ、所有者、依存関係、顧客別データ分離要件。
2. AEMC、ReleaseOps、Developer Sandboxes、DevOps Change Velocity、AutomateProの契約・entitlementと導入可能バージョン。
3. GitHub Enterprise Cloud/Server、接続経路、MID Server要否、認証方式、資格情報管理主体。
4. Dev5国外チームに適用する法務・セキュリティ・データ所在地・アクセス制約。
5. 検証環境の同時利用需要と、追加テスト環境が必要になる閾値。
6. XML資材の実体、Import APIのサポート可否、停止・ロールバック要件。
7. 本番コントローラーにAEMC/ReleaseOpsを導入する際の運用・セキュリティ審査。
8. AutomateProの起動方式、API/Webhook可否、実行アカウント、ネットワーク接続、証跡保管、ReleaseOps連携責任者。

## 13. リポジトリ内の設計根拠

- [App Engine Management Center](../markdown/application-development/app-engine-management-center/app-engine-management-center.md): アプリ受付、パイプライン、開発者生産性、カスタムアプリの洞察を一元管理する。
- [Exploring AEMC](../markdown/application-development/app-engine-management-center/exploring-aemc.md): AEMC 28.2.1以降のReleaseOps統合と、更新セット、Playbook、定期／オンデマンドリリース対応。
- [Configure your controller instance](../markdown/application-development/app-engine-management-center/config-controller-instance.md): 通常は本番をコントローラーとし、要求・承認記録を保持する。
- [ReleaseOps](../markdown/application-development/releaseops/releaseops-landing.md) / [Exploring ReleaseOps](../markdown/application-development/releaseops/exploring-release-ops.md): デプロイ自動化、Deployment Request、リリース、Playbook、Runbook task。
- [Instances in ReleaseOps configuration](../markdown/application-development/releaseops/instances-in-releaseops-configuration.md): コントローラーとManaged Instanceによる一元オーケストレーション。
- [Deployment analyzer](../markdown/application-development/releaseops/deployment-analyzer.md): 更新セットの対象環境比較、ルール、ATFコードカバレッジ。
- [AES integration with a Git source control repository](../markdown/application-development/app-engine-studio/aes-source-control-integration.md): 非本番Git連携、1アプリ1リポジトリ、共有資格情報、本番でのGit管理非対応、外部編集の制約。
- [Add ATF and instance scan suites for testing](../markdown/application-development/app-engine-management-center/add-atf-instance-scan-suite-testing.md): AEMCパイプラインへATFとInstance Scan suiteを追加できる。
- [Exploring Developer Sandboxes](../markdown/application-development/developer-sandboxes/exploring-sandboxes.md) / [Supported features](../markdown/application-development/developer-sandboxes/dev-sbx-supported-features.md): 分離・並行開発、Git・更新セット・IDE対応と制約。
- [Exploring DevOps Change Velocity](../markdown/it-service-management/devops-change-velocity/dev-ops-landing-page.md): 変更自動化、追跡性、DevOps Insights。
- [CICD Spoke](../markdown/integrate-applications/integration-hub/cicd-spoke.md): Application Repository、ATF、Instance Scan等の自動化機能。


## 14. 外部Web情報源

AutomateProは本リポジトリのServiceNow Australiaリリース文書には含まれないため、以下の公開情報を設計補足の根拠として参照する。

- [AutomatePro公式サイト](https://automatepro.com/): ServiceNow向けのAI-firstなテスト自動化／DevOpsプラットフォームとして、AutoTest、AutoDeploy、AutoMonitor、AutoDoc、AutoDev、AutoPlan等の製品群を説明している。
- [AutomatePro AutoTest](https://automatepro.com/products/autotest/): 手動テストのスケール、実ユーザーの振る舞いを模したテスト、AI-generated tests、Reusable blocks、Visual playback、複数ServiceNowインスタンスの進捗・結果確認などを説明している。
- [AutomatePro AutoDeploy](https://automatepro.com/products/autodeploy/): ServiceNowデプロイにおける手動作業、分断されたツール、可視性不足を減らし、トレーサブルなデプロイ、証跡・ログ・テスト結果の保存、承認・監査対応を支援する製品として説明している。
- [AutomatePro AutoDoc](https://automatepro.com/products/autodoc/): テスト実行レポート、ユーザーガイド、監査・コンプライアンス文書等をServiceNow Knowledge Base記事として生成・保管できる旨を説明している。
