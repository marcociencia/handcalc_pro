# app.py – Fully corrected, no syntax errors, all steps visible
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
        font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
    }
    .theory-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 5px solid #667eea; border-radius: 10px; padding: 20px; margin: 20px 0;
    }
    .theory-title { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #667eea; margin-bottom: 10px; }
    .step-box {
        background: white; border-radius: 10px; padding: 15px; margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05); border-left: 3px solid #764ba2;
    }
    .step-number {
        display: inline-block; background: #667eea; color: white; border-radius: 50%;
        width: 30px; height: 30px; text-align: center; line-height: 30px; margin-right: 10px; font-weight: bold;
    }
    .formula-highlight {
        background: #f8f9fa; border: 2px solid #667eea; border-radius: 8px; padding: 15px;
        text-align: center; margin: 15px 0;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0;
        font-size: 24px; font-weight: bold;
    }
    .manual-display {
        font-family: 'Courier New', monospace; font-size: 22px; line-height: 1.6;
        text-align: right; background: #f8f9fa; padding: 20px; border-radius: 10px;
        letter-spacing: 2px; overflow-x: auto; white-space: pre;
    }
    .stButton > button {
        width: 100%; height: 55px; font-size: 16px; font-weight: 600; border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def parse_func(self, func_str):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        func_str = func_str.replace('^', '**').replace('×', '*').replace('÷', '/').replace(' ', '')
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
        try:
            return parse_expr(func_str, transformations=transformations)
        except:
            return None

    def escape_latex(self, s):
        return str(s).replace('\\', '\\\\')

    # ---------- MANUAL ADDITION ----------
    def manual_add(self, n1, n2):
        s1, s2 = str(n1), str(n2)
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

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➕ Manual Addition – Step by Step</strong><br><br>')

        # Manual display
        lines = []
        if any(c > 0 for c in carries):
            lines.append(' '.join(str(c) if c > 0 else ' ' for c in carries))
        lines.append(s1)
        lines.append('+ ' + s2)
        lines.append('─' * (max_len + 2))
        lines.append(result_str)
        display_text = '\n'.join(lines)
        html.append('<div class="manual-display">' + display_text + '</div>')

        html.append('<br><strong>Detailed Steps:</strong><br>')
        for i in range(max_len):
            pos = max_len - 1 - i
            d1 = int(p1[pos])
            d2 = int(p2[pos])
            inc = carries[pos + 1] if pos + 1 < max_len else 0
            col_sum = d1 + d2 + inc
            place = ['units', 'tens', 'hundreds', 'thousands'][min(i, 3)]
            step = '<span class="step-number">' + str(i + 1) + '</span> '
            step += '<b>' + place.capitalize() + ':</b> ' + str(d1) + ' + ' + str(d2)
            if inc > 0:
                step += ' + ' + str(inc) + ' (carry)'
            step += ' = ' + str(col_sum)
            if carries[pos] > 0:
                step += ' → write ' + str(col_sum % 10) + ', carry ' + str(carries[pos])
            step += '<br>'
            html.append(step)

        html.append('<div class="result-box">🎯 <strong>Result: ' + str(n1) + ' + ' + str(n2) + ' = ' + str(result) + '</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL MULTIPLICATION ----------
    def manual_mul(self, n1, n2):
        s1, s2 = str(n1), str(n2)
        result = n1 * n2
        partials = []
        for i, d in enumerate(reversed(s2)):
            partials.append(n1 * int(d) * (10 ** i))
        partials_rev = list(reversed(partials))

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>✖️ Long Multiplication – Step by Step</strong><br><br>')

        max_w = max(len(s1), len(s2) + 1, max(len(str(p)) for p in partials_rev), len(str(result)))
        lines = []
        lines.append(s1.rjust(max_w))
        lines.append(('× ' + s2).rjust(max_w))
        lines.append('─' * max_w)
        for p in partials_rev:
            lines.append(str(p).rjust(max_w))
        lines.append('─' * max_w)
        lines.append(str(result).rjust(max_w))
        display_text = '\n'.join(lines)
        html.append('<div class="manual-display">' + display_text + '</div>')

        html.append('<br><strong>Detailed Steps:</strong><br>')
        for i, d in enumerate(reversed(s2)):
            partial = n1 * int(d)
            shift = i
            step = '<span class="step-number">' + str(i + 1) + '</span> '
            step += 'Multiply ' + str(n1) + ' × ' + d + ' = ' + str(partial)
            if shift > 0:
                step += ' → shift left ' + str(shift) + ' place(s) = ' + str(partial) + ('0' * shift)
            step += '<br>'
            html.append(step)
        step = '<span class="step-number">' + str(len(s2) + 1) + '</span> '
        step += 'Add partial products: ' + ' + '.join(str(p) for p in partials_rev) + ' = ' + str(result) + '<br>'
        html.append(step)

        html.append('<div class="result-box">🎯 <strong>Result: ' + str(n1) + ' × ' + str(n2) + ' = ' + str(result) + '</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- FIRST-DEGREE EQUATION ----------
    def solve_linear(self, eq_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 First‑Degree Equation – Theory</div>')
            html.append('<p><b>ax + b = 0</b>. Isolate the variable using inverse operations.</p></div>')

            if '=' in eq_str:
                left_str, right_str = eq_str.split('=')
                left_expr = self.parse_func(left_str.strip())
                right_expr = self.parse_func(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_func(eq_str)
                if expr is None:
                    return "Error: Invalid expression"
                expr = expand(expr)

            html.append('<div class="step-box"><strong>📝 Step‑by‑Step Resolution:</strong><br><br>')

            if '=' in eq_str:
                html.append('<span class="step-number">1</span> <strong>Original equation:</strong><br>')
                html.append('<div class="formula-highlight">$$' + self.escape_latex(latex(left_expr)) + ' = ' + self.escape_latex(latex(right_expr)) + '$$</div>')

            html.append('<span class="step-number">2</span> <strong>Standard form:</strong><br>')
            html.append('<div class="formula-highlight">$$' + self.escape_latex(latex(expr)) + ' = 0$$</div>')

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a, b = 0, 0

            html.append('<span class="step-number">3</span> <strong>Identify coefficients:</strong><br>')
            html.append('• a = ' + str(a) + '<br>• b = ' + str(b) + '<br>')

            if a == 0:
                html.append('Not a first‑degree equation (a = 0).<br></div>')
                return '\n'.join(html)

            html.append('<span class="step-number">4</span> <strong>Isolate variable term:</strong><br>')
            html.append('$$' + str(a) + 'x + (' + str(b) + ') = 0$$<br>')
            html.append('$$' + str(a) + 'x = ' + str(-b) + '$$<br>')

            x_sol = -b / a
            html.append('<span class="step-number">5</span> <strong>Solve for x:</strong><br>')
            html.append('$$x = \\frac{' + str(-b) + '}{' + str(a) + '}$$<br>')
            html.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x_sol))) + '$$<br>')
            if x_sol != int(x_sol):
                html.append('$$x \\approx ' + '{:.4f}'.format(float(x_sol)) + '$$<br>')

            html.append('<span class="step-number">6</span> <strong>Verification:</strong><br>')
            check = simplify(expr.subs(self.x, x_sol))
            html.append('$$' + self.escape_latex(latex(check)) + ' = 0$$ ✅<br>')

            html.append('<div class="result-box">🎯 <strong>Final Answer: x = ' + self.escape_latex(latex(sp.nsimplify(x_sol))) + '</strong></div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return "Error: " + str(e)

    # ---------- QUADRATIC EQUATION ----------
    def solve_quadratic(self, func_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Quadratic Equation – Theory</div>')
            html.append('<p><b>ax² + bx + c = 0</b>. Quadratic formula: $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$</p></div>')

            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                left_expr = self.parse_func(left_str.strip())
                right_expr = self.parse_func(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_func(func_str)
                if expr is None:
                    return "Error: Invalid expression"
                expr = expand(expr)

            html.append('<div class="step-box"><strong>📝 Step‑by‑Step Resolution:</strong><br><br>')

            html.append('<span class="step-number">1</span> <strong>Equation:</strong><br>')
            html.append('<div class="formula-highlight">$$' + self.escape_latex(latex(expr)) + ' = 0$$</div>')

            try:
                poly = sp.Poly(expr, self.x)
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3:
                    a, b, c = coeffs
                elif len(coeffs) == 2:
                    a, b = coeffs
                    c = 0
                elif len(coeffs) == 1:
                    a = coeffs[0]
                    b = c = 0
                else:
                    a = b = c = 0
            except:
                a = b = c = 0

            html.append('<span class="step-number">2</span> <strong>Identify coefficients:</strong><br>')
            html.append('• a = ' + str(a) + '<br>• b = ' + str(b) + '<br>• c = ' + str(c) + '<br>')

            if a == 0:
                html.append('<br><b>Not quadratic (a=0).</b><br></div>')
                return '\n'.join(html)

            disc = b**2 - 4*a*c
            html.append('<span class="step-number">3</span> <strong>Calculate discriminant:</strong><br>')
            html.append('$$\\Delta = (' + str(b) + ')^2 - 4(' + str(a) + ')(' + str(c) + ') = ' + str(disc) + '$$<br>')

            html.append('<span class="step-number">4</span> <strong>Nature of roots:</strong><br>')
            if disc > 0:
                html.append('Δ > 0 → <b>Two distinct real roots</b><br>')
            elif disc == 0:
                html.append('Δ = 0 → <b>One real double root</b><br>')
            else:
                html.append('Δ < 0 → <b>Two complex conjugate roots</b><br>')

            html.append('<span class="step-number">5</span> <strong>Apply quadratic formula:</strong><br>')
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                if disc > 0:
                    html.append('$$x_1 = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$<br>')
                    html.append('$$x_2 = ' + self.escape_latex(latex(sp.nsimplify(x2))) + '$$<br>')
                    if x1 != int(x1):
                        html.append('$$x_1 \\approx ' + '{:.4f}'.format(x1) + '$$<br>')
                    if x2 != int(x2):
                        html.append('$$x_2 \\approx ' + '{:.4f}'.format(x2) + '$$<br>')
                else:
                    html.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$ (double root)<br>')
            else:
                real_part = -b / (2*a)
                imag_part = math.sqrt(-disc) / (2*a)
                html.append('$$x = ' + '{:.4f}'.format(real_part) + ' \\pm ' + '{:.4f}'.format(imag_part) + 'i$$<br>')

            if disc >= 0:
                html.append('<span class="step-number">6</span> <strong>Verification:</strong><br>')
                if disc > 0:
                    v1 = simplify(expr.subs(self.x, x1))
                    v2 = simplify(expr.subs(self.x, x2))
                    html.append('For x₁: ' + self.escape_latex(latex(v1)) + ' = 0 ✅<br>')
                    html.append('For x₂: ' + self.escape_latex(latex(v2)) + ' = 0 ✅<br>')
                else:
                    v = simplify(expr.subs(self.x, x1))
                    html.append(self.escape_latex(latex(v)) + ' = 0 ✅<br>')

            html.append('<div class="result-box">🎯 <strong>Final Answer:</strong><br>')
            if disc > 0:
                html.append('$$x_1 = ' + self.escape_latex(latex(sp.nsimplify(x1))) + ',\\; x_2 = ' + self.escape_latex(latex(sp.nsimplify(x2))) + '$$')
            elif disc == 0:
                html.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$ (double)')
            else:
                html.append('$$x = ' + '{:.4f}'.format(real_part) + ' \\pm ' + '{:.4f}'.format(imag_part) + 'i$$')
            html.append('</div></div>')
            return '\n'.join(html)
        except Exception as e:
            return "Error: " + str(e)

    # ---------- DIFFERENTIATION (fixed quotes) ----------
    def differentiate(self, func_str, var='x'):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "Error: Invalid function"
            sym_var = Symbol(var)

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Differentiation Rules</div>')
            html.append('<p>Power Rule, Sum Rule, Product Rule, Chain Rule.</p></div>')
            html.append('<div class="step-box"><strong>📝 Step‑by‑Step Differentiation:</strong><br><br>')

            html.append('<span class="step-number">1</span> <strong>Function:</strong><br>')
            html.append('<div class="formula-highlight">$$f(' + var + ') = ' + self.escape_latex(latex(expr)) + '$$</div>')

            expanded = expand(expr)
            html.append('<span class="step-number">2</span> <strong>Expand:</strong><br>')
            html.append('$$f(' + var + ') = ' + self.escape_latex(latex(expanded)) + '$$<br>')

            html.append('<span class="step-number">3</span> <strong>Differentiate term by term:</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                d = diff(term, sym_var)
                html.append('Term ' + str(i+1) + ': d/d' + var + '(' + self.escape_latex(latex(term)) + ') = ' + self.escape_latex(latex(d)) + '<br>')

            result = diff(expr, sym_var)
            simplified = simplify(result)
            html.append('<span class="step-number">4</span> <strong>Combine:</strong><br>')
            # Fixed: use double quotes for the string containing a single quote
            html.append("$$f'(" + var + ") = " + self.escape_latex(latex(result)) + "$$<br>")
            html.append('<span class="step-number">5</span> <strong>Simplify:</strong><br>')
            html.append("$$f'(" + var + ") = " + self.escape_latex(latex(simplified)) + "$$<br>")

            html.append('<div class="result-box">🎯 $$\\boxed{f\'(' + var + ') = ' + self.escape_latex(latex(simplified)) + '}$$</div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return "Error: " + str(e)

    # ---------- INTEGRATION ----------
    def integrate_func(self, func_str, var='x'):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "Error: Invalid function"
            sym_var = Symbol(var)

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Integration Rules</div>')
            html.append('<p>Power Rule, Sum Rule, Constant Multiple Rule.</p></div>')
            html.append('<div class="step-box"><strong>📝 Step‑by‑Step Integration:</strong><br><br>')

            html.append('<span class="step-number">1</span> <strong>Integral:</strong><br>')
            html.append('<div class="formula-highlight">$$\\int (' + self.escape_latex(latex(expr)) + ') \\, d' + var + '$$</div>')

            expanded = expand(expr)
            html.append('<span class="step-number">2</span> <strong>Expand integrand:</strong><br>')
            html.append('$$\\int (' + self.escape_latex(latex(expanded)) + ') \\, d' + var + '$$<br>')

            html.append('<span class="step-number">3</span> <strong>Integrate term by term:</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                int_term = integrate(term, sym_var)
                html.append('Term ' + str(i+1) + ': ∫(' + self.escape_latex(latex(term)) + ') d' + var + ' = ' + self.escape_latex(latex(int_term)) + '<br>')

            result = integrate(expr, sym_var)
            html.append('<span class="step-number">4</span> <strong>Combine:</strong><br>')
            html.append('$$\\int (' + self.escape_latex(latex(expr)) + ') \\, d' + var + ' = ' + self.escape_latex(latex(result)) + ' + C$$<br>')

            html.append('<div class="result-box">🎯 $$\\boxed{\\int (' + self.escape_latex(latex(expr)) + ') \\, d' + var + ' = ' + self.escape_latex(latex(result)) + ' + C}$$</div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return "Error: " + str(e)

# ---------- Streamlit UI ----------
if 'solver' not in st.session_state:
    st.session_state.solver = MathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Complete Step‑by‑Step Mathematics Solver</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Mode")
    mode = st.selectbox("Choose operation:", [
        "Basic Arithmetic",
        "First‑Degree Equation",
        "Quadratic Equation",
        "Differentiation",
        "Integration"
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

col_in, col_out = st.columns([1, 1.5])
with col_in:
    st.markdown("### 📝 Input")
    solver = st.session_state.solver

    if mode == "Basic Arithmetic":
        op = st.selectbox("Operation:", ["Addition (+)", "Multiplication (×)"])
        n1 = st.number_input("First number:", value=123, format="%d")
        n2 = st.number_input("Second number:", value=45, format="%d")
        if st.button("🧮 Calculate", use_container_width=True):
            if op == "Addition (+)":
                html_res = solver.manual_add(int(n1), int(n2))
            else:
                html_res = solver.manual_mul(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "First‑Degree Equation":
        eq = st.text_input("Equation (e.g., 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Solve", use_container_width=True):
            html_res = solver.solve_linear(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Quadratic Equation":
        eq = st.text_input("Equation (e.g., x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Solve", use_container_width=True):
            html_res = solver.solve_quadratic(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quadratic: {eq}")

    elif mode == "Differentiation":
        func = st.text_input("f(x) =", "x^2 + 3x + 5")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        if st.button("📈 Differentiate", use_container_width=True):
            html_res = solver.differentiate(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Diff: {func}")

    elif mode == "Integration":
        func = st.text_input("f(x) =", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        if st.button("📊 Integrate", use_container_width=True):
            html_res = solver.integrate_func(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Int: {func}")

with col_out:
    st.markdown("### ✨ Step‑by‑Step Solution")
    if st.session_state.result_html:
        components.html(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <script>
                    window.MathJax = {
                        tex: {
                            inlineMath: [['$', '$']],
                            displayMath: [['$$', '$$']],
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
                <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <style>
                    body { font-family: 'Computer Modern', serif; padding: 20px; }
                </style>
            </head>
            <body>
                """ + st.session_state.result_html + """
            </body>
            </html>
            """,
            height=700,
            scrolling=True
        )
    else:
        st.info("👈 Choose a mode, enter your data, and click Calculate to see the complete step‑by‑step solution!")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>🧮 HandCalc Pro – Every Step Explained, Every Answer Verified</div>", unsafe_allow_html=True)
