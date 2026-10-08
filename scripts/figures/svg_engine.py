#!/usr/bin/env python3
"""
scripts/figures/svg_engine.py
Publication-Grade Vector Diagram Engine for Computer Networks
Provides high-level builders for 32-bit packet headers, protocol flows, and D2 compilation.
"""

import os
import subprocess
import html

COLOR_PALETTE = {
    'blue': {'fill': '#dbeafe', 'text': '#1e40af', 'stroke': '#93c5fd'},
    'amber': {'fill': '#fef3c7', 'text': '#92400e', 'stroke': '#fde68a'},
    'green': {'fill': '#dcfce7', 'text': '#166534', 'stroke': '#86efac'},
    'rose': {'fill': '#fee2e2', 'text': '#991b1b', 'stroke': '#fca5a5'},
    'purple': {'fill': '#f3e8ff', 'text': '#6b21a8', 'stroke': '#d8b4fe'},
    'slate': {'fill': '#f1f5f9', 'text': '#334155', 'stroke': '#cbd5e1'},
    'teal': {'fill': '#ccfbf1', 'text': '#115e59', 'stroke': '#99f6e4'},
    'indigo': {'fill': '#e0e7ff', 'text': '#3730a3', 'stroke': '#c7d2fe'},
    'white': {'fill': '#ffffff', 'text': '#0f172a', 'stroke': '#cbd5e1'}
}

# Semantic mapping
COLOR_MAP = {
    'address': 'blue',
    'port': 'blue',
    'seq': 'amber',
    'ack': 'green',
    'control': 'rose',
    'flag': 'rose',
    'checksum': 'purple',
    'options': 'purple',
    'crypto': 'purple',
    'meta': 'slate',
    'reserved': 'slate',
    'length': 'teal',
    'type': 'indigo'
}

def get_color(color_key):
    mapped_key = COLOR_MAP.get(color_key, color_key)
    return COLOR_PALETTE.get(mapped_key, COLOR_PALETTE['slate'])

def draw_32bit_packet_header(title, rows, output_path, total_bits=32, bit_ruler=True, width=820, row_height=44):
    """
    Renders an exact, publication-quality 32-bit (or custom width) packet header in SVG.
    rows: list of rows, each containing a list of tuples: (field_name, bits, color_key, sublabel)
    """
    margin_x = 40
    margin_y = 50
    ruler_height = 28 if bit_ruler else 0
    grid_width = width - 2 * margin_x
    bit_width = grid_width / float(total_bits)
    total_height = margin_y + ruler_height + len(rows) * row_height + 30

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="100%" height="auto" style="background:#ffffff; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">')
    
    # Outer container with subtle border & shadow
    svg.append(f'<rect x="10" y="10" width="{width - 20}" height="{total_height - 20}" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>')
    
    # Title
    safe_title = html.escape(title)
    svg.append(f'<text x="{width / 2}" y="36" text-anchor="middle" font-size="15" font-weight="700" fill="#0f172a">{safe_title}</text>')

    # Bit Ruler (0 to total_bits-1)
    if bit_ruler:
        ruler_y = margin_y
        svg.append(f'<rect x="{margin_x}" y="{ruler_y}" width="{grid_width}" height="{ruler_height}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>')
        ruler_ticks = [0, 4, 8, 12, 16, 20, 24, 28, total_bits - 1]
        for b in ruler_ticks:
            bx = margin_x + b * bit_width
            svg.append(f'<text x="{bx + 3}" y="{ruler_y + 18}" font-size="11" font-weight="600" fill="#64748b">Bit {b}</text>')
            if 0 < b < total_bits - 1:
                svg.append(f'<line x1="{bx}" y1="{ruler_y}" x2="{bx}" y2="{ruler_y + ruler_height}" stroke="#cbd5e1" stroke-width="1"/>')

    # Rows rendering
    curr_y = margin_y + ruler_height
    for row_idx, row in enumerate(rows):
        curr_x = margin_x
        for field in row:
            name, bits, c_key, sublabel = field
            w = bits * bit_width
            c = get_color(c_key)
            
            c_fill = c['fill']
            c_stroke = c['stroke']
            c_text = c['text']
            
            # Field box
            svg.append(f'<rect x="{curr_x}" y="{curr_y}" width="{w}" height="{row_height}" fill="{c_fill}" stroke="{c_stroke}" stroke-width="1.2"/>')
            
            # Labels
            safe_name = html.escape(str(name))
            safe_sub = html.escape(str(sublabel)) if sublabel else ""
            
            center_x = curr_x + w / 2.0
            if sublabel:
                svg.append(f'<text x="{center_x}" y="{curr_y + 19}" text-anchor="middle" font-size="12" font-weight="700" fill="{c_text}">{safe_name}</text>')
                svg.append(f'<text x="{center_x}" y="{curr_y + 33}" text-anchor="middle" font-size="10" font-weight="500" fill="#475569">{safe_sub}</text>')
            else:
                svg.append(f'<text x="{center_x}" y="{curr_y + row_height/2.0 + 4}" text-anchor="middle" font-size="12" font-weight="700" fill="{c_text}">{safe_name}</text>')
                
            curr_x += w
        curr_y += row_height

    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))
    return output_path

def compile_d2(d2_code, output_path, theme=1, sketch=False):
    """
    Compiles D2 code to standalone SVG using local D2 installation.
    Theme 1: Neutral Grey (perfect for academic papers)
    Theme 4: Cool Classics
    Theme 100: Vanilla Nitro
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    tmp_d2 = output_path + ".tmp.d2"
    with open(tmp_d2, 'w', encoding='utf-8') as f:
        f.write(d2_code)
    
    cmd = ["d2", f"--theme={theme}"]
    if sketch:
        cmd.append("--sketch")
    cmd.extend([tmp_d2, output_path])
    
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if os.path.exists(tmp_d2):
            os.remove(tmp_d2)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error compiling D2 diagram to {output_path}: {e.stderr}")
        raise e

def compile_dot(dot_code, output_path):
    """
    Compiles Graphviz DOT code to standalone SVG using /usr/bin/dot.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    tmp_dot = output_path + ".tmp.dot"
    with open(tmp_dot, 'w', encoding='utf-8') as f:
        f.write(dot_code)
    
    cmd = ["dot", "-Tsvg", tmp_dot, "-o", output_path]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if os.path.exists(tmp_dot):
            os.remove(tmp_dot)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error compiling DOT diagram to {output_path}: {e.stderr}")
        raise e

def configure_matplotlib_style():
    """
    Configures Matplotlib for clean, publication-grade figures.
    """
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.sans-serif'] = ['Liberation Sans', 'DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['axes.edgecolor'] = '#cbd5e1'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['grid.color'] = '#f1f5f9'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['figure.autolayout'] = True

