# app.py - UPDATED with elegant manual calculation display
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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Cormorant+Garamond:wght@400;600;700&display=swap');
    
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .number-display {
        font-size: 42px;
        font-family: 'Playfair Display', serif;
        padding: 25px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        text-align: right;
        color: #e94560;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(233, 69, 96, 0.3);
        letter-spacing: 2px;
    }
    
    .manual-calc-container {
        background: linear-gradient(145deg, #0f0c29, #302b63, #24243e);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .manual-calc-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(233, 69, 96, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
    
    .manual-calc-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        color: #e94560;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .calculation-lines {
        font-family: 'Cormorant Garamond', serif;
        font-size: 28px;
        color: #ffffff;
        line-height: 1.8;
        text-align: right;
        padding: 30px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 20px;
        border: 1px solid rgba(233, 69, 96, 0.2);
        position: relative;
        z-index: 1;
        letter-spacing: 1px;
        backdrop-filter: blur(10px);
    }
    
    .calculation-line {
        padding: 5px 15px;
        transition: all 0.3s ease;
        border-radius: 5px;
    }
    
    .calculation-line:hover {
        background: rgba(233, 69, 96, 0.1);
    }
    
    .operator-symbol {
        color: #e94560;
        font-weight: 700;
        font-size: 32px;
    }
    
    .result-line {
        color: #4ade80;
        font-weight: 700;
        font-size: 34px;
        text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);
    }
    
    .separator-line {
        color: rgba(233, 69, 96, 0.6);
        letter-spacing: 2px;
    }
    
    .step-number {
        color: #e94560;
        font-size: 18px;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .carry-number {
        color: #fbbf24;
        font-size: 24px;
        font-style: italic;
    }
    
    .title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #e94560 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 56px;
        font-weight: bold;
        font-family: 'Playfair Display', serif;
        text-shadow: none;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 18px;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
    }
    
    /* Elegant input fields */
    .stTextInput > div > div > input {
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(233, 69, 96, 0.3);
        border-radius: 15px;
        color: white;
        padding: 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 15px;
    }
    
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: white;
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

