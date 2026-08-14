# Architecture

## Portfolio loop

1. **Ideation** — deterministic generator または外部LLMからGameSpec生成
2. **Normalize** — LLM出力を許可mode/parameter schemaへ閉じ込める
3. **Dedup** — mechanics / hooks / palette fingerprint
4. **Rank** — hook/pacing/readability/price仮説
5. **Generate** — Godot text template + game_spec.json
6. **QA** — file/spec checks + optional Godot headless run
7. **Build** — Windows / Linux / Web export
8. **Marketing** — store copy / social copy / trailer plan / asset manifest
9. **Release pack** — itch butler / Steam manifest + release gates
10. **Feedback** — wishlist/conversion/review/playtime/refund
11. **Next generation** — successful mode weightsを更新

## Key principle: proof over claims

AIが「完成した」と言うことは品質証拠にしない。最低でもstatic QA、可能ならGodot headless run、最終的には画面/操作のplaytestを通す。大規模gameを一発生成せず、小さなarchetypeを確実に動かしてからgenre adapterを増やす。

## External OSS policy

外部repositoryは `config/oss_sources.json` のallowlistからだけcloneし、取得commitとlicense fileを `vendor.lock.json` に記録する。外部コードをそのまま商品化するのではなく、architecture/reference/templateとして利用し、アセットlicenseと商標/IPを別チェックする。

## Autonomy boundary

自動: ideation, code/spec generation, QA, build, marketing drafts, release package, analytics.

明示gate: credentials, purchase/payment, contracts, legal/content declarations, store pricing, third-party IP approval, final release.
