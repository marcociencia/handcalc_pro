
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

# ================= BASIC ARITHMETIC - EXACT LOGIC FROM IMAGE =================
COLORS = ["#2563eb", "#7c3aed", "#dc2626", "#16a34a", "#ea580c"]  # blue, violet, red, green, orange - per partial product

def analyze_multiplication(a,b):
    """Implement exact reasoning from image:
    - multiplier digits from bottom (units) to top (hundreds)
    - multiplicand digits from bottom (units) to top
    - small carry on top of next left digit, colored per partial
    - digit that includes carry is colored to reference last account
    Returns structure for rendering
    """
    a_str = str(abs(a))
    b_str = str(abs(b))
    a_digits = list(map(int, a_str))  # left to right
    b_digits = list(map(int, b_str))  # left to right
    b_digits_rev = b_digits[::-1]  # right to left processing order (units first)

    n = len(a_digits)
    # columns_carries[pos] = list of {value, color, partial_idx}
    columns_carries = [[] for _ in range(n)]
    partials_info = []  # each: {digits: list left->right with color info, value:int, b_digit, color}

    for partial_idx, bd in enumerate(b_digits_rev):
        color = COLORS[partial_idx % len(COLORS)]
        carry = 0
        partial_digits = []  # left to right after processing, each element {digit, color, used_carry_color}
        # We'll process right to left and collect
        temp_digits_rev = []  # right to left order of write digits with info
        carries_this_partial = []  # list of (target_pos, value, color)
        for j in range(n-1, -1, -1):
            ad = a_digits[j]
            carry_in = carry
            prod = ad * bd + carry_in
            write = prod % 10
            new_carry = prod // 10
            # Determine color of this write digit: if carry_in>0, color = color of that carry_in
            # carry_in color is color of previous carry that was placed above this position? Actually carry_in comes from previous right digit's new_carry, which has same partial color
            # So if carry_in>0, write digit color = color (since it references last account)
            write_color = "black"
            if carry_in > 0:
                write_color = color  # blue for first partial's last digit 4, violet for second partial's 6 and 7

            temp_digits_rev.append({"digit": write, "color": write_color, "carry_in": carry_in, "ad": ad, "bd": bd, "prod": prod})

            if new_carry > 0:
                target_pos = j-1
                if target_pos >= 0:
                    columns_carries[target_pos].append({"value": new_carry, "color": color, "partial_idx": partial_idx})
                # else: leading extra digit, will be handled as extra digit after loop
            carry = new_carry

        # After loop, if carry >0, it becomes extra leading digit(s)
        if carry > 0:
            # extra digit(s) - could be >9? rare
            extra_str = str(carry)
            for k, ch in enumerate(extra_str):
                # These extra digits are also colored? In example, first partial has no extra, second has no extra
                temp_digits_rev.append({"digit": int(ch), "color": color if len(extra_str)==1 else "black", "carry_in": 0, "ad": None, "bd": None, "prod": None})
            # Actually need to reverse correctly
            # For simplicity, if carry>0 after processing all, it is the leftmost digit(s)
            # Our temp_digits_rev currently has n digits, right to left. The extra carry should be at front.
            # We already appended extra after loop, but we need to ensure order
            pass

        # Convert temp_digits_rev (right to left) to left to right
        # temp_digits_rev[0] is rightmost digit, last is leftmost
        # If we had extra carry, it was appended at end, so it will be leftmost after reverse
        partial_digits_lr = list(reversed(temp_digits_rev))
        # Value of partial
        # Compute numeric value: a * bd
        partial_value = a * bd

        partials_info.append({
            "b_digit": bd,
            "color": color,
            "digits_info": partial_digits_lr,  # left to right
            "value": partial_value,
            "partial_idx": partial_idx
        })

    # For final extra leading digits that were from final carry beyond leftmost, our logic above already included them as extra entries in temp_digits_rev?
    # Let's recompute partials values correctly for display: use a*bd for numeric, but digits_info already contains the breakdown

    # Compute max depth of carry columns
    max_depth = max((len(col) for col in columns_carries), default=0)

    return {
        "a_str": a_str,
        "b_str": b_str,
        "a_digits": a_digits,
        "b_digits": b_digits,
        "b_digits_rev": b_digits_rev,
        "columns_carries": columns_carries,
        "max_depth": max_depth,
        "partials_info": partials_info
    }

