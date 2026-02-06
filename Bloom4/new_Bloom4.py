from __future__ import annotations

import textwrap
import math
import numpy as np
from manim import *


BACKGROUND_COLOR = "#0b0b0b"
PRIMARY_COLOR = "#f5f5f5"
ACCENT_COLOR = "#4ec9f5"
SECONDARY_COLOR = "#a0a0a0"
HIGHLIGHT_COLOR = "#ffb84d"


def wrap_lines(text: str, width: int = 48) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False)


def make_sentence(text: str, font_size: int = 34) -> Paragraph:
    lines = wrap_lines(text, width=42)  # Reduced width to ensure better wrapping
    sentence = Paragraph(*lines, alignment="center", font_size=font_size, color=PRIMARY_COLOR)
    sentence.to_edge(UP, buff=0.5)
    # Ensure the paragraph fits within frame width (default is 14.2 units)
    if sentence.width > 13.0:
        scale_factor = 13.0 / sentence.width
        sentence.scale(scale_factor)
    return sentence


def dna_helix(height=5, width=1.4, turns=3, color_a=ACCENT_COLOR, color_b=HIGHLIGHT_COLOR, stroke_width=4) -> VGroup:
    strands = VGroup()
    connectors = VGroup()
    for i, color in enumerate([color_a, color_b]):
        strand = VMobject(stroke_color=color, stroke_width=stroke_width)
        points = []
        for t in np.linspace(0, TAU * turns, 80):
            x = ((-1) ** i) * math.sin(t) * width * 0.5
            y = (t / (TAU * turns) - 0.5) * height
            points.append([x, y, 0])
        strand.set_points_smoothly(points)
        strands.add(strand)
    for t in np.linspace(0, TAU * turns, 14):
        x = math.sin(t) * width * 0.5
        y = (t / (TAU * turns) - 0.5) * height
        bar = Line([x, y, 0], [-x, y, 0], stroke_width=max(2, stroke_width - 1), stroke_color=PRIMARY_COLOR)
        bar.set_opacity(0.65)
        connectors.add(bar)
    return VGroup(strands, connectors)


def make_capsule(color: str = ACCENT_COLOR) -> VGroup:
    radius = 0.35
    left = Circle(radius=radius)
    right = Circle(radius=radius)
    rect = Rectangle(width=radius * 2, height=radius * 2)
    parts = VGroup(left, rect, right).arrange(RIGHT, buff=0)
    parts.set_fill(color, opacity=1.0)
    parts.set_stroke(color, width=0)
    return parts


def make_clipboard(color: str = PRIMARY_COLOR) -> VGroup:
    board = RoundedRectangle(width=1.6, height=2.1, corner_radius=0.1)
    clip = RoundedRectangle(width=0.6, height=0.25, corner_radius=0.08)
    clip.move_to(board.get_top() + DOWN * 0.1)
    line_1 = Line(board.get_top() + DOWN * 0.6, board.get_top() + DOWN * 0.6 + RIGHT * 0.9)
    line_2 = Line(board.get_top() + DOWN * 0.9, board.get_top() + DOWN * 0.9 + RIGHT * 0.9)
    lines = VGroup(line_1, line_2).set_stroke(color, width=2)
    lines.shift(LEFT * 0.35)
    clipboard = VGroup(board, clip, lines)
    clipboard.set_stroke(color, width=2)
    clipboard.set_fill(opacity=0)
    return clipboard


def make_chain_link(color: str = PRIMARY_COLOR) -> VGroup:
    left = Circle(radius=0.18).shift(LEFT * 0.12)
    right = Circle(radius=0.18).shift(RIGHT * 0.12)
    link = VGroup(left, right)
    link.set_stroke(color, width=2)
    link.set_fill(opacity=0)
    return link


