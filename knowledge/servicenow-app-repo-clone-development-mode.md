# ServiceNow: Application Repositoryアプリがクローン後に開発者モードになる場合の整理

## 事象

本番環境からPoC/開発などの非本番環境へシステムクローンした後、本番環境ではApplication Repositoryからインストール済みだった自社所有アプリが、クローン先では開発者モード（Studioなどで開発可能な状態）に見えることがある。

## 結論

これは、クローン先インスタンスに同一アプリの開発版が存在していた場合のServiceNowの想定動作として扱う。ServiceNowのドキュメントでは、システムクローンは開発中アプリやカスタマイズのバージョン差分を保持せず、クローン元にインストールされているアプリ/カスタマイズのバージョンだけをクローン先へコピーすると説明されている。また、クローン先に同一アプリの開発版があった場合、クローン後のアプリはクローン元にインストールされていたバージョンになるが、編集可能な状態になる。

そのため、PoC環境で「Application Repositoryからインストールされた状態のまま」にしたい場合は、クローン前またはクローン後に、対象アプリをApplication Repositoryモード（インストール済みアプリとして更新を受ける状態）に戻す必要がある。

## 主な原因

- クローン先（PoC）に、同じアプリがCustom Applications（`sys_app`）の開発版として存在していた。
- システムクローンは、開発版とインストール版の状態差分をそのまま保持するための機能ではない。
- クローン元（本番）にインストールされているアプリバージョンはコピーされるが、クローン先に同一アプリの開発版があった場合は編集可能な状態として残る。
- 逆方向の変換として、ServiceNowには「Installed」タブのアプリを「Convert to Development Mode」で開発モードに変換する機能がある。この変換後は、そのインスタンスではApplication Repositoryから更新を受けられなくなる。

## Application Repositoryからインストールされた状態のままにする対応

### 推奨対応

1. クローン前にPoC環境で対象アプリの状態を確認する。
   - **System Applications > My Company Applications > In Development** に対象アプリがある場合、開発版（`sys_app`）として存在している。
   - **Installed** に対象アプリがある場合、Application Repositoryからインストールされた状態（`sys_store_app`側）として扱われる。
2. クローン後もApplication Repositoryで更新したい対象アプリは、開発版のままにしない。
3. 必要に応じて、PoC環境で対象アプリを **Convert to Application Repository Mode** でApplication Repositoryモードへ変換する。
4. 変換後、**System Applications > My Company Applications** からApplication Repository上のアプリをインストール/更新する。

### クローン前にPoC側の開発中差分を残したい場合

ServiceNowの推奨に従い、クローン前にPoC環境の開発版を保全する。

- ソースコントロールにリンク済みの場合は、最新差分をコミットする。
- ソースコントロールを使っていない場合は、アプリをUpdate SetへPublish/Exportする。
- クローン後、必要に応じてリモート変更の適用またはUpdate Setのロードで復元する。

ただし、Application Repository運用とUpdate Set運用は混在させない。Application Repositoryからインストールしたアプリは、以降もApplication Repositoryで開発・公開・更新する運用に統一する。

## 確認ポイント

- PoC環境で対象アプリが **Installed** ではなく **In Development** に表示されていないか。
- 対象アプリのレコードが `sys_app` にあるか、`sys_store_app` にあるか。
- 過去にPoC環境で **Convert to Development Mode** を実行していないか。
- そのアプリが自社所有アプリか。ServiceNow Storeなど他社/他組織所有アプリは通常、同じようには開発モード化できない。
- Application Repositoryの更新を継続したい環境で、Update Setによる同一スコープの移送を行っていないか。

## 参考ドキュメント

- `markdown/application-development/application-repository-self-hosted/preserve-applications-during-clone.md`
- `markdown/application-development/application-repository-self-hosted/convert-installed-applications-to-development-mode.md`
- `markdown/application-development/application-repository-self-hosted/convert-custom-app-to-update-app-repo.md`
- `markdown/application-development/application-repository-self-hosted/manage-apps.md`
