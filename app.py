# app.py - FIXED VERSION
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
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: transform 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .number-display {
        font-size: 32px;
        font-family: 'Courier New', monospace;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        text-align: right;
        color: white;
        margin: 10px 0;
    }
    .manual-calc {
        font-family: 'Courier New', monospace;
        font-size: 18px;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: bold;
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
        """Format number for display"""
        if num == int(num):
            return str(int(num))
        # Remove trailing zeros
        formatted = f"{num:.6f}"
        formatted = formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
        return formatted
    
    def add(self, a: str, b: str) -> Tuple[str, str]:
        """Addition with manual step-by-step"""
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 + num2
            
            # For integers, show column addition
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
                
                # Show carry if any
                carries = self._calculate_carries(int1, int2, '+')
                if carries:
                    carry_str = ''.join(str(c) if c > 0 else ' ' for c in carries)
                    visual.insert(0, " " * (total_width - len(carry_str)) + carry_str)
                
                self.steps = visual
            else:
                # For decimals
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
        """Subtraction with manual step-by-step"""
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
        """Multiplication with long multiplication process"""
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            result = num1 * num2
            
            # For integers, show long multiplication
            if num1 == int(num1) and num2 == int(num2) and num1 != 0 and num2 != 0:
                int1, int2 = int(num1), int(num2)
                str1, str2 = str(int1), str(int2)
                
                # Calculate partial products
                partial_products = []
                for i, digit in enumerate(reversed(str2)):
                    partial = int1 * int(digit) * (10 ** i)
                    partial_products.append(partial)
                
                # Build visual
                max_width = max(len(str1), len(str2) + 1)
                result_str = str(int(result))
                total_width = max(max_width + 2, len(result_str)) + 2
                
                visual = []
                visual.append(" " * (total_width - len(str1)) + str1)
                visual.append("×" + " " * (total_width - len(str2) - 1) + str2)
                visual.append(self._create_line(total_width))
                
                # Show partial products
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
                # For decimals or small numbers
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
        """Division with manual step-by-step"""
        self.steps = []
        try:
            num1 = float(a)
            num2 = float(b)
            
            if num2 == 0:
                self.steps = ["Error: Division by zero!"]
                return "Error"
            
            result = num1 / num2
            result_str = self._format_number(result)
            
            # Show long division for integers
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
        """Square root with Newton's method"""
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
            visual.append("Newton's Method Approximation:")
            
            if value > 0:
                x0 = value / 2
                visual.append(f"Step 0: Initial guess = {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (x0 + value / x0) / 2
                    visual.append(f"Step {i}: {self._format_number(x0)} → {self._format_number(x1)}")
                    x0 = x1
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def cube_root(self, num: str) -> Tuple[str, str]:
        """Cube root with approximation steps"""
        self.steps = []
        try:
            value = float(num)
            result = value ** (1/3)
            result_str = self._format_number(result)
            
            visual = [f"∛{num} = {result_str}"]
            visual.append("")
            visual.append("Approximation Steps:")
            
            if value != 0:
                x0 = value / 3
                visual.append(f"Step 0: Initial guess = {self._format_number(x0)}")
                
                for i in range(1, 4):
                    x1 = (2 * x0 + value / (x0 * x0)) / 3
                    visual.append(f"Step {i}: {self._format_number(x0)} → {self._format_number(x1)}")
                    x0 = x1
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def rule_of_three(self, a: str, b: str, c: str) -> Tuple[str, str]:
        """Rule of Three calculation"""
        self.steps = []
        try:
            val1 = float(a)
            val2 = float(b)
            val3 = float(c)
            
            result = (val2 * val3) / val1
            result_str = self._format_number(result)
            
            visual = []
            visual.append("Rule of Three (Direct Proportion):")
            visual.append("")
            visual.append(f"{a} ———→ {b}")
            visual.append(f"{c} ———→ x")
            visual.append("")
            visual.append(f"x = ({b} × {c}) ÷ {a}")
            visual.append(f"x = {self._format_number(val2 * val3)} ÷ {a}")
            visual.append(f"x = {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def integrate(self, expression: str, lower: str, upper: str, intervals: int = 100) -> Tuple[str, str]:
        """Numerical integration using trapezoidal rule"""
        self.steps = []
        try:
            a = float(lower)
            b = float(upper)
            h = (b - a) / intervals
            
            # Define function f(x) = x^2
            def f(x):
                return x * x
            
            # Trapezoidal rule
            result = (f(a) + f(b)) / 2
            for i in range(1, intervals):
                result += f(a + i * h)
            result *= h
            
            result_str = self._format_number(result)
            
            visual = []
            visual.append(f"Numerical Integration (Trapezoidal Rule)")
            visual.append(f"∫ {expression} dx from {lower} to {upper}")
            visual.append("")
            visual.append(f"Using {intervals} intervals")
            visual.append(f"Step size h = {self._format_number(h)}")
            visual.append("")
            visual.append(f"f({self._format_number(a)}) = {self._format_number(f(a))}")
            visual.append(f"f({self._format_number(b)}) = {self._format_number(f(b))}")
            visual.append(f"Sum of interior points = {self._format_number(result / h)}")
            visual.append("")
            visual.append(f"Result ≈ {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def derivative(self, expression: str, point: str) -> Tuple[str, str]:
        """Numerical derivative using central difference"""
        self.steps = []
        try:
            x = float(point)
            h = 0.0001
            
            # Define function f(x) = x^2
            def f(x):
                return x * x
            
            f_plus = f(x + h)
            f_minus = f(x - h)
            derivative = (f_plus - f_minus) / (2 * h)
            
            result_str = self._format_number(derivative)
            
            visual = []
            visual.append(f"Numerical Derivative")
            visual.append(f"d/dx ({expression}) at x = {point}")
            visual.append("")
            visual.append("Using central difference method:")
            visual.append(f"f'({self._format_number(x)}) ≈ [f({self._format_number(x + h)}) - f({self._format_number(x - h)})] / (2 × {h})")
            visual.append(f"f'({self._format_number(x)}) ≈ ({self._format_number(f_plus)} - {self._format_number(f_minus)}) / {self._format_number(2 * h)}")
            visual.append(f"f'({self._format_number(x)}) ≈ {result_str}")
            
            self.steps = visual
            return result_str
        except:
            return "Error"
    
    def _calculate_carries(self, num1: int, num2: int, operation: str) -> List[int]:
        """Calculate carries for addition/subtraction"""
        str1, str2 = str(num1), str(num2)
        max_len = max(len(str1), len(str2))
        str1 = str1.zfill(max_len)
        str2 = str2.zfill(max_len)
        
        carries = [0] * max_len
        carry = 0
        
        for i in range(max_len - 1, -1, -1):
            digit1 = int(str1[i])
            digit2 = int(str2[i])
            if operation == '+':
                sum_digits = digit1 + digit2 + carry
                carries[i] = sum_digits // 10
                carry = sum_digits // 10
        
        return carries

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
st.markdown('<h1 class="title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Manual Arithmetic Visualizer - Watch Calculations Unfold Step by Step!</p>', unsafe_allow_html=True)

# Sidebar for operation selection
with st.sidebar:
    st.markdown("## 🎯 Operations")
    operation = st.radio(
        "Select Operation:",
        ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)",
         "Square Root (√)", "Cube Root (∛)", "Rule of Three", "Integration (∫)", "Derivative (d/dx)"],
        key="op_select"
    )
    
    st.markdown("---")
    st.markdown("## 📊 History")
    for calc in st.session_state.history[-5:]:
        st.code(calc, language='text')

# Main calculator interface
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("### 📝 Input")
    
    num3 = ""
    
    if operation in ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]:
        num1 = st.text_input("First Number:", key="input_num1", value="")
        num2 = st.text_input("Second Number:", key="input_num2", value="")
        
    elif operation in ["Square Root (√)", "Cube Root (∛)"]:
        num1 = st.text_input("Number:", key="input_num1", value="")
        num2 = ""
        
    elif operation == "Rule of Three":
        num1 = st.text_input("Value A:", key="input_num1", value="")
        num2 = st.text_input("Value B:", key="input_num2", value="")
        num3 = st.text_input("Value C:", key="input_num3", value="")
        
    elif operation in ["Integration (∫)", "Derivative (d/dx)"]:
        st.markdown("**Note: Currently supports f(x) = x² as example**")
        num1 = st.text_input("Lower bound / Point:", key="input_num1", value="")
        if operation == "Integration (∫)":
            num2 = st.text_input("Upper bound:", key="input_num2", value="")
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
                
                # Add to history
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
    st.markdown("### 🎨 Visualization")
    
    if st.session_state.result is not None:
        st.markdown(f'<div class="number-display">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        # Create visualization
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
                    title="Operation Visualization",
                    template="plotly_dark",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        except:
            pass

with col3:
    st.markdown("### 📐 Manual Calculation")
    
    if st.session_state.steps:
        st.markdown('<div class="manual-calc">', unsafe_allow_html=True)
        for step in st.session_state.steps:
            st.code(step, language='text')
        st.markdown('</div>', unsafe_allow_html=True)

# WebGL 3D Calculator Visual
st.markdown("---")
st.markdown("### 🌐 WebGL 3D Calculator")

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
        scene.background = new THREE.Color(0x1a1a2e);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 200, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, 200);
        document.body.appendChild(renderer.domElement);
        
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 5, 5);
        scene.add(directionalLight);
        
        const symbols = ['+', '-', '×', '÷', '=', '√', '∫', '∂', '0', '1', '2', '3', '4'];
        const objects = [];
        
        symbols.forEach((symbol, index) => {
            const geometry = new THREE.TorusGeometry(0.3, 0.1, 16, 32);
            const material = new THREE.MeshPhongMaterial({ 
                color: new THREE.Color(`hsl(${index * 27}, 70%, 50%)`),
                emissive: new THREE.Color(`hsl(${index * 27}, 70%, 20%)`),
            });
            const torus = new THREE.Mesh(geometry, material);
            
            torus.position.x = (Math.random() - 0.5) * 10;
            torus.position.y = (Math.random() - 0.5) * 3;
            torus.position.z = (Math.random() - 0.5) * 5;
            
            torus.userData = {
                speed: Math.random() * 0.02 + 0.01,
                rotationSpeed: Math.random() * 0.03 + 0.01,
                offset: Math.random() * Math.PI * 2
            };
            
            scene.add(torus);
            objects.push(torus);
        });
        
        camera.position.z = 5;
        
        function animate() {
            requestAnimationFrame(animate);
            
            objects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.8;
                obj.position.y += Math.sin(Date.now() * obj.userData.speed + obj.userData.offset) * 0.005;
            });
            
            camera.rotation.y += 0.002;
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / 200;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 200);
        });
    </script>
</body>
</html>
"""

components.html(webgl_html, height=220)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🧮 HandCalc Pro v1.0 - Manual Arithmetic Visualizer</p>
    <p>Watch your calculations come to life with step-by-step manual methods!</p>
</div>
""", unsafe_allow_html=True)