def make_flask(color: str = PRIMARY_COLOR) -> VGroup:
    # Flask outline
    neck = RoundedRectangle(width=0.6, height=1.4, corner_radius=0.2)
    neck.shift(UP * 0.7)
    shoulder_left = Line(neck.get_bottom() + LEFT * 0.25, LEFT * 1.2 + DOWN * 1.2)
    shoulder_right = Line(neck.get_bottom() + RIGHT * 0.25, RIGHT * 1.2 + DOWN * 1.2)
    base = Line(LEFT * 1.2 + DOWN * 1.2, RIGHT * 1.2 + DOWN * 1.2)
    outline = VGroup(neck, shoulder_left, shoulder_right, base)
    outline.set_stroke(color, width=4)
    outline.set_fill(opacity=0)

    # White fill for non-liquid portion (neck and upper part of flask)
    neck_fill = RoundedRectangle(width=0.6, height=1.4, corner_radius=0.2)
    neck_fill.shift(UP * 0.7)
    neck_fill.set_fill(WHITE, opacity=1.0)
    neck_fill.set_stroke(width=0)
    
    # Upper conical part fill (above liquid)
    upper_fill = Polygon(
        neck.get_bottom() + LEFT * 0.25,
        neck.get_bottom() + RIGHT * 0.25,
        RIGHT * 0.6 + DOWN * 0.4,
        LEFT * 0.6 + DOWN * 0.4,
    )
    upper_fill.set_fill(WHITE, opacity=1.0)
    upper_fill.set_stroke(width=0)
    
    flask_fill = VGroup(neck_fill, upper_fill)

    # Liquid in the bottom third
    liquid = Polygon(
        LEFT * 0.9 + DOWN * 1.05,
        RIGHT * 0.9 + DOWN * 1.05,
        RIGHT * 0.6 + DOWN * 0.4,
        LEFT * 0.6 + DOWN * 0.4,
    )
    liquid.set_fill("#3da5ff", opacity=0.85)
    liquid.set_stroke(width=0)

    # Bubbles in liquid
    bubbles = VGroup(
        Circle(radius=0.08, color=WHITE).move_to(LEFT * 0.3 + DOWN * 0.7),
        Circle(radius=0.06, color=WHITE).move_to(RIGHT * 0.2 + DOWN * 0.8),
    )
    bubbles.set_fill(WHITE, opacity=1.0)
    bubbles.set_stroke(width=0)

    # Tick marks on neck (black)
    ticks = VGroup(
        Line(RIGHT * 0.3 + UP * 0.5, RIGHT * 0.5 + UP * 0.5),
        Line(RIGHT * 0.3 + UP * 0.2, RIGHT * 0.5 + UP * 0.2),
    )
    ticks.set_stroke(BLACK, width=3)

    # Plus sign near top
    plus = VGroup(
        Line(UP * 0.1, DOWN * 0.1),
        Line(LEFT * 0.1, RIGHT * 0.1),
    )
    plus.move_to(neck.get_top() + DOWN * 0.15)
    plus.set_stroke(WHITE, width=3)

    return VGroup(flask_fill, outline, liquid, bubbles, ticks, plus)


def make_dna(color: str = ACCENT_COLOR) -> VGroup:
    curve_a = ParametricFunction(
        lambda t: np.array([0.25 * np.sin(t), 0.3 * t, 0.0]),
        t_range=[-PI, PI],
    )
    curve_b = ParametricFunction(
        lambda t: np.array([0.25 * np.sin(t + PI), 0.3 * t, 0.0]),
        t_range=[-PI, PI],
    )
    dna = VGroup(curve_a, curve_b)
    dna.set_stroke(color, width=2.2)
    return dna


def make_target(color: str = PRIMARY_COLOR) -> VGroup:
    outer = Circle(radius=0.32)
    inner = Circle(radius=0.16)
    cross_h = Line(LEFT * 0.4, RIGHT * 0.4)
    cross_v = Line(UP * 0.4, DOWN * 0.4)
    target = VGroup(outer, inner, cross_h, cross_v)
    target.set_stroke(color, width=2)
    target.set_fill(opacity=0)
    return target


def make_biomarker_chart(color: str = PRIMARY_COLOR) -> VGroup:
    axis_x = Line(LEFT * 0.4, RIGHT * 0.4)
    axis_y = Line(DOWN * 0.4, UP * 0.4)
    axis = VGroup(axis_x, axis_y).set_stroke(color, width=2)
    dot = Dot(point=RIGHT * 0.2 + UP * 0.2, radius=0.06, color=HIGHLIGHT_COLOR)
    return VGroup(axis, dot)


def make_phone(color: str = PRIMARY_COLOR) -> VGroup:
    body = RoundedRectangle(width=0.6, height=1.1, corner_radius=0.08)
    button = Circle(radius=0.04).move_to(body.get_bottom() + UP * 0.12)
    phone = VGroup(body, button)
    phone.set_stroke(color, width=2)
    phone.set_fill(opacity=0)
    return phone


