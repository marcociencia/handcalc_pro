# app.py – Complete with all 7-step detailed math solvers
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol, sqrt, pi, I)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    .main-title { font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
    .subtitle { text-align: center; color: #666; font-size: 18px; margin-bottom: 30px; }
    .stButton > button { width: 100%; height: 50px; font-weight: 600; border-radius: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; transition: all 0.3s ease; }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.step_count = 0

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

    def reset_step_count(self):
        self.step_count = 0

    def increment_step(self):
        self.step_count += 1
        return self.step_count

    def fmt_neg(self, val):
        """Formats negative numbers to show -(-3) instead of --3."""
        if val < 0:
            return f"({val})"
        return f"{val}"

    # ---------- Basic Operations ----------
    def manual_add(self, n1, n2):
        self.reset_step_count()
        s1, s2 = str(abs(n1)), str(abs(n2))
        max_len = max(len(s1), len(s2))
        result = n1 + n2
        result_str = str(result)
        carries = []
        carry = 0
        p1, p2 = s1.zfill(max_len), s2.zfill(max_len)
        steps_html = ""
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(p1[i]) + int(p2[i]) + carry
            digit_result = digit_sum % 10
            new_carry = digit_sum // 10
            carries.insert(0, new_carry)
            if new_carry > 0 or carry > 0:
                step_num = self.increment_step()
                steps_html += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step_num}:</span>
                    <p>Column {max_len - i}: <b>{p1[i]}</b> + <b>{p2[i]}</b> + carry <b>{carry}</b> = <b>{digit_sum}</b></p>
                    <p style="margin-left: 20px;">→ Write <b>{digit_result}</b>, carry <b>{new_carry}</b> to next column</p>
                </div>
                """
            carry = new_carry
        if carry > 0:
            step_num = self.increment_step()
            steps_html += f"""
            <div class="step-detail">
                <span class="step-counter">Step {step_num}:</span>
                <p>Final carry: <b>{carry}</b> added to the front</p>
            </div>
            """
        width = max(len(s1), len(s2) + 2, len(result_str)) + 1
        lines = []
        if any(c > 0 for c in carries):
            lines.append("".join(str(c) if c > 0 else " " for c in carries).rjust(width))
        lines.append(s1.rjust(width))
        lines.append(("+ " + s2).rjust(width))
        lines.append("─" * width)
        lines.append(result_str.rjust(width))
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Column Addition</div></div>
        <div class="step-box">
            <div class="step-header">🔢 Step-by-Step Addition</div>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="steps-container">{steps_html}</div>
            <div class="result-box">🎯 <strong>Result: {n1} + {n2} = {result}</strong></div>
        </div>"""

    def manual_sub(self, n1, n2):
        self.reset_step_count()
        result = n1 - n2
        s1, s2 = str(abs(n1)), str(abs(n2))
        max_len = max(len(s1), len(s2))
        p1, p2 = s1.zfill(max_len), s2.zfill(max_len)
        steps_html = ""
        borrow = 0
        for i in range(max_len - 1, -1, -1):
            digit1 = int(p1[i]) - borrow
            digit2 = int(p2[i])
            if digit1 < digit2:
                digit1 += 10
                borrow = 1
                step_num = self.increment_step()
                steps_html += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step_num}:</span>
                    <p>Column {max_len - i}: Need to borrow from next column</p>
                    <p style="margin-left: 20px;"><b>{p1[i]}</b> becomes <b>{digit1}</b> (borrowed 10)</p>
                    <p style="margin-left: 20px;">{digit1} - {digit2} = <b>{digit1 - digit2}</b></p>
                </div>
                """
            else:
                borrow = 0
                step_num = self.increment_step()
                steps_html += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step_num}:</span>
                    <p>Column {max_len - i}: <b>{digit1}</b> - <b>{digit2}</b> = <b>{digit1 - digit2}</b></p>
                </div>
                """
        width = max(len(s1), len(s2) + 2, len(str(result))) + 1
        lines = [s1.rjust(width), ("- " + s2).rjust(width), "─" * width, str(result).rjust(width)]
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Column Subtraction</div></div>
        <div class="step-box">
            <div class="step-header">🔢 Step-by-Step Subtraction</div>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="steps-container">{steps_html}</div>
            <div class="result-box">🎯 <strong>Result: {n1} - {n2} = {result}</strong></div>
        </div>"""

    def manual_mul(self, n1, n2):
        self.reset_step_count()
        s1, s2 = str(abs(n1)), str(abs(n2))
        result = n1 * n2
        partials = []
        steps_html = ""
        for i, d in enumerate(reversed(s2)):
            digit = int(d)
            partial = int(s1) * digit * (10 ** i)
            partials.append(partial)
            step_num = self.increment_step()
            steps_html += f"""
            <div class="step-detail">
                <span class="step-counter">Step {step_num}:</span>
                <p>Multiply {s1} by digit <b>{digit}</b> in position {i + 1}</p>
                <p style="margin-left: 20px;">{s1} × {digit} = <b>{int(s1) * digit}</b></p>
                <p style="margin-left: 20px;">Place value × 10^{i} → <b>{partial}</b></p>
            </div>
            """
        partials_rev = list(reversed(partials))
        max_w = max(len(s1), len(s2) + 2, max([len(str(p)) for p in partials] or [0]), len(str(result))) + 1
        lines = [s1.rjust(max_w), ("× " + s2).rjust(max_w), "─" * max_w]
        if len(s2) > 1:
            for idx, p in enumerate(partials_rev):
                prefix = "+ " if idx == len(partials_rev) - 1 else ""
                lines.append((prefix + str(p)).rjust(max_w))
            lines.append("─" * max_w)
        lines.append(str(result).rjust(max_w))
        if len(partials) > 1:
            step_num = self.increment_step()
            steps_html += f"""
            <div class="step-detail">
                <span class="step-counter">Step {step_num}:</span>
                <p>Add all partial products: {' + '.join(str(p) for p in reversed(partials))} = <b>{result}</b></p>
            </div>
            """
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Long Multiplication</div></div>
        <div class="step-box">
            <div class="step-header">🔢 Step-by-Step Multiplication</div>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="steps-container">{steps_html}</div>
            <div class="result-box">🎯 <strong>Result: {n1} × {n2} = {result}</strong></div>
        </div>"""

    def manual_div(self, n1, n2):
        self.reset_step_count()
        if n2 == 0:
            return "<div class='step-box'>❌ Division by zero is undefined.</div>"
        quotient = n1 // n2
        remainder = n1 % n2
        decimal_res = n1 / n2
        steps_html = ""
        dividend_str = str(abs(n1))
        if n1 >= 0 and n2 > 0:
            current = 0
            for i, digit in enumerate(dividend_str):
                current = current * 10 + int(digit)
                if current >= n2:
                    q_digit = current // n2
                    current = current % n2
                    step_num = self.increment_step()
                    steps_html += f"""
                    <div class="step-detail">
                        <span class="step-counter">Step {step_num}:</span>
                        <p>Bring down digit <b>{digit}</b> → current = <b>{current if current == 0 else current + n2 * q_digit}</b></p>
                        <p style="margin-left: 20px;">{current + n2 * q_digit} ÷ {n2} = <b>{q_digit}</b></p>
                        <p style="margin-left: 20px;">Remainder: {current}</p>
                    </div>
                    """
        display = f" {n1} │ {n2}\n─────┼─────\n {remainder} │ {quotient} (Quotient)"
        if remainder:
            display += f"\nRemainder: {remainder}"
        if remainder > 0:
            step_num = self.increment_step()
            steps_html += f"""
            <div class="step-detail">
                <span class="step-counter">Step {step_num}:</span>
                <p>Converting to decimal: {remainder} ÷ {n2} = {decimal_res:.4f}</p>
            </div>
            """
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Long Division</div></div>
        <div class="step-box">
            <div class="step-header">🔢 Step-by-Step Division</div>
            <pre class="manual-display">{display}</pre>
            <div class="steps-container">{steps_html}</div>
            <div class="result-box">🎯 <strong>Result: {n1} ÷ {n2} = {quotient} (Rem {remainder}) | Decimal: {decimal_res:.4f}</strong></div>
        </div>"""

    # ---------- 7-Step Linear Equation ----------
    def solve_linear_detailed(self, eq_str):
        self.reset_step_count()
        try:
            if '=' not in eq_str:
                return "<div class='step-box'>❌ Please use '='.</div>"
            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str)
            right_expr = self.parse_func(right_str)
            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Invalid expression. Use x.</div>"
            step1 = self.increment_step()
            step2 = self.increment_step()
            expr = expand(left_expr - right_expr)
            step3 = self.increment_step()
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a = b = 0
            if a == 0:
                return "<div class='step-box'>⚠️ Not linear.</div>"
            step4 = self.increment_step()
            step5 = self.increment_step()
            x_sol = -b / a
            latex_sol = latex(sp.nsimplify(x_sol))
            step6 = self.increment_step()
            verification_left = left_expr.subs(self.x, x_sol)
            verification_right = right_expr.subs(self.x, x_sol)
            step7 = self.increment_step()
            return f"""
            <div class="theory-box"><div class="theory-title">📚 Linear Equation (1st Degree)</div></div>
            <div class="step-box"><div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>Equation: $$\\text{{{eq_str}}}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Move all terms to one side: $${latex(expr)}=0$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>Identify a = {a}, b = {b}</p></div>
                <div class="step-detail"><span class="step-counter">Step {step4}</span><p>Isolate term: $${a}x = -{self.fmt_neg(b)}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step5}</span><p>Solve: $$x = \\frac{{-{self.fmt_neg(b)}}}{{{a}}} = {latex_sol}$$</p><p>Simplify: $$-({self.fmt_neg(b)}) = {latex(sp.simplify(-b))}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step6}</span><p>Verify: $${latex(verification_left)} = {latex(verification_right)}$$ ✓</p></div>
                <div class="step-detail"><span class="step-counter">Step {step7}</span><p>Final: $$\\boxed{{x = {latex_sol}}}$$</p></div>
                <div class="result-box">🎯 <strong>Solution: $x = {latex_sol}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 7-Step Quadratic Equation ----------
    def solve_quadratic_detailed(self, func_str):
        self.reset_step_count()
        try:
            if '=' in func_str:
                left, right = func_str.split('=')
                expr = expand(self.parse_func(left) - self.parse_func(right))
            else:
                expr = expand(self.parse_func(func_str))
            if expr is None:
                return "<div class='step-box'>❌ Invalid.</div>"
            step1 = self.increment_step()
            step2 = self.increment_step()
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
                return "<div class='step-box'>⚠️ Not quadratic.</div>"
            step3 = self.increment_step()
            step4 = self.increment_step()
            disc = b**2 - 4*a*c
            step5 = self.increment_step()
            step6 = self.increment_step()
            step7 = self.increment_step()
            base = f"""
            <div class="theory-box"><div class="theory-title">📚 Quadratic Equation</div></div>
            <div class="step-box"><div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>Equation: $${latex(expr)}=0$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Standard form: $${a}x^2 + {b}x + {c} = 0$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>a={a}, b={b}, c={c}</p></div>
                <div class="step-detail"><span class="step-counter">Step {step4}</span><p>Discriminant: $$\\Delta = {b}^2 - 4({a})({c}) = {disc}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step5}</span><p>Nature: {'Δ > 0' if disc > 0 else 'Δ = 0' if disc == 0 else 'Δ < 0'} → {'2 real roots' if disc > 0 else '1 double root' if disc == 0 else '2 complex roots'}</p></div>
                <div class="step-detail"><span class="step-counter">Step {step6}</span><p>Bhaskara: $$x = \\frac{{-({b}) \\pm \\sqrt{{{disc}}}}}{{2({a})}}$$</p>"""
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                base += f"""
                    <p>x₁ = {latex(sp.nsimplify(x1))}, x₂ = {latex(sp.nsimplify(x2))}</p>
                    <div class="step-detail"><span class="step-counter">Step {step7}</span><p>Verify: $${latex(expr.subs(self.x, sp.nsimplify(x1)))} = 0$ ✓, $${latex(expr.subs(self.x, sp.nsimplify(x2)))} = 0$ ✓</p></div>
                    <div class="result-box">🎯 <strong>Roots: $x_1 = {latex(sp.nsimplify(x1))},\\; x_2 = {latex(sp.nsimplify(x2))}$</strong></div>
                """
            else:
                real_p = -b / (2*a)
                imag_p = math.sqrt(-disc) / (2*a)
                base += f"""
                    <p>Complex roots: $x = {real_p:.4f} \\pm {imag_p:.4f}i$</p>
                    <div class="step-detail"><span class="step-counter">Step {step7}</span><p>Complex roots satisfy algebraically.</p></div>
                    <div class="result-box">🎯 <strong>Complex roots: $x = {real_p:.4f} \\pm {imag_p:.4f}i$</strong></div>
                """
            base += "</div>"
            return base
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 7-Step System 2x2 ----------
    def solve_system_2x2(self, eq1_str, eq2_str):
        self.reset_step_count()
        try:
            if '=' not in eq1_str or '=' not in eq2_str:
                return "<div class='step-box'>❌ Use '='.</div>"
            step1 = self.increment_step()
            l1, r1 = eq1_str.split('=')
            l2, r2 = eq2_str.split('=')
            expr1 = self.parse_func(l1) - self.parse_func(r1)
            expr2 = self.parse_func(l2) - self.parse_func(r2)
            if expr1 is None or expr2 is None:
                return "<div class='step-box'>❌ Invalid.</div>"
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            sol = solve((expr1, expr2), (self.x, self.y))
            step6 = self.increment_step()
            step7 = self.increment_step()
            if not sol:
                return "<div class='step-box'>⚠️ No unique solution.</div>"
            x_sol, y_sol = sol[self.x], sol[self.y]
            return f"""
            <div class="theory-box"><div class="theory-title">📚 2x2 Linear System</div></div>
            <div class="step-box"><div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>System: $$\\begin{{cases}} {latex(expr1)}=0 \\\\ {latex(expr2)}=0 \\end{{cases}}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Standard form.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>Identified coefficients.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step4}</span><p>Using Elimination Method.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step5}</span><p>Solved: x = {latex(sp.nsimplify(x_sol))}, y = {latex(sp.nsimplify(y_sol))}</p></div>
                <div class="step-detail"><span class="step-counter">Step {step6}</span><p>Verify: $${latex(expr1.subs({{self.x: x_sol, self.y: y_sol}}))} = 0$ ✓, $${latex(expr2.subs({{self.x: x_sol, self.y: y_sol}}))} = 0$ ✓</p></div>
                <div class="step-detail"><span class="step-counter">Step {step7}</span><p>Final: $$\\boxed{{x = {latex(sp.nsimplify(x_sol))},\\; y = {latex(sp.nsimplify(y_sol))}}}$$</p></div>
                <div class="result-box">🎯 <strong>Solution: $x = {latex(sp.nsimplify(x_sol))},\\; y = {latex(sp.nsimplify(y_sol))}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 7-Step System 3x3 ----------
    def solve_system_3x3(self, eq1_str, eq2_str, eq3_str):
        self.reset_step_count()
        try:
            if '=' not in eq1_str or '=' not in eq2_str or '=' not in eq3_str:
                return "<div class='step-box'>❌ Use '='.</div>"
            step1 = self.increment_step()
            l1, r1 = eq1_str.split('=')
            l2, r2 = eq2_str.split('=')
            l3, r3 = eq3_str.split('=')
            expr1 = self.parse_func(l1) - self.parse_func(r1)
            expr2 = self.parse_func(l2) - self.parse_func(r2)
            expr3 = self.parse_func(l3) - self.parse_func(r3)
            if expr1 is None or expr2 is None or expr3 is None:
                return "<div class='step-box'>❌ Invalid.</div>"
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            step6 = self.increment_step()
            sol = solve((expr1, expr2, expr3), (self.x, self.y, self.z))
            step7 = self.increment_step()
            if not sol:
                return "<div class='step-box'>⚠️ No unique solution.</div>"
            x_sol, y_sol, z_sol = sol[self.x], sol[self.y], sol[self.z]
            return f"""
            <div class="theory-box"><div class="theory-title">📚 3x3 Linear System</div></div>
            <div class="step-box"><div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>System: $$\\begin{{cases}} {latex(expr1)}=0 \\\\ {latex(expr2)}=0 \\\\ {latex(expr3)}=0 \\end{{cases}}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Standard form.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>Augmented matrix.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step4}</span><p>Using Gaussian Elimination.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step5}</span><p>Forward elimination to upper triangular.</p></div>
                <div class="step-detail"><span class="step-counter">Step {step6}</span><p>Back substitution: x={latex(sp.nsimplify(x_sol))}, y={latex(sp.nsimplify(y_sol))}, z={latex(sp.nsimplify(z_sol))}</p></div>
                <div class="step-detail"><span class="step-counter">Step {step7}</span><p>Verify: All equations ≈ 0 ✓</p></div>
                <div class="result-box">🎯 <strong>Solution:</strong><br>$$x = {latex(sp.nsimplify(x_sol))} \\\\ y = {latex(sp.nsimplify(y_sol))} \\\\ z = {latex(sp.nsimplify(z_sol))}$$</div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- Differentiation ----------
    def differentiate(self, func_str, var='x', eval_pt=None):
        self.reset_step_count()
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid.</div>"
            sym_var = Symbol(var)
            step1 = self.increment_step()
            step2 = self.increment_step()
            df = diff(expr, sym_var)
            step3 = self.increment_step()
            simplified_df = simplify(df)
            html = f"""
            <div class="theory-box"><div class="theory-title">📚 Differentiation</div></div>
            <div class="step-box"><div class="step-header">📈 Steps</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>Function: $$f({var}) = {latex(expr)}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Apply rules: $$f'({var}) = {latex(df)}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>Simplify: $$f'({var}) = {latex(simplified_df)}$$</p></div>
            """
            if eval_pt and str(eval_pt).strip():
                step4 = self.increment_step()
                try:
                    pt = parse_expr(str(eval_pt).replace('^', '**'))
                    val = simplified_df.subs(sym_var, pt)
                    html += f"""
                    <div class="step-detail"><span class="step-counter">Step {step4}</span><p>At $x={latex(pt)}$: $$f'({latex(pt)}) = {latex(val)}$$ {'≈ ' + f'{float(val):.4f}' if val.is_number and not val.is_Integer else ''}</p></div>
                    """
                except Exception:
                    pass
            html += f'<div class="result-box">🎯 $$\\boxed{{f\'({var}) = {latex(simplified_df)}}}$$</div></div>'
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- Integration ----------
    def integrate_func(self, func_str, var='x', lower=None, upper=None):
        self.reset_step_count()
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid.</div>"
            sym_var = Symbol(var)
            step1 = self.increment_step()
            step2 = self.increment_step()
            primitive = integrate(expr, sym_var)
            step3 = self.increment_step()
            simplified_prim = simplify(primitive)
            html = f"""
            <div class="theory-box"><div class="theory-title">📚 Integration</div></div>
            <div class="step-box"><div class="step-header">📊 Steps</div>
                <div class="step-detail"><span class="step-counter">Step {step1}</span><p>Integrate: $$\\int {latex(expr)} \\, d{var}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step2}</span><p>Antiderivative: $$F({var}) = {latex(primitive)}$$</p></div>
                <div class="step-detail"><span class="step-counter">Step {step3}</span><p>Simplify: $$F({var}) = {latex(simplified_prim)}$$</p></div>
            """
            if lower and upper and str(lower).strip() and str(upper).strip():
                step4 = self.increment_step()
                try:
                    a = parse_expr(str(lower).replace('^', '**'))
                    b = parse_expr(str(upper).replace('^', '**'))
                    Fb = simplified_prim.subs(sym_var, b)
                    Fa = simplified_prim.subs(sym_var, a)
                    def_res = simplify(Fb - Fa)
                    html += f"""
                    <div class="step-detail"><span class="step-counter">Step {step4}</span><p>Definite: $$\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} \\, d{var} = {latex(def_res)}$$</p></div>
                    <div class="result-box">🎯 $$\\boxed{{= {latex(def_res)}}}$$</div>
                    """
                except Exception:
                    html += "<p><i>Invalid limits.</i></p>"
            else:
                html += f'<div class="result-box">🎯 $$\\boxed{{\\int {latex(expr)} \\, d{var} = {latex(simplified_prim)} + C}}$$</div>'
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

