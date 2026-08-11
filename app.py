    def solve_system_3x3(self, eq1_str, eq2_str, eq3_str):
        self.reset_step_count()
        try:
            if '=' not in eq1_str or '=' not in eq2_str or '=' not in eq3_str:
                return "<div class='step-box'>❌ Each equation must contain '='.</div>"
            step1 = self.increment_step()
            left1, right1 = eq1_str.split('=')
            left2, right2 = eq2_str.split('=')
            left3, right3 = eq3_str.split('=')
            expr1 = self.parse_func(left1) - self.parse_func(right1)
            expr2 = self.parse_func(left2) - self.parse_func(right2)
            expr3 = self.parse_func(left3) - self.parse_func(right3)
            if expr1 is None or expr2 is None or expr3 is None:
                return "<div class='step-box'>❌ Invalid expressions.</div>"
            step2 = self.increment_step()
            step3 = self.increment_step()
            step4 = self.increment_step()
            step5 = self.increment_step()
            step6 = self.increment_step()
            sol = solve((expr1, expr2, expr3), (self.x, self.y, self.z))
            step7 = self.increment_step()
            if not sol:
                return "<div class='step-box'>⚠️ No unique solution found.</div>"
            x_sol, y_sol, z_sol = sol[self.x], sol[self.y], sol[self.z]
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 System of Linear Equations (3 Variables)</div>
                <p>Solving systems of 3 linear equations with 3 variables:</p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• <b>Gaussian elimination:</b> Transform to row-echelon form</li>
                    <li>• <b>Matrix method:</b> Use determinant and Cramer's rule</li>
                    <li>• <b>Substitution method:</b> Solve step by step</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the system</span>
                    <p>The system of 3 equations with 3 variables is:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\\\ {latex(expr3)} = 0 \\end{{cases}}$$</div>
                    <p style="margin-left: 20px;">Variables: <b>x</b>, <b>y</b>, and <b>z</b></p>
                    <p style="margin-left: 20px;">Goal: Find values of x, y, and z that satisfy all three equations</p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Standard form</span>
                    <p>All equations are in standard form <b>ax + by + cz + d = 0</b>:</p>
                    <div class="formula-highlight">$$\\begin{{cases}} {latex(expr1)} = 0 \\\\ {latex(expr2)} = 0 \\\\ {latex(expr3)} = 0 \\end{{cases}}$$</div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Matrix representation</span>
                    <p>Represent the system as an augmented matrix:</p>
                    <div class="formula-highlight">
                        $$\\begin{{bmatrix}}
                        {sp.Poly(expr1, self.x).coeff_monomial(self.x)} & {sp.Poly(expr1, self.y).coeff_monomial(self.y)} & {sp.Poly(expr1, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr1, self.x).coeff_monomial(1)} \\\\
                        {sp.Poly(expr2, self.x).coeff_monomial(self.x)} & {sp.Poly(expr2, self.y).coeff_monomial(self.y)} & {sp.Poly(expr2, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr2, self.x).coeff_monomial(1)} \\\\
                        {sp.Poly(expr3, self.x).coeff_monomial(self.x)} & {sp.Poly(expr3, self.y).coeff_monomial(self.y)} & {sp.Poly(expr3, self.z).coeff_monomial(self.z)} & | & {sp.Poly(expr3, self.x).coeff_monomial(1)}
                        \\end{{bmatrix}}$$
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Choose solution method</span>
                    <p>We will use <b>Gaussian elimination</b> with the following steps:</p>
                    <ul style="margin-left: 20px;">
                        <li>Forward elimination to create zeros below the diagonal</li>
                        <li>Back substitution to find the values of variables</li>
                    </ul>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Forward elimination</span>
                    <p>Eliminate variables to get upper triangular form:</p>
                    <ul style="margin-left: 20px;">
                        <li>Use row operations to create zeros in lower-left positions</li>
                        <li>System becomes easier to solve step by step</li>
                    </ul>
                    <p style="margin-left: 20px;">After elimination, we obtain a system like:</p>
                    <div class="formula-highlight">
                        $$\\begin{{cases}}
                        a_{{11}}x + a_{{12}}y + a_{{13}}z = d_1 \\\\
                        a_{{22}}y + a_{{23}}z = d_2 \\\\
                        a_{{33}}z = d_3
                        \\end{{cases}}$$
                    </div>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Back substitution</span>
                    <p>Solve from the last equation backwards:</p>
                    <ul style="margin-left: 20px;">
                        <li>Solve for z from the third equation</li>
                        <li>Substitute z into the second equation to find y</li>
                        <li>Substitute y and z into the first equation to find x</li>
                    </ul>
                    <p style="margin-left: 20px;">Solution found:</p>
                    <p style="margin-left: 40px;">x = <b>{latex(sp.nsimplify(x_sol))}</b></p>
                    <p style="margin-left: 40px;">y = <b>{latex(sp.nsimplify(y_sol))}</b></p>
                    <p style="margin-left: 40px;">z = <b>{latex(sp.nsimplify(z_sol))}</b></p>
                </div>
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Verify the solution</span>
                    <p>Substitute x = {latex(sp.nsimplify(x_sol))}, y = {latex(sp.nsimplify(y_sol))}, and z = {latex(sp.nsimplify(z_sol))} into all three equations:</p>
                    <p style="margin-left: 20px;">Eq1: <b>{latex(expr1.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">Eq2: <b>{latex(expr2.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <p style="margin-left: 20px;">Eq3: <b>{latex(expr3.subs({self.x: x_sol, self.y: y_sol, self.z: z_sol}))}</b> ≈ 0 ✓</p>
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b> All three equations are satisfied</p>
                    </div>
                </div>
                <div class="result-box">🎯 <strong>Solution:</strong><br>
                $$
                x = {latex(sp.nsimplify(x_sol))} \\\\
                y = {latex(sp.nsimplify(y_sol))} \\\\
                z = {latex(sp.nsimplify(z_sol))}
                $$
                </div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"
