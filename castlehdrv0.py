#!/usr/bin/env python3
# -------------------------------------------------------------
# Super Mario 64 - Peach's Castle Outdoors (Ursina)
# -------------------------------------------------------------
# (C) 2025 FlamesCo / Samsoft - GPL-3.0-or-later
# macOS Compatible - No shaders, basic models only
# -------------------------------------------------------------
import math
import os

# Disable shaders before importing Ursina (fixes macOS black screen)
os.environ['URSINA_DISABLE_SHADERS'] = '1'

from ursina import *

app = Ursina(
    title="Super Mario 64 - Peach's Castle",
    borderless=False,
    fullscreen=False,
    development_mode=False,  # Reduces shader usage
    render_mode='default'
)

# Sky color via window
window.color = color.rgb(135, 206, 235)
camera.clip_plane_far = 500

# -------------------------------------------------------------
# GROUND
# -------------------------------------------------------------
ground = Entity(
    model='plane',
    scale=200,
    color=color.rgb(80, 180, 80),
    y=0
)

# Path to castle
path = Entity(
    model='cube',
    scale=(6, 0.1, 30),
    color=color.rgb(190, 160, 110),
    position=(0, 0.05, 12)
)

# -------------------------------------------------------------
# CASTLE (cubes and spheres only - no cone/cylinder)
# -------------------------------------------------------------
# Main body
castle = Entity(
    model='cube',
    scale=(22, 12, 16),
    color=color.rgb(255, 230, 210),
    position=(0, 6, 38)
)

# Center tower
tower_c = Entity(
    model='cube',
    scale=(8, 22, 8),
    color=color.rgb(255, 230, 210),
    position=(0, 11, 38)
)
# Roof as stacked cubes (pyramid shape)
for i in range(4):
    Entity(
        model='cube',
        scale=(7 - i * 1.5, 2, 7 - i * 1.5),
        color=color.rgb(200, 50, 50),
        position=(0, 23 + i * 1.8, 38)
    )

# Left tower
tower_l = Entity(
    model='cube',
    scale=(6, 15, 6),
    color=color.rgb(255, 230, 210),
    position=(-13, 7.5, 38)
)
# Left roof
for i in range(3):
    Entity(
        model='cube',
        scale=(5 - i * 1.2, 1.5, 5 - i * 1.2),
        color=color.rgb(200, 50, 50),
        position=(-13, 16 + i * 1.3, 38)
    )

# Right tower
tower_r = Entity(
    model='cube',
    scale=(6, 15, 6),
    color=color.rgb(255, 230, 210),
    position=(13, 7.5, 38)
)
# Right roof
for i in range(3):
    Entity(
        model='cube',
        scale=(5 - i * 1.2, 1.5, 5 - i * 1.2),
        color=color.rgb(200, 50, 50),
        position=(13, 16 + i * 1.3, 38)
    )

# Door
door = Entity(
    model='cube',
    scale=(5, 7, 0.5),
    color=color.rgb(100, 60, 30),
    position=(0, 3.5, 29.5)
)

# Door arch (sphere squished)
door_arch = Entity(
    model='sphere',
    scale=(3, 2, 1),
    color=color.rgb(100, 60, 30),
    position=(0, 7, 29.5)
)

# Windows
for x in [-7, 7]:
    Entity(
        model='cube',
        scale=(2.5, 3.5, 0.5),
        color=color.rgb(120, 180, 255),
        position=(x, 7, 29.5)
    )

# Bridge
bridge = Entity(
    model='cube',
    scale=(7, 0.4, 14),
    color=color.rgb(140, 100, 60),
    position=(0, 0.2, 22)
)

# Water moat
water = Entity(
    model='cube',
    scale=(70, 0.2, 35),
    color=color.rgb(64, 164, 223),
    position=(0, -0.3, 42)
)

# -------------------------------------------------------------
# TREES (cube trunk + sphere leaves)
# -------------------------------------------------------------
def make_tree(x, z):
    # Trunk (cube instead of cylinder)
    Entity(
        model='cube',
        scale=(1.2, 6, 1.2),
        color=color.rgb(110, 70, 40),
        position=(x, 3, z)
    )
    # Leaves
    Entity(
        model='sphere',
        scale=5,
        color=color.rgb(40, 150, 40),
        position=(x, 7, z)
    )

make_tree(-22, 8)
make_tree(-28, 28)
make_tree(24, 12)
make_tree(30, 32)
make_tree(-18, 50)
make_tree(22, 55)
make_tree(-35, 20)
make_tree(38, 45)

# Hills
Entity(model='sphere', scale=18, color=color.rgb(60, 160, 60), position=(-40, -6, 25))
Entity(model='sphere', scale=24, color=color.rgb(55, 150, 55), position=(45, -8, 40))
Entity(model='sphere', scale=15, color=color.rgb(65, 165, 65), position=(-30, -5, 55))

