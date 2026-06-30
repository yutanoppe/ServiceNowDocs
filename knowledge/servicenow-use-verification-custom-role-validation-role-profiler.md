---
title: "ServiceNow: Use VerificationのCustom Role ValidationとRole Profiler"
created: 2026-06-25
updated: 2026-06-25
type: knowledge
status: draft
tags:
  - servicenow
  - use-verification
  - subscription-management
  - role-profiler
  - custom-role
  - acl
  - license-management
  - knowledge
aliases:
  - "KB1637906"
  - "Understanding Custom Role Validation - Use Verification"
  - "Custom Role Validation"
  - "Role Profiler"
related:
  - "[[servicenow-subscription-mapping-custom-apps-tables]]"
---
# ServiceNow: Use VerificationのCustom Role ValidationとRole Profiler

## メタ情報

- KB番号: KB1637906
- 原題: Understanding Custom Role Validation - Use Verification
- 最終更新日: 2026-04-07
- 対象: Internal, Customer
- 主題: Use Verificationにおけるカスタムロール検証とRole Profilerによるライセンス分類

## 目的

Use Verificationでは、顧客インスタンス上のカスタムロールを検出・分類するために **Role Profiler** を利用する。Role Profilerは、カスタムロールに紐づくACLを分析し、そのロールがどの利用者タイプ・ライセンス分類に該当するかを判定する。

このKnowledgeでは、KB1637906の内容をもとに、Role Profilerの考え方、ロール分類基準、想定外の利用数増加時の確認観点、Role Profiler Insightsの解消方法を整理する。

## 要点

- カスタムロールは、標準ロールでは提供できない個別のアクセス権を実現するために顧客が作成するロールである。
- Role Profilerは、カスタムロールに含まれるACLを分析して、ロールをRequester、Business Stakeholder、Approver、Fulfillerなどに分類する。
- 分類は、ACLがどのテーブルに対して、どの範囲の読み取り・書き込み・承認権限を与えているかで決まる。
- タスク拡張テーブルと非タスク拡張テーブルでは、同じ `read all` でもライセンス分類の扱いが異なる場合がある。
- Role Profilerによって利用数が想定外に増えた場合は、対象ロール、ACL、割り当てユーザー/グループ、分類根拠を確認する。
- ACLやロール割り当てが意図通りで、分類も妥当な場合は実利用とみなし、必要に応じて追加ライセンス購入で是正する。
- ACL設定やロール割り当てが誤っている場合は、設定修正によって利用数・コンプライアンス状態を是正する。
- Role Profilerが検出するInsightsには、セキュリティ上の問題とライセンス権利上の問題が含まれる。

## カスタムロールの基本

### 定義

カスタムロールとは、顧客が作成し、標準ロールでは提供されない特定レベルのアクセス権を付与するために設定されたロールである。

### 仕組み

カスタムロールは、ServiceNowインスタンス内の特定テーブルに対してACLを設定することで、指定ユーザーに個別のアクセス権を与える。

### ライセンス上の影響

カスタムロールは、どの程度のアクセス権を与えるかによって必要なライセンスが変わる。そのため、Use Verificationではカスタムロールを追加分析し、Requester、Business Stakeholder、Approver、Fulfillerなどの分類を判断する。

## Role Profilerを利用する利点

| 利点 | 内容 |
| --- | --- |
| 速度 | カスタムロール監査を大幅に高速化できる。 |
| 正確性 | より客観的で顧客に説明しやすいデータを提供できる。 |
| 網羅性 | 利用数に反映すべきカスタムロールを広く捕捉できる。 |
| 自動化 | Use Verificationアナリストによる手作業の接点を削減できる。 |

## Role Profilerの分類ロジック

Role Profilerは、カスタムロールのユーザータイプを、ロールに含まれるACLに基づいて分類する。ACLは、サブスクリプション製品に含まれるアプリケーションやテーブルに対して、特定レベルのアクセス権を付与するために使われる。

### 基本的な流れ

1. カスタムロールをプロファイルする。
2. カスタマイズされたACLからロールタイプを識別する。
3. ロールプロファイルにはPIIを含めない。
4. 検出されたロールタイプを使ってユーザー数をカウントする。
5. ユーザー数のカウントは、既存のUse Verificationプロセスに従う。

### ACL分析で見る観点

