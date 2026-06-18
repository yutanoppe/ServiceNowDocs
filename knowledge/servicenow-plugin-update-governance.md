# ServiceNow インストール済みプラグイン更新の運用ベストプラクティス

## 目的

このドキュメントは、ServiceNow インスタンスにインストール済みのプラグインを、誰が、どのタイミングで、どのような手順と責任分担で更新していくべきかを整理した Knowledge です。

プラグイン更新は、単なる技術作業ではありません。プラグインには業務アプリケーション、データモデル、ロール、ACL、Script Include、Business Rule、Flow、UI、IntegrationHub の spoke などが含まれる場合があり、更新により既存業務・カスタマイズ・連携・権限に影響が出る可能性があります。

そのため、更新作業は「管理者が気づいたタイミングで本番へ適用する」のではなく、変更管理、検証、リリース判定、証跡管理を含めた運用プロセスとして扱うことが重要です。

## 基本方針

インストール済みプラグインの更新は、ServiceNow プラットフォーム管理チームが主導し、対象業務のオーナー、アプリケーションオーナー、セキュリティ担当、連携担当、テスト担当と連携して進めます。

原則として、以下の方針を採用します。

- 本番環境で直接プラグイン更新を開始しない。
- まず Sub-production 環境で更新し、影響確認と回帰テストを行う。
- 更新前に対象プラグインの目的、利用機能、依存関係、影響範囲を確認する。
- 更新は通常の Change Management プロセスで管理する。
- 重要プラグインは CAB またはリリース判定会で承認を得る。
- 更新後は Skip レコード、エラー、ログ、主要業務テスト結果を確認する。
- 更新判断、実施者、検証結果、残課題を必ず記録する。

## 役割と責任

### ServiceNow プラットフォームオーナー

ServiceNow 全体の安定稼働に責任を持つ役割です。

主な責任は以下です。

- プラグイン更新方針の策定
- 更新対象の優先順位付け
- 本番適用可否の最終判断
- リスク受容の承認
- 業務オーナー、セキュリティ、運用チームとの調整

### ServiceNow プラットフォーム管理者

実際にプラグイン更新作業を計画・実施する技術担当です。

主な責任は以下です。

- インストール済みプラグインと更新可能プラグインの棚卸し
- Sub-production 環境でのプラグイン更新
- 更新前後の設定差分、Skip レコード、ログ確認
- 影響範囲の一次分析
- 更新手順書、切り戻し方針、実施証跡の作成
- 本番適用時の実作業

### アプリケーションオーナー

対象プラグインを利用する業務アプリケーションまたは ServiceNow 製品領域の責任者です。

例:

- ITSM オーナー
- CSM オーナー
- HRSD オーナー
- ITOM オーナー
- SecOps オーナー
- SPM オーナー
- IntegrationHub / 連携基盤オーナー

主な責任は以下です。

- 対象プラグインが自業務で使われているかの確認
- 更新による業務影響の確認
- 重要シナリオの受入テスト実施または承認
- 本番適用可否の業務観点での判断

### セキュリティ・リスク担当

プラグイン更新にセキュリティ修正、認証、認可、監査ログ、データ保護、外部接続の変更が含まれる場合に関与します。

主な責任は以下です。

- セキュリティ修正の重要度確認
- ACL、Role、認証方式、連携認可への影響確認
- 脆弱性対応としての適用期限判断
- リスク受容または延期判断への助言

### 連携担当

外部システム連携、MID Server、IntegrationHub spoke、REST/SOAP API、Import Set、ETL、メール連携などに影響がある場合に関与します。

主な責任は以下です。

- 連携エンドポイント、資格情報、データ変換、スケジュールジョブへの影響確認
- 連携テストの実施
- 外部システム側の変更要否確認
- 障害時の連絡先と復旧手順の確認

### 変更管理者 / CAB

本番適用を変更管理プロセスとして統制する役割です。

主な責任は以下です。

- Change Request の妥当性確認
- 実施日時、影響、リスク、テスト結果、切り戻し方針の確認
- 本番適用承認
- 変更後レビューの実施

## RACI 例

