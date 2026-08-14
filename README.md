# Autonomous Game Factory

Godot + Python で、**企画 → バリエーション生成 → ゲーム実装 → QA → ビルド準備 → ストア素材 → マーケティング素材 → 販売データの学習**までを一つのリポジトリにまとめるゲーム量産基盤です。

> 重要: `publish` 系は **dry-run が既定**です。Steam / itch.io の契約、審査、価格確定、最終公開、支払い設定をこのリポジトリが勝手に実行することはありません。

## できること

- `survivor` / `dodger` / `collector` の3系統から企画を大量生成
- Godot 4 向けのプレイ可能な最小ゲームをパラメータ駆動で生成
- タイトル、フック、難易度、速度、敵密度、色、価格仮説を変えてポートフォリオ化
- 企画重複をfingerprintで抑制
- Python静的QA + Godotがある環境ではheadless起動テスト
- Steam / itch.io 用のリリースパックを生成
- ストア説明、短文コピー、SNS投稿案、トレーラー構成、プレスキットを自動生成
- 売上・Wishlist・Conversion・Review・PlaytimeのCSVから次回企画のモード配分を学習
- 許可リストに登録したOSSテンプレートをcloneし、commitとlicenseファイルをlock記録

## 30秒スタート

```bash
python -m game_factory.cli ideate --count 12 --seed 42 --out ideas.json
python -m game_factory.cli batch --count 12 --keep 3 --seed 42 --out generated
python -m game_factory.cli qa generated/neon-echo
```

GodotがPATHにある場合:

```bash
python -m game_factory.cli run generated/neon-echo
```

OSSスターターを取得:

```bash
python -m game_factory.cli vendor --recommended
```

販売素材を生成:

```bash
python -m game_factory.cli pack generated/neon-echo --itch-target yourname/neon-echo
```

## 自律ループ

```bash
python -m game_factory.cli batch --count 30 --keep 5 --seed 2026 --out portfolio
```

`metrics.csv` を投入して、次のbatchに市場フィードバックを反映できます。

```bash
python -m game_factory.cli learn metrics.csv --out state/learned_preferences.json
python -m game_factory.cli batch --count 30 --keep 5 --seed 2027 --preferences state/learned_preferences.json --out portfolio-2
```

## 設計思想

量産の単位を「コードコピー」ではなく **GameSpec** にしています。同じエンジン・同じ検証基盤の上で、企画、ルール、パラメータ、見た目、ストア訴求を別データとして変えるため、AIが大量に提案しても壊れにくくなります。

詳しくは `docs/ARCHITECTURE.md`、販売運用は `docs/STORE_PLAYBOOK.md`、調査元は `docs/RESEARCH.md` を参照してください。

## ライセンス

このリポジトリ自身は MIT License。cloneする外部OSSは各リポジトリのライセンスに従います。`vendor.lock.json` に取得commitを記録します。外部アセットはコードと別にライセンス確認してください。
