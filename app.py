# app.py – Final working version with forced iframe refresh (no key argument)
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

# Minimal external styling
st.markdown("""
<style>
    .main-title {
        font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stButton > button {
        width: 100%; height: 50px; font-weight: 600; border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
    }
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

    # ---------- Basic Column Arithmetic ----------
    def manual_add(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        max_len = max(len(s1), len(s2))
        result = n1 + n2
        result_str = str(result)
        carries = []
        carry = 0
        p1, p2 = s1.zfill(max_len), s2.zfill(max_len)
        for i in range(max_len - 1, -1, -1):
            s = int(p1[i]) + int(p2[i]) + carry
            carries.insert(0, s // 10)
            carry = s // 10
        width = max(len(s1), len(s2) + 2, len(result_str)) + 1
        lines = []
        if any(c > 0 for c in carries):
            lines.append("".join(str(c) if c > 0 else " " for c in carries).rjust(width))
        lines.append(s1.rjust(width))
        lines.append(("+ " + s2).rjust(width))
        lines.append("─" * width)
        lines.append(result_str.rjust(width))
        return f"""
        <div class="step-box">
            <strong>➕ Column Addition (Step by Step)</strong><br><br>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 <strong>Result: {n1} + {n2} = {result}</strong></div>
        </div>"""

    def manual_sub(self, n1, n2):
        result = n1 - n2
        s1, s2 = str(abs(n1)), str(abs(n2))
        width = max(len(s1), len(s2) + 2, len(str(result))) + 1
        lines = [s1.rjust(width), ("- " + s2).rjust(width), "─" * width, str(result).rjust(width)]
        return f"""
        <div class="step-box">
            <strong>➖ Column Subtraction (Step by Step)</strong><br><br>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 <strong>Result: {n1} - {n2} = {result}</strong></div>
        </div>"""

    def manual_mul(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        result = n1 * n2
        partials = [int(s1) * int(d) * (10 ** i) for i, d in enumerate(reversed(s2))]
        partials_rev = list(reversed(partials))
        max_w = max(len(s1), len(s2) + 2, max([len(str(p)) for p in partials] or [0]), len(str(result))) + 1
        lines = [s1.rjust(max_w), ("× " + s2).rjust(max_w), "─" * max_w]
        if len(s2) > 1:
            for idx, p in enumerate(partials_rev):
                prefix = "+ " if idx == len(partials_rev) - 1 else ""
                lines.append((prefix + str(p)).rjust(max_w))
            lines.append("─" * max_w)
        lines.append(str(result).rjust(max_w))
        return f"""
        <div class="step-box">
            <strong>✖️ Long Multiplication (Step by Step)</strong><br><br>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 <strong>Result: {n1} × {n2} = {result}</strong></div>
        </div>"""

    def manual_div(self, n1, n2):
        if n2 == 0:
            return "<div class='step-box'>❌ Division by zero.</div>"
        quotient = n1 // n2
        remainder = n1 % n2
        decimal_res = n1 / n2
        display = f" {n1} │ {n2}\n─────┼─────\n {remainder} │ {quotient} (Quotient)"
        if remainder:
            display += f"\nRemainder: {remainder}"
        return f"""
        <div class="step-box">
            <strong>➗ Long Division (with Remainder)</strong><br><br>
            <pre class="manual-display">{display}</pre>
            <p><b>Dividend:</b> {n1} · <b>Divisor:</b> {n2} · <b>Quotient:</b> {quotient} · <b>Remainder:</b> {remainder}</p>
            <div class="result-box">🎯 <strong>Result: {n1} ÷ {n2} = {quotient} (Rem {remainder}) | Decimal: {decimal_res:.4f}</strong></div>
        </div>"""

    # ---------- Algebra ----------
    def solve_linear(self, eq_str):
        try:
            if '=' not in eq_str:
                return "<div class='step-box'>❌ Use an equation with '='.</div>"
            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str)
            right_expr = self.parse_func(right_str)
            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Invalid expression.</div>"
            expr = expand(left_expr - right_expr)
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a = b = 0
            if a == 0:
                return "<div class='step-box'>⚠️ Not a linear equation (a = 0).</div>"
            x_sol = -b / a
            latex_sol = latex(sp.nsimplify(x_sol))
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 Linear Equation (1st Degree)</div>
                <p>Standard form: $ax + b = 0$ → $x = -b/a$</p>
            </div>
            <div class="step-box">
                <strong>📝 Resolution:</strong><br>
                <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                <p>Identifying: $a = {a},\\ b = {b}$<br>
                $$x = \\frac{{-{b}}}{{{a}}} = {latex_sol}$$</p>
                <div class="result-box">🎯 <strong>Solution: $x = {latex_sol}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    def solve_quadratic(self, func_str):
        try:
            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                expr = expand(self.parse_func(left_str) - self.parse_func(right_str))
            else:
                expr = expand(self.parse_func(func_str))
            if expr is None:
                return "<div class='step-box'>❌ Invalid expression.</div>"
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a, b, c = 0, 0, 0
            if len(coeffs) == 3:
                a, b, c = coeffs
            elif len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a = coeffs[0]
            if a == 0:
                return "<div class='step-box'>⚠️ Not quadratic (a = 0).</div>"
            disc = b**2 - 4*a*c
            base = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Quadratic Equation (Bhaskara)</div>
                <p>$ax^2+bx+c=0$, $\\Delta = b^2-4ac$</p>
            </div>
            <div class="step-box">
                <strong>📝 Resolution:</strong><br>
                <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                <p>$\\Delta = {disc}$</p>"""
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                base += f"""
                <p>$x_1 = {latex(sp.nsimplify(x1))}$, $x_2 = {latex(sp.nsimplify(x2))}$</p>
                <div class="result-box">🎯 <strong>Roots: $x_1 = {latex(sp.nsimplify(x1))},\\; x_2 = {latex(sp.nsimplify(x2))}$</strong></div>"""
            else:
                real_p = -b / (2*a)
                imag_p = math.sqrt(-disc) / (2*a)
                base += f"""
                <p>Complex roots: $x = {real_p:.4f} \\pm {imag_p:.4f}i$</p>
                <div class="result-box">🎯 <strong>Complex roots</strong></div>"""
            base += "</div>"
            return base
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- Calculus ----------
    def differentiate(self, func_str, var='x', eval_pt=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid function.</div>"
            sym_var = Symbol(var)
            df = diff(expr, sym_var)
            simplified_df = simplify(df)
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Differentiation Rules</div>
                <p>Power, chain, sum, product rules applied.</p>
            </div>
            <div class="step-box">
                <strong>📝 Derivative:</strong><br>
                <div class="formula-highlight">$$f({var}) = {latex(expr)}$$</div>
                <p>$$f'({var}) = {latex(df)}$$</p>
                <p>Simplified: $$f'({var}) = {latex(simplified_df)}$$</p>"""
            if eval_pt and str(eval_pt).strip():
                try:
                    pt = parse_expr(str(eval_pt).replace('^', '**'))
                    val = simplified_df.subs(sym_var, pt)
                    html += f"<p>At $x = {latex(pt)}$: $f'({latex(pt)}) = {latex(val)}$"
                    if val.is_number and not val.is_Integer:
                        html += f" ≈ {float(val):.4f}</p>"
                    else:
                        html += "</p>"
                except Exception:
                    html += "<p><i>Could not evaluate at that point.</i></p>"
            html += f"""
                <div class="result-box">🎯 $$\\boxed{{f'({var}) = {latex(simplified_df)}}}$$</div>
            </div>"""
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    def integrate_func(self, func_str, var='x', lower=None, upper=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid function.</div>"
            sym_var = Symbol(var)
            primitive = integrate(expr, sym_var)
            simplified_prim = simplify(primitive)
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Integration Rules</div>
                <p>Term‑by‑term antiderivative.</p>
            </div>
            <div class="step-box">
                <strong>📝 Integral:</strong><br>
                <div class="formula-highlight">$$\\int \\left({latex(expr)}\\right) \\, d{var}$$</div>
                <p>Antiderivative: $$F({var}) = {latex(simplified_prim)}$$</p>"""
            if lower and upper and str(lower).strip() and str(upper).strip():
                try:
                    a = parse_expr(str(lower).replace('^', '**'))
                    b = parse_expr(str(upper).replace('^', '**'))
                    Fb = simplified_prim.subs(sym_var, b)
                    Fa = simplified_prim.subs(sym_var, a)
                    def_res = simplify(Fb - Fa)
                    html += f"""
                    <p>Definite integral from ${latex(a)}$ to ${latex(b)}$:<br>
                    $$\\int_{{{latex(a)}}}^{{{latex(b)}}} \\left({latex(expr)}\\right) \\, d{var} = {latex(def_res)}$$</p>
                    <div class="result-box">🎯 $$\\boxed{{= {latex(def_res)}}}$$</div>"""
                except Exception:
                    html += "<p><i>Invalid limits.</i></p>"
            else:
                html += f"""
                <div class="result-box">🎯 $$\\boxed{{\\int \\left({latex(expr)}\\right) \\, d{var} = {latex(simplified_prim)} + C}}$$</div>"""
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

# ---------------------------
#  Streamlit UI
# ---------------------------
if 'solver' not in st.session_state:
    st.session_state.solver = MathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'iframe_version' not in st.session_state:
    st.session_state.iframe_version = 0

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">Step‑by‑Step Mathematics – every carry, every derivative explained</p>', unsafe_allow_html=True)

with st.sidebar:
    mode = st.selectbox("Operation mode:", [
        "Basic Operations (Column)",
        "Linear Equation (1st Degree)",
        "Quadratic Equation (2nd Degree)",
        "Differentiation (Derivatives)",
        "Integration (Definite/Indefinite)"
    ])
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset"):
            st.session_state.result_html = ""
            st.session_state.iframe_version += 1
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All"):
            st.session_state.result_html = ""
            st.session_state.history = []
            st.session_state.iframe_version += 1
            st.rerun()
    st.markdown("---")
    st.markdown("## 📊 History")
    for h in st.session_state.history[-5:]:
        st.info(h)

col_in, col_out = st.columns([1, 1.4])
with col_in:
    st.markdown("### 📝 Input")
    solver = st.session_state.solver

    if mode == "Basic Operations (Column)":
        op = st.selectbox("Operation:", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])
        n1 = st.number_input("First number:", value=145, step=1, format="%d")
        n2 = st.number_input("Second number:", value=12, step=1, format="%d")
        if st.button("🧮 Compute", use_container_width=True):
            if op == "Addition (+)": html_res = solver.manual_add(int(n1), int(n2))
            elif op == "Subtraction (-)": html_res = solver.manual_sub(int(n1), int(n2))
            elif op == "Multiplication (×)": html_res = solver.manual_mul(int(n1), int(n2))
            else: html_res = solver.manual_div(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "Linear Equation (1st Degree)":
        eq = st.text_input("Equation (e.g., 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Solve", use_container_width=True):
            st.session_state.result_html = solver.solve_linear(eq)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Quadratic Equation (2nd Degree)":
        eq = st.text_input("Equation (e.g., x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Solve", use_container_width=True):
            st.session_state.result_html = solver.solve_quadratic(eq)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Quadratic: {eq}")

    elif mode == "Differentiation (Derivatives)":
        func = st.text_input("f(x) =", "x^2 + 3x + 5")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        eval_pt = st.text_input("Evaluate at point (optional):", "")
        if st.button("📈 Differentiate", use_container_width=True):
            st.session_state.result_html = solver.differentiate(func, var, eval_pt)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Diff: f({var}) = {func}")

    elif mode == "Integration (Definite/Indefinite)":
        func = st.text_input("f(x) =", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        use_limits = st.checkbox("Definite integral")
        low_bnd, upp_bnd = None, None
        if use_limits:
            c1, c2 = st.columns(2)
            with c1: low_bnd = st.text_input("Lower limit:", "0")
            with c2: upp_bnd = st.text_input("Upper limit:", "1")
        if st.button("📊 Integrate", use_container_width=True):
            st.session_state.result_html = solver.integrate_func(func, var, low_bnd, upp_bnd)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Integral: f({var}) = {func}")

with col_out:
    st.markdown("### ✨ Step‑by‑Step Solution")

    if st.session_state.result_html:
        # Embed a unique version number to force iframe reload
        full_page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <!-- version {st.session_state.iframe_version} -->
    <script>
        window.MathJax = {{
            tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                    processEscapes: true }},
            startup: {{ pageReady: () => MathJax.startup.defaultPageReady().then(() => MathJax.typesetPromise()) }}
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 10px; color: #1a202c; }}
        .manual-display {{
            font-family: 'Courier New', monospace; font-size: 20px; font-weight: bold; line-height: 1.3;
            background: #1e293b; color: #38bdf8; padding: 14px 20px; border-radius: 8px;
            display: inline-block; white-space: pre; text-align: left; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 10px 0;
        }}
        .step-box {{ background: white; border-radius: 12px; padding: 20px; margin: 15px 0;
                     box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #764ba2; }}
        .formula-highlight {{ background: #f8fafc; border: 2px solid #667eea; border-radius: 10px;
                              padding: 12px; text-align: center; margin: 12px 0; }}
        .result-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
                       border-radius: 10px; padding: 18px; text-align: center; margin: 18px 0;
                       font-size: 20px; font-weight: bold; }}
        .theory-box {{ background: #f0f4ff; border-left: 5px solid #667eea; border-radius: 10px;
                       padding: 16px; margin: 15px 0; }}
        .theory-title {{ font-size: 18px; font-weight: 700; color: #4c51bf; margin-bottom: 8px; }}
    </style>
</head>
<body>
    {st.session_state.result_html}
</body>
</html>"""
        components.html(full_page, height=700, scrolling=True)
    else:
        st.info("👈 Choose a mode, enter data, and click **Compute** to see the complete step‑by‑step resolution.")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>🧮 HandCalc Pro – Every step displayed clearly</div>", unsafe_allow_html=True)