# -------------------------------------------------------------
# MARIO
# -------------------------------------------------------------
class Mario(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.red,
            scale=(1, 2, 1),
            position=(0, 1, -8)
        )
        # Head
        self.head = Entity(
            parent=self,
            model='sphere',
            color=color.rgb(255, 200, 160),
            scale=0.55,
            y=0.8
        )
        # Hat
        self.hat = Entity(
            parent=self.head,
            model='cube',
            color=color.red,
            scale=(1.4, 0.35, 1.4),
            y=0.35
        )
        
        self.speed = 8
        self.vy = 0
        self.grounded = True
        
    def update(self):
        # Input
        dx = held_keys['d'] - held_keys['a']
        dz = held_keys['w'] - held_keys['s']
        
        # Camera-relative movement
        angle_rad = math.radians(cam.angle)
        fwd_x = math.sin(angle_rad)
        fwd_z = math.cos(angle_rad)
        rgt_x = math.cos(angle_rad)
        rgt_z = -math.sin(angle_rad)
        
        move_x = fwd_x * dz + rgt_x * dx
        move_z = fwd_z * dz + rgt_z * dx
        
        length = math.sqrt(move_x * move_x + move_z * move_z)
        if length > 0:
            move_x /= length
            move_z /= length
            self.rotation_y = math.degrees(math.atan2(move_x, move_z))
        
        self.x += move_x * self.speed * time.dt
        self.z += move_z * self.speed * time.dt
        
        # Gravity
        self.vy -= 32 * time.dt
        self.y += self.vy * time.dt
        
        # Ground clamp
        if self.y <= 1:
            self.y = 1
            self.vy = 0
            self.grounded = True
        
        # Jump
        if held_keys['space'] and self.grounded:
            self.vy = 13
            self.grounded = False

mario = Mario()

# -------------------------------------------------------------
# LAKITU CAMERA
# -------------------------------------------------------------
class LakituCam:
    def __init__(self):
        self.dist = 16
        self.height = 6
        self.angle = 0
        
    def update(self):
        # Rotate camera
        rot_speed = 90
        self.angle += (held_keys['e'] - held_keys['q']) * rot_speed * time.dt
        self.angle += (held_keys['right arrow'] - held_keys['left arrow']) * rot_speed * time.dt
        
        # Zoom
        self.dist -= (held_keys['up arrow'] - held_keys['down arrow']) * 10 * time.dt
        self.dist = max(6, min(35, self.dist))
        
        # Calculate position
        rad = math.radians(self.angle)
        target_x = mario.x - math.sin(rad) * self.dist
        target_z = mario.z - math.cos(rad) * self.dist
        target_y = mario.y + self.height
        
        # Smooth follow
        smooth = 6 * time.dt
        camera.x += (target_x - camera.x) * smooth
        camera.y += (target_y - camera.y) * smooth
        camera.z += (target_z - camera.z) * smooth
        
        # Look at mario
        look_target = Vec3(mario.x, mario.y + 1, mario.z)
        camera.look_at(look_target)

cam = LakituCam()
camera.position = (0, 8, -24)

# -------------------------------------------------------------
# COINS
# -------------------------------------------------------------
coins = []
coin_positions = [
    (-5, 1, -2), (5, 1, -2), (0, 1, 3),
    (-4, 1, 10), (4, 1, 10), (0, 1, 16),
    (-8, 1, 22), (8, 1, 22)
]
for pos in coin_positions:
    c = Entity(
        model='sphere',
        color=color.yellow,
        scale=0.7,
        position=pos
    )
    coins.append(c)

coin_count = 0

# -------------------------------------------------------------
# UI
# -------------------------------------------------------------
title_text = Text(
    text="Peach's Castle",
    position=(0, 0.45),
    origin=(0, 0),
    scale=1.6,
    color=color.white
)
control_text = Text(
    text="WASD=Move  SPACE=Jump  Q/E=Camera  Arrows=Rotate/Zoom",
    position=(0, 0.40),
    origin=(0, 0),
    scale=0.7,
    color=color.white
)
coin_text = Text(
    text="Coins: 0",
    position=(-0.85, 0.45),
    scale=1.4,
    color=color.yellow
)

# -------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------
def update():
    global coin_count
    
    # Camera
    cam.update()
    
    # Coins spin and collect
    for c in coins:
        if c.enabled:
            c.rotation_y += 200 * time.dt
            dx = mario.x - c.x
            dy = mario.y - c.y
            dz = mario.z - c.z
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < 1.5:
                c.disable()
                coin_count += 1
                coin_text.text = f"Coins: {coin_count}"

# -------------------------------------------------------------
# INPUT
# -------------------------------------------------------------
def input(key):
    if key == 'escape':
        application.quit()

# -------------------------------------------------------------
app.run()
