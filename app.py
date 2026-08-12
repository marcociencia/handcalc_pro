import streamlit as st
import sympy as sp
from sympy import latex, expand, solve, Eq, Matrix, limit, Limit, diff, Integral, integrate, oo
import matplotlib.pyplot as plt
import numpy as np
import math

# ------------------------------------------------------------
# SYMBOLIC HELPERS
# ------------------------------------------------------------
x, y, z = sp.symbols('x y z')
sym_vars = {'x': x, 'y': y, 'z': z}

def parse_expr(expr_str, var='x'):
    """Convert a string to a sympy expression."""
    try:
        return sp.sympify(expr_str.replace("^", "**"), locals=sym_vars)
    except:
        return None

# ------------------------------------------------------------
# 1. LONG SUBTRACTION with borrowing (armada)
# ------------------------------------------------------------
def subtraction_visual(num1, num2):
    """
    Perform manual subtraction and show borrowing steps.
    Returns a string showing the process.
    """
    if num2 > num1:
        # Force negative result: compute num2 - num1, then show negative
        abs_result = num2 - num1
        sign = "-"
        # Show subtraction as num2 - num1 and then attach negative sign
        # We'll borrow from larger (num2) minus smaller (num1)
        top = list(str(num2))
        bottom = list(str(num1))
    else:
        sign = ""
        top = list(str(num1))
        bottom = list(str(num2))

    # Pad with leading zeros if necessary
    while len(bottom) < len(top):
        bottom.insert(0, '0')
    while len(top) < len(bottom):
        top.insert(0, '0')

    result_digits = []
    borrow = False
    steps = []
    top_copy = top.copy()
    bottom_copy = bottom.copy()

    steps.append("Step-by-step subtraction:")
    steps.append(f"  {''.join(top)}   ← top number")
    steps.append(f"- {''.join(bottom)}   ← bottom number")
    steps.append("-" * (len(top) + 2))

    for i in range(len(top)-1, -1, -1):
        top_digit = int(top[i])
        bottom_digit = int(bottom[i])
        if borrow:
            top_digit -= 1
            borrow = False
        if top_digit < bottom_digit:
            # Need to borrow from the next left digit
            if i > 0 and top[i-1] != '0':
                # Simple borrow from non-zero
                top[i-1] = str(int(top[i-1]) - 1)
                steps.append(f"  Borrow from {top[i-1]} (now {int(top[i-1])+1}→{top[i-1]})")
                top_digit += 10
            else:
                # Borrow across zeros
                j = i - 1
                while j >= 0 and top[j] == '0':
                    j -= 1
                if j >= 0:
                    # Decrease that digit
                    top[j] = str(int(top[j]) - 1)
                    steps.append(f"  Borrow from position {j}: {int(top[j])+1} → {top[j]}")
                    # Set all zeros between to 9
                    for k in range(j+1, i):
                        top[k] = '9'
                    top_digit += 10
                else:
                    # Cannot borrow (should not happen in normal subtraction)
                    pass
            borrow = False  # already handled
        diff = top_digit - bottom_digit
        result_digits.insert(0, str(diff))
        steps.append(f"  Column {i}: {top_digit} - {bottom_digit} = {diff}")

    # Build final result
    result = int(''.join(result_digits))
    if sign == "-":
        result = -abs_result
    steps.append("-" * (len(top) + 2))
    steps.append(f"  {sign}{''.join(result_digits)}   ← result")
    return "\n".join(steps)

# ------------------------------------------------------------
# 2. LONG DIVISION with L-shape visual
# ------------------------------------------------------------
def long_division_visual(dividend, divisor):
    """Return a string showing the long division process in a 'L' layout."""
    if divisor == 0:
        return "Error: division by zero"
    quotient = dividend // divisor
    remainder = dividend % divisor

    # Build the layout
    lines = []
    # Top: quotient above the line
    lines.append(f"      {quotient}")
    lines.append(f"   ┌{'─' * max(len(str(divisor)), len(str(dividend))+1)}")
    lines.append(f"{divisor} │ {dividend}")
    # Subtract divisor*quotient
    product = divisor * quotient
    lines.append(f"   │ {product}")
    lines.append(f"   ├{'─' * (len(str(dividend)))}")
    lines.append(f"   │   {remainder}")
    return "\n".join(lines)