class LongArithmeticCalculator:
    def __init__(self):
        self.steps = []
    
    def _create_separator(self, length: int) -> str:
        return "─" * length
    
    def _format_number(self, num: float) -> str:
        if num == int(num):
            return str(int(num))
        formatted = f"{num:.6f}"
        formatted = formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
        return formatted
    
    def add(self, a: str, b: str) -> str:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 + num2
            
            if num1 == int(num1) and num2 == int(num2):
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                max_len = max(len(str1), len(str2))
                str1 = str1.zfill(max_len)
                str2 = str2.zfill(max_len)
                
                # Calculate carries
                carries = []
                carry = 0
                for i in range(max_len - 1, -1, -1):
                    d1 = int(str1[i])
                    d2 = int(str2[i])
                    sum_d = d1 + d2 + carry
                    carries.insert(0, sum_d // 10)
                    carry = sum_d // 10
                
                result_str = str(int(result))
                total_width = max(max_len, len(result_str)) + 4
                
                formatted_steps = []
                
                # Show carries if any exist
                if any(carries):
                    carry_display = " ".join(str(c) if c > 0 else " " for c in carries)
                    formatted_steps.append({
                        'text': carry_display,
                        'type': 'carry',
                        'align': 'right'
                    })
                
                # First number
                formatted_steps.append({
                    'text': " ".join(str1),
                    'type': 'number',
                    'align': 'right'
                })
                
                # Operator and second number
                formatted_steps.append({
                    'text': "+ " + " ".join(str2),
                    'type': 'operation',
                    'align': 'right'
                })
                
                # Separator
                formatted_steps.append({
                    'text': self._create_separator(max(len(str1), len(str2)) * 2 + 2),
                    'type': 'separator',
                    'align': 'right'
                })
                
                # Result
                formatted_steps.append({
                    'text': " ".join(result_str),
                    'type': 'result',
                    'align': 'right'
                })
                
                self.steps = formatted_steps
            else:
                self.steps = [{'text': f"{a} + {b} = {self._format_number(result)}", 'type': 'simple', 'align': 'center'}]
            
            return self._format_number(result)
        except:
            return "Error"
    
    def subtract(self, a: str, b: str) -> str:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 - num2
            
            if num1 == int(num1) and num2 == int(num2):
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                max_len = max(len(str1), len(str2))
                str1 = str1.zfill(max_len)
                str2 = str2.zfill(max_len)
                
                result_str = str(int(result)).zfill(max_len)
                
                formatted_steps = []
                
                # First number
                formatted_steps.append({
                    'text': " ".join(str1),
                    'type': 'number',
                    'align': 'right'
                })
                
                # Operator and second number
                formatted_steps.append({
                    'text': "- " + " ".join(str2),
                    'type': 'operation',
                    'align': 'right'
                })
                
                # Separator
                formatted_steps.append({
                    'text': self._create_separator(max(len(str1), len(str2)) * 2 + 2),
                    'type': 'separator',
                    'align': 'right'
                })
                
                # Result
                formatted_steps.append({
                    'text': " ".join(result_str),
                    'type': 'result',
                    'align': 'right'
                })
                
                self.steps = formatted_steps
            else:
                self.steps = [{'text': f"{a} - {b} = {self._format_number(result)}", 'type': 'simple', 'align': 'center'}]
            
            return self._format_number(result)
        except:
            return "Error"
    
    def multiply(self, a: str, b: str) -> str:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 * num2
            
            if num1 == int(num1) and num2 == int(num2) and num1 != 0 and num2 != 0:
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                # Calculate partial products
                partial_products = []
                for i, digit in enumerate(reversed(str2)):
                    partial = int1 * int(digit)
                    partial_products.append((partial, i))
                
                result_str = str(int(result))
                max_width = max(len(str1), len(str2) + 1)
                
                formatted_steps = []
                
                # Show carries for multiplication
                formatted_steps.append({
                    'text': f"({len(str2)})",
                    'type': 'carry',
                    'align': 'right'
                })
                
                # First number
                formatted_steps.append({
                    'text': "  " + "  ".join(str1),
                    'type': 'number',
                    'align': 'right'
                })
                
                # Operator and second number
                formatted_steps.append({
                    'text': "× " + "  ".join(str2),
                    'type': 'operation',
                    'align': 'right'
                })
                
                # Separator
                formatted_steps.append({
                    'text': self._create_separator(max(len(str1), len(str2)) * 3 + 2),
                    'type': 'separator',
                    'align': 'right'
                })
                
                # Partial products
                for partial, shift in reversed(partial_products):
                    partial_str = str(partial)
                    if shift == 0:
                        formatted_steps.append({
                            'text': "  " + "  ".join(partial_str),
                            'type': 'partial',
                            'align': 'right'
                        })
                    else:
                        # Add zeros for shift
                        shifted = partial_str + "0" * shift
                        formatted_steps.append({
                            'text': "+ " + "  ".join(shifted),
                            'type': 'partial_sum',
                            'align': 'right'
                        })
                
                # Final separator
                formatted_steps.append({
                    'text': self._create_separator(max_width * 3 + 2),
                    'type': 'separator',
                    'align': 'right'
                })
                
                # Result
                formatted_steps.append({
                    'text': "  " + "  ".join(result_str),
                    'type': 'result',
                    'align': 'right'
                })
                
                self.steps = formatted_steps
            else:
                self.steps = [{'text': f"{a} × {b} = {self._format_number(result)}", 'type': 'simple', 'align': 'center'}]
            
            return self._format_number(result)
        except:
            return "Error"
    
    def divide(self, a: str, b: str) -> str:
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            
            if num2 == 0:
                self.steps = [{'text': "Error: Division by zero!", 'type': 'error', 'align': 'center'}]
                return "Error"
            
            result = num1 / num2
            result_str = self._format_number(result)
            
            if num1 == int(num1) and num2 == int(num2) and num1 >= num2:
                dividend = int(num1)
                divisor = int(num2)
                quotient = dividend // divisor
                remainder = dividend % divisor
                
                formatted_steps = []
                
                formatted_steps.append({
                    'text': f"    {quotient}",
                    'type': 'result',
                    'align': 'left'
                })
                formatted_steps.append({
                    'text': f"{divisor} ) {dividend}",
                    'type': 'number',
                    'align': 'left'
                })
                formatted_steps.append({
                    'text': f"    {divisor * quotient}",
                    'type': 'partial',
                    'align': 'left'
                })
                formatted_steps.append({
                    'text': "    " + self._create_separator(len(str(dividend))),
                    'type': 'separator',
                    'align': 'left'
                })
                formatted_steps.append({
                    'text': f"    {remainder}",
                    'type': 'partial_sum',
                    'align': 'left'
                })
                
                self.steps = formatted_steps
            else:
                self.steps = [{'text': f"{a} ÷ {b} = {result_str}", 'type': 'simple', 'align': 'center'}]
            
            return result_str
        except:
            return "Error"
    
    def square_root(self, num: str) -> str:
        self.steps = []
        try:
            value = float(num)
            if value < 0:
                self.steps = [{'text': "Error: Cannot calculate square root of negative number!", 'type': 'error', 'align': 'center'}]
                return "Error"
            
            result = math.sqrt(value)
            result_str = self._format_number(result)
            
            formatted_steps = []
            formatted_steps.append({
                'text': f"√{num} = {result_str}",
                'type': 'result',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "Newton's Method:",
                'type': 'title',
                'align': 'center'
            })
            
            if value > 0:
                x0 = value / 2
                formatted_steps.append({
                    'text': f"x₀ = {self._format_number(x0)}",
                    'type': 'step',
                    'align': 'center'
                })
                
                for i in range(1, 4):
                    x1 = (x0 + value / x0) / 2
                    formatted_steps.append({
                        'text': f"x{i} = ({self._format_number(x0)} + {num}/{self._format_number(x0)})/2 = {self._format_number(x1)}",
                        'type': 'step',
                        'align': 'center'
                    })
                    x0 = x1
            
            self.steps = formatted_steps
            return result_str
        except:
            return "Error"
    
    def cube_root(self, num: str) -> str:
        self.steps = []
        try:
            value = float(num)
            result = value ** (1/3)
            result_str = self._format_number(result)
            
            formatted_steps = []
            formatted_steps.append({
                'text': f"∛{num} = {result_str}",
                'type': 'result',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "Approximation Steps:",
                'type': 'title',
                'align': 'center'
            })
            
            if value != 0:
                x0 = value / 3
                formatted_steps.append({
                    'text': f"x₀ = {self._format_number(x0)}",
                    'type': 'step',
                    'align': 'center'
                })
                
                for i in range(1, 4):
                    x1 = (2 * x0 + value / (x0 * x0)) / 3
                    formatted_steps.append({
                        'text': f"x{i} = (2·{self._format_number(x0)} + {num}/{self._format_number(x0)}²)/3 = {self._format_number(x1)}",
                        'type': 'step',
                        'align': 'center'
                    })
                    x0 = x1
            
            self.steps = formatted_steps
            return result_str
        except:
            return "Error"
    
    def rule_of_three(self, a: str, b: str, c: str) -> str:
        self.steps = []
        try:
            val1 = float(a)
            val2 = float(b)
            val3 = float(c)
            result = (val2 * val3) / val1
            result_str = self._format_number(result)
            
            formatted_steps = []
            formatted_steps.append({
                'text': "Rule of Three",
                'type': 'title',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"{a} ⟶ {b}",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"{c} ⟶ x",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"x = ({b} × {c}) ÷ {a}",
                'type': 'operation',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"x = {self._format_number(val2 * val3)} ÷ {a}",
                'type': 'operation',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"x = {result_str}",
                'type': 'result',
                'align': 'center'
            })
            
            self.steps = formatted_steps
            return result_str
        except:
            return "Error"
    
    def integrate(self, expression: str, lower: str, upper: str, intervals: int = 100) -> str:
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
            
            formatted_steps = []
            formatted_steps.append({
                'text': f"∫ {expression} dx from {lower} to {upper}",
                'type': 'title',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"Trapezoidal Rule with {intervals} intervals",
                'type': 'subtitle',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"h = ({upper} - {lower})/{intervals} = {self._format_number(h)}",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"f({lower}) = {self._format_number(f(a))}",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"f({upper}) = {self._format_number(f(b))}",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"Result ≈ {result_str}",
                'type': 'result',
                'align': 'center'
            })
            
            self.steps = formatted_steps
            return result_str
        except:
            return "Error"
    
    def derivative(self, expression: str, point: str) -> str:
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
            
            formatted_steps = []
            formatted_steps.append({
                'text': f"d/dx ({expression}) at x = {point}",
                'type': 'title',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "",
                'type': 'empty',
                'align': 'center'
            })
            formatted_steps.append({
                'text': "Central Difference Method:",
                'type': 'subtitle',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"f'({point}) ≈ [f({self._format_number(x+h)}) - f({self._format_number(x-h)})] / (2·{h})",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"f'({point}) ≈ ({self._format_number(f_plus)} - {self._format_number(f_minus)}) / {self._format_number(2*h)}",
                'type': 'step',
                'align': 'center'
            })
            formatted_steps.append({
                'text': f"f'({point}) ≈ {result_str}",
                'type': 'result',
                'align': 'center'
            })
            
            self.steps = formatted_steps
            return result_str
        except:
            return "Error"

# Initialize session state
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
st.markdown('<h1 class="title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Elegant Manual Arithmetic • Watch Calculations Come Alive</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <h2 style='color: #e94560; font-family: "Playfair Display", serif; text-align: center;'>
            🎯 Operations
        </h2>
    """, unsafe_allow_html=True)
    
    operation = st.radio(
        "Select Operation:",
        ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)",
         "Square Root (√)", "Cube Root (∛)", "Rule of Three", "Integration (∫)", "Derivative (d/dx)"],
        key="op_select"
    )
    
    st.markdown("---")
    st.markdown("""
        <h3 style='color: #e94560; font-family: "Playfair Display", serif; text-align: center;'>
            📊 History
        </h3>
    """, unsafe_allow_html=True)
    
    for calc in st.session_state.history[-5:]:
        st.code(calc, language='text')

# Main layout
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("""
        <h3 style='color: #e94560; font-family: "Playfair Display", serif;'>
            📝 Input Numbers
        </h3>
    """, unsafe_allow_html=True)
    
    num3 = ""
    
    if operation in ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]:
        num1 = st.text_input("First Number:", key="input_num1", value="5" if operation == "Addition (+)" else "")
        num2 = st.text_input("Second Number:", key="input_num2", value="6" if operation == "Addition (+)" else "")
        
    elif operation in ["Square Root (√)", "Cube Root (∛)"]:
        num1 = st.text_input("Number:", key="input_num1", value="25" if operation == "Square Root (√)" else "")
        num2 = ""
        
    elif operation == "Rule of Three":
        num1 = st.text_input("Value A:", key="input_num1", value="10")
        num2 = st.text_input("Value B:", key="input_num2", value="20")
        num3 = st.text_input("Value C:", key="input_num3", value="30")
        
    elif operation in ["Integration (∫)", "Derivative (d/dx)"]:
        st.markdown("<p style='color: #fbbf24; font-style: italic;'>Currently using f(x) = x²</p>", unsafe_allow_html=True)
        num1 = st.text_input("Lower bound / Point:", key="input_num1", value="0")
        if operation == "Integration (∫)":
            num2 = st.text_input("Upper bound:", key="input_num2", value="10")
        else:
            num2 = ""
    
    col_calc, col_clear = st.columns(2)
    with col_calc:
        if st.button("✨ Calculate", use_container_width=True):
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
                
                # Add to history
                if operation == "Rule of Three":
                    history_entry = f"{num1} : {num2} :: {num3} : {result}"
                elif num2:
                    history_entry = f"{num1} {st.session_state.operation} {num2} = {result}"
                else:
                    history_entry = f"{st.session_state.operation}{num1} = {result}"
                
                st.session_state.history.append(history_entry)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col_clear:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.result = None
            st.session_state.steps = []
            st.rerun()

with col2:
    st.markdown("""
        <h3 style='color: #e94560; font-family: "Playfair Display", serif; text-align: center;'>
            📐 Manual Calculation
        </h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.result is not None:
        # Result display
        st.markdown(f'<div class="number-display">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        # Manual calculation steps
        if st.session_state.steps:
            st.markdown('<div class="manual-calc-container">', unsafe_allow_html=True)
            st.markdown('<div class="manual-calc-title">✦ Step by Step Resolution ✦</div>', unsafe_allow_html=True)
            st.markdown('<div class="calculation-lines">', unsafe_allow_html=True)
            
            for step in st.session_state.steps:
                if isinstance(step, dict):
                    step_type = step.get('type', 'simple')
                    text = step.get('text', '')
                    
                    if step_type == 'carry':
                        st.markdown(f'<div class="calculation-line"><span class="carry-number">{text}</span></div>', unsafe_allow_html=True)
                    elif step_type == 'number':
                        st.markdown(f'<div class="calculation-line">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'operation':
                        st.markdown(f'<div class="calculation-line"><span class="operator-symbol">{text[0]}</span> {text[1:]}</div>', unsafe_allow_html=True)
                    elif step_type == 'separator':
                        st.markdown(f'<div class="calculation-line separator-line">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'result':
                        st.markdown(f'<div class="calculation-line result-line">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'partial':
                        st.markdown(f'<div class="calculation-line" style="color: #fbbf24;">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'partial_sum':
                        st.markdown(f'<div class="calculation-line" style="color: #60a5fa;">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'title':
                        st.markdown(f'<div class="calculation-line" style="color: #e94560; font-size: 26px; font-weight: bold;">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'subtitle':
                        st.markdown(f'<div class="calculation-line" style="color: #fbbf24; font-size: 22px;">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'step':
                        st.markdown(f'<div class="calculation-line" style="color: #94a3b8;">{text}</div>', unsafe_allow_html=True)
                    elif step_type == 'error':
                        st.markdown(f'<div class="calculation-line" style="color: #ef4444;">{text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="calculation-line">{text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="calculation-line">{step}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Placeholder
        st.markdown("""
            <div class="manual-calc-container">
                <div class="manual-calc-title">✦ Ready to Calculate ✦</div>
                <div class="calculation-lines">
                    <div class="calculation-line" style="color: #94a3b8; text-align: center; font-style: italic;">
                        Enter numbers and click Calculate<br>
                        to see the magic unfold...
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# WebGL 3D Visualization
st.markdown("---")
st.markdown("""
    <h3 style='color: #e94560; font-family: "Playfair Display", serif; text-align: center;'>
        🌐 3D Mathematical Visualization
    </h3>
""", unsafe_allow_html=True)

webgl_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #0f0c29; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f0c29);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 250, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, 250);
        document.body.appendChild(renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        scene.add(ambientLight);
        
        const pointLight1 = new THREE.PointLight(0xe94560, 1, 10);
        pointLight1.position.set(3, 3, 3);
        scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0x667eea, 1, 10);
        pointLight2.position.set(-3, -1, -2);
        scene.add(pointLight2);
        
        // Create elegant geometric shapes
        const symbols = ['+', '−', '×', '÷', '=', '√', '∫', '∂', '∑', '∏', '∞', 'π'];
        const objects = [];
        
        symbols.forEach((symbol, index) => {
            // Mix of different geometries
            let geometry;
            const random = Math.random();
            
            if (random < 0.3) {
                geometry = new THREE.TorusGeometry(0.25, 0.08, 16, 32);
            } else if (random < 0.6) {
                geometry = new THREE.OctahedronGeometry(0.3);
            } else if (random < 0.8) {
                geometry = new THREE.IcosahedronGeometry(0.25);
            } else {
                geometry = new THREE.TorusKnotGeometry(0.2, 0.06, 64, 8);
            }
            
            const material = new THREE.MeshPhongMaterial({ 
                color: new THREE.Color(`hsl(${index * 30}, 70%, 60%)`),
                emissive: new THREE.Color(`hsl(${index * 30}, 70%, 15%)`),
                shininess: 100,
                specular: 0x444444,
                transparent: true,
                opacity: 0.8
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.x = (Math.random() - 0.5) * 12;
            mesh.position.y = (Math.random() - 0.5) * 4;
            mesh.position.z = (Math.random() - 0.5) * 6;
            
            mesh.userData = {
                speed: Math.random() * 0.015 + 0.005,
                rotationSpeed: Math.random() * 0.02 + 0.005,
                amplitude: Math.random() * 1.5 + 0.5,
                offset: Math.random() * Math.PI * 2,
                initialY: mesh.position.y
            };
            
            scene.add(mesh);
            objects.push(mesh);
        });
        
        // Add floating particles
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 200;
        const posArray = new Float32Array(particlesCount * 3);
        
        for (let i = 0; i < particlesCount * 3; i += 3) {
            posArray[i] = (Math.random() - 0.5) * 15;
            posArray[i + 1] = (Math.random() - 0.5) * 8;
            posArray[i + 2] = (Math.random() - 0.5) * 10;
        }
        
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.02,
            color: 0xe94560,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });
        
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);
        
        camera.position.z = 6;
        camera.position.y = 1;
        
        function animate() {
            requestAnimationFrame(animate);
            
            objects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.7;
                obj.rotation.z += obj.userData.rotationSpeed * 0.3;
                
                obj.position.y = obj.userData.initialY + 
                    Math.sin(Date.now() * obj.userData.speed + obj.userData.offset) * obj.userData.amplitude;
            });
            
            particles.rotation.y += 0.0005;
            particles.rotation.x += 0.0003;
            
            camera.rotation.y += 0.001;
            camera.position.y += Math.sin(Date.now() * 0.0005) * 0.003;
            
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

components.html(webgl_html, height=270)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: #e94560; font-family: 'Playfair Display', serif; font-size: 24px;">
        ✦ HandCalc Pro ✦
    </p>
    <p style="color: rgba(255, 255, 255, 0.5); font-family: 'Cormorant Garamond', serif; font-style: italic;">
        Elegant Mathematics • Manual Precision • Timeless Beauty
    </p>
</div>
""", unsafe_allow_html=True)
