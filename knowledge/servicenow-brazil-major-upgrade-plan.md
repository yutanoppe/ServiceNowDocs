# ServiceNow Brazil メジャーバージョンアップ計画ベストプラクティス

## 目的

このドキュメントは、次期 ServiceNow メジャーバージョンである **Brazil** へのアップグレードを、事前準備、検証、リハーサル、本番切替、安定化まで一貫して管理するための実務ベストプラクティスです。

ServiceNow のメジャーバージョンアップは、単なる技術作業ではなく、業務プロセス、標準機能、カスタマイズ、連携、権限、データ、運用手順を横断して確認するプログラムとして扱います。特に Brazil の正式なリリースノート、パッチ情報、既知問題、製品別の事前・事後タスクは、利用可能になり次第必ず確認し、本計画に反映してください。

## 基本方針

Brazil アップグレードでは、以下の方針を標準とします。

- **本番アップグレード前に、最低 1 回以上のフルリハーサルを実施する。**
- **アップグレード対象インスタンス、対象アプリケーション、対象連携を明確にする。**
- **Preview / sub-production での検証結果に基づき、本番実施可否を判定する。**
- **Skip レコード、カスタマイズ、非推奨機能、Store アプリ、連携影響を重点管理する。**
- **本番切替日までに、重大な未解決課題、未レビュー Skip、未承認リスクを残さない。**
- **アップグレード後は、即時確認だけでなく安定化期間を設ける。**

## 推奨タイムライン

一般的なメジャーバージョンアップでは、以下の期間を目安に計画します。組織規模、カスタマイズ量、連携数、規制要件、凍結期間に応じて調整してください。

| フェーズ | 目安 | 主な目的 |
| --- | --- | --- |
| 0. 企画・方針決定 | T-12〜10 週 | スコープ、体制、対象インスタンス、実施時期を決める |
| 1. 事前調査 | T-10〜8 週 | リリースノート、非推奨、既知問題、利用機能影響を確認する |
| 2. 事前是正 | T-8〜6 週 | 不要カスタマイズ、古い Update Set、未適用 Store 更新、ATF 不足を是正する |
| 3. Preview / 初回検証 | T-6〜4 週 | 非本番に Brazil を適用し、差分、Skip、主要業務影響を把握する |
| 4. 修正・回帰テスト | T-4〜2 週 | Skip 解決、業務テスト、連携テスト、性能確認を完了する |
| 5. 本番リハーサル・Go/No-Go | T-2〜1 週 | 手順、所要時間、体制、切戻し判断、最終リスクを確認する |
| 6. 本番アップグレード | T 日 | 変更凍結、バックアップ確認、アップグレード、即時検証を実施する |
| 7. 安定化 | T+1〜2 週 | 問い合わせ、障害、性能、業務影響、残課題を管理する |

## フェーズ 0: 企画・方針決定

### 実施事項

1. **アップグレード責任者を任命する。**
   - Platform Owner
   - Upgrade Manager
   - Technical Lead
   - Test Lead
   - Business Process Owner
   - Integration Owner
   - Security / Compliance Owner

2. **対象範囲を確定する。**
   - Production
   - Sub-production
   - Developer / Sandbox
   - MID Server
   - ServiceNow Store アプリ
   - IntegrationHub / spokes
   - 外部連携先
   - モバイル、ポータル、Workspace、Virtual Agent、Now Assist などの利用チャネル

3. **アップグレード方針を決める。**
   - 直接 Brazil に上げるか、中間リリースや最新パッチを経由するか
   - 本番実施日は業務繁忙期、リリース凍結期間、監査期間を避ける
   - 本番直前に適用する Brazil パッチレベルを決める
   - Store アプリ更新のタイミングを決める

4. **コミュニケーション計画を作成する。**
   - 影響を受ける業務部門
   - 変更審査会 / CAB
   - ヘルプデスク
   - 外部ベンダー
   - 経営層またはサービスオーナー

### 成果物

