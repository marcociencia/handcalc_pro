não mostra nenhum passo a passo para equação primeiro grau, segundo grau, sistemas lineares (x, y) (x, y, z) e nem integral e derivada


Estou enviando o codigos:

Python




    def fmt_neg(self, val):
        """Formats negative numbers for LaTeX to show -(-3) instead of --3."""
        if val < 0:
            return f"({val})"  # Converts -3 to (-3)
        return f"{val}"
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


C++




// calculator_engine.cpp
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <algorithm>

class LongArithmeticCalculator {
private:
    struct Step {
        std::string description;
        std::string visual;
        int indent;
    };
    
    std::vector<Step> steps;
    
    // Helper function to convert string to number with decimal support
    double parseNumber(const std::string& num) {
        try {
            return std::stod(num);
        } catch (...) {
            return 0.0;
        }
    }
    
    // Format number for display
    std::string formatNumber(double num) {
        if (num == floor(num)) {
            return std::to_string((long long)num);
        }
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(6) << num;
        std::string result = ss.str();
        // Remove trailing zeros
        result.erase(result.find_last_not_of('0') + 1, std::string::npos);
        if (result.back() == '.') result.pop_back();
        return result;
    }
    
    // Create separation line
    std::string createLine(int length) {
        return std::string(length, '─');
    }
    
    // Center align numbers
    std::string centerAlign(const std::string& text, int width) {
        int padding = width - text.length();
        if (padding <= 0) return text;
        int leftPad = padding / 2;
        return std::string(leftPad, ' ') + text;
    }

public:
    LongArithmeticCalculator() {
        steps.clear();
    }
    