# ------------------------------------------------------------
# 3. LIMITS
# ------------------------------------------------------------
def limit_steps(expr_str, var_str, point):
    """Evaluate limit and show steps."""
    try:
        expr = parse_expr(expr_str, var_str)
        var = sp.Symbol(var_str)
        # Direct substitution first
        direct = expr.subs(var, point)
        steps = []
        steps.append(f"**Step 1:** Direct substitution $x = {point}$:")
        steps.append(f"  $f({point}) = {sp.latex(direct)}$")
        if direct.is_finite and not direct.has(sp.oo, sp.zoo, sp.nan):
            steps.append("  The limit exists and equals this value (no indeterminacy).")
            lim_val = direct
        else:
            steps.append("  Indeterminate form. Applying algebraic manipulation or L'Hôpital's rule.")
            # Try L'Hôpital if 0/0 or ∞/∞
            if direct == sp.nan:
                # Attempt limit
                lim_val = sp.limit(expr, var, point)
                steps.append(f"**Step 2:** Compute limit using sympy: ${sp.latex(lim_val)}$")
            else:
                lim_val = sp.limit(expr, var, point)
                steps.append(f"**Step 2:** Limit computed: ${sp.latex(lim_val)}$")
        steps.append(f"**Step 3:** Final limit = ${sp.latex(lim_val)}$")
        # Graph
        fig, ax = plt.subplots()
        t_vals = np.linspace(float(point)-2, float(point)+2, 400)
        f_lamb = sp.lambdify(var, expr, 'numpy')
        try:
            y_vals = f_lamb(t_vals)
            ax.plot(t_vals, y_vals)
            ax.axvline(float(point), color='red', linestyle='--', label=f'x={point}')
            if lim_val.is_real:
                ax.axhline(float(lim_val), color='green', linestyle='--', label=f'Limit = {float(lim_val):.2f}')
            ax.legend()
            ax.set_title("Limit visualization")
        except:
            pass
        return "\n\n".join(steps), lim_val, fig
    except Exception as e:
        return f"Error: {e}", None, None

# ------------------------------------------------------------
# 4. LIMIT DEFINITION OF DERIVATIVE
# ------------------------------------------------------------
def derivative_limit_steps(expr_str, var_str='x', point_val=1):
    """Show limit of difference quotient to compute derivative at a point."""
    try:
        expr = parse_expr(expr_str, var_str)
        var = sp.Symbol(var_str)
        h = sp.Symbol('h')
        # f(x+h) - f(x) / h
        diff_quot = (expr.subs(var, var+h) - expr) / h
        deriv = sp.limit(diff_quot, h, 0)
        steps = []
        steps.append(f"**Definition:** $f'({var}) = \\lim_{{h \\to 0}} \\frac{{f({var}+h) - f({var})}}{{h}}$")
        steps.append(f"**Step 1:** Write difference quotient:")
        steps.append(f"  $\\frac{{f({var}+h) - f({var})}}{{h}} = {sp.latex(diff_quot)}$")
        steps.append(f"**Step 2:** Simplify the expression if possible.")
        simplified = sp.simplify(diff_quot)
        steps.append(f"  $= {sp.latex(simplified)}$")
        steps.append(f"**Step 3:** Take the limit as $h \\to 0$:")
        steps.append(f"  $\\lim_{{h \\to 0}} {sp.latex(simplified)} = {sp.latex(deriv)}$")
        steps.append(f"**Step 4:** So $f'({var}) = {sp.latex(deriv)}$")
        # Plot at a specific point
        if point_val is not None:
            slope = deriv.subs(var, point_val)
            steps.append(f"**Step 5:** At $x={point_val}$, slope $m = {sp.latex(slope)}$")
            fig, ax = plt.subplots()
            t_vals = np.linspace(float(point_val)-2, float(point_val)+2, 200)
            f_lamb = sp.lambdify(var, expr, 'numpy')
            y_vals = f_lamb(t_vals)
            ax.plot(t_vals, y_vals, label=f'f({var_str})')
            # tangent line
            y0 = float(expr.subs(var, point_val))
            m_val = float(slope)
            tangent = m_val * (t_vals - float(point_val)) + y0
            ax.plot(t_vals, tangent, '--', label='Tangent')
            ax.scatter([float(point_val)], [y0], color='red')
            ax.legend()
            ax.set_title("Derivative as limit of secant")
            return "\n\n".join(steps), deriv, fig
        return "\n\n".join(steps), deriv, None
    except Exception as e:
        return f"Error: {e}", None, None

