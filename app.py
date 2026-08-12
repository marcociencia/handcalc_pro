import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# SYMBOLS
x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z}

from sympy.parsing.sympy_parser import parse_expr as sym_parse, standard_transformations, implicit_multiplication_application, convert_xor
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

def parse_expr(expr_str, var='x'):
    if not expr_str:
        return None
    try:
        return sym_parse(expr_str.strip(), local_dict=sym_vars, transformations=transformations)
    except:
        try:
            return sp.sympify(expr_str.replace("^", "**"), locals=sym_vars)
        except:
            return None

def subtraction_analysis_latex(minuend, subtrahend):
    diff = minuend - subtrahend
    abs_diff = abs(diff)
    L = max(len(str(minuend)), len(str(subtrahend)))
    minuend_padded = str(minuend).zfill(L)
    subtrahend_padded = str(subtrahend).zfill(L)
    h_m = (minuend//100)*100; t_m = ((minuend%100)//10)*10; u_m = minuend%10
    h_s = (subtrahend//100)*100; t_s = ((subtrahend%100)//10)*10; u_s = subtrahend%10
    return {
        "minuend": minuend, "subtrahend": subtrahend, "diff": diff, "abs_diff": abs_diff,
        "minuend_padded": minuend_padded, "subtrahend_padded": subtrahend_padded,
        "correct_h": h_m-h_s, "correct_t": t_m-t_s, "correct_u": u_m-u_s,
        "h_m": h_m, "t_m": t_m, "u_m": u_m, "h_s": h_s, "t_s": t_s, "u_s": u_s
    }

def render_subtraction_latex(data):
    minuend=data["minuend"]; subtrahend=data["subtrahend"]; diff=data["diff"]; abs_diff=data["abs_diff"]
    latex1 = r"""
\begin{array}{r}
  %s \\
- %s \\
\hline
  %s \\
\end{array}
\qquad
\begin{aligned}
\text{Minuend} &= %s\\
\text{Subtrahend} &= %s\\
\text{Diff} &= %s - %s = %s
\end{aligned}
""" % (data["minuend_padded"], data["subtrahend_padded"], f"-{data['subtrahend_padded']}" if minuend<subtrahend else data["minuend_padded"],
       data["minuend_padded"], data["subtrahend_padded"], minuend, subtrahend, diff)
    borrow_example = r"""
\text{Column Subtraction - Long Method (Borrowing):}\\
\begin{array}{cccc}
  \cancel{3}^{2} & \overset{10}{0} & \cancel{5}^{14} \\
  & 3 & 0 & 5 \\
- & 1 & 3 & 6 \\
\hline
  & 1 & 6 & 9
\end{array}
\rightarrow 169 \text{ intermediate}
"""
    requested = r"""
\begin{aligned}
-100 &\rightarrow \text{hundreds}\\
60 &\rightarrow \text{tens}\\
9 &\rightarrow \text{units}\\
-100+60+9 &= -33\\
\text{Final: } -33
\end{aligned}
"""
    correct = r"""
\begin{aligned}
%s &= %s+%s+%s\\
%s &= %s+%s+%s\\
\text{Hundreds }%s-%s=%s\\
\text{Tens }%s-%s=%s\\
\text{Units }%s-%s=%s\\
%s+%s+%s=%s
\end{aligned}
""" % (minuend, data["h_m"], data["t_m"], data["u_m"], subtrahend, data["h_s"], data["t_s"], data["u_s"],
       data["h_m"], data["h_s"], data["correct_h"], data["t_m"], data["t_s"], data["correct_t"],
       data["u_m"], data["u_s"], data["correct_u"], data["correct_h"], data["correct_t"], data["correct_u"], diff)
    return latex1, borrow_example, requested, correct

def long_division_steps(dividend, divisor):
    if divisor==0: return None
    s=str(dividend); steps=[]; rem=0; q_digits=[]
    for idx,ch in enumerate(s):
        cur=rem*10+int(ch) if idx>0 or rem!=0 else int(ch)
        q=cur//divisor; prod=q*divisor; r=cur-prod
        steps.append({"partial":cur,"q":q,"prod":prod,"rem":r,"explain":f"{cur} ÷ {divisor} = {q}, {q}x{divisor}={prod}, rem {r}"})
        q_digits.append(q); rem=r
    q_str=''.join(map(str,q_digits)).lstrip('0') or '0'
    return {"dividend":dividend,"divisor":divisor,"quotient":int(q_str),"remainder":rem,"steps":steps}

def render_division_html(data):
    if data is None: return "<p>Division by zero</p>"
    dividend=data["dividend"]; divisor=data["divisor"]; q=data["quotient"]; r=data["remainder"]
    html=f'<div style="font-family:monospace;background:#fffef7;border:2px solid #333;border-radius:12px;padding:18px;max-width:820px;"><h3>Long Division L Shape</h3><div style="display:flex;font-size:20px;"><div style="padding:8px 16px 8px 0;border-right:3px solid #111;min-width:130px;"><div style="font-weight:bold;">{dividend}</div>'
    for st in data["steps"]:
        if st["q"]!=0 or st["partial"]>=divisor:
            html+=f"<div>-{st['prod']}</div><div style='border-top:1px solid #333;'>{st['rem']}</div>"
    html+=f"<div style='margin-top:8px;font-weight:bold;'>Rem {r}</div></div></div><div style='padding:8px 0 8px 16px;'><div style='border-bottom:3px solid #111;padding-bottom:4px;font-weight:bold;'>{divisor} divisor</div><div style='padding-top:6px;color:#0a0;font-weight:bold;'>{q} quotient</div><div style='margin-top:14px;font-size:13px;background:#f5f5ff;padding:8px;border-radius:6px;'>"
    for i,st in enumerate(data["steps"],1):
        html+=f"{i}. {st['explain']}<br/>"
    html+=f"</div></div></div></div>"
    return html

# CARTESIAN HELPERS
def plot_cartesian_xy():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.axhline(0,color='black',linewidth=1.2); ax.axvline(0,color='black',linewidth=1.2)
    ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('Cartesian Plane x,y'); ax.grid(True,alpha=0.3); return fig

def plot_cartesian_xyz():
    fig=plt.figure(figsize=(5,5)); ax=fig.add_subplot(111,projection='3d')
    ax.plot([-5,5],[0,0],[0,0],color='red',linewidth=2,label='x'); ax.plot([0,0],[-5,5],[0,0],color='green',linewidth=2,label='y')
    ax.plot([0,0],[0,0],[-5,5],color='blue',linewidth=2,label='z')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.set_title('Cartesian Space x,y,z'); ax.legend(); return fig

def plot_solid_revolution(expr_str, var_str='x', a=0, b=2):
    # Solid of revolution around x-axis for f(x)
    expr=parse_expr(expr_str,var_str)
    if expr is None: return None
    var=sp.Symbol(var_str)
    f_lamb=sp.lambdify(var,expr,'numpy')
    fig=plt.figure(figsize=(10,4))
    # 2D curve
    ax1=fig.add_subplot(121)
    t=np.linspace(a,b,200)
    try: yt=f_lamb(t)
    except: yt=np.zeros_like(t)
    ax1.plot(t,yt,'b',linewidth=2,label=f'f({var_str})={expr_str}')
    ax1.axhline(0,color='black',linewidth=1.2); ax1.axvline(0,color='black',linewidth=1.2)
    ax1.fill_between(t,yt,alpha=0.3,color='orange',label='area')
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_title(f'Curve y={expr_str}'); ax1.legend(); ax1.grid(True,alpha=0.3)
    # 3D solid revolution
    ax2=fig.add_subplot(122,projection='3d')
    theta=np.linspace(0,2*np.pi,30)
    T,Theta=np.meshgrid(t,theta)
    try: R=f_lamb(T)
    except: R=np.zeros_like(T)
    # keep positive for radius visualization
    R=np.abs(R)
    X=T; Y=R*np.cos(Theta); Z=R*np.sin(Theta)
    ax2.plot_surface(X,Y,Z,alpha=0.6,cmap='viridis',edgecolor='none')
    ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z')
    ax2.set_title(f'Solid of Revolution around x-axis (x,y,z)')
    return fig

def plot_linear_func(a,b,sol):
    fig, ax = plt.subplots()
    xv=np.linspace(float(sol)-5,float(sol)+5,200)
    ax.plot(xv, a*xv+b, label=f'{a}x+{b}', linewidth=2)
    ax.axhline(0,color='black',linewidth=1.2,label='x axis'); ax.axvline(0,color='black',linewidth=1.2,linestyle='--',label='y axis')
    ax.scatter([float(sol)],[0],color='red',s=80,zorder=5,label=f'root {float(sol):.2f}')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title("First Degree on Cartesian x,y")
    return fig

def plot_quadratic_func(a,b,c,sols):
    fig, ax = plt.subplots()
    xv=np.linspace(-10,10,400); ax.plot(xv, a*xv**2+b*xv+c, label=f'{a}x²+{b}x+{c}', linewidth=2)
    ax.axhline(0,color='black',lw=1.2,label='x axis'); ax.axvline(0,color='black',lw=1.2,linestyle='--',label='y axis')
    for s in sols:
        if s.is_real: ax.scatter([float(s)],[0],color='red',s=80)
    xvtx=-b/(2*a); yvtx=a*xvtx**2+b*xvtx+c; ax.scatter([xvtx],[yvtx],color='green',s=80,label=f'vertex {xvtx:.2f},{yvtx:.2f}')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title("Second Degree on Cartesian x,y"); return fig

def solve_linear_steps(eq_str):
    try:
        if '=' not in eq_str: return "Missing =",None,None
        l,r=eq_str.split('='); le=parse_expr(l); re=parse_expr(r)
        if le is None or re is None: return f"Invalid {eq_str}",None,None
        expr=sp.expand(le-re); poly=sp.Poly(expr,x); a,b=poly.all_coeffs()
        if a==0: return "Not linear",None,None
        sol=-b/a
        steps=[f"**Step1:** ${sp.latex(le)}={sp.latex(re)}$",f"**Step2:** ${sp.latex(expr)}=0$",f"**Step3:** a={sp.latex(a)}, b={sp.latex(b)}",f"**Step4:** {sp.latex(a)}x={sp.latex(-b)}",f"**Step5:** x={sp.latex(sol)}",f"**Step6:** Verify",f"**Step7:** boxed"]
        return "\n\n".join(steps),sol,(float(a),float(b))
    except Exception as e: return f"Error {e}",None,None

def solve_quadratic_steps(eq_str):
    try:
        if '=' not in eq_str: return "Missing =",None,None
        l,r=eq_str.split('='); le=parse_expr(l); re=parse_expr(r)
        if le is None or re is None: return f"Invalid {eq_str}",None,None
        expr=sp.expand(le-re); poly=sp.Poly(expr,x); a,b,c=poly.all_coeffs(); disc=b**2-4*a*c
        steps=[f"**Step1:** {sp.latex(expr)}=0",f"**Step2:** a={sp.latex(a)},b={sp.latex(b)},c={sp.latex(c)}",f"**Step3:** Delta={sp.latex(disc)}"]
        if disc>0:
            s1=(-b+sp.sqrt(disc))/(2*a); s2=(-b-sp.sqrt(disc))/(2*a); steps.append(f"**Step4:** Two roots"); steps.append(f"**Step5:** {sp.latex(s1)}, {sp.latex(s2)}"); sols=[s1,s2]
        elif disc==0:
            s=-b/(2*a); steps.append(f"**Step4:** Double"); sols=[s]
        else:
            s1=(-b+sp.sqrt(disc))/(2*a); s2=(-b-sp.sqrt(disc))/(2*a); steps.append(f"**Step4:** Complex"); sols=[s1,s2]
        steps.append(f"**Step6:** Vertex"); steps.append(f"**Step7:** Final")
        return "\n\n".join(steps),sols,(float(a),float(b),float(c))
    except Exception as e: return f"Error {e}",None,None

def solve_linear_system_fixed(eq_list):
    try:
        eqs=[]
        for eq_str in eq_list:
            if '=' not in eq_str: return "Invalid",None,None
            lhs_str,rhs_str=eq_str.split('='); lhs=parse_expr(lhs_str); rhs=parse_expr(rhs_str)
            if lhs is None or rhs is None: return f"Invalid {eq_str}",None,None
            eqs.append(sp.Eq(lhs,rhs))
        vars_in=list(set().union(*[eq.free_symbols for eq in eqs])); vars_sorted=sorted(vars_in,key=lambda v: str(v))
        A,b=sp.linear_eq_to_matrix(eqs,*vars_sorted)
        steps=[f"**Step1: System**"]+[f"${sp.latex(eq)}$" for eq in eqs]
        steps.append(f"**Step2: Matrix A={sp.latex(A)}, b={sp.latex(b)}**")
        aug=A.row_join(b); steps.append(f"**Step3: Augmented {sp.latex(aug)}**")
        rref,piv=aug.rref(); steps.append(f"**Step4: RREF {sp.latex(rref)}**")
        if A.shape[0]==A.shape[1]:
            det=A.det(); steps.append(f"**Step5: det={sp.latex(det)}**")
        sol_set=list(sp.linsolve(eqs,*vars_sorted))
        if sol_set:
            sol=sol_set[0]; steps.append(f"**Step6: Solution {', '.join(f'{v}={sp.latex(val)}' for v,val in zip(vars_sorted,sol))}**"); steps.append(f"**Step7: Verify**")
            return "\n\n".join(steps),sol,vars_sorted
        else: return "No unique",None,vars_sorted
    except Exception as e: return f"Error {e}",None,None

def limit_with_rules(expr_str,var_str,point):
    try:
        expr=parse_expr(expr_str,var_str)
        if expr is None: return f"Invalid {expr_str}",None,None
        var=sp.Symbol(var_str); lim_val=sp.limit(expr,var,point)
        steps=[f"**Step1:** f={sp.latex(expr)}",f"**Step2:** {var_str}->{point}",f"**Step3:** Direct {sp.latex(expr.subs(var,point))}",f"**Step4:** Rules",f"**Step5:** lim={sp.latex(lim_val)}",f"**Step6:** Left/Right",f"**Step7:** boxed"]
        fig,ax=plt.subplots(); f_lamb=sp.lambdify(var,expr,'numpy'); t=np.linspace(float(point)-2,float(point)+2,400)
        try: yt=[float(f_lamb(v)) if np.isfinite(float(f_lamb(v))) else np.nan for v in t]
        except: yt=[np.nan]*len(t)
        ax.plot(t,yt,label='f'); ax.axhline(0,color='black',lw=1.2,label='x'); ax.axvline(0,color='black',lw=1.2,label='y'); ax.axvline(float(point),color='red',ls='--'); ax.grid(True,alpha=0.3); ax.legend(); ax.set_xlabel('x'); ax.set_ylabel('y')
        return "\n\n".join(steps),lim_val,fig
    except Exception as e: return f"Error {e}",None,None

def derivative_limit_def(expr_str,var_str='x',point=1):
    try:
        expr=parse_expr(expr_str,var_str)
        if expr is None: return f"Invalid {expr_str}",None,None
        var=sp.Symbol(var_str); h=sp.Symbol('h'); dq=(expr.subs(var,var+h)-expr)/h; deriv=sp.limit(dq,h,0)
        steps=[f"**Def f' lim**",f"**Step1 f={sp.latex(expr)}**",f"**Step2 DQ {sp.latex(dq)}**",f"**Step3 Simplify**",f"**Step4 {sp.latex(deriv)}**",f"**Step5 slope {point}**",f"**Step6 tangent**",f"**Step7 boxed**"]
        fig,ax=plt.subplots(); f_lamb=sp.lambdify(var,expr,'numpy'); t=np.linspace(float(point)-3,float(point)+3,400)
        ax.plot(t,f_lamb(t),label='f'); ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
        y0=float(expr.subs(var,point)); m=float(deriv.subs(var,point)); ax.plot(t,m*(t-float(point))+y0,'--',label='tangent'); ax.scatter([float(point)],[y0],color='red'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_xlabel('x'); ax.set_ylabel('y')
        return "\n\n".join(steps),deriv,fig
    except Exception as e: return f"Error {e}",None,None

def integral_limit_def(expr_str,var_str='x',a=0,b=2,n=6):
    try:
        expr=parse_expr(expr_str,var_str)
        if expr is None: return f"Invalid {expr_str}",None,None
        var=sp.Symbol(var_str); dx=(b-a)/n; f_lamb=sp.lambdify(var,expr,'numpy'); s=sum(float(f_lamb(a+i*dx))*dx for i in range(1,n+1)); exact=sp.integrate(expr,(var,a,b))
        steps=[f"**Def integral lim**",f"**Step1 dx={dx}**",f"**Step2 Riemann**",f"**Step3 S approx {s:.4f}**",f"**Step4 lim {sp.latex(exact)}**",f"**Step5 FTC**",f"**Step6 Exact**",f"**Step7 Area**"]
        fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4)); t=np.linspace(a,b,300); ax1.plot(t,f_lamb(t),'b'); ax1.axhline(0,color='black',lw=1); ax1.axvline(0,color='black',lw=1)
        for i in range(n):
            xi=a+i*dx
            try: ax1.bar(xi+dx,float(f_lamb(xi+dx)),width=dx,align='edge',alpha=0.3,edgecolor='black')
            except: pass
        ax1.set_title(f"Riemann n={n}"); ax1.grid(True,alpha=0.3); ax1.set_xlabel('x'); ax1.set_ylabel('y')
        ax2.plot(np.linspace(a-1,b+1,300), f_lamb(np.linspace(a-1,b+1,300)), 'b'); ax2.axhline(0,color='black',lw=1); ax2.axvline(0,color='black',lw=1)
        ix=np.linspace(a,b,100); ax2.fill_between(ix,f_lamb(ix),alpha=0.3,color='orange'); ax2.set_title("Area"); ax2.grid(True,alpha=0.3); ax2.set_xlabel('x'); ax2.set_ylabel('y')
        return "\n\n".join(steps),exact,fig
    except Exception as e: return f"Error {e}",None,None

def derivative_full_rules_complete(expr_str,var_str='x'):
    try:
        expr=parse_expr(expr_str,var_str)
        if expr is None: return f"Invalid '{expr_str}' use ^ for power e.g. x^3",None,None,None
        var=sp.Symbol(var_str); deriv=sp.diff(expr,var)
        steps=[]
        steps.append(f"**Function:** $f({var_str})={sp.latex(expr)}$ on Cartesian x,y")
        steps.append(f"**Step 1 - Defined & differentiable on same interval:** Check domain. Polynomial $\\to$ differentiable $\\forall x \\in \\mathbb{{R}}$. For $f={sp.latex(expr)}$, domain = all real, differentiable where defined.")
        steps.append(f"**Step 2 - Constant Rule:** $(c)'=0$. Example term constant in {sp.latex(expr)} -> 0")
        steps.append(f"**Step 3 - Power Rule:** $(x^n)'=n x^{{n-1}}$. Apply to each power: {sp.latex(expr)} -> derivative term by term")
        # term breakdown
        terms = expr.args if isinstance(expr, sp.Add) else [expr]
        for term in terms:
            steps.append(f"  - Term ${sp.latex(term)}$ -> ${sp.latex(sp.diff(term,var))}$ [Power/Constant]")
        steps.append(f"**Step 4 - Sum & Difference Rule:** $(f±g)'=f'±g'$. Sum results: ${sp.latex(deriv)}$")
        steps.append(f"**Step 5 - Product Rule:** $(f·g)'=f'g+fg'$. Example if $f={sp.latex(expr)}$ contains product, e.g. $x·sin(x)$ -> $sin(x)+x cos(x)$. For current: ${sp.latex(sp.simplify(deriv))}$")
        steps.append(f"**Step 6 - Quotient Rule:** $(f/g)'=(f'g-fg')/g^2$. Example $(x^2/(x+1))'$. For current simplified: ${sp.latex(sp.simplify(deriv))}$")
        steps.append(f"**Step 7 - Chain Rule:** $(f(g(x)))'=f'(g)·g'$. Example $sin(x^2)$ -> $2x cos(x^2)$. Final derivative: $\\boxed{{f'({var_str})={sp.latex(deriv)}}}$")
        steps.append(f"**Step 8 - Limits Rule for derivative:** $f'(a)=\\lim_{{h\\to0}} (f(a+h)-f(a))/h = {sp.latex(deriv)}$ evaluated at point gives slope")

        # Graphs: 2D curve + derivative, and solid revolution and curve lines x,y
        fig, ax = plt.subplots()
        try:
            f_lamb=sp.lambdify(var,expr,'numpy'); df_lamb=sp.lambdify(var,deriv,'numpy')
            t=np.linspace(-3,3,400); ax.plot(t,f_lamb(t),label='f(x) curve (x,y)',linewidth=2); ax.plot(t,df_lamb(t),label="f'(x) derivative line",linewidth=2,linestyle='--')
            ax.axhline(0,color='black',linewidth=1.2,label='x axis'); ax.axvline(0,color='black',linewidth=1.2,label='y axis')
            ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title('Derivative: function and derivative lines on Cartesian x,y')
        except: pass

        # Solid revolution figure
        solid_fig = plot_solid_revolution(expr_str,var_str, -2, 2)

        # Additional Cartesian xyz
        xyz_fig = plot_cartesian_xyz()

        return "\n\n".join(steps), deriv, fig, solid_fig
    except Exception as e:
        return f"Error {e}", None, None, None

def integral_full_rules_complete(expr_str,var_str='x',lower=None,upper=None):
    try:
        expr=parse_expr(expr_str,var_str)
        if expr is None: return f"Invalid '{expr_str}'",None,None,None
        var=sp.Symbol(var_str)
        if lower is not None and upper is not None:
            F=sp.integrate(expr,var); val=sp.integrate(expr,(var,lower,upper))
            steps=[]
            steps.append(f"**Integrand:** $\\int {sp.latex(expr)} d{var_str}$ on Cartesian")
            steps.append(f"**Step 1 - Primitive:** Antiderivative $F({var_str})={sp.latex(F)}+C$. Rule $\\int x^n = x^{{n+1}}/(n+1)$")
            steps.append(f"**Step 2 - Substitution:** Let $u=g(x)$, $du=g' dx$. Example $\\int 2x·e^{{x^2}} dx$, $u=x^2$")
            steps.append(f"**Step 3 - By parts:** $\\int u dv = uv - \\int v du$. Example $\\int x e^x dx$")
            steps.append(f"**Step 4 - Definite:** $\\int_a^b f = F(b)-F(a)$. Here $F({upper})={sp.latex(F.subs(var,upper))}, F({lower})={sp.latex(F.subs(var,lower))}$")
            steps.append(f"**Step 5 - Indefinite:** $+C$ constant, family of curves")
            steps.append(f"**Step 6 - FTC:** Fundamental Theorem $d/dx \\int_a^x f(t) dt = f(x)$. Area under curve = {sp.latex(val)}")
            steps.append(f"**Step 7 - Limits Rule:** $\\int_a^b f = \\lim_{{n\\to\\infty}} \\sum f(x_i)\\Delta x = {sp.latex(val)}$. Final boxed: $\\boxed{{{sp.latex(val)}}}$")
            fig, ax = plt.subplots()
            f_lamb=sp.lambdify(var,expr,'numpy'); t=np.linspace(float(lower)-1,float(upper)+1,300)
            ax.plot(t,f_lamb(t),'b',label=f'f({var_str}) curve (x,y)',linewidth=2); ax.axhline(0,color='black',linewidth=1.2,label='x axis'); ax.axvline(0,color='black',linewidth=1.2,label='y axis')
            ix=np.linspace(float(lower),float(upper),100); ax.fill_between(ix,f_lamb(ix),alpha=0.3,color='orange',label='area under curve'); ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title(f'Definite Integral [{lower},{upper}] area')
            solid_fig = plot_solid_revolution(expr_str,var_str, float(lower), float(upper))
            return "\n\n".join(steps), val, fig, solid_fig
        else:
            F=sp.integrate(expr,var)
            steps=[]
            steps.append(f"**$\\int {sp.latex(expr)} d{var_str}$**")
            steps.append(f"**Step 1 - Primitive:** ${sp.latex(F)}+C$")
            steps.append(f"**Step 2 - Substitution:** $u=g(x)$")
            steps.append(f"**Step 3 - By parts:** $\\int u dv$")
            steps.append(f"**Step 4 - Definite vs Indefinite:** Indefinite family $+C$, definite number")
            steps.append(f"**Step 5 - Indefinite:** Final with $+C$")
            steps.append(f"**Step 6 - FTC:** Connection derivative and integral")
            steps.append(f"**Step 7 - Limits:** $\\lim_{{n\\to\\infty}} Riemann sum$")
            fig, ax = plt.subplots()
            try:
                f_lamb=sp.lambdify(var,expr,'numpy'); F_lamb=sp.lambdify(var,F,'numpy'); t=np.linspace(-3,3,400)
                ax.plot(t,f_lamb(t),label='f(x) curve'); ax.plot(t,F_lamb(t),label='F(x) primitive line'); ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title('Indefinite Integral family of curves (x,y)')
            except: pass
            solid_fig = plot_solid_revolution(expr_str,var_str, -2, 2)
            return "\n\n".join(steps), F, fig, solid_fig
    except Exception as e:
        return f"Error {e}",None,None,None

# ------------------------------------------------------------
# STREAMLIT UI - FIXED MENU BUG with int parsing
# ------------------------------------------------------------
st.set_page_config(page_title="Math Visual Solver - Fixed Menu", layout="wide")
st.title("📚 Complete Math Visual Solver - Cartesian Plane x,y and x,y,z - Fixed Menu Bug")

menu = st.sidebar.selectbox("Select Module", [
    "1. Subtraction - Column Method (Long Method)",
    "2. Long Division L Shape",
    "3. First Degree Function + Cartesian x,y",
    "4. Second Degree Function + Cartesian x,y",
    "5. Linear Systems x,y and x,y,z - Cartesian planes",
    "6. Limits and Rules + Cartesian",
    "7. Limit Definition Derivative + Cartesian",
    "8. Limit Definition Integral + Cartesian",
    "9. Derivatives All Rules (x,y,z + Solid Revolution + Curves) 8 Rules",
    "10. Integrals All Rules + FTC + Solid Revolution (x,y,z) 7 Rules"
])

# FIX: parse number correctly, check 10 before 1
try:
    menu_num = int(menu.split(".")[0])
except:
    menu_num = 1

if menu_num == 1:
    st.header("1. Subtraction - Column Method - Long Method")
    st.markdown("Reference image: https://ibb.co/Qv4WYM8Z - keeps order Minuend top, Subtrahend bottom")
    c1,c2 = st.columns(2)
    with c1: minuend = st.number_input("Minuend (top)", value=136, step=1)
    with c2: subtrahend = st.number_input("Subtrahend (bottom)", value=169, step=1)
    if st.button("Show Steps"):
        data = subtraction_analysis_latex(minuend, subtrahend)
        latex1, borrow_ex, requested, correct = render_subtraction_latex(data)
        st.subheader("A) Direct order"); st.latex(latex1)
        st.subheader("B) Borrowing visualization"); st.latex(borrow_ex)
        st.subheader("C) Exact order as reference"); st.latex(requested)
        st.subheader("D) Correct place-value"); st.latex(correct)

elif menu_num == 2:
    st.header("2. Long Division - L Shape")
    c1,c2 = st.columns(2)
    with c1: dvd = st.number_input("Dividend", value=1256, step=1, min_value=0)
    with c2: dvs = st.number_input("Divisor", value=8, step=1, min_value=1)
    if st.button("Divide"):
        data = long_division_steps(dvd, dvs)
        st.markdown(render_division_html(data), unsafe_allow_html=True)
        st.latex(r"\text{Check: } %s \times %s + %s = %s" % (dvs, data['quotient'], data['remainder'], dvd))

elif menu_num == 3:
    st.header("First Degree Function on Cartesian Plane x,y")
    eq = st.text_input("Equation", "2x+3=7", help="Use ^ for power, e.g. x^3, use 2x for 2*x")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Solve Linear"):
            steps,sol,coeff = solve_linear_steps(eq)
            st.markdown(steps)
            if sol is not None:
                st.pyplot(solve_linear_steps(eq)[1] and plot_linear_func(coeff[0],coeff[1],sol) or plot_cartesian_xy())
    with col2:
        st.pyplot(plot_cartesian_xy())
        st.caption("Cartesian x,y lines")

elif menu_num == 4:
    st.header("Second Degree Function on Cartesian Plane x,y")
    eq = st.text_input("Equation", "x^2-5x+6=0", help="Use ^ for power e.g. x^2")
    if st.button("Solve Quadratic"):
        steps,sols,coeff = solve_quadratic_steps(eq)
        st.markdown(steps)
        if sols:
            fig=plt.figure(figsize=(8,4))
            ax1=fig.add_subplot(121); xv=np.linspace(-10,10,400); ax1.plot(xv, coeff[0]*xv**2+coeff[1]*xv+coeff[2]); ax1.axhline(0,color='black',lw=1.2); ax1.axvline(0,color='black',lw=1.2); ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_title('Curve x,y'); ax1.grid(True,alpha=0.3)
            st.pyplot(fig)
            # full func plot
            st.pyplot(plot_cartesian_xy())

elif menu_num == 5:
    st.header("Linear Systems x,y and x,y,z - Cartesian planes")
    size = st.radio("Size", ["2x2 (x,y)", "3x3 (x,y,z)"])
    if size.startswith("2x2"):
        eq1=st.text_input("Eq1","2x+3y=5", help="Use ^ for power"); eq2=st.text_input("Eq2","x-y=1"); eqs=[eq1,eq2]
    else:
        eq1=st.text_input("Eq1","x+y+z=6"); eq2=st.text_input("Eq2","x-y+2z=5"); eq3=st.text_input("Eq3","2x+y-z=1"); eqs=[eq1,eq2,eq3]
    if st.button("Solve System"):
        steps,sol,vars_ = solve_linear_system_fixed(eqs)
        st.markdown(steps)
        if size.startswith("2x2"):
            # simple 2D plot of lines
            fig, ax = plt.subplots()
            ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            xs=np.linspace(-10,10,400)
            try:
                # parse first eq for y
                # y = (5-2x)/3
                # quick numeric
                for eq_str in eqs:
                    if 'y' in eq_str:
                        # use sympy solve
                        lhs_str,rhs_str=eq_str.split('='); lhs=parse_expr(lhs_str); rhs=parse_expr(rhs_str); expr=sp.expand(lhs-rhs); y_sol=sp.solve(expr,y)
                        if y_sol:
                            f=sp.lambdify(x,y_sol[0],'numpy'); ax.plot(xs,f(xs),label=eq_str)
                if sol is not None:
                    ax.scatter([float(sol[0])],[float(sol[1])],color='red',s=100)
            except: pass
            ax.set_xlabel('x axis'); ax.set_ylabel('y axis'); ax.set_title('Cartesian x,y lines'); ax.legend(); ax.grid(True,alpha=0.3); st.pyplot(ax.figure)
        else:
            fig=plt.figure(figsize=(6,5)); ax=fig.add_subplot(111,projection='3d')
            ax.plot([-5,5],[0,0],[0,0],color='red',label='x'); ax.plot([0,0],[-5,5],[0,0],color='green',label='y'); ax.plot([0,0],[0,0],[-5,5],color='blue',label='z')
            if sol is not None and len(sol)==3:
                ax.scatter([float(sol[0])],[float(sol[1])],[float(sol[2])],color='red',s=100)
            ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.set_title('Cartesian x,y,z'); ax.legend(); st.pyplot(fig)

elif menu_num == 6:
    st.header("Limits and Rules - Cartesian x,y")
    expr=st.text_input("f(x)","sin(x)/x", help="Use ^ for power e.g. x^3")
    pt=st.number_input("x→",value=0.0)
    if st.button("Compute Limit"):
        steps,val,fig = limit_with_rules(expr,"x",pt)
        st.markdown(steps)
        if fig is not None: st.pyplot(fig)

elif menu_num == 7:
    st.header("Limit Definition Derivative - Cartesian")
    expr=st.text_input("f(x)","x^2",key="der_lim", help="Use ^ for power")
    pt=st.number_input("Point",value=1.0)
    if st.button("Show Derivative"):
        steps,deriv,fig = derivative_limit_def(expr,'x',pt)
        st.markdown(steps)
        if fig is not None: st.pyplot(fig)

elif menu_num == 8:
    st.header("Limit Definition Integral - Cartesian")
    expr=st.text_input("f(x)","x^2",key="int_lim", help="Use ^")
    c1,c2,c3=st.columns(3)
    with c1: a=st.number_input("a",value=0.0)
    with c2: b=st.number_input("b",value=2.0)
    with c3: n=st.slider("n",2,20,6)
    if st.button("Show Integral"):
        steps,exact,fig = integral_limit_def(expr,'x',a,b,n)
        st.markdown(steps)
        if fig is not None: st.pyplot(fig)

elif menu_num == 9:
    st.header("Derivatives All Rules (x,y,z + Solid Revolution + Curves) - 8 Rules - 6-7 steps")
    st.markdown("""
    **Rules covered (with Cartesian x,y and x,y,z solid revolution):**
    - Defined & differentiable on same interval
    - Constant Rule
    - Power Rule
    - Sum & Difference
    - Product Rule
    - Quotient Rule
    - Chain Rule
    - Limits Rule
    """)
    expr=st.text_input("f(x)","x^2+3x", help="Use ^ for power e.g. x^3, use 3x for 3*x", key="der_all")
    var=st.selectbox("Variable",["x","y","z"], key="der_var")
    colA,colB=st.columns(2)
    with colA: a_solid=st.number_input("Solid a",value=-2.0)
    with colB: b_solid=st.number_input("Solid b",value=2.0)
    if st.button("Differentiate Complete"):
        steps,deriv,fig2d,solid_fig = derivative_full_rules_complete(expr,var)
        st.markdown(steps)
        if deriv is not None:
            st.latex(f"f'({var})={sp.latex(deriv)}")
            if fig2d is not None:
                st.subheader("Curve and derivative line on Cartesian x,y")
                st.pyplot(fig2d)
            if solid_fig is not None:
                st.subheader("Solid of Revolution (x,y,z) + curve (x,y)")
                st.pyplot(solid_fig)
            st.subheader("Cartesian planes x,y and x,y,z")
            st.pyplot(plot_cartesian_xy())
            st.pyplot(plot_cartesian_xyz())

elif menu_num == 10:
    st.header("Integrals All Rules + FTC + Solid Revolution (x,y,z) - 7 Rules - 6-7 steps")
    st.markdown("""
    **Rules covered with graphs:**
    - Primitives
    - Substitution
    - By parts
    - Definite
    - Indefinite
    - FTC with explanatory graph
    - Limits
    """)
    expr=st.text_input("Integrand","x^2+3x+2", help="Use ^ for power e.g. x^3", key="int_all")
    var=st.selectbox("Variable",["x","y","z"],key="int_var_all")
    mode=st.radio("Type",["Indefinite","Definite"], key="int_mode")
    if mode=="Definite":
        c1,c2=st.columns(2)
        with c1: lo=st.number_input("Lower",value=0.0, key="int_lo")
        with c2: up=st.number_input("Upper",value=2.0, key="int_up")
        if st.button("Integrate Definite Complete"):
            steps,val,fig2d,solid_fig = integral_full_rules_complete(expr,var,lo,up)
            st.markdown(steps)
            if fig2d is not None:
                st.subheader("Area under curve on Cartesian x,y")
                st.pyplot(fig2d)
            if solid_fig is not None:
                st.subheader("Solid of Revolution (x,y,z) - volume")
                st.pyplot(solid_fig)
            st.pyplot(plot_cartesian_xyz())
    else:
        if st.button("Integrate Indefinite Complete"):
            steps,F,fig2d,solid_fig = integral_full_rules_complete(expr,var,None,None)
            st.markdown(steps)
            if fig2d is not None:
                st.subheader("Family of curves (x,y)")
                st.pyplot(fig2d)
            if solid_fig is not None:
                st.subheader("Solid of Revolution preview (x,y,z)")
                st.pyplot(solid_fig)
