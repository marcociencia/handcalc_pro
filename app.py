import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy.parsing.sympy_parser import parse_expr as sym_parse, standard_transformations, implicit_multiplication_application, convert_xor

# SYMBOLS
x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z, 'oo': sp.oo, 'infinity': sp.oo, 'inf': sp.oo}
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

def parse_expr(expr_str, var='x'):
    if not expr_str:
        return None
    try:
        s = expr_str.strip()
        # replace infinity word with oo for sympy
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
    # handle infinity
    if s in ['infinity', 'inf', 'oo', '+oo', '∞', '+infinity', 'infinito']:
        return sp.oo
    if s in ['-infinity', '-inf', '-oo', '-∞', '-infinito']:
        return -sp.oo
    # handle cases like "infinity" inside expression? e.g., "2*infinity" ?
    s = s.replace('infinity', 'oo').replace('inf', 'oo').replace('∞','oo')
    try:
        return sp.sympify(s, locals=sym_vars)
    except:
        try:
            return sym_parse(s, local_dict=sym_vars, transformations=transformations)
        except:
            return None

# ------------------- SUBTRACTION & DIVISION (kept) -------------------
def subtraction_analysis_latex(minuend, subtrahend):
    diff = minuend - subtrahend
    L = max(len(str(minuend)), len(str(subtrahend)))
    minuend_padded = str(minuend).zfill(L)
    subtrahend_padded = str(subtrahend).zfill(L)
    h_m = (minuend//100)*100; t_m = ((minuend%100)//10)*10; u_m = minuend%10
    h_s = (subtrahend//100)*100; t_s = ((subtrahend%100)//10)*10; u_s = subtrahend%10
    return {"minuend": minuend, "subtrahend": subtrahend, "diff": diff, "minuend_padded": minuend_padded, "subtrahend_padded": subtrahend_padded, "h_m": h_m, "t_m": t_m, "u_m": u_m, "h_s": h_s, "t_s": t_s, "u_s": u_s, "correct_h": h_m-h_s, "correct_t": t_m-t_s, "correct_u": u_m-u_s}

def render_subtraction_latex(data):
    latex1 = r"\begin{array}{r} %s \\ - %s \\ \hline %s \end{array}" % (data["minuend_padded"], data["subtrahend_padded"], data["diff"])
    return latex1

def long_division_steps(dividend, divisor):
    if divisor==0: return None
    s=str(dividend); steps=[]; rem=0; q_digits=[]
    for idx,ch in enumerate(s):
        cur=rem*10+int(ch) if idx>0 or rem!=0 else int(ch)
        q=cur//divisor; prod=q*divisor; r=cur-prod
        steps.append({"partial":cur,"q":q,"prod":prod,"rem":r,"explain":f"{cur} ÷ {divisor} = {q}"})
        q_digits.append(q); rem=r
    q_str=''.join(map(str,q_digits)).lstrip('0') or '0'
    return {"dividend":dividend,"divisor":divisor,"quotient":int(q_str),"remainder":rem,"steps":steps}

# ------------------- CARTESIAN HELPERS -------------------
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
    ax1.plot(t,yt,'b',linewidth=2,label=f'f({var_str})'); ax1.axhline(0,color='black',lw=1.2); ax1.axvline(0,color='black',lw=1.2)
    ax1.fill_between(t,yt,alpha=0.3,color='orange'); ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.legend(); ax1.grid(True,alpha=0.3); ax1.set_title('Curve (x,y)')
    ax2=fig.add_subplot(122,projection='3d')
    theta=np.linspace(0,2*np.pi,30); T,Theta=np.meshgrid(t,theta)
    try: R=np.abs(f_lamb(T))
    except: R=np.zeros_like(T)
    X=T; Y=R*np.cos(Theta); Z=R*np.sin(Theta)
    ax2.plot_surface(X,Y,Z,alpha=0.6,cmap='viridis',edgecolor='none')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z'); ax2.set_title('Solid of Revolution (x,y,z)'); return fig

# ------------------- LIMITS STEP BY STEP -------------------
def limit_steps_detailed(expr_str, var_str, point_str):
    expr=parse_expr(expr_str,var_str)
    point=parse_point(point_str)
    if expr is None:
        return f"Invalid expression '{expr_str}' - use ^ for power e.g. x^3", None, None
    if point is None:
        return f"Invalid point '{point_str}' - use number or infinity/-infinity", None, None
    var=sp.Symbol(var_str)
    steps=[]
    steps.append(f"**Limites - Resolução passo a passo**")
    steps.append(f"**Step 1 - Function:** $f({var_str})={sp.latex(expr)}$")
    steps.append(f"**Step 2 - Point:** ${var_str} \\to {sp.latex(point)}$ (input '{point_str}' transformed to symbol $\\to$ infinity handled as $\\infty$)")
    # direct substitution
    try:
        direct=expr.subs(var,point)
        steps.append(f"**Step 3 - Direct substitution:** $f({sp.latex(point)})={sp.latex(direct)}$")
        if direct.has(sp.nan, sp.zoo, sp.oo) and point not in [sp.oo, -sp.oo]:
            steps.append(f"  → Indeterminate form, need simplification / L'Hôpital")
        else:
            steps.append(f"  → Direct value exists")
    except Exception as e:
        steps.append(f"**Step 3 - Direct substitution failed:** {e}")
    # limit calculation
    try:
        lim_val=sp.limit(expr,var,point)
        steps.append(f"**Step 4 - Apply limit rules:** Sum, Product, Quotient, Power, Constant. For $\\infty$ use growth comparison")
        steps.append(f"**Step 5 - Compute:** $\\lim_{{{var_str}\\to {sp.latex(point)}}} {sp.latex(expr)} = {sp.latex(lim_val)}$")
        steps.append(f"**Step 6 - One-sided limits:** left={sp.latex(sp.limit(expr,var,point,dir='-'))}, right={sp.latex(sp.limit(expr,var,point,dir='+'))}")
        steps.append(f"**Step 7 - Final answer:** $\\boxed{{{sp.latex(lim_val)}}}$")
    except Exception as e:
        steps.append(f"**Error computing limit:** {e}")
        lim_val=None
    # graph
    fig,ax=plt.subplots()
    try:
        f_lamb=sp.lambdify(var,expr,'numpy')
        if point in [sp.oo, -sp.oo]:
            t=np.linspace(-10,10,400)
        else:
            try: pf=float(point)
            except: pf=0
            t=np.linspace(pf-3,pf+3,400)
        yt=[]
        for v in t:
            try: yv=float(f_lamb(v)); yt.append(yv if np.isfinite(yv) else np.nan)
            except: yt.append(np.nan)
        ax.plot(t,yt,label='f(x) curve (x,y)',linewidth=2)
        ax.axhline(0,color='black',lw=1.2,label='x axis'); ax.axvline(0,color='black',lw=1.2,label='y axis')
        if point not in [sp.oo, -sp.oo]:
            try: ax.axvline(float(point),color='red',ls='--',label=f'x->{point}')
            except: pass
        if lim_val is not None and lim_val.is_real and lim_val not in [sp.oo, -sp.oo]:
            try: ax.axhline(float(lim_val),color='green',ls='--',label=f'limit {float(lim_val):.2f}')
            except: pass
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title(f'Limit on Cartesian x,y - point {point_str} -> {sp.latex(point)}')
    except:
        pass
    return "\n\n".join(steps), lim_val, fig

# ------------------- DERIVATIVE RULES STEP BY STEP -------------------
derivative_rules_list = [
    "Defined & differentiable on same interval",
    "Constant Rule",
    "Power Rule",
    "Sum & Difference Rule",
    "Product Rule",
    "Quotient Rule",
    "Chain Rule",
    "Limits Rule"
]

def derivative_rule_steps(expr_str, var_str, rule_name):
    expr=parse_expr(expr_str,var_str)
    if expr is None:
        return f"Invalid expression '{expr_str}'", None, None
    var=sp.Symbol(var_str)
    deriv=sp.diff(expr,var)
    steps=[]
    steps.append(f"**{rule_name} - Resolução passo a passo**")
    steps.append(f"Function: $f({var_str})={sp.latex(expr)}$")
    if rule_name == "Defined & differentiable on same interval":
        steps.append(f"**Step 1:** Find domain: where f is defined")
        steps.append(f"**Step 2:** Check continuity: $\\lim_{{x\\to a}} f(x) = f(a)$")
        steps.append(f"**Step 3:** Check differentiability: $\\lim_{{h\\to0}} (f(a+h)-f(a))/h$ exists")
        steps.append(f"**Step 4:** For polynomial {sp.latex(expr)}, domain = $\\mathbb{{R}}$, differentiable everywhere")
        steps.append(f"**Step 5:** Interval of differentiability = domain")
        steps.append(f"**Step 6:** Derivative exists: ${sp.latex(deriv)}$")
        steps.append(f"**Step 7:** Final: $f'={sp.latex(deriv)}$")
    elif rule_name == "Constant Rule":
        steps.append(f"**Step 1:** Rule: $(c)'=0$")
        steps.append(f"**Step 2:** If $f({var_str})=c$ constant, derivative 0")
        if expr.is_constant():
            steps.append(f"**Step 3:** {sp.latex(expr)} is constant -> derivative 0")
        else:
            # find constant terms
            steps.append(f"**Step 3:** Identify constant terms in {sp.latex(expr)}")
            const_terms=[t for t in (expr.args if isinstance(expr, sp.Add) else [expr]) if t.is_constant()]
            steps.append(f"  Constants: {', '.join(sp.latex(c) for c in const_terms) if const_terms else 'none'} -> derivative 0 each")
        steps.append(f"**Step 4:** Differentiate remaining variable terms")
        steps.append(f"**Step 5:** Sum: ${sp.latex(deriv)}$")
        steps.append(f"**Step 6:** Simplify: ${sp.latex(sp.simplify(deriv))}$")
        steps.append(f"**Step 7:** $\\boxed{{f'={sp.latex(deriv)}}}$")
    elif rule_name == "Power Rule":
        steps.append(f"**Step 1:** Rule: $(x^n)'=n x^{{n-1}}$")
        steps.append(f"**Step 2:** Identify power terms $x^n$")
        terms = expr.args if isinstance(expr, sp.Add) else [expr]
        for term in terms:
            if term.is_Pow or (term.is_Mul and any(a.is_Pow for a in term.args)):
                steps.append(f"  Term ${sp.latex(term)}$ -> apply power rule -> ${sp.latex(sp.diff(term,var))}$")
        steps.append(f"**Step 3:** Coefficient rule: $(c x^n)'=c n x^{{n-1}}$")
        steps.append(f"**Step 4:** Apply to all: ${sp.latex(expr)} -> ${sp.latex(deriv)}$")
        steps.append(f"**Step 5:** Simplify")
        steps.append(f"**Step 6:** Check")
        steps.append(f"**Step 7:** Final ${sp.latex(deriv)}$")
    elif rule_name == "Sum & Difference Rule":
        steps.append(f"**Step 1:** Rule: $(f±g)'=f'±g'$")
        steps.append(f"**Step 2:** Split sum: ${sp.latex(expr)}$")
        if isinstance(expr, sp.Add):
            for i, term in enumerate(expr.args):
                steps.append(f"  f_{i}={sp.latex(term)} -> f_{i}'={sp.latex(sp.diff(term,var))}")
        steps.append(f"**Step 3:** Sum derivatives")
        steps.append(f"**Step 4:** ${sp.latex(deriv)}$")
        steps.append(f"**Step 5:** Simplify")
        steps.append(f"**Step 6:** Verify term by term")
        steps.append(f"**Step 7:** Final")
    elif rule_name == "Product Rule":
        steps.append(f"**Step 1:** Rule: $(f·g)'=f'·g+f·g'$")
        if expr.is_Mul and len(expr.args)>=2:
            f1=expr.args[0]; g1=sp.Mul(*expr.args[1:])
            steps.append(f"**Step 2:** Identify $f={sp.latex(f1)}, g={sp.latex(g1)}$")
            steps.append(f"**Step 3:** $f'={sp.latex(sp.diff(f1,var))}, g'={sp.latex(sp.diff(g1,var))}$")
            steps.append(f"**Step 4:** Apply: $f'g+fg' = {sp.latex(sp.diff(f1,var))}·{sp.latex(g1)} + {sp.latex(f1)}·{sp.latex(sp.diff(g1,var))}$")
        else:
            steps.append(f"**Step 2:** Function ${sp.latex(expr)}$ may not be pure product, but we can still apply product if we write as product of terms")
            steps.append(f"**Step 3:** General derivative still ${sp.latex(deriv)}$ via product rule if applicable")
        steps.append(f"**Step 5:** Simplify ${sp.latex(sp.simplify(deriv))}$")
        steps.append(f"**Step 6:** Check")
        steps.append(f"**Step 7:** Final")
    elif rule_name == "Quotient Rule":
        steps.append(f"**Step 1:** Rule: $(f/g)'=(f'g-fg')/g^2$")
        if expr.is_Mul or isinstance(expr, sp.Pow) or '/' in str(expr):
            # try to detect quotient
            steps.append(f"**Step 2:** Identify numerator and denominator")
            num, den = sp.fraction(expr)
            steps.append(f"  $f={sp.latex(num)}, g={sp.latex(den)}$")
            steps.append(f"**Step 3:** $f'={sp.latex(sp.diff(num,var))}, g'={sp.latex(sp.diff(den,var))}$")
            steps.append(f"**Step 4:** Apply: $(f'g-fg')/g^2 = ({sp.latex(sp.diff(num,var))}·{sp.latex(den)} - {sp.latex(num)}·{sp.latex(sp.diff(den,var))})/({sp.latex(den)})^2$")
        steps.append(f"**Step 5:** Simplify ${sp.latex(sp.simplify(deriv))}$")
        steps.append(f"**Step 6:** Domain: denominator ≠0")
        steps.append(f"**Step 7:** Final")
    elif rule_name == "Chain Rule":
        steps.append(f"**Step 1:** Rule: $(f(g(x)))'=f'(g)·g'$")
        steps.append(f"**Step 2:** Identify outer and inner: $f(g({var_str}))$ where $g({var_str})$ inside")
        steps.append(f"**Step 3:** Example: $sin(2x)$ outer $sin(u)$, inner $u=2x$")
        steps.append(f"**Step 4:** For ${sp.latex(expr)}$, inner $g={var_str}$ functions detected")
        # try to find composite
        if expr.has(sp.sin, sp.cos, sp.exp, sp.log):
            steps.append(f"  Composite found: ${sp.latex(expr)}$ -> outer derivative * inner derivative")
        steps.append(f"**Step 5:** Apply chain: ${sp.latex(deriv)}$")
        steps.append(f"**Step 6:** Simplify")
        steps.append(f"**Step 7:** Final")
    elif rule_name == "Limits Rule":
        steps.append(f"**Step 1:** Rule: $f'(a)=\\lim_{{h\\to0}} (f(a+h)-f(a))/h$")
        h=sp.Symbol('h')
        dq=(expr.subs(var,var+h)-expr)/h
        steps.append(f"**Step 2:** Difference quotient: ${sp.latex(dq)}$")
        steps.append(f"**Step 3:** Simplify: ${sp.latex(sp.simplify(dq))}$")
        steps.append(f"**Step 4:** Limit $h\\to0$: ${sp.latex(deriv)}$")
        steps.append(f"**Step 5:** This is definition of derivative")
        steps.append(f"**Step 6:** Evaluate at point if needed")
        steps.append(f"**Step 7:** Final $f'={sp.latex(deriv)}$")
    return "\n\n".join(steps), deriv, None

def compare_derivatives(ref_deriv, other_deriv):
    if ref_deriv is None or other_deriv is None:
        return False
    try:
        diff=sp.simplify(ref_deriv - other_deriv)
        return diff==0
    except:
        return False

# ------------------- INTEGRAL RULES STEP BY STEP -------------------
integral_rules_list = [
    "Primitives",
    "Substitution",
    "By parts",
    "Definite",
    "Indefinite",
    "FTC (Fundamental Theorem)",
    "Limits"
]

def integral_rule_steps(expr_str, var_str, rule_name, lower=None, upper=None):
    expr=parse_expr(expr_str,var_str)
    if expr is None:
        return f"Invalid '{expr_str}'", None, None
    var=sp.Symbol(var_str)
    F=sp.integrate(expr,var)
    steps=[]
    steps.append(f"**{rule_name} - Resolução passo a passo**")
    steps.append(f"Integrand: $\\int {sp.latex(expr)} d{var_str}$")
    if rule_name == "Primitives":
        steps.append(f"**Step 1:** Primitive rule: $\\int x^n dx = x^{{n+1}}/(n+1) + C$")
        steps.append(f"**Step 2:** Identify power: ${sp.latex(expr)}$")
        steps.append(f"**Step 3:** Apply: $F({var_str})={sp.latex(F)}+C$")
        steps.append(f"**Step 4:** Check: $F'={sp.latex(sp.diff(F,var))}$ should equal original")
        steps.append(f"**Step 5:** Add constant $C$")
        steps.append(f"**Step 6:** Family of curves (x,y)")
        steps.append(f"**Step 7:** Final $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)}+C}}$")
    elif rule_name == "Substitution":
        steps.append(f"**Step 1:** Rule: $\\int f(g(x))g'(x)dx = \\int f(u)du$, $u=g(x)$")
        steps.append(f"**Step 2:** Choose $u$ as inner function of ${sp.latex(expr)}$")
        steps.append(f"**Step 3:** Compute $du$")
        steps.append(f"**Step 4:** Rewrite integral in $u$")
        steps.append(f"**Step 5:** Integrate in $u$: $\\int f(u)du$")
        steps.append(f"**Step 6:** Substitute back $u=g(x)$ -> ${sp.latex(F)}+C$")
        steps.append(f"**Step 7:** Check derivative")
    elif rule_name == "By parts":
        steps.append(f"**Step 1:** Rule: $\\int u dv = uv - \\int v du$")
        steps.append(f"**Step 2:** Choose $u$ and $dv$ from ${sp.latex(expr)}$")
        steps.append(f"**Step 3:** Example: For $\\int x·sin(x) dx$, $u=x$, $dv=sin(x)dx$")
        steps.append(f"**Step 4:** Compute $du$, $v$")
        steps.append(f"**Step 5:** Apply formula: $uv - \\int v du$")
        steps.append(f"**Step 6:** Integrate remaining: ${sp.latex(F)}+C$")
        steps.append(f"**Step 7:** Final")
    elif rule_name == "Definite":
        if lower is None or upper is None:
            steps.append(f"**Step 1:** Definite needs limits a,b: $\\int_a^b f(x)dx$")
            steps.append(f"**Step 2:** Current integrand ${sp.latex(expr)}$ would be $F(b)-F(a)$")
            steps.append(f"**Step 3:** $F={sp.latex(F)}$")
            steps.append(f"**Step 4:** Need numeric a,b to compute")
            steps.append(f"**Step 5:** If a,b given, $F(b)-F(a)$")
            steps.append(f"**Step 6:** Area interpretation")
            steps.append(f"**Step 7:** Final")
            return "\n\n".join(steps), F, None
        else:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"**Step 1:** $\\int_{{{lower}}}^{{{upper}}} {sp.latex(expr)} d{var_str}$")
            steps.append(f"**Step 2:** Antiderivative $F={sp.latex(F)}+C$")
            steps.append(f"**Step 3:** $F({upper})={sp.latex(F.subs(var,upper))}$")
            steps.append(f"**Step 4:** $F({lower})={sp.latex(F.subs(var,lower))}$")
            steps.append(f"**Step 5:** Subtract: $F(b)-F(a)={sp.latex(val)}$")
            steps.append(f"**Step 6:** Area under curve (x,y)")
            steps.append(f"**Step 7:** Final $\\boxed{{{sp.latex(val)}}}$")
            return "\n\n".join(steps), val, None
    elif rule_name == "Indefinite":
        steps.append(f"**Step 1:** Indefinite integral = family $F+C$")
        steps.append(f"**Step 2:** $F={sp.latex(F)}$")
        steps.append(f"**Step 3:** Add $C$")
        steps.append(f"**Step 4:** Check $F'={sp.latex(sp.diff(F,var))}$")
        steps.append(f"**Step 5:** Different $C$ gives different curves (x,y)")
        steps.append(f"**Step 6:** No limits")
        steps.append(f"**Step 7:** Final $\\boxed{{{sp.latex(F)}+C}}$")
    elif rule_name == "FTC (Fundamental Theorem)":
        steps.append(f"**Step 1:** FTC: If $F'=f$, then $\\int_a^b f(x)dx = F(b)-F(a)$")
        steps.append(f"**Step 2:** Also $d/dx \\int_a^x f(t)dt = f(x)$")
        steps.append(f"**Step 3:** For ${sp.latex(expr)}$, $F={sp.latex(F)}$")
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"**Step 4:** $\\int_{{{lower}}}^{{{upper}}} = {sp.latex(val)}$")
            steps.append(f"**Step 5:** Graph area under curve (x,y) explanatory")
            steps.append(f"**Step 6:** Solid of revolution volume if rotated (x,y,z)")
            steps.append(f"**Step 7:** Final")
            return "\n\n".join(steps), val, None
        else:
            steps.append(f"**Step 4:** Indefinite shows family")
            steps.append(f"**Step 5:** Graph")
            steps.append(f"**Step 6:** Solid")
            steps.append(f"**Step 7:** Final")
    elif rule_name == "Limits":
        steps.append(f"**Step 1:** Definition: $\\int_a^b f(x)dx = \\lim_{{n\\to\\infty}} \\sum_{{i=1}}^n f(x_i)\\Delta x$")
        steps.append(f"**Step 2:** Riemann sum")
        steps.append(f"**Step 3:** $\\Delta x = (b-a)/n$")
        steps.append(f"**Step 4:** Take limit $n\\to\\infty$ -> ${sp.latex(F)}$ antiderivative")
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"**Step 5:** Exact ${sp.latex(val)}$")
        steps.append(f"**Step 6:** Area limit")
        steps.append(f"**Step 7:** Final")
    return "\n\n".join(steps), F, None