def make_signal_waves(color: str = PRIMARY_COLOR) -> VGroup:
    wave1 = Arc(radius=0.2, start_angle=-PI / 3, angle=PI / 1.5)
    wave2 = Arc(radius=0.32, start_angle=-PI / 3, angle=PI / 1.5)
    wave3 = Arc(radius=0.44, start_angle=-PI / 3, angle=PI / 1.5)
    waves = VGroup(wave1, wave2, wave3)
    waves.set_stroke(color, width=2)
    return waves


def make_gear(color: str = PRIMARY_COLOR) -> VGroup:
    core = Circle(radius=0.22)
    teeth = VGroup(
        *[
            Rectangle(width=0.08, height=0.18).shift(UP * 0.32).rotate(i * PI / 4)
            for i in range(8)
        ]
    )
    gear = VGroup(core, teeth)
    gear.set_stroke(color, width=2)
    gear.set_fill(opacity=0)
    return gear


def make_house(color: str = PRIMARY_COLOR) -> VGroup:
    base = Square(side_length=0.3)
    roof = Polygon(LEFT * 0.18, RIGHT * 0.18, UP * 0.18).shift(UP * 0.18)
    house = VGroup(base, roof)
    house.set_stroke(color, width=2)
    house.set_fill(opacity=0)
    return house


class BaseBloomScene(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR

    def fade_out_all(self, run_time: float = 0.6) -> None:
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=run_time)


class TitleScene(BaseBloomScene):
    def construct(self):
        total_time = 3.0
        used = 0.0

        title = make_sentence("Pharma's Future Rests with Contract Research Organizations", font_size=46)

        # Load pill image
        pill = ImageMobject("pill.png")
        pill.height = 2.5
        pill.move_to(LEFT * 4.4 + DOWN * 2.0)

        # Load diagnosis image
        diagnosis = ImageMobject("diagnosis.png")
        diagnosis.height = 2.5
        diagnosis.move_to(RIGHT * 4.4 + DOWN * 2.0)

        tether = always_redraw(
            lambda: Line(
                pill.get_right() + RIGHT * 0.05,
                diagnosis.get_left() + RIGHT * 0.05,
                stroke_width=3,
                color=PRIMARY_COLOR,
            )
        )
        self.play(
            Write(title),
            FadeIn(pill),
            FadeIn(diagnosis),
            FadeIn(tether),
            run_time=1.0,
        )
        used += 1.0

        self.play(pill.animate.shift(RIGHT * 3.5), diagnosis.animate.shift(LEFT * 3.5), run_time=0.7)
        used += 0.7

        # Circle that tightens around both icons (after they've moved)
        icons_group = Group(pill, diagnosis)
        center_point = icons_group.get_center()
        
        # Calculate radius to wrap around both icons
        # Get the width and height of the group
        group_width = icons_group.width
        group_height = icons_group.height
        # Use diagonal to ensure circle wraps around both icons
        diagonal = np.sqrt(group_width**2 + group_height**2)
        loose_radius = diagonal / 2 + 0.8
        tight_radius = diagonal / 2 + 0.2
        
        loose_circle = Circle(radius=loose_radius, color=PRIMARY_COLOR, stroke_width=3)
        loose_circle.move_to(center_point)
        loose_circle.set_fill(opacity=0)

        tight_circle = Circle(radius=tight_radius, color=PRIMARY_COLOR, stroke_width=3)
        tight_circle.move_to(center_point)
        tight_circle.set_fill(opacity=0)

        self.play(FadeOut(tether), Create(loose_circle), run_time=0.4)
        tether.clear_updaters()
        self.remove(tether)
        used += 0.4
        self.play(Transform(loose_circle, tight_circle), run_time=0.4)
        used += 0.4

        # Use renderer time to guarantee total scene length
        # Hold the final visual an extra second before timing the fade-out
        self.wait(1.0)
        remaining = max(total_time - self.renderer.time - 0.6, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.6)