- アップグレード憲章
- 体制図 / RACI
- 対象インスタンス一覧
- マイルストーン計画
- コミュニケーション計画
- 初期リスク一覧

## フェーズ 1: 事前調査

### Brazil リリース情報の確認

Brazil の正式情報が利用可能になったら、以下を必ず確認します。

- Brazil release notes
- Brazil patch notes
- Brazil security and notable fixes
- Brazil fixed problems
- Brazil known errors / known problems
- Pre- and post-upgrade tasks for products in use
- Deprecation information
- Browser and mobile support
- Store application compatibility

特に、現在のリリースから Brazil まで複数世代をまたぐ場合は、途中リリースの累積変更、非推奨、削除、互換性変更も確認します。

### 現行環境の棚卸し

以下をアップグレード前に棚卸しします。

| 領域 | 確認内容 |
| --- | --- |
| カスタマイズ | Business Rule、Script Include、ACL、Client Script、UI Action、Flow、Workflow、Portal widget、Workspace 変更 |
| アプリケーション | インストール済みプラグイン、Store アプリ、カスタムアプリ、スコープアプリ |
| データ | 大量データテーブル、アーカイブ、監査ログ、添付ファイル、CMDB 品質 |
| 連携 | REST/SOAP、MID Server、LDAP/SSO、メール、IntegrationHub、ETL、外部監視 |
| セキュリティ | ACL、ロール、認証方式、証明書、IP 制限、監査設定 |
| UI / UX | Service Portal、Employee Center、Workspace、UI Builder、モバイル |
| 自動化 | Flow Designer、Workflow、Scheduled Job、Event、Notification、SLA |
| テスト | ATF、手動テスト、業務受入テスト、性能テスト |

### 重点リスク

Brazil アップグレードでは、以下を重点リスクとして事前に評価します。

- 重要業務テーブルに対する標準カスタマイズが多い
- ACL または認証周辺の変更が多い
- Store アプリのバージョンが古い
- MID Server または外部連携が多数ある
- Workflow から Flow Designer への移行が未完了
- Service Portal / Widget の独自実装が多い
- 過去アップグレードの Skip レコードが未整理
- ATF や回帰テストが不足している

## フェーズ 2: 事前是正

初回 Brazil 適用前に、以下の事前是正を行います。

### カスタマイズ整理

- 不要な Business Rule、Client Script、UI Policy、UI Action を廃止する。
- 標準機能で代替できるカスタマイズを削減する。
- 利用されていない Update Set、古い開発ブランチ、未完了変更を整理する。
- 重大なカスタマイズにはオーナーと業務理由を付与する。

### テスト資産整備

最低限、以下の回帰テストを用意します。

- ログイン / SSO / 多要素認証
- 主要レコードの作成、更新、承認、クローズ
- Incident / Request / Change / Problem などの主要 ITSM プロセス
- CMDB 参照、CI 選択、Discovery / Service Mapping を利用する処理
- 通知メール、イベント、SLA
- 主要 Flow / Workflow
- ポータル、カタログ、Workspace、モバイル
- 主要外部連携
- 代表的な権限ロールごとの操作

ATF で自動化できるものは優先して自動化し、画面変更や外部連携など自動化が難しいものは手動テストとして明文化します。

### Store アプリとプラグイン

- Store アプリの互換性を確認する。
- アプリ更新を Brazil 前に行うか、Brazil 後に行うかを決める。
- ベンダー管理アプリは、ベンダーから Brazil 対応方針を取得する。
- 未使用プラグインや非推奨機能を確認する。

## フェーズ 3: Preview / 初回検証

### 実施前準備

1. Production に近い sub-production を最新クローンする。
2. 開発中変更を凍結または識別する。
3. 連携先が検証環境に向いていることを確認する。
4. メール送信、外部 API 呼び出し、バッチ実行の誤作動を防止する。
5. Upgrade Preview または Upgrade Center で事前影響を確認する。

### 初回 Brazil 適用後の確認

アップグレード完了後、直ちに以下を確認します。

