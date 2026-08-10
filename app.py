import streamlit as st
import streamlit.components.v1 as components
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, expand,
                   Matrix, Eq, Symbol)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Page config
st.set_page_config(
    page_title="HandCalc Pro – Complete Step-by-Step",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap');
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
    }
    .step-box {
        background: white; border-radius: 10px; padding: 25px; margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05); border-left: 5px solid #764ba2;
        font-size: 18px;
    }
    .stButton > button {
        width: 100%; height: 55px; font-size: 16px; font-weight: 600; border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

class CompleteMathSolver:
    def _escape_latex(self, s: str) -> str:
        """Escape backslashes so they survive Python string formatting."""
        return s.replace('\\', '\\\\')

    def parse_eq(self, eq_str: str):
        transformations = (standard_transformations + (implicit_multiplication_application,))
        eq_str = eq_str.replace('^', '**').replace(' ', '')
        if '=' in eq_str:
            left, right = eq_str.split('=')
            lhs = parse_expr(left, transformations=transformations)
            rhs = parse_expr(right, transformations=transformations)
            return Eq(lhs, rhs)
        else:
            lhs = parse_expr(eq_str, transformations=transformations)
            return Eq(lhs, 0)

    # ---------- BASIC ARITHMETIC IN LATEX FORMAT ----------
    def manual_addition(self, num1: int, num2: int) -> str:
        result = num1 + num2
        latex_str = f"$$ \\begin{{array}}{{r}} {num1} \\\\ + \\ {num2} \\\\ \\hline {result} \\end{{array}} $$"
        html = '<div class="step-box"><strong>➕ Soma de conta armada a mão livre</strong><br><br>'
        html += latex_str
        html += '</div>'
        return html

    def manual_multiplication(self, num1: int, num2: int) -> str:
        str2 = str(num2)
        result = num1 * num2
        
        partials = []
        for i, digit in enumerate(reversed(str2)):
            partials.append(num1 * int(digit) * (10**i))
        
        latex_str = f"$$ \\begin{{array}}{{r}} {num1} \\\\ \\times \\ {num2} \\\\ \\hline "
        
        if len(partials) == 1:
            latex_str += f"{result} \\end{{array}} $$"
        else:
            for i, p in enumerate(partials):
                if i == 0:
                    latex_str += f"{p} \\\\"
                elif i == len(partials) - 1:
                    latex_str += f" + {p} \\\\ \\hline "
                else:
                    latex_str += f" + {p} \\\\"
            latex_str += f"{result} \\end{{array}} $$"
            
        html = '<div class="step-box"><strong>✖️ Multiplicação de conta armada a mão livre</strong><br><br>'
        html += latex_str
        html += '</div>'
        return html

    # ---------- FIRST-DEGREE EQUATION ----------
    def solve_first_degree_equation(self, equation_str: str) -> str:
        var = symbols('x')
        try:
            eq = self.parse_eq(equation_str)
            expr = eq.lhs - eq.rhs
            a = expr.coeff(var)
            b = expr.subs(var, 0)
            
            steps = []
            steps.append(f"{latex(eq)}")
            if eq.rhs != 0:
                steps.append(f"{latex(eq.lhs)} - ({latex(eq.rhs)}) = 0")
            if expand(expr) != expr:
                steps.append(f"{latex(expand(expr))} = 0")
            
            steps.append(f"{latex(a*var)} = {latex(-b)}")
            sol = solve(expr, var)
            if sol:
                steps.append(f"x = {latex(sol[0])}")
            
            latex_steps = " \\\\ \n\\Rightarrow \\quad & ".join(steps)
            html = f"""<div class="step-box">
            <strong>📐 Passos da Equação do 1º Grau</strong>
            $$ \\begin{{align*}} & {self._escape_latex(latex_steps)} \\end{{align*}} $$
            </div>"""
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar equação: {str(e)}</div>"

    # ---------- QUADRATIC EQUATION ----------
    def solve_quadratic_equation(self, equation_str: str) -> str:
        var = symbols('x')
        try:
            eq = self.parse_eq(equation_str)
            expr = expand(eq.lhs - eq.rhs)
            a = expr.coeff(var, 2)
            b = expr.coeff(var, 1)
            c = expr.subs(var, 0)
            
            delta = b**2 - 4*a*c
            
            html = f"""<div class="step-box">
            <strong>🔢 Equação do 2º Grau (Bhaskara)</strong>
            $$ \\text{{Equação: }} {self._escape_latex(latex(eq))} $$
            $$ \\text{{Forma Padrão: }} {self._escape_latex(latex(expr))} = 0 $$
            $$ a = {self._escape_latex(latex(a))}, \\quad b = {self._escape_latex(latex(b))}, \\quad c = {self._escape_latex(latex(c))} $$
            <br><strong>1. Discriminante ($\\Delta$):</strong>
            $$ \\Delta = b^2 - 4ac $$
            $$ \\Delta = ({self._escape_latex(latex(b))})^2 - 4({self._escape_latex(latex(a))})({self._escape_latex(latex(c))}) $$
            $$ \\Delta = {self._escape_latex(latex(delta))} $$
            <br><strong>2. Raízes ($x_1, x_2$):</strong>
            """
            if delta < 0:
                html += "$$ \\Delta < 0 \\implies \\text{Sem raízes reais.} $$"
            elif delta == 0:
                x1 = -b / (2*a)
                html += f"""
                $$ x = \\frac{{-b}}{{2a}} = \\frac{{-({self._escape_latex(latex(b))})}}{{2({self._escape_latex(latex(a))})}} $$
                $$ x = {self._escape_latex(latex(x1))} $$
                """
            else:
                html += f"""
                $$ x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} = \\frac{{-({self._escape_latex(latex(b))}) \\pm \\sqrt{{{self._escape_latex(latex(delta))}}}}}{{2({self._escape_latex(latex(a))})}} $$
                """
                sol = solve(expr, var)
                for i, s in enumerate(sol):
                    html += f"$$ x_{i+1} = {self._escape_latex(latex(s))} $$"
                    
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar equação: {str(e)}</div>"

    # ---------- LINEAR SYSTEMS 2x2 & 3x3 ----------
    def solve_system_2x2(self, eq1_str: str, eq2_str: str) -> str:
        x, y = symbols('x y')
        try:
            eq1 = self.parse_eq(eq1_str)
            eq2 = self.parse_eq(eq2_str)
            
            expr1 = expand(eq1.lhs - eq1.rhs)
            expr2 = expand(eq2.lhs - eq2.rhs)
            
            a1, b1, c1 = expr1.coeff(x), expr1.coeff(y), -expr1.subs({x:0, y:0})
            a2, b2, c2 = expr2.coeff(x), expr2.coeff(y), -expr2.subs({x:0, y:0})
            
            D = a1*b2 - a2*b1
            Dx = c1*b2 - c2*b1
            Dy = a1*c2 - a2*c1
            
            html = f"""<div class="step-box">
            <strong>🔄 Sistema Linear 2x2 (Regra de Cramer)</strong>
            $$ \\begin{{cases}} {self._escape_latex(latex(eq1))} \\\\ {self._escape_latex(latex(eq2))} \\end{{cases}} $$
            $$ \\text{{Forma Padrão:}} $$
            $$ \\begin{{cases}} {self._escape_latex(latex(a1*x + b1*y))} = {self._escape_latex(latex(c1))} \\\\ {self._escape_latex(latex(a2*x + b2*y))} = {self._escape_latex(latex(c2))} \\end{{cases}} $$
            <br><strong>1. Determinantes:</strong>
            $$ D = \\begin{{vmatrix}} {self._escape_latex(latex(a1))} & {self._escape_latex(latex(b1))} \\\\ {self._escape_latex(latex(a2))} & {self._escape_latex(latex(b2))} \\end{{vmatrix}} = {self._escape_latex(latex(D))} $$
            $$ D_x = \\begin{{vmatrix}} {self._escape_latex(latex(c1))} & {self._escape_latex(latex(b1))} \\\\ {self._escape_latex(latex(c2))} & {self._escape_latex(latex(b2))} \\end{{vmatrix}} = {self._escape_latex(latex(Dx))} $$
            $$ D_y = \\begin{{vmatrix}} {self._escape_latex(latex(a1))} & {self._escape_latex(latex(c1))} \\\\ {self._escape_latex(latex(a2))} & {self._escape_latex(latex(c2))} \\end{{vmatrix}} = {self._escape_latex(latex(Dy))} $$
            <br><strong>2. Solução:</strong>
            """
            if D == 0:
                if Dx == 0 and Dy == 0:
                    html += "$$ D = 0, D_x = 0, D_y = 0 \\implies \\text{Soluções infinitas (SPI).} $$"
                else:
                    html += "$$ D = 0 \\implies \\text{Sem solução (SI).} $$"
            else:
                html += f"""
                $$ x = \\frac{{D_x}}{{D}} = \\frac{{{self._escape_latex(latex(Dx))}}}{{{self._escape_latex(latex(D))}}} = {self._escape_latex(latex(Dx/D))} $$
                $$ y = \\frac{{D_y}}{{D}} = \\frac{{{self._escape_latex(latex(Dy))}}}{{{self._escape_latex(latex(D))}}} = {self._escape_latex(latex(Dy/D))} $$
                """
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar sistema: {str(e)}</div>"

    def solve_system_3x3(self, eq1_str: str, eq2_str: str, eq3_str: str) -> str:
        x, y, z = symbols('x y z')
        try:
            eq1 = self.parse_eq(eq1_str)
            eq2 = self.parse_eq(eq2_str)
            eq3 = self.parse_eq(eq3_str)
            
            expr1 = expand(eq1.lhs - eq1.rhs)
            expr2 = expand(eq2.lhs - eq2.rhs)
            expr3 = expand(eq3.lhs - eq3.rhs)
            
            a1, b1, c1, d1 = expr1.coeff(x), expr1.coeff(y), expr1.coeff(z), -expr1.subs({x:0, y:0, z:0})
            a2, b2, c2, d2 = expr2.coeff(x), expr2.coeff(y), expr2.coeff(z), -expr2.subs({x:0, y:0, z:0})
            a3, b3, c3, d3 = expr3.coeff(x), expr3.coeff(y), expr3.coeff(z), -expr3.subs({x:0, y:0, z:0})
            
            M = Matrix([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])
            Mx = Matrix([[d1, b1, c1], [d2, b2, c2], [d3, b3, c3]])
            My = Matrix([[a1, d1, c1], [a2, d2, c2], [a3, d3, c3]])
            Mz = Matrix([[a1, b1, d1], [a2, b2, d2], [a3, b3, d3]])
            
            D = M.det()
            Dx = Mx.det()
            Dy = My.det()
            Dz = Mz.det()
            
            html = f"""<div class="step-box">
            <strong>🔄 Sistema Linear 3x3 (Regra de Cramer)</strong>
            $$ \\begin{{cases}} {self._escape_latex(latex(eq1))} \\\\ {self._escape_latex(latex(eq2))} \\\\ {self._escape_latex(latex(eq3))} \\end{{cases}} $$
            <br><strong>1. Determinantes:</strong>
            $$ D = \\begin{{vmatrix}} {self._escape_latex(latex(a1))} & {self._escape_latex(latex(b1))} & {self._escape_latex(latex(c1))} \\\\ {self._escape_latex(latex(a2))} & {self._escape_latex(latex(b2))} & {self._escape_latex(latex(c2))} \\\\ {self._escape_latex(latex(a3))} & {self._escape_latex(latex(b3))} & {self._escape_latex(latex(c3))} \\end{{vmatrix}} = {self._escape_latex(latex(D))} $$
            $$ D_x = \\begin{{vmatrix}} {self._escape_latex(latex(d1))} & {self._escape_latex(latex(b1))} & {self._escape_latex(latex(c1))} \\\\ {self._escape_latex(latex(d2))} & {self._escape_latex(latex(b2))} & {self._escape_latex(latex(c2))} \\\\ {self._escape_latex(latex(d3))} & {self._escape_latex(latex(b3))} & {self._escape_latex(latex(c3))} \\end{{vmatrix}} = {self._escape_latex(latex(Dx))} $$
            $$ D_y = \\begin{{vmatrix}} {self._escape_latex(latex(a1))} & {self._escape_latex(latex(d1))} & {self._escape_latex(latex(c1))} \\\\ {self._escape_latex(latex(a2))} & {self._escape_latex(latex(d2))} & {self._escape_latex(latex(c2))} \\\\ {self._escape_latex(latex(a3))} & {self._escape_latex(latex(d3))} & {self._escape_latex(latex(c3))} \\end{{vmatrix}} = {self._escape_latex(latex(Dy))} $$
            $$ D_z = \\begin{{vmatrix}} {self._escape_latex(latex(a1))} & {self._escape_latex(latex(b1))} & {self._escape_latex(latex(d1))} \\\\ {self._escape_latex(latex(a2))} & {self._escape_latex(latex(b2))} & {self._escape_latex(latex(d2))} \\\\ {self._escape_latex(latex(a3))} & {self._escape_latex(latex(b3))} & {self._escape_latex(latex(d3))} \\end{{vmatrix}} = {self._escape_latex(latex(Dz))} $$
            <br><strong>2. Solução:</strong>
            """
            if D == 0:
                html += "$$ D = 0 \\implies \\text{Sistema não possui solução única (SPI ou SI).} $$"
            else:
                html += f"""
                $$ x = \\frac{{D_x}}{{D}} = \\frac{{{self._escape_latex(latex(Dx))}}}{{{self._escape_latex(latex(D))}}} = {self._escape_latex(latex(Dx/D))} $$
                $$ y = \\frac{{D_y}}{{D}} = \\frac{{{self._escape_latex(latex(Dy))}}}{{{self._escape_latex(latex(D))}}} = {self._escape_latex(latex(Dy/D))} $$
                $$ z = \\frac{{D_z}}{{D}} = \\frac{{{self._escape_latex(latex(Dz))}}}{{{self._escape_latex(latex(D))}}} = {self._escape_latex(latex(Dz/D))} $$
                """
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar sistema: {str(e)}</div>"

    # ---------- DIFFERENTIATION ----------
    def differentiate_step_by_step(self, func_str: str, var_str: str = 'x') -> str:
        var = Symbol(var_str)
        try:
            func = parse_expr(func_str.replace('^', '**'), transformations=(standard_transformations + (implicit_multiplication_application,)))
            
            html = f"""<div class="step-box">
            <strong>📈 Derivadas (Regras de Cálculo)</strong>
            $$ f({var_str}) = {self._escape_latex(latex(func))} $$
            $$ f'({var_str}) = \\frac{{d}}{{d{var_str}}} \\left( {self._escape_latex(latex(func))} \\right) $$
            """
            if func.is_Add:
                html += f"$$ = " + " + ".join([f"\\frac{{d}}{{d{var_str}}}\\left({self._escape_latex(latex(arg))}\\right)" for arg in func.args]) + " $$"
            
            deriv_eval = diff(func, var)
            html += f"$$ f'({var_str}) = {self._escape_latex(latex(deriv_eval))} $$"
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar derivada: {str(e)}</div>"

    # ---------- INTEGRATION ----------
    def integrate_step_by_step(self, func_str: str, var_str: str = 'x') -> str:
        var = Symbol(var_str)
        try:
            func = parse_expr(func_str.replace('^', '**'), transformations=(standard_transformations + (implicit_multiplication_application,)))
            
            html = f"""<div class="step-box">
            <strong>📊 Integrais (Regras de Cálculo)</strong>
            $$ \\int {self._escape_latex(latex(func))} \\, d{var_str} $$
            """
            if func.is_Add:
                html += f"$$ = " + " + ".join([f"\\int {self._escape_latex(latex(arg))} \\, d{var_str}" for arg in func.args]) + " $$"
                
            integral_eval = integrate(func, var)
            html += f"$$ = {self._escape_latex(latex(integral_eval))} + C $$"
            html += "</div>"
            return html
        except Exception as e:
            return f"<div class='step-box'>Erro ao processar integral: {str(e)}</div>"


# ---------- Streamlit UI ----------
if 'solver' not in st.session_state:
    st.session_state.solver = CompleteMathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">Resoluções completas em formato TeX/LaTeX padrão</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Modo de Operação")
    mode = st.selectbox("Escolha:", [
        "Aritmética Básica",
        "Equação do 1º Grau",
        "Equação do 2º Grau",
        "Sistema Linear 2x2",
        "Sistema Linear 3x3",
        "Derivação",
        "Integração"
    ])
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset"): st.session_state.result_html = ""; st.rerun()
    with col2:
        if st.button("🗑️ Limpar"): st.session_state.result_html = ""; st.session_state.history = []; st.rerun()
    st.markdown("---")
    st.markdown("## 📊 Histórico")
    for h in st.session_state.history[-5:]:
        st.info(h)

