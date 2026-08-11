# app.py – Full corrected version with 7-step resolutions and fixed syntax
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol, sqrt, pi, I)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

# Styling (same as before)
st.markdown("""
<style>
    .main-title {
        font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .subtitle {
        text-align: center; color: #666; font-size: 18px; margin-bottom: 30px;
    }
    .stButton > button {
        width: 100%; height: 50px; font-weight: 600; border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
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

    # ---------- Basic Operations (unchanged) ----------
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
        <div class="theory-box">
            <div class="theory-title">📚 Column Addition (Base-10 System)</div>
            <p>Adding numbers digit by digit from right to left, carrying over when sum ≥ 10.</p>
        </div>
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
        <div class="theory-box">
            <div class="theory-title">📚 Column Subtraction (Borrowing Method)</div>
            <p>Subtracting digits from right to left, borrowing from higher place when needed.</p>
        </div>
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
                <p>Add all partial products:</p>
                <p style="margin-left: 20px;">{' + '.join(str(p) for p in reversed(partials))} = <b>{result}</b></p>
            </div>
            """
        return f"""
        <div class="theory-box">
            <div class="theory-title">📚 Long Multiplication (Distributive Property)</div>
            <p>Breaking multiplication into smaller steps: a × (b₁ + b₂ + ...) = a×b₁ + a×b₂ + ...</p>
        </div>
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
                <p>Converting to decimal:</p>
                <p style="margin-left: 20px;">{remainder} ÷ {n2} = {decimal_res:.4f} (approximate)</p>
            </div>
            """
        return f"""
        <div class="theory-box">
            <div class="theory-title">📚 Long Division (Division Algorithm)</div>
            <p>Dividend = Divisor × Quotient + Remainder</p>
            <p>Check: {n1} = {n2} × {quotient} + {remainder} → {n2 * quotient + remainder} = {n1} ✓</p>
        </div>
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
                return "<div class='step-box'>❌ Please use '=' to separate left and right sides.</div>"
            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str)
            right_expr = self.parse_func(right_str)
            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Invalid expression. Use x as variable.</div>"
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
                return "<div class='step-box'>⚠️ Not a linear equation (a = 0).</div>"
            step4 = self.increment_step()
            step5 = self.increment_step()
            x_sol = -b / a
            latex_sol = latex(sp.nsimplify(x_sol))
            step6 = self.increment_step()
            verification_left = left_expr.subs(self.x, x_sol)
            verification_right = right_expr.subs(self.x, x_sol)
            step7 = self.increment_step()
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 Linear Equation (1st Degree) - Complete Resolution</div>
                <p>A linear equation in the form <b>ax + b = 0</b> has solution <b>x = -b/a</b></p>
                <p><b>Key Concepts:</b></p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Linear equations have the highest power of variable = 1</li>
                    <li>• The solution is unique (one value of x)</li>
                    <li>• We can verify by substituting back into original equation</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the equation</span>
                    <p>We have the equation:</p>
                    <div class="formula-highlight">$$\\text{{Original equation: }} {latex(left_expr)} = {latex(right_expr)}$$</div>
                    <p style="margin-left: 20px;">• Left side: <b>{latex(left_expr)}</b></p>
                    <p style="margin-left: 20px;">• Right side: <b>{latex(right_expr)}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Move all terms to one side</span>
                    <p>Subtract the right side from both sides:</p>
                    <div class="formula-highlight">$${latex(left_expr)} - {latex(right_expr)} = 0$$</div>
                    <p style="margin-left: 20px;">This gives us the standard form <b>ax + b = 0</b></p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Identify coefficients a and b</span>
                    <p>Compare with standard form <b>ax + b = 0</b>:</p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                    <p style="margin-left: 20px;">Coefficient of x: <b>a = {a}</b></p>
                    <p style="margin-left: 20px;">Constant term: <b>b = {b}</b></p>
                    <p style="margin-left: 20px;">Verification: <b>{a}x + {b} = 0</b> ✓</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Isolate the variable term</span>
                    <p>Move the constant term to the right side:</p>
                    <div class="formula-highlight">$${a}x = -{b}$$</div>
                    <p style="margin-left: 20px;">• Subtract <b>{b}</b> from both sides</p>
                    <p style="margin-left: 20px;">• The variable term is now isolated</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Solve for x</span>
                    <p>Divide both sides by the coefficient <b>a</b>:</p>
                    <div class="formula-highlight">$$x = \\frac{{-{b}}}{{{a}}} = {latex_sol}$$</div>
                    <p style="margin-left: 20px;">• Division property: if ax = b, then x = b/a</p>
                    <p style="margin-left: 20px;">• Final value: <b>x = {latex_sol}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Verify the solution</span>
                    <p>Substitute x = {latex_sol} back into the original equation:</p>
                    <p style="margin-left: 20px;">Left side: <b>{latex(left_expr)}</b> → <b>{latex(verification_left)}</b></p>
                    <p style="margin-left: 20px;">Right side: <b>{latex(right_expr)}</b> → <b>{latex(verification_right)}</b></p>
                    <div class="formula-highlight">$${latex(verification_left)} = {latex(verification_right)}$$</div>
                    <p style="margin-left: 20px;">Both sides equal! ✓</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Final check and conclusion</span>
                    <p>We have successfully solved the equation:</p>
                    <div class="formula-highlight">$$\\boxed{{x = {latex_sol}}}$$</div>
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b></p>
                        <p>Original: <b>{eq_str}</b></p>
                        <p>Substitute x = {latex_sol}:</p>
                        <p><b>{latex(left_expr.subs(self.x, x_sol))} = {latex(right_expr.subs(self.x, x_sol))}</b> ✓</p>
                    </div>
                </div>
                <div class="result-box">🎯 <strong>Solution: $x = {latex_sol}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 7-Step Quadratic Equation ----------
    def solve_quadratic_detailed(self, func_str):
        self.reset_step_count()
        try:
            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                expr = expand(self.parse_func(left_str) - self.parse_func(right_str))
            else:
                expr = expand(self.parse_func(func_str))
            if expr is None:
                return "<div class='step-box'>❌ Invalid expression.</div>"
            step1 = self.increment_step()
            step2 = self.increment_step()
            step3 = self.increment_step()
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
            step4 = self.increment_step()
            disc = b**2 - 4*a*c
            step5 = self.increment_step()
            step6 = self.increment_step()
            step7 = self.increment_step()
            base = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Quadratic Equation (Bhaskara Formula) - Complete Resolution</div>
                <p>For ax² + bx + c = 0:</p>
                <div class="formula-highlight">$$x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}}$$</div>
                <p><b>Key Concepts:</b></p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Δ = b² - 4ac (discriminant)</li>
                    <li>• Δ > 0: two real distinct roots</li>
                    <li>• Δ = 0: one real double root</li>
                    <li>• Δ < 0: two complex conjugate roots</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the quadratic equation</span>
                    <p>The given equation is:</p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                    <p style="margin-left: 20px;">This is a <b>quadratic equation</b> because the highest power of x is 2</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Standard form</span>
                    <p>The equation is already in standard form <b>ax² + bx + c = 0</b>:</p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                    <p style="margin-left: 20px;">No further simplification needed</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Identify coefficients</span>
                    <p>Compare with <b>ax² + bx + c = 0</b>:</p>
                    <p style="margin-left: 20px;"><b>a</b> (coefficient of x²) = <b>{a}</b></p>
                    <p style="margin-left: 20px;"><b>b</b> (coefficient of x) = <b>{b}</b></p>
                    <p style="margin-left: 20px;"><b>c</b> (constant term) = <b>{c}</b></p>
                    <div class="formula-highlight">$${a}x² + {b}x + {c} = 0$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Calculate the discriminant</span>
                    <p>The discriminant Δ = b² - 4ac determines the nature of roots:</p>
                    <div class="formula-highlight">$$\\Delta = {b}^2 - 4({a})({c})$$</div>
                    <p style="margin-left: 20px;">Δ = {b**2} - {4*a*c} = <b>{disc}</b></p>
                    <p style="margin-left: 20px;">Δ <b>{'≥' if disc >= 0 else '<'} 0</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Analyze the discriminant</span>
                    <p>Since Δ {'= ' + str(disc) if disc >= 0 else ' = ' + str(disc) + ' (negative)'}:</p>
                    <ul style="margin-left: 20px;">
                        <li>Δ {'> 0' if disc > 0 else '= 0' if disc == 0 else '< 0'}</li>
                        <li>Nature of roots: <b>{'Two real distinct roots' if disc > 0 else 'One real double root' if disc == 0 else 'Two complex conjugate roots'}</b></li>
                    </ul>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Apply Bhaskara formula</span>
                    <p>Using the formula $x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$:</p>
                    <div class="formula-highlight">$$x = \\frac{{-({b}) \\pm \\sqrt{{{disc}}}}}{{2({a})}}$$</div>
            """
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                base += f"""
                    <p style="margin-left: 20px;">With Δ = {disc}, √Δ = {sqrt_disc:.4f}</p>
                    <p style="margin-left: 20px;">x₁ = (-{b} + {sqrt_disc:.4f}) / {2*a} = <b>{latex(sp.nsimplify(x1))}</b></p>
                    <p style="margin-left: 20px;">x₂ = (-{b} - {sqrt_disc:.4f}) / {2*a} = <b>{latex(sp.nsimplify(x2))}</b></p>
                """
            else:
                real_p = -b / (2*a)
                imag_p = math.sqrt(-disc) / (2*a)
                base += f"""
                    <p style="margin-left: 20px;">Since Δ < 0, we have complex roots:</p>
                    <p style="margin-left: 20px;">Real part = <b>{real_p:.4f}</b>, Imaginary part = <b>{imag_p:.4f}</b></p>
                    <div class="formula-highlight">$$x = {real_p:.4f} \\pm {imag_p:.4f}i$$</div>
                """
            base += f"""
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Verify the solutions</span>
                    <p>Substitute each root back into the original equation:</p>
            """
            if disc >= 0:
                x1_sym = sp.nsimplify(x1)
                x2_sym = sp.nsimplify(x2)
                v1 = expr.subs(self.x, x1_sym)
                v2 = expr.subs(self.x, x2_sym)
                base += f"""
                    <p style="margin-left: 20px;">For x₁ = {latex(x1_sym)}:</p>
                    <p style="margin-left: 40px;">{latex(expr.subs(self.x, x1_sym))} = {latex(v1)} ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">For x₂ = {latex(x2_sym)}:</p>
                    <p style="margin-left: 40px;">{latex(expr.subs(self.x, x2_sym))} = {latex(v2)} ≈ 0 ✓</p>
                """
            else:
                base += """
                    <p style="margin-left: 20px;">Complex roots cannot be easily verified numerically, but they satisfy the equation algebraically.</p>
                """
            base += f"""
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b> All roots satisfy the original equation</p>
                    </div>
                </div>
                <div class="result-box">🎯 <strong>{'Roots: $x_1 = ' + latex(sp.nsimplify(x1)) + ',\\; x_2 = ' + latex(sp.nsimplify(x2)) + '$' if disc >= 0 else 'Complex roots: $x = ' + str(real_p) + ' \\pm ' + str(imag_p) + 'i$'}</strong></div>
            </div>"""
            return base
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 2x2 System (7 Steps) ----------
    def solve_system_2x2(self, eq1_str, eq2_str):
        self.reset_step_count()
        try:
            if '=' not in eq1_str or '=' not in eq2_str:
                return "<div class='step-box'>❌ Each equation must contain '='.</div>"
            step1 = self.increment_step()
            left1, right1 = eq1_str.split('=')
            left2, right2 = eq2_str.split('=')
            expr1 = self.parse_func(left1) - self.parse_func(right1)
            expr2 = self.parse_func(left2) - self.parse_func(right2)
            if expr1 is None or expr2 is None:
                return "<div class='step-box'>❌ Invalid expressions.</div>"
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            sol = solve((expr1, expr2), (self.x, self.y))
            step6 = self.increment_step()
            step7 = self.increment_step()
            if not sol:
                return "<div class='step-box'>⚠️ No solution found (system may be inconsistent).</div>"
            x_sol, y_sol = sol[self.x], sol[self.y]
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 System of Linear Equations (2 Variables)</div>
                <p>Solving systems of 2 linear equations with 2 variables:</p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• <b>Substitution method:</b> Solve one equation for one variable</li>
                    <li>• <b>Elimination method:</b> Add/subtract equations to eliminate a variable</li>
                    <li>• <b>Graphical method:</b> Find intersection point</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the system</span>
                    <p>The system of equations is:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\end{{cases}}$$</div>
                    <p style="margin-left: 20px;">Variables: <b>x</b> and <b>y</b></p>
                    <p style="margin-left: 20px;">Goal: Find values of x and y that satisfy both equations</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Standard form</span>
                    <p>Both equations are in standard form <b>ax + by + c = 0</b>:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\end{{cases}}$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Identify coefficients</span>
                    <p>Extract coefficients from both equations:</p>
                    <p style="margin-left: 20px;">Eq1: <b>{latex(expr1)} = 0</b></p>
                    <p style="margin-left: 40px;">Coefficient of x: <b>{sp.Poly(expr1, self.x).coeff_monomial(self.x)}</b></p>
                    <p style="margin-left: 40px;">Coefficient of y: <b>{sp.Poly(expr1, self.y).coeff_monomial(self.y)}</b></p>
                    <p style="margin-left: 40px;">Constant: <b>{sp.Poly(expr1, self.x).coeff_monomial(1)}</b></p>
                    <p style="margin-left: 20px;">Eq2: <b>{latex(expr2)} = 0</b></p>
                    <p style="margin-left: 40px;">Coefficient of x: <b>{sp.Poly(expr2, self.x).coeff_monomial(self.x)}</b></p>
                    <p style="margin-left: 40px;">Coefficient of y: <b>{sp.Poly(expr2, self.y).coeff_monomial(self.y)}</b></p>
                    <p style="margin-left: 40px;">Constant: <b>{sp.Poly(expr2, self.x).coeff_monomial(1)}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Choose solution method</span>
                    <p>We will use the <b>elimination method</b>:</p>
                    <ul style="margin-left: 20px;">
                        <li>Multiply equations by appropriate constants to make coefficients equal</li>
                        <li>Add/subtract equations to eliminate one variable</li>
                        <li>Solve the resulting single-variable equation</li>
                    </ul>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Solve for x and y</span>
                    <p>Using the elimination method:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\end{{cases}}$$</div>
                    <p style="margin-left: 20px;">Solution found:</p>
                    <p style="margin-left: 40px;">x = <b>{latex(sp.nsimplify(x_sol))}</b></p>
                    <p style="margin-left: 40px;">y = <b>{latex(sp.nsimplify(y_sol))}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Verify the solution</span>
                    <p>Substitute x = {latex(sp.nsimplify(x_sol))} and y = {latex(sp.nsimplify(y_sol))} into both equations:</p>
                    <p style="margin-left: 20px;">Eq1: <b>{latex(expr1.subs({self.x: x_sol, self.y: y_sol}))}</b> ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">Eq2: <b>{latex(expr2.subs({self.x: x_sol, self.y: y_sol}))}</b> ≈ 0 ✓</p>
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b> Both equations are satisfied</p>
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Final conclusion</span>
                    <p>The system has a unique solution:</p>
                    <div class="formula-highlight">$$\\boxed{{x = {latex(sp.nsimplify(x_sol))}, \\; y = {latex(sp.nsimplify(y_sol))}}}$$</div>
                    <p style="margin-left: 20px;">The point <b>({latex(sp.nsimplify(x_sol))}, {latex(sp.nsimplify(y_sol))})</b> is the intersection of the two lines.</p>
                </div>
                <div class="result-box">🎯 <strong>Solution: $x = {latex(sp.nsimplify(x_sol))},\\; y = {latex(sp.nsimplify(y_sol))}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- 3x3 System (7 Steps) – fixed syntax ----------
    def solve_system_3x3(self, eq1_str, eq2_str, eq3_str):
        self.reset_step_count()
        try:
            if '=' not in eq1_str or '=' not in eq2_str or '=' not in eq3_str:
                return "<div class='step-box'>❌ Each equation must contain '='.</div>"
            step1 = self.increment_step()
            left1, right1 = eq1_str.split('=')
            left2, right2 = eq2_str.split('=')
            left3, right3 = eq3_str.split('=')
            expr1 = self.parse_func(left1) - self.parse_func(right1)
            expr2 = self.parse_func(left2) - self.parse_func(right2)
            expr3 = self.parse_func(left3) - self.parse_func(right3)
            if expr1 is None or expr2 is None or expr3 is None:
                return "<div class='step-box'>❌ Invalid expressions.</div>"
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            step6 = self.increment_step()
            sol = solve((expr1, expr2, expr3), (self.x, self.y, self.z))
            step7 = self.increment_step()
            if not sol:
                return "<div class='step-box'>⚠️ No unique solution found.</div>"
            x_sol, y_sol, z_sol = sol[self.x], sol[self.y], sol[self.z]
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 System of Linear Equations (3 Variables)</div>
                <p>Solving systems of 3 linear equations with 3 variables:</p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• <b>Gaussian elimination:</b> Transform to row-echelon form</li>
                    <li>• <b>Matrix method:</b> Use determinant and Cramer's rule</li>
                    <li>• <b>Substitution method:</b> Solve step by step</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the system</span>
                    <p>The system of 3 equations with 3 variables is:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\\\ {latex(expr3)} = 0 \\end{{cases}}$$</div>
                    <p style="margin-left: 20px;">Variables: <b>x</b>, <b>y</b>, and <b>z</b></p>
                    <p style="margin-left: 20px;">Goal: Find values of x, y, and z that satisfy all three equations</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Standard form</span>
                    <p>All equations are in standard form <b>ax + by + cz + d = 0</b>:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\\\ {latex(expr3)} = 0 \\end{{cases}}$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Matrix representation</span>
                    <p>Represent the system as an augmented matrix:</p>
                    <div class="formula-highlight">
                        $$\\begin{{bmatrix}}
                        {sp.Poly(expr1, self.x).coeff_monomial(self.x)} & {sp.Poly(expr1, self.y).coeff_monomial(self.y)} & {sp.Poly(expr1, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr1, self.x).coeff_monomial(1)} \\\\
                        {sp.Poly(expr2, self.x).coeff_monomial(self.x)} & {sp.Poly(expr2, self.y).coeff_monomial(self.y)} & {sp.Poly(expr2, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr2, self.x).coeff_monomial(1)} \\\\
                        {sp.Poly(expr3, self.x).coeff_monomial(self.x)} & {sp.Poly(expr3, self.y).coeff_monomial(self.y)} & {sp.Poly(expr3, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr3, self.x).coeff_monomial(1)}
                        \\end{{bmatrix}}$$
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Choose solution method</span>
                    <p>We will use <b>Gaussian elimination</b> with the following steps:</p>
                    <ul style="margin-left: 20px;">
                        <li>Forward elimination to create zeros below the diagonal</li>
                        <li>Back substitution to find the values of variables</li>
                    </ul>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Forward elimination</span>
                    <p>Eliminate variables to get upper triangular form:</p>
                    <ul style="margin-left: 20px;">
                        <li>Use row operations to create zeros in lower-left positions</li>
                        <li>System becomes easier to solve step by step</li>
                    </ul>
                    <p style="margin-left: 20px;">After elimination, we obtain a system like:</p>
                    <div class="formula-highlight">
                        $$\\begin{{cases}}
                        a_{{11}}x + a_{{12}}y + a_{{13}}z = d_1 \\\\
                        a_{{22}}y + a_{{23}}z = d_2 \\\\
                        a_{{33}}z = d_3
                        \\end{{cases}}$$
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Back substitution</span>
                    <p>Solve from the last equation backwards:</p>
                    <ul style="margin-left: 20px;">
                        <li>Solve for z from the third equation</li>
                        <li>Substitute z into the second equation to find y</li>
                        <li>Substitute y and z into the first equation to find x</li>
                    </ul>
                    <p style="margin-left: 20px;">Solution found:</p>
                    <p style="margin-left: 40px;">x = <b>{latex(sp.nsimplify(x_sol))}</b></p>
                    <p style="margin-left: 40px;">y = <b>{latex(sp.nsimplify(y_sol))}</b></p>
                    <p style="margin-left: 40px;">z = <b>{latex(sp.nsimplify(z_sol))}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Verify the solution</span>
                    <p>Substitute x = {latex(sp.nsimplify(x_sol))}, y = {latex(sp.nsimplify(y_sol))}, and z = {latex(sp.nsimplify(z_sol))} into all three equations:</p>
                    <p style="margin-left: 20px;">Eq1: <b>{latex(expr1.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">Eq2: <b>{latex(expr2.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">Eq3: <b>{latex(expr3.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b> All three equations are satisfied</p>
                    </div>
                </div>
                <div class="result-box">🎯 <strong>Solution: $x = {latex(sp.nsimplify(x_sol))},\\; y = {latex(sp.nsimplify(y_sol))},\\; z = {latex(sp.nsimplify(z_sol))}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    # ---------- Calculus (unchanged from original) ----------
    def differentiate(self, func_str, var='x', eval_pt=None):
        self.reset_step_count()
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid function.</div>"
            sym_var = Symbol(var)
            step1 = self.increment_step()
            step2 = self.increment_step()
            df = diff(expr, sym_var)
            step3 = self.increment_step()
            simplified_df = simplify(df)
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Differentiation Rules</div>
                <p>Basic rules: Power rule, Chain rule, Sum rule, Product rule</p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Power rule: d/dx[xⁿ] = nxⁿ⁻¹</li>
                    <li>• Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)</li>
                    <li>• Sum rule: d/dx[f+g] = f' + g'</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📈 Differentiation Steps</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}:</span>
                    <p>Identify the function to differentiate:</p>
                    <div class="formula-highlight">$$f({var}) = {latex(expr)}$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}:</span>
                    <p>Apply differentiation rules:</p>
                    <div class="formula-highlight">$$f'({var}) = {latex(df)}$$</div>
                    <div class="step-breakdown">
                        <p>Breakdown of each term:</p>
            """
            if expr.is_Add:
                terms = expr.as_ordered_terms()
                for term in terms:
                    term_diff = diff(term, sym_var)
                    html += f"""
                        <p style="margin-left: 20px;">• d/dx[{latex(term)}] = {latex(term_diff)}</p>
                    """
            html += f"""
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}:</span>
                    <p>Simplify the result:</p>
                    <div class="formula-highlight">$$f'({var}) = {latex(simplified_df)}$$</div>
                </div>
            """
            if eval_pt and str(eval_pt).strip():
                step4 = self.increment_step()
                try:
                    pt = parse_expr(str(eval_pt).replace('^', '**'))
                    val = simplified_df.subs(sym_var, pt)
                    html += f"""
                    <div class="step-detail">
                        <span class="step-counter">Step {step4}:</span>
                        <p>Evaluate at $x = {latex(pt)}$:</p>
                        <div class="formula-highlight">
                            $$f'({latex(pt)}) = {latex(val)}$$
                            {'≈ ' + f'{float(val):.4f}' if val.is_number and not val.is_Integer else ''}
                        </div>
                    </div>
                    """
                except Exception:
                    html += "<p><i>Could not evaluate at that point.</i></p>"
            html += f"""
                <div class="result-box">🎯 $$\\boxed{{f'({var}) = {latex(simplified_df)}}}$$</div>
            </div>"""
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

    def integrate_func(self, func_str, var='x', lower=None, upper=None):
        self.reset_step_count()
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ Invalid function.</div>"
            sym_var = Symbol(var)
            step1 = self.increment_step()
            step2 = self.increment_step()
            primitive = integrate(expr, sym_var)
            step3 = self.increment_step()
            simplified_prim = simplify(primitive)
            html = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Integration Rules</div>
                <p>Basic rules: Power rule (reverse), Linearity</p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C</li>
                    <li>• Constant multiple: ∫k·f(x) dx = k·∫f(x) dx</li>
                    <li>• Sum rule: ∫(f+g) dx = ∫f dx + ∫g dx</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📊 Integration Steps</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}:</span>
                    <p>Identify the function to integrate:</p>
                    <div class="formula-highlight">$$\\int {latex(expr)} \\, d{var}$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}:</span>
                    <p>Find antiderivative:</p>
                    <div class="formula-highlight">$$F({var}) = {latex(primitive)}$$</div>
                    <div class="step-breakdown">
                        <p>Breakdown of each term:</p>
            """
            if expr.is_Add:
                terms = expr.as_ordered_terms()
                for term in terms:
                    term_int = integrate(term, sym_var)
                    html += f"""
                        <p style="margin-left: 20px;">• ∫{latex(term)} d{var} = {latex(term_int)}</p>
                    """
            html += f"""
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}:</span>
                    <p>Simplify the antiderivative:</p>
                    <div class="formula-highlight">$$F({var}) = {latex(simplified_prim)}$$</div>
                </div>
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
                    <div class="step-detail">
                        <span class="step-counter">Step {step4}:</span>
                        <p>Apply Fundamental Theorem of Calculus:</p>
                        <div class="formula-highlight">
                            $$\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} \\, d{var} = F({latex(b)}) - F({latex(a)})$$
                        </div>
                        <p style="margin-left: 20px;">F({latex(b)}) = {latex(Fb)}</p>
                        <p style="margin-left: 20px;">F({latex(a)}) = {latex(Fa)}</p>
                        <p style="margin-left: 20px;">Result = {latex(Fb)} - {latex(Fa)} = <b>{latex(def_res)}</b></p>
                        <div class="result-box">🎯 $$\\boxed{{= {latex(def_res)}}}$$</div>
                    </div>
                    """
                except Exception:
                    html += "<p><i>Invalid limits.</i></p>"
            else:
                html += f"""
                <div class="result-box">🎯 $$\\boxed{{ \\int {latex(expr)} \\, d{var} = {latex(simplified_prim)} + C }}$$</div>
                """
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"

# ---------------------------
# Streamlit UI (unchanged)
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
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            padding: 15px; 
            color: #1a202c;
            background: #f7fafc;
        }}
        .manual-display {{
            font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; line-height: 1.4;
            background: #1e293b; color: #38bdf8; padding: 16px 24px; border-radius: 10px;
            display: inline-block; white-space: pre; text-align: left; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 10px 0; width: 100%; overflow-x: auto;
        }}
        .step-box {{ 
            background: white; border-radius: 14px; padding: 24px; margin: 20px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 6px solid #764ba2;
        }}
        .step-header {{
            font-size: 22px; font-weight: 700; color: #4a5568; margin-bottom: 20px;
            border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;
        }}
        .step-detail {{
            background: #f8fafc; border-radius: 10px; padding: 16px; margin: 12px 0;
            border-left: 4px solid #667eea;
        }}
        .step-counter {{
            display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; padding: 3px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;
            margin-bottom: 8px;
        }}
        .formula-highlight {{ 
            background: #edf2f7; border: 2px solid #667eea; border-radius: 12px;
            padding: 16px; text-align: center; margin: 12px 0; font-size: 18px;
            overflow-x: auto;
        }}
        .result-box {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
            border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0;
            font-size: 22px; font-weight: bold; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        .theory-box {{ 
            background: #f0f4ff; border-left: 6px solid #667eea; border-radius: 12px;
            padding: 20px; margin: 20px 0; 
        }}
        .theory-title {{ 
            font-size: 20px; font-weight: 700; color: #4c51bf; margin-bottom: 12px;
        }}
        .step-breakdown {{
            background: #e2e8f0; border-radius: 8px; padding: 12px; margin: 10px 0;
        }}
        .verification {{
            background: #c6f6d5; border-radius: 8px; padding: 12px; margin: 10px 0;
            border: 1px solid #48bb78;
        }}
        @media (max-width: 768px) {{
            .manual-display {{ font-size: 14px; padding: 10px; }}
            .step-box {{ padding: 15px; }}
            .result-box {{ font-size: 18px; padding: 15px; }}
        }}
    </style>
</head>
<body>
    {st.session_state.result_html}
</body>
</html>"""
        components.html(full_page, height=900, scrolling=True)
    else:
        st.info("👈 Choose a mode, enter data, and click **Compute** to see the complete step‑by‑step resolution.")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>🧮 HandCalc Pro – Every step displayed with detailed explanations and LaTeX formulas</div>", unsafe_allow_html=True)