- Upgrade Monitor / Upgrade History の結果
- Upgrade duration と想定停止時間との差分
- Skipped Changes to Review
- Upgrade errors / warnings
- Plugin activation failures
- Store app compatibility issues
- Clone 後設定差分
- 主要画面の表示崩れ
- 主要連携の疎通
- Background Script / Scheduled Job の異常
- System Logs / Transaction Logs / Node logs のエラー傾向

### 初回検証の完了条件

- Brazil 適用の所要時間が記録されている。
- Skip レコードの件数、分類、優先度が把握できている。
- 重大なアップグレードエラーが一覧化されている。
- 主要業務の Smoke Test が完了している。
- 本番までに解決すべき課題が Backlog 化されている。

## フェーズ 4: Skip・課題解決・回帰テスト

Skip レコードの詳細な扱いは、既存の Skip レコード管理ナレッジを参照してください。Brazil 計画では、以下の完了条件を設定します。

- Priority 1 / Priority 2 の Skip は全件レビュー済み。
- ACL、Business Rule、Script Include、Flow、Workflow の Skip は全件判断済み。
- Retain / Merge / Revert / Reviewed の判断理由が記録済み。
- Merge または Revert したレコードは、関連業務テストが Pass 済み。
- 本番前に未レビューの重大 Skip が残っていない。

### 課題管理の分類

| 分類 | 説明 | 本番前の扱い |
| --- | --- | --- |
| Blocker | 業務停止、ログイン不可、重大セキュリティ影響 | 必ず解決 |
| Critical | 主要業務が実行不可、重要連携不可 | 原則解決。例外は承認必須 |
| High | 代替手段はあるが影響大 | 解決または明確な回避策が必要 |
| Medium | 限定的な業務影響 | 安定化期間で対応可 |
| Low | 表示、文言、軽微な改善 | 本番後対応可 |

### 回帰テストの観点

- 標準機能が期待どおり動作するか
- カスタマイズが Brazil でも動作するか
- 既存データに対する処理が問題ないか
- ロール別に必要な操作が可能か
- 通知、承認、SLA、エスカレーションが動くか
- 外部連携の認証、データ形式、エラー処理が動くか
- 画面性能、リスト表示、検索、レポートが許容範囲か
- 監査ログ、セキュリティログ、証跡が維持されるか

## フェーズ 5: 本番リハーサルと Go/No-Go

### 本番リハーサル

本番に近い条件で、以下を通しで確認します。

1. 変更凍結開始
2. 最終クローンまたは比較確認
3. アップグレード要求
4. Upgrade Monitor 監視
5. Post-upgrade tasks 実行
6. Store アプリ更新
7. Skip レコード確認
8. Smoke Test
9. 業務代表テスト
10. 連携疎通
11. Go/No-Go 判定
12. 周知

リハーサルでは、手順の正しさだけでなく、担当者、所要時間、判断ポイント、連絡経路、エスカレーション先も検証します。

### Go/No-Go 基準

以下を満たす場合に Go とします。

- Blocker / Critical 課題が解決済み、または正式承認された回避策がある。
- 重大 Skip がレビュー済み。
- 主要業務の回帰テストが Pass している。
- 主要連携の疎通が確認済み。
- 本番手順、担当、連絡先、時間割が確定している。
- 変更凍結範囲が合意済み。
- ヘルプデスクと業務部門への周知が完了している。
- 切戻しではなく、復旧・ServiceNow Support 連携・回避策を含む障害対応計画が明確である。

## フェーズ 6: 本番アップグレード

### 直前チェックリスト

- 変更凍結が開始されている。
- 本番直前の未コミット Update Set / アプリ変更が確認されている。
- 重要な Scheduled Job の実行タイミングを確認している。
- メール、連携、バッチの影響を把握している。
- ServiceNow Support への連絡経路を確認している。
- 業務部門、ヘルプデスク、監視チームへの周知が完了している。
- 本番後 Smoke Test の担当者が待機している。

### 本番後即時確認

