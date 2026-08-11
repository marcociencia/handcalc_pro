
import streamlit as st
import sympy as sp
import numpy as np
from sympy import symbols, Eq, solve, Poly
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(page_title="Advanced Step-by-Step Math Solver", page_icon="🧮", layout="wide", initial_sidebar_state="expanded")
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
x, y, z, t = sp.symbols('x y z t')
SYMBOL_MAP = {'x': x, 'y': y, 'z': z, 't': t}

def safe_parse(expr_str: str, var=x):
    try:
        expr_str = expr_str.replace('^', '**')
        return parse_expr(expr_str, transformations=transformations, local_dict=SYMBOL_MAP)
    except:
        return None

def theory_box(title, content_md):
    st.markdown(f"### 📚 Theoretical Background: {title}")
    st.markdown(content_md)
    st.divider()

def step_header(n, title, desc=""):
    st.markdown(f"#### Step {n}: {title}")
    if desc:
        st.markdown(desc)

# ================= CORRECTED MULTIPLICATION LOGIC =================
def get_pos_mapping(a_str, b_str):
    # positions from right 0 = units
    # multiplicand a occupies pos 0..len(a)-1
    # multiplier b occupies pos 0..len(b)-1
    # max pos for final product = len(a)+len(b) maybe
    return max(len(a_str), len(b_str)) + len(b_str)