# ------------------------------------------------------------
# 5. LIMIT DEFINITION OF INTEGRAL (Riemann sum)
# ------------------------------------------------------------
def integral_limit_steps(expr_str, var_str='x', a=0, b=1, n=5):
    """Show Riemann sum limit leading to definite integral."""
    try:
        expr = parse_expr(expr_str, var_str)
        var = sp.Symbol(var_str)
        delta_x = (b - a) / n
        steps = []
        steps.append(f"**Definition:** $\\int_{{a}}^{{b}} f(x) dx = \\lim_{{n \\to \\infty}} \\sum_{{i=1}}^{n} f(x_i^*) \\Delta x$")
        steps.append(f"**Step 1:** Partition $[a,b]$ into $n$ subintervals, $\\Delta x = \\frac{{{b}-{a}}}{{{n}}} = {delta_x}$")
        # Right Riemann sum
        x_i = a + (i+1)*delta_x  # if using 0-indexed
        # Use sympy summation
        i = sp.Symbol('i')
        sum_expr = sp.summation(expr.subs(var, a + i*delta_x) * delta_x, (i, 1, n))
        steps.append(f"**Step 2:** Right Riemann sum $S_n = \\sum_{{i=1}}^{{n}} f(x_i) \\Delta x$:")
        steps.append(f"  $S_{n} = {sp.latex(sum_expr)}$")
        # Limit
        limit_sum = sp.limit(sp.summation(expr.subs(var, a + i*(b-a)/n) * (b-a)/n, (i, 1, n)), n, sp.oo)
        steps.append(f"**Step 3:** Take the limit $n \\to \\infty$: ${sp.latex(limit_sum)}$")
        exact = sp.integrate(expr, (var, a, b))
        steps.append(f"**Step 4:** Exact integral = ${sp.latex(exact)}$")
        # Plot rectangles
        fig, ax = plt.subplots()
        t_vals = np.linspace(a, b, 300)
        f_lamb = sp.lambdify(var, expr, 'numpy')
        y_vals = f_lamb(t_vals)
        ax.plot(t_vals, y_vals, 'b', label=f'f({var_str})')
        # draw rectangles
        for i in range(n):
            xi = a + i * delta_x
            yi = f_lamb(xi + delta_x)  # right endpoint
            ax.bar(xi+delta_x, yi, width=delta_x, align='edge', alpha=0.3, color='orange', edgecolor='black')
        ax.set_title(f"Riemann sum approximation (n={n})")
        return "\n\n".join(steps), exact, fig
    except Exception as e:
        return f"Error: {e}", None, None

# ------------------------------------------------------------
# 6. LINEAR EQUATION (fixed graph bug)
# ------------------------------------------------------------
def solve_linear_steps(eq_str):
    try:
        if '=' not in eq_str:
            return "Error: Missing '=' sign.", None, None, None
        left_str, right_str = eq_str.split('=')
        left_expr = parse_expr(left_str)
        right_expr = parse_expr(right_str)
        expr = sp.expand(left_expr - right_expr)
        poly = sp.Poly(expr, x)
        coeffs = poly.all_coeffs()
        if len(coeffs) == 2:
            a, b = coeffs
        elif len(coeffs) == 1:
            a, b = 0, coeffs[0]
        else:
            a, b = 0, 0
        if a == 0:
            return "Not a linear equation (a=0).", None, None, None
        sol = -b / a
        steps = []
        steps.append(f"**Step 1:** Original equation: ${sp.latex(left_expr)} = {sp.latex(right_expr)}$")
        steps.append(f"**Step 2:** Bring all terms to one side: ${sp.latex(expr)} = 0$")
        steps.append(f"**Step 3:** Identify coefficients: $a = {a}$, $b = {b}$")
        steps.append(f"**Step 4:** Isolate variable: ${a}x = {-b}$")
        steps.append(f"**Step 5:** Solve: $x = \\frac{{-{b}}}{{{a}}} = {sp.latex(sol)}$")
        # verification
        left_val = left_expr.subs(x, sol)
        right_val = right_expr.subs(x, sol)
        steps.append(f"**Step 6:** Verify: ${sp.latex(left_expr)} = {sp.latex(right_expr)} \\rightarrow {sp.latex(left_val)} = {sp.latex(right_val)}$ ✓")
        steps.append(f"**Step 7:** Solution: $\\boxed{{x = {sp.latex(sol)}}}$")
        return "\n\n".join(steps), sol, float(a), float(b)
    except Exception as e:
        return f"Error: {e}", None, None, None