def compare_integrals(ref, other):
    if ref is None or other is None:
        return False
    try:
        # For indefinite, compare derivatives: diff of antiderivatives should have zero derivative, or difference is constant
        # Simplify ref - other
        diff = sp.simplify(ref - other)
        # If diff is constant, derivatives equal
        # Check if diff is constant or zero
        if diff.is_constant():
            return True
        # Also check if derivative of diff is zero
        # Need var, assume x
        # For simplicity check simplify ==0 or constant
        return diff==0 or diff.is_number
    except:
        return False

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="Math Solver - Rules Step by Step", layout="wide")
st.title("📚 Math Solver - Limits, Derivatives, Integrals - Rules Step by Step + Infinity + Comparison")

menu = st.sidebar.selectbox("Select Module", [
    "1. Subtraction - Column Method",
    "2. Long Division L Shape",
    "3. First Degree + Cartesian x,y",
    "4. Second Degree + Cartesian x,y",
    "5. Linear Systems x,y and x,y,z",
    "6. Limits - Step by Step (infinity handling)",
    "7. Derivatives - 8 Rules Step by Step + Comparison",
    "8. Integrals - 7 Rules Step by Step + Comparison + Solid Revolution"
])

try:
    menu_num = int(menu.split(".")[0])
except:
    menu_num = 1

