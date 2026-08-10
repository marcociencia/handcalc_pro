# app.py - VERSÃO COMPLETA ELEGANTE
import streamlit as st
import streamlit.components.v1 as components
import math
from typing import List, Tuple
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="HandCalc Pro - Manual Arithmetic Visualizer",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS SUPER ELEGANTE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Tema escuro elegante */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2b 100%);
    }
    
    /* Título principal */
    .main-title {
        text-align: center;
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(240, 147, 251, 0.8)); }
    }
    
    .subtitle {
        text-align: center;
        color: #a8b2d1;
        font-size: 18px;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }
    
    /* Botões estilosos */
    .stButton > button {
        width: 100%;
        height: 55px;
        font-size: 18px;
        font-weight: 700;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        border-color: rgba(240, 147, 251, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Display do resultado */
    .result-display {
        font-size: 48px;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-weight: 700;
        padding: 25px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        text-align: right;
        color: #fff;
        margin: 15px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
        letter-spacing: 3px;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Manual Calculation Card */
    .manual-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 2px 4px rgba(255, 255, 255, 0.05),
            inset 0 -2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .manual-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 50%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Linhas do cálculo manual */
    .calculation-line {
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 24px;
        color: #e0e0e0;
        padding: 8px 20px;
        margin: 2px 0;
        position: relative;
        z-index: 1;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    
    .calculation-line:hover {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 5px;
        transform: scale(1.02);
    }
    
    .operator-line {
        color: #f093fb;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(240, 147, 251, 0.5);
    }
    
    .result-line {
        color: #4facfe;
        font-weight: 700;
        font-size: 28px;
        text-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
    }
    
    .carry-line {
        color: #ffa500;
        font-size: 18px;
        font-style: italic;
        text-shadow: 0 0 8px rgba(255, 165, 0, 0.5);
    }
    
    /* Separador elegante */
    .divider-line {
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(102, 126, 234, 0.5) 20%, 
            rgba(240, 147, 251, 0.5) 50%, 
            rgba(102, 126, 234, 0.5) 80%, 
            transparent 100%);
        margin: 20px 0;
        position: relative;
    }
    
    .divider-line::before {
        content: '✦';
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        color: #f093fb;
        font-size: 20px;
        background: #1a1a2e;
        padding: 0 15px;
    }
    
    /* Section headers */
    .section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 700;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #e0e0e0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        padding: 15px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f093fb;
        box-shadow: 0 0 20px rgba(240, 147, 251, 0.3);
        background: rgba(26, 26, 46, 0.95);
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1a3e 100%);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(26, 26, 46, 0.5);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stRadio label {
        color: #a8b2d1 !important;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stRadio label:hover {
        color: #f093fb !important;
    }
    
    /* History items */
    .history-item {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        font-family: 'JetBrains Mono', monospace;
        color: #a8b2d1;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(240, 147, 251, 0.1);
        border-color: rgba(240, 147, 251, 0.3);
        transform: translateX(5px);
    }
    
    /* WebGL container */
    .webgl-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #a8b2d1;
        padding: 30px;
        font-size: 14px;
        letter-spacing: 1px;
    }
    
    /* Animation for manual calc */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .manual-card .calculation-line {
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .manual-card .calculation-line:nth-child(1) { animation-delay: 0.1s; }
    .manual-card .calculation-line:nth-child(2) { animation-delay: 0.2s; }
    .manual-card .calculation-line:nth-child(3) { animation-delay: 0.3s; }
    .manual-card .calculation-line:nth-child(4) { animation-delay: 0.4s; }
    .manual-card .calculation-line:nth-child(5) { animation-delay: 0.5s; }
    .manual-card .calculation-line:nth-child(6) { animation-delay: 0.6s; }
    .manual-card .calculation-line:nth-child(7) { animation-delay: 0.7s; }
    .manual-card .calculation-line:nth-child(8) { animation-delay: 0.8s; }
</style>
""", unsafe_allow_html=True)

# Pure Python Calculator Engine (MANTIDO IGUAL)
class LongArithmeticCalculator:
    def __init__(self):
        self.steps = []
    
    def _create_line(self, length: int) -> str:
        return "─" * length
    
    def _format_number(self, num: float) -> str:
        if num == int(num):
            return str(int(num))
        formatted = f"{num:.6f}"
        formatted = formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
        return formatted
    
    def add(self, a: str, b: str) -> Tuple[str, str]:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 + num2
            
            if num1 == int(num1) and num2 == int(num2):
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                max_len = max(len(str1), len(str2))
                result_str = str(int(result))
                total_width = max(max_len + 2, len(result_str)) + 2
                
                visual = []
                visual.append(" " * (total_width - len(str1)) + str1)
                visual.append("+ " + " " * (total_width - len(str2) - 2) + str2)
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(result_str)) + result_str)
                
                self.steps = visual
            else:
                total_width = max(len(a), len(b) + 1, len(self._format_number(result))) + 2
                visual = []
                visual.append(" " * (total_width - len(a)) + a)
                visual.append("+ " + " " * (total_width - len(b) - 2) + b)
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(self._format_number(result))) + self._format_number(result))
                self.steps = visual
            
            return self._format_number(result)
        except:
            return "Error"
    
    def subtract(self, a: str, b: str) -> Tuple[str, str]:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 - num2
            
            str1, str2 = a, b
            max_len = max(len(str1), len(str2))
            result_str = self._format_number(result)
            total_width = max(max_len + 2, len(result_str)) + 2
            
            visual = []
            visual.append(" " * (total_width - len(str1)) + str1)
            visual.append("- " + " " * (total_width - len(str2) - 2) + str2)
            visual.append(self._create_line(total_width))
            visual.append(" " * (total_width - len(result_str)) + result_str)
            
            self.steps = visual
            return self._format_number(result)
        except:
            return "Error"
    
    def multiply(self, a: str, b: str) -> Tuple[str, str]:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 * num2
            
            if num1 == int(num1) and num2 == int(num2) and num1 != 0 and num2 != 0:
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                partial_products = []
                for i, digit in enumerate(reversed(str2)):
                    partial = int1 * int(digit) * (10 ** i)
                    partial_products.append(partial)
                
                max_width = max(len(str1), len(str2) + 1)
                result_str = str(int(result))
                total_width = max(max_width + 2, len(result_str)) + 2
                
                visual = []
                visual.append(" " * (total_width - len(str1)) + str1)
                visual.append("× " + " " * (total_width - len(str2) - 2) + str2)
                visual.append(self._create_line(total_width))
                
                partial_products.reverse()
                for i, pp in enumerate(partial_products):
                    pp_str = str(pp)
                    if i == 0:
                        visual.append(" " * (total_width - len(pp_str)) + pp_str)
                    else:
                        visual.append("+ " + " " * (total_width - len(pp_str) - 2) + pp_str)
                
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(result_str)) + result_str)
                
                self.steps = visual
            else:
                total_width = max(len(a), len(b) + 1, len(self._format_number(result))) + 2
                visual = []
                visual.append(" " * (total_width - len(a)) + a)
                visual.append("× " + " " * (total_width - len(b) - 2) + b)
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(self._format_number(result))) + self._format_number(result))
                self.steps = visual
            
            return self._format_number(result)
        except:
            return "Error"
    
    def divide(self, a: str, b: str) -> Tuple[str, str]:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            
            if num2 == 0:
                self.steps = ["Error: Division by zero!"]
                return "Error"
            
            result = num1 / num2
            result_str = self._format_number(result)
            
            if num1 == int(num1) and num2 == int(num2) and num1 >= num2:
                dividend = int(num1)
                divisor = int(num2)
                quotient = dividend // divisor
                remainder = dividend % divisor
                
                visual = []
                visual.append(f"    {quotient}")
                visual.append(f"{divisor} ) {dividend}")
                visual.append(f"    {divisor * quotient}")
                visual.append("    " + self._create_line(len(str(dividend))))
                visual.append(f"    {remainder}")
                visual.append(f"\nResult: {result_str}")
                
                self.steps = visual
            else:
                visual = [f"{a} ÷ {b} = {result_str}"]
                self.steps = visual
            
            return result_str
        except:
            return "Error"
    
    def square_root(self, num: str) -> Tuple[str, str]:
        self.steps = []
        try:
            value = float(num)
            
            if value < 0:
                self.steps = ["Error: Cannot calculate square root of negative number!"]
                return "Error"
            
            result = math.sqrt(value)
            result_str = self._format_number(result)
            
            visual = [f"√{num} = {result_str}"]
            visual.append("")
            visual.append("Newton's Method:")
            
            if value > 0:
                x0 = value / 2
                visual.append(f"x₀ = {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (x0 + value / x0) / 2
                    visual.append(f"x{i} = {self._format_number(x1)}")
                    x0 = x1
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def cube_root(self, num: str) -> Tuple[str, str]:
        self.steps = []
        try:
            value = float(num)
            result = value ** (1/3)
            result_str = self._format_number(result)
            
            visual = [f"∛{num} = {result_str}"]
            visual.append("")
            visual.append("Approximation:")
            
            if value != 0:
                x0 = value / 3
                visual.append(f"x₀ = {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (2 * x0 + value / (x0 * x0)) / 3
                    visual.append(f"x{i} = {self._format_number(x1)}")
                    x0 = x1
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def rule_of_three(self, a: str, b: str, c: str) -> Tuple[str, str]:
        self.steps = []
        try:
            val1 = float(a)
            val2 = float(b)
            val3 = float(c)
            
            result = (val2 * val3) / val1
            result_str = self._format_number(result)
            
            visual = []
            visual.append("Rule of Three:")
            visual.append("")
            visual.append(f"{a}  →  {b}")
            visual.append(f"{c}  →  x")
            visual.append("")
            visual.append(f"x = ({b} × {c}) ÷ {a}")
            visual.append(f"x = {self._format_number(val2 * val3)} ÷ {a}")
            visual.append(f"x = {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def integrate(self, expression: str, lower: str, upper: str, intervals: int = 100) -> Tuple[str, str]:
        self.steps = []
        try:
            a = float(lower)
            b = float(upper)
            h = (b - a) / intervals
            
            def f(x):
                return x * x
            
            result = (f(a) + f(b)) / 2
            for i in range(1, intervals):
                result += f(a + i * h)
            result *= h
            
            result_str = self._format_number(result)
            
            visual = []
            visual.append(f"∫ {expression} dx from {lower} to {upper}")
            visual.append("")
            visual.append(f"h = {self._format_number(h)}")
            visual.append(f"f(a) = {self._format_number(f(a))}")
            visual.append(f"f(b) = {self._format_number(f(b))}")
            visual.append("")
            visual.append(f"∫ ≈ {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def derivative(self, expression: str, point: str) -> Tuple[str, str]:
        self.steps = []
        try:
            x = float(point)
            h = 0.0001
            
            def f(x):
                return x * x
            
            f_plus = f(x + h)
            f_minus = f(x - h)
            derivative = (f_plus - f_minus) / (2 * h)
            
            result_str = self._format_number(derivative)
            
            visual = []
            visual.append(f"d/dx ({expression}) at x = {point}")
            visual.append("")
            visual.append(f"f(x+h) = {self._format_number(f_plus)}")
            visual.append(f"f(x-h) = {self._format_number(f_minus)}")
            visual.append("")
            visual.append(f"f'(x) ≈ {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"

# Initialize calculator
if 'calc' not in st.session_state:
    st.session_state.calc = LongArithmeticCalculator()
if 'result' not in st.session_state:
    st.session_state.result = None
if 'operation' not in st.session_state:
    st.session_state.operation = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'steps' not in st.session_state:
    st.session_state.steps = []

# Title
st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Watch Calculations Come Alive - Step by Step ✨</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #667eea; font-size: 24px;">🎯 Operations</h2>
        </div>
    """, unsafe_allow_html=True)
    
    operation = st.radio(
        "Select Operation:",
        ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)",
         "Square Root (√)", "Cube Root (∛)", "Rule of Three", "Integration (∫)", "Derivative (d/dx)"],
        key="op_select",
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: #667eea; font-size: 20px;">📊 History</h3>
        </div>
    """, unsafe_allow_html=True)
    
    for calc in st.session_state.history[-5:]:
        st.markdown(f'<div class="history-item">📝 {calc}</div>', unsafe_allow_html=True)

# Main calculator interface
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown('<h3 class="section-title">📝 Input Values</h3>', unsafe_allow_html=True)
    
    num3 = ""
    
    if operation in ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]:
        num1 = st.text_input("First Number:", key="input_num1", value="", placeholder="Enter first number...")
        num2 = st.text_input("Second Number:", key="input_num2", value="", placeholder="Enter second number...")
        
    elif operation in ["Square Root (√)", "Cube Root (∛)"]:
        num1 = st.text_input("Number:", key="input_num1", value="", placeholder="Enter number...")
        num2 = ""
        
    elif operation == "Rule of Three":
        num1 = st.text_input("Value A:", key="input_num1", value="", placeholder="A → B")
        num2 = st.text_input("Value B:", key="input_num2", value="", placeholder="C → X")
        num3 = st.text_input("Value C:", key="input_num3", value="", placeholder="Find X")
        
    elif operation in ["Integration (∫)", "Derivative (d/dx)"]:
        st.info("💡 Currently supports f(x) = x² as example function")
        num1 = st.text_input("Lower bound / Point:", key="input_num1", value="", placeholder="Enter value...")
        if operation == "Integration (∫)":
            num2 = st.text_input("Upper bound:", key="input_num2", value="", placeholder="Enter upper bound...")
        else:
            num2 = ""
    
    col_calc, col_clear = st.columns(2)
    with col_calc:
        if st.button("🧮 Calculate", use_container_width=True, key="calc_button"):
            calc = st.session_state.calc
            result = "Error"
            
            try:
                if operation == "Addition (+)":
                    result = calc.add(num1, num2)
                    st.session_state.operation = "+"
                elif operation == "Subtraction (-)":
                    result = calc.subtract(num1, num2)
                    st.session_state.operation = "-"
                elif operation == "Multiplication (×)":
                    result = calc.multiply(num1, num2)
                    st.session_state.operation = "×"
                elif operation == "Division (÷)":
                    result = calc.divide(num1, num2)
                    st.session_state.operation = "÷"
                elif operation == "Square Root (√)":
                    result = calc.square_root(num1)
                    st.session_state.operation = "√"
                elif operation == "Cube Root (∛)":
                    result = calc.cube_root(num1)
                    st.session_state.operation = "∛"
                elif operation == "Rule of Three":
                    result = calc.rule_of_three(num1, num2, num3)
                    st.session_state.operation = "R3"
                elif operation == "Integration (∫)":
                    result = calc.integrate("x²", num1, num2)
                    st.session_state.operation = "∫"
                elif operation == "Derivative (d/dx)":
                    result = calc.derivative("x²", num1)
                    st.session_state.operation = "d/dx"
                
                st.session_state.result = result
                st.session_state.steps = calc.steps
                
                if num2 and num3:
                    history_entry = f"{num1} : {num2} :: {num3} : {result}"
                elif num2:
                    history_entry = f"{num1} {st.session_state.operation} {num2} = {result}"
                else:
                    history_entry = f"{st.session_state.operation}{num1} = {result}"
                
                st.session_state.history.append(history_entry)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_button"):
            st.session_state.result = None
            st.session_state.steps = []
            st.rerun()

with col2:
    st.markdown('<h3 class="section-title">✨ Result</h3>', unsafe_allow_html=True)
    
    if st.session_state.result is not None and st.session_state.result != "Error":
        st.markdown(f'<div class="result-display">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        try:
            values = []
            labels = []
            
            if 'input_num1' in st.session_state and st.session_state.input_num1:
                val1 = float(st.session_state.input_num1)
                values.append(val1)
                labels.append('Num1')
            
            if 'input_num2' in st.session_state and st.session_state.input_num2:
                val2 = float(st.session_state.input_num2)
                values.append(val2)
                labels.append('Num2')
            
            if 'input_num3' in st.session_state and st.session_state.input_num3:
                val3 = float(st.session_state.input_num3)
                values.append(val3)
                labels.append('Num3')
            
            if values:
                fig = go.Figure(data=[
                    go.Bar(
                        name='Values', 
                        x=labels, 
                        y=values,
                        marker=dict(
                            color=['#667eea', '#764ba2', '#f093fb', '#4facfe'][:len(values)],
                            line=dict(color='rgba(255, 255, 255, 0.2)', width=2)
                        ),
                        text=values,
                        textposition='auto',
                        textfont=dict(color='white', size=14)
                    )
                ])
                fig.update_layout(
                    title=dict(
                        text="Operation Visualization",
                        font=dict(color='#667eea', size=16)
                    ),
                    template="plotly_dark",
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
        except:
            pass
    elif st.session_state.result == "Error":
        st.error("⚠️ Invalid calculation")

with col3:
    st.markdown('<h3 class="section-title">📐 Manual Calculation</h3>', unsafe_allow_html=True)
    
    if st.session_state.steps:
        steps_html = '<div class="manual-card">'
        
        for i, step in enumerate(st.session_state.steps):
            # Adiciona classes diferentes baseado no tipo de linha
            if any(op in step for op in ['+', '-', '×', '÷']) and '──' not in step:
                css_class = 'calculation-line operator-line'
            elif '─' in step:
                css_class = 'calculation-line'
            elif any(word in step.lower() for word in ['result', 'error', '=']):
                css_class = 'calculation-line result-line'
            elif any(word in step for word in ['carry', 'x₀', 'x₁', 'x₂', 'x₃', 'Step']):
                css_class = 'calculation-line carry-line'
            else:
                css_class = 'calculation-line'
            
            # Escape HTML e preserva espaços
            step_escaped = step.replace(' ', '&nbsp;')
            steps_html += f'<div class="{css_class}">{step_escaped}</div>'
        
        steps_html += '</div>'
        st.markdown(steps_html, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="manual-card" style="text-align: center; color: #a8b2d1; padding: 40px;">
                <div style="font-size: 48px; margin-bottom: 15px;">📝</div>
                <div style="font-size: 18px;">Enter values and click Calculate</div>
                <div style="font-size: 14px; margin-top: 10px; color: #667eea;">to see the magic happen!</div>
            </div>
        """, unsafe_allow_html=True)

