import streamlit as st
import sympy as sp
from sympy import latex, expand
import math

# ============================================================
# 1. SOLUCIONADOR DE EQUAÇÕES LINEARES (já em Python)
# ============================================================
class EquationSolver:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.step_counter = 0

    def reset_step_count(self):
        self.step_counter = 0

    def increment_step(self):
        self.step_counter += 1
        return self.step_counter

    def fmt_neg(self, val):
        if val < 0:
            return f"({val})"
        return f"{val}"

    def parse_func(self, expr_str):
        try:
            return sp.sympify(expr_str.replace("^", "**"))
        except:
            return None

    def solve_linear_detailed(self, eq_str):
        self.reset_step_count()
        try:
            if '=' not in eq_str:
                return "<div class='step-box'>❌ Use '=' para separar os lados esquerdo e direito.</div>"

            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str)
            right_expr = self.parse_func(right_str)

            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Expressão inválida. Use 'x' como variável.</div>"

            step1 = self.increment_step()
            step2 = self.increment_step()
            expr = expand(left_expr - right_expr)

            step3 = self.increment_step()
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()

            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a = b = 0

            if a == 0:
                return "<div class='step-box'>⚠️ Não é uma equação linear (a = 0).</div>"

            step4 = self.increment_step()
            step5 = self.increment_step()
            x_sol = -b / a
            latex_sol = latex(sp.nsimplify(x_sol))

            step6 = self.increment_step()
            verification_left = left_expr.subs(self.x, x_sol)
            verification_right = right_expr.subs(self.x, x_sol)

            step7 = self.increment_step()

            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 Equação Linear (1º Grau) – Resolução Completa</div>
                <p>Uma equação na forma <b>ax + b = 0</b> tem solução <b>x = -b/a</b></p>
                <p><b>Conceitos:</b></p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Maior potência da variável é 1</li>
                    <li>• Solução única (um valor de x)</li>
                    <li>• Podemos verificar substituindo na equação original</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Resolução Detalhada (7 Passos)</div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step1}: Identificar a equação</span>
                    <p>Temos a equação:</p>
                    <div class="formula-highlight">$$\\text{{Equação original: }} {latex(left_expr)} = {latex(right_expr)}$$</div>
                    <p style="margin-left: 20px;">• Lado esquerdo: <b>{latex(left_expr)}</b></p>
                    <p style="margin-left: 20px;">• Lado direito: <b>{latex(right_expr)}</b></p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step2}: Mover todos os termos para um lado</span>
                    <p>Subtrair o lado direito de ambos os lados:</p>
                    <div class="formula-highlight">$${latex(left_expr)} - {latex(right_expr)} = 0$$</div>
                    <p style="margin-left: 20px;">Obtemos a forma padrão <b>ax + b = 0</b></p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step3}: Identificar coeficientes a e b</span>
                    <p>Comparando com <b>ax + b = 0</b>:</p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                    <p style="margin-left: 20px;">Coeficiente de x: <b>a = {a}</b></p>
                    <p style="margin-left: 20px;">Termo constante: <b>b = {b}</b></p>
                    <p style="margin-left: 20px;">Verificação: <b>{a}x + {b} = 0</b> ✓</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step4}: Isolar o termo com variável</span>
                    <p>Mover o termo constante para o lado direito:</p>
                    <div class="formula-highlight">
                        $${a}x = -{self.fmt_neg(b)}$$
                    </div>
                    <p style="margin-left: 20px;">• Subtraímos <b>{b}</b> de ambos os lados</p>
                    <p style="margin-left: 20px;">• O termo variável está isolado</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step5}: Resolver para x</span>
                    <p>Dividir ambos os lados pelo coeficiente <b>a</b>:</p>
                    <div class="formula-highlight">
                        $$x = \\frac{{-{self.fmt_neg(b)}}}{{{a}}}$$
                    </div>
                    <p style="margin-left: 20px;">Simplificando o sinal negativo:</p>
                    <div class="formula-highlight">
                        $$-({self.fmt_neg(b)}) = {latex(sp.simplify(-b))}$$
                    </div>
                    <p style="margin-left: 20px;">Valor final: <b>x = {latex_sol}</b></p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step6}: Verificar a solução</span>
                    <p>Substituir x = {latex_sol} na equação original:</p>
                    <p style="margin-left: 20px;">Lado esquerdo: <b>{latex(left_expr)}</b> → <b>{latex(verification_left)}</b></p>
                    <p style="margin-left: 20px;">Lado direito: <b>{latex(right_expr)}</b> → <b>{latex(verification_right)}</b></p>
                    <div class="formula-highlight">$${latex(verification_left)} = {latex(verification_right)}$$</div>
                    <p style="margin-left: 20px;">Ambos os lados são iguais! ✓</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Passo {step7}: Conclusão final</span>
                    <p>Resolvemos a equação com sucesso:</p>
                    <div class="formula-highlight">$$\\boxed{{x = {latex_sol}}}$$</div>
                    <div class="verification">
                        <p>✅ <b>Verificação completa:</b></p>
                        <p>Original: <b>{eq_str}</b></p>
                        <p>Substituindo x = {latex_sol}:</p>
                        <p><b>{latex(left_expr.subs(self.x, x_sol))} = {latex(right_expr.subs(self.x, x_sol))}</b> ✓</p>
                    </div>
                </div>
                
                <div class="result-box">🎯 <strong>Solução: $x = {latex_sol}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Erro: {str(e)}</div>"