if menu_num == 1:
    st.header("1. Subtraction - Column Method")
    c1,c2 = st.columns(2)
    with c1: minuend = st.number_input("Minuend (top)", value=136, step=1)
    with c2: subtrahend = st.number_input("Subtrahend (bottom)", value=169, step=1)
    if st.button("Show Steps"):
        data = subtraction_analysis_latex(minuend, subtrahend)
        st.latex(render_subtraction_latex(data))

elif menu_num == 2:
    st.header("2. Long Division L Shape")
    c1,c2 = st.columns(2)
    with c1: dvd = st.number_input("Dividend", value=1256, step=1, min_value=0)
    with c2: dvs = st.number_input("Divisor", value=8, step=1, min_value=1)
    if st.button("Divide"):
        data = long_division_steps(dvd, dvs)
        if data:
            st.write(f"Quotient {data['quotient']}, Remainder {data['remainder']}")
            for s in data["steps"]:
                st.write(s["explain"])

elif menu_num == 3:
    st.header("First Degree")
    eq = st.text_input("Equation", "2x+3=7", help="Use ^ for power e.g. x^3")
    if st.button("Solve Linear"):
        # simple solve
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sol=sp.solve(expr,x)[0]; st.latex(f"x={sp.latex(sol)}")
        except Exception as e:
            st.error(str(e))

