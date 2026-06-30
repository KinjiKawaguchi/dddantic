# dddantic

> ⚠️ 開発初期（alpha）。API は未確定です。

Pydantic をベースに、DDD（ドメイン駆動設計）の戦術的設計要素を**型付きの構成要素**として提供する
ライブラリです。各要素に DDD の不変条件を強制し、定義したモデル群を解析して
**モデル図（Mermaid）やコンテキストマップを生成**します。

## 何ができるか

- **DDD 要素のベースモデル** — `Entity` / `ValueObject` / `AggregateRoot` / `DomainEvent` などを
  Pydantic モデルとして提供。
- **不変条件の強制** — Value Object は不変・値等価、Entity は同一性ベースの等価、集約は他集約を
  ID でしか参照できない、といった DDD の制約をクラス定義時に検査します。
- **解析と作図** — 定義された要素を内省し、包含・参照関係を Mermaid のクラス図として出力します。
- **Pydantic v1 / v2 両対応** — 既存資産のバージョンに合わせて導入できます。

## インストール

```bash
pip install dddantic   # 公開後
```

## イメージ（予定 API）

```python
from dddantic import ValueObject, Entity, AggregateRoot

class Money(ValueObject):
    amount: int
    currency: str          # 不変・値等価。識別子は持てない

class OrderId(ValueObject):
    value: str

class Order(AggregateRoot):
    id: OrderId            # 同一性で等価
    total: Money           # 集約は VO / 子 Entity を包含し、他集約は ID でのみ参照
```

詳細な設計方針は [CLAUDE.md](CLAUDE.md) を参照してください。

## 開発

```bash
uv sync
uv run pytest
uv run ruff check src/ tests/
uv run pyrefly check src/
```

## ライセンス

MIT
