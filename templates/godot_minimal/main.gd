extends Node2D

var spec: Dictionary = {}
var mechanics: Dictionary = {}
var palette: Dictionary = {}
var player := Vector2(480, 270)
var enemies: Array[Vector2] = []
var pickups: Array[Vector2] = []
var enemy_spawn := 0.0
var pickup_spawn := 0.0
var elapsed := 0.0
var invuln := 0.0
var score := 0
var health := 3
var finished := false
var rng := RandomNumberGenerator.new()
var hud: Label
var message: Label

func _ready() -> void:
    var raw := FileAccess.get_file_as_string("res://game_spec.json")
    var parsed = JSON.parse_string(raw)
    if typeof(parsed) != TYPE_DICTIONARY:
        push_error("Invalid game_spec.json")
        get_tree().quit(2)
        return
    spec = parsed
    mechanics = spec.get("mechanics", {})
    palette = spec.get("palette", {})
    rng.seed = int(spec.get("seed", 1))
    health = int(mechanics.get("health", 3))
    _build_ui()
    for i in range(4):
        _spawn_enemy()
    for i in range(3):
        _spawn_pickup()
    queue_redraw()

func _build_ui() -> void:
    hud = Label.new()
    hud.position = Vector2(18, 14)
    hud.add_theme_font_size_override("font_size", 22)
    add_child(hud)
    message = Label.new()
    message.position = Vector2(300, 230)
    message.add_theme_font_size_override("font_size", 28)
    add_child(message)

func _process(delta: float) -> void:
    if Input.is_key_pressed(KEY_ESCAPE):
        get_tree().quit()
    if finished:
        if Input.is_key_pressed(KEY_R):
            get_tree().reload_current_scene()
        return
    elapsed += delta
    invuln = max(0.0, invuln - delta)
    var dir := Vector2.ZERO
    if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT): dir.x -= 1.0
    if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT): dir.x += 1.0
    if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP): dir.y -= 1.0
    if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN): dir.y += 1.0
    if dir.length() > 0.0:
        dir = dir.normalized()
    player += dir * float(mechanics.get("player_speed", 290.0)) * delta
    player.x = clamp(player.x, 18.0, 942.0)
    player.y = clamp(player.y, 54.0, 522.0)

    enemy_spawn -= delta
    pickup_spawn -= delta
    if enemy_spawn <= 0.0 and enemies.size() < int(mechanics.get("enemy_limit", 45)):
        _spawn_enemy()
        enemy_spawn = float(mechanics.get("spawn_interval", 0.85))
    if pickup_spawn <= 0.0:
        _spawn_pickup()
        pickup_spawn = float(mechanics.get("pickup_interval", 2.2))

    _move_enemies(delta)
    _collisions()
    _check_end()
    hud.text = "%s   Score %d   HP %d   Time %02d" % [spec.get("title", "Game"), score, health, int(elapsed)]
    queue_redraw()

func _spawn_enemy() -> void:
    var side := rng.randi_range(0, 3)
    var p := Vector2.ZERO
    if side == 0: p = Vector2(rng.randf_range(0, 960), 54)
    elif side == 1: p = Vector2(942, rng.randf_range(54, 540))
    elif side == 2: p = Vector2(rng.randf_range(0, 960), 522)
    else: p = Vector2(18, rng.randf_range(54, 540))
    enemies.append(p)

func _spawn_pickup() -> void:
    if pickups.size() < 12:
        pickups.append(Vector2(rng.randf_range(50, 910), rng.randf_range(85, 500)))

func _move_enemies(delta: float) -> void:
    var base_speed := float(mechanics.get("enemy_speed", 100.0))
    var pressure := 1.0 + min(elapsed / 120.0, 0.8)
    for i in range(enemies.size()):
        var target_dir := enemies[i].direction_to(player)
        enemies[i] += target_dir * base_speed * pressure * delta

func _collisions() -> void:
    for i in range(pickups.size() - 1, -1, -1):
        if player.distance_to(pickups[i]) < 23.0:
            pickups.remove_at(i)
            score += 1
    if invuln <= 0.0:
        for enemy in enemies:
            if player.distance_to(enemy) < 25.0:
                health -= 1
                invuln = 1.0
                break

func _check_end() -> void:
    var mode := str(spec.get("mode", "survivor"))
    var target := int(mechanics.get("target_score", 20))
    var limit := float(mechanics.get("time_limit", 60))
    if health <= 0:
        _finish(false)
    elif mode == "collector" and score >= target:
        _finish(true)
    elif mode == "dodger" and elapsed >= limit:
        _finish(true)
    elif mode == "survivor" and score >= target and elapsed >= 20.0:
        _finish(true)
    elif mode == "collector" and elapsed >= limit:
        _finish(false)

func _finish(win: bool) -> void:
    finished = true
    message.text = ("CLEAR" if win else "RUN OVER") + "\nPress R to restart"

func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, Vector2(960, 540)), Color(palette.get("background", "#10131a")))
    draw_circle(player, 13.0, Color(palette.get("player", "#62f6ff")))
    for enemy in enemies:
        draw_circle(enemy, 11.0, Color(palette.get("enemy", "#ff4d7d")))
    for pickup in pickups:
        draw_circle(pickup, 7.0, Color(palette.get("pickup", "#ffd166")))
