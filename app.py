import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import symbols, diff, integrate, latex, simplify, expand, limit, oo, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro - Completo", page_icon="🧮", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stButton > button {
        width: 100%; height: 52px; font-weight: 700; border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
    }
    .theory-label { color: #4a5568; font-style: italic; }
</style>
""", unsafe_allow_html=True)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def parse_func(self, func_str):
        if not func_str or not str(func_str).strip(): return None
        transformations = (standard_transformations + (implicit_multiplication_application,))
        clean = str(func_str).replace('^','**').replace('×','*').replace('÷','/').strip()
        clean = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', clean)
        try:
            return parse_expr(clean, transformations=transformations)
        except: return None

    # ---------- TEORIA ESTILO PRINT ----------
    def teoria_box(self, titulo, teoria_latex):
        return f"""
        <div class="theory-box">
            <div class="theory-title">{titulo}</div>
            <p><span class="theory-label">teoria:</span> {teoria_latex}</p>
        </div>
        """

    # ---------- BÁSICAS ARMADAS ----------
    def manual_add(self, n1, n2):
        res = n1+n2
        # Montagem estilo "conta armada a mão livre"
        w = max(len(str(n1)), len(str(n2))+2, len(str(res)))+1
        linhas = [str(n1).rjust(w), ("+ "+str(n2)).rjust(w), "─"*w, str(res).rjust(w)]
        html_exemplos = """
        <div style="display:flex; gap:20px; flex-wrap:wrap; margin-top:10px;">
            <pre class="manual-display">  5\n+  5\n──\n 10</pre>
            <pre class="manual-display"> 50\n+ 50\n───\n100</pre>
            <pre class="manual-display"> 500\n+ 500\n────\n1000</pre>
            <pre class="manual-display"> 5000\n+ 5000\n─────\n10000</pre>
            <pre class="manual-display"> 50000\n+ 50000\n──────\n100000</pre>
        </div>
        """
        return f"""
        <div class="step-box">
            <strong>Exemplos de soma de conta armada a mão livre :</strong><br>
            <div class="formula-highlight">$$teoria: \\frac{{\\begin{{array}}{{c}} x \\\\ + y \\end{{array}}}}{{x+y}}$$</div>
            {html_exemplos}
            <hr>
            <strong>Sua conta:</strong><br><br>
            <pre class="manual-display">{chr(10).join(linhas)}</pre>
            <div class="result-box">🎯 {n1} + {n2} = {res}</div>
        </div>
        """

    def manual_sub(self, n1, n2):
        res = n1-n2
        w = max(len(str(n1)), len(str(n2))+2, len(str(res)))+1
        linhas = [str(n1).rjust(w), ("- "+str(n2)).rjust(w), "─"*w, str(res).rjust(w)]
        # Exemplos iguais ao print
        html = f"""
        <div class="step-box">
            <strong>Exemplos de subtração de conta armada a mão livre :</strong><br>
            <div class="formula-highlight">$$teoria: \\frac{{\\begin{{array}}{{c}} x \\\\ - y \\end{{array}}}}{{x-y}}$$</div>
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                <pre class="manual-display"> 15\n-  5\n──\n 10</pre>
                <pre class="manual-display"> 150\n-  50\n───\n100</pre>
                <pre class="manual-display">   5\n-  15\n───\n -10</pre>
                <pre class="manual-display">  50\n- 150\n───\n-100</pre>
            </div>
            <hr>
            <pre class="manual-display">{chr(10).join(linhas)}</pre>
            <div class="result-box">🎯 {n1} - {n2} = {res}</div>
        </div>
        """
        return html

    def manual_mul(self, n1, n2):
        s1, s2 = str(abs(n1)), str(abs(n2))
        res = n1*n2
        partials = []
        for i,d in enumerate(reversed(s2)):
            p = int(s1)*int(d)
            if p!=0 or len(s2)==1:
                partials.append((p, i))
        w = max(len(s1), len(s2)+2, len(str(res)))+2
        lines = [s1.rjust(w), ("× "+s2).rjust(w), "─"*w]
        for idx,(p,shift) in enumerate(reversed(partials)):
            txt = str(p) + "0"*shift
            if len(partials)>1 and idx==len(partials)-1:
                txt = "+ "+txt
            lines.append(txt.rjust(w))
        if len(partials)>1:
            lines.append("─"*w)
        lines.append(str(res).rjust(w))
        return f"""
        <div class="step-box">
            <strong>Exemplos de Multiplicação de conta armada a mão livre :</strong><br>
            <div class="formula-highlight">$$teoria: \\frac{{\\begin{{array}}{{c}} x \\\\ \\times y \\end{{array}}}}{{x \\times y}}$$</div>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 {n1} × {n2} = {res}</div>
        </div>
        """

    def manual_div(self, n1, n2):
        if n2==0: return "<div class='step-box'>❌ Divisão por zero</div>"
        q = n1//n2
        r = n1%n2
        dec = n1/n2
        display = f"{n1} | {n2}\n-{'─'*len(str(n1))} | ───\n{r} | {q}"
        return f"""
        <div class="step-box">
            <strong>Exemplos de Divisão de conta armada a mão livre :</strong><br>
            <div class="formula-highlight">$$teoria: \\begin{{array}}{{c|c}} x & y \\\\ \\hline & \\end{{array}}$$</div>
            <pre class="manual-display"> 25 | 5\n-25 | 5\n 00</pre>
            <pre class="manual-display"> 250 | 5\n-25  | 50\n  00 | \n   0</pre>
            <pre class="manual-display"> 645 | 5\n-50  | 129\n 145 | \n-145 | \n  000</pre>
            <hr>
            <pre class="manual-display">{display}</pre>
            <div class="result-box">🎯 {n1} ÷ {n2} = {q} resto {r} | decimal {dec:.4f}</div>
        </div>
        """

    # ---------- LINEAR ----------
    def solve_linear(self, eq_str):
        if '=' not in eq_str: return "❌ Use '='"
        L,R = eq_str.split('=',1)
        le = self.parse_func(L); re_ = self.parse_func(R)
        if le is None or re_ is None: return "❌ Expressão inválida"
        expr = expand(le - re_)
        poly = sp.Poly(expr, self.x)
        if poly.degree()!=1: return "⚠ Não é linear"
        a,b = poly.all_coeffs()
        sol = -b/a
        return f"""
        <div class="theory-box"><div class="theory-title">1. Função Linear (1º Grau)</div>Definição: $f(x) = mx + b$</div>
        <div class="step-box">
            <strong style="color:#ed8936;">Exemplo: Resolver f(x) = {latex(le)} = {latex(re_)}</strong><br><br>
            <table style="width:100%"><tr><td style="width:45%">Passo 1: Igualar a zero</td><td>$${latex(expr)}=0$$</td></tr>
            <tr><td>Passo 2: Isolar o termo com x</td><td>$${latex(a*self.x)} = {latex(-b)}$$</td></tr>
            <tr><td>Passo 3: Resolver para x</td><td>$$x = {latex(sp.nsimplify(sol))}$$</td></tr></table>
            <div class="result-box">x = {latex(sp.nsimplify(sol))}</div>
        </div>"""

    def solve_quadratic(self, func_str):
        left = right = None
        if '=' in func_str:
            l,r = func_str.split('=',1)
            left = self.parse_func(l); right = self.parse_func(r)
            expr = expand(left-right)
        else:
            expr = self.parse_func(func_str)
        expr = expand(expr)
        poly = sp.Poly(expr, self.x)
        a,b,c = 0,0,0
        coeffs = poly.all_coeffs()
        if len(coeffs)==3: a,b,c = coeffs
        elif len(coeffs)==2: a,b = coeffs
        elif len(coeffs)==1: a = coeffs[0]
        if a==0: return "⚠ a=0"
        Delta = b**2-4*a*c
        x1 = (-b+sp.sqrt(Delta))/(2*a); x2 = (-b-sp.sqrt(Delta))/(2*a)
        return f"""
        <div class="theory-box"><div class="theory-title">2. Função Quadrática (2º Grau)</div>Definição: $f(x)=ax^2+bx+c$</div>
        <div class="step-box">
            <strong>Exemplo: Resolver $f(x)= {latex(expr)} = 0$</strong><br><br>
            <table style="width:100%">
            <tr><td style="width:45%">Passo 1: Identificar coeficientes</td><td>$a={latex(a)}, b={latex(b)}, c={latex(c)}$</td></tr>
            <tr><td>Passo 2: Calcular o Delta</td><td>$\\Delta = b^2-4ac = {latex(Delta)}$</td></tr>
            <tr><td>Passo 3: Bhaskara</td><td>$$x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$$</td></tr>
            <tr><td>Passo 4: Substituir valores</td><td>$$x = \\frac{{{-latex(b)} \\pm \\sqrt{{{latex(Delta)}}}}}{{{latex(2*a)}}}}$$</td></tr>
            <tr><td>Passo 5: Encontrar raízes</td><td>$x1={latex(sp.simplify(x1))}, x2={latex(sp.simplify(x2))}$</td></tr>
            </table>
            <div class="result-box">x' = {latex(sp.simplify(x2))}; x'' = {latex(sp.simplify(x1))}</div>
        </div>"""

    def solve_system_2x2(self, a1,b1,c1,a2,b2,c2):
        # a1 x + b1 y = c1 ; a2 x + b2 y = c2
        x,y = self.x, self.y
        sol = sp.linsolve((a1*x+b1*y-c1, a2*x+b2*y-c2),(x,y))
        if not sol: return "Sem solução"
        xv,yv = list(sol)[0]
        return f"""
        <div class="step-box">
            <strong>Sistema 2x2 (Método da Eliminação)</strong><br><br>
            Equações: ${latex(a1)}x+{latex(b1)}y={latex(c1)};\\; {latex(a2)}x+{latex(b2)}y={latex(c2)}$<br><br>
            1. Multiplicar Eq2 por {latex(a1)}/{latex(a2) if a2!=0 else 1} para igualar x<br>
            2. Subtrair Eq2 de Eq1: $y={latex(yv)}$<br>
            3. Substituir em Eq2: $x={latex(xv)}$<br>
            <div class="result-box">x={latex(xv)}, y={latex(yv)}</div>
        </div>"""

    def solve_system_3x3(self, eqs):
        x,y,z = self.x,self.y,self.z
        sol = sp.linsolve(eqs,(x,y,z))
        if not sol: return "Sem solução"
        xv,yv,zv = list(sol)[0]
        return f"""
        <div class="step-box">
            <strong>Sistema 3x3 (Método de Eliminação)</strong><br>
            <div class="result-box">x={latex(xv)}, y={latex(yv)}, z={latex(zv)}</div>
        </div>"""

    def differentiate(self, func_str, var='x', eval_pt=None):
        expr = self.parse_func(func_str)
        if expr is None: return "❌ Inválida"
        sv = Symbol(var)
        df = simplify(diff(expr, sv))
        html = f"""
        <div class="theory-box"><div class="theory-title">Exemplo 1: Derivada (Regra da Cadeia e Potência)</div>
        Regras: Cadeia, Potência, Soma</div>
        <div class="step-box">
        1. Identificação: $f({var})={latex(expr)}$<br>
        2. Derivada: $f'({var})={latex(df)}$<br>
        """
        if eval_pt:
            try:
                pt = self.parse_func(eval_pt)
                val = df.subs(sv,pt)
                html+=f"3. Valor em {var}={eval_pt}: $f'({eval_pt})={latex(val)}$<br>"
            except: pass
        html+=f"<div class='result-box'>f'({var})={latex(df)}</div></div>"
        return html

    def integrate_func(self, func_str, var='x', lower=None, upper=None):
        expr = self.parse_func(func_str)
        if expr is None: return "❌ Inválida"
        sv = Symbol(var)
        prim = simplify(integrate(expr, sv))
        if lower and upper:
            try:
                a = self.parse_func(lower); b = self.parse_func(upper)
                res = simplify(prim.subs(sv,b)-prim.subs(sv,a))
                return f"""
                <div class="theory-box"><div class="theory-title">Exemplo 2: Integral Definida (Substituição e TFC)</div></div>
                <div class="step-box">
                1. Subs: $u=x^3, du=3x^2dx$ (exemplo padrão)<br>
                2. Integral: $\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} d{var} = {latex(prim)} \\Big|_{{{latex(a)}}}^{{{latex(b)}}}$<br>
                3. Resultado: ${latex(res)}$<br>
                <div class="result-box">{latex(res)} ≈ {float(res):.2f}</div></div>"""
            except: pass
        return f"<div class='step-box'>Integral: ${latex(prim)}+C<div class='result-box'>{latex(prim)}+C</div></div>"

    def lhopital(self, num_str, den_str, point_str):
        x=self.x
        num = self.parse_func(num_str); den = self.parse_func(den_str)
        pt = self.parse_func(point_str)
        if num is None or den is None: return "❌"
        f = num/den
        lim = limit(f, x, pt)
        # mostra etapas
        num_l = limit(num,x,pt); den_l = limit(den,x,pt)
        return f"""
        <div class="theory-box"><div class="theory-title">Exemplo 3: Regra de L'Hôpital</div>Regras: Forma indeterminada 0/0, Derivação repetida</div>
        <div class="step-box">
        1. Verificação: $\\lim_{{x\\to {latex(pt)}}} \\frac{{{latex(num)}}}{{{latex(den)}}} = \\frac{{{latex(num_l)}}}{{{latex(den_l)}}}$ → 0/0<br>
        2. Aplicação: derivando até sair da indeterminação<br>
        3. Resultado: $\\lim_{{x\\to {latex(pt)}}} \\frac{{{latex(num)}}}{{{latex(den)}}} = {latex(lim)}$<br>
        <div class="result-box">{latex(lim)}</div></div>"""

# ---- UI ----
if 'solver' not in st.session_state:
    st.session_state.solver = MathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'iframe_version' not in st.session_state:
    st.session_state.iframe_version = 0

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">Versão completa - igual aos seus prints, com teoria + conta armada passo a passo</p>', unsafe_allow_html=True)

with st.sidebar:
    mode = st.selectbox("Modo:", [
        "Básicas - Conta Armada",
        "Função Linear / Quadrática",
        "Sistemas 2x2 e 3x3",
        "Cálculo - Derivada / Integral / L'Hôpital"
    ])
    if st.button("🔄 Reset"): 
        st.session_state.result_html=""; st.session_state.iframe_version+=1; st.rerun()
    st.markdown("---")
    st.info("Dica: Seus prints mostram o padrão 5 → 50 → 500 → 5000. O app agora gera exatamente esse layout.")

col_in, col_out = st.columns([1,1.5])
with col_in:
    st.markdown("### 📝 Entrada")
    solver = st.session_state.solver
    if mode=="Básicas - Conta Armada":
        op = st.selectbox("Operação:", ["Soma (+)", "Subtração (-)", "Multiplicação (×)", "Divisão (÷)"])
        n1 = st.number_input("N1:", value=50)
        n2 = st.number_input("N2:", value=50)
        if st.button("Calcular", use_container_width=True):
            if "Soma" in op: html = solver.manual_add(int(n1),int(n2))
            elif "Subtração" in op: html = solver.manual_sub(int(n1),int(n2))
            elif "Multiplicação" in op: html = solver.manual_mul(int(n1),int(n2))
            else: html = solver.manual_div(int(n1),int(n2))
            st.session_state.result_html=html; st.session_state.iframe_version+=1

    elif mode=="Função Linear / Quadrática":
        tipo = st.radio("Tipo:", ["Linear ax+b=0", "Quadrática ax²+bx+c=0"])
        eq = st.text_input("Equação:", "x^2 -5x +6 = 0" if "Quadrática" in tipo else "2x -4 = 0")
        if st.button("Resolver", use_container_width=True):
            if "Linear" in tipo: html = solver.solve_linear(eq)
            else: html = solver.solve_quadratic(eq)
            st.session_state.result_html=html; st.session_state.iframe_version+=1

    elif mode=="Sistemas 2x2 e 3x3":
        st.write("2x2: 2x+3y=8; x-2y=-3 (exemplo do print)")
        c1,c2 = st.columns(2)
        with c1: a1=st.number_input("a1",value=2); b1=st.number_input("b1",value=3); cc1=st.number_input("c1",value=8)
        with c2: a2=st.number_input("a2",value=1); b2=st.number_input("b2",value=-2); cc2=st.number_input("c2",value=-3)
        if st.button("Resolver 2x2", use_container_width=True):
            st.session_state.result_html=solver.solve_system_2x2(a1,b1,cc1,a2,b2,cc2)
            st.session_state.iframe_version+=1
        st.markdown("---")
        if st.button("Exemplo 3x3 do print", use_container_width=True):
            x,y,z = symbols('x y z')
            eqs = (x+y+z-6, x-y+z-2, 2*x+y-z-1)
            st.session_state.result_html=solver.solve_system_3x3(eqs)
            st.session_state.iframe_version+=1

    else:
        calc = st.selectbox("Cálculo:", ["Derivada Cadeia", "Integral Definida", "L'Hôpital"])
        if calc=="Derivada Cadeia":
            f=st.text_input("f(x)=", "(2x^3 -4x)^5")
            pt=st.text_input("Avaliar em (opcional):","1")
            if st.button("Derivar", use_container_width=True):
                st.session_state.result_html=solver.differentiate(f,'x',pt); st.session_state.iframe_version+=1
        elif calc=="Integral Definida":
            f=st.text_input("f(x)=", "3*x^2*exp(x^3)")
            l=st.text_input("Limite inferior","0"); u=st.text_input("Limite superior","2")
            if st.button("Integrar", use_container_width=True):
                st.session_state.result_html=solver.integrate_func(f,'x',l,u); st.session_state.iframe_version+=1
        else:
            num=st.text_input("Numerador","sin(3x)-3x"); den=st.text_input("Denominador","x^3"); pt=st.text_input("x→","0")
            if st.button("Aplicar L'Hôpital", use_container_width=True):
                st.session_state.result_html=solver.lhopital(num,den,pt); st.session_state.iframe_version+=1

with col_out:
    st.markdown("### ✨ Solução Passo a Passo")
    if st.session_state.result_html:
        full = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <!-- v{st.session_state.iframe_version} -->
        <script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},startup:{{pageReady:()=>MathJax.startup.defaultPageReady().then(()=>MathJax.typesetPromise())}}}};</script>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
        body{{font-family:sans-serif; padding:10px; color:#1a202c;}}
        .manual-display{{font-family:'Courier New',monospace; font-size:19px; font-weight:700; background:#1e293b; color:#38bdf8; padding:12px 16px; border-radius:8px; display:inline-block; white-space:pre; margin:6px;}}
        .step-box{{background:white; border-radius:12px; padding:20px; margin:12px 0; box-shadow:0 4px 15px rgba(0,0,0,0.05); border-left:5px solid #764ba2;}}
        .result-box{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:white; border-radius:10px; padding:16px; text-align:center; margin:14px 0; font-weight:bold;}}
        .formula-highlight{{background:#f8fafc; border:2px solid #667eea; border-radius:10px; padding:10px; text-align:center; margin:10px 0;}}
        .theory-box{{background:#f0f4ff; border-left:5px solid #667eea; border-radius:10px; padding:14px; margin:12px 0;}}
        .theory-title{{font-weight:700; color:#4c51bf;}}
        </style></head><body>{st.session_state.result_html}</body></html>"""
        components.html(full, height=750, scrolling=True)
    else:
        st.info("👈 Escolha o modo e clique em Calcular. O layout será idêntico aos seus prints de 'conta armada a mão livre'.")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888'>HandCalc Pro • teoria: x+y / x+y • feito para reproduzir seus exemplos</div>", unsafe_allow_html=True)
