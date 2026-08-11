
import streamlit as st
import sympy as sp
import numpy as np
from sympy import symbols, sympify, Eq, solve, sqrt, diff, integrate, latex, Poly, factor, expand
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import re

st.set_page_config(
    page_title="Advanced Step-by-Step Math Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Transformations for parsing like 2x, 2^3 etc
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

x, y, z, t = sp.symbols('x y z t')
SYMBOL_MAP = {'x': x, 'y': y, 'z': z, 't': t}

def safe_parse(expr_str: str, var=x):
    try:
        expr_str = expr_str.replace('^', '**')
        return parse_expr(expr_str, transformations=transformations, local_dict=SYMBOL_MAP)
    except Exception as e:
        return None

def theory_box(title, content_md):
    st.markdown(f"### 📚 Theoretical Background: {title}")
    st.markdown(content_md)
    st.divider()

def step_header(n, title, desc=""):
    st.markdown(f"#### Step {n}: {title}")
    if desc:
        st.markdown(desc)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🧮 Math Solver Pro")
    st.caption("Detailed step-by-step solver with theory")
    mode = st.radio(
        "Choose Solver:",
        ["First-Degree Equation", "Second-Degree Equation", "Linear Systems", "Derivative", "Integral"],
        index=0
    )
    st.divider()
    st.markdown("**How to write expressions:**")
    st.code("2*x + 3\nx^2 + 3*x + 2\nsin(x) + x**2\n1/(x+1)\nexp(x), sqrt(x), log(x)")
    st.info("All explanations are in English as requested. The solver shows every algebraic manipulation.")

# ================= 1 - FIRST DEGREE =================
if mode == "First-Degree Equation":
    st.title("1️⃣ First-Degree Equation Solver")
    theory_box("Linear Equation (First Degree)",
    r"""
**Definition:** A first-degree equation in one variable is an equation that can be written in the form:
$$ a x + b = 0 \quad \text{or} \quad a x + b = c $$
where $a \neq 0$ and $a, b, c \in \mathbb{R}$.

**Fundamental Concept:** The degree is 1 because the highest exponent of the variable is 1. Geometrically, $y = a x + b$ is a straight line, and the solution is where this line crosses the x-axis (or where two lines intersect).

**Properties Used to Solve:**
1.  **Addition/Subtraction Property of Equality:** If $A = B$, then $A \pm k = B \pm k$
2.  **Multiplication/Division Property of Equality:** If $A = B$, then $k \cdot A = k \cdot B$ for $k \neq 0$
3.  **Goal:** Isolate the variable $x$ on one side: $x = \text{value}$.

**General Solution Formula:** For $a x + b = 0$ → $x = -b / a$.
    """)

    st.subheader("Enter your equation")
    col1, col2 = st.columns([2,1])
    with col1:
        eq_input = st.text_input("Equation (e.g., 2*x + 3 = 7, or 4x - 5 = 0)", value="2*x + 3 = 11")
    with col2:
        solve_mode = st.selectbox("Input mode", ["Full Equation String", "Coefficients a*x + b = c"])

    a_val = b_val = c_val = None

    if solve_mode == "Coefficients a*x + b = c":
        c1, c2, c3 = st.columns(3)
        a_val = c1.number_input("a (coefficient of x)", value=2.0)
        b_val = c2.number_input("b (constant left)", value=3.0)
        c_val = c3.number_input("c (right side)", value=11.0)
        eq_input = f"{a_val}*x + {b_val} = {c_val}"

    if st.button("Solve First-Degree Equation", type="primary"):
        if "=" not in eq_input:
            st.error("Please include '=' in your equation.")
        else:
            left_str, right_str = eq_input.split("=", 1)
            left_expr = safe_parse(left_str)
            right_expr = safe_parse(right_str)
            if left_expr is None or right_expr is None:
                st.error(f"Could not parse equation. Check syntax.")
            else:
                st.markdown("### 🔍 Detailed Step-by-Step Solution")
                
                eq_sym = Eq(left_expr, right_expr)
                st.latex(sp.latex(eq_sym))
                
                # Step 1: Identify
                step_header(1, "Identify and Understand the Equation", 
                            f"We have: ${sp.latex(left_expr)} = {sp.latex(right_expr)}$\n\nThis is a first-degree equation because the variable $x$ appears with exponent 1 only.")
                
                # Step 2: Bring all to one side / Standard form
                expr_combined = left_expr - right_expr
                expr_expanded = sp.expand(expr_combined)
                st.markdown(f"We want to bring all terms to the left side to get standard form $a x + b = 0$.")
                st.latex(f"{sp.latex(left_expr)} - ({sp.latex(right_expr)}) = 0")
                st.latex(f"{sp.latex(expr_expanded)} = 0")
                
                poly = Poly(expr_expanded, x)
                if poly.degree() != 1:
                    st.warning(f"After simplification, this is degree {poly.degree()}, not 1. But we will continue.")
                    coeffs = poly.all_coeffs()
                else:
                    coeffs = poly.all_coeffs() # [a, b]
                    a_std = coeffs[0]
                    b_std = coeffs[1] if len(coeffs) > 1 else 0
                    
                    step_header(2, "Extract Coefficients in Standard Form",
                                f"Standard form is $a x + b = 0$. By comparing:")
                    st.latex(f"a = {sp.latex(a_std)}, \\quad b = {sp.latex(b_std)}")
                    st.markdown(f"So our equation is: ${sp.latex(a_std)} x + ({sp.latex(b_std)}) = 0$")

                # Step 3: Isolate
                step_header(3, "Isolate the Variable Term using Subtraction Property",
                            "We subtract $b$ from both sides to move the constant term to the right.")
                if poly.degree() == 1:
                    st.latex(f"{sp.latex(a_std)} x + {sp.latex(b_std)} - ({sp.latex(b_std)}) = 0 - ({sp.latex(b_std)})")
                    st.latex(f"{sp.latex(a_std)} x = {-b_std}")

                # Step 4: Division
                step_header(4, "Isolate x using Division Property",
                            "Now divide both sides by coefficient $a$ (which must be non-zero).")
                solution = solve(eq_sym, x)
                if solution:
                    sol = solution[0]
                    if poly.degree() == 1:
                        st.latex("x = \\frac{" + str(-b_std) + "}{" + sp.latex(a_std) + "}")
                        st.latex(f"x = {sp.latex(sol)}")
                        try:
                            st.latex(f"x \\approx {float(sol):.6f}")
                        except:
                            pass
                    else:
                        st.latex(f"x = {sp.latex(sol)}")

                # Step 5: Verification
                step_header(5, "Verification (Proof that solution is correct)",
                            "Substitute the found value back into the original equation.")
                if solution:
                    sol = solution[0]
                    lhs_check = left_expr.subs(x, sol)
                    rhs_check = right_expr.subs(x, sol)
                    st.latex(f"\\text{{Left}} = {sp.latex(left_expr)} = {sp.latex(left_expr.subs(x, sol))} = {sp.latex(sp.simplify(lhs_check))}")
                    st.latex(f"\\text{{Right}} = {sp.latex(right_expr)} = {sp.latex(sp.simplify(rhs_check))}")
                    if sp.simplify(lhs_check - rhs_check) == 0:
                        st.success(f"✅ Verified! LHS = RHS = {sp.latex(sp.simplify(lhs_check))}. The solution is correct.")
                    else:
                        st.error("Verification failed.")

                st.info("**Conceptual Summary:** We used inverse operations. Addition is undone by subtraction, multiplication by division. This preserves equality and leads to $x = \\text{number}$.")

# ================= 2 - SECOND DEGREE =================
elif mode == "Second-Degree Equation":
    st.title("2️⃣ Second-Degree (Quadratic) Equation Solver")
    theory_box("Quadratic Equation",
    r"""
**Definition:** A quadratic equation is a second-degree polynomial equation in one variable:
$$ a x^2 + b x + c = 0, \quad a \neq 0 $$

**Key Concepts:**
- **Degree 2:** Highest exponent is 2 → Graph is a parabola.
- **Number of Solutions:** Up to 2 real solutions (roots).
- **Discriminant:** $\Delta = b^2 - 4ac$ determines the nature of roots:
  - $\Delta > 0$: Two distinct real roots (parabola crosses x-axis twice)
  - $\Delta = 0$: One real double root (parabola touches x-axis)
  - $\Delta < 0$: No real roots, two complex conjugate roots (parabola does not cross)

**Solution Methods:**
1. **Factoring:** If possible, write as $(x - r_1)(x - r_2)=0$
2. **Completing the Square:** Transform to $(x + \frac{b}{2a})^2 = \frac{-c}{a} + \frac{b^2}{4a^2}$
3. **Quadratic Formula (Bhaskara):** The universal formula:
$$ x = \frac{-b \pm \sqrt{\Delta}}{2a} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$

**Vieta's Formulas:** For roots $r_1, r_2$: $r_1 + r_2 = -b/a$, $r_1 \cdot r_2 = c/a$.
    """)
    st.subheader("Enter quadratic: a*x^2 + b*x + c = 0")
    col_a, col_b, col_c = st.columns(3)
    a_q = col_a.number_input("a", value=1.0, format="%.5f")
    b_q = col_b.number_input("b", value=-3.0, format="%.5f")
    c_q = col_c.number_input("c", value=2.0, format="%.5f")
    
    alt_input = st.text_input("Or type full equation (e.g., x^2 - 3*x + 2 = 0)", value="x^2 - 3*x + 2 = 0")
    use_alt = st.checkbox("Use text equation instead of coefficients above")

    if st.button("Solve Quadratic", type="primary"):
        if use_alt:
            if "=" not in alt_input:
                st.error("Include '='")
                st.stop()
            l, r = alt_input.split("=",1)
            lex = safe_parse(l)
            rex = safe_parse(r)
            expr = sp.expand(lex - rex)
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            # pad to degree 2
            while len(coeffs) < 3:
                coeffs = [0] + coeffs
            a_q, b_q, c_q = float(coeffs[0]), float(coeffs[1]), float(coeffs[2]) if len(coeffs)>2 else 0
            a_sym, b_sym, c_sym = coeffs[0], coeffs[1], coeffs[2] if len(coeffs)>2 else 0
        else:
            a_sym, b_sym, c_sym = sp.nsimplify(a_q), sp.nsimplify(b_q), sp.nsimplify(c_q)
            expr = a_sym*x**2 + b_sym*x + c_sym

        st.markdown("### 🔍 Detailed Step-by-Step Solution")
        st.latex(f"{sp.latex(a_sym)} x^2 + {sp.latex(b_sym)} x + {sp.latex(c_sym)} = 0")

        if a_sym == 0:
            st.error("Coefficient 'a' cannot be zero for a quadratic equation. It would be linear.")
            st.stop()

        step_header(1, "Identify Coefficients and Standard Form",
                    "We compare to $a x^2 + b x + c = 0$")
        st.latex(f"a = {sp.latex(a_sym)}, \\; b = {sp.latex(b_sym)}, \\; c = {sp.latex(c_sym)}")

        step_header(2, "Compute the Discriminant", 
                    "Discriminant $\\Delta = b^2 - 4ac$ tells us the nature of roots. Derived from completing the square.")
        delta = b_sym**2 - 4*a_sym*c_sym
        delta_simplified = sp.expand(delta)
        st.latex(f"\\Delta = b^2 - 4ac = ({sp.latex(b_sym)})^2 - 4({sp.latex(a_sym)})({sp.latex(c_sym)})")
        st.latex(f"\\Delta = {sp.latex(b_sym**2)} - {sp.latex(4*a_sym*c_sym)} = {sp.latex(delta_simplified)}")
        try:
            st.write(f"Numerical value: Δ ≈ {float(delta_simplified):.6f}")
        except:
            pass

        if delta_simplified.is_number:
            if delta_simplified > 0:
                st.success("Δ > 0 → Two distinct real roots. Parabola intersects x-axis at two points.")
            elif delta_simplified == 0:
                st.warning("Δ = 0 → One real double root (repeated). Parabola touches x-axis at vertex.")
            else:
                st.info("Δ < 0 → No real roots, two complex conjugate roots. Parabola does not cross x-axis.")

        step_header(3, "Apply Quadratic Formula (Bhaskara)",
                    "Formula comes from completing the square for general quadratic:")
        st.latex(r"x = \frac{-b \pm \sqrt{\Delta}}{2a}")
        latex_b = sp.latex(b_sym)
        latex_delta = sp.latex(delta_simplified)
        latex_a = sp.latex(a_sym)
        latex_2a = sp.latex(2*a_sym)
        latex_minus_b = sp.latex(-b_sym)
        st.latex("x = \\frac{ -(" + latex_b + ") \\pm \\sqrt{" + latex_delta + "}}{2 \\cdot " + latex_a + "}")
        st.latex("x = \\frac{" + latex_minus_b + " \\pm \\sqrt{" + latex_delta + "}}{" + latex_2a + "}")

        step_header(4, "Compute the Two Roots Separately",
                    "We evaluate both plus and minus branches.")
        roots = solve(Eq(expr,0), x)
        for i, r in enumerate(roots):
            st.latex(f"x_{i+1} = {sp.latex(r)} \\approx {complex(r.evalf()):.6f}" if r.is_number else f"x_{i+1} = {sp.latex(r)}")
        
        # If complex, show real/imag
        if len(roots) == 2:
            step_header(5, "Detailed Calculation for Each Root")
            sqrt_delta = sp.sqrt(delta_simplified)
            x1_form = (-b_sym + sqrt_delta) / (2*a_sym)
            x2_form = (-b_sym - sqrt_delta) / (2*a_sym)
            st.latex("x_1 = \\frac{" + latex_minus_b + " + \\sqrt{" + latex_delta + "}}{" + latex_2a + "} = " + sp.latex(sp.simplify(x1_form)))
            st.latex("x_2 = \\frac{" + latex_minus_b + " - \\sqrt{" + latex_delta + "}}{" + latex_2a + "} = " + sp.latex(sp.simplify(x2_form)))

        step_header(6, "Factorization and Vieta Verification",
                    "If $r_1, r_2$ are roots, then $a x^2 + b x + c = a(x - r_1)(x - r_2)$")
        if len(roots) >=1:
            try:
                factored = sp.factor(expr)
                st.latex(f"\\text{{Factored form: }} {sp.latex(expr)} = {sp.latex(factored)}")
            except:
                pass
            if len(roots)==2:
                sum_roots = sp.simplify(roots[0] + roots[1])
                prod_roots = sp.simplify(roots[0]*roots[1])
                st.latex(f"r_1 + r_2 = {sp.latex(sum_roots)} \\; \\text{{ should be }} -b/a = {sp.latex(sp.simplify(-b_sym/a_sym))}")
                st.latex(f"r_1 \\cdot r_2 = {sp.latex(prod_roots)} \\; \\text{{ should be }} c/a = {sp.latex(sp.simplify(c_sym/a_sym))}")
                if sp.simplify(sum_roots + b_sym/a_sym) == 0 and sp.simplify(prod_roots - c_sym/a_sym) == 0:
                    st.success("✅ Vieta's formulas verified!")

        # Vertex
        step_header(7, "Extra: Vertex and Graph Information",
                    "The vertex is the maximum/minimum point of the parabola.")
        xv = -b_sym/(2*a_sym)
        yv = expr.subs(x, xv)
        st.latex(f"x_v = -b/(2a) = {sp.latex(sp.simplify(xv))}, \\quad y_v = f(x_v) = {sp.latex(sp.simplify(yv))}")
        if a_sym > 0:
            st.markdown("Since $a > 0$, parabola opens **upwards** → vertex is minimum.")
        else:
            st.markdown("Since $a < 0$, parabola opens **downwards** → vertex is maximum.")

# ================= 3 - LINEAR SYSTEMS =================
elif mode == "Linear Systems":
    st.title("📐 Linear Systems Solver")
    theory_box("Systems of Linear Equations",
    r"""
**Definition:** A system of linear equations is a collection of linear equations with the same variables.
For example, a $2 \times 2$ system:
$$
\begin{cases}
a_{11} x + a_{12} y = b_1 \\
a_{21} x + a_{22} y = b_2
\end{cases}
$$

**Possible Solutions:**
1.  **Unique solution:** Lines intersect at one point (determinant $\neq 0$)
2.  **No solution:** Lines are parallel (inconsistent)
3.  **Infinitely many solutions:** Lines are the same (dependent)

**Solution Methods:**
- **Substitution:** Solve one equation for one variable and substitute into the other.
- **Elimination (Gaussian Elimination):** Add multiples of equations to eliminate variables. This is systematic and works for any size.
- **Cramer's Rule (for $2\times2$):** $x = \frac{\det(A_x)}{\det(A)}$, $y = \frac{\det(A_y)}{\det(A)}$
- **Matrix Inverse:** $A \mathbf{x} = \mathbf{b} \implies \mathbf{x} = A^{-1} \mathbf{b}$

**This solver uses Gaussian Elimination with detailed row operations**, because it is the most instructive and general method. Each operation corresponds to an elementary row operation that preserves the solution set:
- Swap rows
- Multiply a row by non-zero constant
- Add multiple of one row to another.
    """)

    size = st.selectbox("System size", ["2x2 (2 equations, 2 variables)", "3x3 (3 equations, 3 variables)"], index=0)
    n = 2 if "2x2" in size else 3
    vars_sym = [x, y, z][:n]
    var_names = ['x', 'y', 'z'][:n]

    st.subheader(f"Enter coefficients for {n}x{n} system: A * [vars] = b")
    st.markdown("Form: $a_{11}x + a_{12}y (+ a_{13}z) = b_1$ etc.")

    A = []
    b_vec = []
    cols = st.columns(n+1)
    for i in range(n):
        row = []
        st.markdown(f"**Equation {i+1}:**")
        c = st.columns(n+1)
        for j in range(n):
            val = c[j].number_input(f"a[{i+1},{j+1}] ({var_names[j]})", value=float(1 if i==j else (1 if j==0 else 0)), key=f"a_{i}_{j}", format="%.4f")
            row.append(val)
        b_val = c[n].number_input(f"b[{i+1}]", value=float(i+1), key=f"b_{i}", format="%.4f")
        A.append(row)
        b_vec.append(b_val)

    if st.button("Solve Linear System", type="primary"):
        A_np = np.array(A, dtype=float)
        b_np = np.array(b_vec, dtype=float)
        st.markdown("### 🔍 Detailed Solution via Gaussian Elimination")

        # Augmented matrix
        Aug = np.hstack([A_np, b_np.reshape(-1,1)])
        st.markdown("**Initial Augmented Matrix [A|b]:**")
        st.latex(sp.latex(sp.Matrix(Aug)))

        step_header(1, "Check Determinant (Existence of Unique Solution)",
                    "Compute det(A) to predict solution type.")
        det = np.linalg.det(A_np)
        st.latex(f"\\det(A) = {det:.6f}")
        if abs(det) < 1e-9:
            st.warning("Determinant ≈ 0 → Matrix is singular. System may have no solution or infinite solutions. Proceeding with elimination to classify.")
        else:
            st.success(f"Determinant ≠ 0 ({det:.4f}) → Unique solution exists.")

        # Gaussian elimination with steps
        st.markdown("#### Gaussian Elimination Steps:")
        M = Aug.copy()
        steps_log = []
        for col in range(n):
            # Partial pivoting
            pivot_row = col + np.argmax(np.abs(M[col:, col]))
            if abs(M[pivot_row, col]) < 1e-12:
                st.write(f"Column {col+1}: No pivot found, column is zero below.")
                continue
            if pivot_row != col:
                st.markdown(f"**Swap R{col+1} ↔ R{pivot_row+1}** to get larger pivot")
                M[[col, pivot_row]] = M[[pivot_row, col]]
                st.latex(sp.latex(sp.Matrix(np.round(M,4))))
            
            pivot = M[col, col]
            st.markdown(f"**Pivot at R{col+1}, C{col+1} = {pivot:.4f}**")
            
            # Normalize pivot row (optional, we will show)
            # Eliminate below
            for r in range(col+1, n):
                factor = M[r, col] / pivot
                if abs(factor) > 1e-12:
                    st.markdown(f"**Eliminate x_{col+1} from R{r+1}:** $R_{r+1} \\leftarrow R_{r+1} - ({factor:.4f}) \\cdot R_{col+1}$")
                    M[r, :] = M[r, :] - factor * M[col, :]
                    st.latex(sp.latex(sp.Matrix(np.round(M,4))))

        # Back substitution
        st.markdown("#### Back Substitution (from bottom to top):")
        x_sol = np.zeros(n)
        for i in reversed(range(n)):
            if abs(M[i,i]) < 1e-12:
                if abs(M[i,-1]) < 1e-12:
                    st.markdown(f"Row {i+1}: $0 = 0$ → infinite solutions along this dimension")
                else:
                    st.error(f"Row {i+1}: $0 = {M[i,-1]:.4f}$ → No solution! Inconsistent system.")
                    st.stop()
                continue
            sum_ax = np.dot(M[i, i+1:n], x_sol[i+1:n])
            x_sol[i] = (M[i, -1] - sum_ax) / M[i,i]
            st.latex(f"{var_names[i]} = \\frac{{{M[i,-1]:.4f} - {sum_ax:.4f}}}{{{M[i,i]:.4f}}} = {x_sol[i]:.6f}")

        st.success("### ✅ Final Solution:")
        for i, name in enumerate(var_names):
            st.latex(f"{name} = {x_sol[i]:.8f}")

        # Verification
        st.markdown("#### Verification: Substitute into original equations")
        for i in range(n):
            lhs = np.dot(A_np[i], x_sol)
            st.latex(f"Eq {i+1}: {lhs:.6f} \\approx {b_np[i]:.6f} \\; { '✅' if abs(lhs-b_np[i])<1e-6 else '❌'}")

        # Cramer's for 2x2
        if n==2:
            step_header(2, "Alternative Check: Cramer's Rule for 2x2",
                        "For completeness, we also show Cramer's Rule.")
            A_mat = sp.Matrix(A_np)
            detA = A_mat.det()
            Ax = A_mat.copy()
            Ax[:,0] = sp.Matrix(b_np)
            Ay = A_mat.copy()
            Ay[:,1] = sp.Matrix(b_np)
            st.latex(f"\\det(A) = {sp.latex(detA)}")
            st.latex("\\det(A_x) = " + sp.latex(Ax.det()) + ", \\; x = \\frac{\\det(A_x)}{\\det(A)} = " + sp.latex(Ax.det()/detA))
            st.latex("\\det(A_y) = " + sp.latex(Ay.det()) + ", \\; y = \\frac{\\det(A_y)}{\\det(A)} = " + sp.latex(Ay.det()/detA))

# ================= 4 - DERIVATIVE =================
elif mode == "Derivative":
    st.title("📈 Derivative Solver")
    theory_box("Derivatives",
    r"""
**Definition (Limit):** The derivative of $f$ at $x$ is:
$$ f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} $$
if the limit exists.

**Geometric Interpretation:** $f'(x_0)$ is the slope of the tangent line to the curve $y = f(x)$ at $x_0$.
**Physical Interpretation:** Instantaneous rate of change (velocity if $f$ is position).

**Core Differentiation Rules:**
1.  **Power Rule:** $\frac{d}{dx}[x^n] = n x^{n-1}$
2.  **Constant Multiple:** $\frac{d}{dx}[c f] = c f'$
3.  **Sum/Difference:** $(f \pm g)' = f' \pm g'$
4.  **Product Rule:** $(f g)' = f' g + f g'$
5.  **Quotient Rule:** $\left(\frac{f}{g}\right)' = \frac{f' g - f g'}{g^2}$
6.  **Chain Rule:** $(f(g(x)))' = f'(g(x)) \cdot g'(x)$ - for composite functions.
7.  **Special Functions:** $\frac{d}{dx} \sin x = \cos x$, $\frac{d}{dx} e^x = e^x$, $\frac{d}{dx} \ln x = 1/x$

**This solver identifies which rules apply and shows the breakdown.**
    """)

    st.subheader("Enter function f(x)")
    f_input = st.text_input("f(x) =", value="x^3 + 2*x^2 - 5*x + sin(x)")
    var_choice = st.selectbox("Variable to differentiate w.r.t.", ["x", "t"], index=0)
    var = x if var_choice=="x" else t
    order = st.slider("Order of derivative", 1, 3, 1)

    if st.button("Compute Derivative", type="primary"):
        f_expr = safe_parse(f_input, var=var)
        if f_expr is None:
            st.error("Could not parse function. Check syntax.")
            st.stop()
        
        st.markdown("### 🔍 Detailed Step-by-Step Differentiation")
        st.latex(f"f({var_choice}) = {sp.latex(f_expr)}")

        step_header(1, "Identify Structure of Function",
                    "We analyze whether it's a sum, product, quotient, composition, etc.")
        # Breakdown if Add
        if f_expr.is_Add:
            st.markdown(f"The function is a **sum/difference of {len(f_expr.args)} terms**. By the Sum Rule, derivative of sum = sum of derivatives.")
            for i, term in enumerate(f_expr.args):
                st.latex(f"\\text{{Term {i+1}}}: {sp.latex(term)}")
        elif f_expr.is_Mul:
            st.markdown("The function is a **product** of factors → Product Rule will be needed.")
            st.latex(f"f = {sp.latex(f_expr.args[0])} \\cdot {sp.latex(f_expr.args[1])}" if len(f_expr.args)==2 else sp.latex(f_expr))
        elif f_expr.is_Pow:
            st.markdown("The function is a **power** → Power Rule + Chain Rule if base is not just x.")
        else:
            st.markdown(f"Function type: `{type(f_expr).__name__}`. We will apply appropriate rules.")

        step_header(2, f"Apply Differentiation Rules (Order {order})",
                    "We differentiate term by term.")
        
        # Show manual steps for each term if Add
        if f_expr.is_Add:
            deriv_terms = []
            for term in f_expr.args:
                d_term = sp.diff(term, var)
                st.markdown(f"**Derivative of term** ${sp.latex(term)}$:")
                # Explain power rule if applicable
                if term.is_Pow or (term.is_Mul and any(a.is_Pow for a in term.args)):
                    st.markdown("- Apply Power Rule / Constant Multiple: $\\frac{d}{d" + var_choice + "} " + sp.latex(term) + " = " + sp.latex(d_term) + "$")
                else:
                    # try to detect sin etc
                    st.latex("\\frac{d}{d" + var_choice + "} \\left[ " + sp.latex(term) + " \\right] = " + sp.latex(d_term))
                deriv_terms.append(d_term)
            st.markdown("Now sum all derivatives:")
            st.latex(f"f' = {' + '.join([sp.latex(d) for d in deriv_terms])}")
        else:
            # For product/chain, show chain breakdown
            if f_expr.has(sp.sin) or f_expr.has(sp.cos) or f_expr.has(sp.exp) or f_expr.has(sp.log):
                st.markdown("This contains **transcendental composition** → Chain Rule is used.")
                st.markdown("Chain Rule: $(f(g(x)))' = f'(g(x)) \\cdot g'(x)$")
        
        # Final derivative
        f_prime = sp.diff(f_expr, var, order)
        f_prime_simplified = sp.simplify(f_prime)
        st.markdown(f"#### Result after differentiation (order {order}):")
        st.latex("\\frac{d^{" + str(order) + "}}{d" + var_choice + "^{" + str(order) + "}} f = " + sp.latex(f_prime))
        st.latex(f"\\text{{Simplified: }} {sp.latex(f_prime_simplified)}")

        step_header(3, "Simplification and Interpretation",
                    "Simplify and discuss meaning.")
        st.latex(f"f^{{{order}}}({var_choice}) = {sp.latex(sp.factor(f_prime_simplified))}")
        
        # Show evaluation at point
        st.markdown("**Evaluate derivative at a point (optional check):**")
        pt = st.number_input(f"Evaluate at {var_choice} =", value=1.0)
        val_at = f_prime_simplified.subs(var, pt)
        st.latex(f"f^{{{order}}}({pt}) = {sp.latex(val_at)} \\approx {float(val_at.evalf()):.6f}" if val_at.is_number else f"f^{{{order}}}({pt}) = {sp.latex(val_at)}")
        st.info(f"Geometrically, this is the slope of the {'tangent line' if order==1 else 'rate of change of slope'} at {var_choice}={pt}.")

# ================= 5 - INTEGRAL =================
elif mode == "Integral":
    st.title("∫ Integral Solver")
    theory_box("Integrals",
    r"""
**Definition:**
- **Indefinite Integral (Antiderivative):** $\int f(x) dx = F(x) + C$ where $F'(x) = f(x)$. Represents a family of functions.
- **Definite Integral:** $\int_a^b f(x) dx$ is the limit of Riemann sums, equal to the net signed area under $y=f(x)$ from $a$ to $b$.

**Fundamental Theorem of Calculus (FTC):**
1.  If $F(x) = \int_a^x f(t) dt$, then $F'(x) = f(x)$
2.  $\int_a^b f(x) dx = F(b) - F(a)$ where $F$ is any antiderivative of $f$.

**Core Integration Rules:**
1.  **Power Rule:** $\int x^n dx = \frac{x^{n+1}}{n+1} + C$, $n \neq -1$
2.  **Exponential:** $\int e^x dx = e^x + C$
3.  **Trigonometric:** $\int \sin x dx = -\cos x + C$, $\int \cos x dx = \sin x + C$
4.  **Constant Multiple & Sum:** $\int (c f + g) = c\int f + \int g$
5.  **Substitution (u-sub):** $\int f(g(x)) g'(x) dx = \int f(u) du$, $u=g(x)$ - reverse chain rule.
6.  **Integration by Parts:** $\int u dv = u v - \int v du$ - reverse product rule.

**This solver identifies the pattern and shows step-by-step application.**
    """)

    st.subheader("Enter function to integrate")
    f_int_input = st.text_input("f(x) =", value="x^2 + 3*x + 2")
    int_type = st.radio("Type", ["Indefinite Integral (antiderivative)", "Definite Integral"], horizontal=True)
    var_int_choice = st.selectbox("Variable", ["x", "t"], index=0, key="var_int")
    var_int = x if var_int_choice=="x" else t

    a_lim = b_lim = None
    if int_type == "Definite Integral":
        c1, c2 = st.columns(2)
        a_lim = c1.number_input("Lower limit a", value=0.0)
        b_lim = c2.number_input("Upper limit b", value=1.0)

    if st.button("Compute Integral", type="primary"):
        f_expr = safe_parse(f_int_input, var=var_int)
        if f_expr is None:
            st.error("Could not parse function.")
            st.stop()

        st.markdown("### 🔍 Detailed Step-by-Step Integration")
        st.latex(f"f({var_int_choice}) = {sp.latex(f_expr)}")

        step_header(1, "Analyze Integrand Structure",
                    "Check if integrand is sum, power, product (needs by parts), composite (needs u-sub), etc.")
        if f_expr.is_Add:
            st.markdown(f"Integrand is **sum of {len(f_expr.args)} terms** → Use Sum Rule: integral of sum = sum of integrals.")
            for term in f_expr.args:
                st.latex(f"\\int {sp.latex(term)} d{var_int_choice}")
        elif f_expr.is_Mul and len(f_expr.args) == 2:
            st.markdown("Integrand is **product** → May need Integration by Parts: $\\int u dv = uv - \\int v du$")
            st.latex(f"\\text{{Try: }} u = {sp.latex(f_expr.args[0])}, dv = {sp.latex(f_expr.args[1])} d{var_int_choice}")
        elif f_expr.is_Pow or f_expr.is_Symbol:
            st.markdown("Power function detected → Direct Power Rule applicable: $\\int x^n = x^{n+1}/(n+1)$")

        # Manual integrate for steps if possible
        try:
            from sympy.integrals.manualintegrate import manualintegrate, integral_steps
            steps = integral_steps(f_expr, var_int)
            st.markdown("**SymPy Manual Integration Steps (rule breakdown):**")
            st.code(str(steps)[:2000])
        except Exception as e:
            steps = None

        step_header(2, "Apply Integration Rules Term by Term",
                    "We integrate each piece using appropriate rule.")
        
        if f_expr.is_Add:
            integrated_terms = []
            for term in f_expr.args:
                int_term = sp.integrate(term, var_int)
                # Explain rule
                if term.is_Pow or term.is_Symbol or term.is_Number:
                    # power rule
                    if term == var_int:
                        st.latex("\\int " + sp.latex(term) + " d" + var_int_choice + " = \\int " + var_int_choice + "^1 d" + var_int_choice + " = \\frac{" + var_int_choice + "^2}{2} = " + sp.latex(int_term))
                    elif term.is_Pow:
                        base, exp = term.as_base_exp()
                        if base == var_int:
                            st.latex("\\int " + var_int_choice + "^{" + sp.latex(exp) + "} d" + var_int_choice + " = \\frac{" + var_int_choice + "^{" + sp.latex(exp+1) + "}}{" + sp.latex(exp+1) + "} = " + sp.latex(int_term) + " \\quad \\text{(Power Rule)}")
                        else:
                            st.latex(f"\\int {sp.latex(term)} d{var_int_choice} = {sp.latex(int_term)}")
                    else:
                        st.latex(f"\\int {sp.latex(term)} d{var_int_choice} = {sp.latex(int_term)}")
                elif term.is_Mul:
                    # constant multiple
                    coeff = term.as_coeff_Mul()[0]
                    rest = term.as_coeff_Mul()[1]
                    st.latex(f"\\int {sp.latex(term)} d{var_int_choice} = {sp.latex(coeff)} \\int {sp.latex(rest)} d{var_int_choice} = {sp.latex(int_term)} \\quad \\text{{(Constant Multiple Rule)}}")
                else:
                    st.latex(f"\\int {sp.latex(term)} d{var_int_choice} = {sp.latex(int_term)}")
                integrated_terms.append(int_term)
            antideriv = sum(integrated_terms)
        else:
            antideriv = sp.integrate(f_expr, var_int)
            st.latex(f"\\int {sp.latex(f_expr)} d{var_int_choice} = {sp.latex(antideriv)} + C")

        step_header(3, "General Antiderivative (Indefinite Integral)",
                    "Add constant of integration $C$ because derivative of constant is zero.")
        antideriv_simplified = sp.simplify(antideriv)
        st.latex(f"\\int {sp.latex(f_expr)} d{var_int_choice} = {sp.latex(antideriv_simplified)} + C")
        st.markdown("**Verification by differentiation:** $\\frac{d}{d" + var_int_choice + "} [" + sp.latex(antideriv_simplified) + "] = " + sp.latex(sp.diff(antideriv_simplified, var_int)) + "$ → Should equal original integrand.")
        if sp.simplify(sp.diff(antideriv_simplified, var_int) - f_expr) == 0:
            st.success("✅ Differentiation check passed: derivative of antiderivative equals original integrand.")

        if int_type == "Definite Integral" and a_lim is not None:
            step_header(4, "Apply Fundamental Theorem for Definite Integral",
                        f"FTC Part 2: $\\int_{{{a_lim}}}^{{{b_lim}}} f(x) dx = F({b_lim}) - F({a_lim})$ where $F$ is antiderivative.")
            Fa = antideriv_simplified.subs(var_int, a_lim)
            Fb = antideriv_simplified.subs(var_int, b_lim)
            definite_val = sp.integrate(f_expr, (var_int, a_lim, b_lim))
            st.latex(f"F({var_int_choice}) = {sp.latex(antideriv_simplified)}")
            st.latex(f"F({b_lim}) = {sp.latex(Fb)} \\approx {float(Fb.evalf()):.6f}")
            st.latex(f"F({a_lim}) = {sp.latex(Fa)} \\approx {float(Fa.evalf()):.6f}")
            st.latex(f"\\int_{{{a_lim}}}^{{{b_lim}}} {sp.latex(f_expr)} d{var_int_choice} = F({b_lim}) - F({a_lim}) = {sp.latex(Fb)} - ({sp.latex(Fa)}) = {sp.latex(definite_val)}")
            try:
                st.latex(f"\\approx {float(definite_val.evalf()):.8f}")
            except:
                pass
            st.info(f"Geometric meaning: Net signed area under $y=f(x)$ from $x={a_lim}$ to $x={b_lim}$ is {float(definite_val.evalf()):.6f}." if definite_val.is_number else "")

        # Extra: u-sub example hint
        if f_expr.has(sp.sin) and (var_int in f_expr.args[0].free_symbols if f_expr.args else False):
            st.markdown("#### 💡 Pattern Recognition Tip")
            st.markdown("Integrand contains $\\sin(g(x))$ or $\\cos(g(x))$ → Consider $u = g(x)$, $du = g'(x) dx$ substitution.")

st.markdown("---")
st.caption("Built with SymPy + Streamlit | All steps in English with theoretical introduction before solving | Educational purpose")
