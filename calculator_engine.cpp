
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

# ================= CORRECTED MULTIPLICATION - EXACT IMAGE LOGIC =================
# Rule from user:
# - Multiplicand = top (152)
# - Multiplier = bottom (153) -> digits are multiplicadores, 5 is tens
# - Multiplier digit 3 (below multiplicand 2) x5=15 -> 5 descends, 1 orange above multiplicand 1
# - Product 760: 0 aligned to multiplier 5 (below 456), then 76 left of 0
# - Product 152: 2 aligned to multiplier 1 (below 760), 15 left of 2

def render_multiplication_corrected_html(a,b):
    if b==0 or a==0:
        return f'<div style="font-family:monospace; font-size:28px">{a} × {b} = 0</div>'
    a = abs(int(a)); b = abs(int(b))
    a_str = str(a)
    b_str = str(b)
    n_a = len(a_str)
    n_b = len(b_str)
    b_rev = list(map(int, b_str[::-1]))  # units first: [3,5,1] for 153

    max_pos = n_a + n_b  # enough columns

    # Compute partials: each partial's digits dict pos->char and carries list
    partials = []
    for p_idx, bd in enumerate(b_rev):
        pos_offset = p_idx  # rightmost digit of this partial aligned under multiplier digit at pos p_idx
        carry = 0
        row_dict = {}
        carries = []  # list of {pos, value}
        # Process multiplicand digits from rightmost to leftmost
        for j in range(n_a-1, -1, -1):
            ad = int(a_str[j])
            a_pos = n_a-1 - j  # 0 for rightmost digit of a
            write_pos = a_pos + pos_offset
            prod = ad * bd + carry
            write = prod % 10
            new_carry = prod // 10
            row_dict[write_pos] = str(write)
            if new_carry > 0:
                carries.append({"pos": write_pos+1, "value": new_carry})
            carry = new_carry
        if carry > 0:
            # Extra leading digit
            extra_pos = n_a + pos_offset
            # Handle multi-digit carry (rare)
            extra_str = str(carry)
            # Place from rightmost of extra
            for k, ch in enumerate(reversed(extra_str)):
                row_dict[extra_pos + k] = ch
        partials.append({"b_digit": bd, "pos_offset": pos_offset, "row": row_dict, "carries": carries, "value": a*bd})

    # Build HTML
    html = '<div style="background:#fff; padding:20px; display:inline-block; border-radius:12px; border:1px solid #ddd">'

    # Helper to render a row dict as flex from max_pos-1 down to 0
    def render_row(row_dict, small=False, color="#000000", is_plus=False):
        h = '<div style="display:flex; justify-content:flex-start; font-family:monospace; '
        if small:
            h += 'font-size:18px; color:#E67E22; font-weight:bold; min-height:22px; '
        else:
            h += 'font-size:32px; '
        h += '">'
        for pos in range(max_pos-1, -1, -1):
            ch = row_dict.get(pos, "")
            # plus handling: if is_plus, we want + at leftmost+1
            if is_plus and pos == max(row_dict.keys())+1 if row_dict else False:
                ch = "+"
            style = f'width:34px; text-align:center; color:{color if not small else "#E67E22"};'
            h += f'<div style="{style}">{ch if ch else "&nbsp;"}</div>'
        h += '</div>'
        return h

    # 1. Top carry row for first partial (only first partial's carries) - above multiplicand
    if partials and partials[0]["carries"]:
        carry_dict = {c["pos"]: str(c["value"]) for c in partials[0]["carries"]}
        html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:18px; color:#E67E22; font-weight:bold; min-height:22px">'
        for pos in range(max_pos-1, -1, -1):
            ch = carry_dict.get(pos, "")
            html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html += '</div>'

    # 2. Multiplicand row (152) - right aligned: its digits at pos 0..n_a-1
    html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px">'
    for pos in range(max_pos-1, -1, -1):
        if pos < n_a:
            ch = a_str[n_a-1 - pos] if pos < n_a else ""
            # Actually a_str right aligned: pos 0 = rightmost of a
            if pos < n_a:
                ch = a_str[n_a-1 - pos]
            else:
                ch = ""
        else:
            ch = ""
        html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
    html += '</div>'

    # 3. Multiplier row X 153 - X at position n_a, digits at pos 0..n_b-1
    html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px">'
    for pos in range(max_pos-1, -1, -1):
        if pos == n_a:
            html += f'<div style="width:34px; text-align:center">X</div>'
        elif pos < n_b:
            ch = b_str[n_b-1 - pos]
            html += f'<div style="width:34px; text-align:center">{ch}</div>'
        else:
            html += f'<div style="width:34px; text-align:center">&nbsp;</div>'
    html += '</div>'

    # 4. Line
    html += f'<div style="border-top:3px solid black; margin:6px 0; width:{max_pos*34}px"></div>'

    # 5. Partial 0 row 456
    p0 = partials[0]
    html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
    for pos in range(max_pos-1, -1, -1):
        ch = p0["row"].get(pos, "")
        html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
    html += '</div>'

    # 6. Carry row for partial 1 (2 1) - above 760
    if len(partials) > 1:
        p1_carries = partials[1]["carries"]
        carry_dict = {c["pos"]: str(c["value"]) for c in p1_carries}
        html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:18px; color:#E67E22; font-weight:bold; min-height:22px">'
        for pos in range(max_pos-1, -1, -1):
            ch = carry_dict.get(pos, "")
            html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html += '</div>'

    # 7. Partial 1 row 760 - 0 aligned to multiplier 5 (pos 1)
    if len(partials) > 1:
        p1 = partials[1]
        html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
        for pos in range(max_pos-1, -1, -1):
            ch = p1["row"].get(pos, "")
            html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html += '</div>'

    # 8. Partial 2 row +152 - 2 aligned to multiplier 1 (pos 2)
    if len(partials) > 2:
        p2 = partials[2]
        html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:30px">'
        for pos in range(max_pos-1, -1, -1):
            if pos == max(p2["row"].keys())+1:
                html += f'<div style="width:34px; text-align:center">+</div>'
            else:
                ch = p2["row"].get(pos, "")
                html += f'<div style="width:34px; text-align:center">{ch if ch else "&nbsp;"}</div>'
        html += '</div>'

    # 9. Line
    html += f'<div style="border-top:3px solid black; margin:8px 0; width:{max_pos*34}px"></div>'

    # 10. Final result
    final_val = a*b
    final_str = str(final_val)
    html += '<div style="display:flex; justify-content:flex-start; font-family:monospace; font-size:32px; font-weight:bold">'
    for pos in range(max_pos-1, -1, -1):
        if pos < len(final_str):
            ch = final_str[len(final_str)-1 - pos]
            html += f'<div style="width:34px; text-align:center">{ch}</div>'
        else:
            html += f'<div style="width:34px; text-align:center">&nbsp;</div>'
    html += '</div>'

    html += '</div>'

    detail = '<div style="margin-top:16px; font-family:sans-serif; font-size:14px; background:#f9fafb; padding:12px; border-radius:8px">'
    detail += '<b>Posicionamento exato como você pediu:</b><br>'
    detail += f'• Multiplicadores são os dígitos de {b} (153): 3 abaixo do 2 (unidade), 5 é dezena, 1 é centena<br>'
    detail += f'• 3×5=15: desce 5, <span style="color:#E67E22">1 laranja</span> acima do multiplicando 1 (152)<br>'
    detail += f'• Produto 760: <b>0 alinhado ao multiplicador 5</b> (abaixo de 456), 76 à esquerda do 0<br>'
    detail += f'• Produto 152: <b>2 alinhado ao multiplicador 1</b> (abaixo de 760), 15 à esquerda do 2<br>'
    detail += f'• Soma em escada = {final_val}<br>'
    detail += '</div>'

    return html + detail

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
    theory_box("Regra de Posicionamento (do seu exemplo 152×153)",
    r"""
**Multiplicadores:** Em $153$, cada dígito é um multiplicador: $3$ é unidade (abaixo do $2$ do multiplicando $152$), $5$ é dezena, $1$ é centena.

**Passo 1 - $3 \times 152$:**
- $3 \times 2 =6$ abaixo da linha
- $3 \times 5 =15$: desce $5$ e **$1$ laranja acima do multiplicando $1$**
- $3 \times 1 +1 =4$ → $456$

**Passo 2 - $5 \times 152 =760$:**
- $0$ **alinhado ao multiplicador $5$** (abaixo de $456$), $76$ à esquerda do $0$

**Passo 3 - $1 \times 152 =152$:**
- $2$ **alinhado ao multiplicador $1$** (abaixo de $760$), $15$ à esquerda do $2$

**Soma em escada** = $23256$
    """)
    col_a, col_b = st.columns(2)
    a_in = col_a.number_input("Multiplicand (top) 152", value=152, min_value=0, max_value=9999999)
    b_in = col_b.number_input("Multiplier (bottom) 153 - digits are multiplicadores, 5 is tens", value=153, min_value=0, max_value=9999999)
    if st.button("Show Handwritten Steps", type="primary"):
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
