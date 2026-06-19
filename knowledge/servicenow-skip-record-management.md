---
title: "ServiceNow メジャーバージョンアップ時の Skip レコード管理方法"
created: 2026-06-19
updated: 2026-06-19
type: knowledge
status: draft
tags:
  - servicenow
  - upgrade
  - skip-records
  - governance
  - knowledge
aliases:
  - "Skip レコード管理"
related:
  - "[[servicenow-brazil-major-upgrade-plan]]"
  - "[[servicenow-plugin-update-governance]]"
---
# ServiceNow メジャーバージョンアップ時の Skip レコード管理方法

## 目的

このドキュメントは、ServiceNow のメジャーバージョンアップ、パッチ適用、プラグイン更新などで発生する Skip レコード（Skipped Records / Skipped Changes）を、どのように確認・管理・解決するかを実務向けに整理したものです。

Skip レコードは、単なるエラーではありません。ServiceNow が標準機能の更新を適用しようとした際に、対象レコードが顧客環境でカスタマイズ済みであるため、自動上書きを避けてレビュー対象として残したものです。

## Skip レコードとは

ServiceNow では、顧客が変更した標準レコードは Customer Updates `[sys_update_xml]` に記録されます。アップグレード時に ServiceNow 標準側にも同じレコードの更新がある場合、プラットフォームは顧客カスタマイズを保護するため、標準更新を自動適用せず Skip レコードとして記録します。

つまり Skip レコードは、以下の衝突を示します。

- ServiceNow 標準機能として更新された内容
- 顧客環境で過去にカスタマイズされた内容

そのため、Skip レコード対応では「すべて標準に戻す」または「すべてカスタマイズを残す」のではなく、1件ずつ差分を確認して判断することが重要です。

## 管理の基本方針

Skip レコード管理の目的は、Skip 件数を機械的にゼロにすることではありません。重要なのは、各 Skip レコードについて以下を明確にすることです。

- 誰が確認したか
- 何を確認したか
- Retain / Merge / Revert / Reviewed のどれを選んだか
- なぜその判断をしたか
- どのテストで影響確認したか

特に本番アップグレード前には、未レビューの Skip レコードを原則として残さない運用が望ましいです。

## 主な確認場所

Skip レコードは、主に Upgrade History または Upgrade Monitor から確認します。

代表的な確認手順は以下です。

1. ServiceNow に管理者権限でログインする。
2. **All > Admin Center > Upgrade Management > Upgrade History** を開く。
3. 対象のアップグレード履歴を開く。
4. 関連リストの **Skipped Changes to Review** を確認する。
5. 必要に応じて **Skipped Changes Reviewed** も確認する。

関連リストの代表例は以下です。

| 関連リスト | 用途 |
| --- | --- |
| Skipped Changes to Review | 未レビューまたは未解決の Skip レコードを確認する |
| Skipped Changes Reviewed | レビュー済みの Skip レコードを確認する |
| Customization Unchanged | カスタマイズはあるが、今回の標準差分がないレコードを確認する |
| Changes Applied | 今回適用された標準更新を確認する |
| Claim Outcomes to Review | Claim Status の確認や解決対象を確認する |

日々の進捗管理では、**Skipped Changes to Review をゼロに近づけること**を完了条件にすると管理しやすくなります。

## 解決ステータスの考え方

Skip レコードでは、差分確認後に以下のような判断を行います。

| 判断 | 意味 | 主な利用場面 |
| --- | --- | --- |
| Reviewed and Retained / Retain | 顧客カスタマイズをそのまま残す | 自社要件を標準更新より優先する場合 |
| Reviewed and Merged / Merge | 標準更新の必要部分を取り込みつつ、顧客カスタマイズも残す | セキュリティ修正、API 変更、性能改善などを取り込む場合 |
| Reviewed and Reverted / Revert to Base System | 顧客カスタマイズを破棄して標準に戻す | カスタマイズが不要、または標準機能で代替可能な場合 |
| Reviewed | 内容確認済みだがレコード自体には処置しない | 影響なし、利用なし、または別方式で対応済みの場合 |
| Not Reviewed | 未確認 | 後続担当者による確認が必要な場合 |

## 推奨する処理順序

大量の Skip レコードがある場合、すべてを同じ優先度で処理すると時間がかかります。以下の順序で優先順位を付けると効率的です。

