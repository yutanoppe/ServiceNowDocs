---
title: "ServiceNowモダン開発環境 To-Be提案: GitHub運用標準"
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
  - "GitHub運用標準"
related:
  - "[[04-quality-gates-and-testing]]"
  - "[[06-migration-roadmap]]"
---
# ServiceNowモダン開発環境 To-Be提案: GitHub運用標準

> [!note] Obsidian navigation
> [[to-be-proposal|提案インデックス]] / [[04-quality-gates-and-testing|前へ]] / [[06-migration-roadmap|次へ]]


- **作成日:** 2026-06-04
- **参照ドキュメント:** 本リポジトリのAustraliaリリース、およびAutomatePro公式公開情報
- **対象:** AEMC、ReleaseOps、GitHub、ATF、AutomateProを軸にした、ITSM/ITOMおよびApp Engineカスタムアプリの開発・テスト・リリース

## 7. GitHub運用標準

### 7.1 GitHub連携の意義とレビュー方針

ServiceNowのGit連携でリポジトリに登録される多くのファイルは、JavaやJavaScriptの一般的なソースコードではなく、ServiceNowが生成するXMLである。そのため、GitHub導入の価値を「XMLを人がすべて行単位で読むこと」と捉えると効果が出にくい。GitHubは、ServiceNow上の変更を**人がレビューしやすい単位に整理し、変更理由・承認・差分・バージョンを追跡する正本**として使う。

GitHub連携の主な意義は次の通りである。

- **変更の追跡性:** どの要求、Issue、Pull Request、コミット、アプリバージョンが本番に入ったかを後から追える。ServiceNow内だけの履歴より、監査・障害調査・ロールバック判断が容易になる。
- **レビューと職務分離:** 開発者が直接`main`へ反映せず、CODEOWNERSや必須レビューにより、アプリ所有者、Tech Lead、セキュリティ担当が承認してからリリース候補にできる。
- **リリース単位の固定:** Gitタグ、Application Repositoryのアプリバージョン、ReleaseOps Deployment Requestを対応付けることで、検証済みの同一成果物を本番へ昇格できる。Pre-Prodを使う場合も任意リハーサルとして同一成果物を適用する。
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

ServiceNowアプリのGitHub運用は、**GitFlowのような長期`develop`ブランチを置かず、`main`を常に本番リリース可能に保つトランクベース寄りの運用**を標準にする。検証環境やPre-Prod環境の状態をブランチで表現せず、リリース可否はGitタグ、Application Repositoryバージョン、ReleaseOps Deployment Requestで固定する。

#### 7.3.1 ブランチ種別と命名規則

| 種別 | 命名例 | 作成元 | 用途 | 寿命・削除ルール |
|---|---|---|---|---|
| 本線 | `main` | なし | 本番リリース可能な唯一の本線。保護し、直接Pushを禁止する。 | 永続 |
| 機能／要件 | `feature/REQ-1234-short-title` | 最新`main` | 1要件・1ストーリー・1PRの開発。 | PRマージ後に削除 |
| 不具合修正 | `fix/INC-5678-short-title` | 最新`main` | 通常リリースに載せる不具合修正。 | PRマージ後に削除 |
| 緊急修正 | `hotfix/CHG-9012-short-title` | 最新本番タグ | 本番障害など、通常リリースを待てない最小修正。 | 本番反映・`main`バックポート後に削除 |
| リリース候補 | `release/v2.4.0` | リリース対象の`main`コミット | リリース凍結後の最終確認、タグ付け、ReleaseOps申請のための一時ブランチ。 | 本番リリース後に削除またはアーカイブ |
| 実験／PoC | `experiment/POC-short-title` | 任意の非本番ベース | PoC、破壊的検証、技術検証。 | 本番リリース不可。期限を決めて削除 |

命名には要求ID、変更ID、障害IDなど、ServiceNow側の追跡IDを必ず含める。個人名だけのブランチ、顧客別の長期ブランチ、検証環境専用ブランチは標準運用にしない。

#### 7.3.2 ブランチ作成・PR・マージのルール

