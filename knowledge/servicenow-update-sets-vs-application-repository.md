---
title: "ServiceNow: Update SetsとApplication Repositoryの使い分け"
created: 2026-06-24
updated: 2026-06-24
type: knowledge
status: draft
tags:
  - servicenow
  - update-sets
  - application-repository
  - application-development
  - technical-governance
  - knowledge
aliases:
  - "Update Sets Vs Application Repository"
  - "Update SetsとApplication Repositoryの比較"
related:
  - "[[servicenow-app-repo-clone-development-mode]]"
  - "[[servicenow-plugin-update-governance]]"
  - "[[servicenow-skip-record-management]]"
---
# ServiceNow: Update SetsとApplication Repositoryの使い分け

## 目的

ServiceNowの技術ガバナンスでは、開発・変更内容をどの仕組みで移送/配布するかを事前に決めておく必要がある。

特に **System Update Sets** と **ServiceNow Application Repository** はどちらもインスタンス間で変更を動かすために使われるが、目的と運用単位が異なる。使い分けを誤ると、アプリケーションのバージョン管理、更新経路、ロールバック方針、Skipレコード対応、リリース証跡が複雑になる。

このKnowledgeでは、ServiceNow Community投稿「Update Sets Vs Application Repository」の内容をもとに、Update SetsとApplication Repositoryの利用判断を整理する。

## 用語の整理

### ServiceNow Application Repository

ServiceNow Application Repositoryは、開発・テスト済みの **Scoped Application** を自社の複数インスタンスへ配布するためのリポジトリである。

開発元インスタンスでアプリケーションを作成・検証した後、Application Repositoryへ公開することで、同一会社に属するインスタンスからそのアプリケーションをインストールまたは更新できる。

### System Update Sets

System Update Setsは、あるインスタンス上で行った設定変更をグループ化し、別インスタンスへ移送するための仕組みである。

管理者は複数の設定変更を名前付きのUpdate Setにまとめ、テスト環境や本番環境へ一括で移送・プレビュー・コミットできる。

## 結論

- **アプリケーションとして継続的に配布・更新するもの** は、原則として **Application Repository** を使う。
- **ベースシステムや既存インストール済みアプリへの個別設定変更、パッチ、単発の変更移送** は、原則として **Update Sets** を使う。
- **アプリケーションの初回インストール目的でUpdate Setsを使わない。** アプリケーションのインストールはApplication RepositoryまたはServiceNow Storeを使う。
- 同一スコープ/同一アプリに対して、Application Repository運用とUpdate Set運用を無計画に混在させない。

## Update Setsを使う場面

Update Setsは、アプリケーションそのものの配布というより、構成変更や差分変更をまとめて移送する用途に向いている。

### 適している用途

| 観点 | 内容 |
| --- | --- |
| ベースシステム変更 | ベースシステムへの設定変更を保存・移送する。 |
| インストール済みアプリへの変更 | 既にインストールされているアプリケーションへのパッチや変更を移送する。 |
| 特定バージョンの保全 | 必要に応じて、特定時点の変更内容をUpdate Setとして保存する。 |
| ファイル出力 | Update SetをXMLなどでエクスポートし、別経路で受け渡す。 |
| テスト/本番展開 | 一連の設定変更をテスト環境や本番環境へまとめて展開する。 |

### 注意点

- Update Setsは、アプリケーションのライフサイクル全体を管理する仕組みではない。
- アプリケーションの初回インストールには使わない。
- Application RepositoryやServiceNow StoreからインストールすべきアプリをUpdate Setで代替しない。
- Update Setでアプリの過去バージョン相当を保全することはできるが、標準的な配布・更新経路はApplication Repositoryに寄せる。
- Update Setのプレビュー、競合、Skipレコード、コミット順序はリリース手順として管理する。

## Application Repositoryを使う場面

Application Repositoryは、完成したScoped Applicationを社内インスタンスへ配布し、バージョンとして更新する用途に向いている。

### 適している用途

| 観点 | 内容 |
| --- | --- |
| アプリのインストール | 自社インスタンスへScoped Applicationをインストールする。 |
| アプリの更新 | 公開済みアプリケーションを会社内インスタンスへ更新配布する。 |
| バージョン管理 | アプリケーション単位でバージョンを管理する。 |
| アクセス制御 | 同一会社のインスタンスに限定してアプリを利用させる。 |
| 完成アプリの展開 | 開発・テスト済みのアプリをエンドユーザー利用環境へ展開する。 |