| 作業 | Platform Owner | Platform Admin | App Owner | Security | Integration | Change Manager |
| --- | --- | --- | --- | --- | --- | --- |
| 更新候補の棚卸し | A | R | C | C | C | I |
| 影響範囲の一次分析 | A | R | C | C | C | I |
| 業務影響確認 | C | C | A/R | C | C | I |
| セキュリティ影響確認 | C | C | C | A/R | C | I |
| 連携影響確認 | C | C | C | C | A/R | I |
| Sub-production 更新 | A | R | I | I | I | I |
| 回帰テスト | A | R | R | C | R | I |
| 本番適用承認 | A | C | A/C | C | C | A/R |
| 本番更新作業 | A | R | I | I | I | C |
| 更新後レビュー | A | R | R | C | C | R |

凡例:

- R: Responsible / 実行責任
- A: Accountable / 説明責任・最終責任
- C: Consulted / 相談先
- I: Informed / 報告先

## 更新対象を把握する方法

定期的に、インストール済みプラグインと更新可能なプラグインを棚卸しします。

確認観点は以下です。

- プラグイン名
- Plugin ID
- 現在のバージョン
- 更新可能なバージョン
- 関連アプリケーションまたは製品領域
- 利用中か未利用か
- 依存プラグイン
- Store アプリかプラットフォーム標準プラグインか
- 更新に管理者操作が必要か
- セキュリティ修正または不具合修正を含むか
- 本番業務への重要度

棚卸し結果は、ServiceNow 内のナレッジ、構成管理、アプリケーション台帳、または変更管理台帳で管理します。

## 更新頻度の考え方

プラグイン更新は、以下のように分類して運用します。

### 緊急更新

セキュリティ修正、重大障害修正、ServiceNow サポートからの明確な適用指示がある場合です。

- 優先度: 高
- 承認: 緊急変更プロセス
- 検証: 最小限の必須テストを Sub-production で実施
- 本番適用: 影響範囲とリスクを明記して速やかに実施

### 定期更新

四半期、月次、メジャーバージョンアップ前後など、計画されたタイミングで行う更新です。

- 優先度: 中
- 承認: 通常変更プロセス
- 検証: 主要業務シナリオと回帰テスト
- 本番適用: リリースカレンダーに合わせて実施

### 保留更新

新機能追加が中心で、現時点で利用予定がない、または影響が大きく検証時間が不足している場合です。

- 優先度: 低から中
- 承認: 保留理由を Platform Owner が承認
- 検証: 次回リリース計画に組み込む
- 注意点: セキュリティ修正や前提バージョン変更を含む場合は長期保留しない

## 推奨プロセス

### 1. 更新候補を棚卸しする

Platform Admin は、定期的に更新可能なプラグインを確認し、更新候補リストを作成します。

リストには以下を含めます。

| 項目 | 内容 |
| --- | --- |
| Plugin name | プラグイン名 |
| Plugin ID | プラグイン ID |
| Current version | 現在のバージョン |
| Target version | 更新後バージョン |
| Application owner | 業務またはアプリケーションオーナー |
| Business criticality | 業務重要度 |
| Dependencies | 依存プラグイン |
| Expected impact | 想定影響 |
| Test owner | テスト責任者 |
| Change number | 関連 Change Request |
| Decision | Apply / Defer / Reject |
| Decision reason | 判断理由 |

### 2. 影響範囲を分析する

更新前に、少なくとも以下を確認します。

- 対象プラグインが提供する機能
- 対象機能を利用している部署や業務プロセス
- カスタマイズ済みレコードの有無
- 関連する Script Include、Business Rule、ACL、Flow、Workflow
- 関連するテーブル、フォーム、UI Policy、Client Script
- 外部連携、MID Server、資格情報、スケジュールジョブ
- 関連する Store アプリや依存プラグイン
- 既知の不具合、リリースノート、既存インシデントとの関連

### 3. Sub-production 環境で更新する

本番更新前に、原則として開発環境または検証環境でプラグインを更新します。

推奨順序は以下です。

1. 本番から最新の Clone を取得した検証環境を用意する。
2. 更新対象プラグインと依存関係を確認する。
3. 更新前の主要設定、件数、ジョブ、連携状態を記録する。
4. プラグイン更新を実行する。
5. 更新完了後、エラー、ログ、イベント、スケジュールジョブを確認する。
6. Skip レコードまたは競合が発生した場合は、内容を確認して解決方針を決める。
7. 主要業務シナリオのテストを実施する。