def render_multiplication_corrected_html(a,b):
    """Correct positioning as user described:
    - multiplier digit 3 below multiplicand 2 (units aligned)
    - 3x5=15 -> 5 descends and 1 orange above multiplicand 1
    - product 760: 0 aligned to multiplier 5 (below 456), then 76 left of 0
    - product 152: 2 aligned to multiplier 1 (below 760), 15 left of 2
    """
    if b==0 or a==0:
        return f'<div style="font-family:monospace; font-size:28px">{a} × {b} = 0</div>'
    a = abs(int(a)); b = abs(int(b))
    a_str = str(a)
    b_str = str(b)
    a_digits = list(map(int, a_str))  # left to right
    b_digits = list(map(int, b_str))  # left to right
    b_rev = b_digits[::-1]  # right to left: units first

    n_a = len(a_str)
    n_b = len(b_str)
    max_pos = n_a + n_b  # enough columns
    # positions 0..max_pos-1 from right (0=rightmost)
    # We'll create grid rows as dict pos->char

    # Helper to create empty row
    def empty_row():
        return {p: "" for p in range(max_pos)}

    # Rows list in order top to bottom
    rows = []  # each row = {"type": "carry"/"num"/"line", "data": dict pos->str, "color_data": dict pos->color, "small": bool}

    # --- Carry rows and multiplicand ---
    # We will process partials and collect carries
    partials = []  # list of dicts {pos->digit, value, b_digit, carries: list of (pos, value)}
    all_carries_for_top = []  # for first partials above multiplicand? Actually we will interleave

    # For each partial
    for p_idx, bd in enumerate(b_rev):
        pos_offset = p_idx  # rightmost digit of this partial aligned under multiplier digit at pos p_idx
        carry = 0
        partial_row = {}
        carries_this_partial = []  # list of {pos, value}
        # Process a_digits from right to left
        # a_digits right to left
        for j in range(n_a-1, -1, -1):
            ad = int(a_str[j])
            # position of this ad in overall pos system:
            # ad at position (n_a-1 - j) from right? Actually a_str rightmost is pos0
            # So ad at pos = (n_a-1 - j)
            # But partial's digit for this ad should be at pos = (n_a-1 - j) + pos_offset
            a_pos = (n_a-1 - j)  # 0 for rightmost of a
            # For partial product, the digit we write for this ad*bd is at position a_pos + pos_offset
            prod = ad * bd + carry
            write = prod % 10
            new_carry = prod // 10
            write_pos = a_pos + pos_offset
            partial_row[write_pos] = str(write)
            if new_carry > 0:
                # carry goes to next left position: write_pos+1
                carries_this_partial.append({"pos": write_pos+1, "value": new_carry})
            carry = new_carry
        if carry > 0:
            # Extra leading digit beyond a length
            extra_pos = n_a + pos_offset
            # If carry is >9, split digits (rare)
            extra_str = str(carry)
            # For simplicity, if carry is multi-digit, place digits left to right
            for k, ch in enumerate(reversed(extra_str)):  # rightmost of extra at extra_pos
                partial_row[extra_pos + k] = ch
            # No further carry

        partials.append({
            "b_digit": bd,
            "pos_offset": pos_offset,
            "row": partial_row,
            "carries": carries_this_partial,
            "value": a * bd
        })

    # Now build visual rows in exact order as image:
    # 1. Carry row for first partial (p_idx=0) - only its carries, placed above multiplicand
    # 2. Multiplicand row (152)
    # 3. Multiplier row (X 153)
    # 4. Line
    # 5. Partial 0 row (456)
    # 6. Carry row for partial 1 (2 1) above 760
    # 7. Partial 1 row (760)
    # 8. Partial 2 row (+152)
    # 9. Line
    # 10. Final result row (23256)

    # Helper to render a row dict pos->char as HTML flex from leftmost max_pos down to 0
    def render_row_html(row_dict, color_dict=None, small=False, is_plus=False, extra_left_char=""):
        # Find max pos used
        # Render from max_pos-1 down to 0 left to right? Actually leftmost is highest pos
        # We'll render flex with columns from max_pos-1 to 0
        # Determine max pos to display: max of keys in row_dict or max_pos
        display_max = max_pos -1
        # For simplicity, render from display_max down to 0
        html = '<div style="display:flex; justify-content:flex-start; font-family:monospace; '
        if small:
            html += 'font-size:18px; color:#E67E22; font-weight:bold; min-height:22px; '
        else:
            html += 'font-size:32px; '
        html += 'letter-spacing:0px">'
        for pos in range(display_max, -1, -1):
            ch = row_dict.get(pos, "")
            col = ""
            if color_dict and pos in color_dict:
                col = color_dict[pos]
            style = f'width:32px; text-align:center; color:{col if col else ("#E67E22" if small else "black")};'
            if ch == "" :
                html += f'<div style="{style}">&nbsp;</div>'
            else:
                if is_plus and pos == min(row_dict.keys()):
                    # Actually plus sign is separate left of row
                    pass
                html += f'<div style="{style}">{ch}</div>'
        html += '</div>'
        return html

    # More precise rendering using grid where we control order left to right = highest pos to 0
    # Build rows as per image logic

    html_output = '<div style="background:#fff; padding:20px; display:inline-block; border-radius:12px; border:1px solid #ddd">'

    # 1. Top carry row for first partial (p_idx=0)
    # First partial carries: from partials[0]["carries"]
    if partials and partials[0]["carries"]:
        carry_row_dict = {}
        for c in partials[0]["carries"]:
            carry_row_dict[c["pos"]] = str(c["value"])
        # Render small orange
        html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:18px; color:#E67E22; font-weight:bold; min-height:22px">'
        for pos in range(max_pos-1, -1, -1):
            ch = carry_row_dict.get(pos, "")
            html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html_output += '</div>'

    # 2. Multiplicand row 152 - right aligned (pos 0..n_a-1)
    html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px">'
    for pos in range(max_pos-1, -1, -1):
        if pos < n_a:
            # a digit at pos
            a_pos = pos
            # a_str index from right: a_str[ n_a-1 - a_pos ] if a_pos < n_a
            if a_pos < n_a:
                ch = a_str[n_a-1 - a_pos]
            else:
                ch = ""
        else:
            ch = ""
        html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
    html_output += '</div>'

    # 3. Multiplier row X 153 - with X on left of number? In image X is left of 153
    html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px">'
    for pos in range(max_pos-1, -1, -1):
        if pos == n_a:  # place X one column left of multiplicand?
            ch = "X"
        elif pos < n_b:
            ch = b_str[n_b-1 - pos] if pos < n_b else ""
        else:
            ch = "&nbsp;"
        # Actually we want X at position n_a (just left of multiplicand)
        # Let's handle: if pos == n_a, X, else if pos < n_b, digit of b
        if pos == n_a:
            html_output += f'<div style="width:32px; text-align:center">X</div>'
        elif pos < n_b:
            ch = b_str[n_b-1 - pos]
            html_output += f'<div style="width:32px; text-align:center">{ch}</div>'
        else:
            html_output += f'<div style="width:32px; text-align:center">&nbsp;</div>'
    html_output += '</div>'

    # 4. Line
    html_output += f'<div style="border-top:3px solid black; margin:6px 0; width:{max_pos*32}px"></div>'

    # 5. Partial 0 row 456 - pos_offset 0
    p0 = partials[0]
    html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
    for pos in range(max_pos-1, -1, -1):
        ch = p0["row"].get(pos, "")
        # Color logic: if this digit was computed with carry_in >0, color it orange? For first partial, 4 is result of 3+1, so should be blue/orange? In image 456 all black? Actually image shows 456 black? In your latest image 456 is black, 760 black, +152 black. So we keep black for partial digits, orange only for small carries.
        html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
    html_output += '</div>'

    # 6. Carry row for partial 1 (2 1) - above 760
    if len(partials) > 1:
        p1_carries = partials[1]["carries"]
        carry_dict = {c["pos"]: str(c["value"]) for c in p1_carries}
        html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:18px; color:#E67E22; font-weight:bold; min-height:22px">'
        for pos in range(max_pos-1, -1, -1):
            ch = carry_dict.get(pos, "")
            html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html_output += '</div>'

    # 7. Partial 1 row 760 - pos_offset 1
    if len(partials) > 1:
        p1 = partials[1]
        html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
        for pos in range(max_pos-1, -1, -1):
            ch = p1["row"].get(pos, "")
            html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html_output += '</div>'

    # 8. Partial 2 row +152 - pos_offset 2, with + sign
    if len(partials) > 2:
        p2 = partials[2]
        html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
        for pos in range(max_pos-1, -1, -1):
            if pos == p2["pos_offset"]-1:  # place + just left of rightmost? Actually image shows +152 with + at left of 152
                # For simplicity, put + at position pos_offset-1? Let's put + at pos = pos_offset-1? For p2 pos_offset=2, + at pos1? But image shows + at left of 152, which is at pos4? Actually 152 occupies pos2,3,4, + should be at pos1? Let's check image: +152 row shows + at left of 1? In image +152 has + just left of 1? Actually +152 shows + at same column as leftmost? We'll put + at one position left of leftmost digit of this partial
                pass
            ch = p2["row"].get(pos, "")
            # Add + sign at leftmost-1 position
            if pos == p2["pos_offset"] + n_a:  # one left of leftmost digit
                html_output += f'<div style="width:32px; text-align:center">+</div>'
            else:
                html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        # Simpler: render with + prefix
        html_output += '</div>'
        # Actually redo with + included
        # We'll recreate this row correctly with + sign
        # Remove last added row and redo
        html_output = html_output[:-6]  # hack to remove last div close? Let's just append another correct row
        # Correct row for +152
        html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
        for pos in range(max_pos-1, -1, -1):
            if pos == max(p2["row"].keys())+1:
                html_output += f'<div style="width:32px; text-align:center">+</div>'
            else:
                ch = p2["row"].get(pos, "")
                html_output += f'<div style="width:32px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html_output += '</div>'

    # 9. Line
    html_output += f'<div style="border-top:3px solid black; margin:8px 0; width:{max_pos*32}px"></div>'

    # 10. Final result
    final_val = a*b
    final_str = str(final_val)
    # final occupies pos 0..len(final_str)-1
    html_output += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px; font-weight:bold">'
    for pos in range(max_pos-1, -1, -1):
        if pos < len(final_str):
            ch = final_str[len(final_str)-1 - pos]
            html_output += f'<div style="width:32px; text-align:center">{ch}</div>'
        else:
            html_output += f'<div style="width:32px; text-align:center">&nbsp;</div>'
    html_output += '</div>'

    html_output += '</div>'

    # Explanation
    detail = '<div style="margin-top:16px; font-family:sans-serif; font-size:14px; background:#f9fafb; padding:12px; border-radius:8px">'
    detail += f'<b>Positioning logic (as you described):</b><br>'
    detail += f'• Multiplier digit 3 (below multiplicand 2, units) × 5 =15 → 5 descends, <span style="color:#E67E22">1 orange</span> above multiplicand 1<br>'
    detail += f'• Product 760: <b>0 aligned to multiplier 5</b> (below 456), then 76 left of 0<br>'
    detail += f'• Product 152: <b>2 aligned to multiplier 1</b> (below 760), 15 left of 2<br>'
    detail += f'• Staircase sum → {final_val}<br>'
    detail += '</div>'

    return html_output + detail

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🧮 Math Solver Pro")
    st.caption("Detailed step-by-step solver")
    mode = st.radio(
        "Choose Solver:",
        ["Basic Arithmetic (Long Method)", "First-Degree Equation", "Second-Degree Equation", "Linear Systems", "Derivative", "Integral"],
        index=0
    )

