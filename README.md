# Autonomous Game Factory

Godot + Python で、**企画 → バリエーション生成 → ゲーム実装 → QA → 実行/ビルド → ストア素材 → マーケティング素材 → 販売データ学習**までを一つにしたゲーム量産基盤です。

> `publish` 系は **dry-run / 明示ゲートが既定**です。Steam / itch.io の契約、審査、価格確定、支払い設定、最終公開を勝手に実行しません。

## Core pipeline

- GameSpecを大量生成（決定論的generator / 外部LLMのどちらも可）
- `survivor` / `dodger` / `collector` のプレイ可能なGodot 4ゲームへ変換
- fingerprintで企画重複を抑制
- 自動rankingで上位候補だけ実装
- Python QA + Godot headless smoke test
- Windows / Linux / Web export
- Steam / itch.io release pack生成
- Store copy / SNS / trailer shot list / asset manifest生成
- Wishlist / conversion / review / playtime / refund から次回企画配分を学習
- 許可リストのOSSをcloneし、commit/licenseを `vendor.lock.json` に固定

## Start

```bash
python -m game_factory.cli batch --count 12 --keep 3 --seed 42 --out generated
python -m game_factory.cli qa generated/<slug>
python -m game_factory.cli run generated/<slug>
python -m game_factory.cli build generated/<slug> --targets windows linux web
python -m game_factory.cli pack generated/<slug> --itch-target yourname/<slug>
```

OSSスターター:

```bash
python -m game_factory.cli vendor --recommended
```

## AI planner

任意のOpenAI-compatible / local LLM gatewayを差し込めます。Secretはリポジトリへ保存しません。

```bash
export GAME_FACTORY_LLM_ENDPOINT="http://localhost:8000/v1/chat/completions"
export GAME_FACTORY_LLM_MODEL="your-model"
# 必要なgatewayだけ bearer を環境変数で設定
export GAME_FACTORY_LLM_BEARER="..."
python -m game_factory.cli batch --ai --count 30 --keep 5 --seed 2026 --out portfolio
```

LLM出力は直接コードへせず、必ずGameSpecへ正規化してから後段へ渡します。APIが返した候補が不足した場合は決定論的generatorで補完します。

## Feedback loop

```bash
python -m game_factory.cli learn examples/metrics.csv --out state/learned_preferences.json
python -m game_factory.cli batch --count 30 --keep 5 --preferences state/learned_preferences.json --out portfolio-2
```

`docs/ARCHITECTURE.md`, `docs/STORE_PLAYBOOK.md`, `docs/RESEARCH.md` 参照。

## License

本リポジトリはMIT。外部OSSとアセットは各ライセンスを保持し、商用採用前に個別監査します。
