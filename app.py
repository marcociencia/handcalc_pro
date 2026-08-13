python_code = """import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(page_title="Advanced Math Solver", layout="wide", page_icon="♾️")

st.markdown(
    \"\"\"
    <style>
    .step-box {
        background-color: #1E1E1E;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .answer-box {
        background-color: #2C3E50;
        border-left: 5px solid #3498DB;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    </style>
    \"\"\",
    unsafe_allow_html=True
)

st.title("♾️ Advanced Math Solver – Step-by-Step")
st.markdown("### *Elegant, precise, and visually comprehensive solutions.*")
st.divider()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def render_step(step_num, title, latex_expr=None, text=None):
    st.markdown(f"**Step {step_num}: {title}**")
    if text:
        st.markdown(text)
    if latex_expr:
        st.latex(latex_expr)

x, y, z, h = sp.symbols('x y z h')
sym_vars = {'x': x, 'y': y, 'z': z, 'h': h}

def parse_expr(expr_str):
    try:
        return sp.sympify(expr_str.replace("^", "**"), locals=sym_vars)
    except:
        return None

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
menu = st.sidebar.radio(
    "Select Mathematical Module",
    [
        "1. Basic Operations (+, -, *, /)",
        "2. 1st Degree Function (Linear)",
        "3. 2nd Degree Function (Quadratic)",
        "4. Linear Systems (Matrices)",
        "5. Limits & Rules",
        "6. Derivatives & Tangents",
        "7. Integrals & Solids of Revolution"
    ]
)

# ==========================================
# 1. BASIC OPERATIONS WITH VISUAL RULES
# ==========================================
if menu.startswith("1"):
    st.header("1. Basic Operations (Addition, Subtraction, Multiplication, Division)")
    st.markdown("Detailed step-by-step with visual carrying, borrowing, and elegant lines.")
    
    op = st.selectbox("Select Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("First Number", value=136 if "Sub" in op else 125, step=1, min_value=0)
    with col2:
        num2 = st.number_input("Second Number", value=169 if "Sub" in op else 5, step=1, min_value=1 if "Div" in op else 0)

    if st.button("Calculate"):
        if op == "Addition (+)":
            # ADDITION LOGIC WITH CARRY
            n1_str, n2_str = str(num1)[::-1], str(num2)[::-1]
            max_len = max(len(n1_str), len(n2_str))
            n1_str = n1_str.ljust(max_len, '0')
            n2_str = n2_str.ljust(max_len, '0')
            
            carries = [0] * (max_len + 1)
            result = []
            
            for i in range(max_len):
                sum_val = int(n1_str[i]) + int(n2_str[i]) + carries[i]
                result.append(str(sum_val % 10))
                carries[i+1] = sum_val // 10
                
            ans = num1 + num2
            
            # Format LaTeX
            top_row = ""
            n1_latex = ""
            for i in range(max_len - 1, -1, -1):
                if carries[i+1] > 0:
                    n1_latex += f"\\overset{{\\color{{red}}{{{carries[i+1]}}}}}{{{n1_str[i]}}}"
                else:
                    n1_latex += f"{n1_str[i]}"
            
            # if final carry exists
            if carries[max_len] > 0:
                n1_latex = f"\\overset{{\\color{{red}}{{{carries[max_len]}}}}}{{0}}" + n1_latex
                
            latex_add = f\"\"\"
            \\begin{{array}}{{r}}
              {n1_latex} \\\\
            + {num2} \\\\
            \\hline
              {ans}
            \\end{{array}}
            \"\"\"
            st.markdown("### Addition with Carry")
            st.latex(latex_add)
            st.success(f"**Result:** {ans}")
            
        elif op == "Subtraction (-)":
            if num1 < num2:
                st.warning("For visual step-by-step subtraction, the first number should be greater than or equal to the second. I will swap them and add a negative sign to the final result.")
                num1, num2 = num2, num1
                is_negative = True
            else:
                is_negative = False
                
            n1_list = list(int(d) for d in str(num1))
            n2_list = list(int(d) for d in str(num2).zfill(len(n1_list)))
            
            # Tracking borrows for visual representation
            latex_top_row = []
            result_list = []
            
            for i in range(len(n1_list) - 1, -1, -1):
                if n1_list[i] < n2_list[i]:
                    # Borrow from left
                    n1_list[i] += 10
                    # Find non-zero to borrow from
                    j = i - 1
                    while n1_list[j] == 0:
                        n1_list[j] = 9
                        latex_top_row.insert(0, f"\\overset{{\\color{{blue}}9}}{{\\color{{red}}\\cancel{{0}}}}")
                        j -= 1
                    n1_list[j] -= 1
                    latex_top_row.insert(0, f"\\overset{{\\color{{blue}}{{{n1_list[i]}}}}}{{\\color{{red}}\\cancel{{{n1_list[i]-10}}}}}")
                else:
                    latex_top_row.insert(0, str(n1_list[i]))
            
            # Re-process top row visually to include the original numbers crossed out where borrowed
            original_n1 = list(int(d) for d in str(num1))
            current_n1 = list(int(d) for d in str(num1))
            latex_n1 = []
            
            for i in range(len(current_n1) - 1, -1, -1):
                if current_n1[i] < n2_list[i]:
                    current_n1[i] += 10
                    j = i - 1
                    while current_n1[j] == 0:
                        current_n1[j] = 9
                        j -= 1
                    current_n1[j] -= 1
            
            # Building the string for top row representation with cancel
            temp_n1 = list(str(num1))
            modified = list(str(num1))
            visual_row = []
            borrow_tracker = [0] * len(temp_n1)
            
            n1_digits = [int(d) for d in str(num1)]
            n2_digits = [int(d) for d in str(num2).zfill(len(n1_digits))]
            top_latex_parts = []
            
            for i in range(len(n1_digits)-1, -1, -1):
                if n1_digits[i] < n2_digits[i]:
                    val = n1_digits[i] + 10
                    top_latex_parts.insert(0, f"\\overset{{\\color{{blue}}{{{val}}}}}{{\\color{{red}}\\cancel{{{n1_digits[i]}}}}}")
                    
                    # Cascade borrow
                    j = i - 1
                    while j >= 0 and n1_digits[j] == 0:
                        n1_digits[j] = 9
                        top_latex_parts.insert(0, f"\\overset{{\\color{{blue}}9}}{{\\color{{red}}\\cancel{{0}}}}")
                        j -= 1
                    if j >= 0:
                        n1_digits[j] -= 1
                        # We don't append immediately, we just update the value. It will be processed when loop reaches j.
                else:
                    if len(top_latex_parts) < len(n1_digits) - i:
                        top_latex_parts.insert(0, str(n1_digits[i]))
            
            # Fallback robust string construction
            formatted_n1 = "".join(top_latex_parts) if len(top_latex_parts) == len(n1_digits) else ""
            
            # Safer logic for subtraction display
            work_n1 = [int(d) for d in str(num1)]
            work_n2 = [int(d) for d in str(num2).zfill(len(work_n1))]
            display_n1 = []
            
            for i in range(len(work_n1)-1, -1, -1):
                if work_n1[i] < work_n2[i]:
                    display_n1.insert(0, f"\\overset{{\\color{{blue}}{{{work_n1[i]+10}}}}}{{\\color{{red}}\\cancel{{{work_n1[i]}}}}}")
                    work_n1[i-1] -= 1
                else:
                    display_n1.insert(0, f"\\overset{{\\color{{blue}}{{{work_n1[i]}}}}}{{\\color{{red}}\\cancel{{{work_n1[i]+1 if i<len(work_n1)-1 and 'cancel' in display_n1[0] else work_n1[i]}}}}}" if i<len(work_n1)-1 and 'cancel' in display_n1[0] and work_n1[i]!=int(str(num1)[i]) else str(work_n1[i]))

            # Simplify the visual construction for elegance and stability
            st.markdown("### Subtraction with Borrowing")
            final_res = num1 - num2
            sign = "-" if is_negative else ""
            
            # Simple robust display logic
            n1_str_arr = list(str(num1))
            n2_str_arr = list(str(num2).zfill(len(n1_str_arr)))
            latex_str_n1 = ""
            work_arr = [int(x) for x in n1_str_arr]
            
            for i in range(len(work_arr)-1, -1, -1):
                if work_arr[i] < int(n2_str_arr[i]):
                    latex_str_n1 = f"\\overset{{\\color{{blue}}{{{work_arr[i]+10}}}}}{{\\color{{red}}\\cancel{{{n1_str_arr[i]}}}}}" + latex_str_n1
                    j = i - 1
                    while work_arr[j] == 0:
                        work_arr[j] = 9
                        n1_str_arr[j] = f"\\overset{{\\color{{blue}}9}}{{\\color{{red}}\\cancel{{0}}}}"
                        j -= 1
                    work_arr[j] -= 1
                    n1_str_arr[j] = f"\\overset{{\\color{{blue}}{{{work_arr[j]}}}}}{{\\color{{red}}\\cancel{{{int(n1_str_arr[j])}}}}}"
                else:
                    if str(work_arr[i]) == n1_str_arr[i]:
                        latex_str_n1 = n1_str_arr[i] + latex_str_n1
                    else:
                        latex_str_n1 = n1_str_arr[i] + latex_str_n1

            latex_sub = f\"\"\"
            \\begin{{array}}{{r}}
              {latex_str_n1} \\\\
            - {str(num2).zfill(len(str(num1)))} \\\\
            \\hline
              {final_res}
            \\end{{array}}
            \"\"\"
            st.latex(latex_sub)
            st.success(f"**Result:** {sign}{final_res}")

        elif op == "Multiplication (×)":
            st.markdown("### Multiplication Step-by-Step")
            n1_str = str(num1)
            n2_str = str(num2)
            
            lines = []
            for i, digit in enumerate(reversed(n2_str)):
                prod = num1 * int(digit)
                # Pad with spaces/zeros visually
                padding = "\\;" * (2 * i)  # visual shift
                if i == 0:
                    lines.append(f"{prod}")
                else:
                    lines.append(f"+ {prod}{padding}")
            
            lines_str = " \\\\\n".join(lines)
            
            latex_mult = f\"\"\"
            \\begin{{array}}{{r}}
              {num1} \\\\
            \\times {num2} \\\\
            \\hline
            {lines_str} \\\\
            \\hline
              {num1 * num2}
            \\end{{array}}
            \"\"\"
            st.latex(latex_mult)
            st.success(f"**Result:** {num1 * num2}")
            
        elif op == "Division (÷)":
            st.markdown("### Long Division (Brazilian 'L' Layout)")
            quotient = num1 // num2
            remainder = num1 % num2
            
            div_str = str(num1)
            latex_str = f"\\begin{{array}}{{r|l}}\n{num1} & {num2} \\\\\n\\cline{{2-2}}\n"
            
            temp_val = ""
            q_str = ""
            
            # Ensure proper alignment and lines
            for i, digit in enumerate(div_str):
                temp_val += digit
                val = int(temp_val)
                if val >= num2 or i == len(div_str) - 1:
                    q_digit = val // num2
                    q_str += str(q_digit)
                    sub_val = q_digit * num2
                    rem = val - sub_val
                    
                    padding = "0" * (len(div_str) - 1 - i)
                    latex_str += f"-{sub_val}\\phantom{{{padding}}} & {q_str} \\\\\n"
                    latex_str += f"\\cline{{1-1}}\n"
                    
                    temp_val = str(rem) if rem > 0 else ""
                    if i < len(div_str) - 1:
                        next_bring_down = (str(rem) if rem > 0 else "") + div_str[i+1]
                        latex_str += f"{next_bring_down}\\phantom{{{padding[1:]}}} & \\\\\n"
                    else:
                        latex_str += f"{rem} & \\\\\n"
                else:
                    if q_str != "":
                        q_str += "0"
            
            latex_str += "\\end{array}"
            
            st.latex(latex_str)
            st.success(f"**Quotient:** {quotient} | **Remainder:** {remainder}")

# ==========================================
# 2. FIRST DEGREE FUNCTION
# ==========================================
elif menu.startswith("2"):
    st.header("2. 1st Degree Function (Linear)")
    
    eq_input = st.text_input("Equation (e.g., 2*x + 3 = 7)", "2*x + 3 = 7")
    
    if st.button("Solve & Graph"):
        try:
            lhs_str, rhs_str = eq_input.split('=')
            lhs, rhs = parse_expr(lhs_str), parse_expr(rhs_str)
            expr = lhs - rhs
            sol = sp.solve(expr, x)[0]
            
            st.markdown("### Resolution Steps")
            render_step(1, "Original Equation", f"{sp.latex(lhs)} = {sp.latex(rhs)}")
            render_step(2, "Move all terms to one side", f"{sp.latex(expr)} = 0")
            
            a_val = expr.coeff(x)
            b_val = expr.subs(x, 0)
            render_step(3, "Identify Coefficients", f"a = {a_val}, \\quad b = {b_val}")
            render_step(4, "Isolate the variable", f"{a_val}x = {-b_val}")
            render_step(5, "Divide by a", f"x = \\frac{{{-b_val}}}{{{a_val}}}")
            render_step(6, "Simplify", f"x = {sp.latex(sol)}")
            
            st.success(f"**Final Solution:** $x = {sp.latex(sol)}$")
            
            x_vals = np.linspace(float(sol)-10, float(sol)+10, 100)
            y_vals = float(a_val)*x_vals + float(b_val)
            
            fig = px.line(x=x_vals, y=y_vals, title=f"Graph of y = {a_val}x + {b_val}")
            fig.add_scatter(x=[float(sol)], y=[0], mode='markers', marker=dict(size=10, color='red'), name="Root")
            fig.update_layout(xaxis_title="x", yaxis_title="y", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error("Please enter a valid linear equation.")

# ==========================================
# 3. SECOND DEGREE FUNCTION
# ==========================================
elif menu.startswith("3"):
    st.header("3. 2nd Degree Function (Quadratic)")
    
    eq_input = st.text_input("Equation (e.g., x**2 - 5*x + 6 = 0)", "x**2 - 5*x + 6 = 0")
    
    if st.button("Solve & Graph"):
        try:
            lhs_str, rhs_str = eq_input.split('=')
            lhs, rhs = parse_expr(lhs_str), parse_expr(rhs_str)
            expr = lhs - rhs
            
            a_val = expr.coeff(x, 2)
            b_val = expr.coeff(x, 1)
            c_val = expr.subs(x, 0)
            
            st.markdown("### Resolution Steps")
            render_step(1, "Standard Form", f"{sp.latex(expr)} = 0")
            render_step(2, "Identify Coefficients", f"a = {a_val}, \\quad b = {b_val}, \\quad c = {c_val}")
            
            delta = b_val**2 - 4*a_val*c_val
            render_step(3, "Calculate Discriminant ($\\Delta$)", f"\\Delta = b^2 - 4ac = ({b_val})^2 - 4({a_val})({c_val}) = {delta}")
            
            render_step(4, "Bhaskara's Formula", r"x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}")
            
            sols = sp.solve(expr, x)
            if delta > 0:
                render_step(5, "Two Real Roots", f"x_1 = {sp.latex(sols[0])}, \\quad x_2 = {sp.latex(sols[1])}")
            elif delta == 0:
                render_step(5, "One Real Root", f"x = {sp.latex(sols[0])}")
            else:
                render_step(5, "Complex Roots", f"x_1 = {sp.latex(sols[0])}, \\quad x_2 = {sp.latex(sols[1])}")
                
            xv = -b_val / (2*a_val)
            yv = -delta / (4*a_val)
            render_step(6, "Vertex Point", f"V = ({xv}, {yv})")
            
            st.success(f"**Roots:** {', '.join([f'$x = {sp.latex(s)}$' for s in sols])}")
            
            x_vals = np.linspace(float(xv)-5, float(xv)+5, 100)
            y_vals = float(a_val)*x_vals**2 + float(b_val)*x_vals + float(c_val)
            
            fig = px.line(x=x_vals, y=y_vals, title=f"Graph of y = {sp.latex(expr)}")
            for s in sols:
                if s.is_real:
                    fig.add_scatter(x=[float(s)], y=[0], mode='markers', marker=dict(size=10, color='red'), name=f"Root {float(s):.1f}")
            fig.add_scatter(x=[float(xv)], y=[float(yv)], mode='markers', marker=dict(size=10, color='yellow'), name="Vertex")
            fig.update_layout(xaxis_title="x", yaxis_title="y", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error("Please enter a valid quadratic equation.")

# ==========================================
# 4. LINEAR SYSTEMS
# ==========================================
elif menu.startswith("4"):
    st.header("4. Linear Systems (Matrices & Equations)")
    
    sys_type = st.radio("System Size", ["2x2 (x, y)", "3x3 (x, y, z)"])
    
    if sys_type == "2x2 (x, y)":
        eq1 = st.text_input("Equation 1", "2*x + y = 5")
        eq2 = st.text_input("Equation 2", "x - y = 1")
        eqs_str = [eq1, eq2]
        vars_list = [x, y]
    else:
        eq1 = st.text_input("Equation 1", "x + y + z = 6")
        eq2 = st.text_input("Equation 2", "2*x - y + z = 3")
        eq3 = st.text_input("Equation 3", "x + 2*y - z = 2")
        eqs_str = [eq1, eq2, eq3]
        vars_list = [x, y, z]

    if st.button("Solve System"):
        eqs = []
        for e in eqs_str:
            l, r = e.split('=')
            eqs.append(sp.Eq(parse_expr(l), parse_expr(r)))
            
        st.markdown("### Resolution Steps")
        
        sys_latex = "\\begin{cases} " + " \\\\ ".join([sp.latex(eq) for eq in eqs]) + " \\end{cases}"
        render_step(1, "System of Equations", sys_latex)
        
        A, B = sp.linear_eq_to_matrix(eqs, vars_list)
        render_step(2, "Matrix Form $AX = B$", f"\\begin{{bmatrix}} A \\end{{bmatrix}} = {sp.latex(A)}, \\quad \\begin{{bmatrix}} B \\end{{bmatrix}} = {sp.latex(B)}")
        
        det_A = A.det()
        render_step(3, "Determinant of A", f"\\det(A) = {det_A}")
        
        if det_A != 0:
            sol = sp.linsolve(eqs, vars_list)
            sol_list = list(list(sol)[0])
            
            render_step(4, "Applying Inverse / Row Reduction", f"X = A^{{-1}}B = {sp.latex(sp.Matrix(sol_list))}")
            
            ans_str = ", \\quad ".join([f"{vars_list[i]} = {sol_list[i]}" for i in range(len(vars_list))])
            st.success(f"**Solution:** ${ans_str}$")
        else:
            st.error("System has no unique solution (Determinant is 0).")

# ==========================================
# 5. LIMITS
# ==========================================
elif menu.startswith("5"):
    st.header("5. Limits & Rules")
    expr_input = st.text_input("Function f(x)", "sin(x)/x")
    point_input = st.text_input("Limit as x approaches", "0")
    
    if st.button("Evaluate Limit"):
        func = parse_expr(expr_input)
        pt = parse_expr(point_input)
        
        st.markdown("### Resolution Steps")
        render_step(1, "Setup Limit", f"\\lim_{{x \\to {sp.latex(pt)}}} {sp.latex(func)}")
        
        lim_val = sp.limit(func, x, pt)
        dir_sub = func.subs(x, pt)
        
        if dir_sub.is_finite and dir_sub == lim_val:
            render_step(2, "Direct Substitution", f"= {sp.latex(dir_sub)}")
        else:
            render_step(2, "Indeterminate Form Detected", "Applying algebraic simplification or L'Hôpital's Rule.")
            
        render_step(3, "Evaluate Limit", f"= {sp.latex(lim_val)}")
        st.success(f"**Limit:** ${sp.latex(lim_val)}$")

# ==========================================
# 6. DERIVATIVES & SOLIDS
# ==========================================
elif menu.startswith("6"):
    st.header("6. Derivatives & Tangents")
    
    rule = st.selectbox("Derivative Rule / Type", [
        "Power Rule", "Product Rule", "Quotient Rule", "Chain Rule", "Limit Definition", "Partial Derivatives (x,y,z)"
    ])
    
    expr_input = st.text_input("Function f(x) or f(x,y)", "x**3 * sin(x)")
    
    if st.button("Differentiate"):
        func = parse_expr(expr_input)
        
        st.markdown("### Resolution Steps")
        render_step(1, "Original Function", f"f = {sp.latex(func)}")
        
        if "Partial" in rule:
            dx = sp.diff(func, x)
            dy = sp.diff(func, y)
            dz = sp.diff(func, z) if func.has(z) else 0
            render_step(2, "Partial wrt x", f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(dx)}")
            render_step(3, "Partial wrt y", f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(dy)}")
            if func.has(z):
                render_step(4, "Partial wrt z", f"\\frac{{\\partial f}}{{\\partial z}} = {sp.latex(dz)}")
                
            st.info("Generating 3D Surface Graph for f(x,y)...")
            try:
                x_vals = np.linspace(-5, 5, 50)
                y_vals = np.linspace(-5, 5, 50)
                X_mesh, Y_mesh = np.meshgrid(x_vals, y_vals)
                f_lamb = sp.lambdify((x, y), func, "numpy")
                Z_mesh = f_lamb(X_mesh, Y_mesh)
                
                fig = go.Figure(data=[go.Surface(z=Z_mesh, x=X_mesh, y=Y_mesh, colorscale='Viridis')])
                fig.update_layout(title='Surface Plot of f(x,y)', autosize=False, width=800, height=600, template="plotly_dark")
                st.plotly_chart(fig)
            except Exception as e:
                st.warning("Could not plot 3D surface. Ensure the function only contains x and y.")

        elif rule == "Limit Definition":
            diff_quotient = (func.subs(x, x + h) - func) / h
            render_step(2, "Difference Quotient", f"\\frac{{f(x+h) - f(x)}}{{h}} = {sp.latex(diff_quotient)}")
            limit_res = sp.limit(diff_quotient, h, 0)
            render_step(3, "Limit as h -> 0", f"f'(x) = \\lim_{{h \\to 0}} {sp.latex(diff_quotient)} = {sp.latex(limit_res)}")
            st.success(f"**Derivative:** ${sp.latex(limit_res)}$")
        else:
            deriv = sp.diff(func, x)
            render_step(2, "Apply Differentiation Rule", f"\\frac{{d}}{{dx}}[{sp.latex(func)}]")
            render_step(3, "Raw Derivative", f"= {sp.latex(deriv)}")
            render_step(4, "Simplified Form", f"= {sp.latex(sp.simplify(deriv))}")
            st.success(f"**Derivative:** ${sp.latex(sp.simplify(deriv))}$")

# ==========================================
# 7. INTEGRALS & SOLIDS OF REVOLUTION
# ==========================================
elif menu.startswith("7"):
    st.header("7. Integrals & Solids of Revolution")
    
    rule = st.selectbox("Integration Type", [
        "Indefinite Integral (Primitives)", 
        "Definite Integral (FTC)", 
        "By Substitution", 
        "By Parts",
        "Volume of Solid of Revolution"
    ])
    
    expr_input = st.text_input("Function f(x)", "sqrt(x)")
    
    col1, col2 = st.columns(2)
    with col1:
        lower = st.text_input("Lower Bound (a)", "0")
    with col2:
        upper = st.text_input("Upper Bound (b)", "4")
        
    if st.button("Integrate"):
        func = parse_expr(expr_input)
        a_val = parse_expr(lower)
        b_val = parse_expr(upper)
        
        st.markdown("### Resolution Steps")
        
        if "Indefinite" in rule or "Substitution" in rule or "Parts" in rule:
            render_step(1, "Setup Integral", f"\\int {sp.latex(func)} \\, dx")
            integral_res = sp.integrate(func, x)
            render_step(2, "Compute Antiderivative", f"= {sp.latex(integral_res)} + C")
            st.success(f"**Result:** ${sp.latex(integral_res)} + C$")
            
        elif "Definite" in rule:
            render_step(1, "Setup Definite Integral", f"\\int_{{{lower}}}^{{{upper}}} {sp.latex(func)} \\, dx")
            anti = sp.integrate(func, x)
            render_step(2, "Find Antiderivative (FTC)", f"F(x) = {sp.latex(anti)}")
            res = sp.integrate(func, (x, a_val, b_val))
            render_step(3, "Evaluate F(b) - F(a)", f"F({upper}) - F({lower}) = {sp.latex(res)}")
            st.success(f"**Area:** ${sp.latex(res)}$")
            
        elif "Volume" in rule:
            render_step(1, "Setup Volume Integral (Disk Method)", f"V = \\pi \\int_{{{lower}}}^{{{upper}}} [{sp.latex(func)}]^2 \\, dx")
            vol_expr = sp.pi * (func**2)
            vol_res = sp.integrate(vol_expr, (x, a_val, b_val))
            render_step(2, "Evaluate", f"V = {sp.latex(vol_res)}")
            st.success(f"**Volume:** ${sp.latex(vol_res)}$")
            
            st.info("Generating 3D Solid of Revolution around X-axis...")
            try:
                x_num = np.linspace(float(a_val), float(b_val), 100)
                theta = np.linspace(0, 2*np.pi, 100)
                X_mesh, Theta_mesh = np.meshgrid(x_num, theta)
                
                f_lamb = sp.lambdify(x, func, "numpy")
                R_mesh = f_lamb(X_mesh)
                
                Y_mesh = R_mesh * np.cos(Theta_mesh)
                Z_mesh = R_mesh * np.sin(Theta_mesh)
                
                fig = go.Figure(data=[go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Plasma')])
                fig.update_layout(title="Solid of Revolution", autosize=False, width=800, height=600, template="plotly_dark")
                st.plotly_chart(fig)
            except Exception as e:
                st.warning("Ensure the bounds are numeric for plotting.")
"""

with open("Advanced_Math_Solver_Streamlit.py", "w", encoding="utf-8") as f:
    f.write(python_code)

print("File updated successfully.")
