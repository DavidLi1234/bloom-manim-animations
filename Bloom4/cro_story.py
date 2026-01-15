from manim import *
import math

# Canvas and palette for a 9:16 vertical look
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#000000"  # black

NAVY = "#000000"
CYAN = "#5de6ff"
ORANGE = "#ff9f43"
SOFT_WHITE = "#f5f7fb"
MUTED = "#1e2f4e"
VISUAL_SHIFT = UP * 1.6
CAPTION_MAX_WIDTH = 6.4
CAPTION_APPEAR_TIME = 0.15
CAPTION_WRITE_TIME = 1.2
CAPTION_HOLD_TIME = 0.6
CAPTION_FADE_TIME = 0.15
CAPTION_SENTENCE_PAUSE = 0.9


def soft_glow(mob, color=CYAN, width=18, opacity=0.35):
    ring = mob.copy().set_stroke(color, width=width, opacity=opacity)
    ring.set_fill(opacity=0)
    return ring


def gear_icon(radius=0.6, teeth=8, color=SOFT_WHITE):
    base = Circle(radius=radius, stroke_width=2, stroke_color=color)
    spokes = VGroup()
    for i in range(teeth):
        angle = i * TAU / teeth
        tooth = Rectangle(height=0.18, width=0.08, stroke_width=0, fill_color=color, fill_opacity=1)
        tooth.move_to(base.point_at_angle(angle))
        tooth.rotate(angle, about_point=base.get_center())
        spokes.add(tooth)
    hole = Circle(radius=0.2, fill_color=NAVY, fill_opacity=1, stroke_width=0)
    gear = VGroup(base, spokes, hole)
    gear.set_color(color)
    return gear


def dna_helix(height=5, width=1.4, turns=3, color_a=CYAN, color_b=ORANGE):
    strands = VGroup()
    connectors = VGroup()
    for i, color in enumerate([color_a, color_b]):
        strand = VMobject(stroke_color=color, stroke_width=3)
        points = []
        for t in np.linspace(0, TAU * turns, 80):
            x = ((-1) ** i) * math.sin(t) * width * 0.5
            y = (t / (TAU * turns) - 0.5) * height
            z = 0
            points.append([x, y, z])
        strand.set_points_smoothly(points)
        strands.add(strand)
    for t in np.linspace(0, TAU * turns, 14):
        x = math.sin(t) * width * 0.5
        y = (t / (TAU * turns) - 0.5) * height
        bar = Line([x, y, 0], [-x, y, 0], stroke_width=2, stroke_color=SOFT_WHITE)
        bar.set_opacity(0.65)
        connectors.add(bar)
    return VGroup(strands, connectors)


def patient_icon(color=SOFT_WHITE, scale=1.0, outline_only=True):
    head = Circle(radius=0.18 * scale, stroke_color=color, stroke_width=3, fill_opacity=0 if outline_only else 1)
    body = RoundedRectangle(height=0.7 * scale, width=0.35 * scale, corner_radius=0.12 * scale,
                            stroke_color=color, stroke_width=3, fill_opacity=0 if outline_only else 1)
    body.next_to(head, DOWN, buff=0.08 * scale)
    return VGroup(head, body)


