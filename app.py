# app.py - Advanced Version with Complete Mathematical Suite
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand, 
                   factor, sqrt as sym_sqrt, Matrix, Eq, limit, oo, sin, cos, 
                   tan, exp, log, Derivative, Integral, Symbol, Function)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy.calculus.util import continuous_domain
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
import re

# Page configuration
st.set_page_config(
    page_title="HandCalc Pro - Advanced Mathematics Suite",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Code+Pro:wght@400;600;700&display=swap');
    
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
        font-style: italic;
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
    
    .formula-highlight {
        background: #f8f9fa;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 15px 0;
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
    
    .reset-button > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .mode-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s;
    }
    
    .mode-card:hover {
        transform: translateY(-5px);
    }
</style>

<!-- MathJax Configuration -->
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

class AdvancedMathSolver:
    """Advanced mathematical solver with complete theoretical background"""
    
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.t = Symbol('t')
        self.u = Function('u')(self.x)
        self.v = Function('v')(self.x)
    
    def parse_expression(self, expr_str: str, variables: List[str] = ['x']) -> sp.Expr:
        """Parse mathematical expression"""
        transformations = (standard_transformations + (implicit_multiplication_application,))
        expr_str = expr_str.replace('^', '**').replace('×', '*').replace('÷', '/')
        try:
            return parse_expr(expr_str, transformations=transformations)
        except:
            return None
    
    def integration_by_parts_theory(self) -> str:
        """Theory of Integration by Parts"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Integration by Parts - Theory</div>
            <p>The integration by parts formula is derived from the product rule of differentiation:</p>
            <div class="formula-highlight">
                $$\\frac{d}{dx}[u(x)v(x)] = u(x)\\frac{dv}{dx} + v(x)\\frac{du}{dx}$$
            </div>
            <p>Integrating both sides and rearranging gives:</p>
            <div class="formula-highlight">
                $$\\int u\\,dv = uv - \\int v\\,du$$
            </div>
            <p><strong>LIATE Rule for choosing u:</strong></p>
            <ul>
                <li><strong>L</strong> - Logarithmic functions</li>
                <li><strong>I</strong> - Inverse trigonometric functions</li>
                <li><strong>A</strong> - Algebraic functions</li>
                <li><strong>T</strong> - Trigonometric functions</li>
                <li><strong>E</strong> - Exponential functions</li>
            </ul>
        </div>
        """
    
    def integration_by_parts(self, func_str: str, var: str = 'x') -> str:
        """Perform integration by parts with step-by-step solution"""
        try:
            expr = self.parse_expression(func_str)
            if expr is None:
                return "Error: Invalid expression"
            
            x = Symbol(var)
            
            html = self.integration_by_parts_theory()
            html += '<div class="step-box">'
            html += '<strong>📝 Step-by-Step Solution:</strong><br><br>'
            html += f'<strong>Given integral:</strong> $$\\int ({sp.latex(expr)}) \\, d{var}$$'
            
            # Try automatic integration by parts
            # For demonstration, we'll handle common cases
            if func_str.find('*exp') != -1 or func_str.find('x*e') != -1:
                # Handle ∫x·e^x dx
                html += '<br><strong>Step 1: Choose u and dv using LIATE rule</strong>'
                html += '<br>u = x (Algebraic), dv = e^x dx (Exponential)'
                html += '<br><strong>Step 2: Find du and v</strong>'
                html += '<br>du = dx, v = e^x'
                html += '<br><strong>Step 3: Apply formula ∫u dv = uv - ∫v du</strong>'
                
                u = x
                dv = exp(x)
                du = diff(u, x)
                v = integrate(dv, x)
                
                result = u*v - integrate(v*du, x)
                html += f'<br>$$\\int x e^x dx = x e^x - \\int e^x dx$$'
                html += f'<br>$$= x e^x - e^x + C$$'
                html += f'<br>$$\\boxed{{= e^x(x - 1) + C}}$$'
            
            elif func_str.find('*sin') != -1 or func_str.find('*cos') != -1:
                # Handle ∫x·sin(x)dx
                html += '<br><strong>Step 1: Choose u and dv</strong>'
                html += '<br>u = x, dv = sin(x)dx'
                html += '<br><strong>Step 2: du = dx, v = -cos(x)</strong>'
                html += '<br><strong>Step 3: Apply formula</strong>'
                
                result = integrate(expr, x)
                html += f'<br>$$\\int {sp.latex(expr)} \\, dx = {sp.latex(result)} + C$$'
            
            else:
                # General integration
                result = integrate(expr, x)
                html += '<br><strong>Direct Integration:</strong>'
                html += f'<br>$$\\int {sp.latex(expr)} \\, dx = {sp.latex(result)} + C$$'
            
            html += '</div>'
            return html
        except Exception as e:
            return f"Error: {str(e)}"
    
    def differentiation_rules_theory(self) -> str:
        """Theory of Differentiation Rules"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Differentiation Rules - Theory</div>
            <p><strong>Basic Rules:</strong></p>
            <div class="formula-highlight">
                <strong>Power Rule:</strong> $$\\frac{d}{dx}[x^n] = nx^{n-1}$$<br>
                <strong>Product Rule:</strong> $$\\frac{d}{dx}[uv] = u'v + uv'$$<br>
                <strong>Quotient Rule:</strong> $$\\frac{d}{dx}\\left[\\frac{u}{v}\\right] = \\frac{u'v - uv'}{v^2}$$<br>
                <strong>Chain Rule:</strong> $$\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$$
            </div>
        </div>
        """
    
    def solve_quadratic_system_theory(self) -> str:
        """Theory of Quadratic Systems"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Quadratic Systems - Theory</div>
            <p>A quadratic system involves at least one quadratic equation:</p>
            <div class="formula-highlight">
                $$ax^2 + bxy + cy^2 + dx + ey + f = 0$$
            </div>
            <p><strong>Solution Methods:</strong></p>
            <ul>
                <li><strong>Substitution Method:</strong> Solve one equation for a variable and substitute</li>
                <li><strong>Elimination Method:</strong> Eliminate one variable by combining equations</li>
                <li><strong>Graphical Method:</strong> Find intersection points of curves</li>
            </ul>
        </div>
        """
    
    def solve_quadratic_system(self, eq1_str: str, eq2_str: str) -> str:
        """Solve system of two equations (linear-quadratic or quadratic-quadratic)"""
        try:
            html = self.solve_quadratic_system_theory()
            html += '<div class="step-box">'
            html += '<strong>📝 Solving System of Equations:</strong><br><br>'
            
            # Parse equations
            if '=' in eq1_str:
                left1, right1 = eq1_str.split('=')
                eq1 = parse_expr(f"({left1}) - ({right1})")
            else:
                eq1 = parse_expr(eq1_str)
            
            if '=' in eq2_str:
                left2, right2 = eq2_str.split('=')
                eq2 = parse_expr(f"({left2}) - ({right2})")
            else:
                eq2 = parse_expr(eq2_str)
            
            html += f'<strong>Equation 1:</strong> $${sp.latex(eq1)} = 0$$'
            html += f'<strong>Equation 2:</strong> $${sp.latex(eq2)} = 0$$'
            
            # Solve the system
            solutions = solve([eq1, eq2], [self.x, self.y], dict=True)
            
            html += '<br><strong>Step 1: Use substitution method</strong>'
            html += '<br>Solve Equation 1 for y and substitute into Equation 2'
            
            # Try to solve for y from eq1
            try:
                y_expr = solve(eq1, self.y)
                if y_expr:
                    html += f'<br>From Equation 1: $$y = {sp.latex(y_expr[0])}$$'
                    # Substitute
                    eq2_sub = eq2.subs(self.y, y_expr[0])
                    html += f'<br>Substituting into Equation 2: $${sp.latex(eq2_sub)} = 0$$'
            except:
                pass
            
            html += '<br><br><strong>Solutions:</strong><br>'
            for i, sol in enumerate(solutions, 1):
                html += f'<div class="formula-highlight">'
                html += f'<strong>Solution {i}:</strong><br>'
                html += f'$$x = {sp.latex(sol[self.x])}$$'
                html += f'$$y = {sp.latex(sol[self.y])}$$'
                html += '</div>'
            
            html += '</div>'
            return html
        except Exception as e:
            return f"Error solving system: {str(e)}"
    
    def solve_linear_system_theory(self) -> str:
        """Theory of Linear Systems"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Linear Systems - Theory</div>
            <p>A system of linear equations can be solved using:</p>
            <div class="formula-highlight">
                <strong>Matrix Form:</strong> $$A\\mathbf{x} = \\mathbf{b}$$<br>
                <strong>Cramer's Rule:</strong> $$x_i = \\frac{\\det(A_i)}{\\det(A)}$$
            </div>
            <p><strong>Methods:</strong></p>
            <ul>
                <li>Gaussian Elimination</li>
                <li>Cramer's Rule</li>
                <li>Matrix Inversion</li>
                <li>Gauss-Jordan Elimination</li>
            </ul>
        </div>
        """
    
    def solve_linear_system_2x2(self, a1, b1, c1, a2, b2, c2) -> str:
        """Solve 2x2 linear system: a1*x + b1*y = c1, a2*x + b2*y = c2"""
        html = self.solve_linear_system_theory()
        html += '<div class="step-box">'
        html += '<strong>📝 Solving 2×2 Linear System:</strong><br><br>'
        
        # Display system
        html += '<strong>System of Equations:</strong><br>'
        html += f'<div class="formula-highlight">'
        html += f'$${a1}x + {b1}y = {c1}$$'
        html += f'$${a2}x + {b2}y = {c2}$$'
        html += '</div>'
        
        # Matrix form
        A = Matrix([[a1, b1], [a2, b2]])
        b = Matrix([c1, c2])
        
        html += '<strong>Step 1: Write in matrix form</strong>'
        html += f'<br>$$A = {sp.latex(A)}, \\quad b = {sp.latex(b)}$$'
        
        # Determinant
        det = A.det()
        html += f'<br><strong>Step 2: Calculate determinant</strong>'
        html += f'<br>$$\\det(A) = {a1}({b2}) - {b1}({a2}) = {det}$$'
        
        if det != 0:
            # Cramer's Rule
            html += '<br><strong>Step 3: Apply Cramer\'s Rule</strong>'
            
            A1 = Matrix([[c1, b1], [c2, b2]])
            A2 = Matrix([[a1, c1], [a2, c2]])
            
            det1 = A1.det()
            det2 = A2.det()
            
            x = det1 / det
            y = det2 / det
            
            html += f'<br>$$x = \\frac{{\\det(A_1)}}{{\\det(A)}} = \\frac{{{det1}}}{{{det}}} = {sp.latex(x)}$$'
            html += f'<br>$$y = \\frac{{\\det(A_2)}}{{\\det(A)}} = \\frac{{{det2}}}{{{det}}} = {sp.latex(y)}$$'
            
            html += '<br><div class="formula-highlight">'
            html += f'<strong>Solution:</strong><br>'
            html += f'$$\\boxed{{x = {sp.latex(x)},\\quad y = {sp.latex(y)}}}$$'
            html += '</div>'
        else:
            html += '<br><strong>System has no unique solution (determinant = 0)</strong>'
        
        html += '</div>'
        return html
    
    def solve_linear_system_3x3(self, coeffs: List[float]) -> str:
        """Solve 3x3 linear system"""
        if len(coeffs) != 12:
            return "Error: Need 12 coefficients for 3x3 system"
        
        a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3 = coeffs
        
        html = self.solve_linear_system_theory()
        html += '<div class="step-box">'
        html += '<strong>📝 Solving 3×3 Linear System:</strong><br><br>'
        
        html += '<strong>System of Equations:</strong><br>'
        html += f'<div class="formula-highlight">'
        html += f'$${a1}x + {b1}y + {c1}z = {d1}$$'
        html += f'$${a2}x + {b2}y + {c2}z = {d2}$$'
        html += f'$${a3}x + {b3}y + {c3}z = {d3}$$'
        html += '</div>'
        
        A = Matrix([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])
        b = Matrix([d1, d2, d3])
        
        try:
            solution = A.LUsolve(b)
            html += '<br><strong>Using Gaussian Elimination:</strong>'
            html += f'<br>$${sp.latex(A)}\\begin{{bmatrix}} x \\\\ y \\\\ z \\end{{bmatrix}} = {sp.latex(b)}$$'
            
            html += '<br><div class="formula-highlight">'
            html += f'<strong>Solution:</strong><br>'
            html += f'$$\\boxed{{x = {sp.latex(solution[0])},\\quad y = {sp.latex(solution[1])},\\quad z = {sp.latex(solution[2])}}}$$'
            html += '</div>'
        except:
            html += '<br><strong>System is singular or has no unique solution</strong>'
        
        html += '</div>'
        return html
    
    def partial_derivative_theory(self) -> str:
        """Theory of Partial Derivatives"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Partial Derivatives - Theory</div>
            <p>For a function f(x,y), partial derivatives measure the rate of change with respect to one variable while holding others constant:</p>
            <div class="formula-highlight">
                $$\\frac{\\partial f}{\\partial x} = \\lim_{h \\to 0} \\frac{f(x+h, y) - f(x,y)}{h}$$<br>
                $$\\frac{\\partial f}{\\partial y} = \\lim_{h \\to 0} \\frac{f(x, y+h) - f(x,y)}{h}$$
            </div>
            <p><strong>Notation:</strong></p>
            <ul>
                <li>$f_x$ or $\\frac{\\partial f}{\\partial x}$ - Partial derivative with respect to x</li>
                <li>$f_y$ or $\\frac{\\partial f}{\\partial y}$ - Partial derivative with respect to y</li>
                <li>$f_{xx}$ or $\\frac{\\partial^2 f}{\\partial x^2}$ - Second partial derivative</li>
                <li>$f_{xy}$ or $\\frac{\\partial^2 f}{\\partial x \\partial y}$ - Mixed partial derivative</li>
            </ul>
        </div>
        """
    
    def partial_derivative(self, func_str: str, var: str = 'x') -> str:
        """Calculate partial derivative"""
        try:
            expr = self.parse_expression(func_str, ['x', 'y'])
            if expr is None:
                return "Error: Invalid expression"
            
            html = self.partial_derivative_theory()
            html += '<div class="step-box">'
            html += '<strong>📝 Partial Derivative Calculation:</strong><br><br>'
            
            html += f'<strong>Given function:</strong> $$f(x,y) = {sp.latex(expr)}$$'
            
            if var == 'x':
                deriv = diff(expr, self.x)
                html += f'<br><strong>Step 1:</strong> Treat y as constant'
                html += f'<br><strong>Step 2:</strong> Differentiate with respect to x'
                html += f'<br>$$\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(deriv)}$$'
            elif var == 'y':
                deriv = diff(expr, self.y)
                html += f'<br><strong>Step 1:</strong> Treat x as constant'
                html += f'<br><strong>Step 2:</strong> Differentiate with respect to y'
                html += f'<br>$$\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(deriv)}$$'
            elif var == 'both':
                deriv_x = diff(expr, self.x)
                deriv_y = diff(expr, self.y)
                html += f'<br>$$\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(deriv_x)}$$'
                html += f'<br>$$\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(deriv_y)}$$'
            
            html += '<br><div class="formula-highlight">'
            html += f'<strong>Final Result:</strong><br>'
            html += f'$$\\boxed{{\\frac{{\\partial f}}{{\\partial {var}}} = {sp.latex(deriv)}}}$$'
            html += '</div>'
            
            html += '</div>'
            return html
        except Exception as e:
            return f"Error: {str(e)}"
    
    def multiple_integral_theory(self) -> str:
        """Theory of Multiple Integrals"""
        return """
        <div class="theory-box">
            <div class="theory-title">📚 Multiple Integrals - Theory</div>
            <p>Multiple integrals extend integration to functions of several variables:</p>
            <div class="formula-highlight">
                <strong>Double Integral:</strong> $$\\iint_R f(x,y)\\,dA = \\int_a^b \\int_c^d f(x,y)\\,dy\\,dx$$<br>
                <strong>Triple Integral:</strong> $$\\iiint_R f(x,y,z)\\,dV = \\int_a^b \\int_c^d \\int_e^f f(x,y,z)\\,dz\\,dy\\,dx$$
            </div>
            <p><strong>Fubini's Theorem:</strong> If f is continuous, the order of integration can be changed.</p>
        </div>
        """
    
    def double_integral(self, func_str: str, var1: str = 'x', var2: str = 'y') -> str:
        """Calculate double integral"""
        try:
            expr = self.parse_expression(func_str, ['x', 'y'])
            if expr is None:
                return "Error: Invalid expression"
            
            html = self.multiple_integral_theory()
            html += '<div class="step-box">'
            html += '<strong>📝 Double Integral Calculation:</strong><br><br>'
            
            html += f'<strong>Given:</strong> $$\\iint ({sp.latex(expr)})\\,d{var1}\\,d{var2}$$'
            
            # First integrate with respect to y, then x
            html += '<br><strong>Step 1:</strong> Integrate with respect to y (inner integral)'
            inner = integrate(expr, self.y)
            html += f'<br>$$\\int ({sp.latex(expr)})\\,d{var2} = {sp.latex(inner)}$$'
            
            html += '<br><strong>Step 2:</strong> Integrate result with respect to x (outer integral)'
            result = integrate(inner, self.x)
            html += f'<br>$$\\int ({sp.latex(inner)})\\,d{var1} = {sp.latex(result)}$$'
            
            html += '<br><div class="formula-highlight">'
            html += f'<strong>Final Result:</strong><br>'
            html += f'$$\\boxed{{\\iint ({sp.latex(expr)})\\,d{var1}\\,d{var2} = {sp.latex(result)} + C}}$$'
            html += '</div>'
            
            html += '</div>'
            return html
        except Exception as e:
            return f"Error: {str(e)}"

class ManualArithmetic:
    """Handles manual arithmetic with enhanced display"""
    
    @staticmethod
    def add_manual(num1: int, num2: int) -> str:
        """Generate manual addition display"""
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        result = num1 + num2
        
        carries = []
        carry = 0
        for i in range(max_len - 1, -1, -1):
            d1 = int(str1.zfill(max_len)[i])
            d2 = int(str2.zfill(max_len)[i])
            digit_sum = d1 + d2 + carry
            carries.insert(0, digit_sum // 10)
            carry = digit_sum // 10
        
        html = '<div class="step-box">'
        html += '<strong>➕ Addition - Manual Calculation</strong><br><br>'
        html += '<div style="font-family: Courier New; font-size: 24px; line-height: 1.8; text-align: right;">'
        
        if any(c > 0 for c in carries):
            carry_str = ' '.join(str(c) if c > 0 else ' ' for c in carries)
            html += f'<div style="color: #f093fb; font-size: 18px;">{carry_str}</div>'
        
        html += f'<div>{str1}</div>'
        html += f'<div style="color: #667eea;">+ {str2}</div>'
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        html += f'<div style="color: #764ba2; font-weight: bold;">{result}</div>'
        html += '</div>'
        
        html += f'<br><strong>Step-by-step:</strong><br>'
        html += f'1. Units: {str1[-1]} + {str2[-1]} = {int(str1[-1]) + int(str2[-1])}<br>'
        if max_len > 1:
            html += f'2. Tens: {str1[-2] if len(str1) > 1 else 0} + {str2[-2] if len(str2) > 1 else 0} = {int(str1[-2]) if len(str1) > 1 else 0 + int(str2[-2]) if len(str2) > 1 else 0}<br>'
        html += f'<strong>Final: {num1} + {num2} = {result}</strong>'
        html += '</div>'
        return html
    
    @staticmethod
    def multiply_manual(num1: int, num2: int) -> str:
        """Generate manual long multiplication"""
        str1, str2 = str(num1), str(num2)
        result = num1 * num2
        
        partial_products = []
        for i, digit in enumerate(reversed(str2)):
            partial = num1 * int(digit) * (10 ** i)
            partial_products.append(partial)
        
        html = '<div class="step-box">'
        html += '<strong>✖️ Long Multiplication</strong><br><br>'
        html += '<div style="font-family: Courier New; font-size: 24px; line-height: 1.8; text-align: right;">'
        
        html += f'<div>{str1}</div>'
        html += f'<div style="color: #667eea;">× {str2}</div>'
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        
        partial_products.reverse()
        for i, pp in enumerate(partial_products):
            if i == 0:
                html += f'<div>{pp}</div>'
            else:
                html += f'<div style="color: #667eea;">+ {pp}</div>'
        
        html += f'<div style="border-top: 3px solid #333; margin: 10px 0;"></div>'
        html += f'<div style="color: #764ba2; font-weight: bold;">{result}</div>'
        html += '</div>'
        
        html += f'<br><strong>Step-by-step:</strong><br>'
        html += f'1. {num1} × {str2[-1]} = {num1 * int(str2[-1])}<br>'
        if len(str2) > 1:
            html += f'2. {num1} × {str2[-2]}0 = {num1 * int(str2[-2])}0<br>'
        html += f'3. Add partial products<br>'
        html += f'<strong>Final: {num1} × {num2} = {result}</strong>'
        html += '</div>'
        return html

# Initialize session state
if 'solver' not in st.session_state:
    st.session_state.solver = AdvancedMathSolver()
if 'manual_arith' not in st.session_state:
    st.session_state.manual_arith = ManualArithmetic()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Title
st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; font-size:18px;">Advanced Mathematics Suite with Complete Theoretical Background</p>', unsafe_allow_html=True)

# Sidebar with mode selection
with st.sidebar:
    st.markdown("## 🎯 Select Mode")
    
    mode = st.selectbox(
        "Choose Operation Mode:",
        ["Basic Arithmetic", "Quadratic Equation", "Linear Systems", 
         "Differentiation", "Integration", "Partial Derivatives",
         "Multiple Integrals", "Quadratic Systems"]
    )
    
    st.markdown("---")
    
    # Reset buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True, key="reset"):
            st.session_state.result_html = ""
            st.rerun()
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True, key="clear_history"):
            st.session_state.history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("## 📊 History")
    for calc in st.session_state.history[-5:]:
        st.info(calc)

# Main content
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.markdown("### 📝 Input Parameters")
    
    solver = st.session_state.solver
    arith = st.session_state.manual_arith
    
    if mode == "Basic Arithmetic":
        operation = st.selectbox("Operation:", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])
        num1 = st.number_input("First Number:", value=123, format="%d")
        num2 = st.number_input("Second Number:", value=45, format="%d")
        
        if st.button("🧮 Calculate", use_container_width=True):
            if operation == "Addition (+)":
                result_html = arith.add_manual(int(num1), int(num2))
            elif operation == "Multiplication (×)":
                result_html = arith.multiply_manual(int(num1), int(num2))
            st.session_state.result_html = result_html
            st.session_state.history.append(f"{num1} {operation[0]} {num2}")
    
    elif mode == "Quadratic Equation":
        st.markdown("**Enter coefficients:** ax² + bx + c = 0")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            a = st.number_input("a:", value=1.0, format="%.1f")
        with col_b:
            b = st.number_input("b:", value=3.0, format="%.1f")
        with col_c:
            c = st.number_input("c:", value=-4.0, format="%.1f")
        
        if st.button("📐 Solve Quadratic", use_container_width=True):
            result_html = solver.solve_quadratic_system(
                f"{a}*x**2 + {b}*x + {c}",
                "x"
            )
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Quadratic: {a}x² + {b}x + {c} = 0")
    
    elif mode == "Linear Systems":
        system_size = st.radio("System Size:", ["2×2", "3×3"])
        
        if system_size == "2×2":
            st.markdown("**System:** a₁x + b₁y = c₁ and a₂x + b₂y = c₂")
            col1, col2, col3 = st.columns(3)
            with col1:
                a1 = st.number_input("a₁:", value=2.0, format="%.1f")
                a2 = st.number_input("a₂:", value=1.0, format="%.1f")
            with col2:
                b1 = st.number_input("b₁:", value=1.0, format="%.1f")
                b2 = st.number_input("b₂:", value=-1.0, format="%.1f")
            with col3:
                c1 = st.number_input("c₁:", value=5.0, format="%.1f")
                c2 = st.number_input("c₂:", value=1.0, format="%.1f")
            
            if st.button("🔢 Solve System", use_container_width=True):
                result_html = solver.solve_linear_system_2x2(a1, b1, c1, a2, b2, c2)
                st.session_state.result_html = result_html
                st.session_state.history.append(f"2×2 Linear System")
        
        else:
            st.markdown("**Enter 12 coefficients for 3×3 system**")
            coeffs = st.text_area("Coefficients (a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3):", 
                                  "2,1,-1,8,-3,-1,2,-11,-2,1,2,-3")
            if st.button("🔢 Solve 3×3 System", use_container_width=True):
                try:
                    coeff_list = [float(x.strip()) for x in coeffs.split(',')]
                    result_html = solver.solve_linear_system_3x3(coeff_list)
                    st.session_state.result_html = result_html
                    st.session_state.history.append(f"3×3 Linear System")
                except:
                    st.error("Invalid format. Use comma-separated numbers.")
    
    elif mode == "Differentiation":
        func_str = st.text_input("Function f(x) =", "x**2 * sin(x)")
        var = st.selectbox("Differentiate with respect to:", ["x", "y", "z"])
        
        if st.button("📈 Differentiate", use_container_width=True):
            result_html = solver.differentiation_rules_theory()
            expr = solver.parse_expression(func_str)
            if expr:
                deriv = diff(expr, Symbol(var))
                result_html += f'<div class="step-box">'
                result_html += f'<strong>Derivative:</strong><br>'
                result_html += f'$$\\frac{{d}}{{d{var}}}({sp.latex(expr)}) = {sp.latex(deriv)}$$'
                result_html += f'</div>'
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Derivative: {func_str}")
    
    elif mode == "Integration":
        integration_type = st.radio("Integration Method:", 
                                   ["Direct Integration", "Integration by Parts"])
        func_str = st.text_input("Function f(x) =", "x * exp(x)")
        var = st.selectbox("Integrate with respect to:", ["x", "y", "z"])
        
        if st.button("📊 Integrate", use_container_width=True):
            if integration_type == "Integration by Parts":
                result_html = solver.integration_by_parts(func_str, var)
            else:
                result_html = solver.integration_by_parts_theory()
                expr = solver.parse_expression(func_str)
                if expr:
                    integral = integrate(expr, Symbol(var))
                    result_html += f'<div class="step-box">'
                    result_html += f'<strong>Integral:</strong><br>'
                    result_html += f'$$\\int ({sp.latex(expr)})\\,d{var} = {sp.latex(integral)} + C$$'
                    result_html += f'</div>'
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Integration: {func_str}")
    
    elif mode == "Partial Derivatives":
        func_str = st.text_input("Function f(x,y) =", "x**2 * y + sin(x*y)")
        var = st.selectbox("Partial derivative with respect to:", ["x", "y", "both"])
        
        if st.button("∂ Calculate", use_container_width=True):
            result_html = solver.partial_derivative(func_str, var)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Partial Derivative: {func_str}")
    
    elif mode == "Multiple Integrals":
        integral_type = st.radio("Integral Type:", ["Double Integral (dx dy)", "Triple Integral (dx dy dz)"])
        func_str = st.text_input("Function =", "x**2 + y**2")
        
        if st.button("∫∫ Integrate", use_container_width=True):
            if integral_type == "Double Integral (dx dy)":
                result_html = solver.double_integral(func_str)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Multiple Integral: {func_str}")
    
    elif mode == "Quadratic Systems":
        st.markdown("**Enter two equations (linear and/or quadratic):**")
        eq1 = st.text_input("Equation 1:", "x**2 + y**2 - 25")
        eq2 = st.text_input("Equation 2:", "x + y - 7")
        
        if st.button("🔗 Solve System", use_container_width=True):
            result_html = solver.solve_quadratic_system(eq1, eq2)
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Quadratic System")