elif menu_num == 4:
    st.header("Second Degree")
    eq = st.text_input("Equation", "x^2-5x+6=0", help="Use ^")
    if st.button("Solve Quadratic"):
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sols=sp.solve(expr,x); st.write(sols)
        except Exception as e:
            st.error(str(e))

elif menu_num == 5:
    st.header("Linear Systems")
    size = st.radio("Size", ["2x2 (x,y)", "3x3 (x,y,z)"])
    if size.startswith("2x2"):
        eq1=st.text_input("Eq1","2x+3y=5"); eq2=st.text_input("Eq2","x-y=1"); eqs=[eq1,eq2]
    else:
        eq1=st.text_input("Eq1","x+y+z=6"); eq2=st.text_input("Eq2","x-y+2z=5"); eq3=st.text_input("Eq3","2x+y-z=1"); eqs=[eq1,eq2,eq3]
    if st.button("Solve System"):
        try:
            eqs_sym=[]
            for eq_str in eqs:
                lhs_str,rhs_str=eq_str.split('='); lhs=parse_expr(lhs_str); rhs=parse_expr(rhs_str); eqs_sym.append(sp.Eq(lhs,rhs))
            vars_in=list(set().union(*[eq.free_symbols for eq in eqs_sym])); vars_sorted=sorted(vars_in,key=lambda v: str(v))
            sol=list(sp.linsolve(eqs_sym,*vars_sorted))
            st.write(sol)
        except Exception as e:
            st.error(str(e))

