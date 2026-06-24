---
title: "ServiceNow: Update SetでコミットしたスコープアプリをApplication Repository運用へ戻す方法"
created: 2026-06-24
updated: 2026-06-24
type: knowledge
status: draft
tags:
  - servicenow
  - application-repository
  - update-set
  - scoped-application
  - sys-update-xml
  - replace-on-upgrade
  - knowledge
aliases:
  - "KB2717193"
  - "Update Setコミット後にApplication Repositoryへ戻す"
related:
  - "[[servicenow-app-repo-clone-development-mode]]"
  - "[[servicenow-skip-record-management]]"
  - "[[servicenow-plugin-update-governance]]"
source:
  kb: "KB2717193"
  title: "更新セットを介してアプリケーションに変更をコミットした後、アプリケーションリポジトリの使用に戻る方法"
  last_updated: "2026-05-28"
  visibility: "public"
---
# ServiceNow: Update SetでコミットしたスコープアプリをApplication Repository運用へ戻す方法

## 目的

このドキュメントは、ServiceNow KB2717193「更新セットを介してアプリケーションに変更をコミットした後、アプリケーションリポジトリの使用に戻る方法」の内容を、実務で参照しやすい Knowledge として整理したものです。

対象は、もともと Application Repository からインストール/更新していたスコープ対象アプリに対して、誤って Update Set をコミットしてしまった後、再び Application Repository を使う運用へ戻したいケースです。

## 結論

スコープ対象アプリの開発・移送では、**Update Set 運用と Application Repository 運用を併用しない**ことが原則です。

Application Repository からインストールしたアプリは、その後の開発・公開・インストールも Application Repository に統一します。Update Set で開発/移送するアプリは、引き続き Update Set の方式に統一します。両方を混在させると、変更のスキップ、コミットエラー、アップグレード時の競合などが発生しやすくなります。

ただし、過去に Application Repository を使用していたアプリであれば、誤って Update Set をコミットした後でも、特別な手順により Application Repository 運用へ戻せる場合があります。

## 適用できるケース / できないケース

### 適用できるケース

以下を満たす場合は、Application Repository 運用へ戻せる可能性があります。

- 対象がスコープ対象アプリである。
- 対象アプリを過去に Application Repository からインストール/更新したことがある。
- その後、誤って同一アプリの変更を Update Set としてターゲットインスタンスへコミットしてしまった。
- 開発元インスタンスから、対象アプリの最新状態を Application Repository へ公開できる。

### 適用できないケース

アプリが最初から Update Set 経由でインストールされており、過去に Application Repository を使ったことがない場合、この方法は使えません。

その場合に Application Repository 運用へ切り替えるには、原則として対象アプリを完全に削除し、Application Repository から新規インストールし直す必要があります。既存データ、設定、依存関係、参照整合性に影響するため、事前に十分な検証とバックアップ方針を用意します。

## 発生し得る問題

Update Set と Application Repository を同じスコープアプリで混在させると、以下のような問題が起きる可能性があります。

- Application Repository からのインストール/更新時に、過去の `sys_update_xml` レコードが競合を引き起こす。
- 本来 Application Repository から適用したいアプリケーションファイルが、顧客更新として扱われてスキップされる。
- 更新時にコミットエラーや予期しない差分が発生する。
- どの移送経路を正とするかが不明確になり、変更管理やリリース証跡が破綻する。
- インスタンス固有設定まで誤って上書き対象になり、データ損失や設定消失につながる。

## 復旧方針

復旧の考え方は、対象アプリ全体を Application Repository から提供されるベースシステムバージョンへ戻すことです。

そのためには、ターゲットインスタンス側に存在する対象アプリの `sys_update_xml` レコードについて、Application Repository からの更新時に競合として扱われないよう、`replace_on_upgrade` を `true` に設定します。

この設定により、対象の Customer Update はアップグレード/アプリ更新時に置き換え可能なものとして扱われ、Application Repository からインストールされるアプリケーションファイルのベースシステムバージョンを適用しやすくなります。

## 推奨手順

### 1. 開発インスタンスから Application Repository へ公開する

まず、開発インスタンスで対象アプリの最新状態を Application Repository へ公開します。

この操作により、対象アプリの最新バージョンがパッケージ化され、ターゲットインスタンスで Application Repository からインストール/更新できる状態になります。

### 2. ターゲットインスタンスの対象 `sys_update_xml` を確認する

ターゲットインスタンスで、対象アプリに紐づく `sys_update_xml` レコードを確認します。

確認観点は以下です。