1. **Priority 1 / Priority 2 の Skip レコード**
   - Business Rule
   - Script Include
   - ACL
   - UI Page
   - UI Macro
   - Flow
   - Workflow
2. **主要業務に関わるテーブル**
   - Incident
   - Change
   - Request
   - CMDB
   - HR
   - CSM
3. **セキュリティや認可に関わるレコード**
   - ACL
   - Role
   - Authentication
   - Integration
4. **画面・フォーム・選択肢・レポート系**
   - Form
   - Related List
   - Choice
   - Report
5. **影響範囲が限定的な設定レコード**

## 具体的な解決手順

### 1. Skip レコード一覧を抽出する

まず、対象 Upgrade History の **Skipped Changes to Review** を開き、一覧を確認します。必要に応じて Excel などにエクスポートし、担当者、判断結果、テスト結果を管理します。

管理台帳には以下のカラムを用意すると便利です。

| カラム | 内容 |
| --- | --- |
| Upgrade version | 対象リリースまたはアップグレードバージョン |
| sys_id | Skip レコードの sys_id |
| Target name | 対象レコード名 |
| Table | 対象テーブル |
| Type | Business Rule、ACL、Script Include など |
| Plugin / Application | 関連アプリケーション |
| Priority | ServiceNow 側の優先度 |
| Disposition | Skipped、Reverted など |
| Resolution | Retained、Merged、Reverted、Reviewed など |
| Owner | 判断責任者 |
| Business owner | 業務確認者 |
| Decision reason | 判断理由 |
| Test case | ATF または手動テスト名 |
| Test result | Pass / Fail |
| Notes | 補足事項 |

ただし、最終的な判断証跡は外部台帳だけでなく、ServiceNow の Skip レコードのコメントにも必ず残します。

### 2. 差分を確認する

各 Skip レコードを開き、以下を確認します。

- 顧客カスタマイズの内容
- 新バージョンの ServiceNow 標準更新内容
- 差分があるフィールド
- スクリプトの場合はロジック、API、テーブル参照、権限チェック
- UI の場合は利用者影響
- ACL の場合は認可影響
- Flow / Workflow の場合は後続処理や SLA への影響

テキストフィールドやスクリプトでは、Diff/Merge ツールを使って標準更新とカスタマイズの差分を確認します。

### 3. 解決パターンを選択する

#### パターン A: カスタマイズをそのまま残す

以下の場合は、Retain を選択します。

- 自社要件が現在も有効である。
- 標準更新を取り込むと既存業務に悪影響がある。
- 標準更新が自社環境では不要である。
- 標準更新相当の対応を別方式で実装済みである。

操作例:

1. Skip レコードを開く。
2. 差分を確認する。
3. Resolution Status を **Reviewed and Retained** または Retain 系のステータスにする。
4. コメントに判断理由を記載する。
5. Update する。

コメント例:

```text
Retain. This Business Rule contains company-specific assignment logic for Japan operations.
Reviewed baseline change in the target release; baseline update is not required for our process.
Owner: ITSM Platform Team.
Validated by ATF: INC assignment regression test.
```

#### パターン B: 標準更新とカスタマイズをマージする

以下の場合は、Merge を選択します。

- ServiceNow 標準側に重要な修正が入っている。
- セキュリティ修正や性能改善が含まれる。
- API 変更や互換性対応を取り込む必要がある。
- 自社カスタマイズも引き続き必要である。

操作例:

1. Skip レコードを開く。
2. **Resolve Conflicts** をクリックする。
3. 差分を確認する。
4. 必要なフィールドやスクリプト差分をマージする。
5. **Merge** を実行する。
6. コメントに取り込んだ内容と残したカスタマイズを記載する。
7. 関連する業務テストを実施する。

コメント例:

```text
Merged. Adopted ServiceNow baseline null-check and updated API usage from the target release.
Retained company-specific validation for category/subcategory mapping.
Tested: Incident create/update, assignment, SLA start.
Owner: ITSM Platform Team.
```

#### パターン C: 標準へ戻す

以下の場合は、Revert to Base System を選択します。

- カスタマイズが不要になった。
- 標準機能で代替できるようになった。
- 古いカスタマイズがアップグレード阻害要因になっている。
- セキュリティや性能の観点で標準に戻すべきである。