# ============================================================
# 2. CALCULADORA ARITMÉTICA (adaptada do C++ para Python)
# ============================================================
class LongArithmeticCalculator:
    def __init__(self):
        self.steps = []

    def format_number(self, num):
        """Remove zeros decimais desnecessários."""
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        s = f"{num:.10f}".rstrip('0').rstrip('.')
        return s

    def center_align(self, text, width):
        padding = width - len(text)
        if padding <= 0:
            return text
        left = padding // 2
        return ' ' * left + text

    def add(self, a, b):
        self.steps.clear()
        n1, n2 = float(a), float(b)
        res = n1 + n2
        stra, strb = self.format_number(n1), self.format_number(n2)
        strres = self.format_number(res)
        max_len = max(len(stra), len(strb)) + 1
        total_width = max_len + 2

        lines = []
        lines.append(f"{stra:>{total_width}}")
        lines.append(f"+{strb:>{total_width-1}}")
        lines.append('─' * total_width)
        lines.append(f"{strres:>{total_width}}")
        self.steps.append('\n'.join(lines))
        return strres

    def subtract(self, a, b):
        self.steps.clear()
        n1, n2 = float(a), float(b)
        res = n1 - n2
        stra, strb = self.format_number(n1), self.format_number(n2)
        strres = self.format_number(res)
        max_len = max(len(stra), len(strb)) + 1
        total_width = max_len + 2

        lines = []
        lines.append(f"{stra:>{total_width}}")
        lines.append(f"-{strb:>{total_width-1}}")
        lines.append('─' * total_width)
        lines.append(f"{strres:>{total_width}}")
        self.steps.append('\n'.join(lines))
        return strres

    def multiply(self, a, b):
        self.steps.clear()
        n1, n2 = float(a), float(b)
        res = n1 * n2

        # Se ambos são inteiros, mostra multiplicação longa
        if n1 == int(n1) and n2 == int(n2) and n1 >= 0 and n2 >= 0:
            i1, i2 = int(n1), int(n2)
            str1 = str(i1)
            str2 = str(i2)

            # Produtos parciais
            partials = []
            str2_rev = str2[::-1]
            for i, ch in enumerate(str2_rev):
                digit = int(ch)
                partial = i1 * digit * (10 ** i)
                partials.append(partial)

            total_width = max(len(str1), len(str2) + 1, len(str(int(res)))) + 2

            lines = []
            lines.append(f"{str1:>{total_width}}")
            lines.append(f"×{str2:>{total_width-1}}")
            lines.append('─' * total_width)

            for idx, p in enumerate(reversed(partials)):
                p_str = str(p)
                prefix = '+' if idx > 0 else ' '
                lines.append(f"{prefix}{p_str:>{total_width-1}}")

            lines.append('─' * total_width)
            lines.append(f"{int(res):>{total_width}}")
            self.steps.append('\n'.join(lines))
        else:
            # Exibição simples para decimais
            stra, strb = self.format_number(n1), self.format_number(n2)
            strres = self.format_number(res)
            total_width = max(len(stra), len(strb) + 1, len(strres)) + 2
            lines = []
            lines.append(f"{stra:>{total_width}}")
            lines.append(f"×{strb:>{total_width-1}}")
            lines.append('─' * total_width)
            lines.append(f"{strres:>{total_width}}")
            self.steps.append('\n'.join(lines))

        return self.format_number(res)

    def divide(self, a, b):
        self.steps.clear()
        n1, n2 = float(a), float(b)
        if n2 == 0:
            self.steps.append("Erro: divisão por zero!")
            return "Erro"
        res = n1 / n2
        visual = f"{self.format_number(n1)} ÷ {self.format_number(n2)} = {self.format_number(res)}\n"

        # Divisão longa apenas para inteiros positivos
        if n1 == int(n1) and n2 == int(n2) and n1 >= n2 and n2 > 0:
            dividend = int(n1)
            divisor = int(n2)
            quotient = dividend // divisor
            remainder = dividend % divisor
            visual += f"\nDivisão longa:\n"
            visual += f"  {quotient} (quociente)\n"
            visual += f"{divisor}){dividend}\n"
            visual += f"  {divisor * quotient}\n"
            visual += "─" * 10 + "\n"
            visual += f"  {remainder} (resto)\n"
        self.steps.append(visual)
        return self.format_number(res)

    def square_root(self, num):
        self.steps.clear()
        val = float(num)
        if val < 0:
            self.steps.append("Erro: raiz quadrada de número negativo!")
            return "Erro"
        res = math.sqrt(val)
        visual = f"√{self.format_number(val)} = {self.format_number(res)}\n\n"
        if val > 0:
            visual += "Aproximação (método de Newton):\n"
            x0 = val / 2
            visual += f"Passo 0: x₀ = {self.format_number(x0)}\n"
            for i in range(1, 4):
                x1 = (x0 + val / x0) / 2
                visual += f"Passo {i}: {self.format_number(x0)} → {self.format_number(x1)}\n"
                x0 = x1
        self.steps.append(visual)
        return self.format_number(res)

    def cube_root(self, num):
        self.steps.clear()
        val = float(num)
        res = val ** (1/3)  # mais simples que math.cbrt para versões antigas
        visual = f"∛{self.format_number(val)} = {self.format_number(res)}\n\n"
        if val != 0:
            visual += "Aproximação:\n"
            x0 = val / 3
            visual += f"Passo 0: x₀ = {self.format_number(x0)}\n"
            for i in range(1, 4):
                x1 = (2 * x0 + val / (x0 * x0)) / 3
                visual += f"Passo {i}: {self.format_number(x0)} → {self.format_number(x1)}\n"
                x0 = x1
        self.steps.append(visual)
        return self.format_number(res)

    def rule_of_three(self, a, b, c):
        self.steps.clear()
        na, nb, nc = float(a), float(b), float(c)
        res = (nb * nc) / na
        visual = "Regra de três (proporção direta):\n\n"
        visual += f"{self.format_number(na)} ———→ {self.format_number(nb)}\n"
        visual += f"{self.format_number(nc)} ———→ x\n\n"
        visual += f"x = ({self.format_number(nb)} × {self.format_number(nc)}) ÷ {self.format_number(na)}\n"
        visual += f"x = {self.format_number(nb * nc)} ÷ {self.format_number(na)}\n"
        visual += f"x = {self.format_number(res)}\n"
        self.steps.append(visual)
        return self.format_number(res)

    # Os métodos de integração e derivada são mantidos como demonstração,
    # usando funções predefinidas (f(x)=x²)
    def integrate(self, expr, lower, upper, intervals=100):
        self.steps.clear()
        a, b = float(lower), float(upper)
        h = (b - a) / intervals
        def f(x):
            return x*x   # função de exemplo, pode-se estender depois
        result = (f(a) + f(b)) / 2
        for i in range(1, intervals):
            result += f(a + i * h)
        result *= h
        visual = "Integração numérica (Regra do Trapézio)\n"
        visual += f"∫ {expr} dx de {self.format_number(a)} a {self.format_number(b)}\n"
        visual += f"{intervals} intervalos, h = {self.format_number(h)}\n\n"
        visual += f"f({self.format_number(a)}) = {self.format_number(f(a))}\n"
        visual += f"f({self.format_number(b)}) = {self.format_number(f(b))}\n"
        visual += f"Soma dos pontos interiores ≈ {self.format_number(result/h)}\n"
        visual += f"Resultado ≈ {self.format_number(result)}"
        self.steps.append(visual)
        return self.format_number(result)

    def derivative(self, expr, point):
        self.steps.clear()
        x0 = float(point)
        h = 0.0001
        def f(x):
            return x*x
        f_plus = f(x0 + h)
        f_minus = f(x0 - h)
        deriv = (f_plus - f_minus) / (2 * h)
        visual = "Derivada numérica (diferença central)\n"
        visual += f"d/dx ({expr}) em x = {self.format_number(x0)}\n\n"
        visual += f"f'({self.format_number(x0)}) ≈ [f({self.format_number(x0+h)}) - f({self.format_number(x0-h)})] / (2·{h})\n"
        visual += f" ≈ ({self.format_number(f_plus)} - {self.format_number(f_minus)}) / {self.format_number(2*h)}\n"
        visual += f" ≈ {self.format_number(deriv)}"
        self.steps.append(visual)
        return self.format_number(deriv)