- `application` フィールドが対象アプリの `sys_store_app` レコードを指しているか。
- 過去に Update Set でコミットされた対象アプリの Customer Update が含まれているか。
- インスタンス固有設定や、各インスタンスで異なる値を持つべき設定が含まれていないか。
- 上書きされるとデータ損失につながる列定義や設定が含まれていないか。

### 3. `replace_on_upgrade` を `true` に設定する

ターゲットインスタンスで、対象アプリに紐づくすべての `sys_update_xml` レコードについて、`replace_on_upgrade` を `true` に設定します。

KB では、例として以下のような Background Script が示されています。

```javascript
preventConflicts('12345678ABCDEFGH12345678ABCDEFGH'); // Sys ID of your app's sys_store_app record
function preventConflicts(appid) {
    var gr = new GlideRecord('sys_update_xml');
    gr.addQuery('application', appid);
    gr.query();
    while(gr.next()) {
        gr.replace_on_upgrade = true;
        gr.update();
    }
}
```

このスクリプトの引数には、対象アプリの `sys_store_app` レコードの Sys ID を指定します。

### 4. Application Repository から最新バージョンをインストールする

`replace_on_upgrade` の設定後、ターゲットインスタンスで Application Repository から対象アプリの最新バージョンをインストール/更新します。

正しく実行されると、アプリ内の各アプリケーションファイルに対して、Application Repository 側のベースシステムバージョンが適用されます。

### 5. 更新後に検証する

更新後は、少なくとも以下を確認します。

- 対象アプリが Application Repository からインストール/更新された状態になっているか。
- Skipped Changes やエラーが残っていないか。
- 主要なアプリケーションファイルが期待どおりのバージョンになっているか。
- Update Set 由来の不要な差分が残っていないか。
- インスタンス固有設定、プロパティ、選択肢、テーブル列、データが意図せず上書き/消失していないか。
- 主要業務シナリオ、権限、Flow/Workflow、連携、通知、UI が正常に動作するか。

## 重要な注意点

### スクリプトは例であり、そのまま実行する前に検証する

KB のスクリプトはサンプルです。実行は自己責任であり、誤った対象に実行すると `sys_update_xml` データを不可逆的に破損させる可能性があります。

本番相当のターゲットインスタンスで実行する前に、必ず Sub-production 環境で対象件数、対象レコード、影響範囲を確認します。

### `replace_on_upgrade` は広範な上書きにつながる

`replace_on_upgrade` を `true` にすると、対象の更新/カスタマイズはアップグレード時に置き換え可能なものとして扱われます。

そのため、以下のようなレコードが含まれる場合は特に注意が必要です。

- インスタンスごとに異なる値を持つべき設定
- 環境別の接続先、認証、通知、スケジュール設定
- 顧客固有のロール、ACL、フォーム、UI Policy、Business Rule
- テーブル/カラム定義や最大長など、データ保持に影響する構成

特に、列の最大長が短くなるような更新が適用されると、既存データが失われる可能性があります。

## 実務上のチェックリスト

作業前に以下を確認します。

- [ ] 対象アプリの正しい `sys_store_app` Sys ID を確認した。
- [ ] 対象アプリが過去に Application Repository からインストールされていたことを確認した。
- [ ] 開発インスタンスから最新バージョンを Application Repository へ公開した。
- [ ] ターゲットインスタンスで対象 `sys_update_xml` 件数を事前に確認した。
- [ ] `replace_on_upgrade` を変更する対象レコード一覧をエクスポート/記録した。
- [ ] インスタンス固有設定が上書き対象に含まれないか確認した。
- [ ] Sub-production 環境で同じ手順を検証した。
- [ ] Application Repository からのインストール/更新後の確認項目を定義した。
- [ ] 切り戻し方針、バックアップ、変更管理チケットを準備した。

## 運用ルールとして定めるべきこと

再発防止のため、以下をチームの開発/リリース標準に明記します。

- スコープアプリごとに、移送方式を Application Repository または Update Set のどちらかに固定する。
- Application Repository 運用のアプリに対して、同一スコープの Update Set をコミットしない。
- Update Set に対象スコープの更新が含まれている場合、レビュー時にブロックする。
- Application Repository へ公開する開発元インスタンスを明確にする。
- ターゲットインスタンスでのアプリ更新は、Application Repository から実施する。
- 例外対応を行う場合は、事前に影響範囲、切り戻し、検証計画を承認する。

## 関連ナレッジ

- [[servicenow-app-repo-clone-development-mode]]
- [[servicenow-skip-record-management]]
- [[servicenow-plugin-update-governance]]
