# app.py – Fully working, guaranteed resolution display
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

# Page config
st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

# Global CSS (only what is needed outside the iframe)
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

# ---------------------------
#  Math Solver Class
# ---------------------------
class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def parse_func(self, func_str):
        if not func_str or not str(func_str).strip():
            return None
        transformations = (standard_transformations + (implicit_multiplication_application,))
        clean_str = str(func_str).replace('^', '**').replace('×', '*').replace('÷', '/').strip()
        # Ensure multiplication between number and variable (e.g., 2x -> 2*x)
        clean_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', clean_str)
        try:
            return parse_expr(clean_str, transformations=transformations)
        except Exception:
            return None

    # ---------- Basic Arithmetic ----------
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

        html = f"""
        <div class="step-box">
            <strong>➕ Column Addition (Step by Step)</strong><br><br>
            <div style="text-align: center;"><pre class="manual-display">{display_text}</pre></div>
            <div class="result-box">🎯 <strong>Result: {n1} + {n2} = {result}</strong></div>
        </div>
        """
        return html

    def manual_sub(self, n1, n2):
        result = n1 - n2
        s1, s2 = str(abs(n1)), str(abs(n2))
        width = max(len(s1), len(s2) + 2, len(str(result))) + 1
        lines = [s1.rjust(width), ("- " + s2).rjust(width), "─" * width, str(result).rjust(width)]
        display_text = "\n".join(lines)
        html = f"""
        <div class="step-box">
            <strong>➖ Column Subtraction (Step by Step)</strong><br><br>
            <div style="text-align: center;"><pre class="manual-display">{display_text}</pre></div>
            <div class="result-box">🎯 <strong>Result: {n1} - {n2} = {result}</strong></div>
        </div>
        """
        return html

    def manual_mul(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        result = n1 * n2
        partials = []
        for i, d in enumerate(reversed(s2)):
            partials.append(int(s1) * int(d) * (10 ** i))
        partials_rev = list(reversed(partials))

        max_w = max(len(s1), len(s2) + 2, max([len(str(p)) for p in partials] or [0]), len(str(result))) + 1
        lines = [s1.rjust(max_w), ("× " + s2).rjust(max_w), "─" * max_w]
        if len(s2) > 1:
            for idx, p in enumerate(partials_rev):
                if idx == len(partials_rev) - 1:
                    lines.append(("+ " + str(p)).rjust(max_w))
                else:
                    lines.append(str(p).rjust(max_w))
            lines.append("─" * max_w)
        lines.append(str(result).rjust(max_w))
        display_text = "\n".join(lines)
        html = f"""
        <div class="step-box">
            <strong>✖️ Long Multiplication (Step by Step)</strong><br><br>
            <div style="text-align: center;"><pre class="manual-display">{display_text}</pre></div>
            <div class="result-box">🎯 <strong>Result: {n1} × {n2} = {result}</strong></div>
        </div>
        """
        return html

    def manual_div(self, n1, n2):
        if n2 == 0:
            return "<div class='step-box'>❌ <b>Error:</b> Division by zero.</div>"
        quotient = n1 // n2
        remainder = n1 % n2
        decimal_res = n1 / n2
        display_text = f" {n1} │ {n2}\n─────┼─────\n {remainder} │ {quotient} (Quotient)"
        if remainder != 0:
            display_text += f"\nRemainder: {remainder}"
        html = f"""
        <div class="step-box">
            <strong>➗ Long Division (with Remainder)</strong><br><br>
            <div style="text-align: center;"><pre class="manual-display">{display_text}</pre></div>
            <p>• <b>Dividend:</b> {n1} • <b>Divisor:</b> {n2} • <b>Integer Quotient:</b> {quotient} • <b>Remainder:</b> {remainder}</p>
            <div class="result-box">🎯 <strong>Result: {n1} ÷ {n2} = {quotient} (Rem {remainder}) | Exact: {decimal_res:.4f}</strong></div>
        </div>
        """
        return html

    # ---------- Algebraic Equations ----------
    def solve_linear(self, eq_str):
        try:
            if '=' not in eq_str:
                return "<div class='step-box'>❌ Please use '=' in the equation.</div>"
            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str.strip())
            right_expr = self.parse_func(right_str.strip())
            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Invalid expression.</div>"
            expr = expand(left_expr - right_expr)
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a, b = (coeffs[0], coeffs[1]) if len(coeffs) == 2 else (0, coeffs[0] if len(coeffs) == 1 else 0)
            if a == 0:
                return "<div class='step-box'>⚠️ Not a linear equation (a = 0).</div>"
            x_sol = -b / a
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Linear Equation (1st Degree)</div>
                <p>Standard form: $ax + b = 0$ → $x = -b/a$</p>
            </div>
            <div class="step-box">
                <strong>📝 Resolution:</strong><br>
                <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                <p>Identifying coefficients: $a = {a},\\ b = {b}$<br>
                $$x = \\frac{{-{b}}}{{{a}}} = {latex(sp.nsimplify(x_sol))}$$</p>
                <div class="result-box">🎯 <strong>Result: $x = {latex(sp.nsimplify(x_sol))}$</strong></div>
            </div>
            """
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    def solve_quadratic(self, func_str):
        try:
            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                expr = expand(self.parse_func(left_str.strip()) - self.parse_func(right_str.strip()))
            else:
                expr = expand(self.parse_func(func_str))
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a, b, c = 0, 0, 0
            if len(coeffs) == 3: a, b, c = coeffs
            elif len(coeffs) == 2: a, b = coeffs
            elif len(coeffs) == 1: a = coeffs[0]
            if a == 0:
                return "<div class='step-box'>⚠️ Not quadratic (a = 0).</div>"
            disc = b**2 - 4*a*c
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Quadratic Equation (Bhaskara's Formula)</div>
                <p>Standard form: $ax^2+bx+c=0$, discriminant $\Delta=b^2-4ac$</p>
            </div>
            <div class="step-box">
                <strong>📝 Resolution:</strong><br>
                <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                <p>$\\Delta = {disc}$</p>
            """
            if disc >= 0:
                x1 = (-b + math.sqrt(disc)) / (2*a)
                x2 = (-b - math.sqrt(disc)) / (2*a)
                html += f"""
                <p>$x_1 = {latex(sp.nsimplify(x1))},\\ x_2 = {latex(sp.nsimplify(x2))}$</p>
                <div class="result-box">🎯 <strong>Roots: $x_1={latex(sp.nsimplify(x1))},\\; x_2={latex(sp.nsimplify(x2))}$</strong></div>
                """
            else:
                real_p, imag_p = -b / (2*a), math.sqrt(-disc) / (2*a)
                html += f"""
                <p>Complex roots: $x = {real_p:.4f} \\pm {imag_p:.4f}i$</p>
                <div class="result-box">🎯 <strong>Complex Roots</strong></div>
                """
            html += "</div>"
            return html
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
                <p>Power, chain, sum, and product rules applied analytically.</p>
            </div>
            <div class="step-box">
                <strong>📝 Derivative:</strong><br>
                <div class="formula-highlight">$$f({var}) = {latex(expr)}$$</div>
                <p>$$f'({var}) = {latex(df)}$$</p>
                <p>Simplified: $$f'({var}) = {latex(simplified_df)}$$</p>
            """
            if eval_pt and str(eval_pt).strip():
                try:
                    pt = parse_expr(str(eval_pt).replace('^', '**'))
                    val = simplified_df.subs(sym_var, pt)
                    html += f"<p>At $x = {latex(pt)}$: $f'({latex(pt)}) = {latex(val)}$"
                    if val.is_number and not val.is_Integer:
                        html += f" ≈ {float(val):.4f}</p>"
                except:
                    html += "<p><i>Could not evaluate at that point.</i></p>"
            html += f"""
                <div class="result-box">🎯 $$\\boxed{{f'({var}) = {latex(simplified_df)}}}$$</div>
            </div>
            """
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
                <p>Term‑by‑term antiderivative calculation.</p>
            </div>
            <div class="step-box">
                <strong>📝 Integral:</strong><br>
                <div class="formula-highlight">$$\\int \\left({latex(expr)}\\right) \\, d{var}$$</div>
                <p>Antiderivative: $$F({var}) = {latex(simplified_prim)}$$</p>
            """
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
                    <div class="result-box">🎯 $$\\boxed{{= {latex(def_res)}}}$$</div>
                    """
                except:
                    html += "<p><i>Invalid limits.</i></p>"
            else:
                html += f"""
                <div class="result-box">🎯 $$\\boxed{{\\int \\left({latex(expr)}\\right) \\, d{var} = {latex(simplified_prim)} + C}}$$</div>
                """
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

# ---------------------------
#  Streamlit App
# ---------------------------
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
        eval_pt = st.text_input("Evaluate at point (Optional, e.g., 2):", "")
        if st.button("📈 Differentiate Step by Step", use_container_width=True):
            html_res = solver.differentiate(func, var, eval_pt)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Derivative: f({var}) = {func}")

    elif mode == "Integration (Definite/Indefinite)":
        func = st.text_input("Function f(x) (e.g., x^2 + 3x):", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        use_limits = st.checkbox("Definite Integral (with limits)")
        low_bnd, upp_bnd = None, None
        if use_limits:
            col_a, col_b = st.columns(2)
            with col_a:
                low_bnd = st.text_input("Lower limit (a):", "0")
            with col_b:
                upp_bnd = st.text_input("Upper limit (b):", "1")
        if st.button("📊 Integrate Step by Step", use_container_width=True):
            html_res = solver.integrate_func(func, var, low_bnd, upp_bnd)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Integral: f({var}) = {func}")

with col_out:
    st.markdown("### ✨ Step-by-Step Solution")
    # Build a complete HTML page with embedded styles and MathJax
    if st.session_state.result_html:
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            }},
            startup: {{
                pageReady: () => {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        MathJax.typesetPromise();
                    }});
                }}
            }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 10px; color: #2d3748;
        }}
        .manual-display {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 20px; font-weight: bold; line-height: 1.3;
            background: #1e293b; color: #38bdf8;
            padding: 14px 20px; border-radius: 8px;
            display: inline-block; white-space: pre;
            text-align: left; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 10px auto;
        }}
        .step-box {{
            background: white; border-radius: 12px; padding: 20px;
            margin: 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #764ba2;
        }}
        .step-number {{
            display: inline-block; background: #667eea; color: white;
            border-radius: 50%; width: 28px; height: 28px;
            text-align: center; line-height: 28px; margin-right: 8px;
            font-weight: bold; font-size: 14px;
        }}
        .formula-highlight {{
            background: #f8fafc; border: 2px solid #667eea;
            border-radius: 10px; padding: 12px; text-align: center;
            margin: 12px 0;
        }}
        .result-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border-radius: 10px; padding: 18px;
            text-align: center; margin: 18px 0;
            font-size: 20px; font-weight: bold;
        }}
        .theory-box {{
            background: #f0f4ff; border-left: 5px solid #667eea;
            border-radius: 10px; padding: 16px; margin: 15px 0;
        }}
        .theory-title {{
            font-size: 18px; font-weight: 700; color: #4c51bf; margin-bottom: 8px;
        }}
    </style>
</head>
<body>
    {st.session_state.result_html}
</body>
</html>"""
        # Render in iframe
        components.html(full_html, height=800, scrolling=True)
    else:
        st.info("👈 Choose an operation mode, enter the data, and click Compute to view the complete step-by-step resolution!")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>🧮 HandCalc Pro – Guaranteed Step-by-Step Resolution</div>", unsafe_allow_html=True)