def plot_linear(a, b, sol):
    fig, ax = plt.subplots()
    x_vals = np.linspace(float(sol)-5, float(sol)+5, 100)
    y_vals = a * x_vals + b
    ax.plot(x_vals, y_vals, label=f'f(x)={a}x+{b}')
    ax.axhline(0, color='gray')
    ax.axvline(float(sol), color='red', linestyle='--', label=f'Root x={float(sol):.2f}')
    ax.legend()
    ax.set_title("Linear Equation Graph")
    return fig

# ------------------------------------------------------------
# 7. QUADRATIC EQUATION
# ------------------------------------------------------------
def solve_quadratic_steps(eq_str):
    try:
        if '=' not in eq_str:
            return "Error: Missing '=' sign.", None, None
        left_str, right_str = eq_str.split('=')
        left_expr = parse_expr(left_str)
        right_expr = parse_expr(right_str)
        expr = sp.expand(left_expr - right_expr)
        poly = sp.Poly(expr, x)
        coeffs = poly.all_coeffs()
        if len(coeffs) == 3:
            a, b, c = coeffs
        elif len(coeffs) == 2:
            a, b, c = coeffs[0], coeffs[1], 0
        else:
            return "Not a quadratic equation.", None, None
        if a == 0:
            return "Not a quadratic (a=0).", None, None
        discriminant = b**2 - 4*a*c
        steps = []
        steps.append(f"**Step 1:** Original: ${sp.latex(left_expr)} = {sp.latex(right_expr)}$")
        steps.append(f"**Step 2:** Standard form: ${sp.latex(expr)} = 0$")
        steps.append(f"**Step 3:** $a={a},\\ b={b},\\ c={c}$")
        steps.append(f"**Step 4:** Discriminant $\\Delta = {b}^2 - 4\\cdot{a}\\cdot{c} = {discriminant}$")
        if discriminant > 0:
            sol1 = (-b + sp.sqrt(discriminant)) / (2*a)
            sol2 = (-b - sp.sqrt(discriminant)) / (2*a)
            steps.append(f"**Step 5:** Two real roots: $x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}$")
            steps.append(f"  $x_1 = {sp.latex(sp.simplify(sol1))},\\ x_2 = {sp.latex(sp.simplify(sol2))}$")
            sols = [sol1, sol2]
        elif discriminant == 0:
            sol = -b/(2*a)
            steps.append(f"**Step 5:** Double root: $x = \\frac{{-b}}{{2a}} = {sp.latex(sol)}$")
            sols = [sol]
        else:
            real = -b/(2*a)
            imag = sp.sqrt(-discriminant)/(2*a)
            sol1 = real + sp.I*imag
            sol2 = real - sp.I*imag
            steps.append(f"**Step 5:** Complex: $x = {sp.latex(sol1)},\\ {sp.latex(sol2)}$")
            sols = [sol1, sol2]
        steps.append("**Step 6:** Verification:")
        for s in sols:
            val = sp.N(expr.subs(x, s))
            steps.append(f"  $f({sp.latex(s)}) = {val}$ ≈ 0 ✓")
        steps.append(f"**Step 7:** Solutions: ${', '.join(sp.latex(s) for s in sols)}$")
        return "\n\n".join(steps), sols, (float(a), float(b), float(c))
    except Exception as e:
        return f"Error: {e}", None, None

def plot_quadratic(a, b, c, sols):
    fig, ax = plt.subplots()
    x_vals = np.linspace(-10, 10, 200)
    y_vals = a * x_vals**2 + b * x_vals + c
    ax.plot(x_vals, y_vals, label=f'f(x)={a}x²+{b}x+{c}')
    ax.axhline(0, color='gray')
    for s in sols:
        if s.is_real:
            ax.plot(float(s), 0, 'ro')
    ax.legend()
    ax.set_title("Quadratic Graph")
    return fig

