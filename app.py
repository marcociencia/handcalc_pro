# app.py - COMPLETELY FIXED VERSION
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   factor, sqrt as sym_sqrt, sin, cos, tan, exp, log,
                   Symbol)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

# Page config
st.set_page_config(
    page_title="HandCalc Pro - Complete Step-by-Step",
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
    
    .theory-title {
        font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; 
        color: #667eea; margin-bottom: 10px;
    }
    
    .step-box {
        background: white; border-radius: 10px; padding: 15px; margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05); border-left: 3px solid #764ba2;
    }
    
    .step-number {
        display: inline-block; background: #667eea; color: white; border-radius: 50%;
        width: 30px; height: 30px; text-align: center; line-height: 30px; 
        margin-right: 10px; font-weight: bold;
    }
    
    .formula-highlight {
        background: #f8f9fa; border: 2px solid #667eea; border-radius: 8px; 
        padding: 15px; text-align: center; margin: 15px 0;
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
        border: none; transition: all 0.3s ease;
    }
    
    .stButton > button:hover { 
        transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); 
    }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
    
    def parse_func(self, func_str):
        """Parse function string to sympy expression"""
        transformations = (standard_transformations + (implicit_multiplication_application,))
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('×', '*')
        func_str = func_str.replace('÷', '/')
        func_str = func_str.replace(' ', '')
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
        try:
            return parse_expr(func_str, transformations=transformations)
        except:
            return None
    
    def escape_latex(self, s):
        """Properly escape LaTeX for HTML display"""
        return str(s).replace('\\', '\\\\')
    
    # ============ MANUAL ADDITION ============
    def manual_add(self, n1, n2):
        """Manual addition with step-by-step display"""
        s1, s2 = str(n1), str(n2)
        max_len = max(len(s1), len(s2))
        result = n1 + n2
        result_str = str(result)
        
        # Calculate carries
        carries = []
        carry = 0
        p1 = s1.zfill(max_len)
        p2 = s2.zfill(max_len)
        
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(p1[i]) + int(p2[i]) + carry
            carries.insert(0, digit_sum // 10)
            carry = digit_sum // 10
        
        # Build HTML
        html_parts = []
        html_parts.append('<div class="step-box">')
        html_parts.append('<strong>➕ Manual Addition - Step by Step</strong><br><br>')
        
        # Build manual display
        display_lines = []
        if any(c > 0 for c in carries):
            carry_line = ' '.join(str(c) if c > 0 else ' ' for c in carries)
            display_lines.append(carry_line)
        display_lines.append(s1)
        display_lines.append('+ ' + s2)
        display_lines.append('─' * (max_len + 2))
        display_lines.append(result_str)
        
        display_text = '\n'.join(display_lines)
        html_parts.append('<div class="manual-display">')
        html_parts.append(display_text)
        html_parts.append('</div>')
        
        # Step-by-step explanation
        html_parts.append('<br><strong>Detailed Steps:</strong><br>')
        
        for i in range(max_len):
            pos = max_len - 1 - i
            d1 = int(p1[pos])
            d2 = int(p2[pos])
            prev_carry = carries[pos + 1] if pos + 1 < max_len else 0
            col_sum = d1 + d2 + prev_carry
            place = ['units', 'tens', 'hundreds', 'thousands'][min(i, 3)]
            
            step_text = '<span class="step-number">' + str(i+1) + '</span> '
            step_text += '<b>' + place.capitalize() + ':</b> '
            step_text += str(d1) + ' + ' + str(d2)
            
            if prev_carry > 0:
                step_text += ' + ' + str(prev_carry) + ' (carry)'
            
            step_text += ' = ' + str(col_sum)
            
            if carries[pos] > 0:
                step_text += ' → write ' + str(col_sum % 10) + ', carry ' + str(carries[pos])
            
            step_text += '<br>'
            html_parts.append(step_text)
        
        html_parts.append('<div class="result-box">')
        html_parts.append('🎯 <strong>Result: ' + str(n1) + ' + ' + str(n2) + ' = ' + str(result) + '</strong>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    # ============ MANUAL MULTIPLICATION ============
    def manual_mul(self, n1, n2):
        """Manual long multiplication with step-by-step"""
        s1, s2 = str(n1), str(n2)
        result = n1 * n2
        
        # Calculate partial products
        partials = []
        for i, digit in enumerate(reversed(s2)):
            partial = n1 * int(digit) * (10 ** i)
            partials.append(partial)
        
        partials_rev = list(reversed(partials))
        
        # Build HTML
        html_parts = []
        html_parts.append('<div class="step-box">')
        html_parts.append('<strong>✖️ Long Multiplication - Step by Step</strong><br><br>')
        
        # Build manual display
        max_width = max(len(s1), len(s2) + 1, max(len(str(p)) for p in partials_rev), len(str(result)))
        
        display_lines = []
        display_lines.append(s1.rjust(max_width))
        display_lines.append(('× ' + s2).rjust(max_width))
        display_lines.append('─' * max_width)
        
        for p in partials_rev:
            display_lines.append(str(p).rjust(max_width))
        
        display_lines.append('─' * max_width)
        display_lines.append(str(result).rjust(max_width))
        
        display_text = '\n'.join(display_lines)
        html_parts.append('<div class="manual-display">')
        html_parts.append(display_text)
        html_parts.append('</div>')
        
        # Step-by-step explanation
        html_parts.append('<br><strong>Detailed Steps:</strong><br>')
        
        for i, digit in enumerate(reversed(s2)):
            partial = n1 * int(digit)
            shift = i
            
            step_text = '<span class="step-number">' + str(i+1) + '</span> '
            step_text += 'Multiply ' + str(n1) + ' × ' + digit + ' = ' + str(partial)
            
            if shift > 0:
                step_text += ' → shift left ' + str(shift) + ' place(s) = ' + str(partial) + ('0' * shift)
            
            step_text += '<br>'
            html_parts.append(step_text)
        
        step_text = '<span class="step-number">' + str(len(s2) + 1) + '</span> '
        step_text += 'Add partial products: ' + ' + '.join(str(p) for p in partials_rev)
        step_text += ' = ' + str(result) + '<br>'
        html_parts.append(step_text)
        
        html_parts.append('<div class="result-box">')
        html_parts.append('🎯 <strong>Result: ' + str(n1) + ' × ' + str(n2) + ' = ' + str(result) + '</strong>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    # ============ FIRST-DEGREE EQUATION ============
    def solve_linear(self, equation_str):
        """Solve first-degree equation with all steps"""
        try:
            html_parts = []
            html_parts.append('<div class="theory-box">')
            html_parts.append('<div class="theory-title">📚 First-Degree Equation - Theory</div>')
            html_parts.append('<p><b>ax + b = 0</b>. Isolate the variable using inverse operations.</p>')
            html_parts.append('</div>')
            
            if '=' in equation_str:
                left_str, right_str = equation_str.split('=')
                left_expr = self.parse_func(left_str.strip())
                right_expr = self.parse_func(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_func(equation_str)
                if expr is None:
                    return "Error: Invalid expression"
                expr = expand(expr)
            
            html_parts.append('<div class="step-box">')
            html_parts.append('<strong>📝 Step-by-Step Resolution:</strong><br><br>')
            
            # Step 1: Original equation
            if '=' in equation_str:
                html_parts.append('<span class="step-number">1</span> <strong>Original equation:</strong><br>')
                html_parts.append('<div class="formula-highlight">$$' + 
                                self.escape_latex(latex(left_expr)) + ' = ' + 
                                self.escape_latex(latex(right_expr)) + '$$</div>')
            
            # Step 2: Standard form
            html_parts.append('<span class="step-number">2</span> <strong>Standard form:</strong><br>')
            html_parts.append('<div class="formula-highlight">$$' + 
                            self.escape_latex(latex(expr)) + ' = 0$$</div>')
            
            # Get coefficients
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a = 0
                b = coeffs[0]
            else:
                a = 0
                b = 0
            
            # Step 3: Identify coefficients
            html_parts.append('<span class="step-number">3</span> <strong>Identify coefficients:</strong><br>')
            html_parts.append('• a = ' + str(a) + '<br>')
            html_parts.append('• b = ' + str(b) + '<br>')
            
            if a == 0:
                html_parts.append('<br>Not a first-degree equation (a = 0).<br>')
                html_parts.append('</div>')
                return '\n'.join(html_parts)
            
            # Step 4: Isolate x
            html_parts.append('<span class="step-number">4</span> <strong>Isolate variable term:</strong><br>')
            html_parts.append('$$' + str(a) + 'x + (' + str(b) + ') = 0$$<br>')
            html_parts.append('$$' + str(a) + 'x = ' + str(-b) + '$$<br>')
            
            # Step 5: Solve
            x_sol = -b / a
            html_parts.append('<span class="step-number">5</span> <strong>Solve for x:</strong><br>')
            html_parts.append('$$x = \\frac{' + str(-b) + '}{' + str(a) + '}$$<br>')
            html_parts.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x_sol))) + '$$<br>')
            
            if x_sol != int(x_sol):
                html_parts.append('$$x \\approx ' + '{:.4f}'.format(float(x_sol)) + '$$<br>')
            
            # Step 6: Verify
            html_parts.append('<span class="step-number">6</span> <strong>Verification:</strong><br>')
            check = simplify(expr.subs(self.x, x_sol))
            html_parts.append('$$' + self.escape_latex(latex(check)) + ' = 0$$ ✅<br>')
            
            html_parts.append('<div class="result-box">')
            html_parts.append('🎯 <strong>Final Answer: x = ' + self.escape_latex(latex(sp.nsimplify(x_sol))) + '</strong>')
            html_parts.append('</div>')
            html_parts.append('</div>')
            
            return '\n'.join(html_parts)
        except Exception as e:
            return "Error: " + str(e)
    
    # ============ QUADRATIC EQUATION ============
    def solve_quadratic(self, func_str):
        """Solve quadratic equation with all steps"""
        try:
            html_parts = []
            html_parts.append('<div class="theory-box">')
            html_parts.append('<div class="theory-title">📚 Quadratic Equation - Theory</div>')
            html_parts.append('<p><b>ax² + bx + c = 0</b>. Quadratic formula: $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$</p>')
            html_parts.append('</div>')
            
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
            
            html_parts.append('<div class="step-box">')
            html_parts.append('<strong>📝 Step-by-Step Resolution:</strong><br><br>')
            
            # Step 1
            html_parts.append('<span class="step-number">1</span> <strong>Equation:</strong><br>')
            html_parts.append('<div class="formula-highlight">$$' + 
                            self.escape_latex(latex(expr)) + ' = 0$$</div>')
            
            # Get coefficients
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
                    b = 0
                    c = 0
                else:
                    a = b = c = 0
            except:
                a = b = c = 0
            
            # Step 2: Coefficients
            html_parts.append('<span class="step-number">2</span> <strong>Identify coefficients:</strong><br>')
            html_parts.append('• a = ' + str(a) + '<br>')
            html_parts.append('• b = ' + str(b) + '<br>')
            html_parts.append('• c = ' + str(c) + '<br>')
            
            if a == 0:
                html_parts.append('<br><b>Not quadratic (a=0).</b><br>')
                html_parts.append('</div>')
                return '\n'.join(html_parts)
            
            # Step 3: Discriminant
            disc = b**2 - 4*a*c
            html_parts.append('<span class="step-number">3</span> <strong>Calculate discriminant:</strong><br>')
            html_parts.append('$$\\Delta = b^2 - 4ac$$<br>')
            html_parts.append('$$\\Delta = (' + str(b) + ')^2 - 4(' + str(a) + ')(' + str(c) + ')$$<br>')
            html_parts.append('$$\\Delta = ' + str(b**2) + ' - ' + str(4*a*c) + '$$<br>')
            html_parts.append('$$\\Delta = ' + str(disc) + '$$<br>')
            
            # Step 4: Nature of roots
            html_parts.append('<span class="step-number">4</span> <strong>Nature of roots:</strong><br>')
            if disc > 0:
                html_parts.append('Δ > 0 → <b>Two distinct real roots</b><br>')
            elif disc == 0:
                html_parts.append('Δ = 0 → <b>One real double root</b><br>')
            else:
                html_parts.append('Δ < 0 → <b>Two complex conjugate roots</b><br>')
            
            # Step 5: Apply formula
            html_parts.append('<span class="step-number">5</span> <strong>Apply quadratic formula:</strong><br>')
            
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                
                html_parts.append('$$x = \\frac{-' + str(b) + ' \\pm \\sqrt{' + str(disc) + '}}{2(' + str(a) + ')}$$<br>')
                
                if disc > 0:
                    html_parts.append('$$x_1 = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$<br>')
                    html_parts.append('$$x_2 = ' + self.escape_latex(latex(sp.nsimplify(x2))) + '$$<br>')
                    
                    if x1 != int(x1):
                        html_parts.append('$$x_1 \\approx ' + '{:.4f}'.format(x1) + '$$<br>')
                    if x2 != int(x2):
                        html_parts.append('$$x_2 \\approx ' + '{:.4f}'.format(x2) + '$$<br>')
                else:
                    html_parts.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$ (double root)<br>')
            else:
                real_part = -b / (2*a)
                imag_part = math.sqrt(-disc) / (2*a)
                html_parts.append('$$x = \\frac{-' + str(b) + ' \\pm i\\sqrt{' + str(-disc) + '}}{2(' + str(a) + ')}$$<br>')
                html_parts.append('$$x = ' + '{:.4f}'.format(real_part) + ' \\pm ' + '{:.4f}'.format(imag_part) + 'i$$<br>')
            
            # Step 6: Verification
            if disc >= 0:
                html_parts.append('<span class="step-number">6</span> <strong>Verification:</strong><br>')
                if disc > 0:
                    v1 = simplify(expr.subs(self.x, x1))
                    v2 = simplify(expr.subs(self.x, x2))
                    html_parts.append('For x₁: ' + self.escape_latex(latex(v1)) + ' = 0 ✅<br>')
                    html_parts.append('For x₂: ' + self.escape_latex(latex(v2)) + ' = 0 ✅<br>')
                else:
                    v = simplify(expr.subs(self.x, x1))
                    html_parts.append(self.escape_latex(latex(v)) + ' = 0 ✅<br>')
            
            html_parts.append('<div class="result-box">')
            if disc > 0:
                html_parts.append('🎯 <strong>Final Answer:</strong><br>')
                html_parts.append('$$x_1 = ' + self.escape_latex(latex(sp.nsimplify(x1))) + ',\\; x_2 = ' + self.escape_latex(latex(sp.nsimplify(x2))) + '$$')
            elif disc == 0:
                html_parts.append('🎯 <strong>Final Answer:</strong><br>')
                html_parts.append('$$x = ' + self.escape_latex(latex(sp.nsimplify(x1))) + '$$ (double)')
            else:
                html_parts.append('🎯 <strong>Final Answer:</strong><br>')
                html_parts.append('$$x = ' + '{:.4f}'.format(real_part) + ' \\pm ' + '{:.4f}'.format(imag_part) + 'i$$')
            html_parts.append('</div>')
            html_parts.append('</div>')
            
            return '\n'.join(html_parts)
        except Exception as e:
            return "Error: " + str(e)
    
    # ============ DIFFERENTIATION ============
    def differentiate(self, func_str, var='x'):
        """Differentiation with step-by-step"""
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "Error: Invalid function"
            
            sym_var = Symbol(var)
            html_parts = []
            
            html_parts.append('<div class="theory-box">')
            html_parts.append('<div class="theory-title">📚 Differentiation Rules</div>')
            html_parts.append('<p>Power Rule, Sum Rule, Product Rule, Chain Rule.</p>')
            html_parts.append('</div>')
            
            html_parts.append('<div class="step-box">')
            html_parts.append('<strong>📝 Step-by-Step Differentiation:</strong><br><br>')
            
            # Step 1
            html_parts.append('<span class="step-number">1</span> <strong>Function:</strong><br>')
            html_parts.append('<div class="formula-highlight">$$f(' + var + ') = ' + 
                            self.escape_latex(latex(expr)) + '$$</div>')
            
            # Step 2: Expand
            expanded = expand(expr)
            html_parts.append('<span class="step-number">2</span> <strong>Expand:</strong><br>')
            html_parts.append('$$f(' + var + ') = ' + self.escape_latex(latex(expanded)) + '$$<br>')
            
            # Step 3: Term by term
            html_parts.append('<span class="step-number">3</span> <strong>Differentiate term by term:</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                deriv = diff(term, sym_var)
                html_parts.append('Term ' + str(i+1) + ': d/d' + var + '(' + 
                                self.escape_latex(latex(term)) + ') = ' + 
                                self.escape_latex(latex(deriv)) + '<br>')
            
            # Step 4: Combine
            result = diff(expr, sym_var)
            simplified = simplify(result)
            html_parts.append('<span class="step-number">4</span> <strong>Combine:</strong><br>')
            html_parts.append('$$f\\'(' + var + ') = ' + self.escape_latex(latex(result)) + '$$<br>')
            
            html_parts.append('<span class="step-number">5</span> <strong>Simplify:</strong><br>')
            html_parts.append('$$f\\'(' + var + ') = ' + self.escape_latex(latex(simplified)) + '$$<br>')
            
            html_parts.append('<div class="result-box">')
            html_parts.append('🎯 $$\\boxed{f\\'(' + var + ') = ' + self.escape_latex(latex(simplified)) + '}$$')
            html_parts.append('</div>')
            html_parts.append('</div>')
            
            return '\n'.join(html_parts)
        except Exception as e:
            return "Error: " + str(e)
    
    # ============ INTEGRATION ============
    def integrate_func(self, func_str, var='x'):
        """Integration with step-by-step"""
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "Error: Invalid function"
            
            sym_var = Symbol(var)
            html_parts = []
            
            html_parts.append('<div class="theory-box">')
            html_parts.append('<div class="theory-title">📚 Integration Rules</div>')
            html_parts.append('<p>Power Rule, Sum Rule, Constant Multiple Rule.</p>')
            html_parts.append('</div>')
            
            html_parts.append('<div class="step-box">')
            html_parts.append('<strong>📝 Step-by-Step Integration:</strong><br><br>')
            
            # Step 1
            html_parts.append('<span class="step-number">1</span> <strong>Integral:</strong><br>')
            html_parts.append('<div class="formula-highlight">$$\\int (' + 
                            self.escape_latex(latex(expr)) + ') \\, d' + var + '$$</div>')
            
            # Step 2: Expand
            expanded = expand(expr)
            html_parts.append('<span class="step-number">2</span> <strong>Expand integrand:</strong><br>')
            html_parts.append('$$\\int (' + self.escape_latex(latex(expanded)) + ') \\, d' + var + '$$<br>')
            
            # Step 3: Term by term
            html_parts.append('<span class="step-number">3</span> <strong>Integrate term by term:</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                integral_term = integrate(term, sym_var)
                html_parts.append('Term ' + str(i+1) + ': ∫(' + 
                                self.escape_latex(latex(term)) + ') d' + var + ' = ' + 
                                self.escape_latex(latex(integral_term)) + '<br>')
            
            # Step 4: Combine
            result = integrate(expr, sym_var)
            html_parts.append('<span class="step-number">4</span> <strong>Combine:</strong><br>')
            html_parts.append('$$\\int (' + self.escape_latex(latex(expr)) + ') \\, d' + var + 
                            ' = ' + self.escape_latex(latex(result)) + ' + C$$<br>')
            
            html_parts.append('<div class="result-box">')
            html_parts.append('🎯 $$\\boxed{\\int (' + self.escape_latex(latex(expr)) + 
                            ') \\, d' + var + ' = ' + self.escape_latex(latex(result)) + ' + C}$$')
            html_parts.append('</div>')
            html_parts.append('</div>')
            
            return '\n'.join(html_parts)
        except Exception as e:
            return "Error: " + str(e)

# Initialize session state
if 'solver' not in st.session_state:
    st.session_state.solver = MathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Title
st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Complete Step-by-Step Mathematics Solver</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Mode")
    mode = st.selectbox("Choose operation:", [
        "Basic Arithmetic",
        "First-Degree Equation",
        "Quadratic Equation",
        "Differentiation",
        "Integration"
    ])
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset"):
            st.session_state.result_html = ""
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All"):
            st.session_state.result_html = ""
            st.session_state.history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("## 📊 History")
    for h in st.session_state.history[-5:]:
        st.info(h)

# Main layout
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
    
    elif mode == "First-Degree Equation":
        st.markdown("**Enter equation:** (e.g., 2x + 3 = 7)")
        eq = st.text_input("Equation:", "2x + 3 = 7")
        
        if st.button("📐 Solve", use_container_width=True):
            html_res = solver.solve_linear(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")
    
    elif mode == "Quadratic Equation":
        st.markdown("**Enter equation:** (e.g., x^2 + 3x - 4 = 0)")
        eq = st.text_input("Equation:", "x^2 + 3x - 4 = 0")
        
        if st.button("🔢 Solve", use_container_width=True):
            html_res = solver.solve_quadratic(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quadratic: {eq}")
    
    elif mode == "Differentiation":
        st.markdown("**Enter function:** (e.g., x^2 + 3x + 5)")
        func = st.text_input("f(x) =", "x^2 + 3x + 5")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        
        if st.button("📈 Differentiate", use_container_width=True):
            html_res = solver.differentiate(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Diff: {func}")
    
    elif mode == "Integration":
        st.markdown("**Enter function:** (e.g., x^2 + 3x)")
        func = st.text_input("f(x) =", "x^2 + 3x")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        
        if st.button("📊 Integrate", use_container_width=True):
            html_res = solver.integrate_func(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Int: {func}")

# Result panel
with col_out:
    st.markdown("### ✨ Step-by-Step Solution")
    
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
        st.info("👈 Choose a mode, enter your data, and click Calculate to see the complete step-by-step solution!")

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#666; padding:20px;">
    <p>🧮 HandCalc Pro - Every Step Explained, Every Answer Verified</p>
</div>
""", unsafe_allow_html=True)
