import sympy as sp

class MathSolver:
    def __init__(self):
        # Define the math symbols used in equations and integrals
        self.x, self.y, self.z = sp.symbols('x y z')
        self.step_count = 0

    def reset_step_count(self):
        self.step_count = 0

    def increment_step(self):
        self.step_count += 1
        return self.step_count

    def fmt_neg(self, val):
        """Formats negative numbers for LaTeX to show -(-3) instead of --3."""
        if val < 0:
            return f"({val})"
        return f"{val}"

    def parse_func(self, expr_str):
        """Safely parses a string into a SymPy expression."""
        try:
            return sp.sympify(expr_str)
        except Exception:
            return None

    # ==========================================
    # LINEAR SYSTEMS: (x, y) and (x, y, z)
    # ==========================================
    def solve_system_detailed(self, eq_list):
        """
        Solves 2x2 or 3x3 linear systems in exactly 7 steps.
        Example eq_list: ["2*x + y = 5", "x - y = 1"]
        """
        self.reset_step_count()
        try:
            equations = []
            for eq_str in eq_list:
                if '=' not in eq_str:
                    return "<div class='step-box'>❌ Please use '=' in all equations.</div>"
                left_str, right_str = eq_str.split('=')
                equations.append(sp.Eq(self.parse_func(left_str), self.parse_func(right_str)))
                
            all_symbols = set()
            for eq in equations:
                all_symbols.update(eq.free_symbols)
                
            vars_list = sorted(list(all_symbols), key=lambda s: s.name)
            sys_size = len(vars_list)
            
            if len(equations) != sys_size or sys_size not in [2, 3]:
                return "<div class='step-box'>⚠️ Please provide exactly a 2x2 or 3x3 system.</div>"

            # Matrix A and Vector B
            A, B = sp.linear_eq_to_matrix(equations, vars_list)
            
            # STEPS 1 & 2
            step1 = self.increment_step()
            step2 = self.increment_step()
            
            det_A = A.det()
            if det_A == 0:
                return "<div class='step-box'>⚠️ The system has no unique solution (Main Determinant is 0).</div>"

            html_output = f"""
            <div class="theory-box">
                <div class="theory-title">📚 Linear System ({sys_size}x{sys_size})</div>
                <p>Solving step-by-step using <b>Cramer's Rule</b>.</p>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the Equations</span>
                    <p>We are solving the following system:</p>
                    <div class="formula-highlight">
                    \\[
                    \\begin{{cases}}
                    {' \\\\ '.join([sp.latex(eq) for eq in equations])}
                    \\end{{cases}}
                    \\]
                    </div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Matrix Representation ($A \\cdot X = B$)</span>
                    <p>Convert the system into a coefficient matrix $A$ and a constants column matrix $B$:</p>
                    <div class="formula-highlight">$$A = {sp.latex(A)}, \\quad B = {sp.latex(B)}$$</div>
                </div>
            """
            
            # STEP 3
            step3 = self.increment_step()
            html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Calculate the Main Determinant ($D$)</span>
                    <p>Calculate the determinant of matrix A to ensure the system has a unique solution:</p>
                    <div class="formula-highlight">$$D = \\det(A) = {sp.latex(det_A)}$$</div>
                </div>
            """

            # Dictionaries to store modified matrices and determinants
            dets = {}
            solutions = {}
            
            for i, var in enumerate(vars_list):
                A_mod = A.copy()
                A_mod[:, i] = B
                det_mod = A_mod.det()
                dets[var] = (A_mod, det_mod)
                solutions[var] = det_mod / det_A

            # STEPS 4, 5, 6 (Dynamic based on 2x2 or 3x3 to reach exactly 7 steps)
            if sys_size == 3:
                # 3x3 System
                for var, (A_mod, det_mod) in dets.items():
                    step = self.increment_step()
                    html_output += f"""
                    <div class="step-detail">
                        <span class="step-counter">Step {step}: Find Determinant for ${var}$ ($D_{var}$)</span>
                        <p>Replace the column of ${var}$ with matrix B:</p>
                        <div class="formula-highlight">$$D_{var} = \\det({sp.latex(A_mod)}) = {sp.latex(det_mod)}$$</div>
                        <div class="formula-highlight">$${var} = \\frac{{D_{var}}}{{D}} = \\frac{{{sp.latex(det_mod)}}}{{{sp.latex(det_A)}}} = {sp.latex(solutions[var])}$$</div>
                    </div>
                    """
                
                step7 = self.increment_step()
                final_sols = ", \\quad ".join([f"{v} = {sp.latex(val)}" for v, val in solutions.items()])
                html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Final Solution Set</span>
                    <p>Combining all the calculated values, the unique solution for the system is:</p>
                    <div class="formula-highlight">$$S = \\{{({final_sols})\\}}$$</div>
                </div>
                """

            else:
                # 2x2 System (Expanding steps to reach 7)
                var1, var2 = vars_list[0], vars_list[1]
                
                step4 = self.increment_step()
                html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Find Determinant for ${var1}$ ($D_{var1}$)</span>
                    <p>Replace the first column with matrix B:</p>
                    <div class="formula-highlight">$$D_{var1} = \\det({sp.latex(dets[var1][0])}) = {sp.latex(dets[var1][1])}$$</div>
                </div>
                """
                
                step5 = self.increment_step()
                html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Find Determinant for ${var2}$ ($D_{var2}$)</span>
                    <p>Replace the second column with matrix B:</p>
                    <div class="formula-highlight">$$D_{var2} = \\det({sp.latex(dets[var2][0])}) = {sp.latex(dets[var2][1])}$$</div>
                </div>
                """
                
                step6 = self.increment_step()
                html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Calculate final values for ${var1}$ and ${var2}$</span>
                    <p>Apply Cramer's rule formula:</p>
                    <div class="formula-highlight">$${var1} = \\frac{{D_{var1}}}{{D}} = \\frac{{{sp.latex(dets[var1][1])}}}{{{sp.latex(det_A)}}} = {sp.latex(solutions[var1])}$$</div>
                    <div class="formula-highlight">$${var2} = \\frac{{D_{var2}}}{{D}} = \\frac{{{sp.latex(dets[var2][1])}}}{{{sp.latex(det_A)}}} = {sp.latex(solutions[var2])}$$</div>
                </div>
                """
                
                step7 = self.increment_step()
                html_output += f"""
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Final Solution Set</span>
                    <p>The unique point of intersection is:</p>
                    <div class="formula-highlight">$$S = \\{{( {sp.latex(solutions[var1])}, {sp.latex(solutions[var2])} )\\}}$$</div>
                </div>
                """

            final_sols_banner = ", ".join([f"{v} = {sp.latex(val)}" for v, val in solutions.items()])
            html_output += f"""
                <div class="result-box">🎯 <strong>Solution: {final_sols_banner}</strong></div>
            </div>
            """
            return html_output
            
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"


    # ==========================================
    # TRIPLE INTEGRAL
    # ==========================================
    def triple_integral_detailed(self, expr_str, z_limits, y_limits, x_limits):
        """
        Calculates a definite triple integral step-by-step (7 steps).
        Limits must be passed as tuples: e.g., z_limits=("0", "1")
        Integrating order: dz dy dx (Inside out: z, then y, then x).
        """
        self.reset_step_count()
        try:
            func = self.parse_func(expr_str)
            
            z0, z1 = self.parse_func(z_limits[0]), self.parse_func(z_limits[1])
            y0, y1 = self.parse_func(y_limits[0]), self.parse_func(y_limits[1])
            x0, x1 = self.parse_func(x_limits[0]), self.parse_func(x_limits[1])
            
            # Setup Unevaluated integral for display
            full_integral = sp.Integral(func, (self.z, z0, z1), (self.y, y0, y1), (self.x, x0, x1))
            
            # Compute partials
            int_z_indef = sp.Integral(func, self.z)
            res_z = sp.integrate(func, (self.z, z0, z1))
            
            int_y_indef = sp.Integral(res_z, self.y)
            res_y = sp.integrate(res_z, (self.y, y0, y1))
            
            int_x_indef = sp.Integral(res_y, self.x)
            final_res = sp.integrate(res_y, (self.x, x0, x1))

            step1 = self.increment_step()
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            step6 = self.increment_step()
            step7 = self.increment_step()

            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 Triple Integral Resolution</div>
                <p>Evaluating the integral over a 3D region (Volume/Mass). Order of integration: <b>dz, dy, dx</b>.</p>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Setup the Triple Integral</span>
                    <p>We are going to evaluate the integral from the innermost to the outermost boundary:</p>
                    <div class="formula-highlight">$$I = {sp.latex(full_integral)}$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Innermost Integral Setup ($dz$)</span>
                    <p>Treating $x$ and $y$ as constants, we focus on the $z$ boundaries:</p>
                    <div class="formula-highlight">$$I_z = \\int_{{{sp.latex(z0)}}}^{{{sp.latex(z1)}}} {sp.latex(func)} \\,dz$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Evaluate Innermost Integral</span>
                    <p>Calculating the antiderivative for $z$ and applying limits from ${sp.latex(z0)}$ to ${sp.latex(z1)}$:</p>
                    <div class="formula-highlight">$${sp.latex(int_z_indef)} = {sp.latex(sp.integrate(func, self.z))}$$</div>
                    <div class="formula-highlight">$$I_z = {sp.latex(sp.simplify(res_z))}$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Middle Integral Setup ($dy$)</span>
                    <p>Substitute the result $I_z$ into the middle integral. Treating $x$ as a constant:</p>
                    <div class="formula-highlight">$$I_y = \\int_{{{sp.latex(y0)}}}^{{{sp.latex(y1)}}} \\left({sp.latex(res_z)}\\right) \\,dy$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Evaluate Middle Integral</span>
                    <p>Calculating the antiderivative for $y$ and applying limits from ${sp.latex(y0)}$ to ${sp.latex(y1)}$:</p>
                    <div class="formula-highlight">$${sp.latex(int_y_indef)} = {sp.latex(sp.integrate(res_z, self.y))}$$</div>
                    <div class="formula-highlight">$$I_y = {sp.latex(sp.simplify(res_y))}$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Outermost Integral Setup ($dx$)</span>
                    <p>Substitute the result $I_y$ into the outermost integral:</p>
                    <div class="formula-highlight">$$I_x = \\int_{{{sp.latex(x0)}}}^{{{sp.latex(x1)}}} \\left({sp.latex(res_y)}\\right) \\,dx$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Evaluate Outermost Integral & Final Result</span>
                    <p>Calculating the final definite integral for $x$ limits:</p>
                    <div class="formula-highlight">$${sp.latex(int_x_indef)} = {sp.latex(sp.integrate(res_y, self.x))}$$</div>
                    <div class="formula-highlight">$$I_x = {sp.latex(sp.simplify(final_res))}$$</div>
                </div>
                
                <div class="result-box">🎯 <strong>Final Result: $I = {sp.latex(sp.simplify(final_res))}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"