class OutsourcingScene(BaseBloomScene):
    def construct(self):
        self.wait(0.5)

        sentence = make_sentence(
            "Developing new drugs is costly, so pharma increasingly outsources clinical trials "
            "to contract research organizations, or CROs.",
            font_size=30,
        )
        caption_time = 3.0
        visuals_time = 6.0

        cro_box = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.12)
        cro_box.set_stroke("#3da5ff", width=3)
        cro_box.set_fill("#3da5ff", opacity=0.15)
        cro_label = Text("CRO", font_size=38, color=PRIMARY_COLOR).move_to(cro_box)
        cro_group = VGroup(cro_box, cro_label).move_to(DOWN * 2.6)

        def make_node() -> VGroup:
            outer = Circle(radius=0.58)
            outer.set_stroke(PRIMARY_COLOR, width=2.5)
            outer.set_fill(opacity=0)
            cross_h = Line(LEFT * 0.28, RIGHT * 0.28)
            cross_v = Line(UP * 0.28, DOWN * 0.28)
            cross = VGroup(cross_h, cross_v).set_stroke("#ff4d4d", width=5)
            return VGroup(outer, cross)

        node_positions = []
        center = cro_group.get_center()
        ring_radius = 3.2
        for idx in range(7):
            angle = 2 * np.pi * idx / 7
            offset = np.array([np.cos(angle), np.sin(angle), 0.0]) * ring_radius
            node_positions.append(center + offset)
        nodes = VGroup(*[make_node().move_to(pos) for pos in node_positions])

        def connect_line(node: VGroup) -> Line:
            start = node.get_center()
            center_point = cro_box.get_center()
            direction = center_point - start
            length = np.linalg.norm(direction)
            if length == 0:
                return Line(start, center_point)
            unit = direction / length
            half_width = cro_box.width * 0.5
            half_height = cro_box.height * 0.5
            scale_x = half_width / abs(unit[0]) if abs(unit[0]) > 1e-6 else float("inf")
            scale_y = half_height / abs(unit[1]) if abs(unit[1]) > 1e-6 else float("inf")
            edge_scale = min(scale_x, scale_y)
            end = center_point - unit * edge_scale
            line = Line(start, end)
            line.set_stroke(PRIMARY_COLOR, width=2)
            return line

        lines = VGroup(*[connect_line(node) for node in nodes])

        node_line_anims = [
            AnimationGroup(FadeIn(node), Create(line), lag_ratio=0.35, run_time=0.8)
            for node, line in zip(nodes, lines)
        ]
        visuals_anim = Succession(FadeIn(cro_group, run_time=0.6), *node_line_anims)
        visuals_anim.set_run_time(visuals_time)

        self.play(
            Write(sentence, run_time=caption_time),
            visuals_anim,
        )
        self.fade_out_all(run_time=0.25)
        self.wait(2.25)


class TrendsOverviewScene(BaseBloomScene):
    def construct(self):
        total_time = 5.0
        used = 0.0
        self.wait(0.5)
        used += 0.5

        sentence = Text(
            "But there are three trends that will\n"
            "redefine how CROs perform, which will\n"
            "interest retail investors.",
            font_size=30,
            color=PRIMARY_COLOR,
        )
        sentence.to_edge(UP, buff=0.5)
        cro_box = RoundedRectangle(width=2.4, height=1.2, corner_radius=0.1)
        cro_label = Text("CRO", font_size=34, color=PRIMARY_COLOR)
        cro_group = VGroup(cro_box, cro_label).set_stroke(PRIMARY_COLOR, width=2).move_to(DOWN * 1.8)

        self.play(Write(sentence), FadeIn(cro_group), run_time=3.0)
        used += 3.0

        dna_icon = make_dna(color="#4ec9f5").scale(1.2).move_to(cro_group.get_top() + UP * 1.2 + LEFT * 2.6 + DOWN * 0.2)
        digital_icon = VGroup(
            make_phone(color="#ffb84d"),
            make_signal_waves(color="#ffb84d"),
        ).scale(1.2)
        digital_icon.move_to(cro_group.get_top() + UP * 1.5 + DOWN * 0.1)
        gear_icon = VGroup(
            make_gear(color="#9b7bff"),
            Text("AI", font_size=24, color="#9b7bff"),
        ).arrange(RIGHT, buff=0.1)
        gear_icon.scale(1.2).move_to(cro_group.get_top() + UP * 1.2 + RIGHT * 2.6 + DOWN * 0.2)

        def branch_to_icon(icon: Mobject) -> Line:
            start = cro_group.get_top()
            end = icon.get_center()
            direction = end - start
            length = np.linalg.norm(direction)
            if length == 0:
                return Line(start, end)
            unit = direction / length
            end = end - unit * 0.25  # keep line from overlapping icon
            line = Line(start, end)
            line.set_stroke(PRIMARY_COLOR, width=2)
            return line

        branch_left = branch_to_icon(dna_icon)
        branch_mid = branch_to_icon(digital_icon)
        branch_right = branch_to_icon(gear_icon)

        self.play(Create(branch_left), run_time=0.4)
        self.play(Create(branch_mid), run_time=0.4)
        self.play(Create(branch_right), run_time=0.4)
        used += 1.2

        self.play(FadeIn(dna_icon, scale=0.9), run_time=0.4)
        self.play(FadeIn(digital_icon, scale=0.9), run_time=0.4)
        self.play(FadeIn(gear_icon, scale=0.9), run_time=0.4)
        used += 1.2

        remaining = max(total_time - used - 0.6, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.25)
        self.wait(0.25)


