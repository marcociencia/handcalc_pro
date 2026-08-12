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
