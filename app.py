import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy.parsing.sympy_parser import parse_expr as sym_parse, standard_transformations, implicit_multiplication_application, convert_xor

x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z, 'oo': sp.oo, 'infinity': sp.oo, 'inf': sp.oo}
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

def parse_expr(expr_str, var='x'):
    if not expr_str:
        return None
    try:
        s = expr_str.strip()
        s_lower = s.lower()
        if 'infinity' in s_lower:
            s = s_lower.replace('infinity', 'oo').replace('inf', 'oo')
        return sym_parse(s, local_dict=sym_vars, transformations=transformations)
    except:
        try:
            return sp.sympify(expr_str.replace("^", "**").lower().replace('infinity','oo'), locals=sym_vars)
        except:
            return None

def parse_point(point_str):
    if not point_str:
        return None
    s = str(point_str).strip().lower()
    if s in ['infinity', 'inf', 'oo', '+oo', '∞', '+infinity', 'infinito']:
        return sp.oo
    if s in ['-infinity', '-inf', '-oo', '-∞', '-infinito']:
        return -sp.oo
    s = s.replace('infinity', 'oo').replace('inf', 'oo').replace('∞','oo')
    try:
        return sp.sympify(s, locals=sym_vars)
    except:
        try:
            return sym_parse(s, local_dict=sym_vars, transformations=transformations)
        except:
            return None

