# app.py - FIXED VERSION with 1150x700 pixels and no scrollbars
import streamlit as st
import streamlit.components.v1 as components
import math
from typing import List, Tuple
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="HandCalc Pro - Manual Arithmetic Visualizer",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Force 1150x700 viewport and remove scrollbars
st.markdown("""
<style>
    /* Remove scrollbars completely */
    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        overflow: hidden !important;
        max-height: 100vh !important;
        max-width: 100vw !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remove sidebar scrollbar */
    [data-testid="stSidebar"] {
        overflow: hidden !important;
    }
    
    /* Hide scrollbar for all elements */
    * {
        -ms-overflow-style: none !important;
        scrollbar-width: none !important;
    }
    
    *::-webkit-scrollbar {
        display: none !important;
    }
    
    /* Main container styling */
    .stApp {
        max-width: 1150px !important;
        max-height: 700px !important;
        margin: 0 auto !important;
        padding: 10px !important;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    /* Title styling */
    .title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px !important;
        font-weight: bold;
        margin: 5px 0 !important;
        padding: 0 !important;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 12px !important;
        margin: 0 0 10px 0 !important;
        padding: 0 !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 35px !important;
        font-size: 14px !important;
        font-weight: bold;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: transform 0.2s ease;
        padding: 0 10px !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    
    /* Number display */
    .number-display {
        font-size: 24px !important;
        font-family: 'Courier New', monospace;
        padding: 10px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        text-align: right;
        color: white;
        margin: 5px 0 !important;
    }
    
    /* Manual calculation display */
    .manual-calc {
        font-family: 'Courier New', monospace;
        font-size: 14px !important;
        padding: 10px !important;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-height: 300px !important;
        overflow: hidden !important;
    }
    
    /* Compact columns */
    [data-testid="column"] {
        padding: 5px !important;
    }
    
    /* Radio buttons compact */
    .stRadio > div {
        padding: 2px 0 !important;
    }
    
    .stRadio label {
        font-size: 13px !important;
        padding: 3px 0 !important;
    }
    
    /* Text inputs compact */
    .stTextInput > div > div > input {
        font-size: 13px !important;
        padding: 5px 10px !important;
        height: 30px !important;
    }
    
    /* Sidebar compact */
    [data-testid="stSidebar"] {
        min-width: 200px !important;
        max-width: 200px !important;
        padding: 10px !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 12px !important;
    }
    
    /* History code blocks */
    .stCode {
        font-size: 11px !important;
        padding: 5px !important;
        margin: 2px 0 !important;
    }
    
    /* Section headers */
    h3 {
        font-size: 16px !important;
        margin: 5px 0 !important;
        padding: 0 !important;
    }
    
    /* Plotly chart container */
    .js-plotly-plot, .plot-container {
        max-height: 200px !important;
    }
    
    /* WebGL canvas container */
    iframe {
        height: 150px !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 10px !important;
        margin: 5px 0 0 0 !important;
        padding: 0 !important;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Pure Python Calculator Engine
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
                visual.append("+" + " " * (total_width - len(str2) - 1) + str2)
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(result_str)) + result_str)
                self.steps = visual
            else:
                total_width = max(len(a), len(b) + 1, len(self._format_number(result))) + 2
                visual = []
                visual.append(" " * (total_width - len(a)) + a)
                visual.append("+" + " " * (total_width - len(b) - 1) + b)
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
            visual.append("-" + " " * (total_width - len(str2) - 1) + str2)
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
                visual.append("×" + " " * (total_width - len(str2) - 1) + str2)
                visual.append(self._create_line(total_width))
                
                partial_products.reverse()
                for i, pp in enumerate(partial_products):
                    pp_str = str(pp)
                    if i == 0:
                        visual.append(" " * (total_width - len(pp_str)) + pp_str)
                    else:
                        visual.append("+" + " " * (total_width - len(pp_str) - 1) + pp_str)
                
                visual.append(self._create_line(total_width))
                visual.append(" " * (total_width - len(result_str)) + result_str)
                self.steps = visual
            else:
                total_width = max(len(a), len(b) + 1, len(self._format_number(result))) + 2
                visual = []
                visual.append(" " * (total_width - len(a)) + a)
                visual.append("×" + " " * (total_width - len(b) - 1) + b)
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
                visual.append(f"Step 0: {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (x0 + value / x0) / 2
                    visual.append(f"Step {i}: {self._format_number(x1)}")
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
                visual.append(f"Step 0: {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (2 * x0 + value / (x0 * x0)) / 3
                    visual.append(f"Step {i}: {self._format_number(x1)}")
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
            visual.append(f"{a} → {b}")
            visual.append(f"{c} → x")
            visual.append(f"x = ({b} × {c}) ÷ {a}")
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
            visual.append(f"∫ x² dx [{lower}, {upper}]")
            visual.append(f"h = {self._format_number(h)}")
            visual.append(f"Result ≈ {result_str}")
            
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
            
            derivative = (f(x + h) - f(x - h)) / (2 * h)
            result_str = self._format_number(derivative)
            
            visual = []
            visual.append(f"d/dx (x²) at x = {point}")
            visual.append(f"f'({point}) ≈ {result_str}")
            
            self.steps = visual
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

# Title (compact)
st.markdown('<h1 class="title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Watch Manual Calculations Unfold Step by Step!</p>', unsafe_allow_html=True)

# Sidebar (compact)
with st.sidebar:
    st.markdown("### 🎯 Operations")
    operation = st.radio(
        "Select:",
        ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)",
         "Square Root (√)", "Cube Root (∛)", "Rule of Three", "Integration (∫)", 
         "Derivative (d/dx)"],
        key="op_select",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("#### 📊 History")
    for calc in st.session_state.history[-3:]:
        st.code(calc, language='text')

# Main layout with 3 columns
col1, col2, col3 = st.columns([3, 2, 4])

with col1:
    st.markdown("### 📝 Input")
    
    num3 = ""
    
    if operation in ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]:
        num1 = st.text_input("First Number:", key="input_num1", value="", 
                            placeholder="Enter number")
        num2 = st.text_input("Second Number:", key="input_num2", value="", 
                            placeholder="Enter number")
        
    elif operation in ["Square Root (√)", "Cube Root (∛)"]:
        num1 = st.text_input("Number:", key="input_num1", value="", 
                            placeholder="Enter number")
        num2 = ""
        
    elif operation == "Rule of Three":
        num1 = st.text_input("A:", key="input_num1", value="", placeholder="Value A")
        num2 = st.text_input("B:", key="input_num2", value="", placeholder="Value B")
        num3 = st.text_input("C:", key="input_num3", value="", placeholder="Value C")
        
    elif operation in ["Integration (∫)", "Derivative (d/dx)"]:
        st.markdown("*f(x) = x²*")
        num1 = st.text_input("Lower/Point:", key="input_num1", value="", 
                            placeholder="Enter value")
        if operation == "Integration (∫)":
            num2 = st.text_input("Upper bound:", key="input_num2", value="", 
                                placeholder="Enter value")
        else:
            num2 = ""
    
    col_calc, col_clear = st.columns(2)
    with col_calc:
        if st.button("🧮 Calculate", use_container_width=True):
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
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.result = None
            st.session_state.steps = []
            st.rerun()

with col2:
    st.markdown("### 🎨 Result")
    
    if st.session_state.result is not None:
        st.markdown(f'<div class="number-display">{st.session_state.result}</div>', 
                   unsafe_allow_html=True)
        
        try:
            values = []
            labels = []
            
            if 'input_num1' in st.session_state and st.session_state.input_num1:
                val1 = float(st.session_state.input_num1)
                values.append(val1)
                labels.append('A')
            
            if 'input_num2' in st.session_state and st.session_state.input_num2:
                val2 = float(st.session_state.input_num2)
                values.append(val2)
                labels.append('B')
            
            if 'input_num3' in st.session_state and st.session_state.input_num3:
                val3 = float(st.session_state.input_num3)
                values.append(val3)
                labels.append('C')
            
            if st.session_state.result and st.session_state.result != "Error":
                result_val = float(st.session_state.result)
                values.append(result_val)
                labels.append('Result')
            
            if values:
                fig = go.Figure(data=[
                    go.Bar(name='Values', x=labels, y=values,
                          marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe'][:len(values)])
                ])
                fig.update_layout(
                    title="Visualization",
                    template="plotly_dark",
                    height=180,
                    margin=dict(l=10, r=10, t=30, b=10),
                    font=dict(size=10)
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        except:
            pass

with col3:
    st.markdown("### 📐 Manual Steps")
    
    if st.session_state.steps:
        st.markdown('<div class="manual-calc">', unsafe_allow_html=True)
        for step in st.session_state.steps:
            st.code(step, language='text')
        st.markdown('</div>', unsafe_allow_html=True)

# WebGL 3D Visualization
st.markdown("---")
st.markdown("### 🌐 3D Calculator View")

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
        scene.background = new THREE.Color(0x1a1a2e);
        
        const camera = new THREE.PerspectiveCamera(75, 1100 / 120, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(1100, 120);
        document.body.appendChild(renderer.domElement);
        
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 5, 5);
        scene.add(directionalLight);
        
        const symbols = ['+', '-', '×', '÷', '=', '√', '∫', '∂', '0', '1', '2', '3'];
        const objects = [];
        
        symbols.forEach((symbol, index) => {
            const geometry = new THREE.TorusGeometry(0.25, 0.08, 16, 32);
            const material = new THREE.MeshPhongMaterial({ 
                color: new THREE.Color(`hsl(${index * 28}, 70%, 55%)`),
                emissive: new THREE.Color(`hsl(${index * 28}, 70%, 20%)`),
            });
            const torus = new THREE.Mesh(geometry, material);
            
            torus.position.x = (Math.random() - 0.5) * 8;
            torus.position.y = (Math.random() - 0.5) * 2;
            torus.position.z = (Math.random() - 0.5) * 3;
            
            torus.userData = {
                speed: Math.random() * 0.015 + 0.005,
                rotationSpeed: Math.random() * 0.02 + 0.005,
                offset: Math.random() * Math.PI * 2
            };
            
            scene.add(torus);
            objects.push(torus);
        });
        
        camera.position.z = 4;
        
        function animate() {
            requestAnimationFrame(animate);
            
            objects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.8;
                obj.position.y += Math.sin(Date.now() * obj.userData.speed + obj.userData.offset) * 0.003;
            });
            
            camera.rotation.y += 0.001;
            renderer.render(scene, camera);
        }
        
        animate();
    </script>
</body>
</html>
"""

components.html(webgl_html, height=120)

# Footer
st.markdown("""
<div class="footer">
    <p>🧮 HandCalc Pro v1.0 | Manual Arithmetic Visualizer | 2024</p>
</div>
""", unsafe_allow_html=True)
