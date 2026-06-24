---
title: "ServiceNow: カスタムアプリ/カスタムテーブルのサブスクリプション登録手順"
created: 2026-06-24
updated: 2026-06-24
type: knowledge
status: draft
tags:
  - servicenow
  - subscription-management
  - custom-application
  - custom-table
  - app-engine
  - governance
  - knowledge
aliases:
  - "ServiceNowカスタムアプリのサブスクリプション登録"
  - "ServiceNowカスタムテーブルのサブスクリプション登録"
  - "Subscription Management custom tables and applications"
related:
  - "[[servicenow-update-sets-vs-application-repository]]"
  - "[[servicenow-app-repo-clone-development-mode]]"
---
# ServiceNow: カスタムアプリ/カスタムテーブルのサブスクリプション登録手順

## 目的

ServiceNow上で開発したカスタムアプリケーションや作成したカスタムテーブルは、契約上の利用権・カスタムテーブル権利数を正しく管理するため、**Subscription Management** で有効な製品サブスクリプションにマッピングする必要がある。

このKnowledgeでは、特に迷いやすい「開発環境で登録するのか、本番環境で登録するのか」を明確にし、実運用での登録手順と確認観点を整理する。

## 結論

- **本番環境では必ず登録する。** 公式ドキュメントでは、カスタムアプリケーションとカスタムテーブルを **production instance** 上で有効なサブスクリプションにマッピングすると説明されている。
- **非本番環境での登録は推奨だが必須ではない。** 開発環境・テスト環境・検証環境では、事前確認やリリースリハーサルのために登録しておくことは有効だが、契約上の最終的な管理対象は本番環境である。
- **Scoped Applicationの場合は、原則としてアプリケーション単位で登録する。** アプリケーションをサブスクリプションにマッピングすると、そのアプリケーションに後から追加したテーブルも同じサブスクリプションへ自動的にマッピングされる。
- **Global scopeのカスタムテーブルは、テーブル単位で登録する。** グローバルスコープに作成したカスタムテーブルは、Unmapped global custom tablesから個別にマッピングする。

## 判断基準

| 対象 | 登録単位 | 主な登録場所 | 備考 |
| --- | --- | --- | --- |
| Scoped Application内のカスタムテーブル | カスタムアプリケーション単位 | 本番環境のSubscription Management | 後続で追加されるテーブルも自動的に同じサブスクリプションにマッピングされる。 |
| Global scopeのカスタムテーブル | カスタムテーブル単位 | 本番環境のSubscription Management | アプリケーション単位ではなく、Custom Table Inventory上でテーブルごとにマッピングする。 |
| 開発環境だけに存在する試作テーブル | 原則、本番登録対象外 | 必要に応じて非本番で確認 | 本番へ展開しない試作・検証用テーブルは、本番の利用権管理対象にはしない。 |
| 本番リリース予定の新規カスタムアプリ | 事前に非本番で確認、本番で正式登録 | 非本番 + 本番 | 非本番で手順と推奨サブスクリプションを確認し、本番リリース後に正式登録する。 |

## 前提条件

- Subscription Managementを利用できること。
- 本番環境に対象のサブスクリプション情報が連携・表示されていること。
- 作業者に次のいずれかのロールがあること。
  - `usage_admin`
  - `sn_sub_man.admin`
  - `admin`
- どのサブスクリプションに紐付けるべきか不明な場合は、契約内容、App Engine利用有無、製品利用目的、ServiceNow担当者/ライセンス管理者の判断を確認すること。

## 推奨運用フロー

### 1. 開発環境での作業

1. Scoped ApplicationまたはGlobal scopeでテーブルを作成する。
2. アプリケーション/テーブルの用途、利用ユーザー、関連製品、移送方法を記録する。
3. 本番展開予定がある場合、どのサブスクリプションに紐付ける想定かを事前に確認する。
4. 必要に応じて、開発環境やテスト環境のSubscription Managementでマッピング手順をリハーサルする。

> 開発環境でのマッピングは「本番作業の事前確認」として扱う。開発環境で設定したからといって、本番環境のマッピングが完了するわけではない。

### 2. テスト/検証環境での確認

1. 開発環境からテスト/検証環境へアプリケーションまたは変更を移送する。
2. Subscription ManagementのIssuesで、未マッピングのカスタムアプリ/カスタムテーブルが検出されるか確認する。
3. 推奨サブスクリプションが表示される場合は、想定と一致するか確認する。
4. 推奨が表示されない場合や想定と異なる場合は、本番作業前に登録先サブスクリプションを決めておく。

### 3. 本番環境での正式登録

1. 本番環境へアプリケーションまたはカスタムテーブルをリリースする。
2. 本番環境でSubscription Managementを開く。
3. Unmapped custom applicationsまたはUnmapped global custom tablesを確認する。
4. 対象を有効な製品サブスクリプションへマッピングする。
5. 登録後、サブスクリプションの使用数・残数・マッピング結果を確認する。
6. 変更要求、リリース記録、ライセンス管理台帳に、登録先サブスクリプションと対象アプリ/テーブルを記録する。

## 手順: Scoped Applicationをサブスクリプションへ登録する

Scoped Application内にカスタムテーブルを作成している場合は、原則としてアプリケーション単位でマッピングする。

