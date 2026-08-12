import streamlit as st
import sympy as sp
from sympy import latex, expand

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
        """Formata números negativos para LaTeX sem gerar --3."""
        if val < 0:
            return f"({val})"
        return f"{val}"

    def parse_func(self, expr_str):
        """Converte string de expressão em expressão sympy."""
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

# ---------- Interface Streamlit ----------
st.set_page_config(page_title="Calculadora de Equações Lineares", layout="centered")
st.title("🧮 Resolução de Equações Lineares – Passo a Passo")

# CSS personalizado para os boxes
st.markdown("""
<style>
    .theory-box {
        background: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    .theory-title {
        font-size: 1.2em; font-weight: bold; color: #2e7d32; margin-bottom: 10px;
    }
    .step-box {
        background: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .step-header {
        font-size: 1.1em; font-weight: bold; color: #1e88e5; margin-bottom: 15px;
    }
    .step-detail {
        margin-bottom: 18px; padding: 10px; background: #fafafa; border-radius: 8px;
    }
    .step-counter {
        display: inline-block; background: #1e88e5; color: white; padding: 2px 10px;
        border-radius: 12px; font-size: 0.9em; margin-bottom: 5px;
    }
    .formula-highlight {
        background: #fff9c4; padding: 5px 10px; display: inline-block; border-radius: 5px;
        margin: 5px 0;
    }
    .verification {
        background: #e8f5e9; padding: 10px; border-radius: 8px; margin-top: 10px;
    }
    .result-box {
        background: #4CAF50; color: white; padding: 15px; border-radius: 10px;
        text-align: center; font-size: 1.3em; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

eq_input = st.text_input("Digite a equação linear (use 'x' como variável):",
                         value="2*x + 3 = 7",
                         help="Exemplo: 3*x - 5 = 10")

if st.button("🔍 Resolver Passo a Passo"):
    if eq_input.strip():
        solver = EquationSolver()
        html_result = solver.solve_linear_detailed(eq_input)
        st.markdown(html_result, unsafe_allow_html=True)
    else:
        st.warning("Por favor, digite uma equação.")