# ================= BASIC ARITHMETIC =================
if mode == "Basic Arithmetic (Long Method)":
    st.title("🔢 Multiplication - Corrected Positioning")
    theory_box("Exact Positioning Rule (from your image)",
    r"""
**Rule you described:**
- Multiplier digit $3$ is below multiplicand $2$ (units).
- $3 \times 5 =15$: descend $5$, orange $1$ above multiplicand $1$.
- Product $760$: $0$ aligned to multiplier $5$ (below $456$), then $76$ left of $0$.
- Product $152$: $2$ aligned to multiplier $1$ (below $760$), $15$ left of $2$.
- Orange small numbers are carries elevated to left unit.
    """)
    col_a, col_b = st.columns(2)
    a_in = col_a.number_input("Multiplicand (top) - e.g., 152", value=152, min_value=0, max_value=999999)
    b_in = col_b.number_input("Multiplier (bottom) - e.g., 153", value=153, min_value=0, max_value=999999)
    if st.button("Show Handwritten Multiplication", type="primary"):
        st.markdown(render_multiplication_corrected_html(a_in, b_in), unsafe_allow_html=True)

# ================= FIRST DEGREE =================
elif mode == "First-Degree Equation":
    st.title("1️⃣ First-Degree Equation Solver")
    theory_box("Linear Equation", r"""$a x + b = 0$, $x = -b/a$""")
    eq_input = st.text_input("Equation", value="2*x + 3 = 11")
    if st.button("Solve First-Degree", type="primary"):
        if "=" in eq_input:
            left_str, right_str = eq_input.split("=",1)
            left_expr = safe_parse(left_str)
            right_expr = safe_parse(right_str)
            eq_sym = Eq(left_expr, right_expr)
            sol = solve(eq_sym, x)
            st.latex(f"x = {sp.latex(sol[0])}" if sol else "No solution")

