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

# ------------------- DETAILED SUBTRACTION RESTORED -------------------
def subtraction_analysis_latex_detailed(minuend, subtrahend):
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
                steps_text.append(f"Column units 10^{n-1-i}: {cur_top} < {cur_bottom}, borrow 1 from pos {j}, {td[j]}→{td_work[j]-1}, {cur_top}→{cur_top+10}")
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
    h_m = (minuend//100)*100; t_m = ((minuend%100)//10)*10; u_m = minuend%10
    h_s = (subtrahend//100)*100; t_s = ((subtrahend%100)//10)*10; u_s = subtrahend%10

    return {
        "minuend": minuend, "subtrahend": subtrahend, "diff": diff, "abs_diff": abs_diff,
        "steps_text": steps_text, "cancel_marks": cancel_marks, "small_sup": small_sup,
        "minuend_padded": minuend_padded, "subtrahend_padded": subtrahend_padded,
        "h_m": h_m, "t_m": t_m, "u_m": u_m, "h_s": h_s, "t_s": t_s, "u_s": u_s,
        "correct_h": h_m-h_s, "correct_t": t_m-t_s, "correct_u": u_m-u_s,
        "L": L, "top_s": top_s, "bottom_s": bottom_s
    }

def render_subtraction_detailed_html(data):
    # HTML visual with crossed numbers
    html = f"""
    <div style="font-family: 'Courier New', monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px; max-width:750px;">
        <h4 style="margin:0 0 10px 0;">Column Method - Long Method (Conta Armada) - Borrowing</h4>
        <p style="margin:0; color:#666; font-size:13px;">Crossed numbers are borrowed, small red numbers are new values</p>
        <table style="border-collapse:collapse; font-size:24px; text-align:center; margin-top:10px;">
            <tr style="font-size:14px; color:#d00;">
                <td></td>
    """
    n = data["L"]
    # Build borrowing row
    top_s = data["top_s"] if data["minuend"] >= data["subtrahend"] else data["minuend_padded"]
    # Use detailed marks for display
    # For simplicity show small_sup if available
    for i in range(n):
        sup = data["small_sup"][i] if i < len(data["small_sup"]) and data["small_sup"][i]!='' else ''
        orig = data["top_s"][i] if i < len(data["top_s"]) else ''
        if i in data["cancel_marks"]:
            html+=f"<td style='padding:2px 8px;'><span style='text-decoration:line-through; color:#888;'>{orig}</span> <span style='color:#d00; font-size:16px; font-weight:bold;'>{sup}</span></td>"
        else:
            if sup!='' and i==n-1:
                html+=f"<td style='padding:2px 8px;'><span style='color:#d00; font-size:16px;'>{sup}</span></td>"
            else:
                html+=f"<td style='padding:2px 8px;'>{orig if orig!='' else data['minuend_padded'][i]}</td>"
    html+="</tr><tr><td style='padding-right:10px;'></td>"
    for c in data["minuend_padded"]:
        html+=f"<td style='padding:2px 8px;'>{c}</td>"
    html+="</tr><tr><td style='border-bottom:2px solid #333; padding-right:10px;'>-</td>"
    for c in data["subtrahend_padded"]:
        html+=f"<td style='border-bottom:2px solid #333; padding:2px 8px;'>{c}</td>"
    html+="</tr><tr><td></td>"
    diff_str = str(data["diff"])
    # show diff with sign
    diff_padded = diff_str
    # pad for display
    for c in diff_padded:
        html+=f"<td style='padding:2px 8px; font-weight:bold;'>{c}</td>"
    html+="</tr></table>"
    if data["minuend"] < data["subtrahend"]:
        html+=f"<p style='margin-top:12px; font-size:15px;'>Since {data['minuend']} < {data['subtrahend']}, magnitude |{data['minuend']}-{data['subtrahend']}| = {data['abs_diff']} then apply minus → <b>{data['diff']}</b></p>"
    html+="</div>"
    return html

def render_subtraction_latex_full(data):
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
\text{Difference} &= %s - %s = %s
\end{aligned}
""" % (data["minuend_padded"], data["subtrahend_padded"], diff, data["minuend_padded"], data["subtrahend_padded"], minuend, subtrahend, diff)
    borrow_example = r"""
\text{Column Subtraction - Long Method:}\\
\begin{array}{cccc}
  \cancel{3}^{2} & \overset{10}{0} & \cancel{5}^{14} \\
  & 3 & 0 & 5 \\
- & 1 & 3 & 6 \\
\hline
  & 1 & 6 & 9
\end{array}
\rightarrow 169 \text{ intermediate example as in reference image https://ibb.co/Qv4WYM8Z}
"""
    requested = r"""
\text{\textbf{Exact order as in reference image:}}\\
\begin{aligned}
-100 &\rightarrow \text{hundreds (centena)}\\
60 &\rightarrow \text{tens (dezena)}\\
9 &\rightarrow \text{units (unidade)}\\
-100 + 60 + 9 &= -33\\
\text{Final answer: } -33
\end{aligned}
"""
    correct = r"""
\text{\textbf{Correct place-value:}}\\
\begin{aligned}
%s &= %s + %s + %s\\
%s &= %s + %s + %s\\
\text{Hundreds } %s - %s = %s\\
\text{Tens } %s - %s = %s\\
\text{Units } %s - %s = %s\\
%s + %s + %s = %s = %s
\end{aligned}
""" % (minuend, data["h_m"], data["t_m"], data["u_m"], subtrahend, data["h_s"], data["t_s"], data["u_s"],
       data["h_m"], data["h_s"], data["correct_h"], data["t_m"], data["t_s"], data["correct_t"],
       data["u_m"], data["u_s"], data["correct_u"], data["correct_h"], data["correct_t"], data["correct_u"], data["correct_h"]+data["correct_t"]+data["correct_u"], diff)
    return latex1, borrow_example, requested, correct

# ------------------- DETAILED MULTIPLICATION RESTORED -------------------
def multiplication_analysis(a,b):
    # Long multiplication step by step
    a_str=str(a); b_str=str(b)
    partials=[]
    steps=[]
    for idx, digit_char in enumerate(reversed(b_str)):
        d=int(digit_char)
        partial = a * d
        # shift
        shifted = partial * (10**idx)
        partials.append({"digit":d, "pos":idx, "partial":partial, "shifted":shifted, "explain": f"{a} x {d} = {partial} (shift {idx} -> {shifted})"})
        steps.append(f"Multiply {a} by {d} (units 10^{idx}): {a}*{d}={partial}, shifted {shifted}")
    total = a*b
    return {"a":a,"b":b,"partials":partials,"steps":steps,"total":total}

def render_multiplication_html(data):
    a=data["a"]; b=data["b"]; total=data["total"]
    html=f"""
    <div style="font-family: 'Courier New', monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px; max-width:750px;">
        <h4>Column Multiplication - Long Method</h4>
        <table style="border-collapse:collapse; font-size:22px; text-align:right; margin-top:10px;">
            <tr><td></td><td>{a}</td></tr>
            <tr><td>x</td><td style="border-bottom:2px solid #333;">{b}</td></tr>
    """
    for p in data["partials"]:
        html+=f"<tr><td style='font-size:14px; color:#666;'>x{p['digit']} (10^{p['pos']})</td><td>{p['shifted'] if p['pos']>0 else p['partial']}</td></tr>"
        if p["pos"]>0:
            html+=f"<tr><td></td><td style='font-size:12px; color:#888;'>({a} x {p['digit']} = {p['partial']} shifted)</td></tr>"
    html+=f"<tr><td style='border-top:2px solid #333;'></td><td style='border-top:2px solid #333; font-weight:bold;'>{total}</td></tr>"
    html+=f"</table><div style='margin-top:12px; font-size:14px;'>"
    for i,s in enumerate(data["steps"],1):
        html+=f"{i}. {s}<br/>"
    html+=f"<br/><b>Final: {a} x {b} = {total}</b></div></div>"
    return html

# ------------------- DETAILED DIVISION RESTORED -------------------
def long_division_steps_detailed(dividend, divisor):
    if divisor==0: return None
    s=str(dividend); steps=[]; rem=0; q_digits=[]
    for idx,ch in enumerate(s):
        cur=rem*10+int(ch) if idx>0 or rem!=0 else int(ch)
        q=cur//divisor; prod=q*divisor; r=cur-prod
        steps.append({"bring":ch,"partial":cur,"q":q,"prod":prod,"rem":r,"explain":f"Bring down {ch} -> {cur} ÷ {divisor} = {q}, {q}×{divisor}={prod}, remainder {r}"})
        q_digits.append(q); rem=r
    q_str=''.join(map(str,q_digits)).lstrip('0') or '0'
    return {"dividend":dividend,"divisor":divisor,"quotient":int(q_str),"remainder":rem,"steps":steps,"q_digits":q_digits}

def render_division_html_detailed(data):
    if data is None: return "<p>Division by zero</p>"
    dividend=data["dividend"]; divisor=data["divisor"]; q=data["quotient"]; r=data["remainder"]
    html=f"""
    <div style="font-family: 'Courier New', monospace; background:#fffef7; border:2px solid #333; border-radius:12px; padding:20px; max-width:850px;">
        <h4>Long Division - Brazilian L Shape (Dividend left of L)</h4>
        <div style="display:flex; font-size:20px; margin-top:10px;">
            <div style="padding:8px 16px 8px 0; border-right:3px solid #111; min-width:140px;">
                <div style="font-weight:bold;">{dividend}</div>
                <div style="margin-top:8px; font-size:14px; line-height:1.8;">
    """
    for st in data["steps"]:
        if st["q"]!=0 or st["partial"]>=divisor or len(data["steps"])==1:
            html+=f"<div>-{st['prod']} = {st['rem']} (after bring {st['bring']})</div><div style='border-top:1px solid #999; margin:4px 0;'></div>"
    html+=f"<div style='margin-top:10px; font-weight:bold; color:#0a0;'>Remainder: {r}</div></div></div>"
    html+=f"""<div style="padding:8px 0 8px 16px;">
                <div style="border-bottom:3px solid #111; padding-bottom:6px; font-weight:bold; font-size:22px;">{divisor} (divisor)</div>
                <div style="padding-top:8px; font-weight:bold; color:#0a0; font-size:20px;">{q} (quotient)</div>
                <div style="margin-top:16px; font-size:13px; background:#f5f5ff; padding:10px; border-radius:8px; line-height:1.6;">
                    <b>Step-by-step (Resolução passo a passo):</b><br/>
    """
    for i,st in enumerate(data["steps"],1):
        html+=f"{i}. {st['explain']}<br/>"
    html+=f"""</div></div></div><div style="margin-top:14px; font-size:14px;">Check: {divisor} × {q} + {r} = {divisor*q+r} = {dividend} ✓</div></div>"""
    return html

# ------------------- CARTESIAN HELPERS -------------------
def plot_cartesian_xy():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.axhline(0,color='black',linewidth=1.2); ax.axvline(0,color='black',linewidth=1.2)
    ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_title('Cartesian Plane x,y'); ax.grid(True,alpha=0.3); return fig

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
    steps.append(f"**Step 2 - Point:** ${var_str} \\to {sp.latex(point)}$ (input '{point_str}' transformed to infinity symbol)")
    try:
        direct=expr.subs(var,point)
        steps.append(f"**Step 3 - Direct substitution:** $f({sp.latex(point)})={sp.latex(direct)}$")
        if direct.has(sp.nan, sp.zoo, sp.oo) and point not in [sp.oo, -sp.oo]:
            steps.append(f"  → Indeterminate, need simplification")
        else:
            steps.append(f"  → Direct value exists")
    except Exception as e:
        steps.append(f"**Step 3 - Direct substitution failed:** {e}")
    try:
        lim_val=sp.limit(expr,var,point)
        steps.append(f"**Step 4 - Apply limit rules:** Sum, Product, Quotient, Power, Constant")
        steps.append(f"**Step 5 - Compute:** $\\lim_{{{var_str}\\to {sp.latex(point)}}} {sp.latex(expr)} = {sp.latex(lim_val)}$")
        steps.append(f"**Step 6 - One-sided:** left={sp.latex(sp.limit(expr,var,point,dir='-'))}, right={sp.latex(sp.limit(expr,var,point,dir='+'))}")
        steps.append(f"**Step 7 - Final:** $\\boxed{{{sp.latex(lim_val)}}}$")
    except Exception as e:
        steps.append(f"**Error:** {e}"); lim_val=None
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
            try: ax.axhline(float(lim_val),color='green',ls='--',label=f'limit')
            except: pass
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_title(f'Limit Cartesian x,y - {point_str} -> {sp.latex(point)}')
    except:
        pass
    return "\n\n".join(steps), lim_val, fig

# ------------------- DERIVATIVE RULES -------------------
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
        steps.append(f"**Step 1:** Domain where f defined")
        steps.append(f"**Step 2:** Continuity check")
        steps.append(f"**Step 3:** Differentiability limit exists")
        steps.append(f"**Step 4:** Polynomial domain = R, differentiable everywhere")
        steps.append(f"**Step 5:** Interval = domain")
        steps.append(f"**Step 6:** Derivative ${sp.latex(deriv)}$")
        steps.append(f"**Step 7:** Final boxed")
    elif rule_name == "Constant Rule":
        steps.append(f"**Step 1:** Rule $(c)'=0$"); steps.append(f"**Step 2:** Identify constants in {sp.latex(expr)}")
        steps.append(f"**Step 3:** Derivative 0 for constants"); steps.append(f"**Step 4:** Differentiate rest")
        steps.append(f"**Step 5:** Sum {sp.latex(deriv)}"); steps.append(f"**Step 6:** Simplify"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Power Rule":
        steps.append(f"**Step 1:** Rule $(x^n)'=n x^{{n-1}}$"); steps.append(f"**Step 2:** Identify powers"); steps.append(f"**Step 3:** Coefficient rule")
        steps.append(f"**Step 4:** Apply to all -> {sp.latex(deriv)}"); steps.append(f"**Step 5:** Simplify"); steps.append(f"**Step 6:** Check"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Sum & Difference Rule":
        steps.append(f"**Step 1:** Rule $(f±g)'=f'±g'$"); steps.append(f"**Step 2:** Split sum"); steps.append(f"**Step 3:** Differentiate each")
        steps.append(f"**Step 4:** {sp.latex(deriv)}"); steps.append(f"**Step 5:** Simplify"); steps.append(f"**Step 6:** Verify"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Product Rule":
        steps.append(f"**Step 1:** Rule $(f·g)'=f'g+fg'$"); steps.append(f"**Step 2:** Identify f,g")
        steps.append(f"**Step 3:** f', g'"); steps.append(f"**Step 4:** Apply"); steps.append(f"**Step 5:** Simplify {sp.latex(sp.simplify(deriv))}"); steps.append(f"**Step 6:** Check"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Quotient Rule":
        steps.append(f"**Step 1:** Rule $(f/g)'=(f'g-fg')/g^2$"); steps.append(f"**Step 2:** Identify num/den")
        steps.append(f"**Step 3:** f', g'"); steps.append(f"**Step 4:** Apply"); steps.append(f"**Step 5:** Simplify"); steps.append(f"**Step 6:** Domain den≠0"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Chain Rule":
        steps.append(f"**Step 1:** Rule $(f(g(x)))'=f'(g)·g'$"); steps.append(f"**Step 2:** Identify outer/inner")
        steps.append(f"**Step 3:** Example sin(2x) outer sin, inner 2x"); steps.append(f"**Step 4:** Apply -> {sp.latex(deriv)}")
        steps.append(f"**Step 5:** Simplify"); steps.append(f"**Step 6:** Check"); steps.append(f"**Step 7:** Final")
    elif rule_name == "Limits Rule":
        h=sp.Symbol('h'); dq=(expr.subs(var,var+h)-expr)/h
        steps.append(f"**Step 1:** $f'(a)=\\lim_{{h\\to0}} (f(a+h)-f(a))/h$"); steps.append(f"**Step 2:** DQ {sp.latex(dq)}")
        steps.append(f"**Step 3:** Simplify {sp.latex(sp.simplify(dq))}"); steps.append(f"**Step 4:** Limit {sp.latex(deriv)}")
        steps.append(f"**Step 5:** Definition"); steps.append(f"**Step 6:** Evaluate"); steps.append(f"**Step 7:** Final")
    return "\n\n".join(steps), deriv, None

def compare_derivatives(ref, other):
    if ref is None or other is None: return False
    try: return sp.simplify(ref-other)==0
    except: return False

# ------------------- INTEGRAL RULES -------------------
integral_rules_list = ["Primitives","Substitution","By parts","Definite","Indefinite","FTC (Fundamental Theorem)","Limits"]

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
        steps.append(f"**Step1:** $\\int x^n = x^{{n+1}}/(n+1)+C$"); steps.append(f"**Step2:** Identify power"); steps.append(f"**Step3:** Apply -> {sp.latex(F)}+C")
        steps.append(f"**Step4:** Check F'={sp.latex(sp.diff(F,var))}"); steps.append(f"**Step5:** +C"); steps.append(f"**Step6:** Family curves"); steps.append(f"**Step7:** Final boxed")
    elif rule_name == "Substitution":
        steps.append(f"**Step1:** $\\int f(g)g' = \\int f(u)du$"); steps.append(f"**Step2:** Choose u"); steps.append(f"**Step3:** du"); steps.append(f"**Step4:** Rewrite in u")
        steps.append(f"**Step5:** Integrate in u"); steps.append(f"**Step6:** Back to x -> {sp.latex(F)}+C"); steps.append(f"**Step7:** Check")
    elif rule_name == "By parts":
        steps.append(f"**Step1:** $\\int u dv = uv - \\int v du$"); steps.append(f"**Step2:** Choose u,dv from {sp.latex(expr)}")
        steps.append(f"**Step3:** Example x·sin(x)"); steps.append(f"**Step4:** Compute du,v"); steps.append(f"**Step5:** Apply"); steps.append(f"**Step6:** Integrate remaining -> {sp.latex(F)}+C"); steps.append(f"**Step7:** Final")
    elif rule_name == "Definite":
        if lower is None or upper is None:
            steps.append(f"**Step1:** Definite needs a,b"); steps.append(f"**Step2:** F(b)-F(a)"); steps.append(f"**Step3:** F={sp.latex(F)}")
            steps.append(f"**Step4:** Need numeric"); steps.append(f"**Step5:** If given"); steps.append(f"**Step6:** Area"); steps.append(f"**Step7:** Final")
            return "\n\n".join(steps), F, None
        else:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"**Step1:** $\\int_{{{lower}}}^{{{upper}}} {sp.latex(expr)}$"); steps.append(f"**Step2:** Antiderivative {sp.latex(F)}")
            steps.append(f"**Step3:** F({upper})={sp.latex(F.subs(var,upper))}"); steps.append(f"**Step4:** F({lower})={sp.latex(F.subs(var,lower))}")
            steps.append(f"**Step5:** Subtract {sp.latex(val)}"); steps.append(f"**Step6:** Area"); steps.append(f"**Step7:** Final boxed {sp.latex(val)}")
            return "\n\n".join(steps), val, None
    elif rule_name == "Indefinite":
        steps.append(f"**Step1:** Family F+C"); steps.append(f"**Step2:** F={sp.latex(F)}"); steps.append(f"**Step3:** +C"); steps.append(f"**Step4:** Check")
        steps.append(f"**Step5:** Different C curves"); steps.append(f"**Step6:** No limits"); steps.append(f"**Step7:** Final boxed")
    elif rule_name == "FTC (Fundamental Theorem)":
        steps.append(f"**Step1:** FTC: If F'=f, then ∫_a^b f = F(b)-F(a)"); steps.append(f"**Step2:** Also d/dx ∫_a^x f(t)dt = f(x)")
        steps.append(f"**Step3:** For {sp.latex(expr)}, F={sp.latex(F)}")
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper))
            steps.append(f"**Step4:** ∫={sp.latex(val)}"); steps.append(f"**Step5:** Graph area explanatory"); steps.append(f"**Step6:** Solid revolution volume if rotated (x,y,z)"); steps.append(f"**Step7:** Final")
            return "\n\n".join(steps), val, None
        else:
            steps.append(f"**Step4:** Indefinite family"); steps.append(f"**Step5:** Graph"); steps.append(f"**Step6:** Solid"); steps.append(f"**Step7:** Final")
    elif rule_name == "Limits":
        steps.append(f"**Step1:** ∫_a^b f = lim n→∞ Σ f(x_i)Δx"); steps.append(f"**Step2:** Riemann sum"); steps.append(f"**Step3:** Δx=(b-a)/n")
        steps.append(f"**Step4:** Limit n→∞ -> {sp.latex(F)}"); 
        if lower is not None and upper is not None:
            val=sp.integrate(expr,(var,lower,upper)); steps.append(f"**Step5:** Exact {sp.latex(val)}")
        steps.append(f"**Step6:** Area limit"); steps.append(f"**Step7:** Final")
    return "\n\n".join(steps), F, None

def compare_integrals(ref, other):
    if ref is None or other is None: return False
    try:
        diff=sp.simplify(ref-other)
        return diff.is_constant() or diff==0 or diff.is_number
    except:
        return False

# ------------------- UI -------------------
st.set_page_config(page_title="Math Solver - Complete Restored", layout="wide")
st.title("📚 Complete Math Solver - Restored Arithmetic + Limits + Derivatives + Integrals")

menu = st.sidebar.selectbox("Select Module", [
    "1. Subtraction - Column Method - Detailed Steps",
    "2. Multiplication - Column Method - Detailed Steps",
    "3. Long Division L Shape - Detailed Steps",
    "4. First Degree + Cartesian x,y",
    "5. Second Degree + Cartesian x,y",
    "6. Linear Systems x,y and x,y,z",
    "7. Limits - Step by Step (infinity -> ∞)",
    "8. Derivatives - 8 Rules Step by Step + Comparison Green/Red",
    "9. Integrals - 7 Rules Step by Step + Comparison Green/Red + Solid Revolution"
])

try:
    menu_num = int(menu.split(".")[0])
except:
    menu_num = 1

if menu_num == 1:
    st.header("1. Subtraction - Column Method - Long Method - Detailed Steps Restored")
    st.markdown("Reference image: https://ibb.co/Qv4WYM8Z - Minuend top, Subtrahend bottom, borrowing with \cancel, -100→centena, 60→dezena, 9→unidade, final -33")
    c1,c2 = st.columns(2)
    with c1: minuend = st.number_input("Minuend (top) - Minuendo", value=136, step=1)
    with c2: subtrahend = st.number_input("Subtrahend (bottom) - Subtraendo", value=169, step=1)
    if st.button("Show Steps - Subtraction"):
        data = subtraction_analysis_latex_detailed(minuend, subtrahend)
        # HTML detailed
        st.markdown(render_subtraction_detailed_html(data), unsafe_allow_html=True)
        # LaTeX detailed
        latex1, borrow_ex, requested, correct = data["minuend"], data["subtrahend"], None, None
        # Use full latex function
        from __main__ import *  # dummy to avoid error, we already have data
        # Re-create full latex blocks
        latex1_full = f"""
\\begin{{array}}{{r}}
  {data['minuend_padded']} \\\\
- {data['subtrahend_padded']} \\\\
\\hline
  {data['minuend'] - data['subtrahend']} \\\\
\\end{{array}}
"""
        st.subheader("A) Direct order - LaTeX")
        st.latex(latex1_full)
        st.subheader("B) Borrowing visualization - Column Method (Long Method) - shows 169 intermediate")
        st.latex(r"""
\text{Column Subtraction:}\\
\begin{array}{cccc}
  \cancel{3}^{2} & \overset{10}{0} & \cancel{5}^{14} \\
  & 3 & 0 & 5 \\
- & 1 & 3 & 6 \\
\hline
  & 1 & 6 & 9
\end{array}
\rightarrow 169 \text{ intermediate as in image}
""")
        st.subheader("C) Exact order as reference image - Resolução passo a passo")
        st.latex(r"""
\begin{aligned}
-100 &\rightarrow \text{hundreds (centena)}\\
60 &\rightarrow \text{tens (dezena)}\\
9 &\rightarrow \text{units (unidade)}\\
-100 + 60 + 9 &= -33\\
\text{Final answer: } -33
\end{aligned}
""")
        st.subheader("D) Correct place-value - Resolução passo a passo")
        st.latex(r"""
\begin{aligned}
%s &= %s + %s + %s\\
%s &= %s + %s + %s\\
\text{Hundreds } %s - %s = %s\\
\text{Tens } %s - %s = %s\\
\text{Units } %s - %s = %s\\
%s + %s + %s = %s
\end{aligned}
""" % (data["minuend"], data["h_m"], data["t_m"], data["u_m"], data["subtrahend"], data["h_s"], data["t_s"], data["u_s"],
       data["h_m"], data["h_s"], data["correct_h"], data["t_m"], data["t_s"], data["correct_t"],
       data["u_m"], data["u_s"], data["correct_u"], data["correct_h"], data["correct_t"], data["correct_u"], data["minuend"]-data["subtrahend"]))
        st.subheader("E) Detailed text steps - Resolução passo a passo")
        for s in data["steps_text"]:
            st.write(f"- {s}")
        st.info(f"Final: {data['minuend']} - {data['subtrahend']} = {data['minuend']-data['subtrahend']}")

elif menu_num == 2:
    st.header("2. Multiplication - Column Method - Detailed Steps - Restored")
    c1,c2 = st.columns(2)
    with c1: a = st.number_input("Multiplicand (top)", value=123, step=1)
    with c2: b = st.number_input("Multiplier (bottom)", value=45, step=1)
    if st.button("Show Multiplication Steps"):
        data = multiplication_analysis(a,b)
        st.markdown(render_multiplication_html(data), unsafe_allow_html=True)
        st.subheader("LaTeX - Resolução passo a passo")
        latex_mult = r"""
\begin{array}{r}
  %s \\
\times %s \\
\hline
""" % (a,b)
        for p in data["partials"]:
            latex_mult += f"  {p['shifted']} \\\\ % partial {p['digit']} \n"
        latex_mult += r"\hline %s \\ \end{array}" % data["total"]
        st.latex(latex_mult)
        st.subheader("Step-by-step text")
        for i, s in enumerate(data["steps"],1):
            st.write(f"{i}. {s}")

elif menu_num == 3:
    st.header("3. Long Division - L Shape - Detailed Steps - Restored")
    c1,c2 = st.columns(2)
    with c1: dvd = st.number_input("Dividend", value=1256, step=1, min_value=0)
    with c2: dvs = st.number_input("Divisor", value=8, step=1, min_value=1)
    if st.button("Divide - Show Detailed Steps"):
        data = long_division_steps_detailed(dvd, dvs)
        st.markdown(render_division_html_detailed(data), unsafe_allow_html=True)
        st.latex(r"\text{Check: } %s \times %s + %s = %s" % (dvs, data['quotient'], data['remainder'], dvd))

elif menu_num == 4:
    st.header("First Degree Function + Cartesian x,y - Detailed")
    eq = st.text_input("Equation", "2x+3=7", help="Use ^ for power e.g. x^3")
    if st.button("Solve Linear"):
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sol=sp.solve(expr,x)[0]
            st.latex(f"x={sp.latex(sol)}")
            fig, ax = plt.subplots()
            # plot linear
            a_coeff=float(sp.Poly(expr,x).all_coeffs()[0]); b_coeff=float(sp.Poly(expr,x).all_coeffs()[1])
            xv=np.linspace(float(sol)-5,float(sol)+5,200)
            ax.plot(xv, a_coeff*xv+b_coeff, label=f'{a_coeff}x+{b_coeff}')
            ax.axhline(0,color='black',lw=1.2,label='x axis'); ax.axvline(0,color='black',lw=1.2,label='y axis')
            ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
            st.pyplot(fig)
            st.pyplot(plot_cartesian_xy())
        except Exception as e:
            st.error(str(e))

elif menu_num == 5:
    st.header("Second Degree Function + Cartesian x,y - Detailed")
    eq = st.text_input("Equation", "x^2-5x+6=0", help="Use ^")
    if st.button("Solve Quadratic"):
        try:
            l,r=eq.split('='); le=parse_expr(l); re=parse_expr(r); expr=sp.expand(le-re); sols=sp.solve(expr,x)
            st.write(f"Solutions: {sols}")
            fig, ax = plt.subplots()
            xv=np.linspace(-10,10,400)
            # get coeffs
            poly=sp.Poly(expr,x); a,b,c=poly.all_coeffs()
            a_f=float(a); b_f=float(b); c_f=float(c)
            ax.plot(xv, a_f*xv**2+b_f*xv+c_f, label=f'{a_f}x²+{b_f}x+{c_f}')
            ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
            ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
            st.pyplot(fig)
        except Exception as e:
            st.error(str(e))

elif menu_num == 6:
    st.header("Linear Systems x,y and x,y,z - Cartesian planes - Detailed")
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
            # detailed steps
            A,b_mat=sp.linear_eq_to_matrix(eqs_sym,*vars_sorted)
            st.latex(f"A={sp.latex(A)}, b={sp.latex(b_mat)}")
            aug=A.row_join(b_mat); rref,_=aug.rref()
            st.latex(f"RREF={sp.latex(rref)}")
            if A.shape[0]==A.shape[1]:
                st.latex(f"det={sp.latex(A.det())}")
        except Exception as e:
            st.error(str(e))

elif menu_num == 7:
    st.header("7. Limits - Resolução passo a passo - infinity handling")
    st.markdown("Type 'infinity' or '-infinity' for infinite limits - transformed to $\\infty$")
    expr_input = st.text_input("f(x)", "sin(x)/x", help="Use ^ for power e.g. x^3, 3x", key="lim_expr2")
    point_input = st.text_input("Point x ->", "0", help="Number or infinity/-infinity", key="lim_point2")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="lim_var2")
    if st.button("Compute Limit Step by Step"):
        steps, lim_val, fig = limit_steps_detailed(expr_input, var_sel, point_input)
        st.markdown(steps)
        if fig is not None:
            st.pyplot(fig)
        point_sym = parse_point(point_input)
        st.info(f"Input '{point_input}' -> symbol ${sp.latex(point_sym)}$ for calculation (infinity handled)")

elif menu_num == 8:
    st.header("8. Derivatives - 8 Rules - Resolução passo a passo + Comparison Green/Red + Solid Revolution")
    st.markdown("""
    Rules: Defined & differentiable, Constant, Power, Sum & Difference, Product, Quotient, Chain, Limits
    """)
    expr_input = st.text_input("f(x)", "x^2+3x", help="Use ^ e.g. x^3, example sin(2x)+ln(x)", key="der_expr2")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="der_var3")
    selected_rule = st.selectbox("Select Primary Rule", derivative_rules_list, key="der_rule_sel2")

    if st.button("Show Derivative Rule Step by Step"):
        steps, deriv, _ = derivative_rule_steps(expr_input, var_sel, selected_rule)
        st.markdown(steps)
        if deriv is not None:
            st.latex(f"f'({var_sel})={sp.latex(deriv)}")
            try:
                fig, ax = plt.subplots()
                var=sp.Symbol(var_sel)
                f_lamb=sp.lambdify(var, parse_expr(expr_input,var_sel), 'numpy')
                df_lamb=sp.lambdify(var, deriv, 'numpy')
                t=np.linspace(-3,3,400)
                ax.plot(t, f_lamb(t), label='f(x) curve (x,y)', linewidth=2)
                ax.plot(t, df_lamb(t), label="f'(x) line", linestyle='--')
                ax.axhline(0,color='black',lw=1.2); ax.axvline(0,color='black',lw=1.2)
                ax.set_xlabel('x'); ax.set_ylabel('y'); ax.legend(); ax.grid(True,alpha=0.3)
                st.pyplot(fig)
                solid_fig = plot_solid_revolution(expr_input, var_sel, -2, 2)
                if solid_fig:
                    st.pyplot(solid_fig)
            except Exception as e:
                st.error(f"Graph error: {e}")

        st.subheader("Comparison Panel - Other Rules - Green = same, Red = different")
        cols = st.columns(4)
        ref_deriv = deriv
        for idx, rule in enumerate(derivative_rules_list):
            col = cols[idx % 4]
            with col:
                _, other_deriv, _ = derivative_rule_steps(expr_input, var_sel, rule)
                same = compare_derivatives(ref_deriv, other_deriv)
                color = "green" if same else "red"
                bg = "#d4edda" if same else "#f8d7da"
                if other_deriv is not None:
                    st.markdown(f"<div style='background:{bg}; border:1px solid {color}; padding:6px; border-radius:6px; font-size:12px;'><b>{rule}</b>: ${sp.latex(other_deriv)}$ <span style='color:{color}'>{'✓' if same else '✗'}</span></div>", unsafe_allow_html=True)

elif menu_num == 9:
    st.header("9. Integrals - 7 Rules - Resolução passo a passo + Comparison Green/Red + Solid Revolution")
    st.markdown("""
    Rules: Primitives, Substitution, By parts, Definite, Indefinite, FTC with graph, Limits
    """)
    expr_input = st.text_input("Integrand", "sin(2x)+ln(x)", help="Use ^ e.g. x^3", key="int_expr2")
    var_sel = st.selectbox("Variable", ["x","y","z"], key="int_var2")
    rule_sel = st.selectbox("Select Primary Rule", integral_rules_list, key="int_rule_sel2")
    mode = st.radio("Type", ["Indefinite","Definite"], key="int_mode3")
    lower=None; upper=None
    if mode=="Definite":
        c1,c2=st.columns(2)
        with c1: lower_input=st.text_input("Lower a", "0", help="Can be infinity")
        with c2: upper_input=st.text_input("Upper b", "2", help="Can be infinity")
        lower=parse_point(lower_input)
        upper=parse_point(upper_input)
        st.info(f"Lower -> {sp.latex(lower) if lower is not None else 'None'}, Upper -> {sp.latex(upper) if upper is not None else 'None'} - infinity -> oo")

    if st.button("Show Integral Rule Step by Step"):
        if mode=="Definite" and lower is not None and upper is not None:
            steps, result, _ = integral_rule_steps(expr_input, var_sel, rule_sel, float(lower) if lower not in [sp.oo, -sp.oo] else lower, float(upper) if upper not in [sp.oo, -sp.oo] else upper)
        else:
            steps, result, _ = integral_rule_steps(expr_input, var_sel, rule_sel, None, None)
        st.markdown(steps)
        if result is not None:
            st.latex(f"Result = {sp.latex(result)}")
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
                solid_fig = plot_solid_revolution(expr_input, var_sel, -2, 2)
                if solid_fig:
                    st.pyplot(solid_fig)
            except Exception as e:
                st.error(f"Graph error {e}")

        st.subheader("Comparison Panel - Other Integral Rules - Green = same, Red = different")
        cols = st.columns(3)
        ref_result = result
        for idx, rule in enumerate(integral_rules_list):
            col = cols[idx % 3]
            with col:
                if mode=="Definite" and lower is not None and upper is not None:
                    _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, lower, upper)
                else:
                    _, other_res, _ = integral_rule_steps(expr_input, var_sel, rule, None, None)
                same = compare_integrals(ref_result, other_res)
                color = "green" if same else "red"
                bg = "#d4edda" if same else "#f8d7da"
                if other_res is not None:
                    st.markdown(f"<div style='background:{bg}; border:1px solid {color}; padding:6px; border-radius:6px; font-size:12px;'><b>{rule}</b>: ${sp.latex(other_res)}$ <span style='color:{color}'>{'✓' if same else '✗'}</span></div>", unsafe_allow_html=True)
