# app.py – Fully corrected, integration string mismatch fixed, session state refresh for solver, '+' sign in multiplication
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap');
    .main-title {
        font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%; height: 50px; font-size: 16px; font-weight: 600; border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def parse_func(self, func_str):
        if not func_str or not str(func_str).strip():
            return None
        transformations = (standard_transformations + (implicit_multiplication_application,))
        clean_str = str(func_str).replace('^', '**').replace('×', '*').replace('÷', '/').strip()
        clean_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', clean_str)
        try:
            return parse_expr(clean_str, transformations=transformations)
        except Exception:
            return None

    # ---------- MANUAL ADDITION ----------
    def manual_add(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        max_len = max(len(s1), len(s2))
        result = n1 + n2
        result_str = str(result)

        carries = []
        carry = 0
        p1 = s1.zfill(max_len)
        p2 = s2.zfill(max_len)
        for i in range(max_len - 1, -1, -1):
            s = int(p1[i]) + int(p2[i]) + carry
            carries.insert(0, s // 10)
            carry = s // 10

        width = max(len(s1), len(s2) + 2, len(result_str)) + 1
        lines = []
        if any(c > 0 for c in carries):
            carry_str = "".join(str(c) if c > 0 else " " for c in carries)
            lines.append(carry_str.rjust(width))
        lines.append(s1.rjust(width))
        lines.append(("+ " + s2).rjust(width))
        lines.append("─" * width)
        lines.append(result_str.rjust(width))
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➕ Column Addition (Step by Step)</strong><br><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Result: {n1} + {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL SUBTRACTION ----------
    def manual_sub(self, n1, n2):
        result = n1 - n2
        s1, s2 = str(abs(n1)), str(abs(n2))
        width = max(len(s1), len(s2) + 2, len(str(result))) + 1
        lines = [s1.rjust(width), ("- " + s2).rjust(width), "─" * width, str(result).rjust(width)]
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➖ Column Subtraction (Step by Step)</strong><br><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Result: {n1} - {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL MULTIPLICATION ----------
    def manual_mul(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        result = n1 * n2
        partials = []
        for i, d in enumerate(reversed(s2)):
            partials.append(int(s1) * int(d) * (10 ** i))
        partials_rev = list(reversed(partials))

        max_w = max(len(s1), len(s2) + 2, max([len(str(p)) for p in partials] or [0]), len(str(result))) + 1
        lines = []
        lines.append(s1.rjust(max_w))
        lines.append(("× " + s2).rjust(max_w))
        lines.append("─" * max_w)
        if len(s2) > 1:
            for idx, p in enumerate(partials_rev):
                if idx == len(partials_rev) - 1:
                    lines.append(("+ " + str(p)).rjust(max_w))
                else:
                    lines.append(str(p).rjust(max_w))
            lines.append("─" * max_w)
        lines.append(str(result).rjust(max_w))
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>✖️ Column Multiplication (Step by Step)</strong><br><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Result: {n1} × {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL DIVISION (WITH REMAINDER) ----------
    def manual_div(self, n1, n2):
        if n2 == 0:
            return "<div class='step-box'>❌ <b>Error:</b> Division by zero is not allowed.</div>"
        
        quotient = n1 // n2
        remainder = n1 % n2
        decimal_res = n1 / n2

        display_text = f" {n1} │ {n2}\n"
        display_text += f"─────┼─────\n"
        display_text += f" {remainder} │ {quotient} (Quotient)\n"
        if remainder != 0:
            display_text += f"\nRemainder: {remainder}"

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➗ Long Division (with Remainder)</strong><br><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display">' + display_text + '</pre></div>')
        html.append(f'<br>• <b>Dividend:</b> {n1}<br>• <b>Divisor:</b> {n2}<br>• <b>Integer Quotient:</b> {quotient}<br>• <b>Remainder:</b> {remainder}<br>')
        html.append(f'<div class="result-box">🎯 <strong>Result: {n1} ÷ {n2} = {quotient} (Remainder: {remainder}) | Exact: {decimal_res:.4f}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- FIRST-DEGREE EQUATION ----------
    def solve_linear(self, eq_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Linear Equation (1st Degree)</div>')
            html.append('<p><b>ax + b = 0</b>. Isolate the unknown using inverse operations.</p></div>')

            if '=' in eq_str:
                left_str, right_str = eq_str.split('=')
                left_expr = self.parse_func(left_str)
                right_expr = self.parse_func(right_str)
                if left_expr is None or right_expr is None:
                    return "<div class='step-box'>❌ Invalid equation.</div>"
                expr = expand(left_expr - right_expr)
            else:
                expr = expand(self.parse_func(eq_str))

            html.append('<div class="step-box"><strong>📝 Step-by-Step Resolution:</strong><br><br>')
            html.append(f'<div class="formula-highlight">$${latex(expr)} = 0$$</div>')

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a, b = (coeffs[0], coeffs[1]) if len(coeffs) == 2 else (0, coeffs[0] if len(coeffs) == 1 else 0)

            if a == 0:
                html.append('<b>Not a linear equation (a = 0).</b></div>')
                return '\n'.join(html)

            x_sol = -b / a
            html.append(f'$$x = \\frac{{{-b}}}{{{a}}} = {latex(sp.nsimplify(x_sol))}$$<br>')
            html.append(f'<div class="result-box">🎯 <strong>Result: $x = {latex(sp.nsimplify(x_sol))}$</strong></div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- QUADRATIC EQUATION ----------
    def solve_quadratic(self, func_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Quadratic Equation (Bhaskara\'s Formula)</div>')
            html.append('<p><b>ax² + bx + c = 0</b></p></div>')

            if '=' in func_str:
                left_str, right_str = func_str.split('=') if '=' in func_str else (func_str, '')
                expr = expand(self.parse_func(left_str) - self.parse_func(right_str))
            else:
                expr = expand(self.parse_func(func_str))

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a, b, c = 0, 0, 0
            if len(coeffs) == 3: a, b, c = coeffs
            elif len(coeffs) == 2: a, b = coeffs
            elif len(coeffs) == 1: a = coeffs[0]

            if a == 0:
                return "<div class='step-box'>❌ Not a quadratic equation (a = 0).</div>"

            disc = b**2 - 4*a*c
            html.append(f'<div class="step-box"><strong>📝 Resolution:</strong><br>$$\\Delta = {disc}$$<br>')
            if disc >= 0:
                x1 = (-b + math.sqrt(disc)) / (2*a)
                x2 = (-b - math.sqrt(disc)) / (2*a)
                html.append(f'<div class="result-box">🎯 $x_1 = {latex(sp.nsimplify(x1))}, \\; x_2 = {latex(sp.nsimplify(x2))}$</div>')
            else:
                real_p, imag_p = -b / (2*a), math.sqrt(-disc) / (2*a)
                html.append(f'<div class="result-box">🎯 $x = {real_p:.4f} \\pm {imag_p:.4f}i$</div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- DIFFERENTIATION ----------
    def differentiate(self, func_str, var='x', eval_pt=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ <b>Error:</b> Invalid function.</div>"

            sym_var = Symbol(var)
            df = diff(expr, sym_var)
            simplified_df = simplify(df)

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Applied Differentiation Rules</div>')
            html.append('• Power, Chain, Sum, and Product rules applied analytically.</div>')
            html.append('<div class="step-box"><strong>📝 Step-by-Step Derivative:</strong><br><br>')

            html.append(f'<span class="step-number">1</span> <b>Original Function:</b><br>')
            html.append(f'<div class="formula-highlight">$$f({var}) = {latex(expr)}$$</div>')

            html.append(f'<span class="step-number">2</span> <b>Calculated Derivative:</b><br>')
            html.append(f'$$f\'({var}) = {latex(df)}$$<br>')

            html.append(f'<span class="step-number">3</span> <b>Simplified Form:</b><br>')
            html.append(f'$$f\'({var}) = {latex(simplified_df)}$$<br>')

            if eval_pt is not None and str(eval_pt).strip() != "":
                try:
                    clean_pt = str(eval_pt).strip().replace('^', '**')
                    pt_val = parse_expr(clean_pt)
                    val_result = simplified_df.subs(sym_var, pt_val)
                    html.append(f'<span class="step-number">4</span> <b>Evaluation at Point ($' + var + ' = ' + latex(pt_val) + '$):</b><br>')
                    html.append(f'$$f\'({latex(pt_val)}) = {latex(val_result)}$$')
                    if val_result.is_number and not val_result.is_Integer:
                        html.append(f' $$\\approx {float(val_result):.4f}$$')
                    html.append('<br>')
                except Exception as eval_err:
                    html.append(f'<br><i>Notice: Could not evaluate at point ({eval_err})</i><br>')

            html.append(f'<div class="result-box">🎯 $$\\boxed{{f\'({var}) = {latex(simplified_df)}}}$$</div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Error calculating derivative: {str(e)}</div>"

    # ---------- INTEGRATION ----------
    def integrate_func(self, func_str, var='x', lower_bound=None, upper_bound=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ <b>Error:</b> Invalid function.</div>"

            sym_var = Symbol(var)
            is_definite = False
            a_val, b_val = None, None

            if lower_bound is not None and upper_bound is not None and str(lower_bound).strip() != "" and str(upper_bound).strip() != "":
                try:
                    a_val = parse_expr(str(lower_bound).replace('^', '**'))
                    b_val = parse_expr(str(upper_bound).replace('^', '**'))
                    is_definite = True
                except Exception:
                    is_definite = False

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Integration Rules</div>')
            html.append('• Term-by-term integration and antiderivative calculation.</div>')
            html.append('<div class="step-box"><strong>📝 Step-by-Step Integral:</strong><br><br>')

            if is_definite:
                html.append(f'<div class="formula-highlight">$$\\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\left({latex(expr)}\\right) \\, d{var}$$</div>')
            else:
                html.append(f'<div class="formula-highlight">$$\\int \\left({latex(expr)}\\right) \\, d{var}$$</div>')

            primitive = integrate(expr, sym_var)
            simplified_prim = simplify(primitive)

            html.append(f'<span class="step-number">2</span> <b>Antiderivative $F({var})$:</b><br>')
            html.append(f'$$F({var}) = {latex(simplified_prim)}$$<br>')

            if is_definite:
                fb = simplified_prim.subs(sym_var, b_val)
                fa = simplified_prim.subs(sym_var, a_val)
                def_result = simplify(fb - fa)
                html.append(f'<span class="step-number">3</span> <b>Fundamental Theorem of Calculus ($F(b) - F(a)$):</b><br>')
                html.append(f'$$\\left({latex(fb)}\\right) - \\left({latex(fa)}\\right) = {latex(def_result)}$$<br>')
                if def_result.is_number and not def_result.is_Integer:
                    html.append(f'Approximate value: $$\\approx {float(def_result):.4f}$$<br>')
                html.append(f'<div class="result-box">🎯 $$\\boxed{{\\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\left({latex(expr)}\\right) \\, d{var} = {latex(def_result)}}}$$</div>')
            else:
                html.append(f'<div class="result-box">🎯 $$\\boxed{{\\int \\left({latex(expr)}\\right) \\, d{var} = {latex(simplified_prim)} + C}}$$</div>')

            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Error calculating integral: {str(e)}</div>"

# ---------- Streamlit UI ----------
st.session_state.solver = MathSolver()

if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">Step-by-Step Math Resolution with LaTeX and Column Operations</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Operation Mode")
    mode = st.selectbox("Choose calculation:", [
        "Basic Operations (Column)",
        "Linear Equation (1st Degree)",
        "Quadratic Equation (2nd Degree)",
        "Differentiation (Derivatives)",
        "Integration (Definite/Indefinite)"
    ])
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Reset"):
            st.session_state.result_html = ""
            st.rerun()
    with c2:
        if st.button("🗑️ Clear All"):
            st.session_state.result_html = ""
            st.session_state.history = []
            st.rerun()
    st.markdown("---")
    st.markdown("## 📊 History")
    for h in st.session_state.history[-5:]:
        st.info(h)

col_in, col_out = st.columns([1, 1.4])
with col_in:
    st.markdown("### 📝 Data Input")
    solver = st.session_state.solver

    if mode == "Basic Operations (Column)":
        op = st.selectbox("Operation:", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])
        n1 = st.number_input("First number (Dividend):", value=145, step=1, format="%d")
        n2 = st.number_input("Second number (Divisor):", value=12, step=1, format="%d")
        if st.button("🧮 Compute Column Operation", use_container_width=True):
            if op == "Addition (+)":
                html_res = solver.manual_add(int(n1), int(n2))
            elif op == "Subtraction (-)":
                html_res = solver.manual_sub(int(n1), int(n2))
            elif op == "Multiplication (×)":
                html_res = solver.manual_mul(int(n1), int(n2))
            else:
                html_res = solver.manual_div(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "Linear Equation (1st Degree)":
        eq = st.text_input("Equation (e.g., 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Solve Equation", use_container_width=True):
            html_res = solver.solve_linear(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Quadratic Equation (2nd Degree)":
        eq = st.text_input("Equation (e.g., x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Solve Equation", use_container_width=True):
            html_res = solver.solve_quadratic(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quadratic: {eq}")

    elif mode == "Differentiation (Derivatives)":
        func = st.text_input("Function f(x) (e.g., x^2 + 3x + 5):", "x^2 + 3x + 5")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        eval_pt = st.text_input("Evaluate at point / limit (Optional, e.g., 2 or pi):", "")
        if st.button("📈 Differentiate Step by Step", use_container_width=True):
            html_res = solver.differentiate(func, var, eval_pt)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Derivative: f({var}) = {func}")

    elif mode == "Integration (Definite/Indefinite)":
        func = st.text_input("Function f(x) (e.g., x^2 + 3x):", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        use_limits = st.checkbox("Definite Integral (with integration limits)")
        low_bnd, upp_bnd = None, None
        if use_limits:
            col_a, col_b = st.columns(2)
            with col_a:
                low_bnd = st.text_input("Lower Limit (a):", "0")
            with col_b:
                upp_bnd = st.text_input("Upper Limit (b):", "1")

        if st.button("📊 Integrate Step by Step", use_container_width=True):
            html_res = solver.integrate_func(func, var, low_bnd, upp_bnd)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Integral: f({var}) = {func}")

with col_out:
    st.markdown("### ✨ Step-by-Step Solution")
    if st.session_state.result_html:
        components.html(
            """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            startup: {
                pageReady: () => {
                    return MathJax.startup.defaultPageReady().then(() => {
                        MathJax.typesetPromise();
                    });
                }
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 10px; color: #2d3748; }
        .manual-display {
            font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; line-height: 1.3;
            background: #1e293b; color: #38bdf8; padding: 14px 20px; border-radius: 8px; display: inline-block;
            white-space: pre; text-align: left; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 10px auto;
        }
        .step-box { background: white; border-radius: 12px; padding: 20px; margin: 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #764ba2; }
        .step-number { display: inline-block; background: #667eea; color: white; border-radius: 50%; width: 28px; height: 28px; text-align: center; line-height: 28px; margin-right: 8px; font-weight: bold; font-size: 14px; }
        .formula-highlight { background: #f8fafc; border: 2px solid #667eea; border-radius: 10px; padding: 12px; text-align: center; margin: 12px 0; }
        .result-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; padding: 18px; text-align: center; margin: 18px 0; font-size: 20px; font-weight: bold; }
        .theory-box { background: #f0f4ff; border-left: 5px solid #667eea; border-radius: 10px; padding: 16px; margin: 15px 0; }
        .theory-title { font-size: 18px; font-weight: 700; color: #4c51bf; margin-bottom: 8px; }
    </style>
</head>
<body>
""" + st.session_state.result_html + """
</body>
</html>
""",
            height=800,
            scrolling=True
        )
    else:
        st.info("👈 Choose an operation mode, enter the data, and click Compute to view the complete step-by-step resolution!")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>🧮 HandCalc Pro – Guaranteed Step-by-Step Resolution</div>", unsafe_allow_html=True)
