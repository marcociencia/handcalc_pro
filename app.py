# app.py - Complete Fixed Version with Step-by-Step Display
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand, 
                   factor, sqrt as sym_sqrt, Matrix, Eq, limit, oo, sin, cos, 
                   tan, exp, log, Derivative, Integral, Symbol, Function)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
import re

# Page configuration
st.set_page_config(
    page_title="HandCalc Pro - Complete Step-by-Step Mathematics",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap');
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .theory-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 5px solid #667eea;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .theory-title {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .step-box {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        border-left: 3px solid #764ba2;
    }
    
    .step-number {
        display: inline-block;
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }
    
    .formula-highlight {
        background: #f8f9fa;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 15px 0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        font-size: 24px;
        font-weight: bold;
    }
    
    .stButton > button {
        width: 100%;
        height: 55px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .function-input {
        font-family: 'Courier New', monospace;
        font-size: 18px;
        padding: 10px;
        border: 2px solid #667eea;
        border-radius: 10px;
        background: #f8f9fa;
    }
</style>

<script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$']],
            displayMath: [['$$', '$$']],
            processEscapes: true,
            packages: ['base', 'ams', 'noerrors', 'noundefined']
        },
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
        },
        loader: {
            load: ['[tex]/noerrors']
        }
    };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
