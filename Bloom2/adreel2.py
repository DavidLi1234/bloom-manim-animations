from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import numpy as np
from manim import *


DATA_FILES = [
    #Delete these three lines and add own file path to data
    "Bloom 2 Ad Reel Data.csv",
    "Bloom 2 Video Data.csv",
    "Bloom 2 Video Data.py",
]

# Tunable labels/colors
AXIS_Y_LABEL_RETURN = "Cumulative Return %"
#AXIS_Y_LABEL_PRICE = "Price in $"
LINE_LABEL_BLOOM = "Data center" #Change this 
LINE_LABEL_SPY = "S&P 500"
LEGEND_LABEL_BLOOM = "Bloom Data Center Growth Portfolio" #Change this
LEGEND_LABEL_SPY = "S&P 500 Index Fund (SPY)"
LINE_COLOR_BLOOM = BLUE_D #change this (optional)
LINE_COLOR_SPY = RED_D #change this (optional)


def load_portfolio_data() -> tuple[
    list[datetime],
    list[float],
    list[float],
    str,
    str,
    bool,
]:
    data_path = None
    base_dir = Path(__file__).parent
    for filename in DATA_FILES:
        candidate = base_dir / filename
        if candidate.exists():
            data_path = candidate
            break

    if data_path is None:
        raise FileNotFoundError(
            "Could not find Bloom 2 Video Data.csv (or .py) in the script folder."
        )

    dates: list[datetime] = []
    custom_values: list[float] = []
    spy_values: list[float] = []

    with data_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV file does not contain headers.")

        custom_candidates = [
            "Bloom Data Center Portfolio",
            "Cumulative Portfolio Return",
            "Custom Portfolio",
        ]
        spy_candidates = [
            "Cumulative S&P 500 Index (SPY) Return",
            "S&P 500 Index (SPY)",
            "S&P 500 Index Fund (SPY)",
        ]

        def pick_column(candidates: list[str]) -> str:
            for name in candidates:
                if name in reader.fieldnames:
                    return name
            raise KeyError(f"None of the expected columns found: {candidates}")

        custom_col = pick_column(custom_candidates)
        spy_col = pick_column(spy_candidates)
        is_return_series = "Return" in custom_col or "Return" in spy_col

        for row in reader:
            date_str = row["Date"]
            try:
                parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
            except ValueError:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            dates.append(parsed_date)
            custom_values.append(float(row[custom_col]))
            spy_values.append(float(row[spy_col]))

    return dates, custom_values, spy_values, custom_col, spy_col, is_return_series


def nice_step(value_range: float) -> float:
    if value_range <= 0:
        return 1.0
    raw = value_range / 5
    magnitude = 10 ** int(np.floor(np.log10(raw)))
    normalized = raw / magnitude
    if normalized < 2:
        step = 2 * magnitude
    elif normalized < 5:
        step = 5 * magnitude
    else:
        step = 10 * magnitude
    return step


