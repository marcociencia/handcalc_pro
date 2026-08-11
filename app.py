
import streamlit as st
import sympy as sp
import numpy as np
from sympy import symbols, sympify, Eq, solve, sqrt, diff, integrate, latex, Poly, factor, expand
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import re

st.set_page_config(
    page_title="Advanced Step-by-Step Math Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

x, y, z, t = sp.symbols('x y z t')
SYMBOL_MAP = {'x': x, 'y': y, 'z': z, 't': t}

def safe_parse(expr_str: str, var=x):
    try:
        expr_str = expr_str.replace('^', '**')
        return parse_expr(expr_str, transformations=transformations, local_dict=SYMBOL_MAP)
    except Exception as e:
        return None

def theory_box(title, content_md):
    st.markdown(f"### 📚 Theoretical Background: {title}")
    st.markdown(content_md)
    st.divider()

def step_header(n, title, desc=""):
    st.markdown(f"#### Step {n}: {title}")
    if desc:
        st.markdown(desc)

# ================= LONG ARITHMETIC HELPERS =================
def long_addition_steps(a,b):
    a_str, b_str = str(abs(a)), str(abs(b))
    max_len = max(len(a_str), len(b_str))
    a_str = a_str.zfill(max_len)
    b_str = b_str.zfill(max_len)
    carry=0
    steps=[]
    for i in range(max_len-1, -1, -1):
        da=int(a_str[i]); db=int(b_str[i])
        s=da+db+carry
        steps.insert(0, {"da":da,"db":db,"carry_in":carry,"sum":s,"write":s%10,"carry_out":s//10})
        carry=s//10
    if carry>0:
        steps.insert(0, {"da":0,"db":0,"carry_in":0,"sum":carry,"write":carry,"carry_out":0})
    return steps

def render_addition_html(a,b):
    steps=long_addition_steps(a,b)
    # Orange carries: show carry_in when >0, elevated to left (next unit)
    html='<div style="font-family: monospace; font-size:32px; line-height:1.15; background:#fff; padding:16px; display:inline-block; border-radius:10px; border:1px solid #ddd">'
    html+='<div style="color:#E67E22; font-size:18px; letter-spacing:9px; text-align:right; min-height:22px; font-weight:bold">'
    for stp in steps:
        if stp["carry_in"]>0:
            html+=f'<span style="display:inline-block; width:20px">{stp["carry_in"]}</span>'
        else:
            html+='<span style="display:inline-block; width:20px">&nbsp;</span>'
    html+='</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px">{a}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; border-bottom:2.5px solid black; padding-bottom:4px">+ {b}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; padding-top:6px; font-weight:bold">{a+b}</div>'
    html+='</div>'
    detail='<div style="margin-top:12px; font-family:sans-serif; font-size:15px"><b>Carry logic (right to left, orange = elevated to left unit):</b><br>'
    for idx, stp in enumerate(reversed(steps)):
        if stp["da"]==0 and stp["db"]==0 and idx==len(steps)-1 and stp["carry_out"]==0:
            # skip leading zero added for final carry, already explained
            pass
        detail+=f'Units {len(steps)-idx}: {stp["da"]} + {stp["db"]} + carry {stp["carry_in"]} = {stp["sum"]} → write <b>{stp["write"]}</b>, carry <span style="color:#E67E22">{stp["carry_out"]}</span> to next left column<br>'
    detail+='</div>'
    return html+detail

def render_subtraction_html(a,b):
    # ensure a>=b for visual, else swap and show negative
    neg=False
    if a<b:
        neg=True
        a,b=b,a
    a_str=str(a)
    b_str=str(b).zfill(len(a_str))
    borrow=0
    steps=[]
    res_digits=[]
    for i in range(len(a_str)-1, -1, -1):
        da=int(a_str[i])
        db=int(b_str[i]) if i>=len(a_str)-len(b_str) else 0
        da_eff=da-borrow
        need=1 if da_eff<db else 0
        if need:
            da_eff+=10
        write=da_eff-db
        steps.insert(0, {"da":da,"db":db,"borrow_in":borrow,"da_eff":da_eff,"write":write,"borrow_out":need})
        res_digits.insert(0,str(write))
        borrow=need
    result=int(''.join(res_digits)) if res_digits else 0
    html='<div style="font-family: monospace; font-size:32px; line-height:1.15; background:#fff; padding:16px; display:inline-block; border-radius:10px; border:1px solid #ddd">'
    html+='<div style="color:#E67E22; font-size:18px; letter-spacing:9px; text-align:right; min-height:22px; font-weight:bold">'
    for stp in steps:
        html+=f'<span style="display:inline-block; width:20px">{stp["borrow_in"] if stp["borrow_in"] else "&nbsp;"}</span>'
    html+='</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px">{a_str}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; border-bottom:2.5px solid black">- {b_str.lstrip("0") or "0"}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; padding-top:6px; font-weight:bold">{"-" if neg else ""}{result}</div>'
    html+='</div>'
    detail='<div style="margin-top:12px; font-family:sans-serif; font-size:15px"><b>Borrow logic (orange = borrowed 1 from left unit):</b><br>'
    for stp in reversed(steps):
        detail+=f'{stp["da"]} - borrow {stp["borrow_in"]} = {stp["da"]-stp["borrow_in"]}; if < {stp["db"]} borrow 10 → {stp["da_eff"]} - {stp["db"]} = {stp["write"]}<br>'
    detail+='</div>'
    return html+detail

def long_multiplication_steps(a,b):
    a=abs(a); b=abs(b)
    a_digits=list(map(int,str(a)))
    b_digits=list(map(int,str(b)))[::-1]
    partials=[]
    carries_list=[]
    for bd in b_digits:
        carry=0
        p_digits=[]
        carries=[]
        for ad in reversed(a_digits):
            prod=ad*bd+carry
            p_digits.insert(0,prod%10)
            carries.insert(0,carry)
            carry=prod//10
        if carry>0:
            p_digits.insert(0,carry)
            carries.insert(0,0)
        partials.append(int(''.join(map(str,p_digits))) if p_digits else 0)
        carries_list.append(carries)
    return partials, carries_list, a_digits, b_digits

def render_multiplication_html(a,b):
    partials, carries_list, a_digits, b_digits = long_multiplication_steps(a,b)
    a_str=str(a); b_str=str(b)
    html='<div style="font-family: monospace; font-size:30px; line-height:1.2; background:#fff; padding:18px; display:inline-block; border-radius:10px; border:1px solid #ddd">'
    # Show carry row for each partial when needed - orange elevated to left
    # For first partial, show on top
    if carries_list and any(c>0 for c in carries_list[0]):
        html+='<div style="color:#E67E22; font-size:18px; letter-spacing:9px; text-align:right; min-height:20px; font-weight:bold">'
        for c in carries_list[0]:
            html+=f'<span style="display:inline-block; width:20px">{c if c>0 else "&nbsp;"}</span>'
        html+='</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px">{a_str}</div>'
    html+=f'<div style="text-align:right; letter-spacing:9px; border-bottom:2.5px solid black">X {b_str}</div>'
    for idx, p in enumerate(partials):
        if idx>0 and carries_list[idx] and any(c>0 for c in carries_list[idx]):
            html+='<div style="color:#E67E22; font-size:18px; letter-spacing:9px; text-align:right; min-height:20px; font-weight:bold">'
            for c in carries_list[idx]:
                html+=f'<span style="display:inline-block; width:20px">{c if c>0 else "&nbsp;"}</span>'
            html+=f'<span style="display:inline-block; width:{idx*12}px"></span></div>'
        # Shift visual: each next partial is shifted one place left (like school)
        # We show as number with right padding of idx*? Use margin-right
        shift_style = f'margin-right:{idx*12}px' if idx>0 else ''
        prefix = '+' if idx==len(partials)-1 and len(partials)>1 else ''
        html+=f'<div style="text-align:right; letter-spacing:9px; color:#222"><span style="{shift_style}">{prefix}{p}</span></div>'
    html+='<div style="border-top:2.5px solid black; margin-top:6px; text-align:right; letter-spacing:9px; padding-top:6px; font-weight:bold">'
    html+=f'{a*b}</div>'
    html+='</div>'
    detail='<div style="margin-top:14px; font-family:sans-serif; font-size:15px"><b>Carry rule (orange = left elevated):</b> When digit×digit + carry ≥10, write ones, carry tens to next left column.<br>'
    for idx, bd in enumerate(b_digits):
        detail+=f'Partial {idx+1}: {a} × {bd}<br>'
        carry=0
        for ad in reversed(a_digits):
            prod=ad*bd+carry
            detail+=f'&nbsp;&nbsp;{ad}×{bd}+{carry}={prod} → write {prod%10}, carry <span style="color:#E67E22">{prod//10}</span> to left<br>'
            carry=prod//10
        if carry:
            detail+=f'&nbsp;&nbsp;Final carry {carry} → partial {partials[idx]}<br>'
        detail+=f'→ Shifted {idx} → {partials[idx]}×10^{idx} = {partials[idx]*10**idx}<br><br>'
    detail+=f'<b>Sum = {a*b}</b></div>'
    return html+detail

def long_division_steps(dividend, divisor):
    dividend=abs(dividend); divisor=abs(divisor)
    s=str(dividend)
    steps=[]
    cur=0
    q_digits=[]
    for i,ch in enumerate(s):
        cur=cur*10+int(ch)
        q=cur//divisor
        prod=q*divisor
        rem=cur-prod
        steps.append({"current":cur,"q":q,"prod":prod,"rem":rem})
        q_digits.append(str(q))
        cur=rem
    quotient=int(''.join(q_digits)) if q_digits else 0
    return steps, quotient

def render_division_html(dividend, divisor):
    if divisor==0:
        return '<div style="color:red">Division by zero not allowed</div>'
    steps, quotient = long_division_steps(dividend, divisor)
    remainder = steps[-1]["rem"] if steps else 0
    html='<div style="font-family: monospace; font-size:30px; background:#fff; padding:18px; display:inline-block; border-radius:10px; border:1px solid #ddd">'
    html+='<div style="display:flex">'
    html+='<div style="padding-right:24px; text-align:right">'
    html+=f'<div style="color:black; letter-spacing:4px">{dividend}<span style="display:inline-block; width:34px; border-left:3px solid black; border-bottom:3px solid black; margin-left:12px; padding-left:10px">{divisor}</span></div>'
    for idx, st in enumerate(steps):
        if st["q"]==0 and st["current"]<divisor and idx==0 and len(str(dividend))>1:
            continue
        html+=f'<div style="color:#E67E22; letter-spacing:4px; text-align:right; margin-top:2px">-{st["prod"]}</div>'
        html+=f'<div style="border-top:2px solid #E67E22; margin:2px 0"></div>'
        if idx < len(steps)-1:
            nxt=steps[idx+1]["current"]
            html+=f'<div style="color:#E67E22; letter-spacing:4px; text-align:right">{nxt:02d}</div>' if nxt<10 and len(str(dividend))>1 else f'<div style="color:#E67E22; letter-spacing:4px; text-align:right">{nxt}</div>'
    html+=f'<div style="color:#E67E22; letter-spacing:4px; text-align:right; border-top:2px solid #E67E22; margin-top:4px; padding-top:2px">{remainder:02d}</div>'
    html+='</div>'
    html+=f'<div style="margin-left:8px"><div style="color:#E67E22; font-size:30px; margin-left:12px; margin-top:42px">{quotient}</div></div>'
    html+='</div></div>'
    detail='<div style="margin-top:14px; font-family:sans-serif; font-size:15px"><b>Long Division (orange = intermediate subtraction, elevated remainder):</b><br>'
    for st in steps:
        detail+=f'Current {st["current"]} ÷ {divisor} = {st["q"]} ( {st["q"]}×{divisor}={st["prod"]} ), remainder {st["rem"]}<br>'
    detail+=f'<b>Result {dividend} ÷ {divisor} = {quotient} remainder {remainder}</b></div>'
    return html+detail

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
    st.markdown("**How to write expressions:**")
    st.code("2*x + 3\nx^2 + 3*x + 2\nsin(x) + x**2\n1/(x+1)\nexp(x), sqrt(x), log(x)")
    st.info("All explanations are in English as requested.")

# ================= 0 - BASIC ARITHMETIC =================
if mode == "Basic Arithmetic (Long Method)":
    st.title("🔢 Basic Arithmetic - Handwritten Long Method")
    theory_box("Basic Arithmetic - Carry / Borrow Rule",
    r"""
**Core Rule (orange numbers):** When a column sum or product is $\ge 10$, we write only the ones digit and **carry the tens digit to the left column** (elevated to the next unit). This orange small number on top is the carry.

- **Addition:** Add right to left. Example $8+7=15$ → write $5$, carry $1$ (orange) to tens column: $1$ is elevated to left.
- **Subtraction:** If top < bottom, borrow $10$ from left column (orange $1$ on top).
- **Multiplication:** For each digit multiplication $d_1 \times d_2 + carry$, if result $\ge 10$, write ones, carry tens to left (orange). Example $5 \times 5=25$ → write $5$, carry $2$ orange to left.
- **Division:** Divide partial dividend, multiply back, subtract (orange $-product$), bring down next digit (orange next current). Orange numbers are intermediate steps.
    """)

    op = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"], index=2)
    col_a, col_b = st.columns(2)
    a_in = col_a.number_input("First Number (A)", value=152, min_value=0, max_value=9999999, step=1)
    b_in = col_b.number_input("Second Number (B)", value=153, min_value=0, max_value=9999999, step=1)

    if st.button("Calculate with Handwritten Steps", type="primary"):
        if op == "Addition (+)":
            st.markdown("### ➕ Addition")
            st.markdown(render_addition_html(a_in, b_in), unsafe_allow_html=True)
        elif op == "Subtraction (-)":
            st.markdown("### ➖ Subtraction")
            st.markdown(render_subtraction_html(a_in, b_in), unsafe_allow_html=True)
        elif op == "Multiplication (×)":
            st.markdown("### ✖️ Multiplication")
            st.markdown(render_multiplication_html(a_in, b_in), unsafe_allow_html=True)
        elif op == "Division (÷)":
            st.markdown("### ➗ Division - Keyhole Method")
            if b_in==0:
                st.error("Division by zero not allowed")
            else:
                st.markdown(render_division_html(a_in, b_in), unsafe_allow_html=True)

# ================= 1 - FIRST DEGREE =================
elif mode == "First-Degree Equation":
    st.title("1️⃣ First-Degree Equation Solver")
    theory_box("Linear Equation (First Degree)",
    r"""
**Definition:** $a x + b = 0$ or $a x + b = c$ where $a \neq 0$.
**Properties:** Addition/Subtraction and Multiplication/Division Property of Equality.
**Goal:** Isolate $x$.
**General Solution:** $x = -b/a$.
    """)

    st.subheader("Enter your equation")
    col1, col2 = st.columns([2,1])
    with col1:
        eq_input = st.text_input("Equation (e.g., 2*x + 3 = 7)", value="2*x + 3 = 11")
    with col2:
        solve_mode = st.selectbox("Input mode", ["Full Equation String", "Coefficients a*x + b = c"])

    if solve_mode == "Coefficients a*x + b = c":
        c1, c2, c3 = st.columns(3)
        a_val = c1.number_input("a (coefficient of x)", value=2.0)
        b_val = c2.number_input("b (constant left)", value=3.0)
        c_val = c3.number_input("c (right side)", value=11.0)
        eq_input = f"{a_val}*x + {b_val} = {c_val}"

    if st.button("Solve First-Degree Equation", type="primary"):
        if "=" not in eq_input:
            st.error("Please include '=' in your equation.")
        else:
            left_str, right_str = eq_input.split("=", 1)
            left_expr = safe_parse(left_str)
            right_expr = safe_parse(right_str)
            if left_expr is None or right_expr is None:
                st.error(f"Could not parse equation.")
            else:
                st.markdown("### 🔍 Detailed Step-by-Step Solution")
                eq_sym = Eq(left_expr, right_expr)
                st.latex(sp.latex(eq_sym))
                step_header(1, "Identify and Understand the Equation", f"We have: ${sp.latex(left_expr)} = {sp.latex(right_expr)}$")
                expr_combined = left_expr - right_expr
                expr_expanded = sp.expand(expr_combined)
                st.markdown(f"Bring all terms to left to get standard form $a x + b = 0$.")
                st.latex(f"{sp.latex(left_expr)} - ({sp.latex(right_expr)}) = 0")
                st.latex(f"{sp.latex(expr_expanded)} = 0")
                poly = Poly(expr_expanded, x)
                if poly.degree() == 1:
                    coeffs = poly.all_coeffs()
                    a_std = coeffs[0]
                    b_std = coeffs[1] if len(coeffs) > 1 else 0
                    step_header(2, "Extract Coefficients", f"Standard form $a x + b = 0$")
                    st.latex(f"a = {sp.latex(a_std)}, \\quad b = {sp.latex(b_std)}")
                step_header(3, "Isolate Variable Term", "Subtract $b$ from both sides")
                if poly.degree() == 1:
                    st.latex(f"{sp.latex(a_std)} x + {sp.latex(b_std)} - ({sp.latex(b_std)}) = 0 - ({sp.latex(b_std)})")
                    st.latex(f"{sp.latex(a_std)} x = {-b_std}")
                step_header(4, "Divide by $a$", "Isolate $x$")
                solution = solve(eq_sym, x)
                if solution:
                    sol = solution[0]
                    if poly.degree() == 1:
                        st.latex("x = " + str(-b_std) + "/" + sp.latex(a_std))
                        st.latex(f"x = {sp.latex(sol)}")
                    else:
                        st.latex(f"x = {sp.latex(sol)}")
                step_header(5, "Verification", "Substitute back")
                if solution:
                    sol = solution[0]
                    lhs_check = left_expr.subs(x, sol)
                    rhs_check = right_expr.subs(x, sol)
                    st.latex(f"Left = {sp.latex(sp.simplify(lhs_check))}, Right = {sp.latex(sp.simplify(rhs_check))}")
                    if sp.simplify(lhs_check - rhs_check) == 0:
                        st.success(f"✅ Verified!")

# ================= 2 - SECOND DEGREE =================
elif mode == "Second-Degree Equation":
    st.title("2️⃣ Second-Degree (Quadratic) Equation Solver")
    theory_box("Quadratic Equation",
    r"""
**Definition:** $a x^2 + b x + c = 0, a \neq 0$
**Discriminant:** $\Delta = b^2 - 4ac$
- $\Delta > 0$: Two real roots
- $\Delta = 0$: One double root
- $\Delta < 0$: Complex roots
**Formula:** $x = \frac{-b \pm \sqrt{\Delta}}{2a}$
    """)
    st.subheader("Enter quadratic: a*x^2 + b*x + c = 0")
    col_a, col_b, col_c = st.columns(3)
    a_q = col_a.number_input("a", value=1.0, format="%.5f")
    b_q = col_b.number_input("b", value=-3.0, format="%.5f")
    c_q = col_c.number_input("c", value=2.0, format="%.5f")
    alt_input = st.text_input("Or type full equation", value="x^2 - 3*x + 2 = 0")
    use_alt = st.checkbox("Use text equation instead")

    if st.button("Solve Quadratic", type="primary"):
        if use_alt:
            if "=" not in alt_input:
                st.error("Include '='")
                st.stop()
            l, r = alt_input.split("=",1)
            lex = safe_parse(l)
            rex = safe_parse(r)
            expr = sp.expand(lex - rex)
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            while len(coeffs) < 3:
                coeffs = [0] + coeffs
            a_q, b_q, c_q = float(coeffs[0]), float(coeffs[1]), float(coeffs[2]) if len(coeffs)>2 else 0
            a_sym, b_sym, c_sym = coeffs[0], coeffs[1], coeffs[2] if len(coeffs)>2 else 0
        else:
            a_sym, b_sym, c_sym = sp.nsimplify(a_q), sp.nsimplify(b_q), sp.nsimplify(c_q)
            expr = a_sym*x**2 + b_sym*x + c_sym

        st.markdown("### 🔍 Detailed Solution")
        st.latex(f"{sp.latex(a_sym)} x^2 + {sp.latex(b_sym)} x + {sp.latex(c_sym)} = 0")

        if a_sym == 0:
            st.error("a cannot be zero")
            st.stop()

        step_header(1, "Identify Coefficients")
        st.latex(f"a = {sp.latex(a_sym)}, b = {sp.latex(b_sym)}, c = {sp.latex(c_sym)}")

        step_header(2, "Compute Discriminant")
        delta = b_sym**2 - 4*a_sym*c_sym
        delta_simplified = sp.expand(delta)
        latex_b = sp.latex(b_sym)
        latex_delta = sp.latex(delta_simplified)
        latex_a = sp.latex(a_sym)
        latex_2a = sp.latex(2*a_sym)
        latex_minus_b = sp.latex(-b_sym)
        st.latex("Delta = b^2 - 4ac = (" + latex_b + ")^2 - 4(" + latex_a + ")(" + sp.latex(c_sym) + ") = " + latex_delta)

        step_header(3, "Apply Quadratic Formula")
        st.latex(r"x = \frac{-b \pm \sqrt{\Delta}}{2a}")
        st.latex("x = \\frac{ -(" + latex_b + ") \\pm \\sqrt{" + latex_delta + "}}{2 \\cdot " + latex_a + "}")
        st.latex("x = \\frac{" + latex_minus_b + " \\pm \\sqrt{" + latex_delta + "}}{" + latex_2a + "}")

        step_header(4, "Compute Roots")
        roots = solve(Eq(expr,0), x)
        for i, r in enumerate(roots):
            st.latex(f"x_{i+1} = {sp.latex(r)}")

        if len(roots) == 2:
            step_header(5, "Detailed")
            sqrt_delta = sp.sqrt(delta_simplified)
            x1_form = (-b_sym + sqrt_delta) / (2*a_sym)
            x2_form = (-b_sym - sqrt_delta) / (2*a_sym)
            st.latex("x_1 = \\frac{" + latex_minus_b + " + \\sqrt{" + latex_delta + "}}{" + latex_2a + "} = " + sp.latex(sp.simplify(x1_form)))
            st.latex("x_2 = \\frac{" + latex_minus_b + " - \\sqrt{" + latex_delta + "}}{" + latex_2a + "} = " + sp.latex(sp.simplify(x2_form)))

# ================= 3 - LINEAR SYSTEMS =================
elif mode == "Linear Systems":
    st.title("📐 Linear Systems Solver")
    theory_box("Systems of Linear Equations",
    r"""
**Definition:** Collection of linear equations with same variables.
**Methods:** Substitution, Elimination (Gaussian), Cramer's Rule.
**This solver uses Gaussian Elimination.**
    """)
    size = st.selectbox("System size", ["2x2 (2 equations, 2 variables)", "3x3 (3 equations, 3 variables)"], index=0)
    n = 2 if "2x2" in size else 3
    var_names = ['x', 'y', 'z'][:n]
    A = []
    b_vec = []
    for i in range(n):
        st.markdown(f"**Equation {i+1}:**")
        c = st.columns(n+1)
        row=[]
        for j in range(n):
            val = c[j].number_input(f"a[{i+1},{j+1}] ({var_names[j]})", value=float(1 if i==j else 1 if j==0 else 0), key=f"a_{i}_{j}", format="%.4f")
            row.append(val)
        b_val = c[n].number_input(f"b[{i+1}]", value=float(i+1), key=f"b_{i}", format="%.4f")
        A.append(row)
        b_vec.append(b_val)

    if st.button("Solve Linear System", type="primary"):
        A_np = np.array(A, dtype=float)
        b_np = np.array(b_vec, dtype=float)
        st.markdown("### 🔍 Gaussian Elimination")
        Aug = np.hstack([A_np, b_np.reshape(-1,1)])
        st.latex(sp.latex(sp.Matrix(Aug)))
        det = np.linalg.det(A_np)
        st.latex(f"\\det(A) = {det:.6f}")
        M = np.hstack([A_np, b_np.reshape(-1,1)]).copy()
        for col in range(n):
            pivot_row = col + np.argmax(np.abs(M[col:, col]))
            if abs(M[pivot_row, col]) < 1e-12:
                continue
            if pivot_row != col:
                M[[col, pivot_row]] = M[[pivot_row, col]]
                st.latex(sp.latex(sp.Matrix(np.round(M,4))))
            pivot = M[col, col]
            for r in range(col+1, n):
                factor = M[r, col] / pivot
                if abs(factor) > 1e-12:
                    M[r, :] = M[r, :] - factor * M[col, :]
                    st.latex(sp.latex(sp.Matrix(np.round(M,4))))
        x_sol = np.zeros(n)
        for i in reversed(range(n)):
            if abs(M[i,i]) < 1e-12:
                continue
            sum_ax = np.dot(M[i, i+1:n], x_sol[i+1:n])
            x_sol[i] = (M[i, -1] - sum_ax) / M[i,i]
            st.latex(f"{var_names[i]} = {x_sol[i]:.6f}")
        st.success("### ✅ Final Solution:")
        for i, name in enumerate(var_names):
            st.latex(f"{name} = {x_sol[i]:.8f}")

# ================= 4 - DERIVATIVE =================
elif mode == "Derivative":
    st.title("📈 Derivative Solver")
    theory_box("Derivatives",
    r"""
**Definition:** $f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$
**Rules:** Power, Product, Quotient, Chain.
    """)
    f_input = st.text_input("f(x) =", value="x^3 + 2*x^2 - 5*x + sin(x)")
    var_choice = st.selectbox("Variable", ["x", "t"], index=0)
    var = x if var_choice=="x" else t
    order = st.slider("Order", 1, 3, 1)
    if st.button("Compute Derivative", type="primary"):
        f_expr = safe_parse(f_input, var=var)
        if f_expr is None:
            st.error("Could not parse")
            st.stop()
        st.markdown("### 🔍 Differentiation")
        st.latex(f"f({var_choice}) = {sp.latex(f_expr)}")
        f_prime = sp.diff(f_expr, var, order)
        st.latex(f"f^{order} = {sp.latex(sp.simplify(f_prime))}")

# ================= 5 - INTEGRAL =================
elif mode == "Integral":
    st.title("∫ Integral Solver")
    theory_box("Integrals",
    r"""
**Indefinite:** $\int f(x) dx = F(x)+C$ where $F'=f$
**Definite:** $\int_a^b f(x) dx = F(b)-F(a)$
**Rules:** Power, Sum, Substitution, by Parts.
    """)
    f_int_input = st.text_input("f(x) =", value="x^2 + 3*x + 2")
    int_type = st.radio("Type", ["Indefinite", "Definite"], horizontal=True)
    var_int_choice = st.selectbox("Variable", ["x", "t"], index=0, key="var_int")
    var_int = x if var_int_choice=="x" else t
    a_lim = b_lim = None
    if int_type == "Definite":
        c1, c2 = st.columns(2)
        a_lim = c1.number_input("Lower a", value=0.0)
        b_lim = c2.number_input("Upper b", value=1.0)
    if st.button("Compute Integral", type="primary"):
        f_expr = safe_parse(f_int_input, var=var_int)
        if f_expr is None:
            st.error("Could not parse")
            st.stop()
        st.markdown("### 🔍 Integration")
        st.latex(f"f({var_int_choice}) = {sp.latex(f_expr)}")
        antideriv = sp.integrate(f_expr, var_int)
        st.latex(f"\\int {sp.latex(f_expr)} d{var_int_choice} = {sp.latex(antideriv)} + C")
        if int_type == "Definite" and a_lim is not None:
            definite_val = sp.integrate(f_expr, (var_int, a_lim, b_lim))
            st.latex(f"\\int_{{{a_lim}}}^{{{b_lim}}} = {sp.latex(definite_val)}")

st.caption("Built with SymPy + Streamlit | All steps in English | Handwritten long method with orange carries")
