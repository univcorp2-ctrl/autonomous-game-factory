# Research notes — 2026-08-14

## Closest autonomous predecessors

### Godogen

MIT. Godot / Bevy / Babylon.jsを対象に、短い説明からagentがゲームを作り、asset生成、engine実行、録画またはlive gameで結果を確認する設計。重要な学びは **compile成功ではなくrunning resultを証拠にして反復する** 点。

### Everything Game Dev Code

MIT. Unity / Unreal / Godot / Webを共通studio workflowで扱い、GDD、TDD、asset generation、QA、release/live opsまでレイヤー化するscaffold。重要な学びは **engine固有層と共通productionルールを分離する** 点。

### JAMER / JamSet / JamBench

2026年の研究。Godot Game Jam由来の大規模repository集合をproject-level game generationの学習/評価へ利用し、8,133 verified projectsを報告。大きいprojectほどagentのruntime成功率が急落するため、小さなarchetype + deterministic QA +段階的拡張が現実的。

### GameCraft-Bench

2026年のGodotベンチマーク。140 tasks / 15 game familiesでend-to-end playable game generationを評価し、強いagentでも完全なゲーム生成はまだ難しいと報告。したがって本factoryは「AIに全部任せて大量push」ではなく、テンプレート、QA、実行証拠、release gateを固定する。

## OSS / genre sources

- Godot Engine / official demos — MIT, headless/CLI export.
- abagames/headless-godot-skill-kit — MIT.
- crystal-bit/godot-game-template — MIT.
- Kenney Starter Kit FPS / 3D Platformer / Racing / City Builder — MIT, bundled assets documented CC0.
- gdquest-demos/godot-open-rpg — MIT; asset credits review required.
- InvadingOctopus/comedot — MIT component framework.
- GodotSteam — MIT Steam integration ecosystem.

## Commercial proof

Godot公式Showcaseには Brotato, Dome Keeper, Cassette Beasts, Halls of Torment, Buckshot Roulette などが掲載されている。模倣対象ではなく、強い一文hook、明快なcore loop、repeatability、polishの成功パターンを抽象化して使う。

## Distribution

- itch.io: butler CLIでbuild upload可能。
- Steam: SteamPipeでbuild upload可能。ただしStore Presence / content survey / review / Coming Soon / final releaseはpublisher/Valve側の明示工程を残す。