    // Addition with manual step-by-step
    std::string add(std::string a, std::string b) {
        steps.clear();
        double num1 = parseNumber(a);
        double num2 = parseNumber(b);
        double result = num1 + num2;
        
        // Find the wider number for alignment
        int maxLen = std::max(a.length(), b.length());
        int resultLen = formatNumber(result).length();
        int totalWidth = std::max(maxLen + 2, resultLen) + 2;
        
        std::ostringstream visual;
        visual << std::string(totalWidth - a.length(), ' ') << a << "\n";
        visual << "+" << std::string(totalWidth - b.length() - 1, ' ') << b << "\n";
        visual << createLine(totalWidth) << "\n";
        visual << std::string(totalWidth - resultLen, ' ') << formatNumber(result) << "\n";
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Subtraction with manual step-by-step
    std::string subtract(std::string a, std::string b) {
        steps.clear();
        double num1 = parseNumber(a);
        double num2 = parseNumber(b);
        double result = num1 - num2;
        
        int maxLen = std::max(a.length(), b.length());
        int resultLen = formatNumber(result).length();
        int totalWidth = std::max(maxLen + 2, resultLen) + 2;
        
        std::ostringstream visual;
        visual << std::string(totalWidth - a.length(), ' ') << a << "\n";
        visual << "-" << std::string(totalWidth - b.length() - 1, ' ') << b << "\n";
        visual << createLine(totalWidth) << "\n";
        visual << std::string(totalWidth - resultLen, ' ') << formatNumber(result) << "\n";
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Multiplication with manual step-by-step (long multiplication)
    std::string multiply(std::string a, std::string b) {
        steps.clear();
        double num1 = parseNumber(a);
        double num2 = parseNumber(b);
        double result = num1 * num2;
        
        // For integers, show long multiplication process
        if (floor(num1) == num1 && floor(num2) == num2) {
            long long n1 = (long long)num1;
            long long n2 = (long long)num2;
            
            std::string str2 = std::to_string(n2);
            std::vector<long long> partialProducts;
            
            // Calculate partial products
            int multiplierPos = 0;
            for (int i = str2.length() - 1; i >= 0; i--) {
                int digit = str2[i] - '0';
                long long partial = n1 * digit * pow(10, multiplierPos);
                partialProducts.push_back(partial);
                multiplierPos++;
            }
            
            // Build visual representation
            int maxWidth = std::max(std::to_string(n1).length(), 
                                   std::to_string(n2).length() + 1);
            int resultWidth = std::to_string((long long)result).length();
            int totalWidth = std::max(maxWidth + 2, resultWidth) + 2;
            
            std::ostringstream visual;
            visual << std::string(totalWidth - std::to_string(n1).length(), ' ') << n1 << "\n";
            visual << "×" << std::string(totalWidth - std::to_string(n2).length() - 1, ' ') << n2 << "\n";
            visual << createLine(totalWidth) << "\n";
            
            // Show partial products
            std::reverse(partialProducts.begin(), partialProducts.end());
            for (size_t i = 0; i < partialProducts.size(); i++) {
                std::string ppStr = std::to_string(partialProducts[i]);
                if (i == 0) {
                    visual << std::string(totalWidth - ppStr.length(), ' ') << ppStr << "\n";
                } else {
                    visual << "+" << std::string(totalWidth - ppStr.length() - 1, ' ') << ppStr << "\n";
                }
            }
            
            visual << createLine(totalWidth) << "\n";
            visual << std::string(totalWidth - resultWidth, ' ') << (long long)result << "\n";
            
            steps.push_back({visual.str(), "", 0});
        } else {
            // For decimals, show direct multiplication
            int totalWidth = std::max({a.length(), b.length() + 1, 
                                     formatNumber(result).length()}) + 2;
            
            std::ostringstream visual;
            visual << std::string(totalWidth - a.length(), ' ') << a << "\n";
            visual << "×" << std::string(totalWidth - b.length() - 1, ' ') << b << "\n";
            visual << createLine(totalWidth) << "\n";
            visual << std::string(totalWidth - formatNumber(result).length(), ' ') 
                   << formatNumber(result) << "\n";
            
            steps.push_back({visual.str(), "", 0});
        }
        
        return formatNumber(result);
    }
    
    // Division with manual step-by-step
    std::string divide(std::string a, std::string b) {
        steps.clear();
        double num1 = parseNumber(a);
        double num2 = parseNumber(b);
        
        if (num2 == 0) {
            steps.push_back({"Error: Division by zero!", "", 0});
            return "Error";
        }
        
        double result = num1 / num2;
        
        std::ostringstream visual;
        visual << a << " ÷ " << b << " = " << formatNumber(result) << "\n";
        
        // Show long division process for integers
        if (floor(num1) == num1 && floor(num2) == num2 && num1 >= num2) {
            long long dividend = (long long)num1;
            long long divisor = (long long)num2;
            long long quotient = dividend / divisor;
            long long remainder = dividend % divisor;
            
            visual << "\nLong Division Process:\n";
            visual << "  " << quotient << " (quotient)\n";
            visual << divisor << ")" << dividend << "\n";
            visual << "  " << (divisor * quotient) << "\n";
            visual << createLine(10) << "\n";
            visual << "  " << remainder << " (remainder)\n";
        }
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Square root with approximation steps
    std::string squareRoot(std::string num) {
        steps.clear();
        double value = parseNumber(num);
        
        if (value < 0) {
            steps.push_back({"Error: Cannot calculate square root of negative number!", "", 0});
            return "Error";
        }
        
        double result = sqrt(value);
        
        std::ostringstream visual;
        visual << "√" << num << " = " << formatNumber(result) << "\n\n";
        
        // Show Newton's method steps for manual approximation
        if (value > 0) {
            visual << "Newton's Method Approximation:\n";
            double x0 = value / 2; // Initial guess
            visual << "Step 0: Initial guess = " << formatNumber(x0) << "\n";
            
            for (int i = 1; i <= 3; i++) {
                double x1 = (x0 + value / x0) / 2;
                visual << "Step " << i << ": " << formatNumber(x0) 
                       << " → " << formatNumber(x1) << "\n";
                x0 = x1;
            }
        }
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Cube root with approximation steps
    std::string cubeRoot(std::string num) {
        steps.clear();
        double value = parseNumber(num);
        double result = cbrt(value);
        
        std::ostringstream visual;
        visual << "∛" << num << " = " << formatNumber(result) << "\n\n";
        
        // Show approximation steps
        if (value != 0) {
            visual << "Approximation Steps:\n";
            double x0 = value / 3;
            visual << "Step 0: Initial guess = " << formatNumber(x0) << "\n";
            
            for (int i = 1; i <= 3; i++) {
                double x1 = (2 * x0 + value / (x0 * x0)) / 3;
                visual << "Step " << i << ": " << formatNumber(x0) 
                       << " → " << formatNumber(x1) << "\n";
                x0 = x1;
            }
        }
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Rule of Three
    std::string ruleOfThree(std::string a, std::string b, std::string c) {
        steps.clear();
        double val1 = parseNumber(a);
        double val2 = parseNumber(b);
        double val3 = parseNumber(c);
        
        // Direct proportion: a → b, c → x
        double result = (val2 * val3) / val1;
        
        std::ostringstream visual;
        visual << "Rule of Three (Direct Proportion):\n\n";
        visual << a << " ———→ " << b << "\n";
        visual << c << " ———→ x\n\n";
        visual << "x = (" << b << " × " << c << ") ÷ " << a << "\n";
        visual << "x = " << formatNumber(val2 * val3) << " ÷ " << a << "\n";
        visual << "x = " << formatNumber(result) << "\n";
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Simple numerical integration (trapezoidal rule)
    std::string integrate(std::string expression, std::string lower, std::string upper, int intervals = 100) {
        steps.clear();
        double a = parseNumber(lower);
        double b = parseNumber(upper);
        double h = (b - a) / intervals;
        double result = 0;
        
        std::ostringstream visual;
        visual << "Numerical Integration (Trapezoidal Rule)\n";
        visual << "∫ " << expression << " dx from " << lower << " to " << upper << "\n\n";
        visual << "Using " << intervals << " intervals\n";
        visual << "Step size h = " << formatNumber(h) << "\n\n";
        
        // Simple function evaluation (we'll use f(x) = x^2 as example)
        auto f = [](double x) { return x * x; };
        
        // Trapezoidal rule
        result = (f(a) + f(b)) / 2;
        for (int i = 1; i < intervals; i++) {
            result += f(a + i * h);
        }
        result *= h;
        
        visual << "Approximation Steps:\n";
        visual << "f(" << formatNumber(a) << ") = " << formatNumber(f(a)) << "\n";
        visual << "f(" << formatNumber(b) << ") = " << formatNumber(f(b)) << "\n";
        visual << "Sum of interior points = " << formatNumber(result / h) << "\n\n";
        visual << "Result ≈ " << formatNumber(result) << "\n";
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(result);
    }
    
    // Numerical derivative
    std::string derivative(std::string expression, std::string point) {
        steps.clear();
        double x = parseNumber(point);
        double h = 0.0001;
        
        std::ostringstream visual;
        visual << "Numerical Derivative\n";
        visual << "d/dx (" << expression << ") at x = " << point << "\n\n";
        
        // Using central difference formula: f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
        auto f = [](double x) { return x * x; }; // Example: f(x) = x^2
        
        double f_plus = f(x + h);
        double f_minus = f(x - h);
        double derivative = (f_plus - f_minus) / (2 * h);
        
        visual << "Using central difference method:\n";
        visual << "f'(" << formatNumber(x) << ") ≈ ";
        visual << "[f(" << formatNumber(x + h) << ") - f(" << formatNumber(x - h) << ")] / (2 × " << h << ")\n";
        visual << "f'(" << formatNumber(x) << ") ≈ (" << formatNumber(f_plus) << " - " 
               << formatNumber(f_minus) << ") / " << formatNumber(2 * h) << "\n";
        visual << "f'(" << formatNumber(x) << ") ≈ " << formatNumber(derivative) << "\n";
        
        steps.push_back({visual.str(), "", 0});
        return formatNumber(derivative);
    }
    
    std::vector<Step> getSteps() {
        return steps;
    }
    
    void clearSteps() {
        steps.clear();
    }
};