1. 本番環境にログインする。
2. Application Navigatorで次のいずれかへ移動する。
   - **Admin > Subscription Management > Issues**
   - **All > Subscription Management > Issues**
3. **Unmapped custom applications** タブを開く。
4. 未マッピングのカスタムアプリケーションを確認する。
5. 推奨サブスクリプションへ登録する場合:
   1. 対象アプリケーションのチェックボックスを選択する。
   2. **Map to product** を選択する。
   3. 内容を確認し、**Confirm** を選択する。
6. 任意のサブスクリプションへ登録する場合:
   1. 対象アプリケーションを開く。
   2. **Subscription** ルックアップで登録先サブスクリプションを選択する。
   3. **Update** を選択する。
7. 登録後、対象アプリケーションが未マッピング一覧から消えること、またはサブスクリプション詳細に反映されることを確認する。

## 手順: Global scopeのカスタムテーブルをサブスクリプションへ登録する

Global scopeで作成したカスタムテーブルは、テーブル単位でマッピングする。

1. 本番環境にログインする。
2. Application Navigatorで次のいずれかへ移動する。
   - **Admin > Subscription Management > Issues**
   - **All > Subscription Management > Issues**
3. **Unmapped global custom tables** タブを開く。
4. 未マッピングのカスタムテーブルを確認する。
5. 推奨サブスクリプションへ登録する場合:
   1. 対象テーブルのチェックボックスを選択する。
   2. **Map to product** を選択する。
   3. **Save** を選択する。
6. 任意のサブスクリプションへ登録する場合:
   1. 対象テーブルを開く。
   2. **Custom Table Inventory** フォームの **Subscription** ルックアップで登録先サブスクリプションを選択する。
   3. **Update** を選択する。
   4. 未登録テーブルが複数ある場合は、同じ手順を繰り返す。
7. 登録後、Custom Table Inventoryおよびサブスクリプション詳細で反映を確認する。

## 反映タイミングの注意

- 未マッピングのカスタムアプリケーション/カスタムテーブルや推奨サブスクリプションは、作成直後ではなく **翌日** にIssues上へ表示される場合がある。
- Custom Applicationフォームからマッピングした場合、Subscription Management側の表示更新が翌日になる場合がある。
- 本番リリース直後にIssuesへ出てこない場合でも、対象が不要という意味ではない。翌日以降に再確認する。

## 本番作業時のチェックリスト

- [ ] 対象がScoped ApplicationかGlobal scopeのテーブルかを確認した。
- [ ] 本番環境に対象アプリ/テーブルがリリース済みである。
- [ ] 本番環境のSubscription Managementに対象サブスクリプションが存在する。
- [ ] 登録先サブスクリプションが契約・用途・App Engine利用方針と一致している。
- [ ] 推奨サブスクリプションを採用するか、任意のサブスクリプションを選ぶかを判断した。
- [ ] 登録後に未マッピング一覧から対象が解消されたことを確認した。
- [ ] サブスクリプションのカスタムテーブル使用数・残数を確認した。
- [ ] 変更要求/リリース記録/ライセンス台帳に登録結果を記録した。

## よくある誤解

### 開発環境で登録すれば本番にも反映されるか

反映されない。Subscription Managementのマッピングは、対象インスタンス上のサブスクリプション管理情報である。開発環境で登録しても、本番環境での登録作業は別途必要になる。

### 非本番環境では登録しなくてよいか

必須ではないが、推奨される。非本番環境で登録先候補、権限、UI表示、手順を確認しておくと、本番リリース時の判断ミスを減らせる。

### Scoped Application内のテーブルも1件ずつ登録する必要があるか

通常はアプリケーション単位で登録する。アプリケーションをサブスクリプションにマッピングすると、そのアプリケーションに後から追加したテーブルも同じサブスクリプションへ自動的にマッピングされる。

### Global scopeのテーブルはどう扱うか

Global scopeのカスタムテーブルは、アプリケーション単位ではなくテーブル単位で登録する。

### 推奨サブスクリプションが表示されない場合はどうするか

対象がIssuesに表示されるまで翌日以降に再確認する。表示されない、推奨がない、または推奨が妥当でない場合は、Custom ApplicationまたはCustom Table Inventory側から任意のサブスクリプションを選択する運用を検討する。

## 運用ルール案

- 本番に存在するカスタムアプリ/カスタムテーブルは、原則すべてSubscription Managementでマッピングする。
- 本番リリース手順書に「Subscription Management確認」を必須タスクとして入れる。
- Scoped Applicationはアプリケーション単位、Global scopeはテーブル単位で登録する。
- 新規テーブル追加を含むリリースでは、リリース翌営業日にIssuesを再確認する。
- サブスクリプション更新時は、既存のアプリ/テーブルのマッピングを棚卸しする。
- 契約上の判断が必要な場合は、ServiceNow契約管理者またはServiceNow担当者へ確認してから登録する。

## 参考情報

- ServiceNow Docs: Managing custom tables and applications in Subscription Management
- ServiceNow Docs: Map a custom application to a product subscription in Subscription Management
- ServiceNow Docs: Map custom tables to a product subscription in Subscription Management
- ServiceNow Docs: Addressing issues in Subscription Management

## Obsidianリンク

- [[servicenow-update-sets-vs-application-repository]]
- [[servicenow-app-repo-clone-development-mode]]