def render_multiplication_exact_html(a,b):
    if a==0 or b==0:
        return f'<div>{a} × {b} = 0</div>'
    info = analyze_multiplication(a,b)
    a_str = info["a_str"]
    b_str = info["b_str"]
    a_digits = info["a_digits"]
    n = len(a_digits)
    columns_carries = info["columns_carries"]
    max_depth = info["max_depth"]
    partials_info = info["partials_info"]

    # Sort columns_carries for display: each column's carries sorted by partial_idx descending (later partials on top)
    for col in range(n):
        columns_carries[col] = sorted(columns_carries[col], key=lambda x: -x["partial_idx"])

    html = '<div style="font-family: monospace; background:#fff; padding:20px; display:inline-block; border-radius:12px; border:1px solid #ddd; line-height:1.1">'

    # Top carry rows
    for row in range(max_depth):
        html += '<div style="display:flex; justify-content:flex-end; font-size:18px; font-weight:bold; min-height:22px; letter-spacing:0px">'
        # For each column position 0..n-1 left to right
        for col in range(n):
            col_carries = columns_carries[col]
            # Determine which carry should appear in this row
            # Bottom-aligned: if col has k carries, they occupy rows max_depth-k to max_depth-1
            k = len(col_carries)
            if row < max_depth - k:
                # empty
                html += f'<div style="width:28px; text-align:center">&nbsp;</div>'
            else:
                idx_in_col = row - (max_depth - k)
                c = col_carries[idx_in_col]
                html += f'<div style="width:28px; text-align:center; color:{c["color"]}">{c["value"]}</div>'
        # Add extra space for alignment with multiplier (right side)
        html += f'<div style="width:28px"></div>'
        html += '</div>'

    # Multiplicand row 152
    html += '<div style="display:flex; justify-content:flex-end; font-size:32px; letter-spacing:2px">'
    for col in range(n):
        html += f'<div style="width:28px; text-align:center">{a_digits[col]}</div>'
    html += '<div style="width:28px"></div></div>'

    # Multiplier row x153
    html += '<div style="display:flex; justify-content:flex-end; font-size:32px; letter-spacing:2px">'
    html += f'<div style="width:28px; text-align:center">x</div>'
    # b_str right aligned under a_str
    # b_str may be shorter than n, pad left
    b_padded = b_str.rjust(n)
    for col in range(n):
        ch = b_padded[col]
        if ch == ' ':
            html += f'<div style="width:28px; text-align:center">&nbsp;</div>'
        else:
            html += f'<div style="width:28px; text-align:center">{ch}</div>'
    html += '</div>'

    # Line
    html += '<div style="border-top:2.5px solid black; margin:6px 0 8px 0"></div>'

    # Partial products - staircase
    for p_idx, p_info in enumerate(partials_info):
        digits_info = p_info["digits_info"]
        color = p_info["color"]
        # Shift to left: each next partial is shifted one to left? Actually in image, first partial 456 right aligned, second 760 shifted one? Let's check: 456, 760, 152 - they appear as staircase increasing left? In image, 456 rightmost, 760 slightly left, 152 more left? But for simplicity, we will show staircase as in image: each next partial shifted left by one position (visually to left)
        # For right alignment with shift: we add margin-right = p_idx * 28px? Actually shift left means less right margin? Let's do margin-right = p_idx * 0? Let's replicate image: 456 is top partial right aligned, 760 is below with one space? In image, 760 appears under 456 but slightly left? Actually 760 is under 456, with 0 under 5? Hard. We'll use right alignment with increasing left offset: first partial right aligned, second partial shifted 1 to left? In HTML flex, we can add empty divs on right
        shift = p_idx  # number of positions to shift left? For display, we shift right? Let's test: For 152x153, partials: 456 (units*3), 760 (tens*5), 152 (hundreds*1)
        # In standard long multiplication, 760 should be shifted one to left, i.e., actually 7600 but displayed as 760 with one trailing zero not shown, but visually it is shifted left by one.
        # In image, they show 760 directly under 456, with 0 under 5? So shift left by 1.
        # We will implement as: partial row has right padding = p_idx * 28px? That would shift left? No, padding right would shift left? If we add empty space on right, number moves left.
        # Let's add margin-right = p_idx*0 and margin-left? Simpler: use flex with justify-content:flex-end and add extra empty divs on right for shift?
        # Actually to shift left, we need to add empty space on right? No, shifting left means moving left, so add space on right? Wait: right-aligned container: if you add space on right, content moves left. So right padding = p_idx * 28px shifts left.

        html += '<div style="display:flex; justify-content:flex-end; font-size:30px; letter-spacing:2px; align-items:center">'
        # For second partial onward, show + sign for last? In image, third partial has +152
        if p_idx == len(partials_info)-1 and len(partials_info)>1:
            html += f'<div style="width:28px; text-align:center">+</div>'
        else:
            html += f'<div style="width:28px; text-align:center">&nbsp;</div>'

        # Left padding for leading zeros? digits_info may be shorter than n+1
        # Pad left to n
        total_slots = n + (1 if len(digits_info) > n else 0)  # handle extra leading digit
        # For simplicity, render digits_info left to right, right aligned
        # Create array of slots size n + p_idx? Actually staircase: each next partial should have one extra empty on right? Let's just render digits_info right aligned with shift
        # Right shift: add p_idx empty slots on right (so number appears shifted left)
        # Left pad to align to n + max extra

        # Build list of visual slots: we want n + 1 slots for multiplicand width plus shifts
        # For p_idx=0: no right empty
        # p_idx=1: 1 empty on right? In image, 760 appears with 0 under 5 of 456? That suggests shift left by 1? Actually 456 has digits at positions: 4,5,6. 760 has 7,6,0. If 0 of 760 is under 5 of 456, then 760 is shifted left by 1 relative to 456? Let's check: 456 positions: [4,5,6]; 760 positions: [7,6,0] - if 0 under 5, then alignment: 4 5 6 / 7 6 0 with 0 under 5? That would be: 456,  760 with offset? 6 of 456 aligns with 6 of 760? In image, 760 appears slightly left, so 0 under 6? Let's not overthink, use standard shift: second partial shifted one to left (one trailing zero not shown, but visually one position left)
        # So we will add p_idx empty divs on right to shift left? Wait adding empty on right shifts content left? In flex justify flex-end, adding empty divs on right after content would push content left? Actually flex-end aligns to end, so content is at right edge. If we add empty divs after content, they would be at rightmost edge, pushing content left. So we want p_idx empty divs on right.

        # Render digits
        for d_info in digits_info:
            col_color = d_info["color"]
            html += f'<div style="width:28px; text-align:center; color:{col_color}">{d_info["digit"]}</div>'

        # Right shift empties
        for _ in range(p_idx):
            html += f'<div style="width:28px; text-align:center">&nbsp;</div>'

        html += '</div>'

    # Final line and sum
    html += '<div style="border-top:3px solid black; margin:10px 0 8px 0"></div>'
    total = a*b
    html += f'<div style="display:flex; justify-content:flex-end; font-size:32px; font-weight:bold; letter-spacing:2px"><div>{total}</div></div>'

    html += '</div>'

    # Detailed reasoning text (not in code comment, but as explanation for UI, in English as requested for theory)
    detail = '<div style="margin-top:18px; font-family:sans-serif; font-size:15px; line-height:1.5; background:#f9fafb; padding:12px; border-radius:8px">'
    detail += f'<b>How {a} × {b} was computed (exact reasoning from your image):</b><br>'
    for p_idx, p_info in enumerate(partials_info):
        bd = p_info["b_digit"]
        color = p_info["color"]
        detail += f'<br><b>Partial {p_idx+1}: multiplier digit {bd} ({"units" if p_idx==0 else "tens" if p_idx==1 else "hundreds"}) × {a}:</b><br>'
        carry = 0
        a_digits = list(map(int, str(a)))[::-1]  # right to left
        for j, ad in enumerate(a_digits):
            prod = ad*bd + carry
            if j==0:
                detail += f'&nbsp;&nbsp;{bd} × {ad} = {ad*bd} → write <b>{prod%10}</b>, carry <span style="color:{color}">{prod//10}</span> small on top of next left digit<br>'
            else:
                if carry>0:
                    detail += f'&nbsp;&nbsp;{bd} × {ad} = {ad*bd}, + carry {carry} = {prod} → write <b style="color:{color if carry>0 else "black"}">{prod%10}</b> (colored {color} because it includes carry), carry <span style="color:{color}">{prod//10}</span> to left<br>'
                else:
                    detail += f'&nbsp;&nbsp;{bd} × {ad} = {prod} → write <b>{prod%10}</b><br>'
            carry = prod//10
        if carry>0:
            detail += f'&nbsp;&nbsp;Final carry {carry} becomes leftmost digit<br>'
        detail += f'&nbsp;&nbsp;→ Partial product = {p_info["value"]} (colored digits indicate they used a carry)<br>'

    detail += f'<br><b>Sum (staircase):</b> Note the staircase, just sum. Final carries for sum are black. Result {a}×{b}={total}'
    detail += '</div>'

    return html + detail