Role ProfilerはACLをスキャンし、ACLが付与するアクセスレベルを判断するために複数の属性を分析する。KB本文では属性の詳細表が画像/表として示されているが、実務上は少なくとも次の観点を確認する。

- 対象テーブルがタスク拡張テーブルか、非タスク拡張テーブルか。
- 読み取り権限が自分のレコードだけか、全レコードまたは他者のレコードにも及ぶか。
- 書き込み権限が自分のレコードだけか、任意のレコードにも及ぶか。
- 承認権限が自分に関係する承認だけか、広範な承認に及ぶか。
- ACLにロール条件があるか、`snc_internal`、`public`、またはロールなしで広範囲に適用されていないか。
- ACLの条件・スクリプトがRequester相当の範囲に制限しているか。

## 基本ロールタイプの考え方

### タスク拡張テーブルの場合

タスク拡張テーブルには、OOTBテーブルとカスタムテーブルの両方が含まれる。タスク拡張テーブルでは、カスタムロールの分類は概ね次のように判断される。

| 分類 | 権限の例 | 考え方 |
| --- | --- | --- |
| Requester | 自分のレコードを読み取り/書き込みできる | 自分の依頼や関連レコードのみを扱うためRequesterライセンス相当。 |
| Business Stakeholder | 全レコードまたは自分以外のレコードを読み取りできる、または広範に承認できる | 自分以外のデータを閲覧・承認できるためBusiness Stakeholder相当。 |
| Fulfiller | 任意のレコードを書き込みできる | 自分以外の作業・処理対象を更新できるためFulfiller相当。 |

### 非タスク拡張テーブルの場合

非タスク拡張テーブルには、参照・ルックアップ用途のテーブルなどが含まれる。この用途では、Business Stakeholder分類は一般的ではない。

| 分類 | 権限の例 | 考え方 |
| --- | --- | --- |
| Requester | 自分のレコードを読み取り/書き込みできる、または全レコードを読み取りできる | 参照値の検索など、Requesterが広い読み取りを必要とする場合がある。 |
| Fulfiller | 任意のレコードを書き込みできる | 自分以外のデータを更新できるためFulfiller相当。 |

## Requester ACLの例で見る注意点

### Internal User向けRequester

内部ユーザーに割り当てるRequesterロールでは、ユーザークラスがUserである前提で、自分の依頼・自分に関連するレコードに読み取り/書き込み範囲を制限する必要がある。

### External User向けRequester/External User

Customer Service Managementなど一部製品では、外部ユーザーに対する除外・別扱いが含まれる場合がある。外部ユーザー向けのロールは、ContactやConsumerなどの外部ユーザークラスに限定して提供されていることが重要である。

外部ユーザーは、顧客ポータル経由で自分または関連アカウントのリクエストを作成・表示・変更・承認したり、新規連絡先作成を承認したり、自分または関連アカウントのユーザー/資産を管理できる場合がある。ただし、この扱いは対象製品の契約・製品説明に依存する。

## Role Profilerの結果を調査する観点

Role Profilerスキャンによって製品利用数が大きく増えた、または想定外に増えた場合、Use VerificationはSalesに対し、超過の原因となっている具体的なロールとACLを提示できる。

顧客との確認では、次の質問を使う。

1. ACLは意図通りに作られているか。
2. 意図したグループ/ユーザーにだけ、このロールが割り当てられているか。
3. Role Profilerのロール分類が誤っていると考える場合、その理由は何か。

### 判断パターン

| 状況 | 判断 | 対応 |
| --- | --- | --- |
| ACLが意図通りで、ロール割り当ても正しく、分類も妥当 | 真の利用とみなす | ライセンス超過があれば追加購入などで是正する。 |
| ACLが意図通りでない | 設定不備 | ACL条件、ロール条件、スクリプトなどを修正して利用数を是正する。 |
| ロール割り当てが意図通りでない | 運用/割り当て不備 | グループ・ユーザーへのロール付与を見直す。 |
| 顧客が分類誤りを主張し、根拠がある | 要追加調査 | Use Verification、Sales、顧客で調査し、誤りなら例外登録・分類更新を行う。 |

## Role Profiler Insightsへの対応

Insightsは、Role Profilerが検出するロール、ACL、無効なカスタムテーブルマッピングに関する問題である。検出されたInsightsは顧客側で対応する必要がある。

### Insight別の説明と解消方法