# WebGL 3D Calculator Visual
st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #667eea; font-size: 24px;">🌐 3D Visualization</h3>', unsafe_allow_html=True)

webgl_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            background: transparent; 
            overflow: hidden;
        }
        canvas { 
            display: block; 
            border-radius: 20px;
        }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 250, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true 
        });
        renderer.setSize(window.innerWidth, 250);
        renderer.setClearColor(0x000000, 0);
        document.body.appendChild(renderer.domElement);
        
        // Iluminação dramática
        const ambientLight = new THREE.AmbientLight(0x404066, 1.5);
        scene.add(ambientLight);
        
        const pointLight1 = new THREE.PointLight(0x667eea, 2, 10);
        pointLight1.position.set(5, 3, 5);
        scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0xf093fb, 2, 10);
        pointLight2.position.set(-5, -2, -3);
        scene.add(pointLight2);
        
        // Partículas de fundo
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
            blending: THREE.AdditiveBlending,
            transparent: true,
            opacity: 0.8
        });
        
        const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particlesMesh);
        
        // Símbolos matemáticos 3D
        const symbols = ['+', '−', '×', '÷', '=', '√', '∫', 'π', '∞', '∑'];
        const objects = [];
        
        symbols.forEach((symbol, index) => {
            // Criar geometria de torus para cada símbolo
            const geometry = new THREE.TorusKnotGeometry(0.4, 0.15, 64, 8, 2, 3);
            const material = new THREE.MeshStandardMaterial({ 
                color: new THREE.Color(`hsl(${index * 36}, 70%, 60%)`),
                emissive: new THREE.Color(`hsl(${index * 36}, 70%, 30%)`),
                metalness: 0.7,
                roughness: 0.3,
            });
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.x = (Math.random() - 0.5) * 12;
            mesh.position.y = (Math.random() - 0.5) * 4;
            mesh.position.z = (Math.random() - 0.5) * 8;
            
            mesh.userData = {
                speed: Math.random() * 0.01 + 0.005,
                rotationSpeed: Math.random() * 0.02 + 0.01,
                amplitude: Math.random() * 1.5 + 0.5,
                offset: Math.random() * Math.PI * 2,
                colorIndex: index
            };
            
            scene.add(mesh);
            objects.push(mesh);
        });
        
        // Grid elegante
        const gridHelper = new THREE.GridHelper(10, 20, 0x667eea, 0x1a1a3e);
        gridHelper.position.y = -3;
        scene.add(gridHelper);
        
        camera.position.z = 7;
        camera.position.y = 1;
        
        let clock = new THREE.Clock();
        
        function animate() {
            requestAnimationFrame(animate);
            
            const elapsedTime = clock.getElapsedTime();
            
            objects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.7;
                obj.rotation.z += obj.userData.rotationSpeed * 0.3;
                
                obj.position.y = Math.sin(elapsedTime * obj.userData.speed + obj.userData.offset) * obj.userData.amplitude;
                
                // Pulsação suave
                const scale = 1 + Math.sin(elapsedTime * 2 + obj.userData.offset) * 0.1;
                obj.scale.set(scale, scale, scale);
            });
            
            particlesMesh.rotation.y += 0.0005;
            particlesMesh.rotation.x += 0.0002;
            
            camera.rotation.y += 0.001;
            camera.position.y = 1 + Math.sin(elapsedTime * 0.3) * 0.5;
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / 250;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 250);
        });
    </script>
</body>
</html>
"""

st.markdown('<div class="webgl-container">', unsafe_allow_html=True)
components.html(webgl_html, height=270)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div style="font-size: 24px; margin-bottom: 10px;">🧮</div>
    <div style="font-weight: 700; font-size: 16px; color: #667eea;">HandCalc Pro v1.0</div>
    <div style="margin-top: 5px;">Manual Arithmetic Visualizer</div>
    <div style="margin-top: 10px; font-size: 12px; color: #666;">
        Made with ❤️ for Math Enthusiasts
    </div>
</div>
""", unsafe_allow_html=True)