class TrendPrecisionScene(BaseBloomScene):
    def construct(self):
        total_time = 8.5
        used = 0.0
        self.wait(0.5)
        used += 0.5

        sentence = make_sentence(
            "First, medicine is shifting toward precision therapies driven by genetics and biomarkers, "
            "requiring CROs to improve capabilities.",
            font_size=30,
        )
        caption_time = 4.5
        dna = dna_helix(height=9, width=1.6, turns=3, stroke_width=7).rotate(PI / 2).move_to(DOWN * 0.3)
        strands = dna[0]
        connectors = dna[1]

        arrow_positions = [
            dna.get_left() + RIGHT * 1.4,
            dna.get_left() + RIGHT * 3.2,
            dna.get_center(),
            dna.get_right() + LEFT * 3.2,
            dna.get_right() + LEFT * 1.4,
        ]
        biomarker_arrows = VGroup(
            *[
                Arrow(
                    pos + DOWN * 1.6,
                    pos + DOWN * 0.6,
                    buff=0,
                    color="#ff4d4d",
                    stroke_width=4,
                )
                for pos in arrow_positions
            ]
        )
        biomarker_label = Text("Biomarkers", font_size=28, color="#ff4d4d")
        biomarker_label.next_to(biomarker_arrows, DOWN, buff=0.2)

        arrow_anims = [FadeIn(arrow, run_time=0.35) for arrow in biomarker_arrows]
        visuals_anim = Succession(
            AnimationGroup(
                Create(strands[0]),
                Create(strands[1]),
                FadeIn(connectors),
                run_time=2.5,
            ),
            *arrow_anims,
            FadeIn(biomarker_label, run_time=0.5),
        )
        visuals_anim.set_run_time(caption_time)

        self.play(
            Write(sentence, run_time=caption_time),
            visuals_anim,
            run_time=caption_time,
        )
        used += caption_time

        extra_hold = 1.0
        self.wait(extra_hold)
        used += extra_hold

        remaining = max(total_time - used - 0.6, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.25)
        self.wait(0.25)


class TrendDigitalScene(BaseBloomScene):
    def construct(self):
        total_time = 7.0
        used = 0.0
        self.wait(0.75)
        used += 0.75

        sentence = Text(
            "Next, CROs that adopt digital tools will\n"
            "fix patient enrollment bottlenecks and run\n"
            "trials remotely.",
            font_size=30,
            color=PRIMARY_COLOR,
        )
        sentence.to_edge(UP, buff=0.5)
        caption_time = 3.0
        visuals_time = 4.5

        map_box = RoundedRectangle(
            width=6.6,
            height=4.3,
            corner_radius=0.4,
            stroke_color="#7ecbff",
            stroke_width=2,
            fill_color="#7ecbff",
            fill_opacity=0.15,
        ).shift(DOWN * 1.2)
        map_center = map_box.get_center()
        hub = Circle(radius=0.32, color=ACCENT_COLOR, fill_opacity=1, stroke_width=0).move_to(map_center)
        nodes = VGroup()
        for pos in [
            LEFT * 2.4 + UP * 0.6,
            RIGHT * 2.4 + UP * 0.3,
            LEFT * 1.8 + DOWN * 1.4,
            RIGHT * 2.1 + DOWN * 1.2,
            UP * 1.0,
        ]:
            dot = Dot(map_center + pos, color=PRIMARY_COLOR, radius=0.1)
            nodes.add(dot)
        links = VGroup(*[Line(hub.get_center(), n.get_center(), stroke_color=ACCENT_COLOR, stroke_width=2) for n in nodes])
        links.set_opacity(0.7)

        icons = VGroup(
            Text("Mobile", color=PRIMARY_COLOR).scale(0.55).next_to(map_box, DOWN, buff=0.25).shift(LEFT * 1.8),
            Text("Home", color=PRIMARY_COLOR).scale(0.55).next_to(map_box, DOWN, buff=0.25),
            Text("Video", color=PRIMARY_COLOR).scale(0.55).next_to(map_box, DOWN, buff=0.25).shift(RIGHT * 1.8),
        )
        hospital = Text("Hospital", color=PRIMARY_COLOR).scale(0.6).next_to(map_box, UP, buff=0.25).set_opacity(0.6)

        visual_anim = Succession(
            FadeIn(map_box, run_time=0.6),
            AnimationGroup(FadeIn(nodes, lag_ratio=0.05), FadeIn(hub)),
            Create(links, lag_ratio=0.1, run_time=0.8),
            AnimationGroup(FadeIn(icons, lag_ratio=0.1), FadeIn(hospital)),
        )
        visual_anim.set_run_time(visuals_time)

        self.play(
            Write(sentence, run_time=caption_time),
            visual_anim,
            run_time=visuals_time,
        )
        used += visuals_time

        remaining = max(total_time - used - 0.5, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.25)
        self.wait(0.25)


