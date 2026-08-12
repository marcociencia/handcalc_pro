    def solve_linear_detailed(self, eq_str):
        self.reset_step_count()
        try:
            if '=' not in eq_str:
                return "<div class='step-box'>❌ Please use '=' to separate left and right sides.</div>"
            
            left_str, right_str = eq_str.split('=')
            left_expr = self.parse_func(left_str)
            right_expr = self.parse_func(right_str)
            
            if left_expr is None or right_expr is None:
                return "<div class='step-box'>❌ Invalid expression. Use x as variable.</div>"
            
            step1 = self.increment_step()
            step2 = self.increment_step()
            expr = expand(left_expr - right_expr)
            
            step3 = self.increment_step()
            poly = sp.Poly(expr, self.x)
            coeffs = poly.all_coeffs()
            
            if len(coeffs) == 2:
                a, b = coeffs
            elif len(coeffs) == 1:
                a, b = 0, coeffs[0]
            else:
                a = b = 0
            
            if a == 0:
                return "<div class='step-box'>⚠️ Not a linear equation (a = 0).</div>"
            
            step4 = self.increment_step()
            step5 = self.increment_step()
            x_sol = -b / a
            latex_sol = latex(sp.nsimplify(x_sol))
            
            step6 = self.increment_step()
            verification_left = left_expr.subs(self.x, x_sol)
            verification_right = right_expr.subs(self.x, x_sol)
            
            step7 = self.increment_step()
            
            return f"""
            <div class="theory-box">
                <div class="theory-title">📚 Linear Equation (1st Degree) - Complete Resolution</div>
                <p>A linear equation in the form <b>ax + b = 0</b> has solution <b>x = -b/a</b></p>
                <p><b>Key Concepts:</b></p>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>• Linear equations have the highest power of variable = 1</li>
                    <li>• The solution is unique (one value of x)</li>
                    <li>• We can verify by substituting back into original equation</li>
                </ul>
            </div>
            <div class="step-box">
                <div class="step-header">📝 Detailed Resolution (7 Steps)</div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step1}: Identify the equation</span>
                    <p>We have the equation:</p>
                    <div class="formula-highlight">$$\\text{{Original equation: }} {latex(left_expr)} = {latex(right_expr)}$$</div>
                    <p style="margin-left: 20px;">• Left side: <b>{latex(left_expr)}</b></p>
                    <p style="margin-left: 20px;">• Right side: <b>{latex(right_expr)}</b></p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step2}: Move all terms to one side</span>
                    <p>Subtract the right side from both sides:</p>
                    <div class="formula-highlight">$${latex(left_expr)} - {latex(right_expr)} = 0$$</div>
                    <p style="margin-left: 20px;">This gives us the standard form <b>ax + b = 0</b></p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step3}: Identify coefficients a and b</span>
                    <p>Compare with standard form <b>ax + b = 0</b>:</p>
                    <div class="formula-highlight">$${latex(expr)} = 0$$</div>
                    <p style="margin-left: 20px;">Coefficient of x: <b>a = {a}</b></p>
                    <p style="margin-left: 20px;">Constant term: <b>b = {b}</b></p>
                    <p style="margin-left: 20px;">Verification: <b>{a}x + {b} = 0</b> ✓</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step4}: Isolate the variable term</span>
                    <p>Move the constant term to the right side:</p>
                    <div class="formula-highlight">
                        $${a}x = -{self.fmt_neg(b)}$$
                    </div>
                    <p style="margin-left: 20px;">• Subtract <b>{b}</b> from both sides</p>
                    <p style="margin-left: 20px;">• The variable term is now isolated</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step5}: Solve for x</span>
                    <p>Divide both sides by the coefficient <b>a</b>:</p>
                    <div class="formula-highlight">
                        $$x = \\frac{{-{self.fmt_neg(b)}}}{{{a}}}$$
                    </div>
                    <p style="margin-left: 20px;">Simplify the negative sign:</p>
                    <div class="formula-highlight">
                        $$-({self.fmt_neg(b)}) = {latex(sp.simplify(-b))}$$
                    </div>
                    <p style="margin-left: 20px;">Final value: <b>x = {latex_sol}</b></p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step6}: Verify the solution</span>
                    <p>Substitute x = {latex_sol} back into the original equation:</p>
                    <p style="margin-left: 20px;">Left side: <b>{latex(left_expr)}</b> → <b>{latex(verification_left)}</b></p>
                    <p style="margin-left: 20px;">Right side: <b>{latex(right_expr)}</b> → <b>{latex(verification_right)}</b></p>
                    <div class="formula-highlight">$${latex(verification_left)} = {latex(verification_right)}$$</div>
                    <p style="margin-left: 20px;">Both sides equal! ✓</p>
                </div>
                
                <div class="step-detail">
                    <span class="step-counter">Step {step7}: Final check and conclusion</span>
                    <p>We have successfully solved the equation:</p>
                    <div class="formula-highlight">$$\\boxed{{x = {latex_sol}}}$$</div>
                    <div class="verification">
                        <p>✅ <b>Verification complete:</b></p>
                        <p>Original: <b>{eq_str}</b></p>
                        <p>Substitute x = {latex_sol}:</p>
                        <p><b>{latex(left_expr.subs(self.x, x_sol))} = {latex(right_expr.subs(self.x, x_sol))}</b> ✓</p>
                    </div>
                </div>
                
                <div class="result-box">🎯 <strong>Solution: $x = {latex_sol}$</strong></div>
            </div>"""
        except Exception as e:
            return f"<div class='step-box'>❌ Error: {str(e)}</div>"
