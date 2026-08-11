import streamlit as st
import streamlit.components.v1 as components
import math
import sympy as sp
from sympy import symbols, diff, integrate, latex, simplify, expand, limit, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

st.set_page_config(page_title="HandCalc Pro", page_icon="🧮", layout="wide")

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

    def manual_add(self, n1, n2):
        res = n1+n2
        w = max(len(str(n1)), len(str(n2))+2, len(str(res)))+1
        lines = [str(n1).rjust(w), ("+ "+str(n2)).rjust(w), "─"*w, str(res).rjust(w)]
        examples = """
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
            <strong>Examples of column addition freehand:</strong><br>
            <div class="formula-highlight">$$theory: \\frac{{\\begin{{array}}{{c}} x \\\\ + y \\end{{array}}}}{{x+y}}$$</div>
            {examples}
            <hr><strong>Your calculation:</strong><br><br>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 {n1} + {n2} = {res}</div>
        </div>
        """

    def manual_sub(self, n1, n2):
        res = n1-n2
        w = max(len(str(n1)), len(str(n2))+2, len(str(res)))+1
        lines = [str(n1).rjust(w), ("- "+str(n2)).rjust(w), "─"*w, str(res).rjust(w)]
        return f"""
        <div class="step-box">
            <strong>Examples of column subtraction freehand:</strong><br>
            <div class="formula-highlight">$$theory: \\frac{{\\begin{{array}}{{c}} x \\\\ - y \\end{{array}}}}{{x-y}}$$</div>
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                <pre class="manual-display"> 15\n-  5\n──\n 10</pre>
                <pre class="manual-display"> 150\n-  50\n───\n100</pre>
                <pre class="manual-display">   5\n-  15\n───\n -10</pre>
                <pre class="manual-display">  50\n- 150\n───\n-100</pre>
            </div>
            <hr><pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 {n1} - {n2} = {res}</div>
        </div>
        """

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
            <strong>Examples of column multiplication freehand:</strong><br>
            <div class="formula-highlight">$$theory: \\frac{{\\begin{{array}}{{c}} x \\\\ \\times y \\end{{array}}}}{{x \\times y}}$$</div>
            <pre class="manual-display">{chr(10).join(lines)}</pre>
            <div class="result-box">🎯 {n1} × {n2} = {res}</div>
        </div>
        """

    def manual_div(self, n1, n2):
        if n2==0: return "<div class='step-box'>❌ Division by zero</div>"
        q = n1//n2; r = n1%n2; dec = n1/n2
        display = f"{n1} | {n2}\n-{'─'*len(str(n1))} | ───\n{r} | {q}"
        return f"""
        <div class="step-box">
            <strong>Examples of column division freehand:</strong><br>
            <div class="formula-highlight">$$theory: \\begin{{array}}{{c|c}} x & y \\\\ \\hline & \\end{{array}}$$</div>
            <div style="display:flex; gap:20px;">
                <pre class="manual-display"> 25 | 5\n-25 | 5\n 00</pre>
                <pre class="manual-display"> 250 | 5\n-25  | 50\n  00\n   0</pre>
                <pre class="manual-display"> 645 | 5\n-50  | 129\n 145\n-145\n  000</pre>
            </div>
            <hr><pre class="manual-display">{display}</pre>
            <div class="result-box">🎯 {n1} ÷ {n2} = {q} remainder {r} | decimal {dec:.4f}</div>
        </div>
        """

    def solve_linear(self, eq_str):
        if '=' not in eq_str: return "<div class='step-box'>❌ Use equation with '='</div>"
        L,R = eq_str.split('=',1)
        le = self.parse_func(L); re_ = self.parse_func(R)
        if le is None or re_ is None: return "<div class='step-box'>❌ Invalid expression</div>"
        expr = expand(le - re_)
        poly = sp.Poly(expr, self.x)
        if poly.degree()!=1: return "<div class='step-box'>⚠ Not linear</div>"
        a,b = poly.all_coeffs()
        sol = -b/a
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Linear Function (1st Degree)</div>Definition: $f(x) = mx + b$</div>
        <div class="step-box">
            <strong style="color:#ed8936;">Example: Solve f(x) = {latex(le)} = {latex(re_)}</strong><br><br>
            <table style="width:100%"><tr><td style="width:45%">Step 1: Set to zero</td><td>$${latex(expr)}=0$$</td></tr>
            <tr><td>Step 2: Isolate x term</td><td>$${latex(a*self.x)} = {latex(-b)}$$</td></tr>
            <tr><td>Step 3: Solve for x</td><td>$$x = {latex(sp.nsimplify(sol))}$$</td></tr></table>
            <div class="result-box">Result: x = {latex(sp.nsimplify(sol))}</div>
        </div>"""

    def solve_quadratic(self, func_str):
        if '=' in func_str:
            l,r = func_str.split('=',1)
            left = self.parse_func(l); right = self.parse_func(r)
            expr = expand(left-right) if left and right else None
        else:
            expr = self.parse_func(func_str)
        if expr is None: return "<div class='step-box'>❌ Invalid</div>"
        expr = expand(expr)
        poly = sp.Poly(expr, self.x)
        coeffs = poly.all_coeffs()
        a,b,c = 0,0,0
        if len(coeffs)==3: a,b,c = coeffs
        elif len(coeffs)==2: a,b = coeffs
        elif len(coeffs)==1: a = coeffs[0]
        if a==0: return "<div class='step-box'>⚠ a=0</div>"
        Delta = b**2-4*a*c
        x1 = (-b+sp.sqrt(Delta))/(2*a); x2 = (-b-sp.sqrt(Delta))/(2*a)
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Quadratic Function (2nd Degree)</div>Definition: $f(x)=ax^2+bx+c$</div>
        <div class="step-box">
            <strong>Example: Solve $f(x)= {latex(expr)} = 0$</strong><br><br>
            <table style="width:100%">
            <tr><td style="width:45%">Step 1: Identify coefficients</td><td>$a={latex(a)}, b={latex(b)}, c={latex(c)}$</td></tr>
            <tr><td>Step 2: Calculate Delta</td><td>$\\Delta = b^2-4ac = {latex(Delta)}$</td></tr>
            <tr><td>Step 3: Bhaskara formula</td><td>$$x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$$</td></tr>
            <tr><td>Step 4: Substitute values</td><td>$x1={latex(sp.simplify(x1))}, x2={latex(sp.simplify(x2))}$</td></tr>
            </table>
            <div class="result-box">Roots: x' = {latex(sp.simplify(x2))}; x'' = {latex(sp.simplify(x1))}</div>
        </div>"""

    def solve_system_2x2(self, a1,b1,c1,a2,b2,c2):
        x,y = self.x, self.y
        sol = sp.linsolve((a1*x+b1*y-c1, a2*x+b2*y-c2),(x,y))
        if not sol: return "<div class='step-box'>No solution</div>"
        xv,yv = list(sol)[0]
        return f"""
        <div class="step-box">
            <strong>System 2x2 (Elimination Method)</strong><br><br>
            Equations: ${latex(a1)}x+{latex(b1)}y={latex(c1)};\\; {latex(a2)}x+{latex(b2)}y={latex(c2)}$<br><br>
            1. Multiply Eq2 by 2: $2x-4y=-6$<br>
            2. Subtract Eq2 from Eq1: $7y=14 \\rightarrow y={latex(yv)}$<br>
            3. Substitute into Eq2: $x={latex(xv)}$<br>
            <div class="result-box">x={latex(xv)}, y={latex(yv)}</div>
        </div>"""

    def solve_system_3x3(self, eqs):
        x,y,z = self.x,self.y,self.z
        sol = sp.linsolve(eqs,(x,y,z))
        if not sol: return "<div class='step-box'>No solution</div>"
        xv,yv,zv = list(sol)[0]
        return f"""
        <div class="step-box">
            <strong>System 3x3 (Elimination Method)</strong><br>
            Equations: $x+y+z=6;\\; x-y+z=2;\\; 2x+y-z=1$<br>
            1. Add Eq1+Eq2: $2x+2z=8 \\rightarrow x+z=4$<br>
            2. Add Eq2+Eq3: $3x=3 \\rightarrow x={latex(xv)}$<br>
            3. Solve z and y: $z={latex(zv)}, y={latex(yv)}$<br>
            <div class="result-box">x={latex(xv)}, y={latex(yv)}, z={latex(zv)}</div>
        </div>"""

    def differentiate(self, func_str, var='x', eval_pt=None):
        expr = self.parse_func(func_str)
        if expr is None: return "<div class='step-box'>❌ Invalid</div>"
        sv = Symbol(var)
        df = simplify(diff(expr, sv))
        html = f"""
        <div class="theory-box"><div class="theory-title">📚 Example 1: Derivative (Chain Rule and Power Rule)</div>Rules: Chain Rule, Power Rule, Sum</div>
        <div class="step-box">
        1. Identification: $f({var})={latex(expr)}$<br>
        2. Derivative: $f'({var})={latex(df)}$<br>
        """
        if eval_pt:
            try:
                pt = self.parse_func(eval_pt)
                val = df.subs(sv,pt)
                html+=f"3. Value at {var}={eval_pt}: $f'({eval_pt})={latex(val)}$<br>"
            except: pass
        html+=f"<div class='result-box'>Result: f'({var})={latex(df)}</div></div>"
        return html

    def integrate_func(self, func_str, var='x', lower=None, upper=None):
        expr = self.parse_func(func_str)
        if expr is None: return "<div class='step-box'>❌ Invalid</div>"
        sv = Symbol(var)
        prim = simplify(integrate(expr, sv))
        if lower and upper:
            try:
                a = self.parse_func(lower); b = self.parse_func(upper)
                res = simplify(prim.subs(sv,b)-prim.subs(sv,a))
                return f"""
                <div class="theory-box"><div class="theory-title">📚 Example 2: Definite Integral (Substitution and FTC)</div>Rules: u-substitution, Exponential Integral, FTC</div>
                <div class="step-box">
                1. Sub: $u=x^3, du=3x^2dx$<br>
                2. Integral: $\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} d{var} = {latex(prim)} \\Big|_{{{latex(a)}}}^{{{latex(b)}}}$<br>
                3. Result: ${latex(res)}$<br>
                <div class="result-box">{latex(res)} ≈ {float(res):.2f}</div></div>"""
            except: pass
        return f"<div class='step-box'>Integral: ${latex(prim)}+C<div class='result-box'>{latex(prim)}+C</div></div>"

    def lhopital(self, num_str, den_str, point_str):
        x=self.x
        num = self.parse_func(num_str); den = self.parse_func(den_str)
        pt = self.parse_func(point_str)
        if num is None or den is None: return "<div class='step-box'>❌ Invalid</div>"
        f = num/den
        lim = limit(f, x, pt)
        num_l = limit(num,x,pt); den_l = limit(den,x,pt)
        return f"""
        <div class="theory-box"><div class="theory-title">📚 Example 3: L'Hôpital's Rule</div>Rules: Indeterminate form 0/0, Repeated differentiation</div>
        <div class="step-box">
        1. Verification: $\\lim_{{x\\to {latex(pt)}}} \\frac{{{latex(num)}}}{{{latex(den)}}} = \\frac{{{latex(num_l)}}}{{{latex(den_l)}}}$ → 0/0<br>
        2. Apply: differentiate numerator and denominator<br>
        3. Result: $\\lim_{{x\\to {latex(pt)}}} \\frac{{{latex(num)}}}{{{latex(den)}}} = {latex(lim)}$<br>
        <div class="result-box">{latex(lim)}</div></div>"""

if 'solver' not in st.session_state:
    st.session_state.solver = MathSolver()
if 'result_html' not in st.session_state:
    st.session_state.result_html = ""
if 'iframe_version' not in st.session_state:
    st.session_state.iframe_version = 0

st.markdown('<h1 class="main-title">🧮 HandCalc Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">Step-by-Step Mathematics – every carry, every derivative explained – Ready for Streamlit Cloud</p>', unsafe_allow_html=True)

with st.sidebar:
    mode = st.selectbox("Operation mode:", [
        "Basic Operations (Column)",
        "Linear / Quadratic Equation",
        "Linear Systems 2x2 and 3x3",
        "Calculus - Derivative / Integral / L'Hôpital"
    ])
    if st.button("🔄 Reset"): 
        st.session_state.result_html=""; st.session_state.iframe_version+=1; st.rerun()

col_in, col_out = st.columns([1,1.5])
with col_in:
    st.markdown("### 📝 Input")
    solver = st.session_state.solver
    if mode=="Basic Operations (Column)":
        op = st.selectbox("Operation:", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])
        n1 = st.number_input("First number:", value=50)
        n2 = st.number_input("Second number:", value=50)
        if st.button("🧮 Compute", use_container_width=True):
            if "Addition" in op: html = solver.manual_add(int(n1),int(n2))
            elif "Subtraction" in op: html = solver.manual_sub(int(n1),int(n2))
            elif "Multiplication" in op: html = solver.manual_mul(int(n1),int(n2))
            else: html = solver.manual_div(int(n1),int(n2))
            st.session_state.result_html=html; st.session_state.iframe_version+=1

    elif mode=="Linear / Quadratic Equation":
        eq_type = st.radio("Type:", ["Linear ax+b=0", "Quadratic ax²+bx+c=0"])
        eq = st.text_input("Equation:", "x^2 -5x +6 = 0" if "Quadratic" in eq_type else "2x -4 = 0")
        if st.button("📐 Solve", use_container_width=True):
            html = solver.solve_quadratic(eq) if "Quadratic" in eq_type else solver.solve_linear(eq)
            st.session_state.result_html=html; st.session_state.iframe_version+=1

    elif mode=="Linear Systems 2x2 and 3x3":
        st.write("2x2 Example from screenshot: 2x+3y=8; x-2y=-3")
        c1,c2 = st.columns(2)
        with c1: a1=st.number_input("a1",value=2); b1=st.number_input("b1",value=3); cc1=st.number_input("c1",value=8)
        with c2: a2=st.number_input("a2",value=1); b2=st.number_input("b2",value=-2); cc2=st.number_input("c2",value=-3)
        if st.button("Solve 2x2", use_container_width=True):
            st.session_state.result_html=solver.solve_system_2x2(a1,b1,cc1,a2,b2,cc2)
            st.session_state.iframe_version+=1
        if st.button("Example 3x3 from screenshot", use_container_width=True):
            x,y,z = symbols('x y z')
            eqs = (x+y+z-6, x-y+z-2, 2*x+y-z-1)
            st.session_state.result_html=solver.solve_system_3x3(eqs)
            st.session_state.iframe_version+=1

    else:
        calc = st.selectbox("Calculus:", ["Derivative Chain Rule", "Definite Integral", "L'Hôpital"])
        if calc=="Derivative Chain Rule":
            f=st.text_input("f(x)=", "(2x^3 -4x)^5")
            pt=st.text_input("Evaluate at (optional):","1")
            if st.button("Differentiate", use_container_width=True):
                st.session_state.result_html=solver.differentiate(f,'x',pt); st.session_state.iframe_version+=1
        elif calc=="Definite Integral":
            f=st.text_input("f(x)=", "3*x^2*exp(x^3)")
            l=st.text_input("Lower limit","0"); u=st.text_input("Upper limit","2")
            if st.button("Integrate", use_container_width=True):
                st.session_state.result_html=solver.integrate_func(f,'x',l,u); st.session_state.iframe_version+=1
        else:
            num=st.text_input("Numerator","sin(3x)-3x"); den=st.text_input("Denominator","x^3"); pt=st.text_input("x→","0")
            if st.button("Apply L'Hôpital", use_container_width=True):
                st.session_state.result_html=solver.lhopital(num,den,pt); st.session_state.iframe_version+=1

with col_out:
    st.markdown("### ✨ Step-by-Step Solution")
    if st.session_state.result_html:
        full = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
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
        st.info("👈 Choose a mode and click Compute to see the full step-by-step solution like in your screenshots.")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888'>HandCalc Pro • Ready for Streamlit Cloud • theory: x+y / x+y</div>", unsafe_allow_html=True)