操作例:

1. Skip レコードを開く。
2. 差分を確認する。
3. **Revert to Base System** をクリックする。
4. コメントに判断理由を記載する。
5. 業務影響テストを実施する。

コメント例:

```text
Reverted to base. Previous customization was introduced for legacy approval behavior.
Current baseline supports the required condition through standard configuration.
Confirmed with Change Management owner.
Regression tested: normal/standard/emergency change approval.
```

#### パターン D: レビューのみで処置しない

以下の場合は、Reviewed を選択します。

- 差分は確認したが、対象レコードが利用されていない。
- 業務影響がない。
- 別のレコードや設定で対応済みである。
- 今回のアップグレードでは操作不要である。

操作例:

1. Skip レコードを開く。
2. 差分を確認する。
3. Resolution Status を **Reviewed** にする。
4. コメントに判断根拠を記載する。
5. Update する。

コメント例:

```text
Reviewed only. Target record is not used in the current implementation.
No action required for this upgrade.
Confirmed with application owner.
```

## 具体例

### 例 1: Business Rule の Skip

対象:

- Table: `incident`
- Type: Business Rule
- 内容: 標準側で null チェックが追加され、自社側で独自の assignment ロジックがある。

判断:

- 標準の null チェックは有用。
- 自社 assignment ロジックも必要。

解決:

- **Merge** を選択する。

コメント例:

```text
Merged baseline null-check from the target release.
Retained custom assignment logic for Japan Service Desk.
Validated incident creation, reassignment, and SLA start.
```

### 例 2: ACL の Skip

対象:

- Type: ACL
- 内容: 標準側で追加条件があり、自社側で独自ロール条件がある。

判断:

- 権限制御のため Retain だけで済ませるのは危険。
- 標準側の追加条件がセキュリティ修正である可能性がある。

解決:

- 標準差分を必ず確認する。
- 必要に応じて **Merge** を選択する。
- Security Admin または Platform Owner の承認を取る。

コメント例:

```text
Merged baseline ACL condition introduced in the target release.
Retained custom role sn_custom_read_jp for regional support.
Approved by Security Admin.
Tested access with itil, admin, custom support role, and unauthorized user.
```

### 例 3: Form Layout の Skip

対象:

- Type: Form Section / UI Form
- 内容: 自社でフォーム配置を変更済み。

判断:

- 標準側で追加フィールドがある。
- 自社フォームにそのフィールドが必要か確認する。

解決:

- 必要フィールドだけ手動追加する。
- Resolution は **Reviewed and Retained** または **Merged** とする。

コメント例:

```text
Retained custom form layout.
Manually added new baseline field "resolution_code" to custom section.
Confirmed with Incident process owner.
```

### 例 4: 古い UI Policy の Skip

対象:

- Type: UI Policy
- 内容: 過去要件のための制御だが、現在は不要。

判断:

- 標準 UI Policy で代替可能。
- 自社 UI Policy が標準動作を阻害している。

解決:

- **Revert to Base System** を選択する。

コメント例:

```text
Reverted to base. Legacy UI Policy is no longer required after process redesign.
Standard behavior satisfies current requirement.
Regression tested request form behavior.
```

## Skipped Record Rules による自動化

大量の Skip レコードが毎回発生する環境では、Skipped Record Rules による自動化を検討します。

Skipped Record Rules は、アップグレード後のカスタマイズ衝突に対して、自動的に Retain などの処理を行うためのルールです。アップグレード中に自動実行することも、アップグレード後に手動実行することもできます。

### 使いどころ

- 毎回 Retain と判断している UI Form、Related List、Choice など
- 特定アプリケーションの設定系レコード
- 影響が限定的で判断基準が明確なもの
- 過去のアップグレードで同じ判断を繰り返しているもの

### 注意点

Skipped Record Rules は便利ですが、無条件に信頼すべきではありません。自動 Retain されたレコードも、重要アプリケーションではサンプリング確認または全件確認を行います。

また、Skipped Record Rules と Upgrade Plan は同一アップグレード内で併用できないため、どちらを使うか事前に運用方針を決めておきます。

## Xanadu 以降の自動 Retain に関する注意

Xanadu リリース以降、一部のテーブルでは Skip レコードを自動 Retain するデフォルトルールが導入されています。代表的な対象には以下があります。

