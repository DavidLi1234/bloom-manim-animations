from manim import *
import numpy as np

"""
This script is optimized for vertical/portrait format (1080x1920 resolution, 9:16 aspect ratio).

To render in vertical format:
    manim -pql --resolution 1080,1920 new_Bloom2.py SceneName

For higher quality:
    manim -pqh --resolution 1080,1920 new_Bloom2.py SceneName

Available scenes:
    - TitleScene
    - Scene1_AIDataCenter
    - Scene2_Constraints
    - Scene3_Hyperscale
    - Scene4_PowerGrid
    - Scene5_Cooling
    - Scene6_CTA
"""

# Color scheme
ACCENT_COLOR = "#88DDFF"  # Pale cyan for data flow
BG_COLOR = "#0a0a0a"  # Dark background
TEXT_COLOR = WHITE
GRAY_COLOR = GRAY_B


def make_caption(text: str, font_size: int):
    # Use Paragraph so multi-line captions are truly center-aligned.
    return Paragraph(
        *text.split("\n"),
        alignment="center",
        font_size=font_size,
        weight=THIN,
        color=TEXT_COLOR,
    )


class TitleScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Title text - larger and at the top
        title = Text(
            "Lesser-Known Growth Areas\nof the AI–Data Center Boom",
            font_size=50,
            weight=THIN,
            color=TEXT_COLOR
        )
        title.move_to(UP * 4.2)
        
        # Create multiple data center icons (bar chart style)
        num_centers = 4
        base_width = 0.9  # Wider boxes
        base_x_spacing = 2.0  # Even more spacing between boxes
        base_y = -1.5  # Higher bottom position (more screen space)
        heights = [1.8, 2.4, 3.0, 3.6]  # Taller heights
        
        data_centers = VGroup()
        node_networks = VGroup()
        
        for i in range(num_centers):
            # Calculate position (centered horizontally)
            x_offset = (i - (num_centers - 1) / 2) * base_x_spacing
            center_x = x_offset
            
            # Create data center icon (vertical rectangle with smaller rectangles inside)
            outer_rect = Rectangle(
                width=base_width,
                height=heights[i],
                stroke_color=ACCENT_COLOR,  # Blue color
                stroke_width=6,  # Even thicker lines
                fill_opacity=0
            )
            outer_rect.move_to([center_x, base_y + heights[i] / 2, 0])
            
            # Add smaller rectangles inside (server racks)
            num_racks = 3 + i  # More racks for taller centers
            rack_width = base_width * 0.7
            rack_height = heights[i] / (num_racks + 1)
            racks = VGroup()
            
            for j in range(num_racks):
                rack = Rectangle(
                    width=rack_width,
                    height=rack_height * 0.6,
                    stroke_color=ACCENT_COLOR,  # Blue color
                    stroke_width=3,  # Even thicker
                    fill_opacity=0
                )
                rack.move_to([
                    center_x,
                    base_y + (j + 1) * (heights[i] / (num_racks + 1)),
                    0
                ])
                racks.add(rack)
            
            data_center = VGroup(outer_rect, racks)
            data_centers.add(data_center)
            
            # Create tree-style node network below each data center
            # Network size proportional to data center height
            network_scale = 0.6 + (i * 0.2)  # Larger scale, more visible
            num_levels = 2 + i  # More levels for larger centers
            # Generate tree structure: each level has more nodes (1, 2, 3, 4, ...)
            num_nodes_per_level = [min(level + 1, 4) for level in range(num_levels)]
            
            network_nodes = VGroup()
            network_connections = VGroup()
            
            # Create nodes in tree structure
            node_positions = {}
            level_spacing = 0.5 * network_scale  # More spacing between levels
            node_spacing = 0.7 * network_scale  # More spacing between nodes
            
            # Position tree directly below the box
            box_bottom = base_y  # Bottom of the box
            tree_top_y = box_bottom - 0.3  # Start tree just below box
            
            for level in range(num_levels):
                num_nodes = num_nodes_per_level[level]
                y_pos = tree_top_y - (level * level_spacing)
                
                for node_idx in range(num_nodes):
                    if level == 0:
                        # Root node (centered)
                        x_pos = center_x
                    else:
                        # Child nodes (spread out)
                        total_width = (num_nodes - 1) * node_spacing
                        x_pos = center_x - total_width / 2 + node_idx * node_spacing
                    
                    node = Dot(
                        [x_pos, y_pos, 0],
                        radius=0.08 * network_scale,  # Larger dots
                        color=ACCENT_COLOR  # Blue dots
                    ).set_opacity(0.8)  # More visible
                    network_nodes.add(node)
                    node_positions[(level, node_idx)] = [x_pos, y_pos, 0]
            
            # Connect nodes in tree structure
            for level in range(1, num_levels):
                num_parents = num_nodes_per_level[level - 1]
                num_children = num_nodes_per_level[level]
                
                for child_idx in range(num_children):
                    # Connect to parent (distribute children across parents)
                    parent_idx = min(child_idx * num_parents // num_children, num_parents - 1)
                    
                    if (level - 1, parent_idx) in node_positions and (level, child_idx) in node_positions:
                        connection = Line(
                            node_positions[(level - 1, parent_idx)],
                            node_positions[(level, child_idx)],
                            stroke_color=ACCENT_COLOR,  # Blue lines
                            stroke_width=1.5  # Thicker lines
                        ).set_opacity(0.6)  # More visible
                        network_connections.add(connection)
            
            network = VGroup(network_connections, network_nodes)
            node_networks.add(network)
        
        # Set up all data centers with initial height 0
        for i, data_center in enumerate(data_centers):
            outer_rect = data_center[0]
            initial_height = 0.1  # Small initial height
            outer_rect.stretch(initial_height / heights[i], dim=1, about_point=[outer_rect.get_left()[0], base_y, 0])
            outer_rect.move_to([outer_rect.get_center()[0], base_y + initial_height / 2, 0])
            
            # Hide racks initially
            for rack in data_center[1]:
                rack.set_opacity(0)
            
            self.add(data_center)
        
        # Animate title and data centers - overlapping sequential, total 3 seconds
        animation_duration = 2.5  # Main animation duration
        
        # Create title animation
        title_anim = Write(title)
        
        # Create data center animations that will overlap sequentially
        # Each bar expands and graph draws from scratch, but they overlap in time
        individual_duration = 0.65  # Each bar/graph animation duration
        data_center_anims = []
        for i, data_center in enumerate(data_centers):
            outer_rect = data_center[0]
            target_height = heights[i]
            initial_height = 0.1
            
            # Each data center animation group - bar grows and graph fades in
            grow_anim = AnimationGroup(
                outer_rect.animate.stretch(target_height / initial_height, dim=1, about_point=[outer_rect.get_left()[0], base_y, 0])
                .move_to([outer_rect.get_center()[0], base_y + target_height / 2, 0]),
                *[rack.animate.set_opacity(1) for rack in data_center[1]],
                FadeIn(node_networks[i]),  # Graph draws from scratch
                run_time=individual_duration
            )
            data_center_anims.append(grow_anim)
        
        # Play title and data centers simultaneously, with data centers overlapping sequentially
        # Use LaggedStart to create sequential overlap - each starts before previous finishes
        # lag_ratio=0.5 means each starts when previous is 50% done (50% overlap)
        lagged_data_centers = LaggedStart(
            *data_center_anims,
            lag_ratio=0.5  # 50% overlap - each starts when previous is 50% done
        )
        
        self.play(
            title_anim,
            lagged_data_centers,
            run_time=animation_duration
        )
        
        self.wait(0.5)
        
        # Fade out all visuals at the end
        all_visuals = VGroup(title, data_centers, node_networks)
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene1_AIDataCenter(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "Artificial intelligence runs on data,\nand data lives in physical buildings\ncalled data centers",
            font_size=38,
        )
        caption.move_to(UP * 3.5)
        
        # Vertical offset to shift everything down
        vertical_offset = DOWN * 1.5
        
        # Scale factor for everything
        scale_factor = 1.5
        
        # AI Query Box - start in center, scaled larger, shifted down
        query_box_width = 4.5 * scale_factor
        query_box_height = 1.2 * scale_factor
        query_box = Rectangle(
            width=query_box_width,
            height=query_box_height,
            stroke_color=TEXT_COLOR,
            stroke_width=3,
            fill_opacity=0
        )
        query_box.move_to(ORIGIN + vertical_offset)
        
        query_text = Text(
            "Ask AI anything...",
            font_size=36 * scale_factor,
            weight=THIN,
            color=TEXT_COLOR
        )
        query_text.move_to(query_box.get_center())
        
        query_group = VGroup(query_box, query_text)
        query_group.move_to(ORIGIN + vertical_offset)
        
        # Final position for query box (left side, smaller, shifted down)
        query_final_scale = 0.6
        query_final_pos = LEFT * 3.5 + UP * 0.5 + vertical_offset
        
        # Data center icon - matching the image description, scaled larger, shorter, shifted down
        # Tall vertical rectangle with blue outline
        dc_width = 1.2 * scale_factor
        dc_height = 3.5 * scale_factor  # Made shorter (was 5.0)
        dc_outer = Rectangle(
            width=dc_width,
            height=dc_height,
            stroke_color=ACCENT_COLOR,
            stroke_width=4,
            fill_opacity=0
        )
        dc_outer.move_to(RIGHT * 3.0 + vertical_offset)
        
        # 6 smaller white-filled horizontal rectangles inside with separation
        num_servers = 6
        server_width = dc_width * 0.85
        server_height = 0.4 * scale_factor
        server_spacing = 0.15 * scale_factor  # Space between boxes
        total_height_needed = num_servers * server_height + (num_servers - 1) * server_spacing
        start_y = dc_outer.get_top()[1] - (dc_height - total_height_needed) / 2 - server_height / 2
        
        servers = VGroup()
        for i in range(num_servers):
            server = Rectangle(
                width=server_width,
                height=server_height,
                stroke_color=WHITE,
                stroke_width=1.5,
                fill_color=WHITE,
                fill_opacity=1
            )
            y_pos = start_y - i * (server_height + server_spacing)
            server.move_to([dc_outer.get_center()[0], y_pos, 0])
            servers.add(server)
        
        data_center = VGroup(dc_outer, servers)
        
        # Neural network style: input layer -> hidden layers -> output layer
        # Calculate positions after query box moves
        query_final_center = query_final_pos
        query_final_right = query_final_center + RIGHT * (query_box_width * query_final_scale / 2)
        dc_left = dc_outer.get_left()
        
        # Neural network layers - reduced nodes for less clutter
        num_hidden_layers = 2
        nodes_per_layer = 3
        nodes = VGroup()
        edges = VGroup()
        all_node_positions = []  # Store positions for each layer
        all_edges_list = []  # Store edge objects for path following
        
        # Create nodes in layers (neural network style)
        layer_positions = []
        for layer_idx in range(num_hidden_layers):
            # X position for this layer
            t = (layer_idx + 1) / (num_hidden_layers + 1)
            x = query_final_right[0] + (dc_left[0] - query_final_right[0]) * t
            
            # Y positions for nodes in this layer (distributed vertically)
            layer_nodes = []
            for node_idx in range(nodes_per_layer):
                # Distribute nodes vertically around the center
                y_offset = (node_idx - nodes_per_layer / 2 + 0.5) * (dc_height * 0.5 / max(nodes_per_layer - 1, 1))
                y = dc_outer.get_center()[1] + y_offset
                pos = [x, y, 0]
                layer_nodes.append(pos)
                all_node_positions.append(pos)
                
                # Create node
                node = Dot(radius=0.12 * scale_factor, color=ACCENT_COLOR)
                node.move_to(pos)
                nodes.add(node)
            
            layer_positions.append(layer_nodes)
        
        # Create edges in neural network style (each node connects to all nodes in next layer)
        # Edges from query box to first hidden layer
        for first_layer_node in layer_positions[0]:
            edge = Line(
                query_final_right,
                first_layer_node,
                stroke_color=ACCENT_COLOR,
                stroke_width=1.5 * scale_factor
            )
            edges.add(edge)
            all_edges_list.append(edge)
        
        # Edges between hidden layers
        for layer_idx in range(num_hidden_layers - 1):
            for source_node in layer_positions[layer_idx]:
                for target_node in layer_positions[layer_idx + 1]:
                    edge = Line(
                        source_node,
                        target_node,
                        stroke_color=ACCENT_COLOR,
                        stroke_width=1.5 * scale_factor
                    )
                    edges.add(edge)
                    all_edges_list.append(edge)
        
        # Edges from last hidden layer to data center
        for last_layer_node in layer_positions[-1]:
            edge = Line(
                last_layer_node,
                dc_left,
                stroke_color=ACCENT_COLOR,
                stroke_width=1.5 * scale_factor
            )
            edges.add(edge)
            all_edges_list.append(edge)
        
        # Label - scaled larger, shifted down
        label = Text("Data Center", font_size=32 * scale_factor, color=TEXT_COLOR, weight=THIN)
        label.next_to(dc_outer, DOWN, buff=0.5)
        
        # Yellow dots flowing from data center to query box following the edges
        num_packets = 12
        
        def create_packet():
            return Dot(radius=0.15 * scale_factor, color=YELLOW)
        
        # Helper function to find multiple paths from data center to query box
        def get_paths_from_dc_to_query(num_paths=3):
            paths = []
            for path_idx in range(num_paths):
                # Find a path through the network (reverse direction)
                # Start from data center, go through layers to query box
                path = [dc_left]
                
                # Go through layers in reverse, picking different nodes for each path
                for layer_idx in range(num_hidden_layers - 1, -1, -1):
                    layer_nodes = layer_positions[layer_idx]
                    # Cycle through nodes for different paths
                    node_idx = (path_idx + layer_idx) % len(layer_nodes)
                    path.append(layer_nodes[node_idx])
                
                path.append(query_final_right)
                paths.append(path)
            return paths
        
        # Animate everything simultaneously - starts the moment text begins playing
        self.play(
            Write(caption, run_time=2.5),
            FadeIn(query_group, run_time=0.5),
            query_group.animate.scale(query_final_scale).move_to(query_final_pos),
            LaggedStart(
                *[Create(edge) for edge in edges],
                *[FadeIn(node) for node in nodes],
                lag_ratio=0.05
            ),
            FadeIn(data_center),
            FadeIn(label),
            run_time=2.5
        )
        
        # Yellow dots flowing from data center to query box following multiple paths
        num_paths = 3
        paths = get_paths_from_dc_to_query(num_paths)
        
        for i in range(num_packets):
            # Choose a path for this packet (cycle through paths)
            path_idx = i % num_paths
            path_points = paths[path_idx]
            
            packet = create_packet()
            packet.move_to(path_points[0])  # Start at data center
            self.add(packet)
            
            # Animate along each segment of the path
            for segment_idx in range(len(path_points) - 1):
                start_point = path_points[segment_idx]
                end_point = path_points[segment_idx + 1]
                self.play(
                    packet.animate.move_to(end_point),
                    run_time=0.15,
                    rate_func=linear
                )
            
            self.remove(packet)
        
        self.wait(0.5)
        
        # Fade out all visuals at the end (including caption)
        all_visuals = VGroup(caption, query_group, nodes, edges, data_center, label)
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene2_Constraints(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "But data centers have constraints\nin terms of land, power and sustainability.\nCompanies that overcome these constraints grow\nand should be considered by retail investors.",
            font_size=36,
        )
        caption.move_to(UP * 3.5)

        # --- Single constraint visual: data center grows until it hits a constraint box ---
        # Constraint box
        constraint_box = Rectangle(
            width=4.8,
            height=5.3,
            stroke_color=GRAY_COLOR,
            stroke_width=2.5,
            fill_opacity=0
        ).move_to(DOWN * 1.25)

        constraint_label = Text(
            "land, power,\nheating constraints",
            font_size=26,
            color=TEXT_COLOR,
            weight=THIN
        )
        constraint_label.next_to(constraint_box, DOWN, buff=0.25)

        # Data center icon (minimal)
        dc_w, dc_h = 1.2, 2.0
        dc_outer = Rectangle(
            width=dc_w,
            height=dc_h,
            stroke_color=ACCENT_COLOR,
            stroke_width=5,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.25
        )
        racks = VGroup()
        rack_h = 0.18
        rack_inset = 0.28  # padding from top/bottom so racks never exceed outline
        inner_top = dc_outer.get_top()[1] - rack_inset
        inner_bottom = dc_outer.get_bottom()[1] + rack_inset
        ys = np.linspace(inner_top - rack_h / 2, inner_bottom + rack_h / 2, 6)
        for i, y in enumerate(ys):
            r = Rectangle(
                width=dc_w * 0.72,
                height=rack_h,
                stroke_color=TEXT_COLOR,
                stroke_width=1.5,
                fill_color=WHITE,
                fill_opacity=0.95
            )
            r.move_to([dc_outer.get_center()[0], y, 0])
            racks.add(r)

        data_center = VGroup(dc_outer, racks)
        data_center.move_to(constraint_box.get_center())

        # Start small so it can "grow into" the box
        data_center.scale(0.35)

        def vibrate(mob: Mobject, amp=0.09, steps=56):
            # True vibration: fast, small positional jitter (no rotation / no squash)
            orig = mob.get_center()
            anims = []
            for k in range(steps):
                dx = (amp if k % 2 == 0 else -amp)
                dy = (amp * 0.35 if (k // 2) % 2 == 0 else -(amp * 0.35))
                anims.append(mob.animate.shift(RIGHT * dx + UP * dy))
            anims.append(mob.animate.move_to(orig))
            return Succession(*anims)

        # Compute a target scale so the data center nearly touches the constraint box
        # (keep a little padding so it reads as "hitting the wall" without clipping)
        pad = 0.35
        target_w = constraint_box.width - pad
        target_h = constraint_box.height - pad
        base_w = data_center.width
        base_h = data_center.height
        target_scale = min(target_w / base_w, target_h / base_h) * 1.02

        # Everything starts the moment the text begins playing
        self.play(
            Write(caption, run_time=6.0),
            FadeIn(constraint_box, constraint_label, run_time=0.6),
            FadeIn(data_center, run_time=0.6),
            data_center.animate.scale(target_scale),
            run_time=6.0,
            rate_func=smooth
        )

        # Obvious vibration like it's trying to break out
        self.play(vibrate(data_center), run_time=2.8, rate_func=linear)

        # Linger to hit ~10s total (then fade)
        self.wait(0.6)

        # Fade out all visuals at the end (including caption)
        all_visuals = VGroup(caption, constraint_box, constraint_label, data_center)
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene3_Hyperscale(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "One area of growth is hyperscale data center\n"
            "real estate, where space is scarce and\n"
            "long-term leases are increasingly\n"
            "the business model.",
            font_size=36,
        )
        caption.move_to(UP * 3.5)

        # --- Visual: houses fill up + vacancy drains (portrait-friendly) ---
        def make_house(size=0.76):
            body = Square(
                side_length=size,
                stroke_color=GRAY_COLOR,
                stroke_width=2,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.35,
            )
            roof = Polygon(
                body.get_corner(UL),
                body.get_corner(UR),
                body.get_top() + UP * (size * 0.55),
                stroke_color=GRAY_COLOR,
                stroke_width=2,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.35,
            )
            return VGroup(roof, body)

        # 4x4 grid of houses
        houses = VGroup()
        grid_n = 4
        spacing = 1.15
        for r in range(grid_n):
            for c in range(grid_n):
                h = make_house()
                h.move_to(
                    LEFT * ((grid_n - 1) * spacing / 2) + RIGHT * (c * spacing) +
                    UP * ((grid_n - 1) * spacing / 2) + DOWN * (r * spacing)
                )
                houses.add(h)
        houses.move_to(LEFT * 2.0 + DOWN * 1.1)

        # Vacancy bar (filled -> empty)
        vacancy_label = Text("Vacancy", font_size=24, color=TEXT_COLOR, weight=THIN)
        bar_w, bar_h = 0.65, 3.2
        vacancy_bar_outline = Rectangle(
            width=bar_w,
            height=bar_h,
            stroke_color=TEXT_COLOR,
            stroke_width=2.5,
            fill_opacity=0,
        )
        vacancy_bar_fill_full = Rectangle(
            width=bar_w - 0.08,
            height=bar_h - 0.08,
            stroke_width=0,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.6,
        ).move_to(vacancy_bar_outline.get_center())
        vacancy_bar_fill = vacancy_bar_fill_full.copy()

        vacancy_group = VGroup(vacancy_label, vacancy_bar_outline, vacancy_bar_fill)
        vacancy_label.next_to(vacancy_bar_outline, UP, buff=0.25)
        vacancy_group.move_to(RIGHT * 2.6 + DOWN * 1.1)

        # Animations (start with caption)
        house_fill_anims = [
            AnimationGroup(
                h[0].animate.set_stroke(RED, width=2.5).set_fill(RED, opacity=0.75),
                h[1].animate.set_stroke(RED, width=2.5).set_fill(RED, opacity=0.75),
                lag_ratio=0,
            )
            for h in houses
        ]
        houses_fill = LaggedStart(*house_fill_anims, lag_ratio=0.07, run_time=6.0)
        vacancy_drain = (
            vacancy_bar_fill.animate.stretch(0.01, dim=1, about_edge=DOWN)
            .set_run_time(6.0)
        )

        # Fade everything in together
        self.play(
            FadeIn(houses, vacancy_group, run_time=0.6, lag_ratio=0),
            run_time=0.6,
        )

        # Turn houses red one by one while vacancy drains (caption plays alongside)
        self.play(
            Write(caption, run_time=4.0),
            houses_fill,
            vacancy_drain,
            rate_func=linear,
        )

        # Ensure final state stays solid red
        for h in houses:
            h[0].set_stroke(RED, width=2.5)
            h[0].set_fill(RED, opacity=0.75)
            h[1].set_stroke(RED, width=2.5)
            h[1].set_fill(RED, opacity=0.75)

        self.wait(0.5)

        # Fade out all visuals at the end (including caption)
        all_visuals = VGroup(caption, houses, vacancy_group)
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene4_PowerGrid(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "Next, data centers are straining the power grid,\nmaking electricity generation\nand delivery a lucrative area.",
            font_size=36,
        )
        caption.move_to(UP * 3.5)
        
        # Power plant -> towers -> data center with a flickering power line
        plant = VGroup(
            Rectangle(
                width=1.5,
                height=1.5,
                color=YELLOW,
                fill_opacity=0.6,
                stroke_width=4,
            ),
            Polygon(
                np.array([-0.75, 0.75, 0]),
                np.array([0.75, 0.75, 0]),
                np.array([0, 1.2, 0]),
                color=YELLOW,
                fill_opacity=0.6,
                stroke_width=4,
            ),
        ).shift(LEFT * 3.0 + DOWN * 0.5)
        plant_label = Text("Power Plant", font_size=30, color=TEXT_COLOR, weight=THIN).next_to(
            plant, DOWN, buff=0.4
        )
        
        # Horizontal power bar connected to the plant (below the plant)
        bar_w, bar_h = 5.0, 0.35
        power_bar_outline = Rectangle(
            width=bar_w,
            height=bar_h,
            stroke_color=TEXT_COLOR,
            stroke_width=2.5,
            fill_opacity=0,
        )
        power_bar_fill_full = Rectangle(
            width=bar_w - 0.08,
            height=bar_h - 0.08,
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.85,
        ).move_to(power_bar_outline.get_center())
        power_bar_fill = power_bar_fill_full.copy().stretch(0.01, dim=0, about_edge=LEFT)
        power_bar_label = Text("Power usage", font_size=22, color=TEXT_COLOR, weight=THIN)
        power_bar_label.next_to(power_bar_outline, DOWN, buff=0.25)
        power_bar = VGroup(power_bar_outline, power_bar_fill, power_bar_label)
        power_bar.move_to(ORIGIN + DOWN * 3.4)

        towers = VGroup()
        for i in range(3):
            tower = VGroup(
                Line(np.array([-0.12, 0, 0]), np.array([0, 1, 0]), color=GRAY, stroke_width=4),
                Line(np.array([0.12, 0, 0]), np.array([0, 1, 0]), color=GRAY, stroke_width=4),
                Line(np.array([-0.12, 0.5, 0]), np.array([0.12, 0.5, 0]), color=GRAY, stroke_width=3),
            ).shift(RIGHT * (i - 1) * 1.6 + DOWN * 0.5)
            towers.add(tower)
        
        # Data center icon with inner racks
        dc_outer = Rectangle(
            width=1.8,
            height=1.8,
            stroke_color=ACCENT_COLOR,
            stroke_width=4,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.2,
        )
        dc_racks = VGroup()
        rack_w, rack_h = 0.35, 0.5
        rack_spacing_x = 0.2
        rack_spacing_y = 0.15
        for r in range(2):
            for c in range(3):
                rack = Rectangle(
                    width=rack_w,
                    height=rack_h,
                    stroke_color=ACCENT_COLOR,
                    stroke_width=2,
                    fill_color=WHITE,
                    fill_opacity=0.9,
                )
                rack.move_to(
                    dc_outer.get_center()
                    + RIGHT * (c - 1) * (rack_w + rack_spacing_x)
                    + UP * (0.4 - r * (rack_h + rack_spacing_y))
                )
                dc_racks.add(rack)
        data_center = VGroup(dc_outer, dc_racks).shift(RIGHT * 3.0 + DOWN * 0.5)
        dc_label = Text("Data Center", font_size=30, color=TEXT_COLOR, weight=THIN).next_to(
            data_center, DOWN, buff=0.4
        )
        
        self.play(
            FadeIn(plant, plant_label, run_time=0.8),
            FadeIn(power_bar, run_time=0.8),
            FadeIn(towers, run_time=0.8),
            FadeIn(data_center, dc_label, run_time=0.8),
        )

        # Fill the power bar while the caption writes
        self.play(
            Write(caption),
            power_bar_fill.animate.stretch(100, dim=0, about_edge=LEFT),
            run_time=3.0,
            rate_func=linear,
        )
        
        power_lines = VGroup()
        positions = [
            (plant.get_right(), towers[0].get_left()),
            (towers[0].get_right(), towers[1].get_left()),
            (towers[1].get_right(), towers[2].get_left()),
            (towers[2].get_right(), data_center.get_left()),
        ]
        
        for start, end in positions:
            line = Line(start, end, color=YELLOW, stroke_width=4)
            power_lines.add(line)
        
        self.play(Create(power_lines), run_time=1.0)
        
        # Flicker red more times and a bit longer
        for _ in range(6):
            flicker_lines = power_lines.copy()
            flicker_lines.set_color(RED)
            flicker_lines.set_opacity(0.6)
            self.add(flicker_lines)
            self.play(flicker_lines.animate.set_opacity(0), run_time=0.45)
            self.remove(flicker_lines)
        
        self.wait(0.2)
        
        # Fade out all visuals at the end (including caption)
        all_visuals = VGroup(
            caption,
            plant,
            plant_label,
            power_bar,
            towers,
            data_center,
            dc_label,
            power_lines,
        )
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene5_Cooling(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "Finally, as chips draw more power,\nadvanced cooling systems\nare becoming more demanded than ever.",
            font_size=36,
        )
        caption.move_to(UP * 3.5)

        # Detailed red CPU
        cpu_outer = Square(
            side_length=2.2,
            stroke_color=RED,
            stroke_width=4,
            fill_color=RED,
            fill_opacity=0.85,
        )
        cpu_inner = Square(
            side_length=1.5,
            stroke_color=RED,
            stroke_width=3,
            fill_color=RED,
            fill_opacity=0.5,
        )
        cpu_core = Square(
            side_length=0.7,
            stroke_color=RED,
            stroke_width=2,
            fill_color=RED,
            fill_opacity=0.7,
        )

        # Pins around the CPU
        pins = VGroup()
        pin_w, pin_h = 0.08, 0.18
        pin_color = RED
        for i in range(10):
            pins.add(Rectangle(width=pin_w, height=pin_h, stroke_width=0, fill_color=pin_color, fill_opacity=0.9))
        for i in range(10):
            pins.add(Rectangle(width=pin_w, height=pin_h, stroke_width=0, fill_color=pin_color, fill_opacity=0.9))
        for i in range(8):
            pins.add(Rectangle(width=pin_h, height=pin_w, stroke_width=0, fill_color=pin_color, fill_opacity=0.9))
        for i in range(8):
            pins.add(Rectangle(width=pin_h, height=pin_w, stroke_width=0, fill_color=pin_color, fill_opacity=0.9))

        # Arrange pins on each side
        top_pins = pins[:10].arrange(RIGHT, buff=0.08).next_to(cpu_outer, UP, buff=0.02)
        bottom_pins = pins[10:20].arrange(RIGHT, buff=0.08).next_to(cpu_outer, DOWN, buff=0.02)
        left_pins = pins[20:28].arrange(DOWN, buff=0.08).next_to(cpu_outer, LEFT, buff=0.02)
        right_pins = pins[28:36].arrange(DOWN, buff=0.08).next_to(cpu_outer, RIGHT, buff=0.02)

        cpu = VGroup(cpu_outer, cpu_inner, cpu_core, top_pins, bottom_pins, left_pins, right_pins)
        cpu_inner.move_to(cpu_outer.get_center())
        cpu_core.move_to(cpu_outer.get_center())
        cpu.move_to(ORIGIN + DOWN * 0.5)
        cooling_label = Text("Cooling", font_size=32, color=TEXT_COLOR, weight=THIN)
        cooling_label.next_to(cpu, DOWN, buff=0.5)

        # Smoke puff template (spawned repeatedly during animation)
        puff_template = VGroup(
            Circle(radius=0.18, color=GRAY, fill_opacity=0.55, stroke_width=0),
            Circle(radius=0.26, color=GRAY, fill_opacity=0.45, stroke_width=0),
            Circle(radius=0.14, color=GRAY, fill_opacity=0.5, stroke_width=0),
        ).arrange(RIGHT, buff=0.12)

        def make_smoke_stream(count=10, spread=0.25):
            stream_center = cpu.get_top() + UP * 0.6
            bottom_y = stream_center[1] - 0.3
            top_y = stream_center[1] + 1.0
            smoke_speed = 0.6

            stream = VGroup()
            for _ in range(count):
                puff = puff_template.copy()
                puff._smoke_x = stream_center[0] + np.random.uniform(-spread, spread)
                start_y = bottom_y - np.random.uniform(0.05, 0.6)
                puff.move_to(np.array([puff._smoke_x, start_y, 0]))
                puff.set_opacity(0)

                def puff_updater(mob, dt, bottom=bottom_y, top=top_y, speed=smoke_speed):
                    mob.shift(UP * speed * dt)
                    if mob.get_center()[1] > top:
                        reset_y = bottom - np.random.uniform(0.05, 0.6)
                        mob.move_to(np.array([mob._smoke_x, reset_y, 0]))
                    y = mob.get_center()[1]
                    alpha = np.clip((y - bottom) / (top - bottom), 0, 1)
                    mob.set_opacity(0.8 * alpha)

                puff.add_updater(puff_updater)
                stream.add(puff)

            return stream

        # Blue liquid drop below the CPU (circle only)
        drop = Circle(radius=0.2, color=ACCENT_COLOR, fill_opacity=0.9, stroke_width=0)
        drop.move_to(cpu.get_bottom() + DOWN * 1.2)

        # Smoke starts with captions and continues as a stream
        smoke_stream = make_smoke_stream(count=12, spread=0.3)
        self.add(smoke_stream)
        self.play(
            Write(caption, run_time=2.5),
            FadeIn(cpu, cooling_label, drop, run_time=0.8),
            run_time=2.5,
            rate_func=linear,
        )

        # Drop rises while smoke continues streaming
        self.play(
            drop.animate.move_to(cpu.get_center()),
            run_time=2.0,
            rate_func=linear,
        )
        smoke_stream.clear_updaters()
        for puff in smoke_stream:
            puff.clear_updaters()
        cooled_cpu = cpu.copy()
        for part in cooled_cpu:
            if isinstance(part, Mobject):
                part.set_stroke(color=ACCENT_COLOR)
                part.set_fill(color=ACCENT_COLOR, opacity=0.8)
        self.play(
            Transform(cpu, cooled_cpu),
            FadeOut(drop),
            FadeOut(smoke_stream),
            run_time=0.8,
        )

        self.wait(0.3)

        # Fade out all visuals at the end (including caption)
        all_visuals = VGroup(caption, cpu, cooling_label)
        self.play(FadeOut(all_visuals), run_time=0.5)
        self.wait(0.1)  # Brief black screen


class Scene6_CTA(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Caption text - larger and multi-line
        caption = make_caption(
            "To learn more, check out\nthe full article on Bloom's website.",
            font_size=36,
        )
        caption.move_to(UP * 3.5)
        
        # Caption only
        self.play(Write(caption, run_time=2.5))
        self.wait(1.5)
        self.play(FadeOut(caption), run_time=0.8)
        self.wait(0.2)  # Brief black screen