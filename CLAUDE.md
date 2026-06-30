# dddantic — Project Instructions

Pydantic をベースに、DDD の戦術的設計要素（Entity / ValueObject / AggregateRoot / DomainEvent ...）を
型付きの構成要素として提供するライブラリ。各要素に DDD の不変条件を強制し、定義されたモデル群を
解析してモデル図（Mermaid）やコンテキストマップを生成する。

この文書は**設計判断の記録**と**コードから復元できない意図**のみを扱う。ユーザ向けの使い方は
[README.md](README.md) を参照。

> ステータス: 設計初期。`src/dddantic/` は未実装。以下は確定済みの設計方針。

## 確定済みの設計判断

### Pydantic v1/v2 両対応

レガシー資産（v1 利用プロジェクト）でも導入できることを価値とする。v1/v2 の API 差
（`model_config`/`Config`、`model_fields`/`__fields__`、`frozen`/`allow_mutation` 等）は
**薄い互換シム `_compat.py` に閉じ込め**、本体ロジックは 1 本化する。`pydantic.VERSION` で分岐する。

対応 Python は 3.10〜3.14。CI は python × pydantic{v1,v2} のマトリクスで両系統を常時検証する
（`.github/workflows/ci.yml`）。ただし pydantic v1 は 3.13+ をサポートしないため、
v1 のレグは 3.12 までに限定する（3.13/3.14 は v2 のみ）。

### 制約違反はクラス定義時に raise

各要素の不変条件は `__init_subclass__` で検査し、違反したら**クラス定義時に即 `TypeError`**。
lint 的な遅延報告ではなく早期失敗を選ぶ。誤ったモデル定義をリポジトリに残させないため。

### ベースクラスを主、デコレーターを従

挙動・制約・IDE 補完はベースクラス（`ValueObject` 等）で提供する。`__init_subclass__` で
レジストリへ**暗黙登録**し、作図のために明示デコレーターを付けて回らせない。
`@bounded_context` のようなグルーピングのみデコレーターで補う。

### 関心の分離

「制約の強制」と「メタデータ収集・解析」は独立した関心として内部でも分離する。

```
building_blocks/  ValueObject, Entity, AggregateRoot, DomainEvent ...
constraints/      各要素の不変条件チェック（__init_subclass__ から呼ぶ）
registry/         要素の登録・問い合わせ
diagram/          mermaid 出力（将来 plantuml）
specification/    Specification とコンビネータ
_compat.py        pydantic v1/v2 差異の吸収（leaf module）
```

## 要素ごとの制約（実装方針）

- **ValueObject**: 不変・値等価・hashable（v2 `frozen=True` / v1 `allow_mutation=False`）。識別子フィールド禁止。
- **Entity**: `id` フィールド必須。等価性・ハッシュは id のみ（値ではなく同一性）。
- **AggregateRoot**: 集約境界。他集約への参照は ID のみ（他 Entity 型フィールドを持てない）。ドメインイベントを蓄積。
- **DomainEvent**: 不変 + `occurred_on`。VO 的に扱う。
- **Repository**: 型パラメータが AggregateRoot 派生であることを制約。AggregateRoot のみを対象とする。
- **Specification**: `is_satisfied_by` + `&` / `|` / `~` で合成可能に。

## コーディング原則（プロジェクト固有）

ツールで強制できない・グローバル規約を上書きする項目のみ記載。ruff / pyrefly の設定は `pyproject.toml` を参照。

- **`Any` 禁止**: `object` または Protocol を使う。
- **`# noqa` / `type: ignore` は最終手段**: 警告は設計で解決する。使う場合は PR で理由を明記。
- v1/v2 の分岐は `_compat.py` 以外に漏らさない。本体に `pydantic.VERSION` を直接書かない。

## Git / リリース

- Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- main への直接 push 禁止。
- SemVer: v1.0.0 未満は `feat:` → minor, `fix:` → patch。
- リリースは Release Please + PyPI Trusted Publisher で自動化（`.github/workflows/release.yml`）。
