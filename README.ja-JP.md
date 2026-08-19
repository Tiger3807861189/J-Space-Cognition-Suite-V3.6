# J-Space Cognition Suite V3.6

[English](README.md) | [简体中文](README.zh-CN.md)

[![DOI](https://zenodo.org/badge/1308234922.svg)](https://zenodo.org/badge/latestdoi/1308234922)

J-Space Cognition Suite は、深い推論、長期的な作業、ツール利用、検証、リカバリーを対象とした、モデル非依存の推論時制御システムです。

クロスプラットフォームでの利用、選択的な読み込み、摩擦の少ない統合を実現するため、Skill として提供されています。

本スイートは、エージェントがアクセスできる作業表現を、意図的に管理されたワークスペースとして組織します。単一のエントリ、選択的に読み込まれる 9 個のモジュール、3 つの補助リファレンス、そして長期タスクの状態を保持するためのオプションの標準ライブラリ製コントローラーによって動作します。

J-Space は推論時に動作します。モデルの重みと学習には変更を加えません。

## クイックスタート

### 方法 A — 手動インストール

1. 本リポジトリをダウンロードまたはクローンします。
2. 利用中の AI ホストが使用するユーザーレベルの Skills ディレクトリを特定します。
3. [`j-space/`](j-space/) ディレクトリ全体をそこへコピーし、インストール後のエントリが `<skills-directory>/j-space/SKILL.md` となるようにします。
4. 利用可能な Python 3 インタープリターで整合性チェックを実行します。

   ```text
   <python-command> <skills-directory>/j-space/scripts/verify_suite.py
   ```

   `<python-command>` は、ホストで利用できる Python 3 コマンド（一般的には `python`、`python3`、`py -3`）に置き換えてください。

5. ホストが起動時に Skills を検出する仕様であれば、ホストを再読み込みします。

- `SKILL.md` は `modules/`、`references/`、`scripts/` 配下への相対パスを参照するため、ディレクトリ構成はそのまま保つ必要があります。


- リポジトリ直下の `LICENSE` と `THIRD_PARTY_NOTICES.md` も配布物の一部です。
- `j-space/` を単独パッケージとして再配布する場合は、両方のコピーを同梱してください。

### 方法 B — AI エージェントにインストールを依頼する

ファイルと本リポジトリにアクセスできるエージェントに、次のプロンプトをそのまま渡します。

```text
Install J-Space Cognition Suite from
https://github.com/Tiger3807861189/J-Space-Cognition-Suite-V3.6 into this environment's user-level Skills directory.

First inspect the host configuration or documentation to locate the correct Skills directory. Install the complete j-space/ directory as j-space/, preserving SKILL.md, modules/, references/, and scripts/. If a j-space target already exists, compare it and ask before replacing anything. Run scripts/verify_suite.py with an available Python 3 interpreter after installation.

When finished, report the installed path and verification result, then tell me how this host invokes the Skill. Briefly explain fast, full, and loop, and explain that the optional controller records long-task state rather than choosing solutions. If this host has no native Skill loader, explain the selective system/developer-instruction integration instead of reporting an installation.
```

### 使い方

Skill ピッカー、`/j-space`、`$j-space`、あるいは直接の依頼など、ホストが提供する手段で Skill を呼び出します。

```text
Use j-space for this task. Audit this repository, preserve its architecture,
verify every finding, and keep the work consistent across all affected files.
```

エントリのゲートが、適切かつ最も軽量な pass を自動的に選択します。

## 動作モード

| Pass | 適した作業 | 読み込まれるもの |
|---|---|---|
| `fast` | 単一ステップ、または一目で確認できる結果 | 追加の読み込みなし |
| `full` | 相互に依存する複数のステップと、範囲の定まった 1 つの成果物 | 関連するモジュールを 1〜2 個。納品前に `ship` |
| `loop` | 複数の段階、ファイル、ターン、ツール、または永続的な状態 | 台帳、シーム、チェックポイント、レジスター監査、リカバリー |

簡潔さを求める指示は外側の回答の長さを変えるだけで、検証はタスクが要求する水準を維持します。短い作業は軽いまま、長い作業には必要なときにだけ永続的な状態が与えられます。

## 中核メカニズム

| メカニズム | 機能 |
|---|---|
| 選択的ワークスペース読み込み | 支えとなる考えを 1〜2 個だけ活性状態に保ち、残りは外部化する |
| ブロードキャストハブ | 依存する各分岐に対し、名称・値・制約・スタイルの基準を共有する単一の情報源を与える |
| Dense Track | 長い内部の連鎖を圧縮された復号可能な記法で運び、その後クリーンな外部言語へ戻る |
| 結論の前に橋を架ける推論 | 結論がそれを消費する前に、必要な中間結果を明示する |
| メタ認知制御 | 確信度・不整合・失敗のシグナルを、具体的な次の行動へ振り分ける |
| 経験的エスケープと検証 | 行き詰まった導出を、検証者と網羅範囲を明示した範囲限定のテストへ変換する |
| 一人称の主体性と機能的エコー | `I`、`we`、`let's`、`we need` を用いて、ワークスペースの状態を後続の行動とチェックに結び付ける |

これらのメカニズムは選択的に読み込まれます。すべてのリクエストで実行する固定のチェックリストではありません。

## オプションのコントローラー

[`j-space/scripts/jspace.py`](j-space/scripts/jspace.py) は `loop` の状態を、現在のタスクワークスペース内の
`.jspace/` へ外部化します。タスクワークスペースをカレントディレクトリに保ったまま、Skill 上で解決されたパスから呼び出してください。

| コマンド | 目的 |
|---|---|
| `note --goal "..." --next "..."` | 台帳を開き、完了条件と最初の行動を定義する |
| `note --next "..."` | チェックポイントまたはシームの後に、唯一の次の行動を置き換える |
| `note --core "..."` | ハブの項目を記録する |
| `note --core "..." --core-slot 1` | 選択したライブなハブ項目を入れ替える |
| `note --check "..." --by "..."` | 検証者と網羅範囲を伴うチェックポイントを追記する |
| `note --open "..." --settled-by "..."` | 未解決の問いと、それを解決する条件を記録する |
| `note --close N --check "..." --by "..."` | 新たに記録したチェックポイントによって問い `N` をクローズする |
| `seam` | 現在の状態を読み直し、直近の変化を報告する |
| `ship FILE` | 出力テキストにレジスターの漏れや失敗の兆候がないか検査する |
| `resume` | 長い中断の後に、前提・不変条件・台帳全体を再読み込みする |

```text
<python-command> <skill-root>/scripts/jspace.py note --goal "what done means" --next "first action"
<python-command> <skill-root>/scripts/jspace.py note --close 1 --check "what now holds" --by "verifier and coverage"
<python-command> <skill-root>/scripts/jspace.py seam
<python-command> <skill-root>/scripts/jspace.py ship OUTPUT_FILE
<python-command> <skill-root>/scripts/jspace.py resume
```

コントローラーは状態の記録と報告を担当します。解法の選択はモデル側に残ります。Python 標準ライブラリのみを使用し、作業状態はタスクの `.jspace/` ディレクトリ配下にのみ書き込みます。

## 一般的なモデルへの統合

ネイティブの Skill ローダーを備えた環境では、`j-space/` をそのままインストールできます。チャットや API の環境では、[`j-space/SKILL.md`](j-space/SKILL.md) を system または developer レベルの指示として与え、`modules/` と `references/` をファイルツールまたは検索ツール経由で参照できるようにしてください。

必要なファイルはオンデマンドで取得すべきです。選択的な読み込みは、運用設計そのものの一部です。

## ベンチマーク

すべての数値は対応するベンチマークのネイティブスコアで、値が高いほど良好です。`—` は結果が報告されていないことを示します。HLE はツールなしとツールありの条件に分けています。

### 評価コンテキスト

DeepSeek 上での J-Space の評価は、公式の DeepSeek Harness の minimal モード設定を参照し、reasoning effort を `max`、`temperature = 1.0`、`top_p = 0.95` として構成しました。J-Space は、ワークスペースのルーティング、状態の連続性、
検証、リカバリーを通じて推論時のワークフロー全体に関与しています。

結果はプロジェクトで利用可能な評価環境の中で収集されました。ハードウェア条件、プロセス分離、ツールの可用性、情報アクセスの境界も、そのコンテキストの一部です。J-Space は主体性と目標志向の探索を促す傾向があるため、アクセス可能な成果物や実行トレースが観測結果に関係します。

この表は、上記の条件下でのプロジェクトレベルのベンチマーク記録を示しています。比較対象の数値は各提供者が公開した評価コンテキストをそのまま保持しており、環境や Harness の構成によってスコアが変動することは想定内です。出典となる記録には、[DeepSeek V4-Flash-0731 モデルカード](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731)、[Z.ai](https://z.ai/) による GLM-5.3 のリリース評価記録、[Kimi-K3 モデルカード](https://huggingface.co/moonshotai/Kimi-K3)、および Anthropic の [Claude Fable 5 & Claude Mythos 5 システムカード](https://www-cdn.anthropic.com/2f9323abbcc4abe219577539efe19a623c9ca2bd/Claude%20Fable%205%20%26%20Claude%20Mythos%205%20System%20Card.pdf)（同カードは比較対象の条件も報告しています）が含まれます。

### モデル比較

| ベンチマーク | DeepSeek V4-Flash-0731 | DeepSeek V4-Flash-0731 + J-Space V3.6 | GLM-5.3 | Kimi-K3 | Opus-4.8 | Fable 5（fallback あり） |
|---|---:|---:|---:|---:|---:|---:|
| HLE（ツールなし） | 37.8 | 45.5 | — | 43.5 | 49.8 | 53.3 |
| HLE（ツールあり） | 51.5 | 60.6 | 62.5 | 56.0 | 57.9 | 63.0 |
| Terminal Bench 2.1 | 82.7 | 87.1 | 88.2 | 88.3 | 85.0 | 88.0 |
| NL2Repo | 54.2 | 70.2 | 58.0 | 58.0 | 69.7 | — |
| CyberGym | 76.7 | 81.7 | 84.5 | 80.0 | 78.3 | 83.1 |
| DeepSWE | 54.4 | 67.4 | 66.9 | 67.5 | 58.0 | 70.0 |
| Toolathlon-Verified | 70.3 | 77.7 | 73.0 | 76.5 | 76.2 | 77.9 |
| Agents' Last Exam | 25.2 | 30.1 | 28.5 | 27.6 | 25.7 | 23.8 |
| AutomationBench（Public） | 25.1 | 31.7 | 48.2 | 30.8 | 27.2 | 29.1 |

### 効率

以下のタスクレベルの指標は、同一のタスク条件・モデル条件を保ち、それぞれ 1 回の評価実行を記録したものです。Control は対応するベースライン、J-Space はスイートを併用した条件です。速度はベンチマークスコアを経過時間で割った値で、高いほど良好です。トークンコストは消費トークン数をベンチマークスコアで割った値で、低いほど良好です。経過時間とトークン数には、両条件で固定かつ共通のスケーリング係数を用いています。この係数は表示上のスケールに影響しますが、指標内での改善比率は比較可能なままです。

| 指標 | Control | J-Space | 改善 |
|---|---:|---:|---:|
| 速度（スコア/時間、高いほど良い） | 0.43 | 1.09 | 2.53× |
| トークンコスト（トークン/スコア、低いほど良い） | 2.63 | 1.19 | 2.21× |

関連する評価資料：
[DeepSeek V4 × J-Space Capability Realization Report](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report)。

## モデル横断の互換性

これらの動作上の効果は、DeepSeek、Qwen、GLM、GPT、Claude の各モデルファミリーで再現されています。効果の大きさは、ベースとなる能力、コンテキストポリシー、ツール Harness、サンプリング設定、ベンチマーク実装によって変わります。

移植可能な単位はプロトコル、すなわちワークスペースの読み込み、選択的ルーティング、状態の外部化、検証、リカバリーです。これは特定ベンダーのトークナイザーやモデル API に依存しません。

## プロジェクト構成

```text
J-Space-Cognition-Suite-V3.6/
├── .github/workflows/verify.yml    # 3 プラットフォームでの整合性・回帰チェック
├── CITATION.cff                    # 機械可読な引用メタデータ
├── CONTRIBUTING.md                 # コントリビューションと出所に関する要件
├── LICENSE                         # Apache License 2.0
├── README.md                       # 英語版エンジニアリングガイド
├── README.zh-CN.md                 # 中国語版エンジニアリングガイド
├── README.ja-JP.md                 # 日本語版エンジニアリングガイド
├── THIRD_PARTY_NOTICES.md          # 出典資料の帰属とライセンス境界
├── tests/test_jspace.py            # 標準ライブラリ製コントローラーの回帰テスト
└── j-space/
    ├── SKILL.md                    # 単一のエントリ、ゲート、ルーティング、不変条件
    ├── modules/                    # 選択的に読み込まれる 9 個のプロトコル
    ├── references/                 # エビデンス、誘導手法、実例
    └── scripts/
        ├── jspace.py               # オプションの loop コントローラー
        ├── workspace-ledger.md     # 台帳のテンプレートと契約
        └── verify_suite.py         # オーサリング時の整合性チェック
```

登録されるエントリは `SKILL.md` のみです。モジュールとリファレンスはオンデマンドで読み込まれるため、この制御システム自体がコンテキスト圧迫の原因になりません。

メンテナーはパッケージのルートから検証できます。

```text
<python-command> j-space/scripts/verify_suite.py
<python-command> -m unittest discover -s tests -v
```

## 技術的な基盤と適用範囲

J-Space は、Anthropic の関連する解釈可能性研究によって確立された、運用上のワークスペース用語を採用しています。本スイートにおいて一人称の言語は制御文法として扱われます。すなわち、アクセス可能な状態の記述が、明示的な行動・チェック・決着に結び付けられます。

本スイートは、報告可能性、意図的な保持、中間計算、ブロードキャスト、モニタリング、因果的感受性といった観察可能な機能的特性に焦点を当てています。研究上の詳細な解釈、用語、エビデンスの境界、出典は
[`j-space/references/j-space-science.md`](j-space/references/j-space-science.md) で管理されています。

設計原則：

> **内部は密に、必要に応じて復号可能に、外部はクリーンに。**

タスクが必要とする分の仕組みだけを使ってください。

## リリース履歴

J-Space は次のように進化してきました。

**V1 → V1.5 → V1.8 → V2 → V2.5 → V2.6 → V3 → V3.1 → V3.2 → V3.5 → V3.5Turbo → V3.6**

V3.6 パッケージは、1 つのエントリ、9 個の焦点を絞ったモジュール、3 つの補助リファレンス、オプションのランタイムコントローラー、オーサリング時の検証ツール、標準ライブラリによる回帰テスト、3 プラットフォームの CI、Apache-2.0 ライセンス、機械可読な引用メタデータを含みます。

## ライセンス

J-Space Cognition Suite は [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) の下で公開されています。同ライセンスは、その表示および特許条項に従うことを条件に、使用、改変、再配布、商用統合を許可します。完全な条項は [`LICENSE`](LICENSE) を参照してください。引用または要約された外部の資料は引き続きその出典元の条項に従い、[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) に明示されています。ランタイムの `j-space/` ディレクトリのみを再配布する場合は、ルートにあるこれら 2 つのファイルも併せて配布してください。