class CROStory(Scene):
    def sentence_pause(self, chunk):
        return CAPTION_SENTENCE_PAUSE if chunk.rstrip().endswith((".", "!", "?")) else 0.0

    def split_caption(self, text, max_words=5):
        words = text.split()
        chunks = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
        if len(chunks) > 1 and len(chunks[-1].split()) == 1:
            last_word = chunks[-1]
            prev_words = chunks[-2].split()
            chunks[-2] = " ".join(prev_words[:-1])
            chunks[-1] = f"{prev_words[-1]} {last_word}".strip()
        return [c for c in chunks if c]

    def format_caption_text(self, text, max_width=CAPTION_MAX_WIDTH):
        base = Text(text, color=SOFT_WHITE).scale(0.6)
        if base.width <= max_width or " " not in text:
            return text
        words = text.split()
        best = text
        best_width = base.width
        for i in range(1, len(words)):
            # avoid single-word lines
            if i == 1 or i == len(words) - 1:
                continue
            candidate = " ".join(words[:i]) + "\n" + " ".join(words[i:])
            t = Text(candidate, color=SOFT_WHITE).scale(0.6)
            if t.width < best_width:
                best_width = t.width
                best = candidate
            if best_width <= max_width:
                break
        return best

    def make_caption(self, text):
        formatted = self.format_caption_text(text)
        caption = Text(formatted, color=SOFT_WHITE, line_spacing=0.8).scale(0.6)
        box = RoundedRectangle(
            width=max(caption.width + 0.6, 6),
            height=caption.height + 0.45,
            corner_radius=0.2,
            stroke_width=0,
            fill_color="#000000",
            fill_opacity=0.0,
        )
        group = VGroup(box, caption)
        group.move_to(DOWN * 2.6)  # shift captions slightly downward
        caption.move_to(box.get_center())
        return group

    def caption_animation(self, text):
        anims = []
        prev_cap = None
        for chunk in self.split_caption(text, max_words=5):
            cap = self.make_caption(chunk)
            extra_pause = self.sentence_pause(chunk)
            if prev_cap is not None:
                anims.append(FadeOut(prev_cap, run_time=CAPTION_FADE_TIME))
            anims.append(AnimationGroup(
                FadeIn(cap[0], shift=UP * 0.1, run_time=CAPTION_APPEAR_TIME),
                Write(cap[1], run_time=CAPTION_WRITE_TIME),
                lag_ratio=0.0,
            ))
            anims.append(Wait(CAPTION_HOLD_TIME + extra_pause))
            prev_cap = cap
        if prev_cap is not None:
            anims.append(FadeOut(prev_cap, run_time=CAPTION_FADE_TIME))
        return Succession(*anims, group=VGroup())

    def play_with_caption(self, visual_anim, text):
        chunks = self.split_caption(text, max_words=5)
        caption_total = 0.0
        for chunk in chunks:
            caption_total += (
                max(CAPTION_APPEAR_TIME, CAPTION_WRITE_TIME)
                + CAPTION_HOLD_TIME
                + self.sentence_pause(chunk)
                + CAPTION_FADE_TIME
            )
        visual_anim.set_run_time(caption_total)
        # Prevent Manim from pre-adding all visual mobjects at time 0
        visual_anim = Succession(visual_anim, group=VGroup())
        caption_anim = self.caption_animation(text)
        self.play(visual_anim, caption_anim)
        self.clear()

    def construct(self):
        self.camera.background_color = NAVY
        self.section_one()
        self.section_two()
        self.section_three()
        self.section_four()
        self.section_five()
        self.section_six()
        self.section_seven()
        self.section_eight()
        self.section_nine()
        self.section_ten()
        self.section_eleven()
        self.section_twelve()

    # 1. Pill + pharma struggles
    def section_one(self):
        pill = RoundedRectangle(width=4.8, height=2.2, corner_radius=1.1,
                                stroke_color=CYAN, stroke_width=6)
        factory = VGroup(
            Rectangle(height=0.6, width=1.8, stroke_width=0, fill_color=MUTED, fill_opacity=1),
            Rectangle(height=0.9, width=0.5, stroke_width=0, fill_color=MUTED, fill_opacity=1).shift(LEFT * 0.7 + UP * 0.15),
            Rectangle(height=0.9, width=0.5, stroke_width=0, fill_color=MUTED, fill_opacity=1).shift(RIGHT * 0.7 + UP * 0.15),
        )
        chimneys = VGroup(
            Rectangle(height=0.6, width=0.12, stroke_width=0, fill_color=SOFT_WHITE, fill_opacity=0.8).shift(LEFT * 0.8 + UP * 0.6),
            Rectangle(height=0.6, width=0.12, stroke_width=0, fill_color=SOFT_WHITE, fill_opacity=0.8).shift(RIGHT * 0.8 + UP * 0.6),
        )
        factory.add(chimneys)
        factory.move_to(pill.get_center())

        label = Text("Years • Billions • Risk", color=SOFT_WHITE, weight=MEDIUM).scale(0.35)
        label.next_to(pill, DOWN, buff=0.1)

        glow = soft_glow(pill)
        VGroup(pill, factory, label, glow).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            AnimationGroup(Create(pill), FadeIn(glow, run_time=0.6)),
            AnimationGroup(FadeIn(factory, shift=UP * 0.2, run_time=0.8), FadeIn(label, shift=DOWN * 0.1, run_time=0.6)),
            AnimationGroup(glow.animate.set_opacity(0.1), rate_func=there_and_back, run_time=1.2),
            AnimationGroup(pill.animate.scale(0.8), factory.animate.scale(0.8), run_time=0.7),
            Wait(0.4),
            FadeOut(VGroup(pill, factory, glow, label)),
        )
        self.play_with_caption(
            visual_anim,
            "One of the biggest beneficiaries of the new drug development isn't pharmaceutical companies themselves.",
        )

    # 2. Long timelines + cost curve
    def section_two(self):
        line = Line(LEFT * 3.5, RIGHT * 3.5, stroke_color=SOFT_WHITE, stroke_width=3)
        ticks = VGroup()
        labels = ["Phase I", "Phase II", "Phase III", "FDA"]
        for i, t in enumerate(labels):
            pos = LEFT * 3 + RIGHT * (i * 2.2)
            dot = Dot(pos, color=CYAN, radius=0.06)
            lab = Text(t, color=SOFT_WHITE).scale(0.35)
            lab.next_to(dot, DOWN, buff=0.12)
            ticks.add(VGroup(dot, lab))

        dollar = Text("$", color=ORANGE).scale(1.3)
        curve = ParametricFunction(lambda u: np.array([u * 3.5 - 3.5, 0.8 * (u ** 2), 0]), t_range=[0, 1])

        capacity = RoundedRectangle(width=1.9, height=0.6, corner_radius=0.2,
                                    stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.1)
        cap_label = Text("Limited capacity", color=ORANGE).scale(0.35)
        cap_label.move_to(capacity.get_center())
        capacity_group = VGroup(capacity, cap_label).move_to(RIGHT * 3.1 + UP * 1.2)
        VGroup(line, ticks, curve, dollar, capacity_group).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            AnimationGroup(Create(line), FadeIn(ticks, lag_ratio=0.1, run_time=1.0)),
            MoveAlongPath(dollar, curve, run_time=1.0),
            FadeIn(capacity_group, scale=0.8, run_time=0.6),
            Wait(0.4),
            FadeOut(VGroup(line, ticks, dollar, capacity_group)),
        )
        self.play_with_caption(
            visual_anim,
            "It takes years to test and billions of dollars to bring to market — far more work than most biotech firms can handle alone.",
        )

    # 3. CRO hub with inflows
    def section_three(self):
        box = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.3,
                               stroke_color=CYAN, stroke_width=4, fill_opacity=0.05, fill_color=CYAN)
        cro_text = Text("CRO", color=SOFT_WHITE, weight=BOLD).scale(0.6)
        cro_text.next_to(box, UP, buff=0.15)
        cro_group = VGroup(box, cro_text)

        pharma_nodes = VGroup()
        for i in range(3):
            node = VGroup(
                Circle(radius=0.45, stroke_color=SOFT_WHITE, stroke_width=2, fill_opacity=0.08, fill_color=SOFT_WHITE),
                Text("Pharma", color=SOFT_WHITE).scale(0.32)
            ).arrange(DOWN, buff=0.1)
            node.shift(LEFT * 3.2 + UP * (1.4 - i * 1.4))
            pharma_nodes.add(node)

        arrows = VGroup()
        for n in pharma_nodes:
            arr = Arrow(n.get_right(), box.get_left(), stroke_color=CYAN, buff=0.25, max_tip_length_to_length_ratio=0.12)
            arrows.add(arr)

        labels = [
            ("Design studies", UP * 0.6, "📋"),
            ("Enroll patients", ORIGIN, "👥"),
            ("Analyze results", DOWN * 0.6, "📈"),
        ]
        label_group = VGroup()
        for text, pos, emoji in labels:
            line = Text(f"{emoji} {text}", color=SOFT_WHITE).scale(0.34)
            line.move_to(box.get_center() + pos)
            label_group.add(line)

        VGroup(cro_group, pharma_nodes, arrows, label_group).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            AnimationGroup(FadeIn(cro_group, scale=0.9), FadeIn(pharma_nodes, lag_ratio=0.1)),
            Create(arrows, lag_ratio=0.1, run_time=0.8),
            FadeIn(label_group, lag_ratio=0.1, run_time=0.8),
            Wait(0.4),
            FadeOut(VGroup(cro_group, pharma_nodes, arrows, label_group)),
        )
        self.play_with_caption(
            visual_anim,
            "So companies are turning to contract research organizations — CROs — who design studies, enroll patients, and analyze results.",
        )

    # 4. Market growth line
    def section_four(self):
        path = VMobject(stroke_color=CYAN, stroke_width=6)
        points = [
            [-3.2, -2.2, 0],
            [-1.5, -1.0, 0],
            [0.2, -0.5, 0],
            [2.2, 1.2, 0],
            [3.2, 2.3, 0],
        ]
        path.set_points_smoothly(points)
        glow = soft_glow(path, color=CYAN, width=20, opacity=0.25)
        label = Text("$138B (2031)", color=ORANGE, weight=BOLD).scale(0.45)
        label.next_to(path.get_end(), UP, buff=0.2)

        dna_bg = dna_helix(height=6, width=1.3, turns=2, color_a=MUTED, color_b=MUTED)
        dna_bg.set_opacity(0.15)
        dna_bg.shift(RIGHT * 1.5)
        VGroup(path, glow, label, dna_bg).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            FadeIn(dna_bg, run_time=0.8),
            AnimationGroup(Create(path), FadeIn(glow, run_time=0.5)),
            Write(label, run_time=0.5),
            path.animate.set_stroke(width=10).set_run_time(0.6),
            Wait(0.4),
            FadeOut(VGroup(path, glow, label, dna_bg)),
        )
        self.play_with_caption(
            visual_anim,
            "The CRO market is expected to reach nearly $138 billion by 2031 as drug pipelines expand and trials become more complex.",
        )

    # 5. Gears evolving
    def section_five(self):
        center = gear_icon()
        left = gear_icon(radius=0.45, teeth=7, color=MUTED).shift(LEFT * 1.6)
        right = gear_icon(radius=0.4, teeth=6, color=MUTED).shift(RIGHT * 1.6)
        top = gear_icon(radius=0.35, teeth=6, color=MUTED).shift(UP * 1.4)
        gears = VGroup(center, left, right, top)
        gears.shift(VISUAL_SHIFT)

        visual_anim = Succession(
            FadeIn(gears, lag_ratio=0.1),
            Rotate(gears, angle=TAU / 6, run_time=1.2),
            AnimationGroup(
                center.animate.set_color(CYAN),
                left.animate.set_opacity(0.25),
                right.animate.set_opacity(0.25),
                top.animate.set_opacity(0.25),
            ),
            Wait(0.4),
            FadeOut(VGroup(gears)),
        )
        self.play_with_caption(
            visual_anim,
            "More complexity means CROs need to evolve — those that do are poised for the most growth.",
        )

    # 6. Precision medicine DNA
    def section_six(self):
        dna = dna_helix(height=7, width=1.1, turns=3)
        markers = VGroup()
        for y in np.linspace(-3, 3, 6):
            mark = Dot([0, y, 0], color=ORANGE, radius=0.07)
            glow = soft_glow(mark, color=ORANGE, width=10, opacity=0.2)
            markers.add(VGroup(mark, glow))

        text = Text("Precision Medicine", color=SOFT_WHITE, weight=SEMIBOLD).scale(0.5)
        text.shift(DOWN * 3.4)
        VGroup(dna, markers, text).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            AnimationGroup(Create(dna[0]), Create(dna[1]), run_time=1.0),
            FadeIn(markers, lag_ratio=0.1, run_time=0.8),
            Write(text, run_time=0.5),
            Wait(0.4),
            FadeOut(VGroup(dna, markers, text)),
        )
        self.play_with_caption(
            visual_anim,
            "The best CROs will be able to work with precision medicine.",
        )

    # 7. Targeted groups + matching network
    def section_seven(self):
        dna = dna_helix(height=5, width=1.0, turns=2, color_a=MUTED, color_b=MUTED)
        dna.scale(0.9)
        patients = VGroup()
        tags = VGroup()
        positions = [LEFT * 3 + UP * 1.2, LEFT * 3, LEFT * 3 + DOWN * 1.2]
        colors = [CYAN, ORANGE, SOFT_WHITE]
        for pos, col in zip(positions, colors):
            p = patient_icon(color=col)
            p.move_to(pos)
            tag = RoundedRectangle(width=1.1, height=0.35, corner_radius=0.15,
                                   stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.12)
            label = Text("Biomarker", color=col).scale(0.3)
            label.move_to(tag.get_center())
            tag.next_to(p, RIGHT, buff=0.3)
            patients.add(p)
            tags.add(VGroup(tag, label))

        nodes = VGroup(Text("Gene", color=SOFT_WHITE).scale(0.35),
                       Text("Trial", color=SOFT_WHITE).scale(0.35),
                       Text("Patient", color=SOFT_WHITE).scale(0.35))
        nodes.arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)

        links = VGroup(
            Line(nodes[0].get_right(), nodes[1].get_left(), stroke_color=CYAN, stroke_width=3),
            Line(nodes[1].get_right(), nodes[2].get_left(), stroke_color=ORANGE, stroke_width=3),
        )

        VGroup(dna, patients, tags, nodes, links).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            FadeIn(dna),
            AnimationGroup(FadeIn(patients, lag_ratio=0.1), FadeIn(tags, lag_ratio=0.1)),
            AnimationGroup(FadeIn(nodes), Create(links)),
            Wait(0.5),
            FadeOut(VGroup(dna, patients, tags, nodes, links)),
        )
        self.play_with_caption(
            visual_anim,
            "Breakthroughs in sequencing and gene therapies demand trials built around DNA, biomarkers, and highly targeted patient groups.",
        )

    # 8. Enrollment bottleneck
    def section_eight(self):
        silhouettes = VGroup()
        for i in range(7):
            icon = patient_icon(color="#6b6f7a", outline_only=True)
            icon.scale(0.7)
            icon.shift(LEFT * 2.2 + RIGHT * (i * 0.75))
            silhouettes.add(icon)

        fail_counter = DecimalNumber(0, num_decimal_places=0, color=ORANGE, mob_class=Text).scale(0.9)
        fail_label = Text("% fail", color=SOFT_WHITE).scale(0.35)
        fail_group = VGroup(fail_counter, fail_label).arrange(DOWN, buff=0.1).to_corner(UL, buff=0.6)

        demand_counter = DecimalNumber(1, num_decimal_places=1, color=CYAN, mob_class=Text).scale(0.8)
        demand_label = Text("Demand x", color=SOFT_WHITE).scale(0.35)
        year_label = Text("by 2032", color=SOFT_WHITE).scale(0.32)
        demand_group = VGroup(demand_label, demand_counter, year_label).arrange(DOWN, buff=0.05).to_corner(UR, buff=0.6)

        VGroup(silhouettes, fail_group, demand_group).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            FadeIn(silhouettes, lag_ratio=0.05),
            LaggedStart(*[icon.animate.set_color(CYAN).set_run_time(0.25) for icon in silhouettes[:4]], lag_ratio=0.1),
            fail_counter.animate.set_value(70).set_run_time(0.9),
            demand_counter.animate.set_value(3.0).set_run_time(0.9),
            AnimationGroup(
                silhouettes[:4].animate.set_opacity(0.9),
                silhouettes[4:].animate.set_opacity(0.45),
                run_time=0.6,
            ),
            Wait(0.3),
            FadeOut(VGroup(silhouettes, fail_group, demand_group)),
        )
        self.play_with_caption(
            visual_anim,
            "Critical bottleneck: after COVID, 70% of trials fail to enroll enough patients while demand for patients will triple by 2032.",
        )

    # 9. Patient-centric decentralized map
    def section_nine(self):
        map_box = RoundedRectangle(width=5.5, height=3.6, corner_radius=0.4,
                                   stroke_color=MUTED, stroke_width=2, fill_color=MUTED, fill_opacity=0.2)
        hub = Circle(radius=0.25, color=CYAN, fill_opacity=1, stroke_width=0).shift(DOWN * 0.3)
        nodes = VGroup()
        for pos in [LEFT * 2 + UP * 1, RIGHT * 2 + UP * 0.6, LEFT * 1.5 + DOWN * 1.2, RIGHT * 1.8 + DOWN * 0.8, UP * 1.4]:
            dot = Dot(pos, color=SOFT_WHITE, radius=0.08)
            nodes.add(dot)
        links = VGroup(*[Line(hub.get_center(), n.get_center(), stroke_color=CYAN, stroke_width=2) for n in nodes])
        links.set_opacity(0.7)

        icons = VGroup(
            Text("📱✔", color=SOFT_WHITE).scale(0.5).next_to(map_box, DOWN, buff=0.2).shift(LEFT * 1.5),
            Text("🏠🧪", color=SOFT_WHITE).scale(0.5).next_to(map_box, DOWN, buff=0.2),
            Text("💻📹", color=SOFT_WHITE).scale(0.5).next_to(map_box, DOWN, buff=0.2).shift(RIGHT * 1.5),
        )

        hospital = Text("🏥").scale(0.7).next_to(map_box, UP, buff=0.2).set_opacity(0.6)
        VGroup(map_box, hub, nodes, links, icons, hospital).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            FadeIn(map_box),
            AnimationGroup(FadeIn(nodes, lag_ratio=0.05), FadeIn(hub)),
            Create(links, lag_ratio=0.1, run_time=0.8),
            AnimationGroup(FadeIn(icons, lag_ratio=0.1), FadeIn(hospital)),
            hospital.animate.set_opacity(0.2),
            Wait(0.4),
            FadeOut(VGroup(map_box, nodes, links, hub, icons, hospital)),
        )
        self.play_with_caption(
            visual_anim,
            "Remote consent, mobile sampling, and virtual check-ins proved trials don’t need to stay tied to hospitals — patient-centric designs unlock value.",
        )

    # 10. AI mesh with CRO core
    def section_ten(self):
        nodes = VGroup()
        edges = VGroup()
        cols, rows = 8, 6
        for i in range(cols):
            for j in range(rows):
                x = -3.2 + i * (6.4 / (cols - 1))
                y = -2.2 + j * (4.4 / (rows - 1))
                jitter = np.array([np.random.uniform(-0.18, 0.18), np.random.uniform(-0.18, 0.18), 0])
                pos = np.array([x, y, 0]) + jitter
                node = Dot(pos, radius=0.035, color=SOFT_WHITE)
                nodes.add(node)

        for i, a in enumerate(nodes):
            for j, b in enumerate(nodes):
                if j <= i:
                    continue
                if np.linalg.norm(a.get_center() - b.get_center()) < 1.4:
                    edges.add(Line(a.get_center(), b.get_center(), stroke_color=SOFT_WHITE, stroke_width=1))

        edges.set_opacity(0.45)
        nodes.set_opacity(0.9)

        cro_label = Text("CRO", color=SOFT_WHITE, weight=BOLD).scale(0.55)
        cro_label.next_to(nodes.get_top(), UP, buff=0.35)

        VGroup(edges, nodes, cro_label).shift(VISUAL_SHIFT)

        # Animate left-to-right reveal
        x_min = min(n.get_center()[0] for n in nodes)
        x_max = max(n.get_center()[0] for n in nodes)
        buckets = 6
        span = max(x_max - x_min, 1e-6)
        node_buckets = [VGroup() for _ in range(buckets)]
        edge_buckets = [VGroup() for _ in range(buckets)]

        for n in list(nodes):
            idx = int((n.get_center()[0] - x_min) / span * buckets)
            idx = min(max(idx, 0), buckets - 1)
            node_buckets[idx].add(n)

        for e in list(edges):
            edge_x = max(e.get_start()[0], e.get_end()[0])
            idx = int((edge_x - x_min) / span * buckets)
            idx = min(max(idx, 0), buckets - 1)
            edge_buckets[idx].add(e)

        anims = []
        for k in range(buckets):
            anims.append(AnimationGroup(
                FadeIn(node_buckets[k], run_time=0.25),
                Create(edge_buckets[k], run_time=0.35),
                lag_ratio=0.1,
            ))

        visual_anim = Succession(
            LaggedStart(*anims, lag_ratio=0.2),
            FadeIn(cro_label, scale=0.9),
            Wait(0.4),
            FadeOut(VGroup(edges, nodes, cro_label)),
        )
        self.play_with_caption(
            visual_anim,
            "AI may prove the ultimate lever — automation flows into the CRO core.",
        )

    # 11. Automation value shift
    def section_eleven(self):
        divider = Line(UP * 3.5, DOWN * 3.5, stroke_color=MUTED, stroke_width=2)
        manual_stack = VGroup(
            Text("📄 Paper", color=SOFT_WHITE).scale(0.4),
            Text("📊 Charts", color=SOFT_WHITE).scale(0.4),
            Text("🗄 Archive", color=SOFT_WHITE).scale(0.4),
        ).arrange(DOWN, buff=0.2).shift(LEFT * 2.2)

        ai_stack = VGroup(
            Text("✨ Spark", color=SOFT_WHITE).scale(0.4),
            Text("💻 AI", color=SOFT_WHITE).scale(0.4),
            Text("🧬 DNA", color=SOFT_WHITE).scale(0.4),
            Text("📈 Insights", color=SOFT_WHITE).scale(0.4),
        ).arrange(DOWN, buff=0.18).shift(RIGHT * 2.2)

        money = Text("$18B", color=ORANGE, weight=BOLD).scale(0.8)
        money.shift(LEFT * 1.2)
        VGroup(divider, manual_stack, ai_stack, money).shift(VISUAL_SHIFT)

        visual_anim = Succession(
            Create(divider),
            AnimationGroup(FadeIn(manual_stack, lag_ratio=0.1), FadeIn(ai_stack, lag_ratio=0.1)),
            money.animate.shift(RIGHT * 2.4).set_run_time(0.9),
            Wait(0.3),
            FadeOut(VGroup(divider, manual_stack, ai_stack, money)),
        )
        self.play_with_caption(
            visual_anim,
            "Up to $18B of CRO work could shift to automation — from reports to genetic insights.",
        )

    # 12. Future mesh + CRO center
    def section_twelve(self):
        dna = dna_helix(height=8, width=1.2, turns=3, color_a=MUTED, color_b=MUTED).scale(0.9)
        patients = VGroup()
        for pos in [LEFT * 3 + UP * 2, RIGHT * 3 + UP * 1.5, LEFT * 3 + DOWN * 1.5, RIGHT * 3 + DOWN * 2]:
            p = patient_icon(color=SOFT_WHITE, outline_only=False)
            p.scale(0.9)
            p.shift(pos)
            patients.add(p)
        flows = VGroup(*[Line(p.get_center(), ORIGIN, stroke_color=CYAN, stroke_width=2) for p in patients])
        flows.set_opacity(0.6)
        cro = Circle(radius=0.45, color=CYAN, stroke_width=4, fill_color=CYAN, fill_opacity=0.18)
        cro_label = Text("CRO", color=SOFT_WHITE, weight=BOLD).scale(0.5)
        cro_label.move_to(cro.get_center())
        cro_group = VGroup(cro, cro_label)

        mesh_lines = VGroup()
        for angle in np.linspace(0, TAU, 10):
            line = Line(ORIGIN + np.array([math.cos(angle), math.sin(angle), 0]) * 0.5,
                        ORIGIN + np.array([math.cos(angle), math.sin(angle), 0]) * 4.5,
                        stroke_color=MUTED, stroke_width=1)
            line.set_opacity(0.4)
            mesh_lines.add(line)
        rings = VGroup(*[Circle(radius=r, color=MUTED, stroke_width=1) for r in np.linspace(1, 4.5, 5)])
        rings.set_opacity(0.4)
        VGroup(mesh_lines, rings, dna, patients, flows, cro_group).shift(VISUAL_SHIFT)

        pulse = cro.animate.set_stroke_width(8).set_fill(opacity=0.3)
        pulse.set_run_time(1.0)
        pulse.set_rate_func(there_and_back)

        visual_anim = Succession(
            FadeIn(mesh_lines, rings, dna, run_time=1.0),
            AnimationGroup(FadeIn(patients, lag_ratio=0.1), Create(flows)),
            FadeIn(cro_group),
            pulse,
            Wait(0.6),
            AnimationGroup(
                *[FadeOut(mob) for mob in [mesh_lines, rings, dna, patients, flows]],
                cro_group.animate.scale(1.2),
                run_time=0.8,
            ),
            Wait(0.4),
        )
        self.play_with_caption(
            visual_anim,
            "The future of medicine is limitless — CROs that evolve sit at the center of the story.",
        )