# ============================================================
# 3. INTERFACE STREAMLIT UNIFICADA
# ============================================================
st.set_page_config(page_title="Calculadora Completa", layout="centered")

st.title("🧮 Calculadora Passo a Passo")
st.markdown("""
<style>
    .theory-box { background: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4CAF50; }
    .theory-title { font-size: 1.2em; font-weight: bold; color: #2e7d32; margin-bottom: 10px; }
    .step-box { background: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .step-header { font-size: 1.1em; font-weight: bold; color: #1e88e5; margin-bottom: 15px; }
    .step-detail { margin-bottom: 18px; padding: 10px; background: #fafafa; border-radius: 8px; }
    .step-counter { display: inline-block; background: #1e88e5; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.9em; margin-bottom: 5px; }
    .formula-highlight { background: #fff9c4; padding: 5px 10px; display: inline-block; border-radius: 5px; margin: 5px 0; }
    .verification { background: #e8f5e9; padding: 10px; border-radius: 8px; margin-top: 10px; }
    .result-box { background: #4CAF50; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.3em; margin-top: 20px; }
    .calc-steps { background: #f5f5f5; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; white-space: pre; }
</style>
""", unsafe_allow_html=True)

# Barra lateral para escolher o modo
mode = st.sidebar.radio("Selecione a ferramenta:", ["📐 Equações Lineares", "🔢 Calculadora Aritmética"])

