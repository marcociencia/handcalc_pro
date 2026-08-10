# app.py - Complete version with LaTeX styling
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import symbols, diff, integrate, solve, latex, simplify, expand, factor
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import plotly.graph_objects as go
from typing import List, Tuple
import re

# Page configuration
st.set_page_config(
    page_title="HandCalc Pro - LaTeX Manual Arithmetic Visualizer",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Code+Pro:wght@400;600&display=swap');
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-family: 'Playfair Display', serif;
        text-align: center;
        color: #888;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    .manual-calc-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin: 20px 0;
        font-family: 'Latin Modern Math', 'Computer Modern', 'Times New Roman', serif;
    }
    
    .calc-line {
        font-family: 'Latin Modern Math', 'Computer Modern', monospace;
        font-size: 24px;
        padding: 5px 10px;
        line-height: 1.6;
        letter-spacing: 1px;
    }
    
    .operation-sign {
        color: #667eea;
        font-weight: bold;
    }
    
    .result-line {
        border-top: 3px solid #333;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
        color: #764ba2;
    }
    
    .carry-number {
        color: #f093fb;
        font-size: 18px;
        font-weight: bold;
        position: relative;
        top: -10px;
    }
    
    .step-number {
        color: #667eea;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .math-display {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    .function-input {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        transition: border-color 0.3s;
    }
    
    .function-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        font-weight: 700;
        color: #333;
        margin: 20px 0 10px 0;
        border-bottom: 2px solid #667eea;
        padding-bottom: 5px;
    }
    
    .history-item {
        background: white;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #764ba2;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    
    .stButton > button {
        width: 100%;
        height: 55px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .latex-render {
        background: white;
        border-radius: 10px;
        padding: 20px;
        font-size: 20px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

class ManualArithmetic:
    """Handles manual arithmetic display with LaTeX-style formatting"""
    
    @staticmethod
    def add_manual(num1: int, num2: int) -> str:
        """Generate manual addition display"""
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        result = num1 + num2
        result_str = str(result)
        
        # Calculate carries
        carries = []
        carry = 0
        str1_padded = str1.zfill(max_len)
        str2_padded = str2.zfill(max_len)
        
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(str1_padded[i]) + int(str2_padded[i]) + carry
            carries.insert(0, digit_sum // 10)
            carry = digit_sum // 10
        
        # Build HTML
        html = '<div class="manual-calc-container">'
        html += '<div class="section-title">➕ Addition - Step by Step</div>'
        
        # Show carries if any exist
        if any(c > 0 for c in carries):
            carry_str = ' '.join(str(c) if c > 0 else ' ' for c in carries)
            html += f'<div class="calc-line carry-number" style="text-align:right; padding-right:20px;">{carry_str}</div>'
        
        # Main numbers
        total_width = max_len + 4
        html += f'<div class="calc-line" style="text-align:right;">{"&nbsp;" * (total_width - len(str1))}{str1}</div>'
        html += f'<div class="calc-line operation-sign" style="text-align:right;">+ {"&nbsp;" * (total_width - len(str2) - 2)}{str2}</div>'
        html += f'<div class="calc-line" style="text-align:right;">{"─" * (total_width * 12)}</div>'
        html += f'<div class="calc-line result-line" style="text-align:right; color:#764ba2;">{"&nbsp;" * (total_width - len(result_str))}{result_str}</div>'
        
        # Explanation
        html += '<div class="math-display">'
        html += f'<strong>Step 1:</strong> Add units: {str1[-1]} + {str2[-1]} = {int(str1[-1]) + int(str2[-1])}'
        if len(str1) > 1 and len(str2) > 1:
            html += f'<br><strong>Step 2:</strong> Add tens: {str1[-2] if len(str1) > 1 else "0"} + {str2[-2] if len(str2) > 1 else "0"} = {int(str1[-2]) if len(str1) > 1 else 0 + int(str2[-2]) if len(str2) > 1 else 0}'
        html += f'<br><strong>Result:</strong> {num1} + {num2} = {result}'
        html += '</div></div>'
        
        return html
    
    @staticmethod
    def subtract_manual(num1: int, num2: int) -> str:
        """Generate manual subtraction display"""
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        result = num1 - num2
        result_str = str(result)
        
        html = '<div class="manual-calc-container">'
        html += '<div class="section-title">➖ Subtraction - Step by Step</div>'
        
        total_width = max_len + 4
        html += f'<div class="calc-line" style="text-align:right;">{"&nbsp;" * (total_width - len(str1))}{str1}</div>'
        html += f'<div class="calc-line operation-sign" style="text-align:right;">− {"&nbsp;" * (total_width - len(str2) - 2)}{str2}</div>'
        html += f'<div class="calc-line" style="text-align:right;">{"─" * (total_width * 12)}</div>'
        html += f'<div class="calc-line result-line" style="text-align:right; color:#764ba2;">{"&nbsp;" * (total_width - len(result_str))}{result_str}</div>'
        
        html += '<div class="math-display">'
        html += f'<strong>Explanation:</strong> Subtracting {num2} from {num1}<br>'
        html += f'<strong>Result:</strong> {num1} - {num2} = {result}'
        html += '</div></div>'
        
        return html
    
    @staticmethod
    def multiply_manual(num1: int, num2: int) -> str:
        """Generate manual long multiplication display"""
        str1, str2 = str(num1), str(num2)
        result = num1 * num2
        
        html = '<div class="manual-calc-container">'
        html += '<div class="section-title">✖️ Long Multiplication</div>'
        
        # Calculate partial products
        partial_products = []
        str2_reversed = str2[::-1]
        
        for i, digit in enumerate(str2_reversed):
            partial = num1 * int(digit) * (10 ** i)
            partial_products.append(partial)
        
        # Build display
        max_width = max(len(str1), len(str2) + 1) + 4
        result_str = str(result)
        
        html += f'<div class="calc-line" style="text-align:right;">{"&nbsp;" * (max_width - len(str1))}{str1}</div>'
        html += f'<div class="calc-line operation-sign" style="text-align:right;">× {"&nbsp;" * (max_width - len(str2) - 2)}{str2}</div>'
        html += f'<div class="calc-line" style="text-align:right;">{"─" * (max_width * 12)}</div>'
        
        # Show partial products
        partial_products.reverse()
        for i, partial in enumerate(partial_products):
            pp_str = str(partial)
            if i == 0:
                html += f'<div class="calc-line" style="text-align:right;">{"&nbsp;" * (max_width - len(pp_str))}{pp_str}</div>'
            else:
                html += f'<div class="calc-line operation-sign" style="text-align:right;">+ {"&nbsp;" * (max_width - len(pp_str) - 2)}{pp_str}</div>'
        
        html += f'<div class="calc-line" style="text-align:right;">{"─" * (max_width * 12)}</div>'
        html += f'<div class="calc-line result-line" style="text-align:right; color:#764ba2;">{"&nbsp;" * (max_width - len(result_str))}{result_str}</div>'
        
        # Explanation
        html += '<div class="math-display">'
        html += f'<strong>Step 1:</strong> Multiply {num1} × {str2[-1]} = {partial_products[-1]}<br>'
        if len(str2) > 1:
            html += f'<strong>Step 2:</strong> Multiply {num1} × {str2[-2]}0 = {partial_products[-2] if len(partial_products) > 1 else ""}<br>'
        html += f'<strong>Step 3:</strong> Add partial products: {result}'
        html += '</div></div>'
        
        return html
    
    @staticmethod
    def divide_manual(num1: int, num2: int) -> str:
        """Generate manual long division display"""
        if num2 == 0:
            return '<div class="manual-calc-container"><div class="section-title">Error: Division by zero!</div></div>'
        
        quotient = num1 // num2
        remainder = num1 % num2
        
        html = '<div class="manual-calc-container">'
        html += '<div class="section-title">➗ Long Division</div>'
        
        # Build long division format
        html += '<div style="font-family: monospace; font-size: 20px; padding: 20px;">'
        html += f'<div style="text-align:right;">{quotient}</div>'
        html += f'<div style="border-top: 2px solid black; display:inline-block;">{num2} ) {num1}</div><br>'
        html += f'<div style="text-align:right;">{num2 * quotient}</div>'
        html += f'<div style="border-top: 2px solid black;">{remainder}</div>'
        html += '</div>'
        
        html += '<div class="math-display">'
        html += f'<strong>Quotient:</strong> {quotient}<br>'
        html += f'<strong>Remainder:</strong> {remainder}<br>'
        html += f'<strong>Verification:</strong> {num2} × {quotient} + {remainder} = {num2 * quotient + remainder}'
        html += '</div></div>'
        
        return html

class FunctionSolver:
    """Handles function solving with LaTeX display"""
    
    def __init__(self):
        self.x, self.y = symbols('x y')
    
    def parse_function(self, func_str: str, variables: str = 'x') -> sp.Expr:
        """Parse function string to sympy expression"""
        transformations = (standard_transformations + (implicit_multiplication_application,))
        
        # Replace common notations
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('×', '*')
        func_str = func_str.replace('÷', '/')
        
        try:
            expr = parse_expr(func_str, transformations=transformations)
            return expr
        except:
            return None
    
    def solve_linear(self, equation: str) -> str:
        """Solve linear equation and return LaTeX formatted solution"""
        try:
            # Parse equation (format: "ax + b = c" or "ax + b")
            if '=' in equation:
                left, right = equation.split('=')
                expr = parse_expr(f"({left}) - ({right})")
            else:
                expr = parse_expr(equation)
            
            solution = solve(expr, self.x)
            
            html = '<div class="math-display">'
            html += '<div class="section-title">🔢 Equation Solution</div>'
            html += f'<div class="latex-render">\\({latex(expr)} = 0\\)</div>'
            html += '<div style="margin: 20px 0;">'
            html += '<strong>Solution Steps:</strong><br>'
            html += f'1. Original equation: \\({latex(expr)} = 0\\)<br>'
            html += f'2. Solve for x: \\(x = {latex(solution[0])}\\)<br>'
            html += f'3. Final answer: \\(\\boxed{{x = {latex(solution[0])}}}\\)'
            html += '</div></div>'
            
            return html
        except Exception as e:
            return f'<div class="math-display">Error solving equation: {str(e)}</div>'
    
    def solve_quadratic(self, a: float, b: float, c: float) -> str:
        """Solve quadratic equation ax² + bx + c = 0"""
        discriminant = b**2 - 4*a*c
        
        html = '<div class="math-display">'
        html += '<div class="section-title">📐 Quadratic Equation</div>'
        html += f'<div class="latex-render">\\({a}x^2 + {b}x + {c} = 0\\)</div>'
        
        html += '<div style="margin: 20px 0;">'
        html += '<strong>Using Quadratic Formula:</strong><br>'
        html += '\\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\)<br><br>'
        html += f'<strong>Step 1:</strong> Calculate discriminant<br>'
        html += f'\\(\\Delta = ({b})^2 - 4({a})({c}) = {discriminant}\\)<br><br>'
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            html += f'<strong>Step 2:</strong> Two real roots<br>'
            html += f'\\(x_1 = \\frac{{-{b} + \\sqrt{{{discriminant}}}}}{{2({a})}} = {x1:.4f}\\)<br>'
            html += f'\\(x_2 = \\frac{{-{b} - \\sqrt{{{discriminant}}}}}{{2({a})}} = {x2:.4f}\\)<br>'
            html += f'<strong>Final Answer:</strong> \\(\\boxed{{x = {x1:.4f} \\text{{ or }} x = {x2:.4f}}}\\)'
        elif discriminant == 0:
            x = -b / (2*a)
            html += f'<strong>Step 2:</strong> One real root (double)<br>'
            html += f'\\(x = \\frac{{-{b}}}{{2({a})}} = {x:.4f}\\)<br>'
            html += f'<strong>Final Answer:</strong> \\(\\boxed{{x = {x:.4f}}}\\)'
        else:
            real_part = -b / (2*a)
            imag_part = math.sqrt(-discriminant) / (2*a)
            html += f'<strong>Step 2:</strong> Complex roots<br>'
            html += f'\\(x = {real_part:.4f} \\pm {imag_part:.4f}i\\)<br>'
            html += f'<strong>Final Answer:</strong> \\(\\boxed{{x = {real_part:.4f} \\pm {imag_part:.4f}i}}\\)'
        
        html += '</div></div>'
        return html
    
    def derivative_display(self, func_str: str, var: str = 'x') -> str:
        """Calculate and display derivative steps"""
        try:
            expr = self.parse_function(func_str)
            if expr is None:
                return '<div class="math-display">Error: Invalid function</div>'
            
            deriv = diff(expr, self.x)
            
            html = '<div class="math-display">'
            html += '<div class="section-title">📈 Derivative Calculation</div>'
            html += f'<div class="latex-render">\\(f(x) = {latex(expr)}\\)</div>'
            
            html += '<div style="margin: 20px 0;">'
            html += '<strong>Solution Steps:</strong><br>'
            html += f'1. Original function: \\(f(x) = {latex(expr)}\\)<br>'
            html += f'2. Apply differentiation rules<br>'
            html += f'3. Result: \\(f\'(x) = {latex(deriv)}\\)<br>'
            html += f'<strong>Final Answer:</strong> \\(\\boxed{{f\'(x) = {latex(deriv)}}}\\)'
            html += '</div></div>'
            
            return html
        except Exception as e:
            return f'<div class="math-display">Error: {str(e)}</div>'
    
    def integral_display(self, func_str: str, var: str = 'x') -> str:
        """Calculate and display integral steps"""
        try:
            expr = self.parse_function(func_str)
            if expr is None:
                return '<div class="math-display">Error: Invalid function</div>'
            
            integral = integrate(expr, self.x)
            
            html = '<div class="math-display">'
            html += '<div class="section-title">📊 Integral Calculation</div>'
            html += f'<div class="latex-render">\\(\\int ({latex(expr)}) \\, dx\\)</div>'
            
            html += '<div style="margin: 20px 0;">'
            html += '<strong>Solution Steps:</strong><br>'
            html += f'1. Original integral: \\(\\int ({latex(expr)}) \\, dx\\)<br>'
            html += f'2. Apply integration rules<br>'
            html += f'3. Result: \\(\\int ({latex(expr)}) \\, dx = {latex(integral)} + C\\)<br>'
            html += f'<strong>Final Answer:</strong> \\(\\boxed{{\\int ({latex(expr)}) \\, dx = {latex(integral)} + C}}\\)'
            html += '</div></div>'
            
            return html
        except Exception as e:
            return f'<div class="math-display">Error: {str(e)}</div>'
    
    def function_analysis(self, func_str: str) -> str:
        """Complete function analysis with LaTeX display"""
        try:
            expr = self.parse_function(func_str)
            if expr is None:
                return '<div class="math-display">Error: Invalid function</div>'
            
            html = '<div class="math-display">'
            html += '<div class="section-title">📊 Function Analysis</div>'
            html += f'<div class="latex-render">\\(f(x) = {latex(expr)}\\)</div>'
            
            # Simplify
            simplified = simplify(expr)
            html += f'<strong>Simplified:</strong> \\(f(x) = {latex(simplified)}\\)<br>'
            
            # Expand
            expanded = expand(expr)
            html += f'<strong>Expanded:</strong> \\(f(x) = {latex(expanded)}\\)<br>'
            
            # Factor
            factored = factor(expr)
            html += f'<strong>Factored:</strong> \\(f(x) = {latex(factored)}\\)<br>'
            
            # Derivative
            deriv = diff(expr, self.x)
            html += f'<strong>Derivative:</strong> \\(f\'(x) = {latex(deriv)}\\)<br>'
            
            # Integral
            integral = integrate(expr, self.x)
            html += f'<strong>Integral:</strong> \\(\\int f(x) \\, dx = {latex(integral)} + C\\)<br>'
            
            html += '</div>'
            return html
        except Exception as e:
            return f'<div class="math-display">Error: {str(e)}</div>'

# Initialize components
if 'manual_arith' not in st.session_state:
    st.session_state.manual_arith = ManualArithmetic()
if 'func_solver' not in st.session_state:
    st.session_state.func_solver = FunctionSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Title
st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Elegant Manual Arithmetic & Function Solver with LaTeX Display</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Mode Selection")
    mode = st.radio(
        "Choose Mode:",
        ["📝 Basic Arithmetic", "📐 Functions & Algebra", "📈 Calculus"],
        key="mode_select"
    )
    
    st.markdown("---")
    st.markdown("## 📊 History")
    for calc in st.session_state.history[-5:]:
        st.markdown(f'<div class="history-item">{calc}</div>', unsafe_allow_html=True)

# Main content area
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.markdown("### 📝 Input Panel")
    
    if mode == "📝 Basic Arithmetic":
        operation = st.selectbox(
            "Operation:",
            ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]
        )
        
        st.markdown("#### Enter Numbers:")
        num1 = st.number_input("First Number:", value=123, key="num1", format="%d")
        num2 = st.number_input("Second Number:", value=45, key="num2", format="%d")
        
        if st.button("🧮 Calculate", use_container_width=True):
            arith = st.session_state.manual_arith
            result_html = ""
            
            if operation == "Addition (+)":
                result_html = arith.add_manual(int(num1), int(num2))
            elif operation == "Subtraction (-)":
                result_html = arith.subtract_manual(int(num1), int(num2))
            elif operation == "Multiplication (×)":
                result_html = arith.multiply_manual(int(num1), int(num2))
            elif operation == "Division (÷)":
                result_html = arith.divide_manual(int(num1), int(num2))
            
            st.session_state.result_html = result_html
            st.session_state.history.append(f"{num1} {operation[0]} {num2}")
    
    elif mode == "📐 Functions & Algebra":
        st.markdown("#### Enter Function or Equation:")
        st.markdown("*Examples: x^2 + 3*x - 4, 2*x + 5 = 15, sin(x) + cos(x)*")
        
        func_input = st.text_input("f(x) =", value="x^2 + 3*x - 4", key="func_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Analyze Function", use_container_width=True):
                solver = st.session_state.func_solver
                result_html = solver.function_analysis(func_input)
                st.session_state.result_html = result_html
                st.session_state.history.append(f"Analyze: {func_input}")
        
        with col2:
            if st.button("📐 Solve Quadratic", use_container_width=True):
                try:
                    # Parse coefficients
                    coeffs = st.text_input("Enter a, b, c (comma-separated):", "1, 3, -4")
                    a, b, c = map(float, coeffs.split(','))
                    solver = st.session_state.func_solver
                    result_html = solver.solve_quadratic(a, b, c)
                    st.session_state.result_html = result_html
                    st.session_state.history.append(f"Quadratic: {a}x² + {b}x + {c}")
                except:
                    st.error("Invalid coefficients format")
    
    elif mode == "📈 Calculus":
        st.markdown("#### Calculus Operations:")
        calc_operation = st.radio(
            "Select:",
            ["Derivative", "Integral", "Both"]
        )
        
        func_input = st.text_input("f(x) =", value="x^2 + 3*x", key="calc_input")
        
        if st.button("📊 Calculate", use_container_width=True):
            solver = st.session_state.func_solver
            result_html = ""
            
            if calc_operation in ["Derivative", "Both"]:
                result_html += solver.derivative_display(func_input)
                result_html += "<br>"
            
            if calc_operation in ["Integral", "Both"]:
                result_html += solver.integral_display(func_input)
            
            st.session_state.result_html = result_html
            st.session_state.history.append(f"Calculus: {func_input}")

# Result panel with elegant display
with col_result:
    st.markdown("### ✨ Manual Calculation Display")
    
    if st.session_state.result_html:
        st.components.v1.html(
            f"""
            <div style="max-height: 800px; overflow-y: auto; padding: 10px;">
                {st.session_state.result_html}
            </div>
            """,
            height=600,
            scrolling=True
        )
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px; color: #999;">
            <h3>🔮 Your solution will appear here</h3>
            <p>Enter values and click Calculate to see the magic!</p>
        </div>
        """, unsafe_allow_html=True)

# LaTeX rendering support
st.markdown("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
<script>
    MathJax.Hub.Config({
        tex2jax: {
            inlineMath: [['\\\\(', '\\\\)']],
            displayMath: [['\\\\[', '\\\\]']],
            processEscapes: true
        },
        "HTML-CSS": { 
            preferredFont: "TeX", 
            availableFonts: ["STIX","TeX"],
            scale: 100
        }
    });
</script>
""", unsafe_allow_html=True)

# 3D WebGL Background
st.markdown("---")
st.markdown("### 🌐 Mathematical Visualization")

webgl_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #000; overflow: hidden; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a1a);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 150, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, 150);
        document.body.appendChild(renderer.domElement);
        
        // Create mathematical symbols
        const symbols = ['∫', '∑', '∏', '√', '∞', '∂', '∇', '∆', 'π', 'θ', 'α', 'β', 'γ'];
        const objects = [];
        
        // Create particle system
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 200;
        const posArray = new Float32Array(particlesCount * 3);
        
        for(let i = 0; i < particlesCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 15;
        }
        
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        
        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.05,
            color: 0x667eea,
            blending: THREE.AdditiveBlending
        });
        
        const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particlesMesh);
        
        // Add geometric shapes
        symbols.forEach((symbol, index) => {
            const geometry = new THREE.IcosahedronGeometry(0.3, 1);
            const material = new THREE.MeshPhongMaterial({ 
                color: new THREE.Color(`hsl(${index * 27}, 70%, 60%)`),
                emissive: new THREE.Color(`hsl(${index * 27}, 70%, 20%)`),
                wireframe: true,
                transparent: true,
                opacity: 0.8
            });
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.x = (Math.random() - 0.5) * 10;
            mesh.position.y = (Math.random() - 0.5) * 4;
            mesh.position.z = (Math.random() - 0.5) * 5;
            
            mesh.userData = {
                speed: Math.random() * 0.01 + 0.005,
                rotationSpeed: Math.random() * 0.02 + 0.01,
                offset: Math.random() * Math.PI * 2
            };
            
            scene.add(mesh);
            objects.push(mesh);
        });
        
        // Lights
        const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
        scene.add(ambientLight);
        
        const pointLight1 = new THREE.PointLight(0x667eea, 1, 10);
        pointLight1.position.set(5, 3, 3);
        scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0xf093fb, 1, 10);
        pointLight2.position.set(-5, -2, -3);
        scene.add(pointLight2);
        
        camera.position.z = 6;
        camera.position.y = 1;
        
        function animate() {
            requestAnimationFrame(animate);
            
            objects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.7;
                obj.rotation.z += obj.userData.rotationSpeed * 0.5;
                obj.position.y += Math.sin(Date.now() * obj.userData.speed + obj.userData.offset) * 0.003;
            });
            
            particlesMesh.rotation.y += 0.0005;
            particlesMesh.rotation.x += 0.0002;
            
            pointLight1.intensity = 1 + Math.sin(Date.now() * 0.001) * 0.3;
            pointLight2.intensity = 1 + Math.cos(Date.now() * 0.001) * 0.3;
            
            camera.rotation.y += 0.001;
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / 150;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 150);
        });
    </script>
</body>
</html>
"""

components.html(webgl_html, height=160)

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p style="font-family: 'Playfair Display', serif; font-size: 18px;">
        🧮 HandCalc Pro - Where Mathematics Becomes Art
    </p>
    <p>Elegant manual calculations with LaTeX precision</p>
</div>
""", unsafe_allow_html=True)