class TrendAutomationScene(BaseBloomScene):
    def construct(self):
        total_time = 8.0
        used = 0.0
        self.wait(0.5)
        used += 0.5

        sentence = make_sentence(
            "Finally, as trial costs rise, automation and AI are becoming essential to making drug development faster and more efficient.",
            font_size=30,
        )
        cro_box = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.25)
        cro_box.set_stroke("#2d6cff", width=2)
        cro_box.set_fill("#2d6cff", opacity=0.2)
        cro_label = Text("CRO", font_size=26, color=WHITE).move_to(cro_box)
        cro_group = VGroup(cro_box, cro_label).move_to(DOWN * 0.6)

        input_nodes = VGroup(*[Circle(radius=0.18) for _ in range(3)])
        input_nodes.arrange(DOWN, buff=0.55).move_to(LEFT * 2.4)
        input_nodes.set_stroke("#1a1a1a", width=2)
        input_nodes.set_fill("#f5c14d", opacity=1)

        hidden_nodes = VGroup(*[Circle(radius=0.18) for _ in range(4)])
        hidden_nodes.arrange(DOWN, buff=0.45).move_to(ORIGIN)
        hidden_nodes.set_stroke("#1a1a1a", width=2)
        hidden_nodes.set_fill("#f5c14d", opacity=1)

        input_to_hidden = VGroup(
            *[
                Line(a.get_center(), b.get_center())
                for a in input_nodes
                for b in hidden_nodes
            ]
        )
        connections = VGroup(input_to_hidden)
        connections.set_stroke("#1a1a1a", width=5)

        network = VGroup(connections, input_nodes, hidden_nodes)
        network.move_to(LEFT * 3.4 + DOWN * 0.6)

        gear = ImageMobject("gear.png").set_height(2.3).move_to(RIGHT * 3.5 + DOWN * 0.6)

        intro_time = 2.5
        def spin_updater(mob, dt):
            mob.rotate(PI * dt)

        gear.add_updater(spin_updater)
        self.play(
            Write(sentence, run_time=intro_time),
            FadeIn(cro_group),
            Create(connections),
            FadeIn(input_nodes),
            FadeIn(hidden_nodes),
            FadeIn(gear),
            run_time=intro_time,
        )
        used += intro_time

        spin_time = 0.8
        self.wait(spin_time)
        used += spin_time

        pull_time = 2.3
        self.play(
            network.animate.move_to(cro_group).scale(0.2),
            gear.animate.move_to(cro_group).scale(0.2),
            cro_group.animate.scale(2.0),
            run_time=pull_time,
        )
        used += pull_time

        absorb_time = 0.3
        self.play(FadeOut(network), FadeOut(gear), run_time=absorb_time)
        used += absorb_time
        gear.remove_updater(spin_updater)

        remaining = max(total_time - used - 0.6, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.25)
        self.wait(0.25)


class CtaScene(BaseBloomScene):
    def construct(self):
        total_time = 5.0
        used = 0.0
        self.wait(0.5)
        used += 0.5

        sentence = make_sentence(
            "To learn more, check out the full article on Bloom using the link below.",
            font_size=30,
        )
        link = RoundedRectangle(width=4.6, height=0.6, corner_radius=0.1)
        link.set_stroke(PRIMARY_COLOR, width=2)
        link_text = Text("bloom.com/article", font_size=24, color=PRIMARY_COLOR).move_to(link)
        link_group = VGroup(link, link_text).move_to(DOWN * 0.6)
        self.play(Write(sentence), FadeIn(link_group), run_time=0.6)
        used += 0.6

        remaining = max(total_time - used - 0.6, 0)
        if remaining > 0:
            self.wait(remaining)
        self.fade_out_all(run_time=0.25)
        self.wait(0.25)