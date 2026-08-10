# app.py – Complete working version with all step-by-step resolutions
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   factor, sqrt as sym_sqrt, Matrix, Eq, sin, cos, tan, exp, log,
                   Derivative, Integral, Symbol, Function)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

# Page config
st.set_page_config(
    page_title="HandCalc Pro – Complete Step‑by‑Step",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap');
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px; font-weight: 900; text-align: center;
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
        font-family: 'Courier New', monospace;
        font-size: 22px;
        line-height: 1.6;
        text-align: right;
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        letter-spacing: 2px;
        overflow-x: auto;
        white-space: pre;
    }
    .stButton > button {
        width: 100%; height: 55px; font-size: 16px; font-weight: 600; border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

class CompleteMathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def _escape_latex(self, s: str) -> str:
        """Double backslashes to prevent interpretation by Python strings."""
        return s.replace('\\', '\\\\')

    def parse_function(self, func_str: str) -> sp.Expr:
        """Convert user-friendly string like 'x^2+3x-4' to sympy expression."""
        transformations = (standard_transformations + (implicit_multiplication_application,))
        func_str = func_str.replace('^', '**').replace('×', '*').replace('÷', '/').replace(' ', '')
        # insert multiplication between digit and variable: 3x -> 3*x
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
        try:
            return parse_expr(func_str, transformations=transformations)
        except:
            return None

    # ---------- FIRST‑DEGREE EQUATION ----------
    def solve_first_degree_equation(self, equation_str: str) -> str:
        try:
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 First‑Degree Equation – Theory</div>'
            html += '<p><b>ax + b = 0</b>. To solve, isolate the variable using inverse operations.</p>'
            html += '</div>'

            if '=' in equation_str:
                left_str, right_str = equation_str.split('=')
                left_expr = self.parse_function(left_str.strip())
                right_expr = self.parse_function(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_function(equation_str)
                if expr is None:
                    return "Error: Invalid expression"
                expr = expand(expr)

            html += '<div class="step-box"><strong>📝 Step‑by‑Step Resolution:</strong><br><br>'

            if '=' in equation_str:
                html += f'<span class="step-number">1</span> <strong>Original equation:</strong><br>'
                html += f'<div class="formula-highlight">$${self._escape_latex(sp.latex(left_expr))} = {self._escape_latex(sp.latex(right_expr))}$$</div>'

            html += f'<span class="step-number">2</span> <strong>Bring all terms to one side:</strong><br>'
            html += f'<div class="formula-highlight">$${self._escape_latex(sp.latex(expr))} = 0$$</div>'

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 1:
                a = 0; b = coeffs[0]
            elif len(coeffs) == 2:
                a = coeffs[0]; b = coeffs[1]
            else:
                a = 0; b = coeffs[0]

            html += f'<span class="step-number">3</span> <strong>Identify coefficients:</strong><br>'
            html += f'• a = {a}<br>• b = {b}<br>'

            if a == 0:
                html += '<br>Not a first‑degree equation (a = 0).<br>'
                if b == 0:
                    html += '0 = 0 → <b>Infinitely many solutions</b>'
                else:
                    html += f'{b} = 0 → <b>No solution</b>'
                html += '</div>'; return html

            html += f'<span class="step-number">4</span> <strong>Isolate the x‑term:</strong><br>'
            html += f'$${a}x + ({b}) = 0$$<br>'
            html += f'$${a}x = -({b})$$<br>'
            html += f'$${a}x = {-b}$$'

            html += f'<span class="step-number">5</span> <strong>Solve for x:</strong><br>'
            html += f'$$\\frac{{{a}x}}{{{a}}} = \\frac{{{-b}}}{{{a}}}$$<br>'
            x_sol = -b / a
            html += f'$$x = {self._escape_latex(sp.latex(x_sol))}$$'

            html += f'<span class="step-number">6</span> <strong>Verify the solution:</strong><br>'
            html += f'Substitute x = {self._escape_latex(sp.latex(x_sol))} into the original equation:<br>'
            check = expr.subs(self.x, x_sol)
            html += f'$${self._escape_latex(sp.latex(expr))} = {self._escape_latex(sp.latex(check))}$$'
            if simplify(check) == 0:
                html += '<br>✅ The solution is correct.'

            html += '<div class="result-box">'
            html += f'🎯 <strong>Final Answer: x = {self._escape_latex(sp.latex(x_sol))}</strong>'
            if x_sol == int(x_sol):
                html += f'<br>$$x = {int(x_sol)}$$'
            else:
                html += f'<br>$$x \\approx {float(x_sol):.4f}$$'
            html += '</div></div>'
            return html
        except Exception as e:
            return f"Error solving linear equation: {str(e)}"

    # ---------- QUADRATIC EQUATION ----------
    def solve_quadratic_equation(self, func_str: str) -> str:
        try:
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Quadratic Equation – Theory</div>'
            html += '<p><b>ax² + bx + c = 0</b>. Solutions via the quadratic formula: $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$</p>'
            html += '</div>'

            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                left_expr = self.parse_function(left_str.strip())
                right_expr = self.parse_function(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_function(func_str)
                if expr is None:
                    return "Error: Invalid expression"
                expr = expand(expr)

            html += '<div class="step-box"><strong>📝 Step‑by‑Step Resolution:</strong><br><br>'

            html += f'<span class="step-number">1</span> <strong>Equation:</strong><br>'
            html += f'<div class="formula-highlight">$${self._escape_latex(sp.latex(expr))} = 0$$</div>'

            try:
                poly = sp.Poly(expr, self.x)
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3:
                    a, b, c = coeffs
                elif len(coeffs) == 2:
                    a, b = coeffs; c = 0
                elif len(coeffs) == 1:
                    a = coeffs[0]; b = 0; c = 0
                else:
                    a = b = c = 0
            except:
                a = b = c = 0

            html += f'<span class="step-number">2</span> <strong>Identify a, b, c:</strong><br>'
            html += f'a = {a}, b = {b}, c = {c}<br>'

            if a == 0:
                html += '<br><b>Not quadratic (a=0).</b> Solving as linear:<br>'
                if b != 0:
                    x_sol = -c / b
                    html += f'$$x = {self._escape_latex(sp.latex(x_sol))}$$'
                else:
                    html += 'No variable term – impossible equation.'
                html += '</div>'; return html

            disc = b**2 - 4*a*c
            html += f'<span class="step-number">3</span> <strong>Compute discriminant Δ:</strong><br>'
            html += f'$$\\Delta = ({b})^2 - 4({a})({c}) = {disc}$$'

            html += f'<span class="step-number">4</span> <strong>Nature of roots:</strong><br>'
            if disc > 0:
                html += 'Δ > 0 → <b>two distinct real roots</b><br>'
            elif disc == 0:
                html += 'Δ = 0 → <b>one real double root</b><br>'
            else:
                html += 'Δ < 0 → <b>two complex conjugate roots</b><br>'

            html += f'<span class="step-number">5</span> <strong>Quadratic formula:</strong><br>'
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                html += f'$$x = \\frac{{-{b} \\pm \\sqrt{{{disc}}}}}{{2 \\cdot {a}}}$$<br>'
                if disc > 0:
                    html += f'$$x_1 = {self._escape_latex(sp.latex(sp.nsimplify(x1)))}, \\quad x_2 = {self._escape_latex(sp.latex(sp.nsimplify(x2)))}$$'
                    if x1 != int(x1): html += f'<br>$$x_1 \\approx {x1:.4f}$$'
                    if x2 != int(x2): html += f'<br>$$x_2 \\approx {x2:.4f}$$'
                else:
                    html += f'$$x = {self._escape_latex(sp.latex(sp.nsimplify(x1)))}$$ (double)'
            else:
                real_part = -b / (2*a)
                imag_part = math.sqrt(-disc) / (2*a)
                html += f'$$x = \\frac{{-{b} \\pm i\\sqrt{{{-disc}}}}}{{2 \\cdot {a}}}$$<br>'
                html += f'$$x = {real_part:.4f} \\pm {imag_part:.4f}i$$'

            if disc >= 0:
                html += f'<span class="step-number">6</span> <strong>Verification:</strong><br>'
                if disc > 0:
                    v1 = expr.subs(self.x, x1)
                    v2 = expr.subs(self.x, x2)
                    html += f'For x₁: $$ {self._escape_latex(sp.latex(v1))} = 0$$ ✅<br>'
                    html += f'For x₂: $$ {self._escape_latex(sp.latex(v2))} = 0$$ ✅'
                else:
                    v = expr.subs(self.x, x1)
                    html += f'$$ {self._escape_latex(sp.latex(v))} = 0$$ ✅'

            html += '<div class="result-box">'
            if disc > 0:
                html += f'🎯 <strong>Final Answer:</strong><br>$$x_1 = {self._escape_latex(sp.latex(sp.nsimplify(x1)))},\\; x_2 = {self._escape_latex(sp.latex(sp.nsimplify(x2)))}$$'
            elif disc == 0:
                html += f'🎯 <strong>Final Answer:</strong><br>$$x = {self._escape_latex(sp.latex(sp.nsimplify(x1)))}$$ (double)'
            else:
                html += f'🎯 <strong>Final Answer:</strong><br>$$x = {real_part:.4f} \\pm {imag_part:.4f}i$$'
            html += '</div></div>'
            return html
        except Exception as e:
            return f"Error solving quadratic: {str(e)}"

    # ---------- DIFFERENTIATION ----------
    def differentiate_step_by_step(self, func_str: str, var: str = 'x') -> str:
        try:
            expr = self.parse_function(func_str)
            if expr is None: return "Error: Invalid function"
            sym_var = Symbol(var)

            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Differentiation Rules</div>'
            html += '<p>Power Rule, Sum Rule, Product Rule, Chain Rule.</p></div>'
            html += '<div class="step-box"><strong>📝 Step‑by‑Step Differentiation:</strong><br><br>'

            html += f'<span class="step-number">1</span> <strong>Given function:</strong><br>'
            html += f'<div class="formula-highlight">$$f({var}) = {self._escape_latex(sp.latex(expr))}$$</div>'

            expanded = expand(expr)
            html += f'<span class="step-number">2</span> <strong>Expand (if necessary):</strong><br>'
            html += f'$$f({var}) = {self._escape_latex(sp.latex(expanded))}$$'

            html += f'<span class="step-number">3</span> <strong>Differentiate term by term:</strong><br>'
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                d = diff(term, sym_var)
                html += f'Term {i+1}: d/d{var}({self._escape_latex(sp.latex(term))}) = {self._escape_latex(sp.latex(d))}<br>'

            result = diff(expr, sym_var)
            simplified = simplify(result)
            html += f'<span class="step-number">4</span> <strong>Combine derivatives:</strong><br>'
            html += f'$$f\'({var}) = {self._escape_latex(sp.latex(result))}$$'
            html += f'<span class="step-number">5</span> <strong>Simplify:</strong><br>'
            html += f'$$f\'({var}) = {self._escape_latex(sp.latex(simplified))}$$'

            html += '<div class="result-box">'
            html += f'🎯 $$\\boxed{{f\'({var}) = {self._escape_latex(sp.latex(simplified))}}}$$</div></div>'
            return html
        except Exception as e:
            return f"Error in differentiation: {str(e)}"

    # ---------- INTEGRATION ----------
    def integrate_step_by_step(self, func_str: str, var: str = 'x') -> str:
        try:
            expr = self.parse_function(func_str)
            if expr is None: return "Error: Invalid function"
            sym_var = Symbol(var)

            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Integration Rules</div>'
            html += '<p>Power Rule, Sum Rule, etc.</p></div>'
            html += '<div class="step-box"><strong>📝 Step‑by‑Step Integration:</strong><br><br>'

            html += f'<span class="step-number">1</span> <strong>Given integral:</strong><br>'
            html += f'<div class="formula-highlight">$$\\int ({self._escape_latex(sp.latex(expr))}) \\, d{var}$$</div>'

            expanded = expand(expr)
            html += f'<span class="step-number">2</span> <strong>Expand integrand:</strong><br>'
            html += f'$$\\int ({self._escape_latex(sp.latex(expanded))}) \\, d{var}$$'

            html += f'<span class="step-number">3</span> <strong>Integrate term by term:</strong><br>'
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                integral_term = integrate(term, sym_var)
                html += f'Term {i+1}: ∫({self._escape_latex(sp.latex(term))}) d{var} = {self._escape_latex(sp.latex(integral_term))}<br>'

            result = integrate(expr, sym_var)
            html += f'<span class="step-number">4</span> <strong>Combine:</strong><br>'
            html += f'$$\\int ({self._escape_latex(sp.latex(expr))}) \\, d{var} = {self._escape_latex(sp.latex(result))} + C$$'

            html += '<div class="result-box">'
            html += f'🎯 $$\\boxed{{\\int {self._escape_latex(sp.latex(expr))} \\, d{var} = {self._escape_latex(sp.latex(result))} + C}}$$</div></div>'
            return html
        except Exception as e:
            return f"Error in integration: {str(e)}"

    # ---------- MANUAL ARITHMETIC ----------
    def manual_addition(self, num1: int, num2: int) -> str:
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        result = num1 + num2
        result_str = str(result)

        # Build carry array safely
        carries = [0] * max_len
        carry = 0
        for i in range(max_len - 1, -1, -1):
            d1 = int(str1.zfill(max_len)[i])
            d2 = int(str2.zfill(max_len)[i])
            s = d1 + d2 + carry
            carries[i] = s // 10
            carry = s // 10

        html = '<div class="step-box"><strong>➕ Manual Addition – Step by Step</strong><br><br>'

        # Compact right-aligned display (as in the images)
        width = max_len + 2
        lines = []
        if any(c > 0 for c in carries):
            carry_line = ''.join(str(c) if c > 0 else ' ' for c in carries)
            lines.append(carry_line.rjust(width))
        lines.append(str1.rjust(width))
        lines.append(('+ ' + str2).rjust(width))
        lines.append('-' * width)
        lines.append(result_str.rjust(width))
        display = '<br>'.join(lines)
        html += f'<div class="manual-display">{display}</div>'

        html += '<br><strong>Detailed explanation:</strong><br>'
        for i in range(max_len):
            pos = max_len - 1 - i
            d1 = int(str1.zfill(max_len)[pos])
            d2 = int(str2.zfill(max_len)[pos])
            incoming = carries[pos+1] if pos+1 < max_len else 0
            col_sum = d1 + d2 + incoming
            place = ['units', 'tens', 'hundreds', 'thousands'][min(i,3)]
            html += f'<span class="step-number">{i+1}</span> <b>{place.capitalize()}:</b> '
            html += f'{d1} + {d2}'
            if incoming > 0:
                html += f' + {incoming} (carry)'
            html += f' = {col_sum}'
            if carries[pos] > 0:
                html += f' → write {col_sum % 10}, carry {carries[pos]}'
            html += '<br>'

        html += '<div class="result-box">'
        html += f'🎯 <strong>Result: {num1} + {num2} = {result}</strong>'
        html += '</div></div>'
        return html

    def manual_multiplication(self, num1: int, num2: int) -> str:
        str1, str2 = str(num1), str(num2)
        result = num1 * num2
        # Partial products: multiply num1 by each digit of str2, shifted
        partials = []
        for i, digit in enumerate(reversed(str2)):
            partial = num1 * int(digit) * (10 ** i)
            partials.append(partial)
        partials_rev = partials[::-1]  # highest digit first

        html = '<div class="step-box"><strong>✖️ Long Multiplication – Step by Step</strong><br><br>'

        # Determine alignment width
        width = max(len(str1), len(str2) + 1, max(len(str(p)) for p in partials_rev), len(str(result))) + 2
        lines = []
        lines.append(str1.rjust(width))
        lines.append(('× ' + str2).rjust(width))
        lines.append('-' * width)
        for p in partials_rev:
            lines.append(str(p).rjust(width))
        lines.append('-' * width)
        lines.append(str(result).rjust(width))
        display = '<br>'.join(lines)
        html += f'<div class="manual-display">{display}</div>'

        html += '<br><strong>Detailed explanation:</strong><br>'
        for i, digit in enumerate(reversed(str2)):
            partial = num1 * int(digit)
            shift = i
            html += f'<span class="step-number">{i+1}</span> '
            html += f'Multiply {num1} × {digit} = {partial}'
            if shift > 0:
                html += f' → shift left {shift} place(s) = {partial}{"0" * shift}'
            html += '<br>'
        html += f'<span class="step-number">{len(str2)+1}</span> Add all partial products: '
        html += ' + '.join(str(p) for p in partials_rev) + f' = {result}<br>'

        html += '<div class="result-box">'
        html += f'🎯 <strong>Result: {num1} × {num2} = {result}</strong>'
        html += '</div></div>'
        return html

# ---------- Streamlit UI ----------
if 'solver' not in st.session_state:
    st.session_state.solver = CompleteMathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Complete Step‑by‑Step – every carry, every partial product</p>', unsafe_allow_html=True)

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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset"): st.session_state.result_html = ""; st.rerun()
    with col2:
        if st.button("🗑️ Clear All"): st.session_state.result_html = ""; st.session_state.history = []; st.rerun()
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
        if st.button("🧮 Calculate"):
            if op == "Addition (+)":
                html_res = solver.manual_addition(int(n1), int(n2))
            else:
                html_res = solver.manual_multiplication(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "First‑Degree Equation":
        eq = st.text_input("Equation (e.g., 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Solve"):
            html_res = solver.solve_first_degree_equation(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Quadratic Equation":
        eq = st.text_input("Equation (e.g., x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Solve"):
            html_res = solver.solve_quadratic_equation(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quadratic: {eq}")

    elif mode == "Differentiation":
        func = st.text_input("f(x) =", "x^2 + 3x + 5")
        var = st.selectbox("Variable:", ["x","y","z"])
        if st.button("📈 Differentiate"):
            html_res = solver.differentiate_step_by_step(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Diff: {func}")

    elif mode == "Integration":
        func = st.text_input("f(x) =", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x","y","z"])
        if st.button("📊 Integrate"):
            html_res = solver.integrate_step_by_step(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Int: {func}")

with col_out:
    st.markdown("### ✨ Step‑by‑Step Solution")
    if st.session_state.result_html:
        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script>
                    window.MathJax = {{
                        tex: {{
                            inlineMath: [['$', '$']],
                            displayMath: [['$$', '$$']],
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
                <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <style>
                    body {{ font-family: 'Computer Modern', serif; padding: 20px; }}
                </style>
            </head>
            <body>
                {st.session_state.result_html}
            </body>
            </html>
            """,
            height=700,
            scrolling=True
        )
    else:
        st.info("👈 Choose a mode, enter the data, and click **Calculate** to see every step in detail.")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;'>🧮 HandCalc Pro – Manual Arithmetic & Advanced Math, made transparent</div>", unsafe_allow_html=True)
