# ServiceNowモダン開発環境 To-Be提案: GitHub運用標準

- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 7. GitHub運用標準

### 7.1 GitHub連携の意義とレビュー方針

ServiceNowのGit連携でリポジトリに登録される多くのファイルは、JavaやJavaScriptの一般的なソースコードではなく、ServiceNowが生成するXMLである。そのため、GitHub導入の価値を「XMLを人がすべて行単位で読むこと」と捉えると効果が出にくい。GitHubは、ServiceNow上の変更を**人がレビューしやすい単位に整理し、変更理由・承認・差分・バージョンを追跡する正本**として使う。

GitHub連携の主な意義は次の通りである。

- **変更の追跡性:** どの要求、Issue、Pull Request、コミット、アプリバージョンが本番に入ったかを後から追える。ServiceNow内だけの履歴より、監査・障害調査・ロールバック判断が容易になる。
- **レビューと職務分離:** 開発者が直接`main`へ反映せず、CODEOWNERSや必須レビューにより、アプリ所有者、Tech Lead、セキュリティ担当が承認してからリリース候補にできる。
- **リリース単位の固定:** Gitタグ、Application Repositoryのアプリバージョン、ReleaseOps Deployment Requestを対応付けることで、検証済みの同一成果物をPre-Prod／本番へ昇格できる。
- **差分の早期検知:** XML全体を読むのではなく、変更されたメタデータ種別、ファイル数、削除・追加、Script IncludeやBusiness Rule等のスクリプト部分、権限・テーブル定義・Flow変更など、リスクの高い差分を重点的に確認できる。
- **標準チェックの入口:** Secret scanning、ブランチ保護、PRテンプレート、CODEOWNERS、リンクされたチケット、テスト結果、Instance Scan結果をPull Requestに集約できる。

Pull Requestレビューは、XMLの文字列差分だけに依存しない。標準レビューは次の三層で行う。

1. **ServiceNow画面での機能レビュー:** レビュアーは対象インスタンス上でフォーム、Flow、権限、テーブル、ATF結果、Instance Scan結果を確認する。PRはその証跡と承認の器として使う。
2. **GitHub上のメタデータレビュー:** 変更ファイルの種類、スクリプト部分、削除・リネーム、権限・ロール・ACL・データモデル変更、依存アプリ変更を重点的に見る。XML全行の目視確認を必須にしない。
3. **ReleaseOps上の昇格前レビュー:** Deployment Analyzer、ATF、Runbook task、承認履歴で、対象環境との差分とリリースリスクを確認する。

したがって、GitHubは「ServiceNow XMLを通常のソースコードのように全行レビューするためのツール」ではなく、「ServiceNow上で確認した変更を、レビュー可能な単位と監査可能な履歴に変換し、ReleaseOpsで同じ成果物を昇格するための統制基盤」と位置付ける。

### 7.2 リポジトリ設計

- 原則 **1 ServiceNowアプリ = 1 GitHubリポジトリ**。これはServiceNow Git連携の要件にも合致する。
- Dev2の共通部品はA社専用アプリから分離し、明確なAPI・依存バージョンを持たせる。
- 顧客別アプリ、共通部品、テスト資材、補助ツールを混在させない。
- GitタグとServiceNowアプリバージョンを対応付ける。例: `v2.4.0` ↔ Application Repository `2.4.0`。

### 7.3 ブランチ・レビュー

- `main`を常にリリース可能な状態にし、直接Pushを禁止する。
- 短命feature/fixブランチを使い、長期間の顧客別ブランチは避ける。
- 必須PRレビュー、CODEOWNERS、署名／保護ルール、Secret scanning等を組織標準に合わせて有効化する。
- Pull Requestテンプレートには、対象要求、ServiceNow上の確認画面、ATF/Instance Scan結果、スクリーンショットまたは確認証跡、Application Repositoryバージョン、ReleaseOps Deployment Request予定を記載させる。
- GitHub上でServiceNow生成XMLを無秩序に手編集しない。ServiceNowのGit連携は外部編集への対応が限定的で、検証・サニタイズが行われるため、外部編集範囲をルール化する。
- ServiceNow Git連携ではリポジトリ資格情報がインスタンスの開発者間で共有されるため、個人PATではなく、ローテーション可能な最小権限資格情報とMID Server経由接続を検討する。

### 7.4 国外チーム（Dev5）

- GitHub Team、AEMC collaboration、ServiceNow roleをD社スコープに限定する。
- 本番資格情報・本番承認権限は付与せず、開発と本番リリースを分離する。
- テストデータの匿名化、個人情報・機密情報の持ち出し、アクセス時間帯、監査ログ保管、資格情報の管理主体を明文化する。
- PRレビューは国内責任者または指定CODEOWNERを必須にする。
