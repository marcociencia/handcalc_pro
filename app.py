# app.py
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from calculator_engine import LongArithmeticCalculator
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Initialize calculator
if 'calc' not in st.session_state:
    st.session_state.calc = LongArithmeticCalculator()
if 'display' not in st.session_state:
    st.session_state.display = ""
if 'num1' not in st.session_state:
    st.session_state.num1 = ""
if 'num2' not in st.session_state:
    st.session_state.num2 = ""
if 'operation' not in st.session_state:
    st.session_state.operation = None
if 'result' not in st.session_state:
    st.session_state.result = None

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
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    for calc in st.session_state.history[-5:]:
        st.code(calc, language='text')

# Main calculator interface
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("### 📝 Input")
    
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
    
    col_calc, col_clear = st.columns(2)
    with col_calc:
        if st.button("🧮 Calculate", use_container_width=True):
            calc = st.session_state.calc
            
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
                    result = calc.squareRoot(num1)
                    st.session_state.operation = "√"
                elif operation == "Cube Root (∛)":
                    result = calc.cubeRoot(num1)
                    st.session_state.operation = "∛"
                elif operation == "Rule of Three":
                    result = calc.ruleOfThree(num1, num2, num3)
                    st.session_state.operation = "R3"
                elif operation == "Integration (∫)":
                    result = calc.integrate("x²", num1, num2)
                    st.session_state.operation = "∫"
                elif operation == "Derivative (d/dx)":
                    result = calc.derivative("x²", num1)
                    st.session_state.operation = "d/dx"
                
                st.session_state.result = result
                st.session_state.history.append(f"{num1} {st.session_state.operation} {num2} = {result}" if num2 else f"{st.session_state.operation}{num1} = {result}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.display = ""
            st.session_state.num1 = ""
            st.session_state.num2 = ""
            st.session_state.result = None
            st.rerun()

with col2:
    st.markdown("### 🎨 Visualization")
    
    if st.session_state.result is not None:
        st.markdown(f'<div class="number-display">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        # Create 3D visualization using plotly
        if st.session_state.operation in ["+", "-", "×", "÷"]:
            try:
                val1 = float(st.session_state.num1) if 'num1' in st.session_state else 0
                val2 = float(st.session_state.num2) if 'num2' in st.session_state else 0
                result = float(st.session_state.result)
                
                fig = go.Figure(data=[
                    go.Bar(name='Numbers', x=['Num1', 'Num2', 'Result'], 
                          y=[val1, val2, result],
                          marker_color=['#667eea', '#764ba2', '#f093fb'])
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
    
    if st.session_state.result is not None:
        steps = st.session_state.calc.getSteps()
        if steps:
            st.markdown('<div class="manual-calc">', unsafe_allow_html=True)
            for step in steps:
                st.code(step.description if hasattr(step, 'description') else step, language='text')
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
        #info { 
            position: absolute; 
            top: 10px; 
            left: 10px; 
            color: white; 
            font-family: monospace;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div id="info">🧮 HandCalc Pro - WebGL 3D View</div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Initialize Three.js scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a2e);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 200, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, 200);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 5, 5);
        directionalLight.castShadow = true;
        scene.add(directionalLight);
        
        // Create floating numbers
        const numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '×', '÷', '='];
        const floatingObjects = [];
        
        numbers.forEach((num, index) => {
            const geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
            const material = new THREE.MeshPhongMaterial({ 
                color: new THREE.Color(`hsl(${index * 24}, 70%, 50%)`),
                emissive: new THREE.Color(`hsl(${index * 24}, 70%, 20%)`),
                shininess: 100
            });
            const cube = new THREE.Mesh(geometry, material);
            
            cube.position.x = (Math.random() - 0.5) * 10;
            cube.position.y = (Math.random() - 0.5) * 3;
            cube.position.z = (Math.random() - 0.5) * 5;
            
            cube.userData = {
                speed: Math.random() * 0.02 + 0.01,
                rotationSpeed: Math.random() * 0.02 + 0.01,
                amplitude: Math.random() * 2 + 1,
                offset: Math.random() * Math.PI * 2
            };
            
            scene.add(cube);
            floatingObjects.push(cube);
        });
        
        camera.position.z = 5;
        camera.position.y = 2;
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            
            floatingObjects.forEach((obj, index) => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed * 0.8;
                
                obj.position.y += Math.sin(Date.now() * obj.userData.speed + obj.userData.offset) * 0.005;
            });
            
            camera.rotation.y += 0.002;
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Resize handler
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
