import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(page_title="Advanced Math Solver", layout="wide", page_icon="♾️")

st.markdown(
    """
    <style>
    .step-box {
        background-color: #1E1E1E;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .answer-box {
        background-color: #2C3E50;
        border-left: 5px solid #3498DB;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("♾️ Advanced Math Solver – Step-by-Step")
st.markdown("### *Soluções elegantes, precisas e visualmente abrangentes.*")
st.divider()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def render_step(step_num, title, latex_expr=None, text=None):
    st.markdown(f"**Step {step_num}: {title}**")
    if text:
        st.markdown(text)
    if latex_expr:
        st.latex(latex_expr)

x, y, z, h = sp.symbols('x y z h')
sym_vars = {'x': x, 'y': y, 'z': z, 'h': h}

def parse_expr(expr_str):
    try:
        return sp.sympify(expr_str.replace("^", "**"), locals=sym_vars)
    except:
        return None

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
menu = st.sidebar.radio(
    "Select Mathematical Module",
    [
        "1. Operações Básicas (+, -, *, /)",
        "2. Função de 1º Grau (Linear)",
        "3. Função de 2º Grau (Quadrática)",
        "4. Sistemas Lineares (Matrizes)",
        "5. Limites e Regras",
        "6. Derivadas e Tangentes",
        "7. Integrais e Sólidos de Revolução"
    ]
)

# ==========================================
# 1. BASIC OPERATIONS WITH VISUAL RULES
# ==========================================
if menu.startswith("1"):
    st.header("1. Operações Básicas Passo a Passo")
    st.markdown("Regras visuais elegantes de vai um, pegar emprestado e divisões formatadas.")
    
    op = st.selectbox("Selecione a Operação", ["Adição (+)", "Subtração (-)", "Multiplicação (×)", "Divisão (÷)"])
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Primeiro Número", value=136 if "Sub" in op else 125, step=1, min_value=0)
    with col2:
        num2 = st.number_input("Segundo Número", value=169 if "Sub" in op else 5, step=1, min_value=1 if "Div" in op else 0)

    if st.button("Calcular"):
        
        if op == "Adição (+)":
            # LOGIC: Adição com Transporte ("Vai um")
            n1_str, n2_str = str(num1)[::-1], str(num2)[::-1]
            max_len = max(len(n1_str), len(n2_str))
            n1_str = n1_str.ljust(max_len, '0')
            n2_str = n2_str.ljust(max_len, '0')
            
            carries = [0] * (max_len + 1)
            result = []
            
            for i in range(max_len):
                sum_val = int(n1_str[i]) + int(n2_str[i]) + carries[i]
                result.append(str(sum_val % 10))
                carries[i+1] = sum_val // 10
                
            ans = num1 + num2
            
            # Formatação LaTeX Elegante
            n1_latex = ""
            for i in range(max_len - 1, -1, -1):
                if carries[i+1] > 0:
                    n1_latex += f"\\overset{{\\color{{red}}{{{carries[i+1]}}}}}{{{n1_str[i]}}}"
                else:
                    n1_latex += f"{n1_str[i]}"
            
            if carries[max_len] > 0:
                n1_latex = f"\\overset{{\\color{{red}}{{{carries[max_len]}}}}}{{0}}" + n1_latex
                
            latex_add = f"""
            \\begin{{array}}{{r}}
              {n1_latex} \\\\
            + {num2} \\\\
            \\hline
              {ans}
            \\end{{array}}
            """
            st.markdown("### Adição")
            st.latex(latex_add)
            st.success(f"**Resultado:** {ans}")
            
        elif op == "Subtração (-)":
            # LOGIC: Subtração com "Pegar Emprestado"
            if num1 < num2:
                st.warning("Para visualizar o passo-a-passo, o primeiro número deve ser maior. Os números serão invertidos e um sinal negativo será aplicado ao resultado.")
                num1, num2 = num2, num1
                is_negative = True
            else:
                is_negative = False
                
            final_res = num1 - num2
            sign = "-" if is_negative else ""
            
            n1_str_arr = list(str(num1))
            n2_str_arr = list(str(num2).zfill(len(n1_str_arr)))
            latex_str_n1 = ""
            work_arr = [int(x) for x in n1_str_arr]
            
            for i in range(len(work_arr)-1, -1, -1):
                if work_arr[i] < int(n2_str_arr[i]):
                    latex_str_n1 = f"\\overset{{\\color{{blue}}{{{work_arr[i]+10}}}}}{{\\color{{red}}\\cancel{{{n1_str_arr[i]}}}}}" + latex_str_n1
                    j = i - 1
                    while work_arr[j] == 0:
                        work_arr[j] = 9
                        n1_str_arr[j] = f"\\overset{{\\color{{blue}}9}}{{\\color{{red}}\\cancel{{0}}}}"
                        j -= 1
                    work_arr[j] -= 1
                    n1_str_arr[j] = f"\\overset{{\\color{{blue}}{{{work_arr[j]}}}}}{{\\color{{red}}\\cancel{{{int(n1_str_arr[j])}}}}}"
                else:
                    latex_str_n1 = n1_str_arr[i] + latex_str_n1

            latex_sub = f"""
            \\begin{{array}}{{r}}
              {latex_str_n1} \\\\
            - {str(num2).zfill(len(str(num1)))} \\\\
            \\hline
              {final_res}
            \\end{{array}}
            """
            st.markdown("### Subtração (Empréstimo)")
            st.latex(latex_sub)
            st.success(f"**Resultado:** {sign}{final_res}")

        elif op == "Multiplicação (×)":
            # LOGIC: Multiplicação com deslocamento
            st.markdown("### Multiplicação")
            n1_str = str(num1)
            n2_str = str(num2)
            
            lines = []
            for i, digit in enumerate(reversed(n2_str)):
                prod = num1 * int(digit)
                padding = "\\;" * (2 * i) 
                if i == 0:
                    lines.append(f"{prod}")
                else:
                    lines.append(f"+ {prod}{padding}")
            
            lines_str = " \\\\\n".join(lines)
            
            latex_mult = f"""
            \\begin{{array}}{{r}}
              {num1} \\\\
            \\times {num2} \\\\
            \\hline
            {lines_str} \\\\
            \\hline
              {num1 * num2}
            \\end{{array}}
            """
            st.latex(latex_mult)
            st.success(f"**Resultado:** {num1 * num2}")
            
        elif op == "Divisão (÷)":
            # LOGIC: Divisão Longa com Chave em "L" Invertido (Padrão Brasileiro)
            st.markdown("### Divisão Longa (Método da Chave)")
            quotient = num1 // num2
            remainder = num1 % num2
            
            div_str = str(num1)
            latex_str = f"\\begin{{array}}{{r|l}}\n{num1} & {num2} \\\\\n\\cline{{2-2}}\n"
            
            temp_val = ""
            q_str = ""
            
            for i, digit in enumerate(div_str):
                temp_val += digit
                val = int(temp_val)
                if val >= num2 or i == len(div_str) - 1:
                    q_digit = val // num2
                    q_str += str(q_digit)
                    sub_val = q_digit * num2
                    rem = val - sub_val
                    
                    padding = "0" * (len(div_str) - 1 - i)
                    latex_str += f"-{sub_val}\\phantom{{{padding}}} & {q_str} \\\\\n"
                    latex_str += f"\\cline{{1-1}}\n"
                    
                    temp_val = str(rem) if rem > 0 else ""
                    if i < len(div_str) - 1:
                        next_bring_down = (str(rem) if rem > 0 else "") + div_str[i+1]
                        latex_str += f"{next_bring_down}\\phantom{{{padding[1:]}}} & \\\\\n"
                    else:
                        latex_str += f"{rem} & \\\\\n"
                else:
                    if q_str != "":
                        q_str += "0"
            
            latex_str += "\\end{array}"
            
            st.latex(latex_str)
            st.success(f"**Quociente:** {quotient} | **Resto:** {remainder}")

# ... (rest of the original code remains unchanged)