### 4. テストを実施する

プラグイン更新後は、技術確認と業務確認の両方を行います。

#### 技術確認

- 更新処理が正常終了していること
- System Log に重大エラーがないこと
- 対象アプリケーションの主要画面が開けること
- Script エラー、ACL エラー、Flow エラーがないこと
- スケジュールジョブやイベント処理が停止していないこと
- 連携キュー、Import Set、ECC Queue に異常がないこと

#### 業務確認

- 主要レコードの作成、更新、承認、クローズができること
- 対象業務の代表的なシナリオが完了できること
- 権限別に想定どおり表示・操作できること
- 通知、SLA、Flow、レポート、ポータル表示に問題がないこと
- 外部連携が想定どおり送受信できること

可能であれば、ATF などの自動テストと手動受入テストを組み合わせます。

### 5. 本番適用を承認する

本番適用前に、Change Request に以下を記載します。

- 更新対象プラグイン
- 更新理由
- 更新前後バージョン
- 対象環境
- 実施日時
- 影響範囲
- 業務停止の有無
- Sub-production での検証結果
- 未解決課題
- 切り戻し方針または復旧方針
- 連絡体制
- 実施者、確認者、承認者

プラグイン更新は、更新後に完全なロールバックが難しい場合があります。そのため、切り戻し方針は「ボタンで元に戻す」前提ではなく、以下を組み合わせて定義します。

- 更新前 Clone またはバックアップの取得状況
- 問題発生時の修正手順
- 無効化できる設定や Flow の確認
- 影響機能の一時停止手順
- ServiceNow サポートへのエスカレーション手順
- 業務側への代替運用手順

### 6. 本番で更新する

本番更新は、承認済み Change Request に基づいて実施します。

実施時の注意点は以下です。

- 作業開始前に関係者へ通知する。
- 更新対象と対象環境を再確認する。
- 更新中は同一領域の別リリースや更新セット適用を避ける。
- 更新ログ、System Log、イベント、ジョブ状態を確認する。
- 更新直後にスモークテストを実施する。
- 問題があれば事前に定義した連絡体制で判断する。

### 7. 更新後レビューを実施する

本番更新後、以下を確認して Change Request をクローズします。

- 更新が正常終了したこと
- 重大エラーが発生していないこと
- 業務オーナーが主要機能を確認したこと
- 連携担当が主要連携を確認したこと
- 問い合わせやインシデントが発生していない、または対応済みであること
- 判断理由、テスト結果、残課題が記録されていること

## 判断基準

プラグイン更新を適用するか保留するかは、以下の観点で判断します。

### 適用を推奨するケース

- セキュリティ修正が含まれる。
- 既知の重大不具合が修正される。
- 利用中機能の安定性や性能が改善される。
- ServiceNow サポートから更新を推奨されている。
- 次回メジャーバージョンアップの前提となる。
- 依存プラグインや Store アプリの互換性維持に必要である。

### 保留を検討するケース

- 対象機能を利用していない。
- 更新内容が新機能追加のみで、業務上の必要性が低い。
- 影響範囲が大きく、十分な検証期間が確保できない。
- 重要な業務繁忙期や凍結期間に該当する。
- 既知の制限事項が自社利用に影響する。

ただし、保留する場合も「誰が、なぜ、いつ再判断するか」を記録します。

## 更新してはいけない運用パターン

以下の運用は避けます。

- 本番環境で先に更新してから検証する。
- プラグイン更新を個人判断で実施する。
- 更新内容や影響範囲を確認せずに一括適用する。
- 業務オーナーへ確認せずに業務アプリ系プラグインを更新する。
- セキュリティや連携に影響する可能性を確認しない。
- 更新後のログ確認やスモークテストを省略する。
- 更新判断の理由を記録しない。
- 保留した更新を管理台帳に残さない。

## 推奨する管理台帳

プラグイン更新管理台帳には、以下の項目を用意します。