- `sys_ui_section`
- `sys_ui_form`
- `sys_ui_form_section`
- `sysevent_email_action`
- `sys_ui_related_list`
- `sys_ui_list`
- `sys_choice`
- `sys_choice_set`
- `sys_report`
- `pa_dashboards`
- `wf_workflow`

このため、Xanadu 以降では **Skipped Changes to Review** だけでなく、**Skipped Changes Reviewed** も確認対象に含めます。自動 Retain により Reviewed 側に移動したレコードが、実際に妥当な判断だったかを確認するためです。

## 非本番アップグレード時の推奨フロー

1. サブプロダクション環境を本番から Clone する。
2. Clone 後の不要データや連携設定を調整する。
3. Upgrade Preview または Upgrade Plan を確認する。
4. アップグレードを実施する。
5. Upgrade Summary Report を確認する。
6. **Skipped Changes to Review** をエクスポートする。
7. Priority 1 / 2 から担当者を割り当てる。
8. 1件ずつ Retain / Merge / Revert / Reviewed を判断する。
9. Skip レコードにコメントを記入する。
10. ATF または手動回帰テストを実施する。
11. 判断結果とテスト結果を台帳化する。
12. 本番アップグレード手順書に反映する。

## 本番アップグレード時の推奨フロー

1. 非本番で確定した判断結果を再利用する。
2. 本番で新たに発生した Skip レコードのみ追加レビューする。
3. 重要 Skip レコードは本番切替前に確認する。
4. **Skipped Changes to Review** を原則ゼロにする。
5. 本番後、重点業務テストを実施する。
6. 残課題は Problem、Story、Defect などで管理する。

## よくある失敗と対策

### 失敗 1: すべて Retain してしまう

Retain は顧客カスタマイズを守るためには有効ですが、標準側のバグ修正、セキュリティ修正、互換性修正を取り込めない可能性があります。

対策として、Script Include、Business Rule、ACL、Flow などは必ず差分を読み、Merge 要否を判断します。

### 失敗 2: コメントを残さない

コメントがないと、次回アップグレードでなぜその判断をしたか分からなくなります。

コメントには最低限、以下を記載します。

- 判断理由
- 業務オーナーまたは承認者
- テスト内容
- Retain / Merge / Revert の根拠

### 失敗 3: 本番で初めて Skip を確認する

本番アップグレード時に初めて Skip レコードを確認すると、判断に時間がかかり、停止時間やリスクが増えます。

対策として、非本番で必ず Skip を処理し、本番では同じ判断を再実行するだけの状態に近づけます。

### 失敗 4: 自動ルールを無条件に信頼する

自動 Retain された Skip レコードは、Reviewed 側に移動するため、レビュー対象から漏れる可能性があります。

対策として、**Skipped Changes Reviewed** も確認し、自動 Retain の対象テーブル、コメント、影響範囲を確認します。

## 本番前の完了条件

本番アップグレード前には、以下を完了条件として定義することを推奨します。

- **Skipped Changes to Review** がゼロ、または明確に承認された残件のみである。
- Priority 1 / 2 の Skip レコードが全件レビュー済みである。
- ACL、Business Rule、Script Include、Flow が全件テスト済みである。
- 各 Skip レコードにコメントが残っている。
- Retain / Merge / Revert / Reviewed の判断が台帳化されている。
- ATF または手動回帰テストが完了している。
- 本番反映手順に Skip 対応が含まれている。
- 本番後確認項目が定義されている。

## まとめ

Skip レコード対応の基本は、以下の流れです。

1. Upgrade History / Upgrade Monitor で Skip レコードを確認する。
2. Priority と影響度で処理順を決める。
3. 差分を確認する。
4. Retain / Merge / Revert / Reviewed を判断する。
5. 必ずコメントを残す。
6. ATF または手動回帰テストを実施する。
7. 本番前に未レビューをなくす。
8. 繰り返し発生するものは Skipped Record Rules で自動化を検討する。

最も重要なのは、Skip レコードを単に処理済みにすることではなく、**なぜ Retain / Merge / Revert / Reviewed と判断したかを、次回アップグレード時にも説明できる状態にすること**です。
## Obsidianリンク

- [[servicenow-brazil-major-upgrade-plan]]
- [[servicenow-plugin-update-governance]]