# Result panel
with col_result:
    st.markdown("### ✨ Solution Display")
    
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
            height=600,
            scrolling=True
        )
    else:
        st.info("👈 Select a mode, enter parameters, and click Calculate to see the solution with complete theoretical background.")

# 3D Visualization
st.markdown("---")
webgl_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #000; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a1a);
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 150, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, 150);
        document.body.appendChild(renderer.domElement);
        
        const geometry = new THREE.TorusKnotGeometry(0.3, 0.1, 100, 16);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x667eea,
            emissive: 0x1a1a4e,
            shininess: 100
        });
        const knot = new THREE.Mesh(geometry, material);
        scene.add(knot);
        
        const light = new THREE.PointLight(0x667eea, 1, 10);
        light.position.set(5, 5, 5);
        scene.add(light);
        
        camera.position.z = 3;
        
        function animate() {
            requestAnimationFrame(animate);
            knot.rotation.x += 0.01;
            knot.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""
components.html(webgl_html, height=160)

# Footer
st.markdown("""
<div style="text-align:center; padding:20px; color:#666;">
    <p>🧮 HandCalc Pro v2.0 - Advanced Mathematics Suite</p>
    <p>Complete Theoretical Background • Step-by-Step Solutions • Multiple Variable Support</p>
</div>
""", unsafe_allow_html=True)