def render_addition_simple(a,b):
    # Simple addition with orange carry elevated left
    a_str=str(a); b_str=str(b)
    max_len=max(len(a_str), len(b_str))
    a_str=a_str.zfill(max_len); b_str=b_str.zfill(max_len)
    carry=0
    carries=[]
    for i in range(max_len-1, -1, -1):
        s=int(a_str[i])+int(b_str[i])+carry
        carries.insert(0, carry)
        carry=s//10
    # columns_carries for addition: carry to left
    cols=[[] for _ in range(max_len)]
    # Actually carry at position i is placed above i-1
    for i in range(max_len):
        # carry that was generated from position i+1
        # Our carries list is carry_in for each position
        if i>0 and int(a_str[i])+int(b_str[i])+ (carries[i-1] if i>0 else 0) >=10:
            # carry out from this position goes to left
            pass
    # Simplified render
    html='<div style="font-family: monospace; font-size:32px; background:#fff; padding:16px; display:inline-block; border-radius:10px; border:1px solid #ddd">'
    # carry row orange
    html+='<div style="color:#E67E22; font-size:18px; letter-spacing:9px; text-align:right; min-height:20px; font-weight:bold">'
    # show carries that are >0 as orange above next left
    carry=0
    carry_row=['']*max_len
    for i in range(max_len-1, -1, -1):
        da=int(a_str[i]); db=int(b_str[i])
        s=da+db+carry
        if s>=10 and i>0:
            carry_row[i-1]='1'
        carry=s//10
    for c in carry_row:
        html+=f'<span style="display:inline-block; width:22px; text-align:center">{c if c else "&nbsp;"}</span>'
    html+='</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px">{a}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; border-bottom:2.5px solid black">+ {b}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; font-weight:bold; padding-top:4px">{a+b}</div>'
    html+='</div>'
    return html

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🧮 Math Solver Pro")
    st.caption("Detailed step-by-step solver with theory")
    mode = st.radio(
        "Choose Solver:",
        ["Basic Arithmetic (Long Method)", "First-Degree Equation", "Second-Degree Equation", "Linear Systems", "Derivative", "Integral"],
        index=0
    )
    st.divider()

