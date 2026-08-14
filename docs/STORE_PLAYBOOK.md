# Store / Marketing Playbook

## itch.io

`butler push directory user/game:channel` を使う前提で `release/itch-push.*` を生成します。実際のページ作成、価格、支払い設定はPublisher側で行います。

## Steam

SteamPipe用のbuild uploadは自動化できますが、App ID / Depot ID、Store Presence、Content Survey、審査、Coming Soon、ReleaseはSteamworks上のプロセスが必要です。本リポジトリでは `steam-manifest.json` とチェックリストまでを生成し、最終公開を自動クリックしません。

## マーケティング量産

各ゲームごとに最低限:

- 一文フック
- Short / Long store description
- 3本のSNS草案
- 30秒トレーラーshot list
- 6枚のスクリーンショット候補
- カプセル画像のasset manifest
- タグ候補
- 価格仮説

を作ります。

## KPIフィードバック

`metrics.csv` の推奨列:

- `slug`
- `mode`
- `wishlists`
- `conversion_rate`
- `positive_review_rate`
- `median_playtime_minutes`
- `refund_rate`

短期売上だけを最適化せず、レビュー、継続プレイ、返金率も含めて次の企画配分を更新します。