col_in, col_out = st.columns([1, 1.5])
with col_in:
    st.markdown("### 📝 Entrada")
    solver = st.session_state.solver

    if mode == "Aritmética Básica":
        op = st.selectbox("Operação:", ["Soma (+)", "Multiplicação (×)"])
        n1 = st.number_input("Primeiro número:", value=123, format="%d")
        n2 = st.number_input("Segundo número:", value=45, format="%d")
        if st.button("🧮 Calcular"):
            if op == "Soma (+)":
                html_res = solver.manual_addition(int(n1), int(n2))
            else:
                html_res = solver.manual_multiplication(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "Equação do 1º Grau":
        eq = st.text_input("Equação (ex: 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Resolver"):
            html_res = solver.solve_first_degree_equation(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Equação do 2º Grau":
        eq = st.text_input("Equação (ex: x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Resolver"):
            html_res = solver.solve_quadratic_equation(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quad: {eq}")

    elif mode == "Sistema Linear 2x2":
        eq1 = st.text_input("Equação 1:", "2x + y = 5")
        eq2 = st.text_input("Equação 2:", "x - y = 1")
        if st.button("🔄 Resolver Sistema"):
            html_res = solver.solve_system_2x2(eq1, eq2)
            st.session_state.result_html = html_res
            st.session_state.history.append("Sis 2x2")

    elif mode == "Sistema Linear 3x3":
        eq1 = st.text_input("Equação 1:", "x + y + z = 6")
        eq2 = st.text_input("Equação 2:", "2x - y + z = 3")
        eq3 = st.text_input("Equação 3:", "x + 2y - z = 2")
        if st.button("🔄 Resolver Sistema"):
            html_res = solver.solve_system_3x3(eq1, eq2, eq3)
            st.session_state.result_html = html_res
            st.session_state.history.append("Sis 3x3")

    elif mode == "Derivação":
        func = st.text_input("f(x) =", "x^2 + 3x + 5")
        var = st.selectbox("Variável:", ["x","y","z"])
        if st.button("📈 Derivar"):
            html_res = solver.differentiate_step_by_step(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Diff: {func}")

    elif mode == "Integração":
        func = st.text_input("f(x) =", "x^2 + 3x")
        var = st.selectbox("Variável:", ["x","y","z"])
        if st.button("📊 Integrar"):
            html_res = solver.integrate_step_by_step(func, var)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Int: {func}")

with col_out:
    st.markdown("### ✨ Resolução Passo-a-Passo")
    if st.session_state.result_html:
        # A injeção do MathJax garante que tudo o que estiver entre $$...$$ ou $...$ seja renderizado.
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
                            processEscapes: true,
                            tags: 'ams'
                        }},
                        startup: {{
                            pageReady: () => {{
                                return MathJax.startup.defaultPageReady().then(() => {{
                                    MathJax.typesetPromise();
                                }});
                            }}
                        }}
                    }};
                </script>
                <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <style>
                    body {{ font-family: 'Computer Modern', serif; padding: 20px; font-size: 110%; }}
                    .step-box {{ background: white; padding: 20px; border-radius: 10px; font-family: sans-serif; }}
                    strong {{ font-family: sans-serif; }}
                </style>
            </head>
            <body>
                {st.session_state.result_html}
            </body>
            </html>
            """,
            height=750,
            scrolling=True
        )
    else:
        st.info("👈 Escolha um modo, insira os dados e clique em **Calcular** para ver os passos em LaTeX.")
```eof

O código foi atualizado para:
1. **Contas Armadas a Mão Livre:** Utilizar `\begin{array}{r}` exatamente como nas imagens de soma e multiplicação manual. O resultado é exibido perfeitamente formatado na vertical com as quebras corretas.
2. **Sistemas Lineares (Cramer):** Adicionado a resolução de matrizes 2x2 e 3x3 utilizando o formato matricial de equações (`\begin{cases}`) e de determinantes (`\begin{vmatrix}`), assim como na imagem fornecida de sistemas lineares.
3. **Cálculo de 1º e 2º Grau:** Formatação fluida utilizando blocos de `\Rightarrow` em formato LaTeX.
4. **Cálculo II (Integrais e Derivadas):** Passos intermediários formatados demonstrando as quebras das regras (ex: regras da soma onde as somas são desmembradas em partes $\int a + \int b$).