# ================= BASIC ARITHMETIC =================
if mode == "Basic Arithmetic (Long Method)":
    st.title("🔢 Basic Arithmetic - Exact Handwritten Logic")
    theory_box("Carry Rule (orange / colored small numbers)",
    r"""
**Rule from your image:** When sum or product ≥10, write ones digit and **elevate tens digit to next left column** as small colored number on top.

- **Multiplication:** Process bottom multiplier digit from right to left, and multiplicand from right to left (bottom to top). Example $152×3$: $3×2=6$, $3×5=15$ → write $5$ left of $6$ and small blue $1$ on top of $1$, $3×1+1=4$ → write $4$ blue. Product $456$.
- For $152×5$: $5×2=10$ → write $0$ aligned with $5$ and small violet $1$ on top of $5$, $5×5+1=26$ → write $6$ left of $0$ and small $2$ on top of $1$, $5×1+2=7$ → $760$.
- Colors: 1st partial blue, 2nd violet, 3rd red, etc. Final sum carries are black (staircase).
    """)
    op = st.selectbox("Operation", ["Multiplication (×) - Exact from image", "Addition (+)", "Subtraction (-)", "Division (÷)"], index=0)
    col_a, col_b = st.columns(2)
    a_in = col_a.number_input("Multiplicand / First Number", value=152, min_value=0, max_value=9999999, step=1)
    b_in = col_b.number_input("Multiplier / Second Number", value=153, min_value=0, max_value=9999999, step=1)

    if st.button("Calculate - Show Handwritten Steps", type="primary"):
        if op.startswith("Multiplication"):
            st.markdown("### ✖️ Handwritten Multiplication - Exact as Image")
            st.markdown(render_multiplication_exact_html(a_in, b_in), unsafe_allow_html=True)
        elif op.startswith("Addition"):
            st.markdown(render_addition_simple(a_in, b_in), unsafe_allow_html=True)
            st.write(f"Result: {a_in+b_in}")
        elif op.startswith("Subtraction"):
            st.write(f"Result: {a_in-b_in}")
        else:
            if b_in==0:
                st.error("Division by zero")
            else:
                st.write(f"Result: {a_in} ÷ {b_in} = {a_in//b_in} remainder {a_in % b_in}")