1. **ブランチは最新`main`から切る:** 通常変更は最新`main`から`feature/*`または`fix/*`を作る。作業中に`main`が進んだ場合は、PRレビュー前に`main`を取り込み直し、ServiceNow上のアプリ状態とGit差分を再確認する。
2. **1要件／1PRを原則にする:** 要件単位の先行リリースに備え、1つのPRに複数要件を混在させない。やむを得ず混在させる場合は、先行リリース時に分離・再テストが必要になることを事前に合意する。
3. **PRにはServiceNow証跡を添付する:** 対象要求、対象インスタンス、確認画面、ATF/Instance Scan結果、AutomatePro結果、スクリーンショットまたは確認証跡、予定Application Repositoryバージョン、ReleaseOps Deployment Request予定を記載する。
4. **`main`への直接Pushは禁止する:** 必須PRレビュー、CODEOWNERS、署名／保護ルール、Secret scanning等を組織標準に合わせて有効化する。
5. **ServiceNow生成XMLの手編集を制限する:** GitHub上でServiceNow生成XMLを無秩序に手編集しない。外部編集が必要なスクリプト、README、テスト仕様、補助コードなどは、対象範囲と反映手順をルール化する。
6. **マージ後にアプリバージョンを固定する:** PR承認後、`main`にマージし、Gitタグ、Application Repositoryバージョン、Deployment Request IDを相互参照する。
7. **マージ済みブランチは削除する:** 作業ブランチを残して再利用しない。追加変更は新しいブランチ・新しいPRで扱う。

#### 7.3.3 リリースブランチとタグの扱い

- リリース対象が決まった時点で、必要に応じて`release/vX.Y.Z`を切る。ただし、`release/*`は開発を継続する場所ではなく、リリース凍結後の最終確認と申請を安定させるための一時ブランチとする。
- `release/*`へ入れてよい変更は、リリース判定で見つかった軽微な修正、バージョン番号、README、リリースノート、テスト証跡更新に限定する。新機能追加は次リリースへ回す。
- 本番候補は`vX.Y.Z`タグで固定し、Application Repositoryのアプリバージョンと一致させる。例: Gitタグ`v2.4.0` ↔ Application Repository `2.4.0`。
- タグを打った後に差し替えが必要になった場合、タグの上書きは避け、`v2.4.1`など新しいバージョンを作る。

#### 7.3.4 緊急修正・バックポート

- 緊急修正は最新本番タグから`hotfix/*`を切り、最小差分でPRを作成する。
- 本番反映後、同じ修正を必ず`main`へバックポートする。必要に応じて検証中の`release/*`や未完了の`feature/*`にも取り込み、次回リリースで修正が消えないようにする。
- 緊急修正で検証を短縮した場合でも、ReleaseOps Deployment Request、事後ATF/AutomatePro、本番後スモーク、振り返りを必須にする。

#### 7.3.5 資格情報と接続

ServiceNow Git連携ではリポジトリ資格情報がインスタンスの開発者間で共有されるため、個人PATではなく、ローテーション可能な最小権限資格情報とMID Server経由接続を検討する。

### 7.4 国外チーム（Dev5）

- GitHub Team、AEMC collaboration、ServiceNow roleをD社スコープに限定する。
- 本番資格情報・本番承認権限は付与せず、開発と本番リリースを分離する。
- テストデータの匿名化、個人情報・機密情報の持ち出し、アクセス時間帯、監査ログ保管、資格情報の管理主体を明文化する。
- PRレビューは国内責任者または指定CODEOWNERを必須にする。

### 7.5 ブランチ／タグによる先行リリース制御

同一アプリで要件Aと要件Bのリリース順が途中で入れ替わる可能性がある場合、GitHub運用では次のルールを標準にする。

- **短命featureブランチ:** `feature/REQ-A`、`feature/REQ-B`のように要件単位で作り、PRも要件単位にする。
- **リリース候補タグ:** 本番候補は`main`上のコミットへ`vX.Y.Z`タグを打ち、Application Repositoryの同一バージョンと対応させる。
- **先行リリース時のcherry-pick:** 要件Aが未承認で、要件Bだけを先に出す場合は、Bのコミットだけを`main`またはリリースブランチへcherry-pickし、B専用タグを作る。cherry-pick後はPRで差分とテスト結果を再レビューする。
- **revert優先:** すでにAが`main`へ入ってしまった後でBだけを出す必要が出た場合は、Aをrevertしたリリース候補を作る。ただし、アプリメタデータや削除差分が複雑な場合は、安易なrevertよりクリーンなブランチからBを再適用する。
- **Feature flag:** AとBが技術的に分離できない場合は、Aを無効化したままBを有効化できる設計を採用する。flagの初期値、切替権限、監査ログ、ロールバック条件をDeployment Requestに記録する。

この運用の目的は、検証環境の状態に引きずられず、いつでも「本番へ入れるコミット、アプリバージョン、Deployment Request」を一意に示せるようにすることである。