# ------------------------------------------------------------
# 8. LINEAR SYSTEMS
# ------------------------------------------------------------
def solve_linear_system(eq_list):
    try:
        eqs = []
        for eq_str in eq_list:
            if '=' not in eq_str:
                return "Invalid equation", None, None
            lhs_str, rhs_str = eq_str.split('=')
            lhs = parse_expr(lhs_str)
            rhs = parse_expr(rhs_str)
            eqs.append(sp.Eq(lhs, rhs))
        vars_in = list(set().union(*[eq.free_symbols for eq in eqs]))
        vars_sorted = sorted(vars_in, key=lambda v: str(v))
        A, b = sp.linear_eq_to_matrix(eqs, *vars_sorted)
        steps = []
        steps.append("**Step 1:** System:")
        for eq in eqs:
            steps.append(f"  ${sp.latex(eq)}$")
        steps.append(f"**Step 2:** Matrix form $A\\mathbf{{x}} = \\mathbf{{b}}$:")
        steps.append(f"  $A = {sp.latex(A)},\\ \\mathbf{{b}} = {sp.latex(b)}$")
        # Augmented matrix and RREF
        aug = A.row_join(b)
        steps.append(f"**Step 3:** Augmented matrix: ${sp.latex(aug)}$")
        rref, pivots = aug.rref()
        steps.append(f"**Step 4:** Row reduce to RREF: ${sp.latex(rref)}$")
        sol = list(sp.linsolve(eqs, *vars_sorted))
        if sol:
            sol = sol[0]
            steps.append(f"**Step 5:** Solution: ${', '.join(f'{v} = {sp.latex(val)}' for v, val in zip(vars_sorted, sol))}$")
            # Verification
            steps.append("**Step 6:** Verify:")
            for eq in eqs:
                left_val = eq.lhs.subs(dict(zip(vars_sorted, sol)))
                right_val = eq.rhs.subs(dict(zip(vars_sorted, sol)))
                steps.append(f"  ${sp.latex(eq.lhs)} = {sp.latex(left_val)},\\ {sp.latex(eq.rhs)} = {sp.latex(right_val)}$ ✓")
            steps.append("**Step 7:** Done.")
            return "\n\n".join(steps), sol, vars_sorted
        else:
            return "No unique solution.", None, vars_sorted
    except Exception as e:
        return f"Error: {e}", None, None

# ------------------------------------------------------------
# 9. DERIVATIVES (with rules per term)
# ------------------------------------------------------------
def derivative_rules_steps(expr_str, var_str='x'):
    try:
        expr = parse_expr(expr_str, var_str)
        var = sp.Symbol(var_str)
        deriv = sp.diff(expr, var)
        steps = []
        steps.append(f"**Step 1:** $f({var_str}) = {sp.latex(expr)}$")
        # Break expression
        terms = expr.args if isinstance(expr, sp.Add) else [expr]
        steps.append("**Step 2:** Differentiate term by term:")
        for term in terms:
            d = sp.diff(term, var)
            rule = ""
            if term.is_constant():
                rule = "Constant Rule (c' = 0)"
            elif term.is_Pow and term.args[1].is_number:
                rule = "Power Rule"
            elif term.is_Mul:
                rule = "Product Rule (if product of two functions)"
            elif term.func == sp.sin:
                rule = "Derivative of sin: cos"
            elif term.func == sp.cos:
                rule = "Derivative of cos: -sin"
            else:
                rule = "Standard derivative"
            steps.append(f"  ${sp.latex(term)} \\rightarrow {sp.latex(d)}$   ({rule})")
        steps.append(f"**Step 3:** Sum up: $f'({var_str}) = {sp.latex(deriv)}$")
        steps.append(f"**Step 4:** Simplify: ${sp.latex(sp.simplify(deriv))}$")
        return "\n\n".join(steps), deriv
    except Exception as e:
        return f"Error: {e}", None

