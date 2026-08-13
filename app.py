import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(page_title="Advanced Math Solver", layout="wide")

# ------------------------------------------------------------
# SYMBOLIC HELPERS
# ------------------------------------------------------------
x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z}

def parse_expr(expr_str):
    """Convert a string to a sympy expression."""
    try:
        # Standardize input for sympy
        expr_str = expr_str.replace("^", "**").replace("e", "E")
        return sp.sympify(expr_str, locals=sym_vars)
    except Exception as e:
        return None

# ------------------------------------------------------------
# 1. LONG SUBTRACTION (Borrowing & Decomposition)
# ------------------------------------------------------------
def subtraction_visual(num1, num2):
    steps = []
    steps.append(f"### Subtraction: {num1} - {num2}")
    
    # 1. Traditional Borrowing (Conta Armada)
    steps.append("#### 1. Traditional Borrowing Method")
    top = list(str(max(num1, num2)))
    bottom = list(str(min(num1, num2)))
    
    while len(bottom) < len(top):
        bottom.insert(0, '0')
        
    borrow_steps = []
    borrow = False
    result_digits = []
    
    for i in range(len(top)-1, -1, -1):
        t_digit = int(top[i])
        b_digit = int(bottom[i])
        
        if borrow:
            t_digit -= 1
            borrow = False
            
        if t_digit < b_digit:
            t_digit += 10
            borrow = True
            borrow_steps.append(f"Column {len(top)-i}: Borrowed 10, {t_digit} - {b_digit} = {t_digit - b_digit}")
        else:
            borrow_steps.append(f"Column {len(top)-i}: {t_digit} - {b_digit} = {t_digit - b_digit}")
            
        result_digits.insert(0, str(t_digit - b_digit))
        
    final_res = int("".join(result_digits))
    if num1 < num2:
        final_res = -final_res
        
    steps.append("```text\n  " + "".join(top) + "\n- " + "".join(bottom) + "\n  " + "-"*len(top) + "\n  " + "".join(result_digits) + "\n```")
    steps.extend([f"- {s}" for s in borrow_steps])
    if num1 < num2:
        steps.append(f"**Since {num1} < {num2}, the final answer is negative: {final_res}**")

    # 2. Decomposition Method (As requested in the image format)
    steps.append("#### 2. Place Value Decomposition Method")
    diff = num1 - num2
    
    # Calculate hundreds, tens, units of the difference
    h = (diff // 100) * 100 if diff > 0 else (abs(diff) // 100) * -100
    rem = diff - h
    t = (rem // 10) * 10 if rem > 0 else (abs(rem) // 10) * -10
    u = rem - t
    
    steps.append(f"Decomposing the difference ({diff}) into place values:")
    steps.append(f"- {h} → hundreds (centena)")
    steps.append(f"- {t} → tens (dezena)")
    steps.append(f"- {u} → units (unidade)")
    
    # Format the addition strictly as requested
    sign_t = f"+ {t}" if t >= 0 else f"- {abs(t)}"
    sign_u = f"+ {u}" if u >= 0 else f"- {abs(u)}"
    steps.append(f"- {h} {sign_t} {sign_u} = {diff}")
    steps.append(f"**Final Answer: {diff}**")
    
    return "\n".join(steps)

# ------------------------------------------------------------
# 2. LONG DIVISION (Brazilian "L" / Chave format)
# ------------------------------------------------------------
def long_division_visual(dividend, divisor):
    if divisor == 0:
        return "Error: Division by zero."
    
    dividend_str = str(dividend)
    q_str = ""
    steps_log = []
    
    current_val = ""
    visual_text = f"{dividend} |_ {divisor}\n"
    
    for idx, digit in enumerate(dividend_str):
        current_val += digit
        val = int(current_val)
        
        if val >= divisor:
            q = val // divisor
            r = val % divisor
            q_str += str(q)
            
            sub_str = f"-{q * divisor}"
            padding = " " * (idx + 1 - len(sub_str))
            visual_text += f"{padding}{sub_str}   {q_str if idx == len(dividend_str)-1 else ''}\n"
            visual_text += f"{padding}---\n"
            
            current_val = str(r)
            next_padding = " " * (idx + 1 - len(current_val))
            visual_text += f"{next_padding}{current_val}\n"
        else:
            if q_str != "":
                q_str += "0"
                
    visual_text = visual_text.replace(f"   {q_str if idx == len(dividend_str)-1 else ''}", "")
    # Add quotient to the correct spot (under divisor)
    header, rest = visual_text.split("\n", 1)
    
    output = "```text\n"
    output += f"{dividend} |_ {divisor}\n"
    first_rest_line, remaining_lines = rest.split("\n", 1)
    output += f"{first_rest_line.ljust(len(str(dividend)))}  {q_str}\n"
    output += remaining_lines
    output += "```\n"
    
    output += f"**Step-by-step breakdown:**\n"
    output += f"- Dividend: {dividend}\n"
    output += f"- Divisor: {divisor}\n"
    output += f"- Quotient: {q_str}\n"
    output += f"- Remainder: {current_val}\n"
    
    return output

# ------------------------------------------------------------
# 3. 1st DEGREE FUNCTION (Linear)
# ------------------------------------------------------------
def linear_function_steps(eq_str):
    expr = parse_expr(eq_str)
    if expr is None: return "Invalid expression.", None
    
    steps = []
    poly = sp.Poly(expr, x)
    coeffs = poly.all_coeffs()
    
    if len(coeffs) != 2:
        return "Not a valid 1st degree function (must be in form ax + b).", None
        
    a, b = coeffs
    root = sp.solve(expr, x)
    
    steps.append(f"**Step 1: Identify the function.**")
    steps.append(f"  $f(x) = {sp.latex(expr)}$")
    steps.append(f"**Step 2: Set $f(x) = 0$ to find the root (x-intercept).**")
    steps.append(f"  ${sp.latex(expr)} = 0$")
    steps.append(f"**Step 3: Isolate the variable term.**")
    steps.append(f"  ${a}x = {-b}$")
    steps.append(f"**Step 4: Solve for $x$.**")
    steps.append(f"  $x = \\frac{{{-b}}}{{{a}}}$")
    steps.append(f"**Step 5: Calculate the final root value.**")
    steps.append(f"  $x = {root[0]}$")
    steps.append(f"**Step 6: Find the y-intercept (set $x = 0$).**")
    steps.append(f"  $f(0) = {a}(0) + ({b}) = {b}$")
    steps.append(f"**Step 7: Summary of key points.**")
    steps.append(f"  Root: $({root[0]}, 0)$ | Y-intercept: $(0, {b})$")
    
    # Plotting
    fig = go.Figure()
    x_vals = np.linspace(float(root[0])-10, float(root[0])+10, 100)
    y_vals = float(a) * x_vals + float(b)
    
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f(x) = {eq_str}"))
    fig.add_trace(go.Scatter(x=[float(root[0])], y=[0], mode='markers', marker=dict(color='red', size=10), name="Root"))
    fig.update_layout(title="Linear Function Graph", xaxis_title="X", yaxis_title="f(x)")
    
    return "\n\n".join(steps), fig

# ------------------------------------------------------------
# 4. 2nd DEGREE FUNCTION (Quadratic)
# ------------------------------------------------------------
def quadratic_function_steps(eq_str):
    expr = parse_expr(eq_str)
    if expr is None: return "Invalid expression.", None
    
    steps = []
    poly = sp.Poly(expr, x)
    coeffs = poly.all_coeffs()
    
    if len(coeffs) != 3:
        return "Not a valid 2nd degree function (must be ax^2 + bx + c).", None
        
    a, b, c = coeffs
    
    steps.append(f"**Step 1: Identify the standard quadratic form $ax^2 + bx + c$.**")
    steps.append(f"  $f(x) = {sp.latex(expr)}$")
    steps.append(f"**Step 2: Extract coefficients.**")
    steps.append(f"  $a = {a}, \\quad b = {b}, \\quad c = {c}$")
    
    delta = b**2 - 4*a*c
    steps.append(f"**Step 3: Calculate the Discriminant ($\\Delta$).**")
    steps.append(f"  $\\Delta = b^2 - 4ac = ({b})^2 - 4({a})({c})$")
    steps.append(f"  $\\Delta = {delta}$")
    
    roots = sp.solve(expr, x)
    steps.append(f"**Step 4: Use Bhaskara's (Quadratic) Formula to find roots.**")
    steps.append(f"  $x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$")
    
    if delta > 0:
        steps.append(f"  Two real roots exist since $\\Delta > 0$.")
        steps.append(f"  $x_1 = {sp.latex(roots[0])}, \\quad x_2 = {sp.latex(roots[1])}$")
    elif delta == 0:
        steps.append(f"  One real double root exists since $\\Delta = 0$.")
        steps.append(f"  $x = {sp.latex(roots[0])}$")
    else:
        steps.append(f"  Two complex roots exist since $\\Delta < 0$.")
        steps.append(f"  $x_1 = {sp.latex(roots[0])}, \\quad x_2 = {sp.latex(roots[1])}$")
        
    vx = -b / (2*a)
    vy = -delta / (4*a)
    steps.append(f"**Step 5: Find the Vertex (min/max point).**")
    steps.append(f"  $X_v = \\frac{{-b}}{{2a}} = {vx}$")
    steps.append(f"  $Y_v = \\frac{{-\\Delta}}{{4a}} = {vy}$")
    
    steps.append(f"**Step 6: Find the y-intercept (set $x = 0$).**")
    steps.append(f"  $f(0) = c = {c}$")
    
    steps.append(f"**Step 7: Determine concavity.**")
    concavity = "Upwards" if a > 0 else "Downwards"
    steps.append(f"  Since $a = {a}$ (which is {'positive' if a > 0 else 'negative'}), the parabola opens **{concavity}**.")

    # Plotting
    fig = go.Figure()
    x_vals = np.linspace(float(vx)-10, float(vx)+10, 200)
    y_vals = float(a)*x_vals**2 + float(b)*x_vals + float(c)
    
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f(x)={eq_str}"))
    fig.add_trace(go.Scatter(x=[float(vx)], y=[float(vy)], mode='markers', marker=dict(color='orange', size=10), name="Vertex"))
    
    for r in roots:
        if r.is_real:
            fig.add_trace(go.Scatter(x=[float(r)], y=[0], mode='markers', marker=dict(color='red', size=10), name="Root"))
            
    fig.update_layout(title="Quadratic Function Graph", xaxis_title="X", yaxis_title="f(x)")
    return "\n\n".join(steps), fig

# ------------------------------------------------------------
# 5. LINEAR SYSTEMS
# ------------------------------------------------------------
def solve_linear_system(eq_texts):
    steps = []
    eqs = []
    for eq_str in eq_texts:
        if '=' not in eq_str: return "Invalid equations.", None
        lhs, rhs = eq_str.split('=')
        eqs.append(sp.Eq(parse_expr(lhs), parse_expr(rhs)))
        
    system_vars = list(set().union(*[eq.free_symbols for eq in eqs]))
    system_vars = sorted(system_vars, key=lambda v: str(v))
    
    steps.append(f"**Step 1: Write down the system of equations.**")
    for eq in eqs:
        steps.append(f"  ${sp.latex(eq)}$")
        
    A, b = sp.linear_eq_to_matrix(eqs, *system_vars)
    
    steps.append(f"**Step 2: Convert to matrix form $AX = B$.**")
    steps.append(f"  $A = {sp.latex(A)}$")
    steps.append(f"  $X = {sp.latex(sp.Matrix(system_vars))}$")
    steps.append(f"  $B = {sp.latex(b)}$")
    
    aug_matrix = A.row_join(b)
    steps.append(f"**Step 3: Create the Augmented Matrix $[A|B]$.**")
    steps.append(f"  $[A|B] = {sp.latex(aug_matrix)}$")
    
    steps.append(f"**Step 4: Perform Gaussian Elimination (Row Reduction).**")
    rref_matrix, pivots = aug_matrix.rref()
    steps.append(f"  Reduced Row Echelon Form (RREF) = {sp.latex(rref_matrix)}")
    
    sol = sp.solve(eqs, system_vars)
    steps.append(f"**Step 5: Extract solutions from the RREF matrix.**")
    if not sol:
        steps.append("  The system has no unique solution (Inconsistent or Infinite solutions).")
    else:
        for var in system_vars:
            steps.append(f"  ${var} = {sol.get(var, 'Free variable')}$")
            
    steps.append(f"**Step 6: Final Solution Set.**")
    if sol:
        sol_set = ", ".join([f"{v} = {sol[v]}" for v in system_vars if v in sol])
        steps.append(f"  $S = \\{{{sol_set}\\}}$")
        
    return "\n\n".join(steps)

# ------------------------------------------------------------
# 6. LIMITS (And rules for derivative/integral)
# ------------------------------------------------------------
def calculate_limit(expr_str, var_str, point_str):
    expr = parse_expr(expr_str)
    var = sp.Symbol(var_str)
    point = sp.sympify(point_str)
    
    steps = []
    steps.append(f"**Step 1: Define the limit operation.**")
    steps.append(f"  $\\lim_{{{var} \\to {point}}} ({sp.latex(expr)})$")
    
    direct_sub = expr.subs(var, point)
    steps.append(f"**Step 2: Attempt Direct Substitution.**")
    steps.append(f"  $f({point}) = {sp.latex(direct_sub)}$")
    
    limit_val = sp.limit(expr, var, point)
    
    if direct_sub.has(sp.nan, sp.oo, -sp.oo) or direct_sub == sp.nan:
        steps.append(f"**Step 3: Indeterminate form encountered (e.g., 0/0 or $\\infty/\\infty$). Apply L'Hôpital's Rule or algebraic simplification.**")
        steps.append(f"  Evaluating the exact limit mathematically...")
    else:
        steps.append(f"**Step 3: Direct substitution yielded a valid real number.**")
        
    steps.append(f"**Step 4: Final Limit Result.**")
    steps.append(f"  $\\lim_{{{var} \\to {point}}} ({sp.latex(expr)}) = {sp.latex(limit_val)}$")
    
    # 2D Graph near the limit point
    fig = go.Figure()
    if point.is_real:
        p_val = float(point)
        x_vals = np.linspace(p_val - 5, p_val + 5, 200)
        # Avoid dividing by zero visually
        x_vals = x_vals[np.abs(x_vals - p_val) > 0.01] 
        f_lamb = sp.lambdify(var, expr, 'numpy')
        y_vals = f_lamb(x_vals)
        
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f({var})"))
        fig.add_vline(x=p_val, line=dict(color='red', dash='dash'), name="Approach Point")
        if limit_val.is_real:
            fig.add_hline(y=float(limit_val), line=dict(color='green', dash='dot'), name="Limit Value")
        fig.update_layout(title="Limit Visualization", xaxis_title=var_str, yaxis_title="Function Value")
        
    return "\n\n".join(steps), fig

# ------------------------------------------------------------
# 7. DERIVATIVES & RULES (Including 3D Solid of Revolution)
# ------------------------------------------------------------
def calculate_derivative(expr_str, var_str, rule):
    expr = parse_expr(expr_str)
    var = sp.Symbol(var_str)
    
    steps = []
    steps.append(f"**Step 1: Identify the function and the variable of differentiation.**")
    steps.append(f"  $f({var}) = {sp.latex(expr)}$")
    steps.append(f"**Step 2: Selected Rule: {rule}**")
    
    if rule == "Definition of Limit":
        h = sp.Symbol('h')
        diff_quot = (expr.subs(var, var+h) - expr) / h
        steps.append(f"**Step 3: Setup the limit definition.**")
        steps.append(f"  $f'({var}) = \\lim_{{h \\to 0}} \\frac{{f({var}+h) - f({var})}}{{h}}$")
        steps.append(f"**Step 4: Substitute the function into the formula.**")
        steps.append(f"  $= \\lim_{{h \\to 0}} \\frac{{{sp.latex(expr.subs(var, var+h))} - ({sp.latex(expr)})}}{{h}}$")
        steps.append(f"**Step 5: Simplify the numerator.**")
        steps.append(f"  $= \\lim_{{h \\to 0}} {sp.latex(sp.simplify(diff_quot))}$")
        steps.append(f"**Step 6: Evaluate the limit as $h \\to 0$.**")
    else:
        steps.append(f"**Step 3: Apply the analytic derivative operator.**")
        steps.append(f"  $\\frac{{d}}{{d{var}}} [{sp.latex(expr)}]$")
        steps.append(f"**Step 4: Break down according to the {rule}.**")
        steps.append(f"  Applying standard differentiation techniques...")
        steps.append(f"**Step 5: Differentiate each component.**")
        
    deriv = sp.diff(expr, var)
    steps.append(f"**Step 6: Simplify the resulting expression.**")
    steps.append(f"**Step 7: Final Derivative Result.**")
    steps.append(f"  $f'({var}) = {sp.latex(deriv)}$")
    
    # 2D Curve Graph
    fig2d = go.Figure()
    x_vals = np.linspace(-5, 5, 200)
    f_lamb = sp.lambdify(var, expr, 'numpy')
    d_lamb = sp.lambdify(var, deriv, 'numpy')
    
    try:
        y_vals = f_lamb(x_vals)
        dy_vals = d_lamb(x_vals)
        fig2d.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f({var})"))
        fig2d.add_trace(go.Scatter(x=x_vals, y=dy_vals, mode='lines', name=f"f'({var})", line=dict(dash='dash')))
        fig2d.update_layout(title="Function and its Derivative", xaxis_title=var_str, yaxis_title="Value")
    except:
        pass
        
    # 3D Solid of Revolution Graph (Rotating f(x) around X-axis)
    fig3d = go.Figure()
    try:
        u = np.linspace(0.1, 5, 50) # Avoid 0 for some functions
        v = np.linspace(0, 2*np.pi, 50)
        U, V = np.meshgrid(u, v)
        
        # X = u, Y = f(u)cos(v), Z = f(u)sin(v)
        Y = f_lamb(U) * np.cos(V)
        Z = f_lamb(U) * np.sin(V)
        
        fig3d.add_trace(go.Surface(x=U, y=Y, z=Z, colorscale='Viridis', opacity=0.8))
        fig3d.update_layout(title=f"Solid of Revolution (Rotating f({var}) around {var}-axis)",
                            scene=dict(xaxis_title=var_str, yaxis_title="Y", zaxis_title="Z"))
    except:
        pass

    return "\n\n".join(steps), fig2d, fig3d

# ------------------------------------------------------------
# 8. INTEGRALS & RULES (Fundamental Theorem & Solid)
# ------------------------------------------------------------
def calculate_integral(expr_str, var_str, a_str, b_str, rule):
    expr = parse_expr(expr_str)
    var = sp.Symbol(var_str)
    
    is_definite = bool(a_str and b_str)
    
    steps = []
    steps.append(f"**Step 1: Identify the integral type and function.**")
    if is_definite:
        a = sp.sympify(a_str)
        b = sp.sympify(b_str)
        steps.append(f"  Definite Integral: $\\int_{{{a}}}^{{{b}}} {sp.latex(expr)} \\, d{var}$")
    else:
        steps.append(f"  Indefinite Integral: $\\int {sp.latex(expr)} \\, d{var}$")
        
    steps.append(f"**Step 2: Selected Rule: {rule}**")
    
    if rule == "Riemann Sum Limit":
        steps.append(f"**Step 3: Set up the definition of the integral via limits.**")
        steps.append(f"  $\\lim_{{n \\to \\infty}} \\sum_{{i=1}}^{{n}} f(x_i^*) \\Delta x$")
        steps.append(f"**Step 4: Express $\\Delta x$ and $x_i$.**")
        steps.append(f"**Step 5: Evaluate the infinite sum.**")
    elif rule == "Fundamental Theorem of Calculus":
        steps.append(f"**Step 3: State the Fundamental Theorem.**")
        steps.append(f"  $\\int_{{a}}^{{b}} f(x) dx = F(b) - F(a)$ where $F'(x) = f(x)$")
        steps.append(f"**Step 4: Find the antiderivative $F({var})$.**")
    else:
        steps.append(f"**Step 3: Apply the chosen integration technique ({rule}).**")
        steps.append(f"**Step 4: Integrate step-by-step.**")
        
    antideriv = sp.integrate(expr, var)
    steps.append(f"**Step 5: The Antiderivative (Primitive) is:**")
    steps.append(f"  $F({var}) = {sp.latex(antideriv)}$")
    
    if is_definite:
        final_val = sp.integrate(expr, (var, a, b))
        steps.append(f"**Step 6: Evaluate at the boundaries.**")
        steps.append(f"  $F({b}) - F({a}) = ({sp.latex(antideriv.subs(var, b))}) - ({sp.latex(antideriv.subs(var, a))})$")
        steps.append(f"**Step 7: Final Definite Area Result.**")
        steps.append(f"  Area = ${sp.latex(final_val)}$")
    else:
        final_val = antideriv
        steps.append(f"**Step 6: Add the constant of integration.**")
        steps.append(f"**Step 7: Final Indefinite Integral.**")
        steps.append(f"  $\\int {sp.latex(expr)} \\, d{var} = {sp.latex(final_val)} + C$")

    # 2D Area Graph
    fig2d = go.Figure()
    x_vals = np.linspace(-5 if not is_definite else float(a)-2, 5 if not is_definite else float(b)+2, 200)
    f_lamb = sp.lambdify(var, expr, 'numpy')
    
    try:
        y_vals = f_lamb(x_vals)
        fig2d.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f({var})"))
        if is_definite:
            # Fill area
            x_fill = np.linspace(float(a), float(b), 100)
            y_fill = f_lamb(x_fill)
            fig2d.add_trace(go.Scatter(x=np.concatenate([x_fill, x_fill[::-1]]), 
                                       y=np.concatenate([y_fill, np.zeros_like(y_fill)]), 
                                       fill='toself', fillcolor='rgba(0,100,80,0.4)', 
                                       line=dict(color='rgba(255,255,255,0)'), name="Area"))
        fig2d.update_layout(title="Area Under Curve (FTC Visualization)", xaxis_title=var_str, yaxis_title="Value")
    except:
        pass

    # 3D Solid of Revolution
    fig3d = go.Figure()
    try:
        val_a = float(a) if is_definite else 0.1
        val_b = float(b) if is_definite else 5.0
        u = np.linspace(val_a, val_b, 50)
        v = np.linspace(0, 2*np.pi, 50)
        U, V = np.meshgrid(u, v)
        Y = f_lamb(U) * np.cos(V)
        Z = f_lamb(U) * np.sin(V)
        
        fig3d.add_trace(go.Surface(x=U, y=Y, z=Z, colorscale='Plasma', opacity=0.8))
        fig3d.update_layout(title=f"Solid of Revolution for Integral",
                            scene=dict(xaxis_title=var_str, yaxis_title="Y", zaxis_title="Z"))
    except:
        pass

    return "\n\n".join(steps), fig2d, fig3d

# ------------------------------------------------------------
# STREAMLIT UI LAYOUT
# ------------------------------------------------------------
st.sidebar.title("Advanced Math Menu")
section = st.sidebar.radio("Choose a Topic:", [
    "1. Subtraction (Borrow/Decomp)",
    "2. Long Division (L-Shape)",
    "3. 1st Degree Function",
    "4. 2nd Degree Function",
    "5. Linear Systems",
    "6. Limits",
    "7. Derivatives & Rules",
    "8. Integrals & Rules"
])

if section == "1. Subtraction (Borrow/Decomp)":
    st.title("Subtraction: Traditional & Decomposition Method")
    col1, col2 = st.columns(2)
    with col1: num1 = st.number_input("Top Number (Minuend)", value=136, step=1)
    with col2: num2 = st.number_input("Bottom Number (Subtrahend)", value=169, step=1)
    
    if st.button("Calculate Subtraction"):
        res = subtraction_visual(num1, num2)
        st.markdown(res)

elif section == "2. Long Division (L-Shape)":
    st.title("Long Division (Brazilian L-Shape / Chave)")
    col1, col2 = st.columns(2)
    with col1: dividend = st.number_input("Dividend", value=125, step=1)
    with col2: divisor = st.number_input("Divisor", value=5, step=1)
    
    if st.button("Calculate Division"):
        res = long_division_visual(dividend, divisor)
        st.markdown(res)

elif section == "3. 1st Degree Function":
    st.title("1st Degree (Linear) Function Resolution")
    eq_in = st.text_input("Enter function f(x) [e.g., 2*x - 4]", value="2*x - 4")
    if st.button("Solve & Plot"):
        steps, fig = linear_function_steps(eq_in)
        st.markdown(steps)
        if fig: st.plotly_chart(fig, use_container_width=True)

elif section == "4. 2nd Degree Function":
    st.title("2nd Degree (Quadratic) Function Resolution")
    eq_in = st.text_input("Enter function f(x) [e.g., x^2 - 5*x + 6]", value="x^2 - 5*x + 6")
    if st.button("Solve & Plot"):
        steps, fig = quadratic_function_steps(eq_in)
        st.markdown(steps)
        if fig: st.plotly_chart(fig, use_container_width=True)

elif section == "5. Linear Systems":
    st.title("Linear Systems (Equations & Matrices)")
    sys_type = st.radio("System Dimension:", ["2x2 (x, y)", "3x3 (x, y, z)"])
    if sys_type == "2x2 (x, y)":
        eq1 = st.text_input("Equation 1", value="2*x + y = 5")
        eq2 = st.text_input("Equation 2", value="x - y = 1")
        eqs = [eq1, eq2]
    else:
        eq1 = st.text_input("Equation 1", value="x + y + z = 6")
        eq2 = st.text_input("Equation 2", value="2*x - y + z = 3")
        eq3 = st.text_input("Equation 3", value="x + 2*y - z = 2")
        eqs = [eq1, eq2, eq3]
        
    if st.button("Solve System"):
        res = solve_linear_system(eqs)
        st.markdown(res)

elif section == "6. Limits":
    st.title("Limits Calculation")
    eq_in = st.text_input("Function Expression", value="sin(x)/x")
    var_in = st.text_input("Variable", value="x")
    pt_in = st.text_input("Approach Point", value="0")
    
    if st.button("Calculate Limit"):
        steps, fig = calculate_limit(eq_in, var_in, pt_in)
        st.markdown(steps)
        if fig: st.plotly_chart(fig, use_container_width=True)

elif section == "7. Derivatives & Rules":
    st.title("Derivatives, Rules & Solid of Revolution")
    eq_in = st.text_input("Function Expression [e.g., x^3 + 2*x, sin(y)*y, z^2]", value="x^2 + 3*x")
    var_in = st.selectbox("Differentiate with respect to:", ["x", "y", "z"])
    rule = st.selectbox("Apply Rule:", [
        "Power Rule", "Constant Rule", "Sum and Difference Rule", 
        "Product Rule", "Quotient Rule", "Chain Rule", 
        "Definition of Limit", "Defined/Differentiable in Interval"
    ])
    
    if st.button("Calculate Derivative"):
        steps, fig2d, fig3d = calculate_derivative(eq_in, var_in, rule)
        st.markdown(steps)
        st.plotly_chart(fig2d, use_container_width=True)
        st.plotly_chart(fig3d, use_container_width=True)

elif section == "8. Integrals & Rules":
    st.title("Integrals, Rules & Solid of Revolution")
    eq_in = st.text_input("Function Expression", value="x^2")
    var_in = st.selectbox("Integrate with respect to:", ["x", "y", "z"])
    rule = st.selectbox("Apply Rule:", [
        "Antiderivatives (Primitives)", "Substitution", "By Parts", 
        "Fundamental Theorem of Calculus", "Riemann Sum Limit"
    ])
    
    st.write("Limits of Integration (Leave blank for Indefinite Integral):")
    col1, col2 = st.columns(2)
    with col1: a_in = st.text_input("Lower Bound (a)", value="0")
    with col2: b_in = st.text_input("Upper Bound (b)", value="3")
    
    if st.button("Calculate Integral"):
        steps, fig2d, fig3d = calculate_integral(eq_in, var_in, a_in, b_in, rule)
        st.markdown(steps)
        st.plotly_chart(fig2d, use_container_width=True)
        st.plotly_chart(fig3d, use_container_width=True)
