# Research notes — 2026-08-14

## Core engine / automation

- Godot Engine — MIT licensed, cross-platform, CLI/headless export support.
- Godot demo projects — official MIT-licensed demos.
- JAMER / JamSet / JamBench (2026) — GodotのGame Jam由来プロジェクトを大規模に検証し、project-level生成/評価へ利用する研究。8,133 verified projectsを報告。
- abagames/headless-godot-skill-kit — editorを開かずにagentでGodotを扱うためのMIT kit.
- crystal-bit/godot-game-template — 汎用Godot starter + CI patterns, MIT.

## Genre starters

- KenneyNL/Starter-Kit-FPS — Godot 4.6, MIT, bundled assets documented CC0.
- KenneyNL/Starter-Kit-3D-Platformer — Godot 4.6, MIT, bundled assets documented CC0.
- KenneyNL/Starter-Kit-Racing — Godot 4.6, MIT, bundled assets documented CC0.
- KenneyNL/Starter-Kit-City-Builder — Godot 4.6, MIT, bundled assets documented CC0.
- gdquest-demos/godot-open-rpg — turn-based RPG demo, MIT; bundled credits must still be reviewed.
- InvadingOctopus/comedot — component-based Godot framework for many 2D genres, MIT.

## Commercial proof that Godot is viable

Godotの公式Showcaseには Brotato, Dome Keeper, Cassette Beasts, Halls of Torment, Buckshot Roulette などの販売作品が掲載されています。ここから学ぶべきなのは「同じゲームを複製すること」ではなく、**強い一文フック、短い説明で理解できるcore loop、反復可能なrun、十分なpolish**です。

## Distribution

- itch.io butler — CLI build upload.
- SteamPipe — Steamworks build upload.
- Steam Store page / build はValve reviewを通す必要があるため、releaseは完全無人化対象にしない。

## URLs

- https://godotengine.org/license/
- https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- https://itch.io/docs/butler/
- https://partner.steamgames.com/doc/sdk/uploading
- https://partner.steamgames.com/doc/store/review_process
- https://godotengine.org/showcase/
- https://arxiv.org/abs/2606.19830
