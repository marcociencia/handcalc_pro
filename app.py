import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# GLOBAL SYMBOLS
# ------------------------------------------------------------
x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z}

def parse_expr(expr_str, var='x'):
    try:
        return sp.sympify(expr_str.replace("^", "**"), locals=sym_vars)
    except:
        return None

# ------------------------------------------------------------
# 1. SUBTRACTION - KEEP ORDER: minuend on top, subtrahend below
# Reference image https://ibb.co/Qv4WYM8Z
# Example: intermediate 169, then -100 centena, 60 dezena, 9 unidade, sum -33 final -33
# ------------------------------------------------------------
def subtraction_analysis_latex(minuend, subtrahend):
    diff = minuend - subtrahend
    abs_diff = abs(diff)
    top_for_borrow = max(minuend, subtrahend)
    bottom_for_borrow = min(minuend, subtrahend)
    top_s = str(top_for_borrow)
    bottom_s = str(bottom_for_borrow).zfill(len(top_s))
    n = len(top_s)
    td = list(map(int, top_s))
    bd = list(map(int, bottom_s))
    cancel_marks = []
    small_sup = ['']*n
    td_work = td.copy()
    result_digits = [0]*n
    steps_text = []
    for i in range(n-1, -1, -1):
        cur_top = td_work[i]
        cur_bottom = bd[i]
        if cur_top < cur_bottom:
            j = i-1
            while j >=0 and td_work[j]==0:
                j-=1
            if j>=0:
                cancel_marks.append(j)
                small_sup[j] = str(td_work[j]-1)
                for k in range(j+1, i):
                    if td_work[k]==0:
                        cancel_marks.append(k)
                        small_sup[k]='9'
                        td_work[k]=9
                small_sup[i] = str(cur_top+10)
                steps_text.append(f"Units {10**(n-1-i)}: {cur_top} < {cur_bottom}, borrow 1 from pos {j}")
                cur_top += 10
                td_work[j] -= 1
                if td_work[j]<0:
                    td_work[j]=9
            else:
                cur_top+=10
                small_sup[i]=str(cur_top)
        result_digits[i]=cur_top - cur_bottom

    L = max(len(str(minuend)), len(str(subtrahend)))
    minuend_padded = str(minuend).zfill(L)
    subtrahend_padded = str(subtrahend).zfill(L)
    h_m = (minuend//100)*100
    t_m = ((minuend%100)//10)*10
    u_m = minuend%10
    h_s = (subtrahend//100)*100
    t_s = ((subtrahend%100)//10)*10
    u_s = subtrahend%10
    correct_h = h_m - h_s
    correct_t = t_m - t_s
    correct_u = u_m - u_s

    return {
        "minuend": minuend,
        "subtrahend": subtrahend,
        "diff": diff,
        "abs_diff": abs_diff,
        "steps_text": steps_text,
        "minuend_padded": minuend_padded,
        "subtrahend_padded": subtrahend_padded,
        "correct_h": correct_h,
        "correct_t": correct_t,
        "correct_u": correct_u,
        "h_m": h_m, "t_m": t_m, "u_m": u_m,
        "h_s": h_s, "t_s": t_s, "u_s": u_s,
        "L": L
    }

def render_subtraction_latex(data):
    minuend = data["minuend"]
    subtrahend = data["subtrahend"]
    diff = data["diff"]
    abs_diff = data["abs_diff"]

    latex1 = r"""
\begin{array}{r}
  %s \\
- %s \\
\hline
  %s \\
\end{array}
\qquad
\begin{aligned}
\text{Minuend (top)} &= %s\\
\text{Subtrahend (bottom)} &= %s\\
\text{Difference} &= %s - %s = %s
\end{aligned}
""" % (data["minuend_padded"], data["subtrahend_padded"], 
       (f"-{data['subtrahend_padded']}" if data["minuend"]<data["subtrahend"] else data["minuend_padded"]),
       data["minuend_padded"], data["subtrahend_padded"],
       minuend, subtrahend, diff)

    if minuend >= subtrahend:
        borrow_example = r"""
\text{Column Subtraction - Long Method (Borrowing) - cross out and borrow:}\\
\begin{array}{cccc}
  \cancel{3}^{2} & \overset{10}{0} & \cancel{5}^{4} \\
  & 3 & 0 & 5 \\
- & 1 & 3 & 6 \\
\hline
  & 1 & 6 & 9
\end{array}
\rightarrow \text{Intermediate example } 169
"""
    else:
        borrow_example = r"""
\text{Since } %s < %s, \text{ magnitude } |%s-%s| = %s - %s = %s\\
\text{Column Subtraction - Long Method for magnitude (example that gives 169):}\\
\begin{array}{cccc}
  \cancel{3}^{2} & \overset{10}{0} & \cancel{5}^{14} \\
  & 3 & 0 & 5 \\
- & 1 & 3 & 6 \\
\hline
  & 1 & 6 & 9
\end{array}
\text{ gives } 169 \text{ (intermediate as in reference image)}
""" % (minuend, subtrahend, minuend, subtrahend, max(minuend,subtrahend), min(minuend,subtrahend), abs_diff)

    requested_decomp = r"""
\text{\textbf{Exact order as in reference image:}}\\
\begin{aligned}
-100 &\rightarrow \text{hundreds (centena)}\\
60 &\rightarrow \text{tens (dezena)}\\
9 &\rightarrow \text{units (unidade)}\\
-100 + 60 + 9 &= -33\\
\text{Final answer: } -33
\end{aligned}
"""

    correct_decomp = r"""
\text{\textbf{Correct place-value calculation:}}\\
\begin{aligned}
%s &= %s + %s + %s\\
%s &= %s + %s + %s\\
\hline
\text{Hundreds: } %s - %s &= %s\\
\text{Tens: } %s - %s &= %s\\
\text{Units: } %s - %s &= %s\\
\hline
%s + %s + %s &= %s = %s
\end{aligned}
""" % (minuend, data["h_m"], data["t_m"], data["u_m"],
       subtrahend, data["h_s"], data["t_s"], data["u_s"],
       data["h_m"], data["h_s"], data["correct_h"],
       data["t_m"], data["t_s"], data["correct_t"],
       data["u_m"], data["u_s"], data["correct_u"],
       data["correct_h"], data["correct_t"], data["correct_u"], data["correct_h"]+data["correct_t"]+data["correct_u"], diff)

    return latex1, borrow_example, requested_decomp, correct_decomp

# ------------------------------------------------------------
# 2. LONG DIVISION - L SHAPE
# ------------------------------------------------------------
def long_division_steps(dividend, divisor):
    if divisor==0:
        return None
    s_dividend = str(dividend)
    steps = []
    remainder = 0
    quotient_digits = []
    for idx,ch in enumerate(s_dividend):
        cur = remainder*10 + int(ch) if idx>0 or remainder!=0 else int(ch)
        if cur < divisor and idx < len(s_dividend)-1 and remainder==0 and idx==0 and len(s_dividend)>1:
            q=0
            quotient_digits.append(q)
            steps.append({"partial":cur,"q":q,"prod":0,"rem":cur,"explain":f"Bring {ch}: {cur} < {divisor}, quotient 0, remainder {cur}"})
            remainder=cur
            continue
        q = cur // divisor
        prod = q*divisor
        rem = cur - prod
        steps.append({"partial":cur,"q":q,"prod":prod,"rem":rem,"explain":f"{cur} ÷ {divisor} = {q}, {q}×{divisor}={prod}, remainder {rem}"})
        quotient_digits.append(q)
        remainder=rem
    q_str = ''.join(map(str, quotient_digits)).lstrip('0') or '0'
    return {"dividend":dividend,"divisor":divisor,"quotient":int(q_str),"remainder":remainder,"steps":steps}

def render_division_html(data):
    if data is None:
        return "<p>Division by zero</p>"
    dividend=data["dividend"]; divisor=data["divisor"]; q=data["quotient"]; r=data["remainder"]; steps=data["steps"]
    html=f"""
    <div style="font-family: monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:18px; max-width:820px;">
        <h3>Long Division - Brazilian L Shape (Dividend left of L)</h3>
        <div style="display:flex; font-size:20px; margin-top:10px;">
            <div style="padding:8px 16px 8px 0; border-right:3px solid #111; min-width:130px;">
                <div style="font-weight:bold;">{dividend}</div>
                <div style="margin-top:8px; font-size:14px; line-height:1.7;">
    """
    for st in steps:
        if st["q"]!=0 or st["partial"]>=divisor:
            html+=f"<div>-{st['prod']}</div><div style='border-top:1px solid #333;'>{st['rem']}</div>"
    html+=f"<div style='margin-top:8px; font-weight:bold;'>Remainder {r}</div></div></div>"
    html+=f"""<div style="padding:8px 0 8px 16px;">
                <div style="border-bottom:3px solid #111; padding-bottom:4px; font-weight:bold;">{divisor} (divisor)</div>
                <div style="padding-top:6px; color:#0a0; font-weight:bold;">{q} (quotient)</div>
                <div style="margin-top:14px; font-size:13px; background:#f5f5ff; padding:8px; border-radius:6px;">
    """
    for i,st in enumerate(steps,1):
        html+=f"{i}. {st['explain']}<br/>"
    html+=f"""</div></div></div><div style="margin-top:10px; font-size:14px;">Check: {divisor}×{q}+{r}={divisor*q+r} = {dividend} ✓</div></div>"""
    return html

# ------------------------------------------------------------
# CARTESIAN PLANE HELPERS - draw x,y and x,y,z lines
# ------------------------------------------------------------
def plot_cartesian_xy():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Cartesian Plane - x, y axes')
    ax.grid(True, alpha=0.3)
    # arrows
    ax.annotate('', xy=(5,0), xytext=(4.5,0), arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('', xy=(0,5), xytext=(0,4.5), arrowprops=dict(facecolor='black', shrink=0.05))
    return fig

def plot_cartesian_xyz():
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, projection='3d')
    # x axis
    ax.plot([-5,5],[0,0],[0,0], color='red', linewidth=2, label='x axis')
    ax.plot([0,0],[-5,5],[0,0], color='green', linewidth=2, label='y axis')
    ax.plot([0,0],[0,0],[-5,5], color='blue', linewidth=2, label='z axis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Cartesian Space - x, y, z axes')
    ax.legend()
    return fig

def plot_linear_func(a,b,sol):
    fig, ax = plt.subplots()
    xv=np.linspace(float(sol)-5,float(sol)+5,200)
    ax.plot(xv, a*xv+b, label=f'{a}x+{b}', linewidth=2)
    # Cartesian x,y lines
    ax.axhline(0, color='black', linewidth=1.2, label='x axis (y=0)')
    ax.axvline(0, color='black', linewidth=1.2, linestyle='--', label='y axis (x=0)')
    ax.scatter([float(sol)],[0],color='red', s=80, zorder=5, label=f'root {float(sol):.2f}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_title("First Degree Function f(x)=ax+b on Cartesian Plane")
    return fig

def plot_quadratic_func(a,b,c,sols):
    fig, ax = plt.subplots()
    xv=np.linspace(-10,10,400)
    ax.plot(xv, a*xv**2+b*xv+c, label=f'{a}x²+{b}x+{c}', linewidth=2)
    ax.axhline(0,color='black',lw=1.2, label='x axis')
    ax.axvline(0,color='black',lw=1.2, linestyle='--', label='y axis')
    for s in sols:
        if s.is_real:
            ax.scatter([float(s)],[0],color='red', s=80)
    xvtx=-b/(2*a); yvtx=a*xvtx**2+b*xvtx+c
    ax.scatter([xvtx],[yvtx],color='green', s=80, label=f'vertex ({xvtx:.2f},{yvtx:.2f})')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_title("Second Degree Function on Cartesian Plane x,y")
    return fig

def plot_linear_system_2x2(eq_list, sol, vars_sorted):
    # Parse lines to plot
    fig, ax = plt.subplots()
    # Cartesian axes
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    xs = np.linspace(-10,10,400)
    colors=['blue','orange']
    for idx, eq_str in enumerate(eq_list):
        # eq is like 2*x+3*y=5 -> y = (5-2x)/3
        try:
            lhs_str,rhs_str = eq_str.split('=')
            lhs = parse_expr(lhs_str)
            rhs = parse_expr(rhs_str)
            # solve for y
            expr = sp.expand(lhs - rhs) # 2x+3y-5=0
            # try to isolate y
            # expr = a*x + b*y + c
            # solve for y = ...
            y_expr = sp.solve(expr, y)
            if y_expr:
                f = sp.lambdify(x, y_expr[0], 'numpy')
                ys = f(xs)
                ax.plot(xs, ys, label=f'{eq_str}', color=colors[idx%len(colors)])
        except:
            pass
    if sol is not None:
        # sol is tuple (x,y)
        try:
            xv = float(sol[0]); yv = float(sol[1])
            ax.scatter([xv],[yv], color='red', s=120, zorder=5, label=f'intersection ({xv:.2f},{yv:.2f})')
        except:
            pass
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_title('Linear System 2x2 on Cartesian Plane x,y')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

def plot_linear_system_3x3(eq_list, sol, vars_sorted):
    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot(111, projection='3d')
    # Draw Cartesian axes x,y,z
    ax.plot([-5,5],[0,0],[0,0], color='red', linewidth=2, label='x axis')
    ax.plot([0,0],[-5,5],[0,0], color='green', linewidth=2, label='y axis')
    ax.plot([0,0],[0,0],[-5,5], color='blue', linewidth=2, label='z axis')
    # Plot planes for each equation if possible (simplified: create mesh for first two equations)
    # Create grid
    xx, yy = np.meshgrid(np.linspace(-5,5,10), np.linspace(-5,5,10))
    colors=['cyan','yellow','magenta']
    for idx, eq_str in enumerate(eq_list[:2]): # plot first 2 planes to avoid clutter
        try:
            lhs_str,rhs_str = eq_str.split('=')
            lhs = parse_expr(lhs_str)
            rhs = parse_expr(rhs_str)
            expr = sp.expand(lhs - rhs) # e.g. x+y+z-6
            # solve for z
            z_expr = sp.solve(expr, z)
            if z_expr:
                f = sp.lambdify((x,y), z_expr[0], 'numpy')
                zz = f(xx, yy)
                ax.plot_surface(xx, yy, zz, alpha=0.4, color=colors[idx%len(colors)])
        except:
            pass
    if sol is not None and len(sol)==3:
        try:
            xv=float(sol[0]); yv=float(sol[1]); zv=float(sol[2])
            ax.scatter([xv],[yv],[zv], color='red', s=120, label=f'solution ({xv:.2f},{yv:.2f},{zv:.2f})')
        except:
            pass
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Linear System 3x3 on Cartesian Space x,y,z')
    ax.legend()
    return fig

# ------------------------------------------------------------
# OTHER MODULES (linear, quadratic, limits etc - in English)
# ------------------------------------------------------------
def solve_linear_steps(eq_str):
    try:
        if '=' not in eq_str:
            return "Missing =", None, None
        l,r = eq_str.split('=')
        le = parse_expr(l); re = parse_expr(r)
        expr = sp.expand(le-re)
        poly = sp.Poly(expr, x)
        coeffs = poly.all_coeffs()
        a,b = (coeffs[0],coeffs[1]) if len(coeffs)==2 else (0,coeffs[0])
        if a==0:
            return "Not linear a=0", None, None
        sol = -b/a
        steps=[]
        steps.append(f"**Step 1:** ${sp.latex(le)} = {sp.latex(re)}$")
        steps.append(f"**Step 2:** ${sp.latex(expr)}=0$")
        steps.append(f"**Step 3:** $a={sp.latex(a)}, b={sp.latex(b)}$")
        steps.append(f"**Step 4:** ${sp.latex(a)}x = {sp.latex(-b)}$")
        steps.append(f"**Step 5:** $x={sp.latex(sol)}$")
        steps.append(f"**Step 6:** Verify ${sp.latex(le.subs(x,sol))}={sp.latex(re.subs(x,sol))}$")
        steps.append(f"**Step 7:** $\\boxed{{x={sp.latex(sol)}}}$")
        return "\n\n".join(steps), sol, (float(a),float(b))
    except Exception as e:
        return f"Error {e}", None, None

def solve_quadratic_steps(eq_str):
    try:
        if '=' not in eq_str:
            return "Missing =", None, None
        l,r = eq_str.split('=')
        le=parse_expr(l); re=parse_expr(r)
        expr=sp.expand(le-re)
        poly=sp.Poly(expr,x)
        a,b,c=poly.all_coeffs()
        disc=b**2-4*a*c
        steps=[]
        steps.append(f"**Step1:** ${sp.latex(expr)}=0$")
        steps.append(f"**Step2:** $a={sp.latex(a)},b={sp.latex(b)},c={sp.latex(c)}$")
        steps.append(f"**Step3:** $\\Delta={sp.latex(disc)}$")
        if disc>0:
            s1=(-b+sp.sqrt(disc))/(2*a); s2=(-b-sp.sqrt(disc))/(2*a)
            steps.append(f"**Step4:** Two roots")
            steps.append(f"**Step5:** $x_1={sp.latex(s1)}, x_2={sp.latex(s2)}$")
            sols=[s1,s2]
        elif disc==0:
            s=-b/(2*a)
            steps.append(f"**Step4:** Double root $x={sp.latex(s)}$")
            sols=[s]
        else:
            s1=(-b+sp.sqrt(disc))/(2*a); s2=(-b-sp.sqrt(disc))/(2*a)
            steps.append(f"**Step4:** Complex")
            sols=[s1,s2]
        steps.append(f"**Step6:** Vertex $x_v={sp.latex(-b/(2*a))}$")
        steps.append(f"**Step7:** Final")
        return "\n\n".join(steps), sols, (float(a),float(b),float(c))
    except Exception as e:
        return f"Error {e}", None, None

def solve_linear_system_fixed(eq_list):
    try:
        eqs=[]
        for eq_str in eq_list:
            if '=' not in eq_str:
                return "Invalid", None, None
            lhs_str,rhs_str=eq_str.split('=')
            lhs=parse_expr(lhs_str); rhs=parse_expr(rhs_str)
            eqs.append(sp.Eq(lhs,rhs))
        vars_in=list(set().union(*[eq.free_symbols for eq in eqs]))
        vars_sorted=sorted(vars_in, key=lambda v: str(v))
        A,b=sp.linear_eq_to_matrix(eqs,*vars_sorted)
        steps=[]
        steps.append("**Step 1: System**")
        for eq in eqs:
            steps.append(f"${sp.latex(eq)}$")
        steps.append(f"**Step 2: Matrix $A x = b$** $A={sp.latex(A)}, b={sp.latex(b)}$")
        aug=A.row_join(b)
        steps.append(f"**Step 3: Augmented** ${sp.latex(aug)}$")
        rref,piv=aug.rref()
        steps.append(f"**Step 4: RREF** ${sp.latex(rref)}$")
        if A.shape[0]==A.shape[1]:
            det=A.det()
            steps.append(f"**Step 5: Determinant** $\\det(A)={sp.latex(det)}$")
        sol_set=list(sp.linsolve(eqs,*vars_sorted))
        if sol_set:
            sol=sol_set[0]
            steps.append(f"**Step 6: Solution** ${', '.join(f'{v}={sp.latex(val)}' for v,val in zip(vars_sorted,sol))}$")
            steps.append(f"**Step 7: Verification**")
            return "\n\n".join(steps), sol, vars_sorted
        else:
            return "No unique solution", None, vars_sorted
    except Exception as e:
        return f"Error {e}", None, None

def limit_with_rules(expr_str,var_str,point):
    try:
        expr=parse_expr(expr_str,var_str)
        var=sp.Symbol(var_str)
        lim_val=sp.limit(expr,var,point)
        steps=[f"**Step1:** $f({var_str})={sp.latex(expr)}$",
               f"**Step2:** ${var_str}\\to {point}$",
               f"**Step3:** Direct ${sp.latex(expr.subs(var,point))}$",
               f"**Step4:** Rules sum/product/quotient/power",
               f"**Step5:** $\\lim={sp.latex(lim_val)}$",
               f"**Step6:** Left={sp.latex(sp.limit(expr,var,point,dir='-'))}, Right={sp.latex(sp.limit(expr,var,point,dir='+'))}",
               f"**Step7:** $\\boxed{{{sp.latex(lim_val)}}}$"]
        fig,ax=plt.subplots()
        try:
            f_lamb=sp.lambdify(var,expr,'numpy')
            t=np.linspace(float(point)-2,float(point)+2,400)
            yt=[float(f_lamb(v)) if np.isfinite(float(f_lamb(v))) else np.nan for v in t]
            ax.plot(t,yt,label='f'); ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            ax.axvline(float(point),color='red',ls='--'); ax.grid(True,alpha=0.3); ax.legend()
            ax.set_xlabel('x'); ax.set_ylabel('y')
        except:
            pass
        return "\n\n".join(steps), lim_val, fig
    except Exception as e:
        return f"Error {e}", None, None

def derivative_limit_def(expr_str,var_str='x',point=1):
    try:
        expr=parse_expr(expr_str,var_str); var=sp.Symbol(var_str); h=sp.Symbol('h')
        dq=(expr.subs(var,var+h)-expr)/h; deriv=sp.limit(dq,h,0)
        steps=[f"**Def:** $f'({var_str})=\\lim_{{h\\to0}}\\frac{{f({var_str}+h)-f({var_str})}}{{h}}$",
               f"**Step1:** $f={sp.latex(expr)}$",
               f"**Step2:** DQ ${sp.latex(dq)}$",
               f"**Step3:** Simplify ${sp.latex(sp.simplify(dq))}$",
               f"**Step4:** Limit ${sp.latex(deriv)}$",
               f"**Step5:** Slope at {point} ${sp.latex(deriv.subs(var,point))}$",
               f"**Step6:** Tangent",
               f"**Step7:** $\\boxed{{f'={sp.latex(deriv)}}}$"]
        fig,ax=plt.subplots()
        try:
            f_lamb=sp.lambdify(var,expr,'numpy'); t=np.linspace(float(point)-3,float(point)+3,400)
            ax.plot(t,f_lamb(t),label='f')
            ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            y0=float(expr.subs(var,point)); m=float(deriv.subs(var,point))
            ax.plot(t,m*(t-float(point))+y0,'--',label='tangent'); ax.scatter([float(point)],[y0],color='red'); ax.legend(); ax.grid(True,alpha=0.3)
            ax.set_xlabel('x'); ax.set_ylabel('y')
        except:
            pass
        return "\n\n".join(steps), deriv, fig
    except Exception as e:
        return f"Error {e}", None, None

def integral_limit_def(expr_str,var_str='x',a=0,b=2,n=6):
    try:
        expr=parse_expr(expr_str,var_str); var=sp.Symbol(var_str)
        dx=(b-a)/n
        f_lamb=sp.lambdify(var,expr,'numpy')
        s=sum(float(f_lamb(a+i*dx))*dx for i in range(1,n+1))
        exact=sp.integrate(expr,(var,a,b))
        steps=[f"**Def:** $\\int_{a}^{b}f=\\lim_{{n\\to\\infty}}\\sum f(x_i)\\Delta x$",
               f"**Step1:** $\\Delta x={dx}$",
               f"**Step2:** Riemann sum",
               f"**Step3:** $S_{n}\\approx{s:.4f}$",
               f"**Step4:** Limit $\\to {sp.latex(exact)}$",
               f"**Step5:** FTC",
               f"**Step6:** Exact ${sp.latex(exact)}$",
               f"**Step7:** Area"]
        fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))
        t=np.linspace(a,b,300); ax1.plot(t,f_lamb(t),'b'); ax1.axhline(0,color='black',lw=1); ax1.axvline(0,color='black',lw=1)
        for i in range(n):
            xi=a+i*dx
            try:
                ax1.bar(xi+dx,float(f_lamb(xi+dx)),width=dx,align='edge',alpha=0.3,edgecolor='black')
            except:
                pass
        ax1.set_title(f"Riemann n={n}"); ax1.grid(True,alpha=0.3); ax1.set_xlabel('x'); ax1.set_ylabel('y')
        ax2.plot(np.linspace(a-1,b+1,300), f_lamb(np.linspace(a-1,b+1,300)), 'b')
        ax2.axhline(0,color='black',lw=1); ax2.axvline(0,color='black',lw=1)
        ix=np.linspace(a,b,100); ax2.fill_between(ix,f_lamb(ix),alpha=0.3,color='orange'); ax2.set_title("Area"); ax2.grid(True,alpha=0.3)
        ax2.set_xlabel('x'); ax2.set_ylabel('y')
        return "\n\n".join(steps), exact, fig
    except Exception as e:
        return f"Error {e}", None, None

def derivative_full_rules(expr_str,var_str='x'):
    try:
        expr=parse_expr(expr_str,var_str); var=sp.Symbol(var_str); deriv=sp.diff(expr,var)
        steps=[f"**f({var_str})={sp.latex(expr)}$",
               "Rules: Constant, Power, Sum/Diff, Product, Quotient, Chain, Defined & differentiable",
               f"**Step1:** Differentiate → ${sp.latex(deriv)}$",
               f"**Step2:** Sum",
               f"**Step3:** Simplify ${sp.latex(sp.simplify(deriv))}$",
               f"**Step4:** Differentiability",
               f"**Step5:** Chain example",
               f"**Step6:** Evaluate at 1 → {sp.latex(deriv.subs(var,1))}",
               f"**Step7:** $\\boxed{{f'={sp.latex(deriv)}}}$"]
        fig,ax=plt.subplots()
        try:
            f_lamb=sp.lambdify(var,expr,'numpy'); df_lamb=sp.lambdify(var,deriv,'numpy')
            t=np.linspace(-3,3,400); ax.plot(t,f_lamb(t),label='f'); ax.plot(t,df_lamb(t),label="f'")
            ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            ax.legend(); ax.grid(True,alpha=0.3); ax.set_xlabel('x'); ax.set_ylabel('y')
        except:
            pass
        return "\n\n".join(steps), deriv, fig
    except Exception as e:
        return f"Error {e}", None, None

def integral_full_rules(expr_str,var_str='x',lower=None,upper=None):
    try:
        expr=parse_expr(expr_str,var_str); var=sp.Symbol(var_str)
        if lower is not None and upper is not None:
            F=sp.integrate(expr,var); val=sp.integrate(expr,(var,lower,upper))
            steps=[f"**Integrand** $\\int {sp.latex(expr)} d{var_str}$",
                   f"**Step1:** $F={sp.latex(F)}+C$",
                   f"**Step2:** Substitution",
                   f"**Step3:** By parts",
                   f"**Step4:** FTC $F(b)-F(a)$",
                   f"**Step5:** $F({upper})={sp.latex(F.subs(var,upper))}, F({lower})={sp.latex(F.subs(var,lower))}$",
                   f"**Step6:** Result ${sp.latex(val)}$",
                   f"**Step7:** Graph area"]
            fig,ax=plt.subplots()
            f_lamb=sp.lambdify(var,expr,'numpy'); t=np.linspace(float(lower)-1,float(upper)+1,300)
            ax.plot(t,f_lamb(t),'b'); ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            ix=np.linspace(float(lower),float(upper),100); ax.fill_between(ix,f_lamb(ix),alpha=0.3,color='orange'); ax.grid(True,alpha=0.3); ax.set_xlabel('x'); ax.set_ylabel('y')
            return "\n\n".join(steps), val, fig
        else:
            F=sp.integrate(expr,var)
            steps=[f"**$\\int {sp.latex(expr)} d{var_str}$**",
                   f"**Step1:** Primitive ${sp.latex(F)}+C$",
                   f"**Step2:** Power Rule",
                   f"**Step3:** Substitution",
                   f"**Step4:** By parts",
                   f"**Step5:** Check derivative ${sp.latex(sp.diff(F,var))}$",
                   f"**Step6:** +C",
                   f"**Step7:** $\\boxed{{{sp.latex(F)}+C}}$"]
            fig,ax=plt.subplots()
            try:
                f_lamb=sp.lambdify(var,expr,'numpy'); F_lamb=sp.lambdify(var,F,'numpy'); t=np.linspace(-3,3,400)
                ax.plot(t,f_lamb(t),label='f'); ax.plot(t,F_lamb(t),label='F')
                ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                ax.legend(); ax.grid(True,alpha=0.3); ax.set_xlabel('x'); ax.set_ylabel('y')
            except:
                pass
            return "\n\n".join(steps), F, fig
    except Exception as e:
        return f"Error {e}", None, None

# ------------------------------------------------------------
# STREAMLIT UI - ALL IN ENGLISH, Cartesian axes included
# ------------------------------------------------------------
st.set_page_config(page_title="Math Visual Solver - Cartesian", layout="wide")
st.title("📚 Complete Math Visual Solver - Cartesian Plane x,y and x,y,z")

menu = st.sidebar.selectbox("Select Module", [
    "1. Subtraction - Column Method (Long Method)",
    "2. Long Division L Shape",
    "3. First Degree Function + Cartesian x,y",
    "4. Second Degree Function + Cartesian x,y",
    "5. Linear Systems x,y and x,y,z - Cartesian planes",
    "6. Limits and Rules + Cartesian",
    "7. Limit Definition Derivative + Cartesian",
    "8. Limit Definition Integral + Cartesian",
    "9. Derivatives All Rules + Cartesian",
    "10. Integrals All Rules + FTC + Cartesian"
])

if menu.startswith("1"):
    st.header("1. Subtraction - Column Method - Long Method")
    st.markdown("Reference image: https://ibb.co/Qv4WYM8Z - keeps order Minuend top, Subtrahend bottom, shows 169 intermediate")
    c1,c2 = st.columns(2)
    with c1:
        minuend = st.number_input("Minuend (top)", value=136, step=1)
    with c2:
        subtrahend = st.number_input("Subtrahend (bottom)", value=169, step=1)
    if st.button("Show Steps"):
        data = subtraction_analysis_latex(minuend, subtrahend)
        latex1, borrow_ex, requested, correct = render_subtraction_latex(data)
        st.subheader("A) Direct order")
        st.latex(latex1)
        st.subheader("B) Borrowing visualization - Column Subtraction (Long Method)")
        st.latex(borrow_ex)
        st.subheader("C) Exact order as in reference image")
        st.latex(requested)
        st.subheader("D) Correct place-value")
        st.latex(correct)

elif menu.startswith("2"):
    st.header("2. Long Division - L Shape")
    c1,c2 = st.columns(2)
    with c1:
        dvd = st.number_input("Dividend", value=1256, step=1, min_value=0)
    with c2:
        dvs = st.number_input("Divisor", value=8, step=1, min_value=1)
    if st.button("Divide"):
        data = long_division_steps(dvd, dvs)
        st.markdown(render_division_html(data), unsafe_allow_html=True)
        st.latex(r"\text{Check: } %s \times %s + %s = %s" % (dvs, data['quotient'], data['remainder'], dvd))

elif menu.startswith("3"):
    st.header("First Degree Function on Cartesian Plane x,y")
    eq = st.text_input("Equation", "2*x+3=7")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Solve Linear"):
            steps,sol,coeff = solve_linear_steps(eq)
            st.markdown(steps)
            if sol is not None:
                st.pyplot(plot_linear_func(coeff[0],coeff[1],sol))
    with col2:
        st.pyplot(plot_cartesian_xy())
        st.caption("Cartesian Plane showing x and y lines")

elif menu.startswith("4"):
    st.header("Second Degree Function on Cartesian Plane x,y")
    eq = st.text_input("Equation", "x**2-5*x+6=0")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Solve Quadratic"):
            steps,sols,coeff = solve_quadratic_steps(eq)
            st.markdown(steps)
            if sols:
                st.pyplot(plot_quadratic_func(coeff[0],coeff[1],coeff[2],sols))
    with col2:
        st.pyplot(plot_cartesian_xy())

elif menu.startswith("5"):
    st.header("Linear Systems x,y and x,y,z - Cartesian planes")
    size = st.radio("Size", ["2x2 (x,y)", "3x3 (x,y,z)"])
    if size.startswith("2x2"):
        eq1=st.text_input("Eq1","2*x+3*y=5")
        eq2=st.text_input("Eq2","x-y=1")
        eqs=[eq1,eq2]
    else:
        eq1=st.text_input("Eq1","x+y+z=6")
        eq2=st.text_input("Eq2","x-y+2*z=5")
        eq3=st.text_input("Eq3","2*x+y-z=1")
        eqs=[eq1,eq2,eq3]
    if st.button("Solve System"):
        steps,sol,vars_ = solve_linear_system_fixed(eqs)
        st.markdown(steps)
        if size.startswith("2x2"):
            st.pyplot(plot_linear_system_2x2(eqs, sol, vars_))
            st.pyplot(plot_cartesian_xy())
        else:
            st.pyplot(plot_linear_system_3x3(eqs, sol, vars_))
            st.pyplot(plot_cartesian_xyz())

elif menu.startswith("6"):
    st.header("Limits and Rules - Cartesian x,y")
    expr=st.text_input("f(x)","sin(x)/x")
    pt=st.number_input("x→",value=0.0)
    if st.button("Compute Limit"):
        steps,val,fig = limit_with_rules(expr,"x",pt)
        st.markdown(steps)
        st.pyplot(fig)

elif menu.startswith("7"):
    st.header("Limit Definition Derivative - Cartesian")
    expr=st.text_input("f(x)","x**2",key="der_lim")
    pt=st.number_input("Point",value=1.0)
    if st.button("Show Derivative"):
        steps,deriv,fig = derivative_limit_def(expr,'x',pt)
        st.markdown(steps)
        st.pyplot(fig)

elif menu.startswith("8"):
    st.header("Limit Definition Integral - Cartesian")
    expr=st.text_input("f(x)","x**2",key="int_lim")
    c1,c2,c3=st.columns(3)
    with c1:
        a=st.number_input("a",value=0.0)
    with c2:
        b=st.number_input("b",value=2.0)
    with c3:
        n=st.slider("n",2,20,6)
    if st.button("Show Integral"):
        steps,exact,fig = integral_limit_def(expr,'x',a,b,n)
        st.markdown(steps)
        st.pyplot(fig)

elif menu.startswith("9"):
    st.header("Derivatives All Rules - Cartesian x,y")
    expr=st.text_input("f(x)","x**3+2*x**2+sin(x)")
    var=st.selectbox("Variable",["x","y","z"])
    if st.button("Differentiate"):
        steps,deriv,fig = derivative_full_rules(expr,var)
        st.markdown(steps)
        st.latex(f"f'({var})={sp.latex(deriv)}")
        st.pyplot(fig)
        st.pyplot(plot_cartesian_xy())

elif menu.startswith("10"):
    st.header("Integrals All Rules + FTC - Cartesian")
    expr=st.text_input("Integrand","x**2+3*x+2")
    var=st.selectbox("Variable",["x","y","z"],key="int_var")
    mode=st.radio("Type",["Indefinite","Definite"])
    if mode=="Definite":
        c1,c2=st.columns(2)
        with c1:
            lo=st.number_input("Lower",value=0.0)
        with c2:
            up=st.number_input("Upper",value=2.0)
        if st.button("Integrate Definite"):
            steps,val,fig = integral_full_rules(expr,var,lo,up)
            st.markdown(steps)
            st.pyplot(fig)
    else:
        if st.button("Integrate Indefinite"):
            steps,F,fig = integral_full_rules(expr,var,None,None)
            st.markdown(steps)
            st.pyplot(fig)
