code = r'''import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="HandCalc Pro - Passo a Passo", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 32px; font-weight: bold; color: #1e293b; text-align: center; margin-bottom: 20px; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

class CompleteMathSolver:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')

    def parse_eq(self, eq_str):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        if '=' in eq_str:
            lhs, rhs = eq_str.split('=', 1)
            eq_str = f"({lhs}) - ({rhs})"
        eq_str = eq_str.replace('^', '**')
        return parse_expr(eq_str, transformations=transformations)

    def format_latex(self, content):
        return f"$$ {content} $$"

    def manual_addition(self, n1, n2):
        res = n1 + n2
        out = r"\text{Soma de conta armada a mão livre:}\\" + "\n"
        out += f"\\begin{{array}}{{r}} {n1} \\\\ + \\; {n2} \\\\ \\hline {res} \\end{{array}}"
        return self.format_latex(out)
        
    def manual_subtraction(self, n1, n2):
        res = n1 - n2
        out = r"\text{Subtração de conta armada a mão livre:}\\" + "\n"
        out += f"\\begin{{array}}{{r}} {n1} \\\\ - \\; {n2} \\\\ \\hline {res} \\end{{array}}"
        return self.format_latex(out)

    def manual_multiplication(self, n1, n2):
        res = n1 * n2
        str2 = str(n2)
        partials = [n1 * int(d) * (10**i) for i, d in enumerate(reversed(str2))]
        out = r"\text{Multiplicação de conta armada a mão livre:}\\" + "\n"
        out += f"\\begin{{array}}{{r}} {n1} \\\\ \\times \\; {n2} \\\\ \\hline "
        if len(partials) > 1:
            for i, p in enumerate(reversed(partials)):
                out += f"{'+' if i>0 else ''} \\; {p} \\\\ "
            out += "\\hline "
        out += f"{res} \\end{{array}}"
        return self.format_latex(out)

    def manual_division(self, n1, n2):
        if n2 == 0: return "Erro: Divisão por zero."
        q = int(n1 // n2)
        r = int(n1 % n2)
        out = r"\text{Divisão de conta armada a mão livre:}\\" + "\n"
        out += f"\\begin{{array}}{{r|l}} {n1} & {n2} \\\\ \\cline{{2-2}} -{q*n2} & {q} \\\\ \\cline{{1-1}} {r} & \\end{{array}}"
        return self.format_latex(out)

    def solve_linear(self, eq_str):
        eq = self.parse_eq(eq_str)
        eq = sp.expand(eq)
        a = eq.coeff(self.x)
        b = eq.subs(self.x, 0)
        root = sp.solve(eq, self.x)[0] if a != 0 else 0
        
        out = r"\begin{aligned} &\text{1. Função Linear (1º Grau)} \\ &\text{Definição: } f(x) = mx + b \\ &\text{Exemplo: Resolver } " + sp.latex(eq) + r" = 0 \\ \\ \end{aligned}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{Passo 1: Igualar a zero} & " + sp.latex(a*self.x + b) + r" = 0 \\ "
        out += r"\text{Passo 2: Isolar o termo com x} & " + sp.latex(a*self.x) + r" = " + sp.latex(-b) + r" \\ "
        out += r"\text{Passo 3: Resolver para x} & x = " + sp.latex(root) + r" \end{array}"
        return self.format_latex(out)

    def solve_quadratic(self, eq_str):
        eq = self.parse_eq(eq_str)
        eq = sp.expand(eq)
        a = eq.coeff(self.x, 2)
        b = eq.coeff(self.x, 1)
        c = eq.subs(self.x, 0)
        delta = b**2 - 4*a*c
        roots = sp.solve(eq, self.x)
        r1 = roots[0] if len(roots) > 0 else "N/A"
        r2 = roots[1] if len(roots) > 1 else r1
        
        out = r"\begin{aligned} &\text{2. Função Quadrática (2º Grau)} \\ &\text{Definição: } f(x) = ax^2 + bx + c \\ &\text{Exemplo: Resolver } " + sp.latex(eq) + r" = 0 \\ \\ \end{aligned}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{Passo 1: Identificar coeficientes} & a = " + sp.latex(a) + r", b = " + sp.latex(b) + r", c = " + sp.latex(c) + r" \\ "
        out += r"\text{Passo 2: Calcular o Delta} & \Delta = b^2 - 4ac = " + sp.latex(delta) + r" \\ "
        out += r"\text{Passo 3: Bhaskara} & x = \frac{-b \pm \sqrt{\Delta}}{2a} \\ "
        out += r"\text{Passo 4: Substituir valores} & x = \frac{" + sp.latex(-b) + r" \pm \sqrt{" + sp.latex(delta) + r"}}{" + sp.latex(2*a) + r"} \\ "
        out += r"\text{Passo 5: Encontrar raízes} & x_1 = " + sp.latex(r1) + r", x_2 = " + sp.latex(r2) + r" \end{array}"
        return self.format_latex(out)

    def solve_sys2x2(self, eq1_str, eq2_str):
        eq1 = self.parse_eq(eq1_str)
        eq2 = self.parse_eq(eq2_str)
        sol = sp.solve((eq1, eq2), (self.x, self.y))
        
        out = r"\text{Sistema 2x2 (Metodo da Eliminacao)}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{Equacoes:} & " + sp.latex(sp.Eq(eq1+self.x, self.x)) + r"; \;" + sp.latex(sp.Eq(eq2+self.y, self.y)) + r" \\ "
        out += r"\text{1. Multiplicar (Eliminação):} & \text{Alinhando coeficientes...} \\ "
        out += r"\text{2. Subtrair equações:} & \text{Isolando variável...} \\ "
        out += r"\text{3. Solução:} & x = " + sp.latex(sol.get(self.x, '')) + r", y = " + sp.latex(sol.get(self.y, '')) + r" \end{array}"
        return self.format_latex(out)

    def solve_sys3x3(self, eq1_str, eq2_str, eq3_str):
        eq1 = self.parse_eq(eq1_str)
        eq2 = self.parse_eq(eq2_str)
        eq3 = self.parse_eq(eq3_str)
        sol = sp.solve((eq1, eq2, eq3), (self.x, self.y, self.z))
        
        out = r"\text{Sistema 3x3 (Metodo da Eliminacao)}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{Equacoes:} & \text{Sistema de 3 equações} \\ "
        out += r"\text{1. Somar Eq1 + Eq2:} & \text{Eliminando x...} \\ "
        out += r"\text{2. Somar Eq2 + Eq3:} & \text{Eliminando y...} \\ "
        out += r"\text{3. Resolver z e y:} & x = " + sp.latex(sol.get(self.x, '')) + r", y = " + sp.latex(sol.get(self.y, '')) + r", z = " + sp.latex(sol.get(self.z, '')) + r" \end{array}"
        return self.format_latex(out)

    def differentiate(self, func_str):
        f = self.parse_eq(func_str)
        df = sp.diff(f, self.x)
        out = r"\textbf{Derivative Calculation}\\" + "\n"
        out += r"f(x) = " + sp.latex(f) + r" \\\\"
        out += r"\textbf{Solution Steps:}\\" + "\n"
        out += r"\begin{array}{l} "
        out += r"1. \text{ Original function: } f(x) = " + sp.latex(f) + r" \\ "
        out += r"2. \text{ Apply differentiation rules } \\ "
        out += r"3. \text{ Result: } f'(x) = " + sp.latex(df) + r" \\ "
        out += r"\textbf{Final Answer: } \boxed{f'(x) = " + sp.latex(df) + r"} \end{array}"
        return self.format_latex(out)

    def integrate(self, func_str):
        f = self.parse_eq(func_str)
        int_f = sp.integrate(f, self.x)
        out = r"\text{Exemplo 2: Integral Indefinida}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{Problema:} & \int " + sp.latex(f) + r" \,dx \\ "
        out += r"\text{1. Subs:} & \text{Integração Padrão / Exponenciais} \\ "
        out += r"\text{2. Integral:} & " + sp.latex(int_f) + r" + C \end{array}"
        return self.format_latex(out)

    def limit_lhopital(self, func_str, point):
        f = self.parse_eq(func_str)
        lim = sp.limit(f, self.x, point)
        out = r"\text{Exemplo 3: Regra de L'Hopital}\\" + "\n"
        out += r"\begin{array}{ll} "
        out += r"\text{1. Verificacao:} & \lim_{x \to " + str(point) + r"} " + sp.latex(f) + r" \\ "
        out += r"\text{2. Aplicacao:} & \text{Derivando numerador e denominador...} \\ "
        out += r"\text{3. Resultado:} & " + sp.latex(lim) + r" \end{array}"
        return self.format_latex(out)

solver = CompleteMathSolver()

st.markdown('<div class="main-title">🧮 HandCalc Pro - Passo a Passo Completo</div>', unsafe_allow_html=True)

mode = st.sidebar.selectbox("Operação:", [
    "Aritmética Básica (Conta Armada)",
    "Funções (1º e 2º Grau)",
    "Sistemas Lineares",
    "Cálculo"
])

html_res = ""

if mode == "Aritmética Básica (Conta Armada)":
    op = st.selectbox("Operação:", ["Soma", "Subtração", "Multiplicação", "Divisão"])
    n1 = st.number_input("N1", value=250, step=1)
    n2 = st.number_input("N2", value=5, step=1)
    if st.button("Calcular"):
        if op == "Soma": html_res = solver.manual_addition(n1, n2)
        elif op == "Subtração": html_res = solver.manual_subtraction(n1, n2)
        elif op == "Multiplicação": html_res = solver.manual_multiplication(n1, n2)
        elif op == "Divisão": html_res = solver.manual_division(n1, n2)

elif mode == "Funções (1º e 2º Grau)":
    tipo = st.selectbox("Tipo:", ["1º Grau", "2º Grau"])
    if tipo == "1º Grau":
        eq = st.text_input("Equação", "2*x - 4 = 0")
        if st.button("Resolver"): html_res = solver.solve_linear(eq)
    else:
        eq = st.text_input("Equação", "x^2 - 5*x + 6 = 0")
        if st.button("Resolver"): html_res = solver.solve_quadratic(eq)

elif mode == "Sistemas Lineares":
    tipo = st.selectbox("Tamanho:", ["2x2", "3x3"])
    if tipo == "2x2":
        e1 = st.text_input("Eq1", "2*x + 3*y = 8")
        e2 = st.text_input("Eq2", "x - 2*y = -3")
        if st.button("Resolver"): html_res = solver.solve_sys2x2(e1, e2)
    else:
        e1 = st.text_input("Eq1", "x + y + z = 6")
        e2 = st.text_input("Eq2", "x - y + z = 2")
        e3 = st.text_input("Eq3", "2*x + y - z = 1")
        if st.button("Resolver"): html_res = solver.solve_sys3x3(e1, e2, e3)

elif mode == "Cálculo":
    op = st.selectbox("Operação:", ["Derivada", "Integral", "Limite (L'Hopital)"])
    f = st.text_input("Função", "x^2 + 3*x")
    pt = st.number_input("Ponto x ->", value=0) if op == "Limite (L'Hopital)" else 0
    if st.button("Calcular"):
        if op == "Derivada": html_res = solver.differentiate(f)
        elif op == "Integral": html_res = solver.integrate(f)
        else: html_res = solver.limit_lhopital(f, pt)

if html_res:
    components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            <style>body {{ font-family: sans-serif; padding: 20px; font-size: 1.1em; color: #1e293b; background-color: #fff; }}</style>
        </head>
        <body>{html_res}</body>
        </html>
    """, height=500, scrolling=True)
'''

import codecs
with codecs.open("app.py", "w", encoding="utf-8") as file:
    file.write(code)
print("[file-tag: app.py]")
