from manim import *
import math
import random
import numpy as np

# --- FORCE 9:16 REEL COORDINATE FRAME ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * 9 / 16  # 4.5
config.frame_rate = 60

#config.save_last_frame = False
#config.from_animation_number = 5
#config.upto_animation_number = 6


class SpaceEconomyIntro(Scene):
    # ---------------- Caption helpers (true centered multiline) ----------------
    def wrap_text_to_lines(self, text: str, font_size: int, max_width: float):
        words = text.split(" ")
        lines, cur = [], []
        for w in words:
            trial = " ".join(cur + [w])
            if cur and Text(trial, font_size=font_size).width > max_width:
                lines.append(" ".join(cur))
                cur = [w]
            else:
                cur.append(w)
        if cur:
            lines.append(" ".join(cur))
        return lines

    def word_groups_for_line(self, line_mob: Text, line_str: str):
        chars = line_mob.submobjects  # glyphs, no spaces
        groups, cur = [], []
        i = 0
        for ch in line_str:
            if ch == " ":
                if cur:
                    groups.append(VGroup(*cur))
                    cur = []
            else:
                if i < len(chars):
                    cur.append(chars[i])
                    i += 1
        if cur:
            groups.append(VGroup(*cur))
        return groups

    def make_caption(self, sentence: str, font_size: int, top_buff: float = 0.55, add_to_scene: bool = True):
        max_width = config.frame_width - 0.7
        lines = self.wrap_text_to_lines(sentence, font_size=font_size, max_width=max_width)

        line_mobs = []
        for ln in lines:
            t = Text(ln, font_size=font_size)
            t.set_x(0)  # center each line
            for glyph in t.submobjects:
                glyph.set_opacity(0)
            line_mobs.append(t)

        caption_group = VGroup(*line_mobs).arrange(DOWN, buff=0.16, center=True)
        caption_group.to_edge(UP, buff=top_buff).shift(0.25 * OUT)
        caption_group.set_x(0)

        if add_to_scene:
            self.add(caption_group)

        groups = []
        for t, ln in zip(line_mobs, lines):
            groups.extend(self.word_groups_for_line(t, ln))

        return caption_group, groups

    def reveal_caption_groups(self, groups, word_fade_time=0.06):
        for g in groups:
            self.play(g.animate.set_opacity(1), run_time=word_fade_time, rate_func=smooth)

    def caption_lagged_anim(self, groups, lag=0.05):
        return LaggedStart(*[g.animate.set_opacity(1) for g in groups], lag_ratio=lag)

    # ---------------- Scene 3 bars helper ----------------
    def build_exponential_bars(self):
        x_labels = ["25–26", "27–28", "29–30", "31–32", "33–34", "35"]
        n = len(x_labels)

        start_val = 15.0
        end_val = 108.0
        values = start_val * (end_val / start_val) ** np.linspace(0, 1, n)
        values_rounded = [int(round(v)) for v in values]

        chart_width = config.frame_width - 0.8
        baseline_y = -2.65
        max_bar_height = 3.05

        baseline = Line(
            np.array([-chart_width / 2, baseline_y, 0]),
            np.array([ chart_width / 2, baseline_y, 0]),
        ).set_stroke(WHITE, width=3, opacity=0.30)

        y_axis = Line(
            np.array([-chart_width / 2, baseline_y, 0]),
            np.array([-chart_width / 2, baseline_y + max_bar_height + 0.15, 0]),
        ).set_stroke(WHITE, width=3, opacity=0.16)

        x_font = 14
        v_font = 16

        step = chart_width / n
        bar_w = step * 0.55

        bars, xtext, vtext = VGroup(), VGroup(), VGroup()
        for i, (lab, v) in enumerate(zip(x_labels, values_rounded)):
            h = (v / end_val) * max_bar_height
            x = -chart_width / 2 + step * (i + 0.5)

            bar = Rectangle(width=bar_w, height=h)
            bar.set_fill(WHITE, opacity=0.22)
            bar.set_stroke(WHITE, width=2, opacity=0.35)
            bar.move_to(np.array([x, baseline_y + h / 2, 0]))

            bar.save_state()
            bottom_point = bar.get_bottom().copy()
            bar.stretch(0.001 / max(h, 1e-6), dim=1, about_point=bottom_point)
            bar.set_opacity(0)

            xl = Text(lab, font_size=x_font).set_fill(WHITE, opacity=0.55)
            xl.move_to(np.array([x, baseline_y - 0.30, 0]))

            vl = Text(f"${v}B", font_size=v_font).set_fill(WHITE, opacity=0.85)
            vl.set_opacity(0)

            bars.add(bar)
            xtext.add(xl)
            vtext.add(vl)

        chart = VGroup(baseline, y_axis, bars, xtext, vtext)
        return chart, bars, vtext

    # ---------------- Stock axes (NO LaTeX), jagged line, low fluctuation ----------------
    def make_small_stock_axes(self):
        x0, x1 = -1.55, 1.55
        y0, y1 = -1.35, 1.15

        x_axis = Line([x0, y0, 0], [x1, y0, 0]).set_stroke(WHITE, width=3, opacity=0.45)
        y_axis = Line([x0, y0, 0], [x0, y1, 0]).set_stroke(WHITE, width=3, opacity=0.45)

        x_label = Text("Year", font_size=18).set_fill(WHITE, opacity=0.75)
        x_label.next_to(x_axis, DOWN, buff=0.16)

        y_label = Text("Satellites", font_size=18).set_fill(WHITE, opacity=0.75)
        y_label.rotate(90 * DEGREES)
        y_label.next_to(y_axis, LEFT, buff=0.18)

        axes_group = VGroup(x_axis, y_axis, x_label, y_label)

        def to_point(t, val):
            x = x0 + (x1 - x0) * (t / 5)
            y = y0 + (y1 - y0) * (val / 70000)
            return np.array([x, y, 0.0])

        ts = np.linspace(0, 5, 26)
        tnorm = ts / 5.0
        y_start, y_end = 9000, 70000

        base = y_start + (y_end - y_start) * tnorm
        wiggle = (
            420 * np.sin(2 * np.pi * tnorm * 2.0) +
            240 * np.sin(2 * np.pi * tnorm * 4.0 + 0.6)
        )
        ys = np.clip(base + wiggle, 0, 70000)
        pts = [to_point(t, y) for t, y in zip(ts, ys)]

        line_full = VMobject()
        line_full.set_points_as_corners(pts)
        line_full.set_stroke(WHITE, width=5, opacity=0.85)

        return axes_group, line_full

    def clamp_to_frame(self, p, margin=0.30):
        half_w = config.frame_width / 2
        half_h = config.frame_height / 2
        x = min(max(p[0], -half_w + margin), half_w - margin)
        y = min(max(p[1], -half_h + margin), half_h - margin)
        return np.array([x, y, p[2]])

    # ---------------- Main ----------------
    def construct(self):
        self.camera.background_color = "#02030A"

        # =========================
        # Stars (stay throughout until launchpad transition)
        # =========================
        NORMAL_STARS = 350
        BRIGHT_STARS = 35
        stars = VGroup()
        for _ in range(NORMAL_STARS):
            x = random.uniform(-config.frame_width / 2,  config.frame_width / 2)
            y = random.uniform(-config.frame_height / 2, config.frame_height / 2)
            r = random.uniform(0.010, 0.018)
            stars.add(Dot([x, y, 0], radius=r, color=WHITE).set_opacity(random.uniform(0.25, 0.80)))
        for _ in range(BRIGHT_STARS):
            x = random.uniform(-config.frame_width / 2,  config.frame_width / 2)
            y = random.uniform(-config.frame_height / 2, config.frame_height / 2)
            r = random.uniform(0.018, 0.030)
            stars.add(Dot([x, y, 0], radius=r, color=WHITE).set_opacity(random.uniform(0.65, 1.0)))
        self.add(stars)

        # =========================
        # Scene 1: Earth + $415B
        # =========================
        earth = ImageMobject("images/earth.png")
        earth.set_width(config.frame_width * 0.75)
        earth.move_to(1.7 * DOWN)

        glow = Circle(radius=earth.width * 0.60)
        glow.set_fill(BLUE_E, opacity=0.16)
        glow.set_stroke(width=0)
        glow.move_to(earth.get_center())

        overlay_415 = Text("$415B", font_size=64, weight=BOLD).set_fill(WHITE, opacity=0.5)
        overlay_415.move_to(earth.get_center() + 0.05 * UP).shift(0.15 * OUT)

        earth_group = Group(glow, earth, overlay_415)
        self.add(earth_group)

        earth_center = earth.get_center()
        glow_center = glow.get_center()
        earth.save_state()
        glow.save_state()

        earth.scale(0.001, about_point=earth_center)
        glow.scale(0.001, about_point=glow_center)
        overlay_415.set_opacity(0)

        self.play(
            earth.animate.restore(),
            glow.animate.restore(),
            run_time=0.6,
            rate_func=rate_functions.ease_out_back,
        )
        self.play(overlay_415.animate.set_opacity(0.5), run_time=0.25)

        earth.add_updater(lambda m, dt: m.rotate(-0.12 * dt, about_point=m.get_center()))
        glow.add_updater(lambda m: m.move_to(earth.get_center()))

        caption1_text = "The global space economy reached $415 billion this year, but the real engine isn’t moon landings."
        caption1, groups1 = self.make_caption(caption1_text, font_size=24, top_buff=0.55)
        self.reveal_caption_groups(groups1, word_fade_time=0.06)
        self.wait(0.5)

        # =========================
        # Scene 2: satellites + 71%
        # =========================
        self.play(FadeOut(caption1), run_time=0.30)

        target_pos = 0.6 * DOWN
        target_scale = 0.88
        self.play(
            earth_group.animate.scale(target_scale, about_point=earth.get_center()).move_to(target_pos),
            FadeOut(overlay_415),
            run_time=0.8,
            rate_func=smooth
        )
        earth_group.remove(overlay_415)
        self.remove(overlay_415)

        r1 = earth.width * 0.52
        r2 = earth.width * 0.68
        r3 = earth.width * 0.84

        orbits = VGroup(Circle(radius=r1), Circle(radius=r2), Circle(radius=r3))
        orbits.set_stroke(WHITE, width=1, opacity=0.12)
        orbits.move_to(earth.get_center())
        self.add(orbits)
        orbits.add_updater(lambda m: m.move_to(earth.get_center()))

        satellites = VGroup()
        radii = [r1, r2, r3]
        for _ in range(28):
            dot = Dot(radius=0.018, color=WHITE)
            dot.set_opacity(random.uniform(0.65, 1.0))
            dot.theta = random.uniform(0, TAU)
            dot.omega = random.uniform(0.6, 1.3) * (1 if random.random() > 0.5 else -1)
            dot.rad = random.choice(radii)

            def updater(mob, dt):
                mob.theta += mob.omega * dt
                mob.move_to(
                    earth.get_center()
                    + mob.rad * np.array([math.cos(mob.theta), math.sin(mob.theta), 0.0])
                )

            dot.add_updater(updater)
            satellites.add(dot)

        self.play(FadeIn(satellites), run_time=0.35)

        pct = 0.71
        pie_r = earth.width * 0.28
        pie_bg = Circle(radius=pie_r).set_fill(WHITE, opacity=0.08).set_stroke(WHITE, width=2, opacity=0.20)
        sector_71 = Sector(radius=pie_r, start_angle=90 * DEGREES, angle=TAU * pct) \
            .set_fill(WHITE, opacity=0.25).set_stroke(WHITE, width=2, opacity=0.35)
        pie_label = Text("71%", font_size=40, weight=BOLD).set_fill(WHITE, opacity=0.9)

        def lock_to_earth(m):
            m.move_to(earth.get_center()).shift(0.25 * OUT)

        for m in (pie_bg, sector_71, pie_label):
            lock_to_earth(m)
            m.add_updater(lock_to_earth)

        self.play(Create(pie_bg), run_time=0.30)
        self.play(Create(sector_71), run_time=0.55)
        self.play(FadeIn(pie_label), run_time=0.18)

        caption2_text = "It’s satellites, making up 71 percent of the entire space market."
        caption2, groups2 = self.make_caption(caption2_text, font_size=24, top_buff=0.55)
        self.reveal_caption_groups(groups2, word_fade_time=0.06)
        self.wait(0.5)

        # =========================
        # Scene 3: bars (slide left/right)
        # =========================
        old_visuals = Group(earth_group, orbits, satellites, pie_bg, sector_71, pie_label, caption2)

        caption3_text = "By 2035, satellite revenue is expected to grow from $15 billion to more than $108 billion."
        caption3, groups3 = self.make_caption(caption3_text, font_size=24, top_buff=0.55)

        chart, bars, vlabels = self.build_exponential_bars()
        new_visuals = Group(caption3, chart)

        shift_amt = config.frame_width + 2.0
        new_visuals.shift(RIGHT * shift_amt)
        self.add(new_visuals)

        self.play(
            old_visuals.animate.shift(LEFT * shift_amt),
            new_visuals.animate.shift(LEFT * shift_amt),
            run_time=0.85,
            rate_func=smooth
        )

        earth.clear_updaters()
        glow.clear_updaters()
        orbits.clear_updaters()
        pie_bg.clear_updaters()
        sector_71.clear_updaters()
        pie_label.clear_updaters()
        for d in satellites:
            d.clear_updaters()
        self.remove(old_visuals)

        self.reveal_caption_groups(groups3, word_fade_time=0.06)

        bar_groups = []
        for bar, vl in zip(bars, vlabels):
            vl.add_updater(lambda m, b=bar: m.next_to(b, UP, buff=0.10))
            bar_groups.append(AnimationGroup(Restore(bar), vl.animate.set_opacity(1), lag_ratio=0.65))

        self.play(
            LaggedStart(*bar_groups, lag_ratio=0.18),
            run_time=2.8,
            rate_func=rate_functions.ease_in_out_cubic
        )
        for vl in vlabels:
            vl.clear_updaters()

        self.wait(0.35)

        # =========================================================
        # Scene 4A: Low orbit + moving satellite (slide out top / in bottom)
        # =========================================================
        old_scene3 = Group(caption3, chart)

        caption4a_text = "Most are in low orbit, just 100–1,200 miles above us and circling Earth every 90 minutes."
        caption4a, groups4a = self.make_caption(caption4a_text, font_size=22, top_buff=0.55, add_to_scene=False)

        earth2 = ImageMobject("images/earth.png")
        earth2.set_width(config.frame_width * 1.15)
        earth2.move_to(3.35 * DOWN)

        orbit_factor = 0.88

        orbit_path = always_redraw(
            lambda: Circle(radius=earth2.width * orbit_factor)
            .move_to(earth2.get_center())
            .set_stroke(WHITE, width=2, opacity=0.10)
        )

        sat = ImageMobject("images/satellite.png")
        base_sat_w = config.frame_width * 0.12
        sat.set_width(base_sat_w)
        sat.theta = 20 * DEGREES
        sat.omega = 0.30

        def sat_updater_4a(m, dt):
            m.theta += m.omega * dt
            R = earth2.width * orbit_factor
            c = earth2.get_center()
            m.move_to(c + R * np.array([math.cos(m.theta), math.sin(m.theta), 0.0]))

        sat.add_updater(sat_updater_4a)
        sat_updater_4a(sat, 0)

        visuals4a = Group(earth2, orbit_path, sat).shift(0.25 * UP)
        new_scene4a = Group(caption4a, visuals4a)

        slide_amt = config.frame_height + 2.0
        new_scene4a.shift(DOWN * slide_amt)
        self.add(new_scene4a)

        self.play(
            old_scene3.animate.shift(UP * slide_amt),
            new_scene4a.animate.shift(UP * slide_amt),
            run_time=0.85,
            rate_func=smooth
        )
        self.remove(old_scene3)

        def unit_normal():
            v = sat.get_center() - earth2.get_center()
            n = np.linalg.norm(v)
            return v / (n if n > 1e-6 else 1.0)

        marker = always_redraw(
            lambda: Line(
                start=sat.get_center() - unit_normal() * (sat.height * 0.50),
                end=earth2.get_center() + unit_normal() * (earth2.width * 0.50),
            ).set_stroke(WHITE, width=2, opacity=0.65)
        )

        marker_label = always_redraw(
            lambda: Text("1200 miles", font_size=20)
            .set_fill(WHITE, opacity=0.85)
            .next_to(marker.get_start(), RIGHT, buff=0.10)
        )

        marker.set_opacity(0)
        marker_label.set_opacity(0)
        self.add(marker, marker_label)
        self.play(marker.animate.set_opacity(1), marker_label.animate.set_opacity(1), run_time=0.20)

        self.add(caption4a)
        self.reveal_caption_groups(groups4a, word_fade_time=0.06)
        self.wait(3.0)

        # =========================================================
        # Scene 4B: STACKED layout (Earth+orbit+sat above graph)
        # =========================================================
        caption4b_text = "And 70,000 more are expected in the next five years."
        caption4b, groups4b = self.make_caption(caption4b_text, font_size=22, top_buff=0.55, add_to_scene=False)

        axes_group, line_full = self.make_small_stock_axes()

        graph_shift = DOWN * 2.00
        axes_group.shift(graph_shift)
        line_full.shift(graph_shift)
        axes_group.set_opacity(0)

        # Earth becomes tracker-driven live object for smooth transitions
        earth_x = ValueTracker(earth2.get_center()[0])
        earth_y = ValueTracker(earth2.get_center()[1])
        earth_scale_t = ValueTracker(1.0)

        earth_template = ImageMobject("images/earth.png")
        earth_template.set_width(earth2.width)

        def earth_draw():
            c = np.array([earth_x.get_value(), earth_y.get_value(), 0.0])
            s = earth_scale_t.get_value()
            m = earth_template.copy()
            m.move_to(c)
            m.scale(s, about_point=c)
            return m

        earth_live = always_redraw(earth_draw)

        orbit_live = always_redraw(
            lambda: Circle(radius=earth_live.width * orbit_factor)
            .move_to(earth_live.get_center())
            .set_stroke(WHITE, width=2, opacity=0.10)
        )

        self.remove(orbit_path)
        self.remove(earth2)
        self.add(earth_live, orbit_live)

        sat.clear_updaters()

        def sat_updater_live(m, dt):
            m.theta += m.omega * dt
            R = earth_live.width * orbit_factor
            c = earth_live.get_center()
            m.move_to(c + R * np.array([math.cos(m.theta), math.sin(m.theta), 0.0]))
            m.set_width(base_sat_w * earth_scale_t.get_value())

        sat.add_updater(sat_updater_live)

        earth_end = UP * 1.15
        scale_end = 0.22

        prog = ValueTracker(0.0)
        line_partial = always_redraw(lambda: line_full.copy().pointwise_become_partial(line_full, 0, prog.get_value()))

        rocket = ImageMobject("images/rocket.png")
        rocket.set_width(0.22)

        def rocket_updater(m, dt):
            t = prog.get_value()
            p = line_full.point_from_proportion(t)
            m.move_to(p)
            eps = 0.002
            t2 = min(1.0, t + eps)
            p2 = line_full.point_from_proportion(t2)
            v = p2 - p
            if np.linalg.norm(v) > 1e-6:
                ang = angle_of_vector(v)
                m.set_angle(ang - PI / 2)

        rocket.add_updater(rocket_updater)

        def value_text_pos():
            p = rocket.get_center() + 0.20 * UP + 0.12 * RIGHT
            if p[1] > 0.70:
                p = rocket.get_center() + 0.22 * DOWN + 0.12 * RIGHT
            return self.clamp_to_frame(p, margin=0.32)

        def current_value():
            return int(round(9000 + (70000 - 9000) * prog.get_value()))

        val_text = always_redraw(
            lambda: Text(f"{current_value():,}", font_size=20, weight=BOLD)
            .set_fill(WHITE, opacity=0.92)
            .move_to(value_text_pos())
        )
        val_text.set_opacity(0)

        self.add(caption4b, axes_group, line_partial, rocket, val_text)

        self.play(
            FadeOut(caption4a),
            FadeOut(marker),
            FadeOut(marker_label),
            earth_x.animate.set_value(earth_end[0]),
            earth_y.animate.set_value(earth_end[1]),
            earth_scale_t.animate.set_value(scale_end),
            axes_group.animate.set_opacity(1),
            val_text.animate.set_opacity(1),
            FadeIn(caption4b),
            run_time=0.95,
            rate_func=smooth
        )

        self.play(self.caption_lagged_anim(groups4b, lag=0.05), run_time=1.4, rate_func=linear)
        self.play(prog.animate.set_value(1.0), run_time=2.8, rate_func=smooth)
        self.wait(0.35)

        # =========================================================
        # SCENE 5 (AS YOU HAVE IT)
        # =========================================================
        slide_amt = config.frame_height + 2.0

        old_mobs = [m for m in list(self.mobjects) if m is not stars]
        if old_mobs:
            for m in old_mobs:
                try:
                    m.clear_updaters()
                except Exception:
                    pass

            old_group = Group(*old_mobs)

            caption5a_text = "What changed? Reusable rockets. One launch now deploys dozens at once"
            caption5a, groups5a = self.make_caption(caption5a_text, font_size=22, top_buff=0.55, add_to_scene=False)
            caption5a.shift(DOWN * slide_amt)
            self.add(caption5a)

            self.play(
                old_group.animate.shift(UP * slide_amt),
                caption5a.animate.shift(UP * slide_amt),
                run_time=0.75,
                rate_func=smooth,
            )
            self.remove(*old_mobs)
        else:
            caption5a_text = "What changed? Reusable rockets. One launch now deploys dozens at once"
            caption5a, groups5a = self.make_caption(caption5a_text, font_size=22, top_buff=0.55, add_to_scene=True)

        NUM_STATIONS = 9
        stations = Group()

        x_margin = 0.35
        target_w = 0.45

        random.seed(3)
        for _ in range(NUM_STATIONS):
            st = ImageMobject("images/space-station.png")
            st.scale(target_w / st.width)

            x = random.uniform(-config.frame_width / 2 + x_margin, config.frame_width / 2 - x_margin)
            y = -config.frame_height / 2 - random.uniform(0.4, 1.6)
            st.move_to(np.array([x, y, 0.0]))

            st.rotate(random.uniform(-8, 8) * DEGREES)
            stations.add(st)

        self.add(stations)

        fly_anims = []
        for st in stations:
            drift = random.uniform(-0.25, 0.25)
            end_pos = st.get_center() + np.array([drift, config.frame_height + 3.0, 0.0])
            fly_anims.append(st.animate.move_to(end_pos))

        FLY_TIME = 4.2
        self.play(
            self.caption_lagged_anim(groups5a, lag=0.03),
            LaggedStart(*fly_anims, lag_ratio=0.10),
            run_time=FLY_TIME,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.remove(stations)
        self.wait(0.15)

        self.play(FadeOut(caption5a), run_time=0.25)

        caption5b_text = "Pushing launch costs toward $100 per kilogram."
        caption5b, groups5b = self.make_caption(caption5b_text, font_size=22, top_buff=0.55, add_to_scene=True)

        graph_top = caption5b.get_bottom()[1] - 0.35
        graph_bottom = -config.frame_height / 2 + 0.55
        graph_left = -config.frame_width / 2 + 0.55
        graph_right = config.frame_width / 2 - 0.55

        gx0, gx1 = graph_left, graph_right
        gy0, gy1 = graph_bottom, graph_top

        x_axis = Line([gx0, gy0, 0], [gx1, gy0, 0]).set_stroke(WHITE, width=3, opacity=0.45)
        y_axis = Line([gx0, gy0, 0], [gx0, gy1, 0]).set_stroke(WHITE, width=3, opacity=0.45)

        x_lab = Text("Time", font_size=18).set_fill(WHITE, opacity=0.75)
        x_lab.next_to(x_axis, DOWN, buff=0.12)

        y_lab = Text("Cost ($/kg)", font_size=18).set_fill(WHITE, opacity=0.75)
        y_lab.rotate(90 * DEGREES)
        y_lab.next_to(y_axis, LEFT, buff=0.14)

        def map_point(t, val):
            x = gx0 + (gx1 - gx0) * t
            y = gy0 + (gy1 - gy0) * (val / 5000.0)
            return np.array([x, y, 0.0])

        vals = [4700, 3800, 3000, 2200, 1500, 900, 450, 220, 120, 100]
        ts = np.linspace(0, 1, len(vals))
        pts = [map_point(t, v) for t, v in zip(ts, vals)]

        line_full = VMobject()
        line_full.set_points_as_corners(pts)
        line_full.set_stroke(WHITE, width=6, opacity=0.90)

        prog = ValueTracker(0.0)

        def clamp01(x: float) -> float:
            return max(0.0, min(1.0, float(x)))

        line_partial = always_redraw(
            lambda: line_full.copy().pointwise_become_partial(line_full, 0, clamp01(prog.get_value()))
        )

        def current_cost() -> int:
            a = clamp01(prog.get_value())
            return int(round(4700 + (100 - 4700) * a))

        def tip_point():
            a = clamp01(prog.get_value())
            return line_full.point_from_proportion(a)

        def label_pos():
            p = tip_point() + 0.20 * UP + 0.18 * RIGHT
            half_w = config.frame_width / 2
            half_h = config.frame_height / 2
            margin = 0.35
            p[0] = min(max(p[0], -half_w + margin), half_w - margin)
            p[1] = min(max(p[1], -half_h + margin), half_h - margin)
            return p

        cost_label = always_redraw(
            lambda: Text(f"${current_cost():,}", font_size=20, weight=BOLD)
            .set_fill(WHITE, opacity=0.92)
            .move_to(label_pos())
        )

        end_tag = Text("$100", font_size=18, weight=BOLD).set_fill(WHITE, opacity=0.90)
        end_tag.next_to(pts[-1], UP + RIGHT, buff=0.10)
        end_tag.set_opacity(0)

        graph_axes = VGroup(x_axis, y_axis, x_lab, y_lab)

        self.play(
            self.caption_lagged_anim(groups5b, lag=0.03),
            FadeIn(graph_axes, shift=0.10 * UP),
            run_time=1.2,
            rate_func=smooth,
        )

        self.add(line_partial, cost_label)

        self.play(
            prog.animate.set_value(1.0),
            run_time=1.8,
            rate_func=smooth,
        )

        prog.set_value(1.0)
        line_partial.clear_updaters()
        cost_label.clear_updaters()

        self.play(end_tag.animate.set_opacity(1), run_time=0.25)
        self.wait(0.5)

        # =========================================================
        # SCENE 6:
        # - 6A pops in one-by-one: caption -> satellite -> mountains -> ships -> town -> beams extend
        # - 6B slide to pie chart, slice grows + scaling number (NO LaTeX)
        # =========================================================

        # -------------------------
        # 5 -> 6 SLIDE transition (keep stars)
        # -------------------------
        slide_dx = config.frame_width + 2.0

        prev_mobs = [m for m in list(self.mobjects) if m is not stars]
        prev_group = Group(*prev_mobs) if prev_mobs else Group()

        # Build 6A group OFFSCREEN RIGHT (so the slide is smooth)
        caption6a_text = "And with the improvement of antennas, satellites will be used to deliver internet where fiber can’t."
        caption6a, groups6a = self.make_caption(caption6a_text, font_size=22, top_buff=0.55, add_to_scene=False)

        sat_icon = ImageMobject("images/satellite.png")
        sat_icon.scale(0.70 / sat_icon.width)
        sat_icon.next_to(caption6a, DOWN, buff=0.35)
        sat_icon.set_z_index(5)

        # Targets: ensure fully in frame, a bit smaller, and centered with margins
        mountains = ImageMobject("images/mountains.png")
        ships = ImageMobject("images/ships.png")
        town = ImageMobject("images/town.png")

        # Slightly smaller widths so left/right never clip
        for mob, w in [(mountains, 1.25), (ships, 1.20), (town, 1.25)]:
            mob.scale(w / mob.width)
            mob.set_z_index(3)

        # Start dim (not fully opaque)
        DIM_OP = 0.28
        mountains.set_opacity(DIM_OP)
        ships.set_opacity(DIM_OP)
        town.set_opacity(DIM_OP)

        # Place them with safe margins
        y_targets = -2.55
        x_pad = 1.70  # keep away from edges
        mountains.move_to(np.array([-x_pad, y_targets, 0.0]))
        ships.move_to(np.array([0.0, y_targets, 0.0]))
        town.move_to(np.array([x_pad, y_targets, 0.0]))

        # Beams extend out of satellite
        b1_t = ValueTracker(0.0)
        b2_t = ValueTracker(0.0)
        b3_t = ValueTracker(0.0)

        def beam(s_tracker, target_mob):
            return always_redraw(
                lambda: Line(
                    sat_icon.get_bottom(),
                    sat_icon.get_bottom() + s_tracker.get_value() * (target_mob.get_top() - sat_icon.get_bottom()),
                ).set_stroke(WHITE, width=5, opacity=0.60)
            )

        beam1 = beam(b1_t, mountains)
        beam2 = beam(b2_t, ships)
        beam3 = beam(b3_t, town)

        group6a = Group(caption6a, sat_icon, mountains, ships, town, beam1, beam2, beam3)
        group6a.shift(RIGHT * slide_dx)
        self.add(group6a)

        # Slide old out LEFT, new in from RIGHT
        if len(prev_group.submobjects) > 0:
            for m in prev_group.submobjects:
                try:
                    m.clear_updaters()
                except Exception:
                    pass
            self.play(
                prev_group.animate.shift(LEFT * slide_dx),
                group6a.animate.shift(LEFT * slide_dx),
                run_time=0.75,
                rate_func=smooth,
            )
            self.remove(prev_group)
        else:
            self.play(group6a.animate.shift(LEFT * slide_dx), run_time=0.75, rate_func=smooth)

        # Reveal caption words after slide
        self.play(self.caption_lagged_anim(groups6a, lag=0.02), run_time=1.05, rate_func=linear)

        # Animate beams; ONLY after each beam finishes, "light up" that target
        self.play(b1_t.animate.set_value(1.0), run_time=0.65, rate_func=smooth)
        self.play(mountains.animate.set_opacity(1.0), run_time=0.25, rate_func=smooth)

        self.play(b2_t.animate.set_value(1.0), run_time=0.65, rate_func=smooth)
        self.play(ships.animate.set_opacity(1.0), run_time=0.25, rate_func=smooth)

        self.play(b3_t.animate.set_value(1.0), run_time=0.65, rate_func=smooth)
        self.play(town.animate.set_opacity(1.0), run_time=0.25, rate_func=smooth)

        self.wait(0.35)

        # -------------------------
        # 6B: Slide transition -> PROGRESS BAR for 2.5B offline (replace your current 6B block)
        # -------------------------
        caption6b_text = "2.5 billion people today still have no access."
        caption6b, groups6b = self.make_caption(
            caption6b_text, font_size=22, top_buff=0.55, add_to_scene=False
        )

        # Group A (slide out) — keep consistent with your 6A objects
        groupA = Group(caption6a, sat_icon, mountains, ships, town, beam1, beam2, beam3)

        # ---- Progress bar visual (Group B) ----
        total_b = 8.0
        offline_b = 2.5
        online_b = total_b - offline_b
        pct = offline_b / total_b  # ~0.3125

        # Wider + thicker bar
        bar_w = config.frame_width - 0.55
        bar_h = 0.38  # thicker than before

        # Shift everything upward (center the block)
        BLOCK_SHIFT_UP = 0.95

        bar_y = -1.70 + BLOCK_SHIFT_UP
        num_y = -0.80 + BLOCK_SHIFT_UP

        bar_bg = RoundedRectangle(
            width=bar_w, height=bar_h, corner_radius=bar_h / 2
        ).set_fill(WHITE, opacity=0.10).set_stroke(WHITE, width=2, opacity=0.22)
        bar_bg.move_to(np.array([0.0, bar_y, 0.0]))

        fill_t = ValueTracker(0.0)   # 0 -> pct
        num_t = ValueTracker(0.0)    # 0 -> 2.5

        def fill_width():
            return max(0.001, bar_w * float(fill_t.get_value()))

        # Fill (left-anchored inside bg)
        bar_fill = always_redraw(
            lambda: RoundedRectangle(
                width=fill_width(), height=bar_h, corner_radius=bar_h / 2
            )
            .set_fill(WHITE, opacity=0.32)
            .set_stroke(width=0)
            .align_to(bar_bg, LEFT)
            .move_to(bar_bg.get_left() + RIGHT * (fill_width() / 2))
        )

        # Big number above the bar
        big_num = always_redraw(
            lambda: Text(f"{num_t.get_value():.1f}B", font_size=72, weight=BOLD)
            .set_fill(WHITE, opacity=0.95)
            .move_to(np.array([0.0, num_y, 0.0]))
        )

        # Labels below bar (tighten spacing slightly)
        offline_label = Text(f"Offline: {offline_b:.1f}B", font_size=22).set_fill(WHITE, opacity=0.85)
        online_label  = Text(f"Online: {online_b:.1f}B",  font_size=22).set_fill(WHITE, opacity=0.65)
        labels = VGroup(offline_label, online_label).arrange(RIGHT, buff=0.70, center=True)
        labels.next_to(bar_bg, DOWN, buff=0.22)
        labels.set_x(0)
        if labels.width > bar_w:
            labels.scale_to_fit_width(bar_w)
            labels.set_x(0)

        # People icons INSIDE filled portion (tighter spacing)
        person_path = "images/person.png"
        person_h = bar_h * 0.78
        pad = 0.10
        spacing = person_h * 0.70  # less space between people (tighter)

        max_people = 26
        people = Group()
        for _ in range(max_people):
            p = ImageMobject(person_path)
            p.set_height(person_h)
            p.set_opacity(0.0)
            people.add(p)

        def people_updater(g):
            fw = fill_width()
            usable = fw - 2 * pad
            if usable <= person_h * 0.6:
                k = 0
            else:
                k = int(min(max_people, max(0, math.floor(usable / spacing))))

            left_x = bar_bg.get_left()[0] + pad
            y = bar_bg.get_center()[1]

            for i, p in enumerate(g.submobjects):
                if i < k:
                    p.set_opacity(0.85)
                    p.move_to(np.array([left_x + i * spacing, y, 0.0]))
                else:
                    p.set_opacity(0.0)

        people.add_updater(people_updater)
        people_updater(people)

        progress_group = Group(bar_bg, bar_fill, people, big_num, labels)

        # ---- Slide transition (A out left, B in from right) ----
        slide_dx = config.frame_width + 2.0
        groupB = Group(caption6b, progress_group).shift(RIGHT * slide_dx)
        self.add(groupB)

        self.play(
            groupA.animate.shift(LEFT * slide_dx),
            groupB.animate.shift(LEFT * slide_dx),
            run_time=0.75,
            rate_func=smooth,
        )

        # Cleanup A and finalize B
        self.remove(groupA)
        self.add(caption6b)

        self.play(self.caption_lagged_anim(groups6b, lag=0.03), run_time=1.0, rate_func=linear)

        # Animate the fill + number together
        self.play(
            fill_t.animate.set_value(pct),
            num_t.animate.set_value(offline_b),
            run_time=1.6,
            rate_func=smooth,
        )

        self.wait(0.6)

        # =========================================================
        # SCENE 7: "Competition is accelerating everything..." (Option A)
        # Visual: orbital slots filling up + crowding pulse
        # Transition IN: collapse previous visuals (keep stars)
        # =========================================================

        keep = {stars}
        to_remove = [m for m in list(self.mobjects) if m not in keep]
        for m in to_remove:
            try:
                m.clear_updaters()
            except Exception:
                pass
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove], run_time=0.35, rate_func=smooth)
            self.remove(*to_remove)

        # -------------------------
        # Caption
        # -------------------------
        caption7_text = "Competition is accelerating everything, governments and companies racing to claim scarce orbital space and spectrum."
        caption7, groups7 = self.make_caption(caption7_text, font_size=22, top_buff=0.55, add_to_scene=True)

        # -------------------------
        # Earth + orbit ring (STROKE ONLY, NEVER animate set_opacity on Circle)
        # -------------------------
        earth7 = ImageMobject("images/earth.png")
        earth7.set_width(config.frame_width * 0.44)
        earth7.move_to(np.array([0.0, -2.80, 0.0]))
        earth7.set_opacity(0.0)
        earth7.set_z_index(5)
        self.add(earth7)

        earth7.add_updater(lambda m, dt: m.rotate(-0.10 * dt, about_point=m.get_center()))

        orbit_factor = 0.88
        orbit_ring = Circle(radius=earth7.width * orbit_factor).move_to(earth7.get_center())
        orbit_ring.set_fill(opacity=0)  # <-- CRITICAL: never fill
        orbit_ring.set_stroke(WHITE, width=2, opacity=0.0)  # start hidden via stroke opacity
        orbit_ring.set_z_index(6)
        orbit_ring.add_updater(lambda m: m.move_to(earth7.get_center()))
        self.add(orbit_ring)

        # orbital “slot” ticks (strokes only)
        num_slots = 30
        ticks = VGroup()
        ticks.set_z_index(7)

        tick_len_in = 0.05
        tick_len_out = 0.08

        def tick_points(k: int):
            ang = TAU * (k / num_slots)
            u = np.array([math.cos(ang), math.sin(ang), 0.0])
            r = earth7.width * orbit_factor
            c = earth7.get_center()
            start = c + u * (r - tick_len_in)
            end   = c + u * (r + tick_len_out)
            return start, end

        for k in range(num_slots):
            a, b = tick_points(k)
            t = Line(a, b).set_stroke(WHITE, width=3, opacity=0.0)  # start hidden
            ticks.add(t)

        def ticks_follow(_m, dt=0):
            for k, t in enumerate(ticks):
                a, b = tick_points(k)
                t.put_start_and_end_on(a, b)

        ticks.add_updater(lambda m, dt: ticks_follow(m, dt))
        self.add(ticks)

        # Fade in earth + orbit while caption reveals (NO set_opacity on orbit_ring!)
        self.play(
            self.caption_lagged_anim(groups7, lag=0.03),
            earth7.animate.set_opacity(1.0),
            orbit_ring.animate.set_stroke(opacity=0.12),
            LaggedStart(*[t.animate.set_stroke(opacity=0.14) for t in ticks], lag_ratio=0.02),
            run_time=1.15,
            rate_func=linear,
        )

        # Emphasize scarcity: ticks "fill"
        self.play(
            LaggedStart(*[t.animate.set_stroke(opacity=0.85) for t in ticks], lag_ratio=0.03),
            run_time=1.05,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        # -------------------------
        # Satellites: one-at-a-time launch from surface -> orbit -> then orbit continuously
        # -------------------------
        sat_count = 28  # “fill up” orbit
        sat_w = config.frame_width * 0.082
        r_surface = earth7.width * 0.50
        r_orbit   = earth7.width * orbit_factor

        angles = np.linspace(0.10, TAU + 0.10, sat_count, endpoint=False)
        angles = [a + random.uniform(-0.05, 0.05) for a in angles]
        random.shuffle(angles)

        satellites = Group()
        satellites.set_z_index(8)
        self.add(satellites)

        def make_sat(theta: float):
            s = ImageMobject("images/satellite.png")
            s.set_width(sat_w)
            s.theta = float(theta)
            s.omega = random.uniform(0.55, 0.95) * (1 if random.random() > 0.5 else -1)
            return s

        def sat_orbit_updater(mob, dt):
            mob.theta += mob.omega * dt
            c = earth7.get_center()
            u = np.array([math.cos(mob.theta), math.sin(mob.theta), 0.0])
            p = c + r_orbit * u
            mob.move_to(p)

            eps = 0.01
            u2 = np.array([math.cos(mob.theta + eps), math.sin(mob.theta + eps), 0.0])
            p2 = c + r_orbit * u2
            v = p2 - p
            if np.linalg.norm(v) > 1e-6:
                mob.set_angle(angle_of_vector(v))

        for i, th in enumerate(angles):
            s = make_sat(th)

            u = np.array([math.cos(th), math.sin(th), 0.0])
            start_pos = earth7.get_center() + r_surface * u
            end_pos   = earth7.get_center() + r_orbit * u

            s.move_to(start_pos)
            s.set_opacity(0.0)
            satellites.add(s)

            self.play(
                s.animate.set_opacity(0.95).move_to(end_pos),
                run_time=0.20,
                rate_func=rate_functions.ease_out_cubic,
            )

            s.add_updater(sat_orbit_updater)

            if i % 3 == 0:
                self.wait(0.03)

        self.wait(0.6)

        # =========================================================
        # SCENE 8: "Quiet revolution right above us"
        # Visual: shift-zoom Earth to center, remove orbit/satellites, fade-in glowing mesh network
        # =========================================================

        # --- Transition IN from Scene 7: remove orbit visuals + sats, zoom earth ---
        fade_group = Group()
        for mob in [orbit_ring, ticks, satellites]:
            try:
                fade_group.add(mob)
            except Exception:
                pass

        # stop orbiting sats so nothing weird persists
        try:
            satellites.clear_updaters()
        except Exception:
            pass

        # zoom earth up a bit and scale (tweak to taste)
        self.play(
            FadeOut(fade_group),
            FadeOut(caption7),
            earth7.animate.scale(1.55).move_to(0.55 * DOWN),
            run_time=0.9,
            rate_func=smooth,
        )
        self.remove(fade_group)

        # --- Caption ---
        caption8_text = "So while headlines focus on rockets to Mars, the quiet revolution is happening right above us."
        caption8, groups8 = self.make_caption(caption8_text, font_size=22, top_buff=0.55, add_to_scene=True)
        self.play(self.caption_lagged_anim(groups8, lag=0.03), run_time=1.2, rate_func=linear)

        # --- Build a connected-graph mesh that COVERS the Earth disk ---
        earth_center = earth7.get_center()

        # Use a slightly smaller radius than before (earth.png often has padding)
        R = earth7.width * 0.40

        # Denser graph
        N_NODES = 52
        K_NEIGHBORS = 4

        # Prevent long edges that create big “polygons”
        MAX_EDGE_LEN = R * 0.75

        golden_angle = PI * (3 - math.sqrt(5))

        # Sunflower spiral fill (uniform coverage over the disk)
        node_positions = []
        for i in range(N_NODES):
            rr = R * math.sqrt((i + 0.6) / N_NODES)
            th = i * golden_angle
            node_positions.append(
                earth_center + np.array([rr * math.cos(th), rr * math.sin(th), 0.0])
            )

        # Nodes (small, subtle)
        nodes = VGroup(*[
            Dot(p, radius=0.020, color=YELLOW).set_opacity(0.0)
            for p in node_positions
        ])

        # Edges: connect to nearby neighbors only (disk is convex, so segments stay in-disk)
        edges = VGroup()
        seen = set()

        for i, pi in enumerate(node_positions):
            dists = []
            for j, pj in enumerate(node_positions):
                if i == j:
                    continue
                d = np.linalg.norm(pj - pi)
                if d <= MAX_EDGE_LEN:
                    dists.append((d, j))
            dists.sort(key=lambda x: x[0])

            for _, j in dists[:K_NEIGHBORS]:
                a, b = (i, j) if i < j else (j, i)
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                e = Line(node_positions[a], node_positions[b])
                e.set_stroke(YELLOW, width=2, opacity=0.85)
                edges.add(e)

        # Add a few extra short edges for richness (still constrained)
        extra_edges = 24
        pairs = []
        for i in range(N_NODES):
            for j in range(i + 1, N_NODES):
                d = np.linalg.norm(node_positions[j] - node_positions[i])
                if d <= MAX_EDGE_LEN * 0.95:
                    pairs.append((d, i, j))
        pairs.sort(key=lambda x: x[0])
        random.shuffle(pairs)
        added = 0
        for _, i, j in pairs:
            if added >= extra_edges:
                break
            if (i, j) in seen:
                continue
            seen.add((i, j))
            e = Line(node_positions[i], node_positions[j]).set_stroke(YELLOW, width=2, opacity=0.65)
            edges.add(e)
            added += 1

        mesh = VGroup(edges, nodes)
        mesh.set_z_index(10)
        self.add(mesh)

        # Optional: keep mesh “painted on” the Earth as it rotates
        for n in nodes:
            n.set_opacity(0.0)

        for e in edges:
            # keep width/color, but start invisible
            e.set_stroke(YELLOW, width=2, opacity=0.0)

        mesh = VGroup(edges, nodes)
        mesh.set_z_index(10)
        self.add(mesh)

        # Optional: keep mesh “painted on” the Earth as it rotates
        mesh = VGroup(edges, nodes)
        mesh.set_z_index(10)

        # IMPORTANT: add it once, fully invisible so no “flash”
        for n in nodes:
            n.set_opacity(0.0)
        for e in edges:
            e.set_stroke(YELLOW, width=2, opacity=0.0)

        self.add(mesh)

        # Keep mesh “painted on” the Earth as it rotates
        EARTH_OMEGA = -0.10
        mesh.add_updater(lambda m, dt: m.rotate(EARTH_OMEGA * dt, about_point=earth7.get_center()))

        # --- Animate nodes first (they stay) ---
        self.play(
            LaggedStart(*[n.animate.set_opacity(1.0) for n in nodes], lag_ratio=0.03),
            run_time=0.7,
        )

        # --- Animate edges ONCE: draw + fade stroke opacity together ---
        edges_sorted = sorted(list(edges), key=lambda e: e.get_length())

        edge_anims = [
            AnimationGroup(
                Create(e),
                e.animate.set_stroke(opacity=0.85),
                lag_ratio=0.0,
            )
            for e in edges_sorted
        ]

        self.play(
            LaggedStart(*edge_anims, lag_ratio=0.02),
            run_time=2.2,
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.wait(0.5)