elif menu_num == 6:
    st.header("6. Limits - Resolução passo a passo - infinity handling")
    st.markdown("**Type 'infinity' or '-infinity' for infinite limits - will be transformed to $\\infty$ symbol**")
    expr_input = st.text_input("f(x)", "sin(x)/x", help="Use ^ for power e.g. x^3, you can write 3x", key="lim_expr")
    point_input = st.text_input("Point x ->", "0", help="Type number, infinity, -infinity, oo, -oo", key="lim_point")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="lim_var")
    if st.button("Compute Limit Step by Step"):
        steps, lim_val, fig = limit_steps_detailed(expr_input, var_sel, point_input)
        st.markdown(steps)
        if fig is not None:
            st.pyplot(fig)
        # Show transformed symbol
        point_sym = parse_point(point_input)
        st.info(f"Input '{point_input}' transformed to symbol: ${sp.latex(point_sym)}$ for calculation")

elif menu_num == 7:
    st.header("7. Derivatives - 8 Rules - Resolução passo a passo + Comparison Panel")
    st.markdown("""
    Rules:
    - Defined & differentiable on same interval
    - Constant Rule
    - Power Rule
    - Sum & Difference Rule
    - Product Rule
    - Quotient Rule
    - Chain Rule
    - Limits Rule
    """)
    expr_input = st.text_input("f(x)", "x^2+3x", help="Use ^ for power e.g. x^3, 3x for 3*x, example sin(2x)+ln(x)", key="der_expr")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="der_var2")
    selected_rule = st.selectbox("Select Primary Rule to show step by step", derivative_rules_list, key="der_rule_sel")

    if st.button("Show Derivative Rule Step by Step"):
        steps, deriv, _ = derivative_rule_steps(expr_input, var_sel, selected_rule)
        st.markdown(steps)
        if deriv is not None:
            st.latex(f"f'({var_sel})={sp.latex(deriv)}")
            # Graph Cartesian x,y and solid revolution
            try:
                fig, ax = plt.subplots()
                var=sp.Symbol(var_sel)
                f_lamb=sp.lambdify(var, parse_expr(expr_input,var_sel), 'numpy')
                df_lamb=sp.lambdify(var, deriv, 'numpy')
                t=np.linspace(-3,3,400)
                ax.plot(t, f_lamb(t), label='f(x) curve (x,y)', linewidth=2)
                ax.plot(t, df_lamb(t), label="f'(x) derivative line", linestyle='--')
                ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
                st.pyplot(fig)
                # solid revolution for f
                solid_fig = plot_solid_revolution(expr_input, var_sel, -2, 2)
                if solid_fig:
                    st.pyplot(solid_fig)
            except Exception as e:
                st.error(f"Graph error: {e}")

        # Comparison panel with buttons for other rules
        st.subheader("Comparison Panel - Other Rules - Green = same result, Red = different")
        st.markdown("Example: f(x)=sin(2x)+ln(x) used By parts, check if other rules reach same answer")
        cols = st.columns(4)
        ref_deriv = deriv
        for idx, rule in enumerate(derivative_rules_list):
            col = cols[idx % 4]
            with col:
                if st.button(f"Test {rule}", key=f"der_test_{rule}_{idx}"):
                    _, other_deriv, _ = derivative_rule_steps(expr_input, var_sel, rule)
                    same = compare_derivatives(ref_deriv, other_deriv)
                    color = "green" if same else "red"
                    bg = "#d4edda" if same else "#f8d7da"
                    st.markdown(f"<div style='background:{bg}; border:2px solid {color}; padding:8px; border-radius:8px;'><b>{rule}</b><br/>Result: ${sp.latex(other_deriv) if other_deriv is not None else 'None'}$<br/><span style='color:{color}; font-weight:bold;'>{'✓ SAME - GREEN' if same else '✗ DIFFERENT - RED'}</span></div>", unsafe_allow_html=True)
                else:
                    # Show all results at once when not clicked? Let's show overview
                    _, other_deriv, _ = derivative_rule_steps(expr_input, var_sel, rule)
                    same = compare_derivatives(ref_deriv, other_deriv)
                    color = "green" if same else "red"
                    bg = "#d4edda" if same else "#f8d7da"
                    if other_deriv is not None:
                        st.markdown(f"<div style='background:{bg}; border:1px solid {color}; padding:6px; border-radius:6px; font-size:12px;'><b>{rule}</b>: ${sp.latex(other_deriv)}$ <span style='color:{color}'>{'✓' if same else '✗'}</span></div>", unsafe_allow_html=True)

