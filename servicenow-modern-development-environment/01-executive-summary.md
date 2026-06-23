---
title: "ServiceNowモダン開発環境 To-Be提案: 概要・As-Is・設計原則"
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
  - "概要・As-Is・設計原則"
related:
  - "[[02-target-architecture]]"
---
# ServiceNowモダン開発環境 To-Be提案: 概要・As-Is・設計原則

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[02-target-architecture|次へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 1. エグゼクティブサマリー

目指すべき姿は、次のように責務を分離した、監査可能で再現性のある開発・リリース基盤である。

1. **AEMC（App Engine Management Center）をガバナンスの入口にする。** アプリの受付、開発者・コラボレーター権限、アプリの可視化、デプロイ申請を一元管理する。
2. **GitHubをスコープアプリのソースコード管理とレビューの正本にする。** 1アプリ1リポジトリを原則とし、Pull Request、ブランチ保護、CODEOWNERS、セキュリティチェックを標準化する。
3. **ReleaseOpsをServiceNowインスタンス間のデプロイ・リリースオーケストレーターにする。** 更新セットとアプリを同じリリース単位で扱い、ATF、Instance Scan、Deployment Analyzer、承認、リリース日程、手動作業をPlaybookで統制する。
4. **Application Repositoryは廃止せず、スコープアプリを検証・本番へ配布する実行アーティファクト経路として残す。** Pre-Prodは標準パイプライン外の任意リハーサル環境として扱う。GitHubは本番インスタンスへの直接デプロイ経路にしない。
5. **XMLの手動Importを例外にする。** まず資材をスコープアプリ、グローバルアプリ、または更新セットへ再分類する。どうしても残るXMLだけを、チェックサム、レビュー、実行者分離、証跡、検証、ロールバック手順付きのReleaseOps Runbook taskとして管理する。
6. **品質ゲートを自動化する。** ATF、AutomatePro、Instance Scan、Deployment Analyzer、コードレビューを必須化し、将来的にDevOps Change Velocityで変更管理の証跡・承認を自動化する。

既存9インスタンスは直ちに減らさず、まず共通パイプラインと統制を導入する。その後、Developer Sandboxesで個人・ストーリー単位の分離を実現し、6台の開発環境の役割と費用対効果を再評価する。

## 2. As-Is評価

### 2.1 現行構成

| 環境 | 現行用途 | 評価 |
|---|---|---|
| Dev1 | ITSM、ITOM系の開発 | グローバルスコープ変更・更新セットが中心になる可能性が高く、App Engine系とは資材戦略を分ける必要がある。 |
| Dev2 | A社専用、App Engine共通パーツ | 「A社専用」と「共通パーツ」が同居しているため、所有権、依存関係、リリース周期を分離すべき。 |
| Dev3 | B社専用大型App Engineアプリ | スコープアプリ＋GitHubとの親和性が高い。 |
| Dev4 | C社専用大型App Engineアプリ | スコープアプリ＋GitHubとの親和性が高い。 |
| Dev5 | D社専用大型App Engineアプリ、国外チーム | 権限、時差、職務分離、輸出・データ持ち出し、認証情報管理を明文化する必要がある。 |
| Dev6 | PoC | 新方式のパイロットに適する。ただし恒久的なReleaseOpsコントローラーにはしない。 |
| 検証 | 外部結合テスト～UAT | 全チームの変更が集中するボトルネック。入場条件と予約・競合管理が必要。 |
| Pre-Prod | 任意のリリースリハーサル、メジャーアップグレード検証 | 標準パイプラインには置かず、大型・高リスク変更時だけ本番同等性を守って使う。開発・恒常的な手修正は禁止すべき。 |
| 本番 | 本番 | AEMC/ReleaseOpsのコントローラー候補。公式ドキュメントでも通常は本番をコントローラーとする。 |

### 2.2 主な課題

- Dev→検証だけが更新セット、検証→本番がApplication Repositoryとなっており、**同じ変更の識別子と証跡が経路途中で分断**される。
- 検証環境で初めてPublishするため、検証済みのアプリバージョンと開発元のGitコミット・Pull Requestを機械的に対応付けにくい。
- XML資材のImportが手動で、レビュー、実行順、再実行性、ロールバック、監査証跡が弱い。
- 1台の共有検証環境に複数開発ラインが流入するため、競合、待ち時間、UAT中の変更混入が起こりやすい。
- 開発環境ごとに方式がばらつくと、国外チームを含む横断統制と可視化が難しい。
- 品質ゲート、リリース承認、ATF/AutomateProの自動テスト結果、変更管理が自動的につながっていない。

## 3. 設計原則

1. **Build once, promote the same version.** 検証後に新しい成果物を作り直さず、同一アプリバージョン／同一更新セットを後続環境へ昇格する。
2. **Git is source, not the production transport.** GitHubはスコープアプリの履歴・レビューの正本とするが、本番への直接Pullは行わない。ServiceNowのGit連携も本番インスタンス上のアプリ管理をサポートしない。
3. **すべての本番変更はReleaseOpsのDeployment Requestまたは明示的な緊急変更を通す。** 変更、承認、テスト結果、手動作業を1つの追跡単位に束ねる。
4. **自動化できない作業も、未管理にはしない。** Runbook taskで担当者、順序、入力、証跡、完了条件を統制する。
5. **環境用途を固定する。** Pre-Prodを標準パイプライン外の任意リハーサル環境にし、Pre-Prodと本番での直接開発を禁止し、検証・UAT中の無関係変更を制御する。
6. **最小権限・職務分離を守る。** 開発者、レビュアー、テスター、リリースマネージャー、本番承認者を分離する。