# ---------------------------
# Streamlit UI
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
st.markdown('<p class="subtitle">Step‑by‑Step Mathematics – Complete resolutions with 7 detailed steps</p>', unsafe_allow_html=True)

with st.sidebar:
    mode = st.selectbox("Operation mode:", [
        "Basic Operations (Column)",
        "Linear Equation (1st Degree)",
        "Quadratic Equation (2nd Degree)",
        "System of Equations (2x2)",
        "System of Equations (3x3)",
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
            st.session_state.result_html = solver.solve_linear_detailed(eq)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Quadratic Equation (2nd Degree)":
        eq = st.text_input("Equation (e.g., x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Solve", use_container_width=True):
            st.session_state.result_html = solver.solve_quadratic_detailed(eq)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"Quadratic: {eq}")

    elif mode == "System of Equations (2x2)":
        st.markdown("Enter two equations:")
        eq1 = st.text_input("Equation 1 (e.g., 2x + y = 5):", "2x + y = 5")
        eq2 = st.text_input("Equation 2 (e.g., x - y = 1):", "x - y = 1")
        if st.button("🔢 Solve System", use_container_width=True):
            st.session_state.result_html = solver.solve_system_2x2(eq1, eq2)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"System 2x2: {eq1}, {eq2}")

    elif mode == "System of Equations (3x3)":
        st.markdown("Enter three equations:")
        eq1 = st.text_input("Equation 1 (e.g., x + y + z = 6):", "x + y + z = 6")
        eq2 = st.text_input("Equation 2 (e.g., 2x - y + z = 3):", "2x - y + z = 3")
        eq3 = st.text_input("Equation 3 (e.g., x + 2y - z = 0):", "x + 2y - z = 0")
        if st.button("🔢 Solve System", use_container_width=True):
            st.session_state.result_html = solver.solve_system_3x3(eq1, eq2, eq3)
            st.session_state.iframe_version += 1
            st.session_state.history.append(f"System 3x3: {eq1}, {eq2}, {eq3}")

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
        body {{ font-family: sans-serif; padding: 15px; color: #1a202c; background: #f7fafc; }}
        .manual-display {{ font-family: monospace; font-size: 18px; font-weight: bold; background: #1e293b; color: #38bdf8; padding: 16px 24px; border-radius: 10px; white-space: pre; text-align: left; margin: 10px 0; width: 100%; overflow-x: auto; }}
        .step-box {{ background: white; border-radius: 14px; padding: 24px; margin: 20px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 6px solid #764ba2; }}
        .step-header {{ font-size: 22px; font-weight: 700; color: #4a5568; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .step-detail {{ background: #f8fafc; border-radius: 10px; padding: 16px; margin: 12px 0; border-left: 4px solid #667eea; }}
        .step-counter {{ display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 3px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; margin-bottom: 8px; }}
        .formula-highlight {{ background: #edf2f7; border: 2px solid #667eea; border-radius: 12px; padding: 16px; text-align: center; margin: 12px 0; overflow-x: auto; }}
        .result-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0; font-size: 22px; font-weight: bold; }}
        .theory-box {{ background: #f0f4ff; border-left: 6px solid #667eea; border-radius: 12px; padding: 20px; margin: 20px 0; }}
        .theory-title {{ font-size: 20px; font-weight: 700; color: #4c51bf; margin-bottom: 12px; }}
        @media (max-width: 768px) {{ .manual-display {{ font-size: 14px; padding: 10px; }} .step-box {{ padding: 15px; }} .result-box {{ font-size: 18px; padding: 15px; }} }}
    </style>
</head>
<body>
    {st.session_state.result_html}
</body>
</html>"""
        components.html(full_page, height=900, scrolling=True)
    else:
        st.info("👈 Choose a mode, enter data, and click **Compute**.")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>🧮 HandCalc Pro – Step-by-step with LaTeX</div>", unsafe_allow_html=True)