# ------------------------------------------------------------
# 10. INTEGRALS (indefinite/definite with FTC)
# ------------------------------------------------------------
def integral_full_steps(expr_str, var_str='x', lower=None, upper=None):
    try:
        expr = parse_expr(expr_str, var_str)
        var = sp.Symbol(var_str)
        if lower is not None and upper is not None:
            # Definite
            F = sp.integrate(expr, var)
            val = sp.integrate(expr, (var, lower, upper))
            steps = []
            steps.append(f"**Step 1:** Indefinite integral $\\int {sp.latex(expr)} d{var_str}$")
            # Show antiderivative termwise
            terms = expr.args if isinstance(expr, sp.Add) else [expr]
            antideriv_terms = []
            for term in terms:
                at = sp.integrate(term, var)
                antideriv_terms.append(at)
                if term.is_constant():
                    rule = "Constant Rule"
                elif term.is_Pow:
                    rule = "Power Rule"
                else:
                    rule = "Basic"
                steps.append(f"  $\\int {sp.latex(term)} d{var_str} = {sp.latex(at)}$  ({rule})")
            steps.append(f"**Step 2:** Antiderivative $F({var_str}) = {sp.latex(F)} + C$")
            steps.append(f"**Step 3:** FTC: $\\int_{{ {lower} }}^{{ {upper} }} = F({upper}) - F({lower})$")
            F_upper = F.subs(var, upper)
            F_lower = F.subs(var, lower)
            steps.append(f"  $F({upper}) = {sp.latex(F_upper)},\\ F({lower}) = {sp.latex(F_lower)}$")
            steps.append(f"**Step 4:** Compute: ${sp.latex(F_upper)} - ({sp.latex(F_lower)}) = {sp.latex(val)}$")
            steps.append(f"**Step 5:** Result: $\\boxed{{{sp.latex(val)}}}$")
            # Graph
            fig, ax = plt.subplots()
            t = np.linspace(float(lower)-1, float(upper)+1, 300)
            f_lamb = sp.lambdify(var, expr, 'numpy')
            y = f_lamb(t)
            ax.plot(t, y, 'b')
            # fill area
            ix = np.linspace(float(lower), float(upper), 100)
            iy = f_lamb(ix)
            ax.fill_between(ix, iy, alpha=0.3, color='orange')
            ax.set_title("Definite Integral Area")
            return "\n\n".join(steps), val, fig
        else:
            # Indefinite
            F = sp.integrate(expr, var)
            steps = []
            steps.append(f"**Step 1:** $\\int {sp.latex(expr)} d{var_str}$")
            terms = expr.args if isinstance(expr, sp.Add) else [expr]
            for term in terms:
                at = sp.integrate(term, var)
                rule = "Power" if term.is_Pow else "Basic"
                steps.append(f"  $\\int {sp.latex(term)} d{var_str} = {sp.latex(at)}$  ({rule})")
            steps.append(f"**Step 2:** Antiderivative $F({var_str}) = {sp.latex(F)} + C$")
            # Check by differentiation
            steps.append(f"**Step 3:** Check: $\\frac{{d}}{{d{var_str}}}{sp.latex(F)} = {sp.latex(sp.diff(F, var))}$ ✓")
            steps.append(f"**Step 4:** Final: $\\boxed{{\\int {sp.latex(expr)} d{var_str} = {sp.latex(F)} + C}}$")
            return "\n\n".join(steps), F, None
    except Exception as e:
        return f"Error: {e}", None, None

# ------------------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------------------
st.set_page_config(page_title="Advanced Math Solver", layout="wide")
st.title("📚 Advanced Math Solver – Step‑by‑Step with Graphs")
st.markdown("Choose a tool from the sidebar.")

menu = st.sidebar.radio("Select Module",
    ["1. Subtraction (borrowing)",
     "2. Long Division (visual L)",
     "3. Limits",
     "4. Limit Definition of Derivative",
     "5. Limit Definition of Integral (Riemann)",
     "6. Linear Equation (1st degree)",
     "7. Quadratic Equation (2nd degree)",
     "8. Linear Systems (2x2 / 3x3)",
     "9. Derivatives (with rules)",
     "10. Integrals (FTC & area)"
    ])

if menu.startswith("1"):
    st.header("Subtraction with Borrowing (Armada)")
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Top number", value=136, step=1)
    with col2:
        num2 = st.number_input("Bottom number", value=169, step=1)
    if st.button("Subtract"):
        result_text = subtraction_visual(num1, num2)
        st.code(result_text, language="text")