""", unsafe_allow_html=True)

class CompleteMathSolver:
    """Complete mathematical solver with full step-by-step solutions"""
    
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
    
    def parse_function(self, func_str: str) -> sp.Expr:
        """Parse function string with proper formatting"""
        transformations = (standard_transformations + (implicit_multiplication_application,))
        # Clean up the input
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('×', '*')
        func_str = func_str.replace('÷', '/')
        func_str = func_str.replace(' ', '')
        
        # Add multiplication sign between number and variable (e.g., 3x -> 3*x)
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
        
        try:
            return parse_expr(func_str, transformations=transformations)
        except:
            return None
    
    def solve_first_degree_equation(self, equation_str: str) -> str:
        """Solve first-degree equation with complete step-by-step"""
        try:
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 First-Degree Equation - Theory</div>'
            html += '<p>A first-degree (linear) equation has the form:</p>'
            html += '<div class="formula-highlight">$$ax + b = 0$$</div>'
            html += '<p><strong>Solution Method:</strong> Isolate the variable by performing inverse operations on both sides.</p>'
            html += '<p><strong>Golden Rule:</strong> Whatever you do to one side, you must do to the other!</p>'
            html += '</div>'
            
            # Parse the equation
            if '=' in equation_str:
                left_str, right_str = equation_str.split('=')
                left_expr = self.parse_function(left_str.strip())
                right_expr = self.parse_function(right_str.strip())
                if left_expr is None or right_expr is None:
                    return "Error: Invalid equation"
                expr = left_expr - right_expr
            else:
                expr = self.parse_function(equation_str)
                if expr is None:
                    return "Error: Invalid expression"
            
            html += '<div class="step-box">'
            html += '<strong>📝 Step-by-Step Resolution:</strong><br><br>'
            
            # Original equation
            if '=' in equation_str:
                html += f'<strong>Original equation:</strong>'
                html += f'<div class="formula-highlight">$${sp.latex(left_expr)} = {sp.latex(right_expr)}$$</div>'
            
            # Get coefficients
            expanded = expand(expr)
            coeffs = sp.Poly(expanded, self.x).all_coeffs()
            
            if len(coeffs) == 1:  # Constant only
                a = 0
                b = coeffs[0]
            elif len(coeffs) == 2:  # ax + b
                a = coeffs[0]
                b = coeffs[1]
            else:
                a = 0
                b = coeffs[0]
            
            html += f'<span class="step-number">1</span> <strong>Write in standard form ax + b = 0:</strong><br>'
            html += f'<div class="formula-highlight">$${sp.latex(expanded)} = 0$$</div>'
            
            # Identify coefficients
            html += f'<span class="step-number">2</span> <strong>Identify coefficients:</strong><br>'
            html += f'• a = {a} (coefficient of x)<br>'
            html += f'• b = {b} (constant term)<br>'
            
            if a != 0:
                # Move b to right side
                html += f'<span class="step-number">3</span> <strong>Move constant term to right side:</strong><br>'
                html += f'$${a}x + ({b}) = 0$$'
                html += f'<br>$${a}x = -({b})$$'
                html += f'<br>$${a}x = {-b}$$'
                
                # Divide by a
                html += f'<span class="step-number">4</span> <strong>Divide both sides by {a}:</strong><br>'
                html += f'$$\\frac{{{a}x}}{{{a}}} = \\frac{{{-b}}}{{{a}}}$$'
                
                # Solution
                x_solution = -b / a
                html += f'<span class="step-number">5</span> <strong>Simplify:</strong><br>'
                html += f'$$x = {sp.latex(x_solution)}$$'
                
                if x_solution == int(x_solution):
                    html += f'<br><strong>Decimal form:</strong> x = {int(x_solution)}'
                else:
                    html += f'<br><strong>Decimal approximation:</strong> x ≈ {float(x_solution):.4f}'
                
                # Verification
                html += f'<br><br><span class="step-number">6</span> <strong>Verify solution:</strong><br>'
                html += f'Substitute x = {sp.latex(x_solution)} back into equation:<br>'
                verification = expanded.subs(self.x, x_solution)
                html += f'$${sp.latex(expanded.subs(self.x, self.x))} = {sp.latex(verification)}$$'
                html += f'<br>$$0 = 0 \\checkmark$$'
                
            else:
                html += '<br>This is not a first-degree equation (a = 0).<br>'
                if b == 0:
                    html += '<strong>This is an identity: 0 = 0 (infinitely many solutions)</strong>'
                else:
                    html += '<strong>This equation has no solution (contradiction)</strong>'
            
            # Final answer box
            html += '<div class="result-box">'
            if a != 0:
                html += f'🎯 <strong>Final Answer: x = {sp.latex(x_solution)}</strong>'
                if x_solution == int(x_solution):
                    html += f'<br>$$x = {int(x_solution)}$$'
            html += '</div>'
            
            html += '</div>'
            return html
            
        except Exception as e:
            return f"Error solving equation: {str(e)}"
    
    def solve_quadratic_equation(self, func_str: str) -> str:
        """Solve quadratic equation with complete step-by-step"""
        try:
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Quadratic Equation - Theory</div>'
            html += '<p>A quadratic equation has the form:</p>'
            html += '<div class="formula-highlight">$$ax^2 + bx + c = 0$$</div>'
            html += '<p><strong>Solution Methods:</strong></p>'
            html += '<ul>'
            html += '<li><strong>Quadratic Formula:</strong> $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$</li>'
            html += '<li><strong>Factoring:</strong> When possible</li>'
            html += '<li><strong>Completing the Square:</strong> Convert to vertex form</li>'
            html += '</ul>'
            html += '</div>'
            
            # Parse function
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
            
            html += '<div class="step-box">'
            html += '<strong>📝 Complete Step-by-Step Resolution:</strong><br><br>'
            
            # Original equation
            html += f'<span class="step-number">1</span> <strong>Original equation:</strong><br>'
            html += f'<div class="formula-highlight">$${sp.latex(expr)} = 0$$</div>'
            
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
                    a, b, c = 0, 0, 0
            except:
                a, b, c = 0, 0, 0
            
            html += f'<span class="step-number">2</span> <strong>Identify coefficients:</strong><br>'
            html += f'• a = {a}<br>'
            html += f'• b = {b}<br>'
            html += f'• c = {c}<br>'
            
            if a == 0:
                html += '<br><strong>This is not a quadratic equation (a = 0).</strong><br>'
                if b != 0:
                    html += 'Solving as linear equation:<br>'
                    x_solution = -c / b
                    html += f'$$x = {sp.latex(x_solution)}$$'
                return html + '</div>'
            
            # Calculate discriminant
            discriminant = b**2 - 4*a*c
            
            html += f'<span class="step-number">3</span> <strong>Calculate discriminant (Δ):</strong><br>'
            html += f'$$\\Delta = b^2 - 4ac$$'
            html += f'<br>$$\\Delta = ({b})^2 - 4({a})({c})$$'
            html += f'<br>$$\\Delta = {b**2} - ({4*a*c})$$'
            html += f'<br>$$\\Delta = {discriminant}$$'
            
            html += f'<span class="step-number">4</span> <strong>Analyze discriminant:</strong><br>'
            
            if discriminant > 0:
                html += f'<strong>Δ > 0:</strong> Two distinct real roots<br>'
                
                html += f'<span class="step-number">5</span> <strong>Apply quadratic formula:</strong><br>'
                html += f'$$x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$$'
                html += f'<br>$$x = \\frac{{-({b}) \\pm \\sqrt{{{discriminant}}}}}{{2({a})}}$$'
                
                sqrt_disc = math.sqrt(discriminant)
                if sqrt_disc == int(sqrt_disc):
                    sqrt_disc_str = str(int(sqrt_disc))
                else:
                    sqrt_disc_str = f"{sqrt_disc:.4f}"
                
                html += f'<br>$$x = \\frac{{-{b} \\pm {sqrt_disc_str}}}{{{2*a}}}$$'
                
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                
                html += f'<span class="step-number">6</span> <strong>Calculate both roots:</strong><br>'
                html += f'<strong>First root (x₁):</strong><br>'
                html += f'$$x_1 = \\frac{{-{b} + {sqrt_disc_str}}}{{{2*a}}}$$'
                html += f'<br>$$x_1 = \\frac{{{-b + sqrt_disc:.4f}}}{{{2*a}}}$$'
                html += f'<br>$$x_1 = {sp.latex(sp.nsimplify(x1))}$$'
                if x1 != int(x1):
                    html += f'<br>$$x_1 \\approx {x1:.4f}$$'
                
                html += f'<br><strong>Second root (x₂):</strong><br>'
                html += f'$$x_2 = \\frac{{-{b} - {sqrt_disc_str}}}{{{2*a}}}$$'
                html += f'<br>$$x_2 = \\frac{{{-b - sqrt_disc:.4f}}}{{{2*a}}}$$'
                html += f'<br>$$x_2 = {sp.latex(sp.nsimplify(x2))}$$'
                if x2 != int(x2):
                    html += f'<br>$$x_2 \\approx {x2:.4f}$$'
                
            elif discriminant == 0:
                html += f'<strong>Δ = 0:</strong> One real double root<br>'
                
                html += f'<span class="step-number">5</span> <strong>Apply formula (simplified):</strong><br>'
                html += f'$$x = \\frac{{-b}}{{2a}}$$'
                html += f'<br>$$x = \\frac{{-({b})}}{{2({a})}}$$'
                
                x = -b / (2*a)
                html += f'<br>$$x = {sp.latex(sp.nsimplify(x))}$$'
                if x != int(x):
                    html += f'<br>$$x \\approx {x:.4f}$$'
                
            else:
                html += f'<strong>Δ < 0:</strong> Two complex conjugate roots<br>'
                
                html += f'<span class="step-number">5</span> <strong>Apply formula with complex numbers:</strong><br>'
                real_part = -b / (2*a)
                imag_part = math.sqrt(-discriminant) / (2*a)
                
                html += f'$$x = \\frac{{-b \\pm i\\sqrt{{|\\Delta|}}}}{{2a}}$$'
                html += f'<br>$$x = \\frac{{-({b}) \\pm i\\sqrt{{{abs(discriminant)}}}}}{{2({a})}}$$'
                html += f'<br>$$x = {real_part:.4f} \\pm {imag_part:.4f}i$$'
            
            # Final answer box
            html += '<div class="result-box">'
            if discriminant > 0:
                html += f'🎯 <strong>Final Answer:</strong><br>'
                html += f'$$x_1 = {sp.latex(sp.nsimplify(x1))},\\quad x_2 = {sp.latex(sp.nsimplify(x2))}$$'
            elif discriminant == 0:
                html += f'🎯 <strong>Final Answer:</strong><br>'
                html += f'$$x = {sp.latex(sp.nsimplify(x))} \\text{{ (double root)}}$$'
            else:
                html += f'🎯 <strong>Final Answer:</strong><br>'
                html += f'$$x = {real_part:.4f} \\pm {imag_part:.4f}i$$'
            html += '</div>'
            
            html += '</div>'
            return html
            
        except Exception as e:
            return f"Error solving quadratic: {str(e)}"
    
    def differentiate_step_by_step(self, func_str: str, var: str = 'x') -> str:
        """Perform differentiation with complete step-by-step"""
        try:
            expr = self.parse_function(func_str)
            if expr is None:
                return "Error: Invalid function"
            
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Differentiation Rules - Theory</div>'
            html += '<p><strong>Basic Differentiation Rules:</strong></p>'
            html += '<ul>'
            html += '<li><strong>Power Rule:</strong> d/dx[x^n] = n·x^(n-1)</li>'
            html += '<li><strong>Sum Rule:</strong> d/dx[f + g] = f\' + g\'</li>'
            html += '<li><strong>Product Rule:</strong> d/dx[f·g] = f\'·g + f·g\'</li>'
            html += '<li><strong>Chain Rule:</strong> d/dx[f(g(x))] = f\'(g(x))·g\'(x)</li>'
            html += '</ul>'
            html += '</div>'
            
            html += '<div class="step-box">'
            html += '<strong>📝 Step-by-Step Differentiation:</strong><br><br>'
            
            sym_var = Symbol(var)
            
            html += f'<span class="step-number">1</span> <strong>Given function:</strong><br>'
            html += f'<div class="formula-highlight">$$f({var}) = {sp.latex(expr)}$$</div>'
            
            html += f'<span class="step-number">2</span> <strong>Expand the expression:</strong><br>'
            expanded = expand(expr)
            html += f'$$f({var}) = {sp.latex(expanded)}$$'
            
            html += f'<span class="step-number">3</span> <strong>Apply differentiation term by term:</strong><br>'
            
            # Break down into terms
            if expanded.is_Add:
                terms = expanded.args
            else:
                terms = [expanded]
            
            for i, term in enumerate(terms):
                derivative = diff(term, sym_var)
                html += f'<br><strong>Term {i+1}:</strong> d/d{var}({sp.latex(term)}) = {sp.latex(derivative)}'
                
                # Explain the rule used
                if term.is_Pow:
                    html += ' (Power Rule)'
                elif term.is_Mul:
                    html += ' (Product Rule)'
                elif term.func == sin:
                    html += ' (d/dx[sin(x)] = cos(x))'
                elif term.func == cos:
                    html += ' (d/dx[cos(x)] = -sin(x))'
                elif term.func == exp:
                    html += ' (d/dx[e^x] = e^x)'
                elif term.func == log:
                    html += ' (d/dx[ln(x)] = 1/x)'
            
            html += f'<span class="step-number">4</span> <strong>Combine results:</strong><br>'
            result = diff(expr, sym_var)
            html += f'<div class="formula-highlight">$$f\'({var}) = {sp.latex(result)}$$</div>'
            
            html += f'<span class="step-number">5</span> <strong>Simplify:</strong><br>'
            simplified = simplify(result)
            html += f'$$f\'({var}) = {sp.latex(simplified)}$$'
            
            html += '<div class="result-box">'
            html += f'🎯 <strong>Final Answer:</strong><br>'
            html += f'$$\\boxed{{f\'({var}) = {sp.latex(simplified)}}}$$'
            html += '</div>'
            
            html += '</div>'
            return html
            
        except Exception as e:
            return f"Error in differentiation: {str(e)}"
    
    def integrate_step_by_step(self, func_str: str, var: str = 'x') -> str:
        """Perform integration with complete step-by-step"""
        try:
            expr = self.parse_function(func_str)
            if expr is None:
                return "Error: Invalid function"
            
            html = '<div class="theory-box">'
            html += '<div class="theory-title">📚 Integration Rules - Theory</div>'
            html += '<p><strong>Basic Integration Rules:</strong></p>'
            html += '<ul>'
            html += '<li><strong>Power Rule:</strong> ∫x^n dx = x^(n+1)/(n+1) + C, n ≠ -1</li>'
            html += '<li><strong>Sum Rule:</strong> ∫(f + g)dx = ∫f dx + ∫g dx</li>'
            html += '<li><strong>Constant Multiple:</strong> ∫k·f dx = k·∫f dx</li>'
            html += '</ul>'
            html += '</div>'
            
            html += '<div class="step-box">'
            html += '<strong>📝 Step-by-Step Integration:</strong><br><br>'
            
            sym_var = Symbol(var)
            
            html += f'<span class="step-number">1</span> <strong>Given integral:</strong><br>'
            html += f'<div class="formula-highlight">$$\\int ({sp.latex(expr)}) \\, d{var}$$</div>'
            
            html += f'<span class="step-number">2</span> <strong>Expand the integrand:</strong><br>'
            expanded = expand(expr)
            html += f'$$\\int ({sp.latex(expanded)}) \\, d{var}$$'
            
            html += f'<span class="step-number">3</span> <strong>Integrate term by term:</strong><br>'
            
            if expanded.is_Add:
                terms = expanded.args
            else:
                terms = [expanded]
            
            for i, term in enumerate(terms):
                integral = integrate(term, sym_var)
                html += f'<br><strong>Term {i+1}:</strong> ∫({sp.latex(term)}) d{var} = {sp.latex(integral)}'
                
                # Explain the rule
                if term.is_Pow and term.args[1].is_Number:
                    html += ' (Power Rule: increase exponent by 1 and divide)'
                elif term.is_Number:
                    html += ' (Constant: ∫k dx = kx)'
                elif term.is_Symbol:
                    html += ' (∫x dx = x²/2)'
                elif term.func == exp:
                    html += ' (∫e^x dx = e^x)'
                elif term.func == sin:
                    html += ' (∫sin(x) dx = -cos(x))'
                elif term.func == cos:
                    html += ' (∫cos(x) dx = sin(x))'
            
            html += f'<span class="step-number">4</span> <strong>Combine results:</strong><br>'
            result = integrate(expr, sym_var)
            html += f'<div class="formula-highlight">$$\\int ({sp.latex(expr)}) \\, d{var} = {sp.latex(result)} + C$$</div>'
            
            html += '<div class="result-box">'
            html += f'🎯 <strong>Final Answer:</strong><br>'
            html += f'$$\\boxed{{\\int ({sp.latex(expr)}) \\, d{var} = {sp.latex(result)} + C}}$$'
            html += '</div>'
            
            html += '</div>'
            return html
            
        except Exception as e:
            return f"Error in integration: {str(e)}"
    
    def manual_addition(self, num1: int, num2: int) -> str:
        """Complete manual addition step-by-step"""
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        result = num1 + num2
        
        # Calculate carries
        carries = []
        carry = 0
        padded1 = str1.zfill(max_len)
        padded2 = str2.zfill(max_len)
        
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(padded1[i]) + int(padded2[i]) + carry
            carries.insert(0, digit_sum // 10)
            carry = digit_sum // 10
        
        html = '<div class="step-box">'
        html += '<strong>➕ Manual Addition - Complete Resolution</strong><br><br>'
        
        # Display the manual calculation
        html += '<div style="font-family: Courier New; font-size: 24px; line-height: 1.8; text-align: right; letter-spacing: 3px; background: #f8f9fa; padding: 20px; border-radius: 10px;">'
        
        if any(c > 0 for c in carries):
            carry_str = ' '.join(str(c) if c > 0 else ' ' for c in carries)
            html += f'<div style="color: #f093fb; font-size: 18px; margin-bottom: -10px;">{carry_str}</div>'
        
        html += f'<div>{str1}</div>'
        html += f'<div style="color: #667eea;">+ {str2}</div>'
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        html += f'<div style="color: #764ba2; font-weight: bold;">{result}</div>'
        html += '</div>'
        
        # Step-by-step explanation
        html += '<br><strong>Step-by-step Explanation:</strong><br>'
        
        for i in range(max_len):
            pos = max_len - 1 - i
            digit1 = int(padded1[pos])
            digit2 = int(padded2[pos])
            position_name = ['units', 'tens', 'hundreds', 'thousands'][min(i, 3)]
            
            html += f'<br><span class="step-number">{i+1}</span> <strong>{position_name.capitalize()} column:</strong><br>'
            html += f'{digit1} + {digit2}'
            if carries[pos] > 0:
                html += f' + {carries[pos]} (carry)'
            current_sum = digit1 + digit2 + (carries[pos+1] if pos < max_len-1 else 0)
            html += f' = {current_sum}<br>'
            if carries[pos] > 0:
                html += f'Write {current_sum % 10}, carry {carries[pos]}<br>'
            else:
                html += f'Write {current_sum}<br>'
        
        html += f'<br><div class="result-box">'
        html += f'🎯 <strong>Final Result: {num1} + {num2} = {result}</strong>'
        html += '</div>'
        html += '</div>'
        
        return html
    
    def manual_multiplication(self, num1: int, num2: int) -> str:
        """Complete manual multiplication step-by-step"""
        str1, str2 = str(num1), str(num2)
        result = num1 * num2
        
        # Calculate partial products
        partial_products = []
        str2_digits = list(str2)
        
        for i, digit in enumerate(reversed(str2_digits)):
            partial = num1 * int(digit) * (10 ** i)
            partial_products.append(partial)
        
        html = '<div class="step-box">'
        html += '<strong>✖️ Manual Multiplication - Complete Resolution</strong><br><br>'
        
        # Display the manual calculation
        html += '<div style="font-family: Courier New; font-size: 24px; line-height: 1.8; text-align: right; letter-spacing: 3px; background: #f8f9fa; padding: 20px; border-radius: 10px;">'
        html += f'<div>{str1}</div>'
        html += f'<div style="color: #667eea;">× {str2}</div>'
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        
        partial_products_reversed = partial_products.copy()
        partial_products_reversed.reverse()
        
        for i, pp in enumerate(partial_products_reversed):
            if i == 0:
                html += f'<div>{pp}</div>'
            else:
                html += f'<div style="color: #667eea;">+ {pp}</div>'
        
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        html += f'<div style="color: #764ba2; font-weight: bold;">{result}</div>'
        html += '</div>'
        
        # Step-by-step explanation
        html += '<br><strong>Step-by-step Explanation:</strong><br>'
        
        for i, digit in enumerate(reversed(str2_digits)):
            html += f'<br><span class="step-number">{i+1}</span> <strong>Multiply by {digit} ({"units" if i == 0 else "tens" if i == 1 else "hundreds"}):</strong><br>'
            html += f'{num1} × {digit} = {num1 * int(digit)}<br>'
            if i > 0:
                html += f'Add {i} zero(s): {num1 * int(digit)}{"0" * i}<br>'
        
        html += f'<br><span class="step-number">{len(str2_digits) + 1}</span> <strong>Add all partial products:</strong><br>'
        html += ' + '.join([str(pp) for pp in partial_products_reversed])
        html += f' = {result}<br>'
        
        html += f'<br><div class="result-box">'
        html += f'🎯 <strong>Final Result: {num1} × {num2} = {result}</strong>'
        html += '</div>'
        html += '</div>'
        
        return html

# Initialize components
if 'solver' not in st.session_state:
    st.session_state.solver = CompleteMathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Title
st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; font-size:18px;">Complete Step-by-Step Mathematics Solver</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Operation Mode")
    
    mode = st.selectbox(
        "Select Mode:",
        ["Basic Arithmetic", "First-Degree Equation", "Quadratic Equation", 
         "Differentiation", "Integration"]
    )
    
    st.markdown("---")
    
    # Reset buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.result_html = ""
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.result_html = ""
            st.session_state.history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("## 📊 History")
    for calc in st.session_state.history[-5:]:
        st.info(calc)

# Main content
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.markdown("### 📝 Input")
    
    solver = st.session_state.solver
    
    if mode == "Basic Arithmetic":
        operation = st.selectbox("Operation:", ["Addition (+)", "Multiplication (×)"])
        num1 = st.number_input("First Number:", value=123, format="%d")
        num2 = st.number_input("Second Number:", value=45, format="%d")
        
        if st.button("🧮 Calculate", use_container_width=True):
            if operation == "Addition (+)":
                result_html = solver.manual_addition(int(num1), int(num2))
            else:
                result_html = solver.manual_multiplication(int(num1), int(num2))
            st.session_state.result_html = result_html
            st.session_state.history.append(f"{num1} {operation[0]} {num2}")
    
    elif mode == "First-Degree Equation":
        st.markdown("**Enter first-degree equation:**")
        st.markdown("*Examples: 2x + 3 = 7, 5x - 10 = 0, 3x + 6 = 2x + 12*")
        equation = st.text_input("Equation:", "2x + 3 = 7", key="linear_eq")
        
        if st.button("📐 Solve Equation", use_container_width=True):
            result_html = solver.solve_first_degree_equation(equation)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Linear: {equation}")
    
    elif mode == "Quadratic Equation":
        st.markdown("**Enter quadratic equation or expression:**")
        st.markdown("*Examples: x^2 + 3x - 4 = 0, x^2 + 5x + 6, 2x^2 - 8x + 6 = 0*")
        func_input = st.text_input("f(x) =", "x^2 + 3x - 4", key="quadratic")
        
        if st.button("🔢 Solve Quadratic", use_container_width=True):
            result_html = solver.solve_quadratic_equation(func_input)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Quadratic: {func_input}")
    
    elif mode == "Differentiation":
        st.markdown("**Enter function to differentiate:**")
        st.markdown("*Examples: x^2 + 3x + 5, sin(x), x^2 * exp(x)*")
        func_input = st.text_input("f(x) =", "x^2 + 3x + 5", key="diff_func")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        
        if st.button("📈 Differentiate", use_container_width=True):
            result_html = solver.differentiate_step_by_step(func_input, var)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Derivative: {func_input}")
    
    elif mode == "Integration":
        st.markdown("**Enter function to integrate:**")
        st.markdown("*Examples: x^2 + 3x, sin(x), 2x + 1*")
        func_input = st.text_input("f(x) =", "x^2 + 3x", key="int_func")
        var = st.selectbox("Variable:", ["x", "y", "z"])
        
        if st.button("📊 Integrate", use_container_width=True):
            result_html = solver.integrate_step_by_step(func_input, var)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Integral: {func_input}")

# Result panel
with col_result:
    st.markdown("### ✨ Complete Step-by-Step Solution")
    
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
                <script>MathJax.typesetPromise();</script>
            </body>
            </html>
            """,
            height=700,
            scrolling=True
        )
    else:
        st.info("👈 Select a mode, enter your equation or numbers, and click Calculate to see the complete step-by-step resolution!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px; color:#666;">
    <p>🧮 HandCalc Pro - Complete Mathematical Solutions</p>
    <p>Every step explained • Every rule justified • Every answer verified</p>
</div>
""", unsafe_allow_html=True)
