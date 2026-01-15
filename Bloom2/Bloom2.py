from manim import *
import numpy as np

class Scene1_ThreeSecretAreas(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"  # Dark background
        # Title text
        title = Text(
            "There are 3 secret areas of growth\nas the AI-data center partnership grows.",
            font_size=36,
            color=WHITE,
            font="Arial"
        ).to_edge(UP, buff=0.5)
        
        # Create triangle vertices
        vertices = [
            np.array([0, 1.5, 0]),      # Top
            np.array([-2, -1, 0]),       # Bottom left
            np.array([2, -1, 0])         # Bottom right
        ]
        
        # Animate triangle forming line by line
        triangle = Polygon(*vertices, color=TEAL, stroke_width=3)
        triangle_lines = VGroup()
        for i in range(3):
            line = Line(vertices[i], vertices[(i+1)%3], color=TEAL, stroke_width=3)
            triangle_lines.add(line)
        
        # Labels
        labels = VGroup(
            Text("Real Estate", font_size=32, color=YELLOW).move_to(vertices[0] + UP*0.5),
            Text("Power", font_size=32, color=YELLOW).move_to(vertices[1] + DOWN*0.5 + LEFT*0.3),
            Text("Cooling", font_size=32, color=YELLOW).move_to(vertices[2] + DOWN*0.5 + RIGHT*0.3)
        )
        
        # Glowing nodes at corners
        nodes = VGroup(*[
            Dot(vertex, radius=0.15, color=YELLOW)
            for vertex in vertices
        ])
        
        # Animate
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        for line in triangle_lines:
            self.play(Create(line), run_time=0.4)
        
        self.play(FadeIn(nodes), FadeIn(labels), run_time=1)
        
        # Shimmer effect
        shimmer = Line(vertices[0], vertices[1], color=WHITE, stroke_width=5)
        shimmer.set_opacity(0.7)
        self.play(
            shimmer.animate.shift((vertices[1] - vertices[0])),
            run_time=0.8
        )
        self.play(FadeOut(shimmer))
        
        self.wait(0.5)


class Scene2_AIQuery(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # GPT-style prompt box
        prompt_box = RoundedRectangle(
            width=6, height=1.5,
            corner_radius=0.2,
            color=GRAY,
            fill_opacity=0.2,
            stroke_width=2
        )
        
        prompt_text = Text(
            "Ask AI anything...",
            font_size=32,
            color=WHITE
        )
        
        prompt_group = VGroup(prompt_box, prompt_text)
        
        self.play(FadeIn(prompt_group), run_time=1)
        self.wait(0.5)
        
        # Zoom into text and reveal network
        self.play(
            prompt_group.animate.scale(0.3).move_to(ORIGIN),
            run_time=1
        )
        self.play(FadeOut(prompt_group))
        
        # Create network graph
        center = ORIGIN
        network = VGroup()
        
        # Create nodes in layers
        layers = 4
        nodes_per_layer = [1, 6, 18, 54]
        positions = []
        
        # Center node
        center_node = Dot(center, radius=0.08, color=TEAL)
        network.add(center_node)
        positions.append(center)
        
        # Create nodes in expanding layers
        layer_radius = [0, 0.8, 1.6, 2.4]
        for layer in range(1, layers):
            for i in range(nodes_per_layer[layer]):
                angle = 2 * PI * i / nodes_per_layer[layer]
                pos = center + layer_radius[layer] * np.array([
                    np.cos(angle), np.sin(angle), 0
                ])
                node = Dot(pos, radius=0.05, color=BLUE)
                network.add(node)
                positions.append(pos)
        
        # Create connections
        connections = VGroup()
        for i, pos1 in enumerate(positions):
            if i == 0:  # Connect center to first layer
                for j in range(1, nodes_per_layer[1] + 1):
                    line = Line(pos1, positions[j], color=GRAY, stroke_width=0.5)
                    line.set_opacity(0.3)
                    connections.add(line)
            elif i < len(positions) - nodes_per_layer[-1]:  # Connect to next layer
                for j in range(i + 1, min(i + 4, len(positions))):
                    if np.linalg.norm(positions[i] - positions[j]) < 1.5:
                        line = Line(positions[i], positions[j], color=GRAY, stroke_width=0.3)
                        line.set_opacity(0.2)
                        connections.add(line)
        
        # Animate network appearing
        self.play(Create(connections), run_time=1.5)
        self.play(FadeIn(network), run_time=1)
        
        # Pulse animation
        for _ in range(3):
            pulse_nodes = network.copy()
            pulse_nodes.set_color(YELLOW)
            pulse_nodes.scale(1.5)
            pulse_nodes.set_opacity(0.5)
            self.play(
                pulse_nodes.animate.set_opacity(0),
                run_time=0.6
            )


class Scene3_GrowthChart(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "AI-ready data center capacity is growing\n33% per year",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # Create bar chart
        years = ["2024", "2025", "2026", "2027"]
        heights = [1, 1.33, 1.77, 2.35]  # 33% growth each year
        
        bars = VGroup()
        labels = VGroup()
        
        for i, (year, height) in enumerate(zip(years, heights)):
            bar = Rectangle(
                width=1.2,
                height=height,
                color=TEAL,
                fill_opacity=0.7,
                stroke_width=2
            ).shift(RIGHT * (i - 1.5) * 1.5 + DOWN * 0.5)
            
            label = Text(year, font_size=24, color=WHITE).next_to(bar, DOWN, buff=0.2)
            
            bars.add(bar)
            labels.add(label)
        
        # Animate bars appearing
        for bar, label in zip(bars, labels):
            self.play(
                GrowFromEdge(bar, DOWN),
                FadeIn(label),
                run_time=0.5
            )
        
        # +33% YoY overlay
        growth_text = Text(
            "+33% YoY",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        ).move_to(UP * 1.5)
        
        self.play(FadeIn(growth_text), run_time=0.8)
        
        # Shade half to represent generative AI
        highlight = Rectangle(
            width=4.8,
            height=1.2,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0
        ).align_to(bars, DOWN).shift(UP * 0.6)
        
        gen_ai_text = Text(
            "Generative AI driving ~50%",
            font_size=24,
            color=YELLOW
        ).next_to(highlight, UP, buff=0.1)
        
        self.play(FadeIn(highlight), FadeIn(gen_ai_text), run_time=1)
        self.wait(0.5)


class Scene4_HyperscaleCampuses(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Most work happening inside\ncolossal hyperscale campuses",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # Simple US outline (simplified rectangle)
        us_outline = Rectangle(
            width=6,
            height=3.5,
            color=GRAY,
            fill_opacity=0.1,
            stroke_width=2
        ).shift(DOWN * 0.3)
        
        self.play(Create(us_outline), run_time=0.8)
        
        # Large rectangular building footprints
        buildings = VGroup()
        building_positions = [
            np.array([-1.5, 0.5, 0]),
            np.array([1, 0.8, 0]),
            np.array([-0.5, -0.8, 0]),
            np.array([2, -0.5, 0])
        ]
        
        for pos in building_positions:
            building = Rectangle(
                width=1.5,
                height=1.2,
                color=TEAL,
                fill_opacity=0.4,
                stroke_width=2
            ).move_to(pos)
            
            # Small squares inside (hinting at racks)
            racks = VGroup()
            for i in range(3):
                for j in range(2):
                    rack = Square(
                        side_length=0.15,
                        color=WHITE,
                        fill_opacity=0.6
                    ).move_to(building.get_center() + 
                              RIGHT * (i - 1) * 0.2 + UP * (j - 0.5) * 0.2)
                    racks.add(rack)
            
            building_group = VGroup(building, racks)
            buildings.add(building_group)
        
        # Animate buildings appearing
        for building in buildings:
            self.play(FadeIn(building), run_time=0.4)
        
        # Text bubble
        bubble_text = Text(
            "Hyperscale Campuses",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN, buff=1)
        
        self.play(FadeIn(bubble_text), run_time=0.8)
        
        # Pulsing circle for "65% by decade's end"
        circle = Circle(
            radius=0.4,
            color=YELLOW,
            stroke_width=3
        ).move_to(buildings[0].get_center())
        
        percent_text = Text(
            "65% by\ndecade's end",
            font_size=20,
            color=YELLOW
        ).move_to(circle.get_center())
        
        self.play(
            Create(circle),
            FadeIn(percent_text),
            run_time=0.8
        )
        
        # Pulse animation
        for _ in range(2):
            pulse = circle.copy()
            pulse.scale(1.5)
            pulse.set_opacity(0.3)
            self.play(
                pulse.animate.set_opacity(0),
                run_time=0.6
            )
        
        self.wait(0.5)


class Scene5_RealEstate(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "First opportunity: Real Estate",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.2)
        
        # Grid of building icons
        grid_size = 4
        grid = VGroup()
        buildings = []
        
        spacing = 1.2
        start_pos = np.array([-1.8, 0.5, 0])
        
        for i in range(grid_size):
            for j in range(grid_size):
                pos = start_pos + np.array([j * spacing, -i * spacing, 0])
                
                # Building icon (simple rectangle with triangle roof)
                building = VGroup(
                    Rectangle(
                        width=0.6,
                        height=0.6,
                        color=TEAL,
                        fill_opacity=0.5,
                        stroke_width=2
                    ),
                    Polygon(
                        np.array([-0.3, 0.3, 0]),
                        np.array([0.3, 0.3, 0]),
                        np.array([0, 0.5, 0]),
                        color=TEAL,
                        fill_opacity=0.5,
                        stroke_width=2
                    )
                ).move_to(pos)
                
                grid.add(building)
                buildings.append((building, pos))
        
        self.play(FadeIn(grid), run_time=1)
        
        # Fill up grid cells (turn red when full)
        fill_order = list(range(len(buildings)))
        np.random.shuffle(fill_order)
        
        for idx in fill_order[:12]:  # Fill 12 out of 16
            building, pos = buildings[idx]
            self.play(
                building.animate.set_color(RED).set_fill_opacity(0.8),
                run_time=0.15
            )
        
        # Vacancy meter
        meter_bg = Rectangle(
            width=0.3,
            height=2.5,
            color=GRAY,
            fill_opacity=0.3,
            stroke_width=2
        ).to_edge(RIGHT, buff=1)
        
        meter_fill = Rectangle(
            width=0.3,
            height=2.5,
            color=RED,
            fill_opacity=0.8,
            stroke_width=0
        ).align_to(meter_bg, DOWN).align_to(meter_bg, RIGHT)
        
        meter_label = Text("0%", font_size=24, color=RED).next_to(meter_bg, UP, buff=0.2)
        vacancy_label = Text("Vacancy", font_size=20, color=WHITE).next_to(meter_bg, DOWN, buff=0.2)
        
        self.play(
            FadeIn(meter_bg),
            FadeIn(vacancy_label),
            run_time=0.5
        )
        
        self.play(
            meter_fill.animate.align_to(meter_bg, UP),
            FadeIn(meter_label),
            run_time=1.5
        )
        
        # Overlay text
        overlay_text = Text(
            "Rents ↑ & Long-term leases ↑",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(overlay_text), run_time=1)
        self.wait(0.5)


class Scene6_ElectricityConstraint(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Electricity may be the toughest constraint",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # Old chip
        old_chip = Rectangle(
            width=1.5,
            height=1,
            color=GRAY,
            fill_opacity=0.3,
            stroke_width=2
        ).shift(LEFT * 2.5)
        
        old_glow = Circle(
            radius=0.8,
            color=GRAY,
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(old_chip.get_center())
        
        old_label = Text("Old Chip", font_size=20, color=GRAY).next_to(old_chip, DOWN, buff=0.3)
        
        old_group = VGroup(old_glow, old_chip, old_label)
        
        # New AI chip
        new_chip = Rectangle(
            width=2.2,
            height=1.5,
            color=YELLOW,
            fill_opacity=0.5,
            stroke_width=3
        ).shift(RIGHT * 2.5)
        
        new_glow = Circle(
            radius=1.3,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(new_chip.get_center())
        
        new_label = Text("New AI Chip", font_size=20, color=YELLOW).next_to(new_chip, DOWN, buff=0.3)
        
        new_group = VGroup(new_glow, new_chip, new_label)
        
        # Show old chip
        self.play(FadeIn(old_group), run_time=1)
        self.wait(0.3)
        
        # Transform to new chip
        self.play(
            Transform(old_group, new_group),
            FadeIn(new_group),
            run_time=1.5
        )
        
        # Power meter gauge
        gauge_center = DOWN * 1.5
        gauge_radius = 1.2
        
        # Gauge arc
        gauge_arc = Arc(
            radius=gauge_radius,
            angle=PI,
            start_angle=-PI/2,
            color=WHITE,
            stroke_width=3
        ).move_to(gauge_center)
        
        # Needle starting position
        needle_start = Line(
            gauge_center,
            gauge_center + UP * gauge_radius * 0.3,
            color=GREEN,
            stroke_width=4
        )
        
        # Needle ending position (3x higher)
        needle_end = Line(
            gauge_center,
            gauge_center + UP * gauge_radius * 0.9,
            color=RED,
            stroke_width=4
        )
        
        gauge_label = Text("Power", font_size=24, color=WHITE).next_to(gauge_arc, DOWN, buff=0.3)
        
        self.play(
            Create(gauge_arc),
            FadeIn(gauge_label),
            run_time=0.8
        )
        
        self.play(Create(needle_start), run_time=0.5)
        self.play(
            Transform(needle_start, needle_end),
            run_time=1.2
        )
        
        # 3x power draw text
        power_text = Text(
            "3× power draw",
            font_size=24,
            color=RED
        ).next_to(gauge_arc, UP, buff=0.3)
        
        self.play(FadeIn(power_text), run_time=0.8)
        self.wait(0.5)


class Scene7_EnergyDemand(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Driving US demand toward\n50-60 extra gigawatts by 2030",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # US silhouette (simplified)
        us_shape = RoundedRectangle(
            width=5,
            height=3,
            corner_radius=0.3,
            color=TEAL,
            fill_opacity=0.2,
            stroke_width=2
        ).shift(DOWN * 0.2)
        
        self.play(Create(us_shape), run_time=0.8)
        
        # Glow effect
        glow = us_shape.copy()
        glow.set_color(YELLOW)
        glow.set_fill_opacity(0.1)
        glow.scale(1.1)
        self.play(FadeIn(glow), run_time=0.5)
        
        # Arrows pointing inward (energy flowing)
        arrows = VGroup()
        arrow_positions = [
            (LEFT * 3.5, RIGHT * 0.5),
            (RIGHT * 3.5, LEFT * 0.5),
            (UP * 2, DOWN * 0.3),
            (DOWN * 2, UP * 0.3)
        ]
        
        for start, direction in arrow_positions:
            arrow = Arrow(
                start=start,
                end=start + direction * 1.5,
                color=YELLOW,
                stroke_width=4,
                buff=0
            )
            arrows.add(arrow)
        
        self.play(Create(arrows), run_time=1)
        
        # Power capacity bar
        bar_bg = Rectangle(
            width=6,
            height=0.8,
            color=GRAY,
            fill_opacity=0.3,
            stroke_width=2
        ).to_edge(DOWN, buff=1.5)
        
        bar_fill = Rectangle(
            width=0,
            height=0.8,
            color=YELLOW,
            fill_opacity=0.8,
            stroke_width=0
        ).align_to(bar_bg, LEFT).align_to(bar_bg, DOWN)
        
        bar_label = Text(
            "+50-60 GW",
            font_size=28,
            color=YELLOW,
            weight=BOLD
        ).move_to(bar_bg.get_center())
        
        self.play(
            FadeIn(bar_bg),
            FadeIn(bar_label),
            run_time=0.8
        )
        
        # Animate bar filling
        self.play(
            bar_fill.animate.set_width(6),
            run_time=2
        )
        
        # Lightning bolt animation
        bolt = Polygon(
            np.array([-0.2, 0.3, 0]),
            np.array([0, 0.1, 0]),
            np.array([-0.1, 0, 0]),
            np.array([0.1, -0.2, 0]),
            np.array([0, -0.3, 0]),
            np.array([0.2, -0.1, 0]),
            np.array([0.1, 0, 0]),
            np.array([-0.1, 0.2, 0]),
            color=YELLOW,
            fill_opacity=0.9,
            stroke_width=0
        ).scale(0.5).move_to(us_shape.get_center() + UP * 0.5)
        
        self.play(
            FadeIn(bolt),
            bolt.animate.scale(1.5).set_opacity(0.7),
            run_time=0.6
        )
        self.play(FadeOut(bolt), run_time=0.4)
        self.wait(0.5)


class Scene8_GridConstruction(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Delivering that energy is harder\nthan producing it",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # Power plant (left)
        plant = VGroup(
            Rectangle(
                width=1.2,
                height=1.2,
                color=YELLOW,
                fill_opacity=0.6,
                stroke_width=2
            ),
            Polygon(
                np.array([-0.6, 0.6, 0]),
                np.array([0.6, 0.6, 0]),
                np.array([0, 1, 0]),
                color=YELLOW,
                fill_opacity=0.6,
                stroke_width=2
            )
        ).shift(LEFT * 4)
        
        plant_label = Text("Power Plant", font_size=20, color=WHITE).next_to(plant, DOWN, buff=0.3)
        
        # Transmission towers (middle)
        towers = VGroup()
        for i in range(3):
            tower = VGroup(
                Line(
                    np.array([-0.1, 0, 0]),
                    np.array([0, 0.8, 0]),
                    color=GRAY,
                    stroke_width=3
                ),
                Line(
                    np.array([0.1, 0, 0]),
                    np.array([0, 0.8, 0]),
                    color=GRAY,
                    stroke_width=3
                ),
                Line(
                    np.array([-0.1, 0.4, 0]),
                    np.array([0.1, 0.4, 0]),
                    color=GRAY,
                    stroke_width=2
                )
            ).shift(RIGHT * (i - 1) * 1.5)
            towers.add(tower)
        
        # Data center (right)
        data_center = Rectangle(
            width=1.5,
            height=1.5,
            color=TEAL,
            fill_opacity=0.6,
            stroke_width=2
        ).shift(RIGHT * 4)
        
        dc_label = Text("Data Center", font_size=20, color=WHITE).next_to(data_center, DOWN, buff=0.3)
        
        # Show components
        self.play(
            FadeIn(plant),
            FadeIn(plant_label),
            run_time=0.8
        )
        
        self.play(
            FadeIn(towers),
            run_time=0.8
        )
        
        self.play(
            FadeIn(data_center),
            FadeIn(dc_label),
            run_time=0.8
        )
        
        # Power lines
        power_lines = VGroup()
        positions = [
            (plant.get_right(), towers[0].get_left()),
            (towers[0].get_right(), towers[1].get_left()),
            (towers[1].get_right(), towers[2].get_left()),
            (towers[2].get_right(), data_center.get_left())
        ]
        
        for start, end in positions:
            line = Line(start, end, color=YELLOW, stroke_width=3)
            power_lines.add(line)
        
        # Animate lines with flickering
        self.play(Create(power_lines), run_time=1)
        
        # Flicker effect (bottleneck)
        for _ in range(3):
            flicker_lines = power_lines.copy()
            flicker_lines.set_color(RED)
            flicker_lines.set_opacity(0.5)
            self.play(
                flicker_lines.animate.set_opacity(0),
                run_time=0.3
            )
        
        # Label
        grid_label = Text(
            "Grid Construction Needed",
            font_size=32,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=1)
        
        self.play(FadeIn(grid_label), run_time=1)
        self.wait(0.5)


class Scene9_Cooling(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Cooling is the final frontier",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.2)
        
        # Server racks
        racks = VGroup()
        for i in range(3):
            rack = Rectangle(
                width=0.8,
                height=2,
                color=GRAY,
                fill_opacity=0.4,
                stroke_width=2
            ).shift(RIGHT * (i - 1) * 1.2)
            
            # Server units inside
            for j in range(4):
                unit = Rectangle(
                    width=0.7,
                    height=0.4,
                    color=RED,
                    fill_opacity=0.6,
                    stroke_width=1
                ).move_to(rack.get_center() + UP * (1.5 - j * 0.5 - 0.2))
                rack.add(unit)
            
            racks.add(rack)
        
        self.play(Write(title9), FadeIn(racks), run_time=1.2)
        
        # Heat waves rising
        heat_waves = VGroup()
        for rack in racks:
            for _ in range(3):
                wave = Arc(
                    radius=0.4,
                    angle=PI,
                    start_angle=0,
                    color=RED,
                    stroke_width=2,
                    fill_opacity=0.3
                ).move_to(rack.get_top() + UP * 0.3)
                heat_waves.add(wave)
        
        self.play(
            Create(heat_waves),
            heat_waves.animate.shift(UP * 0.5).set_opacity(0.1),
            run_time=1.5
        )
        
        # Liquid pipes from below
        pipes = VGroup()
        for rack in racks:
            pipe = Rectangle(
                width=0.6,
                height=0.3,
                color=BLUE,
                fill_opacity=0.8,
                stroke_width=2
            ).move_to(rack.get_bottom() + DOWN * 0.5)
            pipes.add(pipe)
        
        # Liquid droplets turning into tubes
        droplets = VGroup()
        for pipe in pipes:
            droplet = Circle(
                radius=0.1,
                color=BLUE,
                fill_opacity=0.9
            ).move_to(pipe.get_bottom() + DOWN * 0.5)
            droplets.add(droplet)
        
        self.play(FadeIn(droplets), run_time=0.5)
        self.play(
            Transform(droplets, pipes),
            FadeIn(pipes),
            run_time=1
        )
        
        # Pipes animate upward, pushing heat away
        self.play(
            pipes.animate.shift(UP * 2.5),
            heat_waves.animate.set_opacity(0),
            racks.animate.set_color(BLUE).set_fill_opacity(0.3),
            run_time=2
        )
        
        # Label
        cooling_label = Text(
            "Liquid Cooling",
            font_size=32,
            color=BLUE,
            weight=BOLD
        ).to_edge(DOWN, buff=1)
        
        self.play(FadeIn(cooling_label), run_time=1)
        self.wait(0.5)


class Scene10_Headlines(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        # Title
        title = Text(
            "Headlines focus on AI breakthroughs\nbut behind the scenes...",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        
        # Flashy AI icons (left side)
        ai_icons = VGroup()
        
        # Robot head
        robot_head = VGroup(
            Circle(radius=0.4, color=YELLOW, fill_opacity=0.6),
            Circle(radius=0.15, color=BLACK, fill_opacity=1).shift(LEFT * 0.15 + UP * 0.1),
            Circle(radius=0.15, color=BLACK, fill_opacity=1).shift(RIGHT * 0.15 + UP * 0.1),
            Arc(radius=0.2, angle=PI, start_angle=0, color=BLACK, stroke_width=3).shift(DOWN * 0.1)
        ).shift(LEFT * 3 + UP * 0.5)
        
        # Neural network icon
        neural_net = VGroup()
        nodes = [
            np.array([-0.3, 0.3, 0]),
            np.array([0.3, 0.3, 0]),
            np.array([-0.3, -0.3, 0]),
            np.array([0.3, -0.3, 0]),
            np.array([0, 0, 0])
        ]
        for node in nodes:
            neural_net.add(Dot(node, radius=0.08, color=YELLOW))
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                line = Line(nodes[i], nodes[j], color=YELLOW, stroke_width=1)
                line.set_opacity(0.5)
                neural_net.add(line)
        neural_net.shift(LEFT * 3 + DOWN * 0.5)
        
        ai_icons.add(robot_head, neural_net)
        
        # Show AI icons popping up
        self.play(
            FadeIn(robot_head, scale=1.5),
            FadeIn(neural_net, scale=1.5),
            run_time=1
        )
        
        # Camera slides sideways to reveal infrastructure
        self.play(
            ai_icons.animate.shift(LEFT * 1.5).set_opacity(0.3),
            run_time=1.5
        )
        
        # Infrastructure icons (right side)
        infra_icons = VGroup()
        
        # Data center icon
        dc_icon = Rectangle(
            width=1,
            height=1,
            color=TEAL,
            fill_opacity=0.6,
            stroke_width=2
        ).shift(RIGHT * 2 + UP * 0.5)
        dc_label = Text("Data Centers", font_size=18, color=TEAL).next_to(dc_icon, DOWN, buff=0.2)
        
        # Grid lines
        grid_lines = VGroup(
            Line(LEFT * 0.5 + UP * 0.3, RIGHT * 0.5 + UP * 0.3, color=YELLOW, stroke_width=2),
            Line(LEFT * 0.5, RIGHT * 0.5, color=YELLOW, stroke_width=2),
            Line(LEFT * 0.5 + DOWN * 0.3, RIGHT * 0.5 + DOWN * 0.3, color=YELLOW, stroke_width=2),
            Line(UP * 0.3 + LEFT * 0.5, UP * 0.3 + RIGHT * 0.5, color=YELLOW, stroke_width=2),
            Line(LEFT * 0.5, RIGHT * 0.5, color=YELLOW, stroke_width=2),
            Line(DOWN * 0.3 + LEFT * 0.5, DOWN * 0.3 + RIGHT * 0.5, color=YELLOW, stroke_width=2)
        ).shift(RIGHT * 2)
        grid_label = Text("Grid", font_size=18, color=YELLOW).next_to(grid_lines, DOWN, buff=0.2)
        
        # Cooling coils
        cooling_coils = VGroup()
        for i in range(3):
            coil = Arc(
                radius=0.15,
                angle=2*PI,
                color=BLUE,
                stroke_width=3
            ).shift(RIGHT * 2 + DOWN * 0.5 + RIGHT * (i - 1) * 0.3)
            cooling_coils.add(coil)
        cooling_label = Text("Cooling", font_size=18, color=BLUE).next_to(cooling_coils, DOWN, buff=0.2)
        
        infra_icons.add(
            VGroup(dc_icon, dc_label),
            VGroup(grid_lines, grid_label),
            VGroup(cooling_coils, cooling_label)
        )
        
        # Reveal infrastructure icons with glow
        for icon_group in infra_icons:
            self.play(
                FadeIn(icon_group, scale=1.2),
                run_time=0.8
            )
        
        # Make infrastructure glow softly (add glow effect)
        glow_effects = VGroup()
        for icon_group in infra_icons:
            glow = icon_group.copy()
            glow.scale(1.1)
            glow.set_opacity(0.3)
            glow_effects.add(glow)
        
        self.play(
            FadeIn(glow_effects),
            run_time=1
        )
        
        # Final text
        final_text = Text(
            "Growth in companies that can\nrent centers, build grids, and cool rooms",
            font_size=28,
            color=WHITE
        ).to_edge(DOWN, buff=1)
        
        self.play(FadeIn(final_text), run_time=1.5)
        self.wait(1)


class FullAnimation(Scene):
    """Combines all 10 scenes into one continuous video with smooth transitions.
    Configured for vertical/portrait format (9:16 aspect ratio, 1080x1920 pixels).
    """
    def construct(self):
        # Configure for vertical/portrait format (9:16 aspect ratio)
        # The frame aspect ratio is set via command line: --resolution 1080,1920
        # This adjusts the frame to match vertical format
        
        # Disable auto-preview to avoid xdg-open errors
        config.preview = False
        self.camera.background_color = "#0a0a0a"  # Dark background
        
        # Scene 1: Three Secret Areas
        title1 = Text(
            "There are 3 secret areas of growth\nas the AI-data center partnership grows.",
            font_size=42,
            color=WHITE,
            font="Arial"
        ).center().shift(UP * 3.0)  # Centered high, away from edges
        
        # Adjust triangle to fit vertical format - make it smaller and centered
        vertices = [
            np.array([0, 0.5, 0]),      # Top - centered
            np.array([-2.5, -2.5, 0]),  # Bottom left - smaller
            np.array([2.5, -2.5, 0])    # Bottom right - smaller
        ]
        
        triangle_lines = VGroup()
        for i in range(3):
            line = Line(vertices[i], vertices[(i+1)%3], color=TEAL, stroke_width=7)
            triangle_lines.add(line)
        
        # Create icons for each node - make them VERY large and visible
        # House icon for Real Estate - positioned at top vertex
        house_icon = VGroup(
            Polygon(
                np.array([-0.6, 0, 0]),
                np.array([0.6, 0, 0]),
                np.array([0, 0.85, 0]),
                color=RED,
                fill_opacity=1.0,
                stroke_width=5
            ),
            Rectangle(
                width=0.75,
                height=0.6,
                color=RED,
                fill_opacity=1.0,
                stroke_width=5
            ).shift(DOWN * 0.3)
        ).move_to(vertices[0])
        
        # Lightning bolt for Power - positioned at bottom left vertex
        lightning_icon = Polygon(
            np.array([-0.3, 0.45, 0]),
            np.array([0, 0.22, 0]),
            np.array([-0.16, 0, 0]),
            np.array([0.16, -0.32, 0]),
            np.array([0, -0.48, 0]),
            np.array([0.3, -0.16, 0]),
            np.array([0.16, 0, 0]),
            np.array([-0.16, 0.32, 0]),
            color=YELLOW,
            fill_opacity=1.0,
            stroke_width=0
        ).move_to(vertices[1])
        
        # Snowflake for Cooling - positioned at bottom right vertex
        snowflake_icon = VGroup()
        # Create 6-pointed snowflake with branches
        for i in range(6):
            angle = i * PI / 3
            # Main branch (longer)
            branch = Line(
                ORIGIN,
                np.array([0.4 * np.cos(angle), 0.4 * np.sin(angle), 0]),
                color=BLUE,
                stroke_width=6
            )
            snowflake_icon.add(branch)
            # Side branches
            side_angle1 = angle + PI / 6
            side_angle2 = angle - PI / 6
            side1 = Line(
                np.array([0.25 * np.cos(angle), 0.25 * np.sin(angle), 0]),
                np.array([0.4 * np.cos(side_angle1), 0.4 * np.sin(side_angle1), 0]),
                color=BLUE,
                stroke_width=5
            )
            side2 = Line(
                np.array([0.25 * np.cos(angle), 0.25 * np.sin(angle), 0]),
                np.array([0.4 * np.cos(side_angle2), 0.4 * np.sin(side_angle2), 0]),
                color=BLUE,
                stroke_width=5
            )
            snowflake_icon.add(side1, side2)
        snowflake_icon.move_to(vertices[2])
        
        icons = VGroup(house_icon, lightning_icon, snowflake_icon)
        
        labels1 = VGroup(
            Text("Real Estate", font_size=40, color=YELLOW).center().move_to(vertices[0] + UP*1.0),
            Text("Power", font_size=40, color=YELLOW).center().move_to(vertices[1] + DOWN*1.0),
            Text("Cooling", font_size=40, color=YELLOW).center().move_to(vertices[2] + DOWN*1.0)
        )
        
        self.play(Write(title1), run_time=1.0)
        self.wait(0.3)
        for line in triangle_lines:
            self.play(Create(line), run_time=0.35)
        # Fade in icons and labels smoothly
        self.play(FadeIn(icons, run_time=1.0))
        self.play(FadeIn(labels1), run_time=0.6)
        self.wait(0.4)
        
        # Transition to Scene 2
        scene1_group = VGroup(title1, triangle_lines, house_icon, lightning_icon, snowflake_icon, labels1)
        self.play(FadeOut(scene1_group), run_time=0.8)
        
        # Scene 2: AI Query
        title2 = Text(
            "Every AI query involves\nmillions of servers",
            font_size=42,
            color=WHITE
        ).center().shift(UP * 3.0)  # Centered high, away from edges
        
        self.play(Write(title2), run_time=1.5)
        
        prompt_box = RoundedRectangle(
            width=7, height=2,
            corner_radius=0.4,
            color=GRAY,
            fill_opacity=0.2,
            stroke_width=4
        )
        prompt_text = Text("Ask AI anything...", font_size=48, color=WHITE)
        prompt_group = VGroup(prompt_box, prompt_text).center().shift(UP * 1.2)  # Centered with margins
        
        # Fade in prompt, then zoom/shift it to the left
        self.play(FadeIn(prompt_group), run_time=1)
        self.wait(0.3)
        # Shift further left to make room for a larger tree
        self.play(prompt_group.animate.scale(0.35).move_to(LEFT * 4 + DOWN * 0.3), run_time=1)
        
        # Build a simple growing binary tree from the right side of the prompt
        root_anchor = prompt_box.get_right() + RIGHT * 1.0 + DOWN * 0.1
        level_spacing_y = 1.1
        offset_x = 1.4
        # Build nodes by level for ordered, left-to-right growth
        root_node = Dot(root_anchor, radius=0.12, color=BLUE)
        left1 = root_anchor + np.array([offset_x, -level_spacing_y, 0])
        right1 = root_anchor + np.array([offset_x * 1.4, level_spacing_y, 0])
        level1_nodes = [
            Dot(left1, radius=0.1, color=BLUE),
            Dot(right1, radius=0.1, color=BLUE)
        ]
        # Level 2
        left2a = left1 + np.array([offset_x, -level_spacing_y, 0])
        left2b = left1 + np.array([offset_x, level_spacing_y, 0])
        right2a = right1 + np.array([offset_x, -level_spacing_y, 0])
        right2b = right1 + np.array([offset_x, level_spacing_y, 0])
        level2_nodes = [
            Dot(left2a, radius=0.09, color=BLUE),
            Dot(left2b, radius=0.09, color=BLUE),
            Dot(right2a, radius=0.09, color=BLUE),
            Dot(right2b, radius=0.09, color=BLUE),
        ]
        # Level 3 (additional leaves)
        level3_nodes = []
        level3_parents = [left2a, left2b, right2a, right2b]
        for parent in level3_parents:
            child_up = parent + np.array([offset_x * 0.9, level_spacing_y * 0.8, 0])
            child_down = parent + np.array([offset_x * 0.9, -level_spacing_y * 0.8, 0])
            level3_nodes.append(Dot(child_up, radius=0.08, color=BLUE))
            level3_nodes.append(Dot(child_down, radius=0.08, color=BLUE))
        
        # Edges by level
        edges1 = VGroup(
            Line(root_anchor, left1, color=BLUE, stroke_width=2),
            Line(root_anchor, right1, color=BLUE, stroke_width=2),
        )
        edges2 = VGroup(
            Line(left1, left2a, color=BLUE, stroke_width=1.8),
            Line(left1, left2b, color=BLUE, stroke_width=1.8),
            Line(right1, right2a, color=BLUE, stroke_width=1.8),
            Line(right1, right2b, color=BLUE, stroke_width=1.8),
        )
        edges3 = VGroup()
        for parent in level3_parents:
            child_up = parent + np.array([offset_x * 0.9, level_spacing_y * 0.8, 0])
            child_down = parent + np.array([offset_x * 0.9, -level_spacing_y * 0.8, 0])
            edges3.add(Line(parent, child_up, color=BLUE, stroke_width=1.5))
            edges3.add(Line(parent, child_down, color=BLUE, stroke_width=1.5))
        
        tree_nodes_group = VGroup(
            root_node,
            *level1_nodes,
            *level2_nodes,
            *level3_nodes
        )
        
        # Animate growth left-to-right by levels
        self.play(FadeIn(root_node), run_time=0.4)
        self.play(Create(edges1), FadeIn(VGroup(*level1_nodes)), run_time=0.5)
        self.play(Create(edges2), FadeIn(VGroup(*level2_nodes)), run_time=0.6)
        self.play(Create(edges3), FadeIn(VGroup(*level3_nodes)), run_time=0.6)
        
        # Small pulse to emphasize growth (no scaling to keep alignment)
        pulse = tree_nodes_group.copy().set_color(YELLOW).set_opacity(0.6)
        self.play(FadeIn(pulse, run_time=0.2))
        self.play(pulse.animate.set_opacity(0), run_time=0.6)
        
        self.play(FadeOut(VGroup(prompt_group, tree_nodes_group, edges1, edges2, edges3)), run_time=0.8)
        
        # Transition to Scene 3
        scene2_group = VGroup(title2)
        self.play(FadeOut(scene2_group), run_time=0.5)
        
        # Scene 3: Growth Chart
        title3 = Text(
            "AI-ready data center capacity is growing\n33% per year",
            font_size=42,
            color=WHITE
        ).center().shift(UP * 3.6)  # Higher to avoid overlap with visuals
        
        self.play(Write(title3), run_time=1.5)
        
        years = ["2024", "2025", "2026", "2027"]
        heights = [1.6, 2.0, 2.6, 3.2]  # balanced heights
        base_y = -2.0  # move visuals down to separate from text
        bars = VGroup()
        half_overlays = VGroup()
        labels3 = VGroup()
        
        # Create bars and labels (labels visible from the start)
        for i, (year, height) in enumerate(zip(years, heights)):
            x = (i - 1.5) * 1.8
            bar = Rectangle(width=1.5, height=0.02, color=TEAL, fill_opacity=0.7, stroke_width=4)
            bar.move_to(np.array([x, base_y + 0.01, 0]))
            bars.add(bar)
            label = Text(year, font_size=40, color=WHITE).move_to(np.array([x, base_y - 0.35, 0]))
            labels3.add(label)
        self.add(labels3)
        
        # First animate blue bars growing from bottom
        for bar, height in zip(bars, heights):
            target_center = np.array([bar.get_center()[0], base_y + height / 2, 0])
            self.play(
                bar.animate.stretch_to_fit_height(height).move_to(target_center),
                run_time=0.45
            )
        
        # Then +33% YoY
        growth_text = Text("+33% YoY", font_size=46, color=YELLOW, weight=BOLD).center().shift(UP * 2.4)
        self.play(FadeIn(growth_text), run_time=0.6)
        
        # Then animate yellow half overlays and show half-label together
        half_label = Text("AI is driving nearly half that surge", font_size=36, color=YELLOW)
        half_label.next_to(bars, DOWN, buff=0.8)
        for bar, height in zip(bars, heights):
            x = bar.get_center()[0]
            overlay = Rectangle(width=1.5, height=0.02, color=YELLOW, fill_opacity=0.4, stroke_width=0)
            overlay.move_to(np.array([x, base_y + 0.01, 0]))
            half_overlays.add(overlay)
            half_target_center = np.array([x, base_y + (height * 0.5) / 2, 0])
            self.play(
                overlay.animate.stretch_to_fit_height(height * 0.5).move_to(half_target_center),
                run_time=0.35
            )
        self.play(FadeIn(half_label), run_time=1.0)
        self.wait(0.4)
        
        # Transition to Scene 4
        scene3_group = VGroup(title3, bars, labels3, growth_text, half_overlays, half_label)
        self.play(FadeOut(scene3_group), run_time=0.8)
        
        # Scene 4: Hyperscale Campuses
        title4 = Text(
            "Most work happening inside\ncolossal hyperscale campuses",
            font_size=42,
            color=WHITE
        ).center().shift(UP * 3.0)  # Centered high, away from edges
        
        self.play(Write(title4), run_time=1.5)
        
        us_outline = Rectangle(width=8, height=4.5, color=GRAY, fill_opacity=0.1, stroke_width=4).shift(DOWN * 0.7)
        self.play(Create(us_outline), run_time=0.8)
        
        buildings4 = VGroup()
        building_positions = [
            np.array([-2.5, 0.3, 0]),
            np.array([1.8, 0.6, 0]),
            np.array([-0.8, -1.8, 0]),
            np.array([2.8, -1.5, 0])
        ]
        
        for pos in building_positions:
            building = Rectangle(width=2.2, height=1.7, color=TEAL, fill_opacity=0.4, stroke_width=4).move_to(pos)
            racks = VGroup()
            for i in range(3):
                for j in range(2):
                    rack = Square(side_length=0.22, color=WHITE, fill_opacity=0.6)
                    rack.move_to(building.get_center() + RIGHT * (i - 1) * 0.3 + UP * (j - 0.5) * 0.3)
                    racks.add(rack)
            building_group = VGroup(building, racks)
            buildings4.add(building_group)
        
        for building in buildings4:
            self.play(FadeIn(building), run_time=0.4)
        
        bubble_text = Text("Hyperscale Campuses", font_size=38, color=YELLOW).center().shift(DOWN * 5.0)  # Move further down
        self.play(FadeIn(bubble_text), run_time=0.8)
        
        circle = Circle(radius=0.6, color=YELLOW, stroke_width=4).move_to(buildings4[0].get_center())
        percent_text = Text("65% by\ndecade's end", font_size=32, color=YELLOW).move_to(circle.get_center() + LEFT * 2.5)
        self.play(Create(circle), FadeIn(percent_text), run_time=0.8)
        
        for _ in range(2):
            pulse = circle.copy()
            pulse.scale(1.5)
            pulse.set_opacity(0.3)
            self.play(pulse.animate.set_opacity(0), run_time=0.6)
        self.wait(0.5)
        
        # Transition to Scene 5
        scene4_group = VGroup(title4, us_outline, buildings4, bubble_text, circle, percent_text)
        self.play(FadeOut(scene4_group), run_time=0.8)
        
        # Scene 5: Real Estate
        sentences5 = [
            "The first opportunity is real estate.",
            "Data centers have physical limits,",
            "Vacancy rates in key markets have dropped near zero.",
            "This is driving rentals and long-term leases."
        ]
        text_lines5 = [
            Text(s, font_size=34, color=WHITE).center()
            for s in sentences5
        ]
        current_text = None
        # Pre-build visuals (grid and vacancy meter)
        grid_size = 4
        grid = VGroup()
        buildings5 = []
        spacing = 1.3
        start_pos = np.array([-3.0, -0.2, 0])  # move grid up and left to center visuals
        
        for i in range(grid_size):
            for j in range(grid_size):
                pos = start_pos + np.array([j * spacing, -i * spacing, 0])
                building = VGroup(
                    Rectangle(width=0.7, height=0.7, color=TEAL, fill_opacity=0.5, stroke_width=3),
                    Polygon(np.array([-0.35, 0.35, 0]), np.array([0.35, 0.35, 0]), np.array([0, 0.6, 0]),
                           color=TEAL, fill_opacity=0.5, stroke_width=3)
                ).move_to(pos)
                grid.add(building)
                buildings5.append((building, pos))
        
        meter_bg = Rectangle(width=0.5, height=2.5, color=GRAY, fill_opacity=0.3, stroke_width=4).shift(RIGHT * 3.2 + DOWN * 0.8)
        meter_fill = Rectangle(width=0.5, height=2.5, color=RED, fill_opacity=0.8, stroke_width=0)
        meter_fill.align_to(meter_bg, DOWN).align_to(meter_bg, RIGHT)
        meter_label = Text("100%", font_size=34, color=RED).next_to(meter_bg, UP, buff=0.2)
        vacancy_label = Text("Vacancy", font_size=32, color=WHITE).next_to(meter_bg, DOWN, buff=0.4)
        
        # Show first sentence with static visuals; only one line on screen at a time
        for i, line in enumerate(text_lines5):
            line.shift(UP * 4.4)
            # Clear previous line if any
            if current_text is not None:
                self.play(FadeOut(current_text), run_time=0.3)
            if i == 0:
                self.play(FadeIn(line, grid, meter_bg, meter_fill, meter_label, vacancy_label), run_time=0.7)
            else:
                self.play(FadeIn(line), run_time=0.5)
                self.wait(0.5)
                if i == 2:
                    self.wait(0.5)  # hold "Vacancy rates..." a bit longer
            
            # On second sentence, animate fills and vacancy shrink
            if i == 1:
                fill_order = list(range(len(buildings5)))
                np.random.shuffle(fill_order)
                for idx in fill_order:
                    building, pos = buildings5[idx]
                    self.play(
                        building.animate.set_fill(RED, opacity=0.8).set_stroke(RED),
                        run_time=0.15
                    )
                self.play(
                    meter_fill.animate.set_height(0.1).align_to(meter_bg, DOWN),
                    run_time=0.9
                )
                meter_label_0 = Text("0%", font_size=34, color=RED).move_to(meter_label.get_center())
                self.play(Transform(meter_label, meter_label_0), run_time=0.4)
            current_text = line
        
        overlay_text5 = Text("Rents ↑ & Long-term leases ↑", font_size=38, color=YELLOW).center().shift(DOWN * 8.0)  # Lower to avoid visuals
        self.play(FadeIn(overlay_text5), run_time=1)
        self.wait(0.5)
        
        # Transition to Scene 6
        scene5_group = VGroup(grid, meter_bg, meter_fill, meter_label, vacancy_label, overlay_text5, current_text)
        self.play(FadeOut(scene5_group), run_time=0.8)
        
        # Scene 6: Electricity Constraint
        title6 = Text("Electricity may be the toughest constraint", font_size=42, color=WHITE).center().shift(UP * 3.0)  # Centered high, away from edges
        self.play(Write(title6), run_time=1.5)
        
        old_chip = Rectangle(width=1.8, height=1.2, color=GRAY, fill_opacity=0.3, stroke_width=4).shift(LEFT * 2.5 + DOWN * 0.5)
        old_glow = Circle(radius=1, color=GRAY, fill_opacity=0.1, stroke_width=0).move_to(old_chip.get_center())
        old_label = Text("Old Chip", font_size=36, color=GRAY).next_to(old_chip, DOWN, buff=0.5)
        old_group = VGroup(old_glow, old_chip, old_label)
        
        new_chip_color = "#8ad7ff"
        new_chip = Rectangle(width=2.7, height=1.8, color=new_chip_color, fill_opacity=0.5, stroke_width=4).shift(RIGHT * 2.5 + DOWN * 0.5)
        new_glow = Circle(radius=1.5, color=new_chip_color, fill_opacity=0.2, stroke_width=0).move_to(new_chip.get_center())
        new_label = Text("New AI Chip", font_size=36, color=new_chip_color).next_to(new_chip, DOWN, buff=0.5)
        new_group = VGroup(new_glow, new_chip, new_label)
        
        self.play(FadeIn(old_group), run_time=1)
        self.wait(0.3)
        self.play(Transform(old_group, new_group), FadeIn(new_group), run_time=1.5)
        
        # Power bar with wire from new AI chip: starts 1/3 filled, then fills up
        bar_bg = Rectangle(width=0.9, height=2.4, color=WHITE, fill_opacity=0.1, stroke_width=4).move_to(LEFT * 1.8 + DOWN * 1.6)
        bar_fill = Rectangle(width=bar_bg.width, height=bar_bg.height / 3, color=YELLOW, fill_opacity=0.85, stroke_width=0)
        bar_fill.move_to(bar_bg.get_center()).align_to(bar_bg, DOWN)
        power_label = Text("Power", font_size=38, color=WHITE).next_to(bar_bg, DOWN, buff=0.3)
        wire = Line(
            new_chip.get_left() + LEFT * 0.1,
            bar_bg.get_right() + RIGHT * 0.15,
            color=GRAY,
            stroke_width=5
        )
        power_text = Text(
            "New AI chips consume triple the power\nof older models...",
            font_size=36,
            color=YELLOW,
            line_spacing=0.8
        ).center().shift(DOWN * 4.5)
        
        self.play(Create(wire), FadeIn(bar_bg), FadeIn(bar_fill), FadeIn(power_label), run_time=1.0)
        self.play(
            bar_fill.animate.stretch_to_fit_height(bar_bg.height, about_edge=DOWN),
            run_time=1.4
        )
        self.play(FadeIn(power_text), run_time=0.8)
        self.wait(0.4)
        
        # Transition to Scene 7
        scene6_group = VGroup(title6, old_group, new_group, bar_bg, bar_fill, power_label, wire, power_text)
        self.play(FadeOut(scene6_group), run_time=0.8)
        
        # Scene 7: Energy Demand
        title7 = Text("Driving US demand toward\n50-60 extra gigawatts by 2030", font_size=42, color=WHITE).center().shift(UP * 3.0)  # Centered high, away from edges
        self.play(Write(title7), run_time=1.5)
        
        # Exponential line chart: Years 2025-2030 on x-axis, Power on y-axis
        origin = np.array([-3.8, -2.3, 0])
        x_len = 6.5
        y_len = 4.5
        x_axis = Line(origin, origin + RIGHT * x_len, color=GRAY, stroke_width=4)
        y_axis = Line(origin, origin + UP * y_len, color=GRAY, stroke_width=4)
        x_label = Text("Year", font_size=34, color=WHITE).next_to(x_axis, RIGHT, buff=0.2)
        y_label = Text("Power", font_size=34, color=WHITE).next_to(y_axis, UP, buff=0.2)
        
        years = ["2025", "2026", "2027", "2028", "2029", "2030"]
        ticks = VGroup()
        year_labels = VGroup()
        for i, yr in enumerate(years):
            x_pos = origin + RIGHT * (x_len * (i / (len(years) - 1)))
            tick = Line(x_pos + DOWN * 0.12, x_pos + UP * 0.12, color=GRAY, stroke_width=3)
            ticks.add(tick)
            lbl = Text(yr, font_size=30, color=WHITE).next_to(tick, DOWN, buff=0.15)
            year_labels.add(lbl)
        
        ts = np.linspace(0, 1, 14)
        pts = []
        for t in ts:
            x = t * x_len
            y = (np.exp(2.4 * t) - 1) / (np.exp(2.4) - 1) * y_len
            pts.append(origin + np.array([x, y, 0]))
        power_curve = VMobject(color=YELLOW, stroke_width=6)
        power_curve.set_points_smoothly(pts)
        end_dot = Dot(pts[-1], radius=0.08, color=YELLOW)
        gw_label = Text("60 gigawatts", font_size=36, color=YELLOW).next_to(end_dot, UP + RIGHT, buff=0.25)
        
        chart_group = VGroup(x_axis, y_axis, ticks, year_labels, x_label, y_label, power_curve, end_dot, gw_label)
        chart_group.shift(DOWN * 1.2)
        
        self.play(Create(x_axis), Create(y_axis), FadeIn(ticks), FadeIn(year_labels), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(Create(power_curve), run_time=1.8)
        self.play(FadeIn(end_dot), FadeIn(gw_label), run_time=0.8)
        self.wait(0.5)
        
        # Transition to Scene 8
        scene7_group = VGroup(title7, chart_group)
        self.play(FadeOut(scene7_group), run_time=0.8)
        
        # Scene 8: Grid Construction
        title8 = Text("Delivering that energy is harder\nthan producing it", font_size=42, color=WHITE).center().shift(UP * 3.0)  # Centered high, away from edges
        self.play(Write(title8), run_time=1.5)
        
        plant = VGroup(
            Rectangle(width=1.5, height=1.5, color=YELLOW, fill_opacity=0.6, stroke_width=4),
            Polygon(np.array([-0.75, 0.75, 0]), np.array([0.75, 0.75, 0]), np.array([0, 1.2, 0]),
                   color=YELLOW, fill_opacity=0.6, stroke_width=4)
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        plant_label = Text("Power Plant", font_size=36, color=WHITE).next_to(plant, DOWN, buff=0.5)
        
        towers = VGroup()
        for i in range(3):
            tower = VGroup(
                Line(np.array([-0.12, 0, 0]), np.array([0, 1, 0]), color=GRAY, stroke_width=4),
                Line(np.array([0.12, 0, 0]), np.array([0, 1, 0]), color=GRAY, stroke_width=4),
                Line(np.array([-0.12, 0.5, 0]), np.array([0.12, 0.5, 0]), color=GRAY, stroke_width=3)
            ).shift(RIGHT * (i - 1) * 1.8 + DOWN * 0.5)
            towers.add(tower)
        
        data_center = Rectangle(width=1.8, height=1.8, color=TEAL, fill_opacity=0.6, stroke_width=4).shift(RIGHT * 3.5 + DOWN * 0.5)
        dc_label = Text("Data Center", font_size=36, color=WHITE).next_to(data_center, DOWN, buff=0.5)
        
        self.play(FadeIn(plant), FadeIn(plant_label), run_time=0.8)
        self.play(FadeIn(towers), run_time=0.8)
        self.play(FadeIn(data_center), FadeIn(dc_label), run_time=0.8)
        
        power_lines = VGroup()
        positions8 = [
            (plant.get_right(), towers[0].get_left()),
            (towers[0].get_right(), towers[1].get_left()),
            (towers[1].get_right(), towers[2].get_left()),
            (towers[2].get_right(), data_center.get_left())
        ]
        
        for start, end in positions8:
            line = Line(start, end, color=YELLOW, stroke_width=4)
            power_lines.add(line)
        
        self.play(Create(power_lines), run_time=1)
        
        for _ in range(3):
            flicker_lines = power_lines.copy()
            flicker_lines.set_color(RED)
            flicker_lines.set_opacity(0.5)
            self.play(flicker_lines.animate.set_opacity(0), run_time=0.3)
        
        grid_label = Text(
            "This drives demand for power grid\nconstruction",
            font_size=40,
            color=YELLOW,
            weight=BOLD,
            line_spacing=0.85
        )
        grid_label.center().shift(DOWN * 4.0)
        self.play(FadeIn(grid_label), run_time=1)
        self.wait(0.5)
        
        # Transition to Scene 9
        scene8_group = VGroup(title8, plant, plant_label, towers, data_center, dc_label, power_lines, grid_label)
        self.play(FadeOut(scene8_group), run_time=0.8)
        
        # Scene 9: Cooling
        title9 = Text("Cooling is the final frontier", font_size=42, color=WHITE).center().shift(UP * 3.0)  # Centered high, away from edges
        cooling_detail = Text(
            "Air alone can’t keep up —\n"
            "data centers are rapidly turning\n"
            "to liquid and hybrid cooling\n"
            "as GPU heat soars.",
            font_size=40,
            color=WHITE,
            line_spacing=0.95
        ).center().shift(UP * 5.0)
        
        racks = VGroup()
        for i in range(3):
            rack = Rectangle(width=1, height=2.5, color=GRAY, fill_opacity=0.4, stroke_width=4).shift(RIGHT * (i - 1) * 1.5 + DOWN * 0.5)
            for j in range(4):
                unit = Rectangle(width=0.85, height=0.5, color=RED, fill_opacity=0.6, stroke_width=3)
                unit.move_to(rack.get_center() + UP * (1.8 - j * 0.6 - 0.25))
                rack.add(unit)
            racks.add(rack)
        
        self.play(Write(title9), FadeIn(racks), run_time=1.2)
        
        heat_waves = VGroup()
        for rack in racks:
            for _ in range(3):
                wave = Arc(radius=0.5, angle=PI, start_angle=0, color=RED, stroke_width=3, fill_opacity=0.3)
                wave.move_to(rack.get_top() + UP * 0.3)
                heat_waves.add(wave)
        
        self.play(Create(heat_waves), heat_waves.animate.shift(UP * 0.6).set_opacity(0.1), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(title9), run_time=0.6)
        self.remove(title9)  # ensure title is fully gone before the next line
        title9 = None  # guard against re-adding
        self.wait(0.4)
        self.play(Write(cooling_detail), run_time=1.0)
        
        pipes = VGroup()
        for rack in racks:
            pipe = Rectangle(width=0.75, height=0.4, color=BLUE, fill_opacity=0.8, stroke_width=4)
            pipe.move_to(rack.get_bottom() + DOWN * 0.6)
            pipes.add(pipe)
        
        droplets = VGroup()
        for pipe in pipes:
            droplet = Circle(radius=0.12, color=BLUE, fill_opacity=0.9).move_to(pipe.get_bottom() + DOWN * 0.6)
            droplets.add(droplet)
        
        self.play(FadeIn(droplets), run_time=0.5)
        self.play(Transform(droplets, pipes), FadeIn(pipes), run_time=1)
        self.play(pipes.animate.shift(UP * 3), heat_waves.animate.set_opacity(0),
                 racks.animate.set_color(BLUE).set_fill_opacity(0.3), run_time=2)
        
        cooling_label = Text("Liquid Cooling", font_size=40, color=BLUE, weight=BOLD).center().shift(DOWN * 4.0)  # Centered with margins from edges
        self.play(FadeIn(cooling_label), run_time=1)
        self.wait(0.5)
        
        # Transition to Scene 10
        scene9_group = VGroup(cooling_detail, racks, heat_waves, pipes, droplets, cooling_label)
        self.play(FadeOut(scene9_group), run_time=0.8)
        
        # Scene 10: Headlines
        title10 = Text("Headlines focus on AI breakthroughs\nbut behind the scenes...", font_size=42, color=WHITE).center().shift(UP * 3.0)  # Centered high, away from edges
        follow_text = Text(
            "show growth in companies\n"
            "that can rent centers,\n"
            "build grids, and cool rooms.",
            font_size=40,
            color=WHITE,
            line_spacing=0.95
        ).center().shift(UP * 3.0)
        
        # Neural network (many nodes)
        nn_nodes = []
        layer_x = [-2.2, -1.4, -0.6, 0.2, 1.0]
        for lx in layer_x:
            for ly in [0.9, 0.4, -0.1, -0.6]:
                nn_nodes.append(np.array([lx, ly, 0]))
        neural_net = VGroup()
        for node in nn_nodes:
            neural_net.add(Dot(node, radius=0.09, color=YELLOW))
        for a in range(len(nn_nodes)):
            for b in range(len(nn_nodes)):
                if a != b and np.random.rand() < 0.18:
                    line = Line(nn_nodes[a], nn_nodes[b], color=YELLOW, stroke_width=1.5)
                    line.set_opacity(0.4)
                    neural_net.add(line)
        neural_net.shift(LEFT * 1.0 + DOWN * 0.5)
        
        self.play(Write(title10), FadeIn(neural_net, scale=1.1), run_time=1.5)
        self.play(FadeOut(title10), run_time=0.8)
        self.wait(0.2)
        self.play(
            Write(follow_text),
            neural_net.animate.shift(LEFT * 1.5).set_opacity(0.25),
            run_time=1.2
        )
        
        # Data center stack + grid + cooling (vertical column)
        dc_body = Rectangle(width=1.2, height=2.2, color=TEAL, fill_opacity=0.5, stroke_width=4)
        slots = VGroup()
        for i in range(5):
            slot = Rectangle(width=0.9, height=0.25, color=TEAL, fill_opacity=0.8, stroke_width=2)
            slot.move_to(dc_body.get_top() + DOWN * (0.35 + i * 0.35))
            slots.add(slot)
        dc_group = VGroup(dc_body, slots).shift(RIGHT * 1.5 + UP * 0.1)
        dc_label = Text("Data Center", font_size=32, color=TEAL).next_to(dc_group, DOWN, buff=0.3)
        
        grid_shape = VGroup(
            Rectangle(width=1.3, height=0.35, color=YELLOW, fill_opacity=0.0, stroke_width=3),
            Line(LEFT * 0.65, RIGHT * 0.65, color=YELLOW, stroke_width=2).shift(DOWN * 0.1),
            Line(LEFT * 0.65, RIGHT * 0.65, color=YELLOW, stroke_width=2).shift(UP * 0.1),
            Line(UP * 0.17 + LEFT * 0.65, UP * 0.17 + RIGHT * 0.65, color=YELLOW, stroke_width=2)
        ).move_to(dc_group.get_bottom() + DOWN * 2.0)
        grid_label = Text("Grid", font_size=32, color=YELLOW).next_to(grid_shape, DOWN, buff=0.25)
        
        snowflake = VGroup()
        for i in range(6):
            angle = i * PI / 3
            main = Line(ORIGIN, np.array([0.4 * np.cos(angle), 0.4 * np.sin(angle), 0]), color=BLUE, stroke_width=4)
            side1 = Line(main.get_end(), main.get_end() + np.array([0.15 * np.cos(angle + PI / 6), 0.15 * np.sin(angle + PI / 6), 0]), color=BLUE, stroke_width=3)
            side2 = Line(main.get_end(), main.get_end() + np.array([0.15 * np.cos(angle - PI / 6), 0.15 * np.sin(angle - PI / 6), 0]), color=BLUE, stroke_width=3)
            snowflake.add(main, side1, side2)
        snowflake.move_to(grid_shape.get_bottom() + DOWN * 2.5)
        cooling_label = Text("Cooling", font_size=32, color=BLUE).next_to(snowflake, DOWN, buff=0.25)
        
        infra_column = VGroup(dc_group, dc_label, grid_shape, grid_label, snowflake, cooling_label)
        self.play(
            LaggedStart(*[FadeIn(mob, scale=0.6) for mob in infra_column], lag_ratio=0.12),
            run_time=1.2
        )
        glow_effects = infra_column.copy().set_opacity(0.25).scale(1.05)
        self.add(glow_effects)
        self.play(glow_effects.animate.set_opacity(0.4).scale(1.05), run_time=0.5, rate_func=there_and_back)
        self.play(glow_effects.animate.set_opacity(0.35).scale(1.02), run_time=0.5, rate_func=there_and_back)
        self.wait(1.0)


"""
To render the full continuous video in vertical/portrait format (9:16):
    manim -pql -n --resolution 1080,1920 Bloom2.py FullAnimation
    
    The -n flag disables auto-preview (prevents xdg-open errors in WSL/Windows)
    The --resolution 1080,1920 sets vertical phone-style format (1080x1920 pixels)
    The FullAnimation class also sets frame dimensions for vertical format

For higher quality, use -pqh instead of -pql:
    manim -pqh -n --resolution 1080,1920 Bloom2.py FullAnimation

To render individual scenes separately (these are still in landscape format):
    manim -pql -n Bloom2.py Scene1_ThreeSecretAreas
    manim -pql -n Bloom2.py Scene2_AIQuery
    etc.

Note: The video file will still be created in the media/videos/Bloom2/ directory
even if the preview fails. The -n flag just prevents the auto-open attempt.
"""