elif menu.startswith("2"):
    st.header("Long Division – Visual L Layout")
    col1, col2 = st.columns(2)
    with col1:
        dividend = st.number_input("Dividend", value=1256, step=1)
    with col2:
        divisor = st.number_input("Divisor", value=8, step=1)
    if st.button("Divide"):
        vis = long_division_visual(dividend, divisor)
        st.code(vis, language="text")

elif menu.startswith("3"):
    st.header("Limits of Functions")
    expr_str = st.text_input("Function f(x)", "sin(x)/x")
    point = st.number_input("x approaches", value=0.0)
    if st.button("Compute Limit"):
        steps, lim_val, fig = limit_steps(expr_str, "x", point)
        st.markdown(steps)
        if fig:
            st.pyplot(fig)

elif menu.startswith("4"):
    st.header("Derivative via Limit Definition")
    expr_str = st.text_input("f(x)", "x**2")
    point_val = st.number_input("At point x =", value=1.0)
    if st.button("Compute"):
        steps, deriv, fig = derivative_limit_steps(expr_str, 'x', point_val)
        st.markdown(steps)
        if fig:
            st.pyplot(fig)

elif menu.startswith("5"):
    st.header("Integral via Limit of Riemann Sums")
    expr_str = st.text_input("f(x)", "x**2")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Lower bound a", value=0.0)
    with col2:
        b = st.number_input("Upper bound b", value=2.0)
    n = st.slider("Number of rectangles n", 1, 20, 5)
    if st.button("Compute"):
        steps, exact, fig = integral_limit_steps(expr_str, 'x', a, b, n)
        st.markdown(steps)
        if fig:
            st.pyplot(fig)

elif menu.startswith("6"):
    st.header("Linear Equation (1st degree)")
    eq_input = st.text_input("Equation", "2*x + 3 = 7")
    if st.button("Solve"):
        steps, sol, a, b = solve_linear_steps(eq_input)
        st.markdown(steps)
        if sol is not None and a is not None:
            fig = plot_linear(a, b, sol)
            st.pyplot(fig)

elif menu.startswith("7"):
    st.header("Quadratic Equation (2nd degree)")
    eq_input = st.text_input("Equation", "x**2 - 5*x + 6 = 0")
    if st.button("Solve"):
        steps, sols, coeffs = solve_quadratic_steps(eq_input)
        st.markdown(steps)
        if sols and coeffs:
            fig = plot_quadratic(*coeffs, sols)
            st.pyplot(fig)

elif menu.startswith("8"):
    st.header("Linear System Solver")
    size = st.radio("Size", ["2x2", "3x3"])
    if size == "2x2":
        eq1 = st.text_input("Eq1", "2*x + 3*y = 5")
        eq2 = st.text_input("Eq2", "x - y = 1")
        eqs = [eq1, eq2]
    else:
        eq1 = st.text_input("Eq1", "x + y + z = 6")
        eq2 = st.text_input("Eq2", "x - y + 2*z = 5")
        eq3 = st.text_input("Eq3", "2*x + y - z = 1")
        eqs = [eq1, eq2, eq3]
    if st.button("Solve"):
        steps, sol, vars_ = solve_linear_system(eqs)
        st.markdown(steps)

elif menu.startswith("9"):
    st.header("Derivative Rules (step by step)")
    expr_str = st.text_input("f(x)", "x**3 + 2*x**2 + sin(x)")
    var_str = st.selectbox("Variable", ["x", "y", "z"])
    if st.button("Differentiate"):
        steps, deriv = derivative_rules_steps(expr_str, var_str)
        st.markdown(steps)
        if deriv:
            st.latex(f"f'({var_str}) = {sp.latex(deriv)}")

elif menu.startswith("10"):
    st.header("Integrals (Indefinite / Definite)")
    expr_str = st.text_input("Integrand", "x**2 + 3*x + 2")
    var_str = st.selectbox("Variable", ["x", "y", "z"])
    mode = st.radio("Type", ["Indefinite", "Definite"])
    if mode == "Definite":
        lower = st.number_input("Lower limit", value=0.0)
        upper = st.number_input("Upper limit", value=2.0)
        if st.button("Integrate"):
            steps, val, fig = integral_full_steps(expr_str, var_str, lower, upper)
            st.markdown(steps)
            if fig:
                st.pyplot(fig)
    else:
        if st.button("Integrate"):
            steps, F, _ = integral_full_steps(expr_str, var_str)
            st.markdown(steps)