if mode == "📐 Equações Lineares":
    st.header("Solucionador de Equações Lineares")
    eq_input = st.text_input("Digite a equação (use 'x' como variável):",
                             value="2*x + 3 = 7",
                             help="Exemplo: 3*x - 5 = 10")
    if st.button("Resolver Passo a Passo"):
        if eq_input.strip():
            solver = EquationSolver()
            html = solver.solve_linear_detailed(eq_input)
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("Por favor, digite uma equação.")

elif mode == "🔢 Calculadora Aritmética":
    st.header("Calculadora Aritmética com Passo a Passo")
    op = st.selectbox("Operação:", ["Adição", "Subtração", "Multiplicação", "Divisão", 
                                    "Raiz Quadrada", "Raiz Cúbica", "Regra de Três",
                                    "Integração (f(x)=x²)", "Derivada (f(x)=x²)"])

    calc = LongArithmeticCalculator()

    if op in ["Adição", "Subtração", "Multiplicação", "Divisão"]:
        col1, col2 = st.columns(2)
        with col1:
            num1 = st.text_input("Número 1", "123")
        with col2:
            num2 = st.text_input("Número 2", "456")
        if st.button("Calcular"):
            try:
                if op == "Adição":
                    res = calc.add(num1, num2)
                elif op == "Subtração":
                    res = calc.subtract(num1, num2)
                elif op == "Multiplicação":
                    res = calc.multiply(num1, num2)
                else: # Divisão
                    res = calc.divide(num1, num2)
                st.success(f"Resultado: {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")

    elif op == "Raiz Quadrada":
        num = st.text_input("Número:", "144")
        if st.button("Calcular"):
            try:
                res = calc.square_root(num)
                st.success(f"Resultado: {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")

    elif op == "Raiz Cúbica":
        num = st.text_input("Número:", "27")
        if st.button("Calcular"):
            try:
                res = calc.cube_root(num)
                st.success(f"Resultado: {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")

    elif op == "Regra de Três":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.text_input("a (valor conhecido)", "10")
        with col2:
            b = st.text_input("b (correspondente a a)", "20")
        with col3:
            c = st.text_input("c (outro valor)", "30")
        if st.button("Calcular x"):
            try:
                res = calc.rule_of_three(a, b, c)
                st.success(f"x = {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")

    elif op == "Integração (f(x)=x²)":
        col1, col2 = st.columns(2)
        with col1:
            lower = st.text_input("Limite inferior", "0")
        with col2:
            upper = st.text_input("Limite superior", "1")
        intervals = st.slider("Número de intervalos", 10, 1000, 100)
        if st.button("Integrar"):
            try:
                res = calc.integrate("x^2", lower, upper, intervals)
                st.success(f"∫ x² dx de {lower} a {upper} ≈ {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")

    elif op == "Derivada (f(x)=x²)":
        point = st.text_input("Ponto x:", "2")
        if st.button("Derivar"):
            try:
                res = calc.derivative("x^2", point)
                st.success(f"f'({point}) ≈ {res}")
                st.markdown("**Passo a passo:**")
                for step in calc.steps:
                    st.code(step, language="text")
            except Exception as e:
                st.error(f"Erro: {e}")