### 注意点

- Application Repositoryは、通常は最新の公開バージョンをインストール/更新する運用に向く。
- 過去バージョンを保持・復元したい場合は、ソースコントロール、アプリケーションバージョン、必要に応じたUpdate Setエクスポートなど、別途保全方針を決める。
- Team Developmentと併用する場合、アプリケーション公開は親インスタンスから行う。
- 社外のユーザーや他社へ共有したい場合は、Application RepositoryではなくServiceNow Storeへのアップロードを検討する。

## 判断基準

| 質問 | 推奨 |
| --- | --- |
| 新しいScoped Applicationを他インスタンスへインストールしたいか | Application Repository |
| 完成した社内アプリを複数インスタンスへ配布・更新したいか | Application Repository |
| ベースシステムの設定変更を移送したいか | Update Sets |
| 既にインストール済みのアプリへ小規模パッチを適用したいか | Update Sets |
| アプリケーションのバージョンとして管理したいか | Application Repository |
| 変更単位/リリース単位として一時的にまとめたいか | Update Sets |
| ServiceNow StoreアプリやApp Repoアプリを初回導入したいか | StoreまたはApplication Repository |
| Update Setでアプリケーションを丸ごと導入したいか | 原則避ける |

## 推奨運用パターン

### 1. カスタムScoped Applicationの標準配布

1. 開発インスタンスでScoped Applicationを開発する。
2. ATF、コードレビュー、権限確認、データモデル確認を行う。
3. アプリケーションバージョンを付与する。
4. Application Repositoryへ公開する。
5. テスト環境でApplication Repositoryからインストール/更新する。
6. 検証後、本番環境でもApplication Repositoryから同じアプリケーションバージョンを適用する。

### 2. 既存環境への設定変更/パッチ

1. 変更内容をUpdate Setに記録する。
2. Update SetをCompleteにする。
3. 対象環境で取得・プレビューする。
4. 競合、エラー、Skipレコードを確認する。
5. テスト環境でコミットし、回帰テストを実施する。
6. 本番環境へ同じ手順で適用する。

### 3. App Repo運用中アプリへの変更

Application Repositoryで配布しているアプリへ継続的な変更を行う場合は、原則として開発元でアプリを更新し、新しいバージョンとしてApplication Repositoryへ公開する。

緊急パッチとしてUpdate Setを使う場合は、以下を必ず記録する。

- なぜApplication Repositoryの通常リリースではなくUpdate Setで適用するのか。
- 後続のアプリケーションバージョンへ同じ修正を取り込む方法。
- Update Set適用済み環境と未適用環境の一覧。
- 次回Application Repository更新時に競合や上書きが発生しないか。

## よくあるアンチパターン

- 完成アプリの初回導入をUpdate Setで行う。
- 同じScoped Applicationを、ある環境ではApplication Repository、別環境ではUpdate Setで更新する。
- 本番だけ緊急Update Setを適用し、その修正を開発元アプリに戻さない。
- Update Setのコミット順序や依存関係を管理しない。
- Application Repositoryからインストールしたアプリを不用意に開発モードへ変換する。
- Team Development利用時に子インスタンスからApplication Repositoryへ公開する。

## ガバナンス観点のチェックリスト

- 対象変更は「アプリケーション単位」か「設定差分単位」か。
- 対象スコープの正規の配布経路はApplication Repository、Store、Update Setのどれか。
- 本番適用前にSub-productionで同じ経路・同じ順序で検証したか。
- アプリケーションバージョン、Update Set名、変更要求番号を紐付けたか。
- Skipレコード、Preview Problem、依存関係を確認したか。
- 緊急Update Setを使った場合、次回アプリケーションリリースへ修正を取り込む計画があるか。
- 過去バージョンや切り戻し方針を事前に決めているか。

## 参考ドキュメント

- `markdown/application-development/c_SharingApplications.md`
- `markdown/application-development/planning-applications.md`
- `markdown/application-development/application-repository-self-hosted/install-app-from-repo.md`
- `markdown/application-development/application-repository-self-hosted/t_PublishAppsToTheAppRepository.md`
- `markdown/application-development/management-options.md`
- `markdown/application-development/system-update-sets/`
- `markdown/application-development/releaseops/`

## Obsidianリンク

- [[servicenow-app-repo-clone-development-mode]]
- [[servicenow-plugin-update-governance]]
- [[servicenow-skip-record-management]]