# ================= SECOND DEGREE =================
elif mode == "Second-Degree Equation":
    st.title("2️⃣ Quadratic Solver")
    theory_box("Quadratic", r"""$a x^2 + b x + c =0$, $x = \frac{-b\pm\sqrt{b^2-4ac}}{2a}$""")
    a_q = st.number_input("a", value=1.0)
    b_q = st.number_input("b", value=-3.0)
    c_q = st.number_input("c", value=2.0)
    if st.button("Solve Quadratic", type="primary"):
        a_sym, b_sym, c_sym = sp.nsimplify(a_q), sp.nsimplify(b_q), sp.nsimplify(c_q)
        expr = a_sym*x**2 + b_sym*x + c_sym
        delta = b_sym**2 - 4*a_sym*c_sym
        latex_b = sp.latex(b_sym)
        latex_delta = sp.latex(delta)
        latex_a = sp.latex(a_sym)
        latex_2a = sp.latex(2*a_sym)
        latex_minus_b = sp.latex(-b_sym)
        st.latex("x = \\frac{ -(" + latex_b + ") \\pm \\sqrt{" + latex_delta + "}}{2 \\cdot " + latex_a + "}")
        st.latex("x = \\frac{" + latex_minus_b + " \\pm \\sqrt{" + latex_delta + "}}{" + latex_2a + "}")
        roots = solve(Eq(expr,0), x)
        for i,r in enumerate(roots):
            st.latex(f"x_{i+1} = {sp.latex(r)}")

# ================= LINEAR SYSTEMS =================
elif mode == "Linear Systems":
    st.title("📐 Linear Systems")
    theory_box("Linear Systems", r"""Gaussian Elimination""")
    size = st.selectbox("Size", ["2x2", "3x3"])
    n=2 if "2x2" in size else 3
    var_names=['x','y','z'][:n]
    A=[]; b_vec=[]
    for i in range(n):
        st.markdown(f"Equation {i+1}")
        c=st.columns(n+1)
        row=[]
        for j in range(n):
            row.append(c[j].number_input(f"a[{i+1},{j+1}]", value=float(1 if i==j else 0), key=f"a_{i}_{j}"))
        b_vec.append(c[n].number_input(f"b[{i+1}]", value=float(i+1), key=f"b_{i}"))
        A.append(row)
    if st.button("Solve System", type="primary"):
        A_np=np.array(A,float); b_np=np.array(b_vec,float)
        x_sol=np.linalg.solve(A_np,b_np)
        for i,name in enumerate(var_names):
            st.latex(f"{name} = {x_sol[i]}")

# ================= DERIVATIVE =================
elif mode == "Derivative":
    st.title("📈 Derivative")
    theory_box("Derivative", r"""$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$""")
    f_input=st.text_input("f(x)", value="x^3 + 2*x^2")
    if st.button("Derive", type="primary"):
        f_expr=safe_parse(f_input)
        st.latex(f"f' = {sp.latex(sp.diff(f_expr,x))}")

# ================= INTEGRAL =================
elif mode == "Integral":
    st.title("∫ Integral")
    theory_box("Integral", r"""$\int f(x)dx = F(x)+C$""")
    f_input=st.text_input("f(x)", value="x^2 + 3*x")
    if st.button("Integrate", type="primary"):
        f_expr=safe_parse(f_input)
        st.latex(f"\\int f = {sp.latex(sp.integrate(f_expr,x))} + C")
