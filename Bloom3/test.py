from manim import *
import numpy as np
import math
import random

# --- FORCE 9:16 REEL COORDINATE FRAME ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * 9 / 16  # 4.5
config.frame_rate = 60


class ReusableRocketsTransition(Scene):
    def construct(self):
        self.camera.background_color = "#02030A"

        # --- optional: a few stars before the transition (gets faded out) ---
        stars = VGroup()
        for _ in range(220):
            x = random.uniform(-config.frame_width / 2, config.frame_width / 2)
            y = random.uniform(-config.frame_height / 2, config.frame_height / 2)
            r = random.uniform(0.010, 0.018)
            stars.add(Dot([x, y, 0], radius=r, color=WHITE).set_opacity(random.uniform(0.25, 0.75)))
        self.add(stars)

        # --- Earth (pre-transition) ---
        earth = ImageMobject("images/earth.png")
        earth.set_width(config.frame_width * 0.95)
        earth.move_to(0.8 * DOWN)
        self.add(earth)

        # --- Target background scene ---
        bg = ImageMobject("images/launch_bg.png")
        # Fill vertical frame (will crop horizontally, which is fine for reels)
        bg.set_height(config.frame_height * 1.02)
        bg.move_to(ORIGIN).shift(0.10 * DOWN)
        bg.set_opacity(0)
        self.add(bg)

        # =========================
        # Transition: zoom into EARTH EDGE + crossfade to background
        # =========================
        # Zoom Earth so it becomes basically a texture, then fade into bg
        self.play(
            earth.animate.scale(3.2).shift(2.4 * DOWN),
            bg.animate.set_opacity(1),
            FadeOut(stars),
            run_time=1.0,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.remove(earth)  # after match-cut, keep only bg

        # =========================
        # Place space-station ON the launch pad (edge/horizon area)
        # =========================
        station = ImageMobject("images/space-station.png")
        station.set_width(0.55)
        station.set_z_index(5)

        # --- pad location: relative to background bounding box (robust across scaling) ---
        # These two are the only values you might tweak:
        PAD_X = 0.30   # 0 = left edge, 1 = right edge (in bg coords)
        PAD_Y = 0.12   # 0 = bottom edge, 1 = top edge

        pad_point = bg.get_corner(DL) + PAD_X * bg.width * RIGHT + PAD_Y * bg.height * UP
        station.move_to(pad_point)

        self.play(FadeIn(station, shift=0.10 * UP), run_time=0.25)

        # =========================
        # Shake to imitate liftoff
        # =========================
        # Quick, visible rumble (no rotation, just jitter)
        station.save_state()
        shake = Succession(
            station.animate.shift(0.05 * RIGHT),
            station.animate.shift(0.10 * LEFT),
            station.animate.shift(0.08 * RIGHT),
            station.animate.shift(0.12 * LEFT),
            station.animate.shift(0.07 * RIGHT),
            station.animate.shift(0.10 * LEFT),
            station.animate.shift(0.05 * RIGHT),
            run_time=0.55,
            rate_func=linear,
        )
        self.play(shake)
        self.play(station.animate.restore(), run_time=0.10)

        # =========================
        # Launch straight upward into the sky
        # =========================
        # Add a subtle “trail” (optional but looks good)
        trail = TracedPath(
            station.get_center,
            dissipating_time=0.35,
            stroke_width=6,
            stroke_opacity=[0.9, 0.0],
        )
        self.add(trail)

        self.play(
            station.animate.shift(5.8 * UP).scale(0.65),
            run_time=1.35,
            rate_func=rate_functions.ease_in_cubic,
        )
        self.play(FadeOut(station), run_time=0.25)
        self.wait(0.3)