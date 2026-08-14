# Architecture

## 1. Portfolio loop

1. **Ideation** — `GameSpec` をseed付きで生成
2. **Dedup** — mechanics / hooks / palette のfingerprintで重複を落とす
3. **Ranking** — pacing、hook数、readability、価格仮説で上位だけ残す
4. **Generation** — Godotテンプレートへ `game_spec.json` を注入
5. **QA** — 構成、Spec整合性、パラメータ外れ値を確認。Godotがあればheadless smoke test
6. **Marketing Pack** — Store copy / social / trailer shot list / asset manifest生成
7. **Release Pack** — itch `butler` とSteamPipe準備ファイル生成
8. **Human / Store Gate** — 契約、価格、年齢/内容申告、審査、最終リリース
9. **Feedback** — wishlist / conversion / review / playtime / refund をCSVで戻す
10. **Next generation** — 実績の良いmodeの企画比率を上げる

## 2. なぜGodotか

- プロジェクトがテキスト中心でAI差分生成に向く
- headless実行ができる
- MITでエンジン自体を商用利用しやすい
- 2D/3D/desktop/web/mobileを一つの制作基盤で扱える
- Game Jam由来のOSSやテンプレートが豊富

## 3. AIの差し替えポイント

現在の `ideation.py` は再現性のある決定論的生成です。ここをLLM/ローカルモデルに差し替えても、**出力をGameSpecへ正規化してから後段へ渡す**ことで、ゲームエンジンや販売パイプラインを壊さずに済みます。

将来の追加候補:

- LLMによるGameSpec生成
- 画像生成によるカプセル/ロゴ草案（最終アートは権利・ブランドチェック）
- 自動プレイbotによる難易度推定
- Gameplay telemetryからのパラメータ最適化
- genre-specific templates: FPS / platformer / racing / city builder / RPG

## 4. 自律性の境界

自動で行ってよいもの: 企画、コード生成、テスト、ビルド、コピー草案、素材チェックリスト、分析。

明示ゲートを残すもの: 支払い、契約、ストア価格確定、法的申告、年齢区分、他者権利を含む素材採用、最終公開。