| Insight名 | 説明 | 解消方法 |
| --- | --- | --- |
| `snc_internal` Fulfillers | 一部テーブルで`snc_internal`ロールがFulfillerとして検出された状態。全内部ユーザーにFulfiller権利が必要になる可能性があり、セキュリティ上の問題にもなりやすい。 | ACLに追加条件を入れてRequester相当に制限する、または`snc_internal`ではなく適切な限定ロールをACLに設定する。 |
| Public Fulfillers | 一部テーブルで`public`ロールがFulfillerとして検出された状態。未ログインユーザーにFulfiller権利が必要になる可能性があり、セキュリティ上の問題にもなりやすい。 | 対象ACLから`public`ロールを削除する。 |
| Fulfillers on Unmapped tables | Fulfillerアクセスのあるカスタムテーブルがサブスクリプションにマッピングされていない状態。 | Custom Table Inventory（`ua_custom_table_inventory`）上で、対象カスタムテーブルをカスタムテーブル権利を含む有効なサブスクリプションへマッピングする。 |
| Tables mapped to sub w/ no tables | カスタムテーブル権利を持たないサブスクリプションにテーブルがマッピングされている状態。 | カスタムテーブル権利を含む別のサブスクリプションへ再マッピングする。 |
| Tables over subscribed | サブスクリプションに含まれるカスタムテーブル数を超えてテーブルがマッピングされている状態。 | 十分なカスタムテーブル権利数を持つサブスクリプションへ再マッピングする。 |
| `All Users` are Fulfillers | ロール条件のないACLが全ユーザーに適用され、一部テーブルでFulfillerとして検出された状態。全内部ユーザーにFulfiller権利が必要になる可能性があり、セキュリティ上の問題にもなりやすい。 | ACLに追加条件を入れてRequester相当に制限する、またはACLに適切なロール条件を追加して全ユーザーへ適用されないようにする。 |

## 実務チェックリスト

### Role Profiler結果を受け取ったとき

- [ ] 対象ロール名を確認した。
- [ ] 対象ACLと対象テーブルを確認した。
- [ ] 対象テーブルがタスク拡張テーブルか非タスク拡張テーブルかを確認した。
- [ ] ACLが読み取り、書き込み、承認のどの権限を付与しているか確認した。
- [ ] 権限範囲が「自分のレコードのみ」か「全レコード/任意レコード」か確認した。
- [ ] ACLに`snc_internal`、`public`、ロールなしの広範適用がないか確認した。
- [ ] ロールが意図したユーザー/グループにだけ割り当てられているか確認した。
- [ ] 外部ユーザー向けロールの場合、User Classや利用チャネルが契約上の外部ユーザー条件に合っているか確認した。
- [ ] カスタムテーブルが適切なサブスクリプションへマッピングされているか確認した。

### 是正方針を決めるとき

- [ ] ACLとロール割り当てが意図通りなら、真の利用としてライセンス対応を検討する。
- [ ] ACLが過剰に広い場合は、条件・スクリプト・ロール条件を修正する。
- [ ] ロール割り当てが過剰な場合は、グループ設計・ユーザー割り当てを修正する。
- [ ] カスタムテーブルマッピングが不正な場合は、Subscription Management/Custom Table Inventoryで修正する。
- [ ] Role Profiler分類に異議がある場合は、根拠となるACL条件、利用目的、ユーザー範囲、契約条件を整理してSales/Use Verificationへ連携する。

## 顧客説明用の短い表現

Role Profilerは、カスタムロールそのものの名称ではなく、そのロールに紐づくACLが実際にどの範囲のデータアクセスを許可しているかを見て分類します。自分のレコードだけを扱う権限であればRequester相当ですが、自分以外のレコードを広く読み取る、承認する、または任意レコードを書き込める場合は、Business StakeholderやFulfillerとして分類される可能性があります。

想定外にFulfiller利用が増えた場合は、まずACLが意図通りか、ロールが適切なユーザー/グループにだけ割り当てられているか、カスタムテーブルが正しいサブスクリプションへマッピングされているかを確認します。設定が意図通りで分類も妥当であれば実利用として扱い、設定ミスであればACLやロール割り当てを修正します。

## 参考情報

- ServiceNow KB1637906: Understanding Custom Role Validation - Use Verification
- ServiceNow KB0864132: Use Verificationの既存ユーザーカウントプロセス（KB本文で参照）

## Obsidianリンク

- [[servicenow-subscription-mapping-custom-apps-tables]]