| カラム | 内容 |
| --- | --- |
| Plugin name | プラグイン名 |
| Plugin ID | プラグイン ID |
| Product area | ITSM、CSM、HRSD、ITOM など |
| Current version | 現在バージョン |
| Available version | 更新可能バージョン |
| Environment tested | 検証済み環境 |
| Business owner | 業務オーナー |
| Technical owner | 技術オーナー |
| Security review | Required / Not required / Completed |
| Integration review | Required / Not required / Completed |
| Test result | Pass / Fail / Not tested |
| Decision | Apply / Defer / Reject |
| Decision reason | 判断理由 |
| Change number | Change Request 番号 |
| Production date | 本番適用日 |
| Post-update issue | 更新後課題 |
| Next review date | 次回確認日 |

## チェックリスト

### 更新前チェック

- [ ] 更新対象プラグインを特定した。
- [ ] 現在バージョンと更新後バージョンを確認した。
- [ ] 対象機能の利用有無を確認した。
- [ ] 業務オーナーを特定した。
- [ ] 依存プラグインを確認した。
- [ ] カスタマイズや Skip レコードへの影響を確認した。
- [ ] セキュリティ影響を確認した。
- [ ] 連携影響を確認した。
- [ ] Sub-production 環境で更新する計画を作成した。
- [ ] テスト観点を定義した。

### 検証後チェック

- [ ] Sub-production で更新が正常終了した。
- [ ] System Log に重大エラーがない。
- [ ] Skip レコードまたは競合を確認した。
- [ ] 主要業務シナリオをテストした。
- [ ] 権限別の表示・操作を確認した。
- [ ] 連携テストを実施した。
- [ ] 業務オーナーが結果を承認した。
- [ ] 残課題とリスクを記録した。

### 本番適用前チェック

- [ ] Change Request を作成した。
- [ ] 実施日時を関係者と合意した。
- [ ] 作業手順を準備した。
- [ ] 復旧方針を準備した。
- [ ] 承認者が本番適用を承認した。
- [ ] 関係者へ事前通知した。

### 本番適用後チェック

- [ ] 更新が正常終了した。
- [ ] System Log を確認した。
- [ ] 主要画面を確認した。
- [ ] 主要業務シナリオのスモークテストを実施した。
- [ ] 主要連携を確認した。
- [ ] 業務オーナーへ完了報告した。
- [ ] Change Request に結果を記録した。
- [ ] 管理台帳を更新した。

## コメント記録例

### 適用する場合

```text
Plugin update approved and applied.
Plugin: IntegrationHub Enterprise Pack
Reason: Required bug fixes for spoke execution stability and compatibility with current release.
Validated in sub-production: DEV and UAT.
Tests: REST action execution, credential alias validation, scheduled integration flow, error handling.
Business owner: Integration Platform Owner.
Change: CHG0001234.
Result: No critical issue found.
```

### 保留する場合

```text
Plugin update deferred.
Plugin: Example Product Plugin
Reason: New feature update only. The related functionality is not currently used in production.
Risk: Low, no security fix identified in this update.
Next review: 2026-09 release planning.
Owner: ServiceNow Platform Owner.
```

### リスク受容する場合

```text
Plugin update not applied in this release window.
Reason: Regression testing found an impact on customized approval flow. Business owner accepted temporary deferral.
Mitigation: Existing version remains supported for current release; issue will be retested after remediation in UAT.
Approver: Platform Owner and Change Management Owner.
Next action: Create remediation story and reassess before next production release.
```

## まとめ

ServiceNow のプラグイン更新は、Platform Admin だけで完結する作業ではありません。プラットフォーム全体の安定性、業務影響、セキュリティ、外部連携、変更管理を含めて、複数の責任者が連携して判断する必要があります。

最も重要なポイントは以下です。

- Platform Owner が方針と最終判断を持つ。
- Platform Admin が技術調査と更新作業を実施する。
- App Owner が業務影響と受入可否を判断する。
- Security / Integration 担当が該当領域のリスクを確認する。
- Change Management が本番適用を統制する。
- 本番前に必ず Sub-production で検証する。
- 適用・保留のどちらでも判断理由と次アクションを記録する。

この運用により、プラグイン更新を安全かつ継続的に実施し、ServiceNow 環境の安定性、保守性、セキュリティを維持できます。