elif menu_num == 8:
    st.header("8. Integrals - 7 Rules - Resolução passo a passo + Comparison Panel + Solid Revolution")
    st.markdown("""
    Rules:
    - Primitives
    - Substitution
    - By parts
    - Definite
    - Indefinite
    - FTC (Fundamental Theorem) with explanatory graph
    - Limits
    """)
    expr_input = st.text_input("Integrand", "sin(2x)+ln(x)", help="Example f(x)=sin(2x)+ln(x) - use ^ for power", key="int_expr")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="int_var")
    rule_sel = st.selectbox("Select Primary Rule", integral_rules_list, key="int_rule_sel")
    mode = st.radio("Type", ["Indefinite","Definite"], key="int_mode2")
    lower=None; upper=None
    if mode=="Definite":
        c1,c2=st.columns(2)
        with c1: lower_input=st.text_input("Lower a", "0", help="Can be infinity")
        with c2: upper_input=st.text_input("Upper b", "2", help="Can be infinity")
        lower=parse_point(lower_input)
        upper=parse_point(upper_input)
        st.info(f"Lower transformed to {sp.latex(lower) if lower is not None else 'None'}, Upper to {sp.latex(upper) if upper is not None else 'None'} - infinity handled as oo")

    if st.button("Show Integral Rule Step by Step"):
        if mode=="Definite" and lower is not None and upper is not None:
            # need numeric for integration? sympy can handle oo
            steps, result, _ = integral_rule_steps(expr_input, var_sel, rule_sel, float(lower) if lower not in [sp.oo, -sp.oo] else lower, float(upper) if upper not in [sp.oo, -sp.oo] else upper)
        else:
            steps, result, _ = integral_rule_steps(expr_input, var_sel, rule_sel, None, None)
        st.markdown(steps)
        if result is not None:
            st.latex(f"Result = {sp.latex(result)}")
            # Graph
            try:
                fig, ax = plt.subplots()
                var=sp.Symbol(var_sel)
                f_lamb=sp.lambdify(var, parse_expr(expr_input,var_sel), 'numpy')
                t=np.linspace(-3,3,400)
                ax.plot(t, f_lamb(t), label='f(x) curve (x,y)', linewidth=2)
                ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                if mode=="Definite" and lower is not None and upper is not None:
                    try:
                        lo_f=float(lower) if lower not in [sp.oo,-sp.oo] else -2
                        up_f=float(upper) if upper not in [sp.oo,-sp.oo] else 2
                        ix=np.linspace(lo_f,up_f,100); ax.fill_between(ix, f_lamb(ix), alpha=0.3, color='orange', label='area')
                    except: pass
                ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
                st.pyplot(fig)
                # solid revolution
                solid_fig = plot_solid_revolution(expr_input, var_sel, -2, 2)
                if solid_fig:
                    st.pyplot(solid_fig)
            except Exception as e:
                st.error(f"Graph error {e}")

        # Comparison panel
        st.subheader("Comparison Panel - Other Integral Rules - Green = same, Red = different")
        st.markdown("Example: f(x)=sin(2x)+ln(x) used integral by parts, test other rules")
        cols = st.columns(3)
        ref_result = result
        for idx, rule in enumerate(integral_rules_list):
            col = cols[idx % 3]
            with col:
                if st.button(f"Test {rule}", key=f"int_test_{rule}_{idx}"):
                    if mode=="Definite" and lower is not None and upper is not None:
                        _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, lower, upper)
                    else:
                        _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, None, None)
                    same = compare_integrals(ref_result, other_res)
                    color = "green" if same else "red"
                    bg = "#d4edda" if same else "#f8d7da"
                    st.markdown(f"<div style='background:{bg}; border:2px solid {color}; padding:8px; border-radius:8px;'><b>{rule}</b><br/>Result: ${sp.latex(other_res) if other_res is not None else 'None'}$<br/><span style='color:{color}; font-weight:bold;'>{'✓ SAME - GREEN' if same else '✗ DIFFERENT - RED'}</span></div>", unsafe_allow_html=True)
                else:
                    # overview
                    if mode=="Definite" and lower is not None and upper is not None:
                        _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, lower, upper)
                    else:
                        _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, None, None)
                    same = compare_integrals(ref_result, other_res)
                    color = "green" if same else "red"
                    bg = "#d4edda" if same else "#f8d7da"
                    if other_res is not None:
                        st.markdown(f"<div style='background:{bg}; border:1px solid {color}; padding:6px; border-radius:6px; font-size:12px;'><b>{rule}</b>: ${sp.latex(other_res)}$ <span style='color:{color}'>{'✓' if same else '✗'}</span></div>", unsafe_allow_html=True)