# ================= FIRST DEGREE =================
elif mode == "First-Degree Equation":
    st.title("1️⃣ First-Degree Equation Solver")
    theory_box("Linear Equation", r"""**Definition:** $a x + b = 0$ or $a x + b = c$, $a \neq 0$. **Solution:** $x = -b/a$.""")
    eq_input = st.text_input("Equation", value="2*x + 3 = 11")
    if st.button("Solve First-Degree", type="primary"):
        if "=" in eq_input:
            left_str, right_str = eq_input.split("=",1)
            left_expr = safe_parse(left_str)
            right_expr = safe_parse(right_str)
            eq_sym = Eq(left_expr, right_expr)
            sol = solve(eq_sym, x)
            st.latex(f"Solution: x = {sp.latex(sol[0])}" if sol else "No solution")

# ================= SECOND DEGREE =================
elif mode == "Second-Degree Equation":
    st.title("2️⃣ Quadratic Solver")
    theory_box("Quadratic", r"""$a x^2 + b x + c =0$, $\Delta = b^2-4ac$, $x = \frac{-b\pm\sqrt{\Delta}}{2a}$""")
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
    theory_box("Integral", r"""$\int f(x)dx = F(x)+C$, $F'=f$""")
    f_input=st.text_input("f(x)", value="x^2 + 3*x")
    if st.button("Integrate", type="primary"):
        f_expr=safe_parse(f_input)
        st.latex(f"\\int f = {sp.latex(sp.integrate(f_expr,x))} + C")