アップグレード完了後、以下を優先して確認します。

1. 管理者ログイン
2. 一般ユーザーログイン / SSO
3. 主要ポータル / Workspace 表示
4. 主要レコード作成・更新
5. 承認処理
6. 通知メール
7. SLA / Flow / Scheduled Job
8. 主要連携
9. 主要レポート / ダッシュボード
10. Upgrade History / Skip / Error logs

## フェーズ 7: 安定化

本番アップグレード後、少なくとも 1〜2 週間は安定化期間を設けます。

### 監視項目

- P1/P2 インシデント
- ログイン失敗
- 連携失敗
- メール送受信失敗
- Flow / Workflow エラー
- Scheduled Job エラー
- Transaction response time
- Slow query / slow script
- ユーザー問い合わせ傾向
- Skip レコード由来の後続影響

### 安定化完了条件

- 重大障害が解消している。
- 主要業務が通常運用に戻っている。
- 本番後課題の対応方針が決まっている。
- 未対応 Skip のリスクが承認されている。
- Lessons Learned が記録されている。
- 次回アップグレードに向けた改善アクションが作成されている。

## RACI 例

| 作業 | Platform Owner | Upgrade Manager | Technical Lead | Test Lead | Business Owner | Security | Vendor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 方針決定 | A | R | C | C | C | C | C |
| スコープ定義 | A | R | R | C | C | C | C |
| リリースノート確認 | C | R | R | C | C | C | C |
| Skip レビュー | A | R | R | C | C | C | C |
| 回帰テスト | C | C | C | R | A/R | C | C |
| 連携テスト | C | R | R | C | C | C | R |
| Go/No-Go | A | R | C | C | A/R | C | C |
| 本番実施 | A | R | R | C | C | C | C |
| 安定化 | A | R | R | R | R | C | C |

A = Accountable、R = Responsible、C = Consulted

## 管理台帳テンプレート

### アップグレード課題台帳

| ID | 分類 | 件名 | 影響 | 優先度 | 担当 | 期限 | 状態 | 回避策 | 本番可否 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UP-BRA-001 | Skip | 重要 Business Rule の差分確認 | Incident assignment | Critical | ITSM Lead | YYYY-MM-DD | Open | 手動割当 | No-Go |

### テスト台帳

| ID | 業務領域 | テスト名 | 種別 | 担当 | 結果 | 証跡 | 備考 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-BRA-001 | ITSM | Incident 作成から解決 | ATF | Test Lead | Pass | ATF Result URL | なし |

### Go/No-Go 判定表

| 判定項目 | 基準 | 結果 | 承認者 | コメント |
| --- | --- | --- | --- | --- |
| Critical 課題 | 0 件、または承認済み回避策あり | TBD | Platform Owner |  |
| 主要業務テスト | すべて Pass | TBD | Business Owner |  |
| 主要連携 | すべて疎通済み | TBD | Integration Owner |  |
| 重大 Skip | 全件レビュー済み | TBD | Technical Lead |  |
| 周知 | 完了 | TBD | Upgrade Manager |  |

## 成功指標

Brazil アップグレードの成功は、単にアップグレードが完了したことではなく、以下で評価します。

- 本番アップグレードが予定時間内に完了した。
- ログイン、主要業務、主要連携が当日中に正常確認された。
- 本番後 P1/P2 障害が発生しない、または迅速に復旧した。
- 未レビューの重大 Skip が残っていない。
- 業務部門の受入基準を満たしている。
- アップグレード起因の手戻り変更が最小化されている。
- Lessons Learned が次回計画に反映されている。

## 参考情報

- ServiceNow product documentation: ServiceNow upgrades
- ServiceNow product documentation: Upgrade planning checklist
- ServiceNow product documentation: Upgrade tools and resources
- ServiceNow product documentation: Pre- and post-upgrade tasks for products in use
- ServiceNow product documentation: Release notes and fixed problems for the target family release
- Repository knowledge: `knowledge/servicenow-skip-record-management.md`