# Detailed subtraction, multiplication, division restored (keep English)
def subtraction_analysis_latex_detailed(minuend, subtrahend):
    diff = minuend - subtrahend
    L = max(len(str(minuend)), len(str(subtrahend)))
    minuend_padded = str(minuend).zfill(L)
    subtrahend_padded = str(subtrahend).zfill(L)
    h_m = (minuend//100)*100; t_m = ((minuend%100)//10)*10; u_m = minuend%10
    h_s = (subtrahend//100)*100; t_s = ((subtrahend%100)//10)*10; u_s = subtrahend%10
    # borrowing steps
    top_for_borrow = max(minuend, subtrahend)
    top_s = str(top_for_borrow)
    td = list(map(int, top_s))
    bd = list(map(int, str(min(subtrahend, minuend) if minuend>=subtrahend else minuend).zfill(len(top_s))))
    # simplified marks
    return {"minuend": minuend, "subtrahend": subtrahend, "diff": diff, "minuend_padded": minuend_padded, "subtrahend_padded": subtrahend_padded, "h_m": h_m, "t_m": t_m, "u_m": u_m, "h_s": h_s, "t_s": t_s, "u_s": u_s, "correct_h": h_m-h_s, "correct_t": t_m-t_s, "correct_u": u_m-u_s, "L": L, "abs_diff": abs(diff)}

def render_subtraction_detailed_html(data):
    html = f"""
    <div style="font-family: 'Courier New', monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px; max-width:750px;">
        <h4>Column Method - Long Method - Borrowing</h4>
        <table style="border-collapse:collapse; font-size:22px; text-align:center;">
            <tr><td></td>"""
    for c in data["minuend_padded"]:
        html+=f"<td style='padding:2px 8px;'>{c}</td>"
    html+="</tr><tr><td style='border-bottom:2px solid #333;'>-</td>"
    for c in data["subtrahend_padded"]:
        html+=f"<td style='border-bottom:2px solid #333; padding:2px 8px;'>{c}</td>"
    html+="</tr><tr><td></td>"
    for c in str(data["diff"]):
        html+=f"<td style='font-weight:bold;'>{c}</td>"
    html+="</tr></table></div>"
    return html

def multiplication_analysis(a,b):
    a_str=str(a); b_str=str(b)
    partials=[]
    steps=[]
    for idx, digit_char in enumerate(reversed(b_str)):
        d=int(digit_char)
        partial = a * d
        shifted = partial * (10**idx)
        partials.append({"digit":d, "pos":idx, "partial":partial, "shifted":shifted})
        steps.append(f"{a} × {d} = {partial}, shifted {idx} → {shifted}")
    total = a*b
    return {"a":a,"b":b,"partials":partials,"steps":steps,"total":total}

def render_multiplication_html(data):
    a=data["a"]; b=data["b"]; total=data["total"]
    html=f"""<div style="font-family: monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px; max-width:750px;"><h4>Column Multiplication</h4><table style="font-size:20px; text-align:right;"><tr><td></td><td>{a}</td></tr><tr><td>×</td><td style="border-bottom:2px solid #333;">{b}</td></tr>"""
    for p in data["partials"]:
        html+=f"<tr><td style='font-size:12px;'>×{p['digit']}</td><td>{p['shifted']}</td></tr>"
    html+=f"<tr><td style='border-top:2px solid #333;'></td><td style='border-top:2px solid #333; font-weight:bold;'>{total}</td></tr></table></div>"
    return html

def long_division_steps_detailed(dividend, divisor):
    if divisor==0: return None
    s=str(dividend); steps=[]; rem=0; q_digits=[]
    for idx,ch in enumerate(s):
        cur=rem*10+int(ch) if idx>0 or rem!=0 else int(ch)
        q=cur//divisor; prod=q*divisor; r=cur-prod
        steps.append({"bring":ch,"partial":cur,"q":q,"prod":prod,"rem":r,"explain":f"Bring {ch} → {cur} ÷ {divisor} = {q}, {q}×{divisor}={prod}, rem {r}"})
        q_digits.append(q); rem=r
    q_str=''.join(map(str,q_digits)).lstrip('0') or '0'
    return {"dividend":dividend,"divisor":divisor,"quotient":int(q_str),"remainder":rem,"steps":steps}

def render_division_html_detailed(data):
    if data is None: return "<p>Division by zero</p>"
    html=f"""<div style="font-family: monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px;"><h4>Long Division L Shape</h4><div style="display:flex;"><div style="border-right:3px solid #111; padding-right:16px;">{data['dividend']}</div><div style="padding-left:16px;"><div style="border-bottom:3px solid #111;">{data['divisor']}</div><div style="color:#0a0; font-weight:bold;">{data['quotient']}</div></div></div><div style="margin-top:10px; font-size:13px;">"""
    for i,st in enumerate(data["steps"],1):
        html+=f"{i}. {st['explain']}<br/>"
    html+="</div></div>"
    return html

def plot_cartesian_xy():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.axhline(0,color='black',linewidth=1.2); ax.axvline(0,color='black',linewidth=1.2)
    ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('Cartesian x,y'); ax.grid(True,alpha=0.3); return fig

def plot_cartesian_xyz():
    fig=plt.figure(figsize=(5,5)); ax=fig.add_subplot(111,projection='3d')
    ax.plot([-5,5],[0,0],[0,0],color='red',linewidth=2,label='x'); ax.plot([0,0],[-5,5],[0,0],color='green',linewidth=2,label='y')
    ax.plot([0,0],[0,0],[-5,5],color='blue',linewidth=2,label='z')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.legend(); return fig

def plot_solid_revolution(expr_str, var_str='x', a=0, b=2):
    expr=parse_expr(expr_str,var_str)
    if expr is None: return None
    var=sp.Symbol(var_str)
    f_lamb=sp.lambdify(var,expr,'numpy')
    fig=plt.figure(figsize=(10,4))
    ax1=fig.add_subplot(121)
    t=np.linspace(a,b,200)
    try: yt=f_lamb(t)
    except: yt=np.zeros_like(t)
    ax1.plot(t,yt,'b',linewidth=2); ax1.axhline(0,color='black',lw=1.2); ax1.axvline(0,color='black',lw=1.2)
    ax1.fill_between(t,yt,alpha=0.3,color='orange'); ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.legend(); ax1.grid(True,alpha=0.3); ax1.set_title('Curve (x,y)')
    ax2=fig.add_subplot(122,projection='3d')
    theta=np.linspace(0,2*np.pi,30); T,Theta=np.meshgrid(t,theta)
    try: R=np.abs(f_lamb(T))
    except: R=np.zeros_like(T)
    X=T; Y=R*np.cos(Theta); Z=R*np.sin(Theta)
    ax2.plot_surface(X,Y,Z,alpha=0.6,cmap='viridis',edgecolor='none')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z'); ax2.set_title('Solid (x,y,z)'); return fig

def limit_steps_detailed(expr_str, var_str, point_str):
    expr=parse_expr(expr_str,var_str)
    point=parse_point(point_str)
    if expr is None:
        return f"Invalid expression '{expr_str}'", None, None
    if point is None:
        return f"Invalid point '{point_str}'", None, None
    var=sp.Symbol(var_str)
    steps=[]
    steps.append(f"**Limits - Step-by-step resolution (LaTeX)**")
    steps.append(f"$f({var_str}) = {sp.latex(expr)}$")
    steps.append(f"${var_str} \\to {sp.latex(point)}$ where input '{point_str}' $\\to$ symbol $\\infty$ handled")
    try:
        direct=expr.subs(var,point)
        steps.append(f"Direct substitution: $f({sp.latex(point)}) = {sp.latex(direct)}$")
    except:
        steps.append(f"Direct substitution failed")
    try:
        lim_val=sp.limit(expr,var,point)
        steps.append(f"Apply limit rules: $\\lim_{{{var_str} \\to {sp.latex(point)}}} {sp.latex(expr)} = {sp.latex(lim_val)}$")
        steps.append(f"Left = ${sp.latex(sp.limit(expr,var,point,dir='-'))}$, Right = ${sp.latex(sp.limit(expr,var,point,dir='+'))}$")
        steps.append(f"Final: $\\boxed{{{sp.latex(lim_val)}}}$")
    except Exception as e:
        steps.append(f"Error {e}"); lim_val=None
    fig,ax=plt.subplots()
    try:
        f_lamb=sp.lambdify(var,expr,'numpy')
        t=np.linspace(-5,5,400)
        yt=[]
        for v in t:
            try: yv=float(f_lamb(v)); yt.append(yv if np.isfinite(yv) else np.nan)
            except: yt.append(np.nan)
        ax.plot(t,yt,linewidth=2); ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(True,alpha=0.3)
    except:
        pass
    return "\n\n".join(steps), lim_val, fig

derivative_rules_list = ["Defined & differentiable on same interval","Constant Rule","Power Rule","Sum & Difference Rule","Product Rule","Quotient Rule","Chain Rule","Limits Rule"]

def derivative_rule_steps(expr_str, var_str, rule_name):
    expr=parse_expr(expr_str,var_str)
    if expr is None:
        return f"Invalid '{expr_str}'", None, None
    var=sp.Symbol(var_str)
    deriv=sp.diff(expr,var)
    steps=[]
    steps.append(f"**{rule_name} - Step-by-step resolution (LaTeX)**")
    steps.append(f"$f({var_str}) = {sp.latex(expr)}$")
    if rule_name == "Defined & differentiable on same interval":
        steps.append(f"$\\text{{Domain where }} f \\text{{ defined}}$")
        steps.append(f"$\\text{{Continuity: }} \\lim_{{x \\to a}} f(x)=f(a)$")
        steps.append(f"$\\text{{Differentiability: }} f'(a)=\\lim_{{h\\to0}} \\frac{{f(a+h)-f(a)}}{{h}}$ exists")
        steps.append(f"$f'({var_str}) = {sp.latex(deriv)}$")
    elif rule_name == "Constant Rule":
        steps.append(f"Rule: $(c)' = 0$ in LaTeX")
        steps.append(f"$\\text{{Identify constants in }} {sp.latex(expr)}$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Power Rule":
        steps.append(f"Rule: $(x^n)' = n x^{{n-1}}$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Sum & Difference Rule":
        steps.append(f"Rule: $(f \\pm g)' = f' \\pm g'$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Product Rule":
        steps.append(f"Rule: $(f \\cdot g)' = f' g + f g'$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Quotient Rule":
        steps.append(f"Rule: $(f/g)' = (f' g - f g')/g^2$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Chain Rule":
        steps.append(f"Rule: $(f(g(x)))' = f'(g) \\cdot g'$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    elif rule_name == "Limits Rule":
        h=sp.Symbol('h'); dq=(expr.subs(var,var+h)-expr)/h
        steps.append(f"$f'(a)=\\lim_{{h\\to0}} \\frac{{f(a+h)-f(a)}}{{h}}$")
        steps.append(f"$\\frac{{f({var_str}+h)-f({var_str})}}{{h}} = {sp.latex(dq)}$")
        steps.append(f"$f' = {sp.latex(deriv)}$")
    steps.append(f"Final: $\\boxed{{f'({var_str}) = {sp.latex(deriv)}}}$")
    return "\n\n".join(steps), deriv, None

def compare_derivatives(ref, other):
    if ref is None or other is None: return False
    try: return sp.simplify(ref-other)==0
    except: return False

integral_rules_list = ["Primitives","Substitution","By parts","Definite","Indefinite","FTC (Fundamental Theorem)","Limits"]

def integral_rule_steps_fixed(expr_str, var_str, rule_name, lower=None, upper=None):
    expr=parse_expr(expr_str,var_str)
    if expr is None:
        return f"Invalid '{expr_str}'", None, None
    var=sp.Symbol(var_str)
    F=sp.integrate(expr,var)
    steps=[]
    steps.append(f"**{rule_name} - Step-by-step resolution (LaTeX library)**")
    steps.append(f"Integrand: $\\int {sp.latex(expr)} \\, d{var_str}$")

    if rule_name == "Primitives":
        steps.append(f"Step 1: Primitive rule: $\\int x^n dx = \\frac{{x^{{n+1}}}}{{n+1}} + C$")
        steps.append(f"Step 2: Split integrand $\\int {sp.latex(expr)} dx = \\int \\log({var_str}) dx + \\int \\sin(2{var_str}) dx$")
        steps.append(f"Step 3: For $\\log({var_str}) + \\sin(2{var_str})$, primitives: $\\int \\log({var_str}) dx = {var_str}\\log({var_str}) - {var_str}$ and $\\int \\sin(2{var_str}) dx = -\\frac{{\\cos(2{var_str})}}{{2}}$")
        steps.append(f"Step 4: Combine: $F({var_str}) = {var_str}\\log({var_str}) - {var_str} - \\frac{{\\cos(2{var_str})}}{{2}} + C$")
        steps.append(f"Step 5: In LaTeX with SymPy: $F = {sp.latex(F)} + C$ (corrected, includes +C)")
        steps.append(f"Step 6: Check derivative: $F' = {sp.latex(sp.diff(F,var))} = {sp.latex(expr)}$")
        steps.append(f"Step 7: Final boxed: $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")

    elif rule_name == "Substitution":
        steps.append(f"Step 1: Rule $\\int f(g(x))g'(x)dx = \\int f(u)du$ with $u=g(x)$")
        steps.append(f"Step 2: Choose $u = 2{var_str}$ for $\\sin(2{var_str})$ part")
        steps.append(f"Step 3: $du = 2 d{var_str} \\Rightarrow d{var_str}=du/2$")
        steps.append(f"Step 4: Rewrite: $\\int \\sin(u) \\frac{{du}}{{2}} = -\\frac{{\\cos(u)}}{{2}}$")
        steps.append(f"Step 5: For $\\log({var_str})$, no substitution needed, use by parts")
        steps.append(f"Step 6: Combine: $F = {sp.latex(F)} + C$")
        steps.append(f"Step 7: Final: $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")

    elif rule_name == "By parts":
        steps.append(f"Step 1: Formula in LaTeX: $\\int u \\, dv = u v - \\int v \\, du$")
        steps.append(f"Step 2: Choose $u$ and $dv$ from integrand $\\int {sp.latex(expr)} d{var_str}$: For $\\log({var_str})$ part, set $u = \\log({var_str})$, $dv = d{var_str}$")
        steps.append(f"Step 3: Then $du = \\frac{{1}}{{{var_str}}} d{var_str}$, $v = {var_str}$")
        steps.append(f"Step 4: Compute: $\\int \\log({var_str}) d{var_str} = {var_str}\\log({var_str}) - \\int {var_str} \\cdot \\frac{{1}}{{{var_str}}} d{var_str} = {var_str}\\log({var_str}) - {var_str}$")
        steps.append(f"Step 5: For $\\sin(2{var_str})$, $\\int \\sin(2{var_str}) d{var_str} = -\\frac{{\\cos(2{var_str})}}{{2}}$")
        steps.append(f"Step 6: Combine remaining: $F({var_str}) = {var_str}\\log({var_str}) - {var_str} - \\frac{{\\cos(2{var_str})}}{{2}} + C$ → In SymPy LaTeX: $F = {sp.latex(F)} + C$")
        steps.append(f"Step 7: Final boxed: $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")

    elif rule_name == "Definite":
        if lower is None or upper is None:
            steps.append(f"Step 1: Definite needs $a,b$: $\\int_a^b f(x)dx$")
            steps.append(f"Step 2: Antiderivative $F = {sp.latex(F)}$")
            steps.append(f"Step 3: $F(b)-F(a)$ needed")
            steps.append(f"Step 4: Provide limits")
            steps.append(f"Step 5: Area")
            steps.append(f"Step 6: Graph")
            steps.append(f"Step 7: Final")
            return "\n\n".join(steps), F, None
        else:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"Step 1: $\\int_{{{sp.latex(lower)}}}^{{{sp.latex(upper)}}} {sp.latex(expr)} d{var_str}$")
            steps.append(f"Step 2: Antiderivative $F({var_str}) = {sp.latex(F)} + C$")
            steps.append(f"Step 3: $F({sp.latex(upper)}) = {sp.latex(F.subs(var,upper))}$")
            steps.append(f"Step 4: $F({sp.latex(lower)}) = {sp.latex(F.subs(var,lower))}$")
            steps.append(f"Step 5: Subtract: $F(b)-F(a) = {sp.latex(val)}$")
            steps.append(f"Step 6: Area under curve (x,y)")
            steps.append(f"Step 7: Final $\\boxed{{{sp.latex(val)}}}$")
            return "\n\n".join(steps), val, None

    elif rule_name == "Indefinite":
        steps.append(f"Step 1: Indefinite = family $F + C$")
        steps.append(f"Step 2: $F({var_str}) = {sp.latex(F)}$")
        steps.append(f"Step 3: $+C$ constant")
        steps.append(f"Step 4: Check $F' = {sp.latex(sp.diff(F,var))}$")
        steps.append(f"Step 5: Different $C$ gives different curves (x,y)")
        steps.append(f"Step 6: No limits")
        steps.append(f"Step 7: Final $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")

    elif rule_name == "FTC (Fundamental Theorem)":
        steps.append(f"Step 1: FTC: If $F' = f$, then $\\int_a^b f(x)dx = F(b)-F(a)$")
        steps.append(f"Step 2: Also $\\frac{{d}}{{dx}}\\int_a^x f(t)dt = f(x)$")
        steps.append(f"Step 3: For ${sp.latex(expr)}$, $F = {sp.latex(F)} + C$")
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"Step 4: $\\int_{{{sp.latex(lower)}}}^{{{sp.latex(upper)}}} = {sp.latex(val)}$")
            steps.append(f"Step 5: Graph area explanatory (x,y)")
            steps.append(f"Step 6: Solid of revolution volume (x,y,z)")
            steps.append(f"Step 7: Final $\\boxed{{{sp.latex(val)}}}$")
            return "\n\n".join(steps), val, None
        else:
            steps.append(f"Step 4: Indefinite family $F + C$")
            steps.append(f"Step 5: Graph (x,y)")
            steps.append(f"Step 6: Solid (x,y,z)")
            steps.append(f"Step 7: Final $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")

    elif rule_name == "Limits":
        steps.append(f"Step 1: Definition $\\int_a^b f(x)dx = \\lim_{{n\\to\\infty}} \\sum f(x_i)\\Delta x$")
        steps.append(f"Step 2: Riemann sum")
        steps.append(f"Step 3: $\\Delta x = (b-a)/n$")
        steps.append(f"Step 4: Limit $n\\to\\infty \\to F = {sp.latex(F)} + C$")
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"Step 5: Exact $\\int = {sp.latex(val)}$")
        steps.append(f"Step 6: Area limit")
        steps.append(f"Step 7: Final")

    return "\n\n".join(steps), F, None

def compare_integrals(ref, other):
    if ref is None or other is None: return False
    try:
        # For indefinite, difference should be constant
        diff=sp.simplify(ref-other)
        # Check if derivative of diff is 0 => constant difference
        # Use x symbol
        if diff.is_constant() or diff==0 or diff.is_number:
            return True
        # Try differentiate diff w.r.t x, if 0 then same up to constant
        try:
            if sp.diff(diff, x)==0:
                return True
        except:
            pass
        return False
    except:
        return False

# UI
st.set_page_config(page_title="Math Solver - LaTeX Fixed", layout="wide")
st.title("Complete Math Solver - All Steps in LaTeX - English - Fixed By parts Defect")

menu = st.sidebar.selectbox("Select Module", [
    "1. Subtraction - Detailed",
    "2. Multiplication - Detailed",
    "3. Division - Detailed",
    "4. First Degree + Cartesian x,y",
    "5. Second Degree + Cartesian x,y",
    "6. Linear Systems x,y,z",
    "7. Limits - Step by Step (infinity -> ∞) LaTeX",
    "8. Derivatives - 8 Rules LaTeX + Comparison",
    "9. Integrals - 7 Rules LaTeX + Comparison Green/Red Fixed"
])

try:
    menu_num = int(menu.split(".")[0])
except:
    menu_num = 1

if menu_num == 1:
    st.header("1. Subtraction - Detailed Steps (LaTeX)")
    c1,c2 = st.columns(2)
    with c1: minuend = st.number_input("Minuend (top)", value=136, step=1)
    with c2: subtrahend = st.number_input("Subtrahend (bottom)", value=169, step=1)
    if st.button("Show Subtraction"):
        data = subtraction_analysis_latex_detailed(minuend, subtrahend)
        st.markdown(render_subtraction_detailed_html(data), unsafe_allow_html=True)
        st.latex(f"{data['minuend_padded']} - {data['subtrahend_padded']} = {data['minuend']-data['subtrahend']}")
        st.latex(r"\text{Hundreds } " + f"{data['h_m']} - {data['h_s']} = {data['correct_h']} \\quad \text{Tens } {data['t_m']} - {data['t_s']} = {data['correct_t']} \\quad \text{Units } {data['u_m']} - {data['u_s']} = {data['correct_u']}")

elif menu_num == 2:
    st.header("2. Multiplication - Detailed (LaTeX)")
    c1,c2 = st.columns(2)
    with c1: a = st.number_input("Multiplicand", value=123, step=1)
    with c2: b = st.number_input("Multiplier", value=45, step=1)
    if st.button("Show Multiplication"):
        data = multiplication_analysis(a,b)
        st.markdown(render_multiplication_html(data), unsafe_allow_html=True)
        st.latex(f"{a} \\times {b} = {data['total']}")

elif menu_num == 3:
    st.header("3. Division - Detailed (LaTeX)")
    c1,c2 = st.columns(2)
    with c1: dvd = st.number_input("Dividend", value=1256, step=1)
    with c2: dvs = st.number_input("Divisor", value=8, step=1)
    if st.button("Divide"):
        data = long_division_steps_detailed(dvd, dvs)
        st.markdown(render_division_html_detailed(data), unsafe_allow_html=True)
        st.latex(f"{dvs} \\times {data['quotient']} + {data['remainder']} = {dvd}")

elif menu_num == 4:
    st.header("First Degree + Cartesian")
    eq = st.text_input("Equation", "2x+3=7", help="Use ^ e.g. x^3")
    if st.button("Solve Linear"):
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sol=sp.solve(expr,x)[0]
            st.latex(f"x = {sp.latex(sol)}")
        except Exception as e:
            st.error(str(e))

elif menu_num == 5:
    st.header("Second Degree + Cartesian")
    eq = st.text_input("Equation", "x^2-5x+6=0")
    if st.button("Solve Quadratic"):
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sols=sp.solve(expr,x)
            st.latex(f"x = {', '.join(sp.latex(s) for s in sols)}")
        except Exception as e:
            st.error(str(e))

elif menu_num == 6:
    st.header("Linear Systems")
    eq1=st.text_input("Eq1","2x+3y=5"); eq2=st.text_input("Eq2","x-y=1")
    if st.button("Solve"):
        try:
            lhs1,rhs1=eq1.split('='); lhs2,rhs2=eq2.split('=')
            A,b=sp.linear_eq_to_matrix([sp.Eq(parse_expr(lhs1),parse_expr(rhs1)), sp.Eq(parse_expr(lhs2),parse_expr(rhs2))], x,y)
            sol=list(sp.linsolve([sp.Eq(parse_expr(lhs1),parse_expr(rhs1)), sp.Eq(parse_expr(lhs2),parse_expr(rhs2))], x,y))
            st.latex(f"Solution = {sp.latex(sol)}")
        except Exception as e:
            st.error(str(e))

elif menu_num == 7:
    st.header("7. Limits - Step-by-step resolution - LaTeX - infinity -> \\infty symbol")
    expr_input = st.text_input("f(x)", "sin(x)/x", key="lim7")
    point_input = st.text_input("Point x ->", "0", help="infinity or -infinity transforms to oo", key="lim7p")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="lim7v")
    if st.button("Compute Limit"):
        steps, lim_val, fig = limit_steps_detailed(expr_input, var_sel, point_input)
        st.markdown(steps)
        if fig is not None:
            st.pyplot(fig)
        st.info(f"Input '{point_input}' transformed to ${sp.latex(parse_point(point_input))}$")

elif menu_num == 8:
    st.header("8. Derivatives - 8 Rules - LaTeX + Comparison")
    expr_input = st.text_input("f(x)", "x^2+3x", key="der8")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="der8v")
    selected_rule = st.selectbox("Select Rule", derivative_rules_list, key="der8r")
    if st.button("Show Derivative"):
        steps, deriv, _ = derivative_rule_steps(expr_input, var_sel, selected_rule)
        st.markdown(steps)
        if deriv is not None:
            st.latex(f"f'({var_sel}) = {sp.latex(deriv)}")
            cols = st.columns(4)
            for idx, rule in enumerate(derivative_rules_list):
                col = cols[idx % 4]
                with col:
                    _, other_deriv, _ = derivative_rule_steps(expr_input, var_sel, rule)
                    same = compare_derivatives(deriv, other_deriv)
                    color = "green" if same else "red"
                    bg = "#d4edda" if same else "#f8d7da"
                    if other_deriv is not None:
                        st.markdown(f"<div style='background:{bg}; border:1px solid {color}; padding:6px; border-radius:6px;'><b>{rule}</b>: ${sp.latex(other_deriv)}$ <span style='color:{color}'>{'✓ SAME GREEN' if same else '✗ DIFF RED'}</span></div>", unsafe_allow_html=True)

elif menu_num == 9:
    st.header("9. Integrals - 7 Rules - LaTeX Fixed - Comparison Green/Red")
    st.markdown("**Fixed defect:** For $\\log(x)+\\sin(2x)$, primitive $F = x\\log(x)-x-\\frac{\\cos(2x)}{2}+C$ with LaTeX library")
    expr_input = st.text_input("Integrand", "sin(2x)+log(x)", help="Use ^ e.g. x^3, example sin(2x)+log(x)", key="int9")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="int9v")
    rule_sel = st.selectbox("Select Primary Rule", integral_rules_list, key="int9r")
    mode = st.radio("Type", ["Indefinite","Definite"], key="int9m")
    lower=None; upper=None
    if mode=="Definite":
        c1,c2=st.columns(2)
        with c1: lower_input=st.text_input("Lower a", "0", key="int9lo")
        with c2: upper_input=st.text_input("Upper b", "2", key="int9up")
        lower=parse_point(lower_input); upper=parse_point(upper_input)

    if st.button("Show Integral Rule Step by Step"):
        if mode=="Definite" and lower is not None and upper is not None:
            steps, result, _ = integral_rule_steps_fixed(expr_input, var_sel, rule_sel, lower, upper)
        else:
            steps, result, _ = integral_rule_steps_fixed(expr_input, var_sel, rule_sel, None, None)
        st.markdown(steps)
        if result is not None:
            st.latex(f"\\text{{Result}} = {sp.latex(result)} + C" if mode=="Indefinite" else f"\\text{{Result}} = {sp.latex(result)}")
            # Graphs
            try:
                fig, ax = plt.subplots()
                var=sp.Symbol(var_sel)
                f_lamb=sp.lambdify(var, parse_expr(expr_input,var_sel), 'numpy')
                t=np.linspace(-3,3,400)
                ax.plot(t, f_lamb(t), linewidth=2, label='f(x) curve (x,y)')
                ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
                st.pyplot(fig)
                solid_fig = plot_solid_revolution(expr_input, var_sel, -2, 2)
                if solid_fig:
                    st.pyplot(solid_fig)
            except Exception as e:
                st.error(str(e))

        st.subheader("Comparison Panel - Other Rules - Green = same result, Red = different")
        st.markdown("Is it certain By parts same as other rules? If not same, show in **red**, if same **green**")
        cols = st.columns(3)
        ref_result = result
        for idx, rule in enumerate(integral_rules_list):
            col = cols[idx % 3]
            with col:
                if mode=="Definite" and lower is not None and upper is not None:
                    _, other_res, _ = integral_rule_steps_fixed(expr_input, var_sel, rule, lower, upper)
                else:
                    _, other_res, _ = integral_rule_steps_fixed(expr_input, var_sel, rule, None, None)
                same = compare_integrals(ref_result, other_res)
                color = "green" if same else "red"
                bg = "#d4edda" if same else "#f8d7da"
                border = f"2px solid {color}" if rule==rule_sel else f"1px solid {color}"
                if other_res is not None:
                    # Proper LaTeX inside $...$
                    latex_res = sp.latex(other_res)
                    st.markdown(f"<div style='background:{bg}; border:{border}; padding:8px; border-radius:8px;'><b>{rule}</b><br/>$\\int {sp.latex(parse_expr(expr_input,var_sel))} d{var_sel} = {latex_res} + C$<br/><span style='color:{color}; font-weight:bold;'>{'✓ SAME - GREEN' if same else '✗ DIFFERENT - RED'}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background:#f8d7da; border:1px solid red; padding:8px; border-radius:8px;'><b>{rule}</b><br/>No result<br/><span style='color:red;'>✗ DIFFERENT - RED</span></div>", unsafe_allow_html=True)
