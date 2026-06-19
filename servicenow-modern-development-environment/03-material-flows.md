---
title: "ServiceNowモダン開発環境 To-Be提案: 資材タイプ別フロー"
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
  - "資材タイプ別フロー"
related:
  - "[[02-target-architecture]]"
  - "[[04-quality-gates-and-testing]]"
---
# ServiceNowモダン開発環境 To-Be提案: 資材タイプ別フロー

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[02-target-architecture|前へ]] / [[04-quality-gates-and-testing|次へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 5. 資材タイプ別の標準フロー

### 5.1 スコープアプリ（Dev2～Dev5を中心）

1. AEMCでアプリ要求・所有者・開発者・対象環境を承認する。
2. アプリごとにGitHubリポジトリを1つ作成する。ServiceNow Git連携は非本番から行い、共有個人資格情報ではなく管理されたサービス資格情報を使う。
3. 開発者は短命ブランチまたはDeveloper Sandboxで作業し、ローカルATF/Instance Scanを実行する。
4. Pull Requestで、所有者レビュー、セキュリティ／品質チェック、関連要求・テスト証跡を確認する。
5. 承認済みコミットに対応するアプリバージョンをApplication RepositoryへPublishし、Gitタグ、アプリバージョン、Deployment Request IDを相互参照する。
6. ReleaseOpsが同一バージョンを検証→Pre-Prod→本番へ昇格する。各段階でATF、Instance Scan、承認を実施する。

**禁止事項:** 検証環境でコードを修正してそのままPublishする、GitHubから本番へ直接Pullする、環境ごとに別バージョンを作り直す。

### 5.2 ITSM/ITOM・グローバルスコープ変更（Dev1を中心）

1. 1要求／1ストーリー／1変更単位で更新セットを作成し、命名規則と親子関係を統一する。
2. 開発完了時に更新セットを固定し、Peer Review、Instance Scan、ATFを通す。
3. ReleaseOps Deployment Requestへ更新セットを添付し、Deployment Analyzerで本番または対象環境との差分・ルール・ATFカバレッジを評価する。
4. 同じDeployment Requestを検証→Pre-Prod→本番へ進める。
5. 緊急修正は例外フローで迅速に出すが、直後に通常開発ラインへバックポートし、環境差分を解消する。

GitHubを更新セットの代替経路として無理に使わない。GitHub上には設計、スクリプト、テスト仕様、補助コード等を置けるが、ServiceNow内のデプロイ正本はReleaseOpsで管理する更新セットとする。

### 5.3 XML資材

ここでいうXML資材の見直しは、現行のXML投入を一律に否定するものではない。ServiceNowでは、sys_user、sys_user_group、ロール付与、各アプリで作成したマスター系テーブルのレコードなど、通常のカスタム更新では捕捉されない「データ」や「環境依存レコード」が存在する。そのため、すべてを更新セットやアプリ資材に移せる前提にはしない。目的は、XMLを無理にゼロへすることではなく、**XMLでしか扱えないもの、別方式へ移せるもの、そもそも移送対象にすべきでないものを分け、手動投入のリスクを下げること**である。

最初に全XMLを棚卸しし、次の観点で分類する。

1. **スコープアプリへ包含できる設定:** テーブル定義、フォーム、Business Rule、Flow、Script Include、アプリ内設定など、アプリ成果物として管理できるものは、GitHub＋Application Repository経路に統合する。
2. **更新セットへ包含できる設定:** グローバルスコープ変更、ITSM/ITOM設定、対象環境間で同一にすべき設定は、更新セットへ移し、ReleaseOps経路に統合する。
3. **マスター系・データ系レコード:** sys_user、sys_user_group、グループメンバー、ロール付与、カスタムマスターテーブルの初期レコードなど、更新セットに自然には載らないものは、次の代替方式を検討する。
   - **外部の正本から同期する:** ユーザー、所属、グループ、権限がIdP、LDAP、HR、人事マスター等に正本を持つ場合は、XML移送ではなく連携・同期・手順化を優先する。
   - **Import Set/Transform Mapで投入する:** CSV等のデータファイル、変換定義、投入順、検証SQL相当の確認観点をGitHubで管理し、ReleaseOpsのRunbook taskから実行する。大量データや環境差分があるマスターにはこの方式が向く。
   - **Background Scriptの単発実行ではなく、管理されたデータ投入スクリプトにする:** 少量で冪等性を担保できる初期データは、Fix Script等として`sys_id`指定、既存判定、更新／作成の分岐、再実行時の副作用抑止を備え、アプリまたは更新セットに含める。ただし本番での任意スクリプト実行を常態化させない。
   - **アプリ導入後設定としてRunbook化する:** 環境固有値、接続先、資格情報、運用グループなど、環境ごとに値が異なるものは、同一XMLの横展開ではなく、入力値、承認者、確認方法をRunbook taskに明記する。
   - **XML例外として残す:** ServiceNow標準機能で安全に移送しにくい、`sys_id`維持が必須、またはImport Set化のコストが効果に見合わないものは、統制されたXML例外として残す。
4. **プラグイン、Store app、接続設定、データ投入等:** ServiceNow標準のインストール・設定手順、Flow/Subflow、CICD API等へ置換できるか検証する。
5. **どうしても手動Importが必要なもの:** ReleaseOps Runbook taskにし、ファイル名、バージョン、SHA-256、投入先、投入順、実行者、ダブルチェック、事前バックアップ、成功条件、事後確認、ロールバックを必須項目にする。

XML自動Importの独自実装は、APIのサポート可否、セキュリティ、再実行性、失敗時の復旧を検証したものだけ採用する。未検証の自動化より、統制されたRunbookの方を優先する。

#### 5.3.1 XML例外Runbook taskの具体イメージ

XML例外をRunbook taskにする場合は、「担当者が注意して投入する」という曖昧な手順ではなく、ReleaseOps上で次の項目を標準テンプレート化する。

- **事前条件:** 対象環境、対象アプリ／テーブル、前提プラグイン、投入前件数、関連Deployment Request、承認済みPRまたはチケットを確認する。
- **資材識別:** XMLファイル名、格納場所、Git commit SHA、SHA-256、作成元インスタンス、対象レコード種別、投入順序を記録する。
- **実行手順:** 実行者、確認者、ServiceNow画面／モジュール、入力値、Import後に押下する操作、失敗時に停止する条件を明記する。
- **検証手順:** 件数差分、代表レコード、参照整合性、権限、アプリ画面、ATFまたは手動確認観点を記録し、証跡をDeployment Requestへ添付する。
- **ロールバック／復旧:** 事前Export、削除・戻し手順、再投入可否、失敗時のエスカレーション先、後続タスクを進めてよい条件を明記する。

たとえば、カスタムマスターテーブルの初期レコードであれば、Phase 1ではXML例外Runbookとして安全に扱い、Phase 2以降でImport Set化や冪等なデータ投入スクリプト化を検討する。sys_userやsys_user_group系は、環境固有性とセキュリティ影響が大きいため、まず正本システム、権限設計、同期方式を確認し、XMLでの横展開を標準方式にしない。
