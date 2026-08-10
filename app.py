# app.py – Corrigido cache do Streamlit, Derivadas/Integrais blindadas, e Divisão adicionada
import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import (symbols, diff, integrate, solve, latex, simplify, expand,
                   sin, cos, tan, exp, log, Symbol, S)
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
import traceback

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap');
    .main-title {
        font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%; height: 50px; font-size: 16px; font-weight: 600; border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def parse_func(self, func_str):
        if not func_str or not str(func_str).strip():
            return None
        transformations = (standard_transformations + (implicit_multiplication_application,))
        clean_str = str(func_str).replace('^', '**').replace('×', '*').replace('÷', '/').strip()
        clean_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', clean_str)
        try:
            return parse_expr(clean_str, transformations=transformations)
        except Exception:
            return None

    # ---------- MANUAL ADDITION ----------
    def manual_add(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        max_len = max(len(s1), len(s2))
        result = n1 + n2
        result_str = str(result)

        carries = []
        carry = 0
        p1 = s1.zfill(max_len)
        p2 = s2.zfill(max_len)
        for i in range(max_len - 1, -1, -1):
            s = int(p1[i]) + int(p2[i]) + carry
            carries.insert(0, s // 10)
            carry = s // 10

        width = max(len(s1), len(s2) + 2, len(result_str)) + 1
        lines = []
        if any(c > 0 for c in carries):
            carry_str = "".join(str(c) if c > 0 else " " for c in carries)
            lines.append(carry_str.rjust(width))
        lines.append(s1.rjust(width))
        lines.append(("+ " + s2).rjust(width))
        lines.append("─" * width)
        lines.append(result_str.rjust(width))
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➕ Adição Armada</strong><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display" style="line-height: 1.1; padding: 10px;">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Resultado: {n1} + {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL SUBTRACTION ----------
    def manual_sub(self, n1, n2):
        result = n1 - n2
        s1, s2 = str(abs(n1)), str(abs(n2))
        width = max(len(s1), len(s2) + 2, len(str(result))) + 1
        lines = [s1.rjust(width), ("- " + s2).rjust(width), "─" * width, str(result).rjust(width)]
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➖ Subtração Armada</strong><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display" style="line-height: 1.1; padding: 10px;">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Resultado: {n1} - {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL MULTIPLICATION ----------
    def manual_mul(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        result = n1 * n2
        partials = []
        for i, d in enumerate(reversed(s2)):
            partials.append(int(s1) * int(d) * (10 ** i))
        partials_rev = list(reversed(partials))

        max_w = max(len(s1), len(s2) + 2, max([len(str(p)) for p in partials] or [0]), len(str(result))) + 1
        lines = []
        lines.append(s1.rjust(max_w))
        lines.append(("× " + s2).rjust(max_w))
        lines.append("─" * max_w)
        if len(s2) > 1:
            for p in partials_rev:
                lines.append(str(p).rjust(max_w))
            lines.append("─" * max_w)
        lines.append(str(result).rjust(max_w))
        display_text = "\n".join(lines)

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>✖️ Multiplicação Armada</strong><br>')
        html.append('<div style="text-align: center;"><pre class="manual-display" style="line-height: 1.1; padding: 10px;">' + display_text + '</pre></div>')
        html.append(f'<div class="result-box">🎯 <strong>Resultado: {n1} × {n2} = {result}</strong></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- MANUAL DIVISION (CONTA COM CHAVE) ----------
    def manual_div(self, n1, n2):
        if n2 == 0:
            return "<div class='step-box'>❌ <b>Erro:</b> Divisão por zero não permitida.</div>"

        dividend = abs(n1)
        divisor = abs(n2)
        q = dividend // divisor
        r = dividend % divisor

        html = []
        html.append('<div class="step-box">')
        html.append('<strong>➗ Divisão Armada (Passo a Passo)</strong><br><br>')

        # Desenho da chave de divisão brasileira perfeitamente alinhada
        html.append('<div class="formula-highlight" style="display: flex; justify-content: center; font-size: 24px; font-family: monospace; align-items: flex-start;">')
        html.append(f'<div style="padding-right: 10px; padding-top: 5px;">{dividend}</div>')
        html.append(f'<div style="border-left: 2px solid #333; padding-left: 10px; text-align: left;">')
        html.append(f'<div style="border-bottom: 2px solid #333; padding-bottom: 5px;">{divisor}</div>')
        html.append(f'<div style="padding-top: 5px; color: #d946ef; font-weight: bold;">{q}</div>')
        html.append('</div></div><br>')

        if dividend < divisor:
            html.append(f'O dividendo (<b>{dividend}</b>) é menor que o divisor (<b>{divisor}</b>).<br>')
            html.append(f'Portanto, o quociente inteiro é <b>0</b> e o resto é <b>{dividend}</b>.<br>')
        else:
            html.append('<strong>Passos Detalhados:</strong><br>')
            s1 = str(dividend)
            current_val = 0
            q_str = ""
            step_counter = 1
            for i, digit in enumerate(s1):
                current_val = current_val * 10 + int(digit)
                if current_val < divisor and i < len(s1) - 1 and q_str == "":
                    continue

                q_digit = current_val // divisor
                subtrahend = divisor * q_digit
                rem = current_val % divisor

                step = f'<span class="step-number">{step_counter}</span> '
                step += f'Dividindo <b>{current_val}</b> por {divisor}:<br>'
                step += f'&nbsp;&nbsp; &bull; {divisor} × <b>{q_digit}</b> = {subtrahend}<br>'
                step += f'&nbsp;&nbsp; &bull; Resto: {current_val} - {subtrahend} = <b>{rem}</b><br>'
                html.append(step)

                if i < len(s1) - 1:
                    next_digit = s1[i+1]
                    html.append(f'&nbsp;&nbsp; <i>(Baixando o próximo dígito <b>{next_digit}</b> &rarr; formando <b>{rem}{next_digit}</b>)</i><br><br>')

                current_val = rem
                q_str += str(q_digit)
                step_counter += 1

        html.append(f'<div class="result-box">🎯 <strong>Resultado: {dividend} ÷ {divisor} = {q}</strong><br><span style="font-size: 16px;">(Resto {r})</span></div>')
        html.append('</div>')
        return '\n'.join(html)

    # ---------- FIRST-DEGREE EQUATION ----------
    def solve_linear(self, eq_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Equação do 1º Grau</div>')
            html.append('<p><b>ax + b = 0</b>. Isola-se a incógnita utilizando operações inversas.</p></div>')

            if '=' in eq_str:
                left_str, right_str = eq_str.split('=')
                left_expr = self.parse_func(left_str)
                right_expr = self.parse_func(right_str)
                if left_expr is None or right_expr is None:
                    return "<div class='step-box'>❌ Equação inválida.</div>"
                expr = expand(left_expr - right_expr)
            else:
                expr = self.parse_func(eq_str)
                if expr is None:
                    return "<div class='step-box'>❌ Expressão inválida.</div>"
                expr = expand(expr)

            html.append('<div class="step-box"><strong>📝 Resolução Passo a Passo:</strong><br><br>')

            if '=' in eq_str:
                html.append('<span class="step-number">1</span> <strong>Equação original:</strong><br>')
                html.append(f'<div class="formula-highlight">$${latex(left_expr)} = {latex(right_expr)}$$</div>')

            html.append('<span class="step-number">2</span> <strong>Forma reduzida:</strong><br>')
            html.append(f'<div class="formula-highlight">$${latex(expr)} = 0$$</div>')

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a, b = 0, 0

            if a == 0:
                html.append('<b>Não é uma equação de 1º grau (a = 0).</b></div>')
                return '\n'.join(html)

            x_sol = -b / a
            html.append('<span class="step-number">3</span> <strong>Isolando x:</strong><br>')
            html.append(f'$$x = \\frac{{{-b}}}{{{a}}} = {latex(sp.nsimplify(x_sol))}$$<br>')
            html.append(f'<div class="result-box">🎯 <strong>Resultado: $x = {latex(sp.nsimplify(x_sol))}$</strong></div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Erro: {str(e)}</div>"

    # ---------- QUADRATIC EQUATION ----------
    def solve_quadratic(self, func_str):
        try:
            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Equação do 2º Grau (Bhaskara)</div>')
            html.append('<p><b>ax² + bx + c = 0</b>. Fórmula: $$x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$$</p></div>')

            if '=' in func_str:
                left_str, right_str = func_str.split('=')
                left_expr = self.parse_func(left_str)
                right_expr = self.parse_func(right_str)
                expr = expand(left_expr - right_expr)
            else:
                expr = expand(self.parse_func(func_str))

            html.append('<div class="step-box"><strong>📝 Resolução Passo a Passo:</strong><br><br>')
            html.append(f'<div class="formula-highlight">$${latex(expr)} = 0$$</div>')

            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            a = b = c = 0
            if len(coeffs) == 3:
                a, b, c = coeffs
            elif len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a = coeffs[0]

            if a == 0:
                html.append('<b>Não é equação de 2º grau (a = 0).</b></div>')
                return '\n'.join(html)

            disc = b**2 - 4*a*c
            html.append('<span class="step-number">1</span> <strong>Discriminante (Δ):</strong><br>')
            html.append(f'$$\\Delta = ({b})^2 - 4({a})({c}) = {disc}$$<br>')

            html.append('<span class="step-number">2</span> <strong>Cálculo das Raízes:</strong><br>')
            if disc >= 0:
                sqrt_disc = math.sqrt(disc)
                x1 = (-b + sqrt_disc) / (2*a)
                x2 = (-b - sqrt_disc) / (2*a)
                html.append(f'<div class="result-box">🎯 $x_1 = {latex(sp.nsimplify(x1))}, \\quad x_2 = {latex(sp.nsimplify(x2))}$</div>')
            else:
                real_part = -b / (2*a)
                imag_part = math.sqrt(-disc) / (2*a)
                html.append(f'<div class="result-box">🎯 $x = {real_part:.4f} \\pm {imag_part:.4f}i$</div>')

            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            return f"<div class='step-box'>❌ Erro: {str(e)}</div>"

    # ---------- DIFFERENTIATION (FIXED & ROBUST) ----------
    def differentiate(self, func_str, var='x', eval_pt=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ <b>Erro:</b> Função inválida. Verifique a sintaxe.</div>"

            sym_var = Symbol(var)
            df = diff(expr, sym_var)
            simplified_df = simplify(df)

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Regras de Derivação Identificadas</div>')
            
            # Detecção de regras segura
            rules_used = []
            num, den = expr.as_numer_denom()
            if den != 1 and den.has(sym_var):
                rules_used.append("• <b>Regra do Quociente:</b> $\\frac{d}{d" + var + "}\\left[\\frac{u}{v}\\right] = \\frac{u'v - uv'}{v^2}$")
            elif expr.is_Mul and len([arg for arg in expr.args if arg.has(sym_var)]) > 1:
                rules_used.append("• <b>Regra do Produto:</b> $\\frac{d}{d" + var + "}[u \\cdot v] = u'v + uv'$")

            has_chain = False
            for sub in sp.postorder_traversal(expr):
                if sub.is_Function or (sub.is_Pow and sub.base.has(sym_var) and sub.base != sym_var):
                    has_chain = True
                    break
            if has_chain:
                rules_used.append("• <b>Regra da Cadeia (Função Composta):</b> $\\frac{d}{d" + var + "}[f(g(" + var + "))] = f'(g(" + var + ")) \\cdot g'(" + var + ")$")

            rules_used.append("• <b>Regra da Potência e Linearidade:</b> $\\frac{d}{d" + var + "}[" + var + "^n] = n " + var + "^{n-1}$")
            html.append('<br>'.join(rules_used) + '</div>')

            html.append('<div class="step-box"><strong>📝 Resolução Passo a Passo:</strong><br><br>')
            html.append('<span class="step-number">1</span> <strong>Função Original:</strong><br>')
            html.append(f'<div class="formula-highlight">$$f({var}) = {latex(expr)}$$</div>')

            expanded = expand(expr)
            html.append('<span class="step-number">2</span> <strong>Derivando a Expressão:</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                d_term = diff(term, sym_var)
                html.append(f'• Termo {i+1}: $\\frac{{d}}{{d{var}}}\\left({latex(term)}\\right) = {latex(d_term)}$<br>')

            html.append('<br><span class="step-number">3</span> <strong>Resultado da Derivada (Simplificada):</strong><br>')
            html.append(f'$$f\'({var}) = {latex(simplified_df)}$$<br>')

            # Avaliação no ponto com validação segura
            if eval_pt is not None and str(eval_pt).strip() != "":
                pt_val = parse_expr(str(eval_pt).replace('^', '**'))
                if pt_val is not None:
                    val_result = simplified_df.subs(sym_var, pt_val)
                    html.append('<span class="step-number">4</span> <strong>Avaliação no Ponto ($' + var + ' = ' + latex(pt_val) + '$):</strong><br>')
                    html.append(f'$$f\'({latex(pt_val)}) = {latex(val_result)}$$')
                    if val_result.is_number and not val_result.is_Integer:
                        html.append(f' $$\\approx {float(val_result):.4f}$$')
                    html.append('<br>')

            html.append(f'<div class="result-box">🎯 $$\\boxed{{f\'({var}) = {latex(simplified_df)}}}$$</div>')
            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            err_msg = traceback.format_exc()
            return f"<div class='step-box'>❌ <b>Erro interno na Derivada:</b> {str(e)}<br><pre>{err_msg}</pre></div>"

    # ---------- INTEGRATION (FIXED & ROBUST) ----------
    def integrate_func(self, func_str, var='x', lower_bound=None, upper_bound=None):
        try:
            expr = self.parse_func(func_str)
            if expr is None:
                return "<div class='step-box'>❌ <b>Erro:</b> Função inválida. Verifique a sintaxe.</div>"

            sym_var = Symbol(var)
            is_definite = False
            a_val, b_val = None, None

            if lower_bound is not None and upper_bound is not None and str(lower_bound).strip() != "" and str(upper_bound).strip() != "":
                a_val = parse_expr(str(lower_bound).replace('^', '**'))
                b_val = parse_expr(str(upper_bound).replace('^', '**'))
                if a_val is not None and b_val is not None:
                    is_definite = True

            html = []
            html.append('<div class="theory-box"><div class="theory-title">📚 Regras de Integração Aplicadas</div>')
            html.append("• <b>Regras Básicas:</b> Potência, Substituição Simples, ou Integração por Partes (quando aplicável).<br></div>")

            html.append('<div class="step-box"><strong>📝 Resolução Passo a Passo:</strong><br><br>')

            if is_definite:
                html.append('<span class="step-number">1</span> <strong>Integral Definida:</strong><br>')
                html.append(f'<div class="formula-highlight">$$\\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\left({latex(expr)}\\right) \\, d{var}$$</div>')
            else:
                html.append('<span class="step-number">1</span> <strong>Integral Indefinida:</strong><br>')
                html.append(f'<div class="formula-highlight">$$\\int \\left({latex(expr)}\\right) \\, d{var}$$</div>')

            expanded = expand(expr)
            html.append('<span class="step-number">2</span> <strong>Integração (Primitiva $F(' + var + ')$):</strong><br>')
            terms = expanded.args if expanded.is_Add else [expanded]
            for i, term in enumerate(terms):
                int_t = integrate(term, sym_var)
                html.append(f'• $\\int \\left({latex(term)}\\right) \\, d{var} = {latex(int_t)}$<br>')

            primitive = integrate(expr, sym_var)
            simplified_prim = simplify(primitive)

            html.append(f'<br>$$F({var}) = {latex(simplified_prim)}$$<br>')

            if is_definite:
                html.append('<span class="step-number">3</span> <strong>Teorema Fundamental do Cálculo:</strong><br>')
                fb = simplified_prim.subs(sym_var, b_val)
                fa = simplified_prim.subs(sym_var, a_val)
                def_result = simplify(fb - fa)

                html.append(f'• $F({latex(b_val)}) = {latex(fb)}$<br>')
                html.append(f'• $F({latex(a_val)}) = {latex(fa)}$<br>')
                html.append(f'• $F(b) - F(a) = {latex(def_result)}$<br>')

                if def_result.is_number and not def_result.is_Integer:
                    html.append(f'Valor aproximado: $$\\approx {float(def_result):.4f}$$<br>')

                html.append(f'<div class="result-box">🎯 $$\\boxed{{\\int_{{{latex(a_val)}}}^{{{latex(b_val)}}} \\left({latex(expr)}\\right) \\, d{var} = {latex(def_result)}}}$$</div>')
            else:
                html.append(f'<div class="result-box">🎯 $$\\boxed{{\\int \\left({latex(expr)}\\right) \\, d{var} = {latex(simplified_prim)} + C}}$$</div>')

            html.append('</div>')
            return '\n'.join(html)
        except Exception as e:
            err_msg = traceback.format_exc()
            return f"<div class='step-box'>❌ <b>Erro interno na Integral:</b> {str(e)}<br><pre>{err_msg}</pre></div>"

# ---------- UI Streamlit ----------

# A grande correção para o bug de Cache do Streamlit: instanciar OBRIGATORIAMENTE fora do session_state
solver = MathSolver()

if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">Resolução de Matemática Passo a Passo com LaTeX e Operações Armadas</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Modo de Operação")
    mode = st.selectbox("Escolha o cálculo:", [
        "Operações Básicas (Armadas)",
        "Equação de 1º Grau",
        "Equação de 2º Grau",
        "Diferenciação (Derivadas)",
        "Integração (Definida/Indefinida)"
    ])
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Reset"):
            st.session_state.result_html = ""
            st.rerun()
    with c2:
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.result_html = ""
            st.session_state.history = []
            st.rerun()
    st.markdown("---")
    st.markdown("## 📊 Histórico")
    for h in st.session_state.history[-5:]:
        st.info(h)

col_in, col_out = st.columns([1, 1.4])
with col_in:
    st.markdown("### 📝 Entrada de Dados")

    if mode == "Operações Básicas (Armadas)":
        op = st.selectbox("Operação:", ["Adição (+)", "Subtração (-)", "Multiplicação (×)", "Divisão (÷)"])
        n1 = st.number_input("Primeiro número (Dividendo se Divisão):", value=125, step=1, format="%d")
        n2 = st.number_input("Segundo número (Divisor se Divisão):", value=5, step=1, format="%d")
        if st.button("🧮 Armar e Calcular", use_container_width=True):
            if op == "Adição (+)":
                html_res = solver.manual_add(int(n1), int(n2))
            elif op == "Subtração (-)":
                html_res = solver.manual_sub(int(n1), int(n2))
            elif op == "Multiplicação (×)":
                html_res = solver.manual_mul(int(n1), int(n2))
            else:
                html_res = solver.manual_div(int(n1), int(n2))
            st.session_state.result_html = html_res
            st.session_state.history.append(f"{n1} {op[0]} {n2}")

    elif mode == "Equação de 1º Grau":
        eq = st.text_input("Equação (ex: 2x + 3 = 7):", "2x + 3 = 7")
        if st.button("📐 Resolver Equação", use_container_width=True):
            html_res = solver.solve_linear(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Linear: {eq}")

    elif mode == "Equação de 2º Grau":
        eq = st.text_input("Equação (ex: x^2 + 3x - 4 = 0):", "x^2 + 3x - 4 = 0")
        if st.button("🔢 Resolver Equação", use_container_width=True):
            html_res = solver.solve_quadratic(eq)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Quadrática: {eq}")

    elif mode == "Diferenciação (Derivadas)":
        func = st.text_input("Função f(x) (ex: sin(x^2) + 3x):", "x^2 + 3x + 5")
        var = st.selectbox("Variável:", ["x", "y", "z"])
        eval_pt = st.text_input("Avaliar no ponto / limite (Opcional, ex: 2 ou pi):", "")
        if st.button("📈 Derivar Passo a Passo", use_container_width=True):
            html_res = solver.differentiate(func, var, eval_pt)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Derivada: f({var}) = {func}")

    elif mode == "Integração (Definida/Indefinida)":
        func = st.text_input("Função f(x) (ex: x^2 + 3*sin(x)):", "x^2 + 3x")
        var = st.selectbox("Variável:", ["x", "y", "z"])
        use_limits = st.checkbox("Integral Definida (com limites de integração)")
        low_bnd, upp_bnd = None, None
        if use_limits:
            col_a, col_b = st.columns(2)
            with col_a:
                low_bnd = st.text_input("Limite Inferior (a):", "0")
            with col_b:
                upp_bnd = st.text_input("Limite Superior (b):", "1")

        if st.button("📊 Integrar Passo a Passo", use_container_width=True):
            html_res = solver.integrate_func(func, var, low_bnd, upp_bnd)
            st.session_state.result_html = html_res
            st.session_state.history.append(f"Integral: f({var}) = {func}")

with col_out:
    st.markdown("### ✨ Solução Passo a Passo")
    if st.session_state.result_html:
        components.html(
            """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            startup: {
                pageReady: () => {
                    return MathJax.startup.defaultPageReady().then(() => {
                        MathJax.typesetPromise();
                    });
                }
            }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 10px;
            color: #2d3748;
        }
        .manual-display {
            font-family: 'Courier New', Courier, monospace;
            font-size: 22px;
            font-weight: bold;
            background: #1e293b;
            color: #38bdf8;
            border-radius: 8px;
            display: inline-block;
            white-space: pre;
            text-align: right;
            letter-spacing: 2px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 0 auto;
        }
        .step-box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #764ba2;
        }
        .step-number {
            display: inline-block;
            background: #667eea;
            color: white;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            text-align: center;
            line-height: 28px;
            margin-right: 8px;
            font-weight: bold;
            font-size: 14px;
        }
        .formula-highlight {
            background: #f8fafc;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            margin: 12px 0;
        }
        .result-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 18px;
            text-align: center;
            margin: 18px 0;
            font-size: 20px;
            font-weight: bold;
        }
        .theory-box {
            background: #f0f4ff;
            border-left: 5px solid #667eea;
            border-radius: 10px;
            padding: 16px;
            margin: 15px 0;
        }
        .theory-title {
            font-size: 18px;
            font-weight: 700;
            color: #4c51bf;
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
""" + st.session_state.result_html + """
</body>
</html>
""",
            height=900,
            scrolling=True
        )
    else:
        st.info("👈 Escolha um modo de operação, insira os dados e clique em Calcular para visualizar a resolução completa passo a passo!")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>🧮 HandCalc Pro – Resolução Passo a Passo Garantida</div>", unsafe_allow_html=True)