class PortfolioComparison(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"

        (
            dates,
            custom_values,
            spy_values,
            _custom_column,
            _spy_column,
            is_return_series,
        ) = load_portfolio_data()
        count = len(dates)
        if count == 0:
            return

        def smooth_series(values: list[float], window: int = 9) -> list[float]:
            if window <= 1 or window > len(values):
                return values
            kernel = np.ones(window) / window
            padded = np.pad(values, (window - 1, 0), mode="edge")
            smoothed = np.convolve(padded, kernel, mode="valid")
            return smoothed.tolist()

        # Smooth the lines to reduce jitter
        custom_values = smooth_series(custom_values, window=7)
        spy_values = smooth_series(spy_values, window=7)

        # Window size for scrolling effect
        window_size = min(150, count)  # Number of points visible at once
        
        # Calculate overall ranges
        y_min_all = min(min(custom_values), min(spy_values))
        y_max_all = max(max(custom_values), max(spy_values))
        padding = max((y_max_all - y_min_all) * 0.06, 1.0)
        y_min_all -= padding
        y_max_all += padding
        y_step = nice_step(y_max_all - y_min_all)

        # ValueTracker for current index (needed before create_axes)
        current_index_tracker = ValueTracker(0)
        # Track a floor for y-axis zoom-out to 0 near the end
        y_floor_tracker = ValueTracker(y_min_all)

        # Create static axes (we map values into a normalized 0..1 range)
        layout_drop = 0.3
        axes = Axes(
            x_range=[0, window_size - 1, max(1, window_size // 8)],
            y_range=[0, 1, 0.2],
            x_length=9.0,
            y_length=7.2 + layout_drop,
            tips=False,
            axis_config={"color": GRAY_B, "include_ticks": False},
        )
        axes.to_edge(LEFT, buff=0.9)
        axes.to_edge(DOWN, buff=0.8)
        axes.shift(RIGHT * 1.3)
        axes.shift(DOWN * layout_drop)
        self.add(axes)

        # Axis labels - position relative to fixed location
        def create_y_label():
            current_axes = axes
            label = Text(
                AXIS_Y_LABEL_RETURN if is_return_series else AXIS_Y_LABEL_PRICE,
                font_size=26,
                color=GRAY_A,
            )
            label.rotate(PI / 2)
            label.next_to(current_axes, LEFT, buff=1.0)
            label.shift(LEFT * 0.2)
            return label
        
        y_label = always_redraw(create_y_label)
        self.add(y_label)
        
        def get_window_positions(idx_float: float) -> tuple[float, int, int]:
            start_pos = max(0.0, idx_float - (window_size - 1))
            start_idx = max(0, int(np.floor(start_pos)))
            end_idx = min(int(np.floor(idx_float)) + 1, count)
            return start_pos, start_idx, end_idx

        def get_visible_range(values_a: list[float], values_b: list[float], start: int, end: int) -> tuple[float, float]:
            if end <= start:
                return y_min_all, y_max_all
            visible_a = values_a[start:end]
            visible_b = values_b[start:end]
            current_y_min = min(min(visible_a), min(visible_b))
            current_y_max = max(max(visible_a), max(visible_b))
            current_padding = max((current_y_max - current_y_min) * 0.06, 1.0)
            padded_min = current_y_min - current_padding
            padded_max = current_y_max + current_padding
            y_floor = y_floor_tracker.get_value()
            return min(padded_min, y_floor), padded_max

        def build_line(values: list[float], color: Color) -> VMobject:
            idx_float = current_index_tracker.get_value()
            if idx_float < 1:
                return VMobject()
            start_pos, start_idx, end_idx = get_window_positions(idx_float)
            visible_range = list(range(start_idx, end_idx))
            if len(visible_range) < 2:
                return VMobject()
            y_min, y_max = get_visible_range(custom_values, spy_values, start_idx, end_idx)
            y_span = max(y_max - y_min, 1.0)
            points = [
                axes.c2p(
                    float(data_idx) - start_pos,
                    (values[data_idx] - y_min) / y_span,
                )
                for data_idx in visible_range
            ]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(color=color, width=4)
            return line

        portfolio_color = LINE_COLOR_BLOOM
        spy_color = LINE_COLOR_SPY

        custom_line = always_redraw(lambda: build_line(custom_values, portfolio_color))
        spy_line = always_redraw(lambda: build_line(spy_values, spy_color))

        def build_date_labels() -> VGroup:
            idx_float = current_index_tracker.get_value()
            labels = VGroup()
            if idx_float < 0:
                return labels
            num_labels = 6
            start_pos, start_idx, end_idx = get_window_positions(idx_float)
            visible_count = end_idx - start_idx
            step = max(1, visible_count // (num_labels - 1))
            y_min = 0
            for i in range(0, visible_count, step):
                data_idx = start_idx + i
                if data_idx < len(dates):
                    label = Text(
                        dates[data_idx].strftime("%b %Y"),
                        font_size=18,
                        color=GRAY_A,
                    )
                    label.rotate(PI / 6)
                    label.next_to(
                        axes.c2p(float(data_idx) - start_pos, y_min),
                        DOWN,
                        buff=0.25,
                    )
                    labels.add(label)
            return labels

        def build_y_labels() -> VGroup:
            labels = VGroup()
            idx_float = current_index_tracker.get_value()
            _start_pos, start_idx, end_idx = get_window_positions(idx_float)
            y_min, y_max = get_visible_range(custom_values, spy_values, start_idx, end_idx)
            num_y_labels = 5
            for i in range(num_y_labels + 1):
                t = i / num_y_labels
                y_val = y_min + (y_max - y_min) * t
                label = Text(
                    f"{y_val:.1f}" if is_return_series else f"${y_val:.0f}",
                    font_size=18,
                    color=GRAY_A,
                )
                label.next_to(axes.c2p(0, t), LEFT, buff=0.2)
                labels.add(label)
            return labels

        date_labels_group = always_redraw(build_date_labels)
        y_labels_group = always_redraw(build_y_labels)

        def build_custom_label() -> Mobject:
            line = build_line(custom_values, portfolio_color)
            if line.get_num_points() == 0:
                return VMobject()
            label = Text(LINE_LABEL_BLOOM, font_size=22, color=portfolio_color)
            label.next_to(line.get_end(), RIGHT, buff=0.2)
            return label

        def build_spy_label() -> Mobject:
            line = build_line(spy_values, spy_color)
            if line.get_num_points() == 0:
                return VMobject()
            label = Text(LINE_LABEL_SPY, font_size=22, color=spy_color)
            label.next_to(line.get_end(), RIGHT, buff=0.2)
            return label

        custom_label = always_redraw(build_custom_label)
        spy_label = always_redraw(build_spy_label)

        def build_head_dot(values: list[float], color: Color) -> Mobject:
            line = build_line(values, color)
            if line.get_num_points() == 0:
                return VMobject()
            return Dot(line.get_end(), radius=0.08, color=color)

        custom_dot = always_redraw(lambda: build_head_dot(custom_values, portfolio_color))
        spy_dot = always_redraw(lambda: build_head_dot(spy_values, spy_color))

        def build_glow(values: list[float], color: Color) -> VMobject:
            line = build_line(values, color)
            if line.get_num_points() == 0:
                return VMobject()
            glow = line.copy()
            glow.set_stroke(color=color, width=10, opacity=0.25)
            return glow

        custom_glow = always_redraw(lambda: build_glow(custom_values, portfolio_color))
        spy_glow = always_redraw(lambda: build_glow(spy_values, spy_color))

        legend = VGroup(
            Dot(radius=0.06, color=portfolio_color),
            Text(LEGEND_LABEL_BLOOM, font_size=24, color=portfolio_color),
        ).arrange(RIGHT, buff=0.2)
        legend2 = VGroup(
            Dot(radius=0.06, color=spy_color),
            Text(LEGEND_LABEL_SPY, font_size=24, color=spy_color),
        ).arrange(RIGHT, buff=0.2)
        legend_group = VGroup(legend, legend2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend_group.to_corner(UR, buff=0.4)
        legend_group.shift(UP * 2.0)

        def build_current_date_label() -> Mobject:
            idx = min(int(current_index_tracker.get_value()), len(dates) - 1)
            if idx < 0:
                return VMobject()
            label = Text(dates[idx].strftime("%b %d, %Y"), font_size=44, color=WHITE)
            label.next_to(axes, DOWN, buff=0.9)
            label.shift(DOWN * 0.5)
            return label

        current_date_label = always_redraw(build_current_date_label)

        self.add(
            custom_glow,
            spy_glow,
            custom_line,
            spy_line,
            custom_dot,
            spy_dot,
            date_labels_group,
            y_labels_group,
            custom_label,
            spy_label,
            legend_group,
            current_date_label,
        )
        
        # Animate the progression
        animation_duration = 20.0  # Total duration in seconds
        
        # Animate the index tracker from 0 to count-1
        slowdown_tail = 4.0
        if animation_duration <= slowdown_tail:
            self.play(
                current_index_tracker.animate.set_value(count - 1),
                y_floor_tracker.animate.set_value(0),
                rate_func=rate_functions.ease_out_quad,
                run_time=animation_duration,
            )
        else:
            linear_duration = animation_duration - slowdown_tail
            mid_value = (count - 1) * (linear_duration / animation_duration)
            self.play(
                current_index_tracker.animate.set_value(mid_value),
                rate_func=linear,
                run_time=linear_duration,
            )
            self.play(
                current_index_tracker.animate.set_value(count - 1),
                y_floor_tracker.animate.set_value(0),
                rate_func=rate_functions.ease_out_quad,
                run_time=slowdown_tail,
            )
        
        # Final pause
        self.wait(2.0)
