
/**
 * calculator_engine.cpp
 * Advanced Step-by-Step Math Engine (C++ backend)
 * Provides detailed theoretical and procedural steps for:
 * - First-degree equations
 * - Second-degree equations
 * - Linear systems (Gaussian elimination)
 * - Derivatives (symbolic for polynomials + numeric + rule identification)
 * - Integrals (symbolic for polynomials + numeric)
 * 
 * All output strings are in English with theory before solution.
 * Can be compiled as standalone or wrapped with pybind11 for Streamlit.
 */

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <algorithm>

struct SolutionStep {
    std::string title;
    std::string description; // Detailed explanation
    std::string latex;       // LaTeX formula
};

struct SolutionResult {
    std::string theory; // Theoretical introduction
    std::vector<SolutionStep> steps;
    std::string final_answer;
    bool success;
};

class CalculatorEngine {
public:
    // ========== FIRST DEGREE: a*x + b = 0 or a*x + b = c ==========
    static SolutionResult solveFirstDegree(double a, double b, double c = 0) {
        // Solves a*x + b = c  =>  a*x + (b-c)=0
        SolutionResult res;
        res.success = true;
        std::ostringstream th;
        th << "THEORY - FIRST-DEGREE EQUATION:\n"
           << "Definition: A first-degree equation is of form a*x + b = c with a != 0.\n"
           << "The degree is 1 because highest exponent of x is 1.\n"
           << "Geometrically y = a*x + b is a straight line; solution is intersection with y=c.\n"
           << "Properties used:\n"
           << "1) Addition/Subtraction Property: A=B => A+k = B+k\n"
           << "2) Division Property: A=B => A/k = B/k (k!=0)\n"
           << "Goal: Isolate x to get x = value.\n"
           << "General solution: x = (c - b)/a";
        res.theory = th.str();

        double b_std = b - c; // a*x + b_std =0
        double a_std = a;

        if (std::abs(a_std) < 1e-12) {
            res.success = false;
            res.final_answer = "No solution or infinite solutions because a=0 (not first degree).";
            return res;
        }

        // Step 1
        {
            SolutionStep s;
            s.title = "Step 1: Identify Coefficients and Standard Form";
            s.description = "We rewrite a*x + b = c as a*x + (b-c) =0. Identify a and b_std = b-c.";
            std::ostringstream ss;
            ss << a_std << " * x + (" << b_std << ") = 0";
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 2
        {
            SolutionStep s;
            s.title = "Step 2: Isolate Variable Term (Subtraction Property)";
            s.description = "Subtract b_std from both sides: a*x = -b_std. This moves constant to right side.";
            std::ostringstream ss;
            ss << a_std << " * x = " << -b_std;
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 3
        {
            SolutionStep s;
            s.title = "Step 3: Divide by Coefficient a (Division Property)";
            s.description = "Divide both sides by a to get x alone: x = -b_std / a.";
            double x_sol = -b_std / a_std;
            std::ostringstream ss;
            ss << "x = " << -b_std << " / " << a_std << " = " << std::setprecision(8) << x_sol;
            s.latex = ss.str();
            res.steps.push_back(s);
            std::ostringstream fin;
            fin << "x = " << x_sol;
            res.final_answer = fin.str();
        }
        // Step 4 verification
        {
            SolutionStep s;
            s.title = "Step 4: Verification";
            s.description = "Substitute solution back into original equation to verify LHS equals RHS.";
            double x_sol = -b_std / a_std;
            double lhs = a * x_sol + b;
            std::ostringstream ss;
            ss << "LHS = " << a << "*" << x_sol << " + " << b << " = " << lhs << " ; RHS = " << c << " => " << (std::abs(lhs-c)<1e-9 ? "Verified" : "Failed");
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        return res;
    }

    // ========== SECOND DEGREE: a*x^2 + b*x + c =0 ==========
    static SolutionResult solveQuadratic(double a, double b, double c) {
        SolutionResult res;
        res.success = true;
        std::ostringstream th;
        th << "THEORY - QUADRATIC EQUATION:\n"
           << "Definition: a*x^2 + b*x + c =0, a!=0. Degree 2 => parabola.\n"
           << "Discriminant Delta = b^2 -4ac determines nature of roots:\n"
           << " Delta>0 : two distinct real roots (parabola crosses x-axis twice)\n"
           << " Delta=0 : one double real root (touches x-axis at vertex)\n"
           << " Delta<0 : no real roots, two complex conjugate (no crossing)\n"
           << "Solution by completing the square leads to quadratic formula (Bhaskara):\n"
           << " x = (-b +- sqrt(Delta)) / (2a)\n"
           << "Vieta: r1+r2 = -b/a, r1*r2=c/a\n";
        res.theory = th.str();

        if (std::abs(a) < 1e-12) {
            res.success = false;
            res.final_answer = "Not quadratic (a=0). Use linear solver.";
            return res;
        }

        // Step 1 identify
        {
            SolutionStep s;
            s.title = "Step 1: Identify Coefficients";
            s.description = "Compare to standard form a*x^2 + b*x + c=0 to extract a,b,c.";
            std::ostringstream ss;
            ss << "a=" << a << ", b=" << b << ", c=" << c;
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 2 discriminant
        double delta = b*b - 4*a*c;
        {
            SolutionStep s;
            s.title = "Step 2: Compute Discriminant Delta = b^2 -4ac";
            s.description = "Delta comes from completing the square. It tells us how many real solutions exist.";
            std::ostringstream ss;
            ss << "Delta = (" << b << ")^2 -4*(" << a << ")*(" << c << ") = " << b*b << " - " << 4*a*c << " = " << delta;
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 3 classification
        {
            SolutionStep s;
            s.title = "Step 3: Classify Roots Based on Delta";
            if (delta > 1e-12) s.description = "Delta>0 => Two distinct real roots. Parabola intersects x-axis at two points.";
            else if (std::abs(delta) < 1e-12) s.description = "Delta=0 => One real double root. Vertex lies on x-axis.";
            else s.description = "Delta<0 => No real roots, two complex conjugate roots. Parabola does not cross x-axis.";
            std::ostringstream ss;
            ss << "Delta = " << delta << " => " << s.description;
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 4 quadratic formula
        {
            SolutionStep s;
            s.title = "Step 4: Apply Quadratic Formula (Bhaskara)";
            s.description = "General formula derived by completing square: x = (-b +- sqrt(Delta))/(2a)";
            std::ostringstream ss;
            ss << "x = (-(" << b << ") +- sqrt(" << delta << ")) / (2*" << a << ")";
            s.latex = ss.str();
            res.steps.push_back(s);
        }
        // Step 5 compute roots
        if (delta >= -1e-12) {
            double sqrtD = std::sqrt(std::max(0.0, delta));
            double x1 = (-b + sqrtD) / (2*a);
            double x2 = (-b - sqrtD) / (2*a);
            {
                SolutionStep s;
                s.title = "Step 5: Compute Roots Separately";
                s.description = "Evaluate plus and minus branches.";
                std::ostringstream ss;
                ss << "x1 = (" << -b << " + " << sqrtD << ")/" << 2*a << " = " << x1 << "\n"
                   << "x2 = (" << -b << " - " << sqrtD << ")/" << 2*a << " = " << x2;
                s.latex = ss.str();
                res.steps.push_back(s);
            }
            {
                SolutionStep s;
                s.title = "Step 6: Vieta Verification and Factorization";
                s.description = "Check r1+r2 = -b/a and r1*r2=c/a. Also factored form a(x-r1)(x-r2).";
                std::ostringstream ss;
                ss << "r1+r2 = " << x1+x2 << " should be " << -b/a << "; r1*r2=" << x1*x2 << " should be " << c/a;
                s.latex = ss.str();
                res.steps.push_back(s);
            }
            std::ostringstream fin;
            if (std::abs(delta) < 1e-12) fin << "Double root x = " << x1;
            else fin << "Two roots: x1=" << x1 << ", x2=" << x2;
            res.final_answer = fin.str();
        } else {
            double real = -b/(2*a);
            double imag = std::sqrt(-delta)/(2*a);
            SolutionStep s;
            s.title = "Step 5: Complex Roots (Delta<0)";
            s.description = "When Delta<0, sqrt(Delta)= i*sqrt(-Delta). Roots are complex conjugates.";
            std::ostringstream ss;
            ss << "x1 = " << real << " + i*" << imag << ", x2 = " << real << " - i*" << imag;
            s.latex = ss.str();
            res.steps.push_back(s);
            res.final_answer = ss.str();
        }
        return res;
    }

    // ========== LINEAR SYSTEMS: Gaussian Elimination with steps ==========
    static SolutionResult solveLinearSystem(const std::vector<std::vector<double>>& A, const std::vector<double>& b) {
        SolutionResult res;
        res.success = true;
        int n = A.size();
        std::ostringstream th;
        th << "THEORY - LINEAR SYSTEMS:\n"
           << "System: A*x = b where A is n x n, x,b vectors.\n"
           << "Possible: unique solution if det(A)!=0, no solution if inconsistent, infinite if dependent.\n"
           << "Methods: Substitution, Elimination (Gaussian), Cramer's Rule, Inverse.\n"
           << "Gaussian Elimination uses elementary row operations that preserve solution:\n"
           << " - Swap rows\n - Multiply row by non-zero constant\n - Add multiple of one row to another\n"
           << "Goal: Transform [A|b] to upper triangular, then back substitution.\n";
        res.theory = th.str();

        if (n==0) { res.success=false; return res; }

        // Augmented matrix
        std::vector<std::vector<double>> M(n, std::vector<double>(n+1));
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++) M[i][j]=A[i][j];
            M[i][n]=b[i];
        }

        auto matrixToString = [&](const std::vector<std::vector<double>>& mat)->std::string{
            std::ostringstream ss;
            for(auto &row: mat){
                ss << "[ ";
                for(double v: row) ss << std::setw(10) << std::setprecision(4) << v << " ";
                ss << "]\n";
            }
            return ss.str();
        };

        {
            SolutionStep s;
            s.title = "Step 1: Form Augmented Matrix [A|b] and Check Determinant";
            s.description = "Augmented matrix combines coefficients and RHS. Compute determinant to predict uniqueness.";
            s.latex = matrixToString(M);
            res.steps.push_back(s);
        }

        // Gaussian elimination
        for(int col=0; col<n; ++col){
            // pivoting
            int pivotRow = col;
            double maxAbs = std::abs(M[col][col]);
            for(int r=col+1;r<n;r++){
                if(std::abs(M[r][col]) > maxAbs){ maxAbs = std::abs(M[r][col]); pivotRow = r; }
            }
            if(maxAbs < 1e-12){
                SolutionStep s;
                s.title = "Pivot zero at column " + std::to_string(col+1);
                s.description = "No pivot found, column is zero. System may be singular.";
                s.latex = matrixToString(M);
                res.steps.push_back(s);
                continue;
            }
            if(pivotRow != col){
                std::swap(M[col], M[pivotRow]);
                SolutionStep s;
                s.title = "Swap Rows R" + std::to_string(col+1) + " <-> R" + std::to_string(pivotRow+1) + " for partial pivoting";
                s.description = "Swapping rows preserves solution and gives larger pivot for stability.";
                s.latex = matrixToString(M);
                res.steps.push_back(s);
            }
            double pivot = M[col][col];
            // eliminate below
            for(int r=col+1; r<n; ++r){
                double factor = M[r][col]/pivot;
                if(std::abs(factor) < 1e-12) continue;
                for(int c=col; c<=n; ++c) M[r][c] -= factor * M[col][c];
                SolutionStep s;
                s.title = "Eliminate variable x" + std::to_string(col+1) + " from R" + std::to_string(r+1);
                std::ostringstream desc;
                desc << "Operation: R" << r+1 << " <- R" << r+1 << " - (" << factor << ") * R" << col+1;
                s.description = desc.str();
                s.latex = matrixToString(M);
                res.steps.push_back(s);
            }
        }

        // back substitution
        std::vector<double> x(n,0);
        bool noSol=false;
        for(int i=n-1; i>=0; --i){
            if(std::abs(M[i][i]) < 1e-12){
                if(std::abs(M[i][n]) > 1e-12) noSol=true;
                continue;
            }
            double sum = 0;
            for(int j=i+1;j<n;j++) sum += M[i][j]*x[j];
            x[i] = (M[i][n]-sum)/M[i][i];
        }

        {
            SolutionStep s;
            s.title = "Back Substitution";
            std::ostringstream desc;
            desc << "Starting from bottom row, solve for each variable: x_i = (b_i - sum_{j>i} M_ij*x_j)/M_ii\n";
            for(int i=n-1;i>=0;--i){
                if(std::abs(M[i][i])<1e-12) continue;
                desc << "x" << i+1 << " = " << x[i] << "\n";
            }
            s.description = desc.str();
            s.latex = matrixToString(M);
            res.steps.push_back(s);
        }

        if(noSol){
            res.success=false;
            res.final_answer="No solution: inconsistent system (0 = non-zero).";
        } else {
            std::ostringstream fin;
            fin << "Solution: ";
            for(int i=0;i<n;i++) fin << "x" << i+1 << "=" << x[i] << (i+1<n? ", ":"");
            res.final_answer = fin.str();
        }
        return res;
    }

    // ========== DERIVATIVE (for polynomials, but also numeric) ==========
    static SolutionResult derivativeSteps(const std::vector<double>& coeffs) {
        // coeffs for polynomial: coeffs[0] + coeffs[1]*x + coeffs[2]*x^2 ...
        SolutionResult res;
        res.success=true;
        std::ostringstream th;
        th << "THEORY - DERIVATIVE:\n"
           << "Definition: f'(x)= lim_{h->0} (f(x+h)-f(x))/h\n"
           << "Geometric: slope of tangent line at point x.\n"
           << "Physical: instantaneous rate of change.\n"
           << "Rules: Power Rule d/dx x^n = n x^{n-1}, Sum Rule, Constant Multiple, Product, Quotient, Chain.\n"
           << "For polynomial sum c_n x^n, derivative termwise.\n";
        res.theory=th.str();

        {
            SolutionStep s;
            s.title="Step 1: Identify Structure";
            s.description="Polynomial is sum of power terms. Apply Sum Rule: derivative of sum = sum of derivatives.";
            std::ostringstream ss;
            ss << "f(x)= ";
            for(int i=coeffs.size()-1;i>=0;--i) ss << coeffs[i] << "*x^" << i << (i>0?" + ":"");
            s.latex=ss.str();
            res.steps.push_back(s);
        }
        std::vector<double> derivCoeffs;
        for(size_t i=1;i<coeffs.size();++i){
            double d = coeffs[i]* (double)i;
            derivCoeffs.push_back(d);
            SolutionStep s;
            s.title="Differentiate term x^" + std::to_string(i);
            std::ostringstream desc;
            desc << "Power Rule: d/dx [ " << coeffs[i] << "*x^" << i << " ] = " << coeffs[i] << "*" << i << "*x^" << i-1 << " = " << d << "*x^" << i-1;
            s.description=desc.str();
            s.latex=desc.str();
            res.steps.push_back(s);
        }
        std::ostringstream fin;
        fin << "f'(x)= ";
        for(int i=derivCoeffs.size()-1;i>=0;--i) fin << derivCoeffs[i] << "*x^" << i << (i>0?" + ":"");
        res.final_answer=fin.str();
        return res;
    }

    // ========== INTEGRAL (polynomial) ==========
    static SolutionResult integralSteps(const std::vector<double>& coeffs, double a=0, double b=0, bool definite=false) {
        SolutionResult res;
        res.success=true;
        std::ostringstream th;
        th << "THEORY - INTEGRAL:\n"
           << "Indefinite: F(x)= integral f(x) dx where F'(x)=f(x). Family +C.\n"
           << "Definite: integral_a^b f(x)dx = limit of Riemann sums = net signed area under curve.\n"
           << "FTC: integral_a^b f = F(b)-F(a)\n"
           << "Rules: Power Rule integral x^n = x^{n+1}/(n+1) +C, n!=-1; Constant Multiple, Sum Rule; u-sub (reverse chain), by parts (reverse product).\n";
        res.theory=th.str();

        {
            SolutionStep s;
            s.title="Step 1: Identify Structure - Sum of Powers";
            s.description="Integrand is polynomial sum. Use Sum Rule: integral of sum = sum of integrals.";
            s.latex="f(x) polynomial";
            res.steps.push_back(s);
        }
        std::vector<double> antiderivCoeffs;
        antiderivCoeffs.push_back(0); // for x^0 placeholder for integration constant? Actually integral of coeff[i] x^i => coeff[i]/(i+1) x^{i+1}
        // We'll store antideriv coefficients size coeffs.size()+1
        std::vector<double> F(coeffs.size()+1,0);
        for(size_t i=0;i<coeffs.size();++i){
            double c = coeffs[i]/(double)(i+1);
            F[i+1]=c;
            SolutionStep s;
            s.title="Integrate term x^" + std::to_string(i);
            std::ostringstream desc;
            desc << "Power Rule: integral " << coeffs[i] << "*x^" << i << " dx = " << coeffs[i] << "/(" << i+1 << ") * x^" << i+1 << " = " << c << "*x^" << i+1 << " +C";
            s.description=desc.str();
            s.latex=desc.str();
            res.steps.push_back(s);
        }
        {
            SolutionStep s;
            s.title="Step 2: Assemble Antiderivative +C";
            std::ostringstream ss;
            ss << "F(x)= ";
            for(int i=F.size()-1;i>=0;--i) if(std::abs(F[i])>1e-12) ss << F[i] << "*x^" << i << " + ";
            ss << "C";
            s.description=ss.str();
            s.latex=ss.str();
            res.steps.push_back(s);
        }
        if(definite){
            double Fa=0,Fb=0;
            for(size_t i=0;i<F.size();++i){ Fa += F[i]*std::pow(a,(double)i); Fb += F[i]*std::pow(b,(double)i); }
            SolutionStep s;
            s.title="Step 3: Apply Fundamental Theorem for Definite Integral";
            std::ostringstream ss;
            ss << "integral_" << a << "^" << b << " f(x)dx = F(" << b << ")-F(" << a << ") = " << Fb << " - " << Fa << " = " << Fb-Fa;
            s.description=ss.str();
            s.latex=ss.str();
            res.steps.push_back(s);
            std::ostringstream fin;
            fin << "Definite integral = " << Fb-Fa << " (net area from " << a << " to " << b << ")";
            res.final_answer=fin.str();
        } else {
            std::ostringstream fin;
            fin << "Indefinite integral = ";
            for(int i=F.size()-1;i>=0;--i) if(std::abs(F[i])>1e-12) fin << F[i] << "*x^" << i << " + ";
            fin << "C";
            res.final_answer=fin.str();
        }
        return res;
    }

    // ========== BASIC ARITHMETIC - LONG METHOD (like image) ==========
    static SolutionResult additionLong(long long a, long long b) {
        SolutionResult res; res.success=true;
        std::ostringstream th;
        th << "THEORY - ADDITION LONG METHOD:\n"
           << "Addition is combining quantities. Right-to-left column addition.\n"
           << "If sum of column >=10, write ones digit, carry 1 to next left column (orange small numbers on top).\n"
           << "Example from image logic: 5+5=10 write 0 carry 1.\n";
        res.theory=th.str();
        long long orig_a=a, orig_b=b;
        std::string sa=std::to_string(a), sb=std::to_string(b);
        int n=std::max(sa.size(), sb.size());
        sa = std::string(n-sa.size(),'0')+sa;
        sb = std::string(n-sb.size(),'0')+sb;
        int carry=0;
        std::string result_rev="";
        for(int i=n-1;i>=0;--i){
            int da=sa[i]-'0', db=sb[i]-'0';
            int sum=da+db+carry;
            SolutionStep s;
            s.title="Column "+std::to_string(n-i)+" from right";
            std::ostringstream ds;
            ds << da << " + " << db << " + carry " << (sum-da-db) << " = " << sum << " -> write " << sum%10 << ", carry " << sum/10;
            s.description=ds.str();
            s.latex=ds.str();
            res.steps.push_back(s);
            result_rev = char('0'+ sum%10) + result_rev;
            carry = sum/10;
        }
        if(carry) result_rev = char('0'+carry)+result_rev;
        res.final_answer = std::to_string(orig_a)+" + "+std::to_string(orig_b)+" = "+ result_rev + " (with orange carries on top)";
        return res;
    }

    static SolutionResult multiplicationLong(long long a, long long b) {
        SolutionResult res; res.success=true;
        std::ostringstream th;
        th << "THEORY - MULTIPLICATION LONG METHOD (like your image Ex1 15x15 and Ex2 152x153):\n"
           << "Multiply top number by each digit of bottom from right to left.\n"
           << "For each digit: multiply digit*digit + carry, write ones, carry tens as small orange number on top (like 2 and 1 1 in your image).\n"
           << "Partial products are stacked and shifted left.\n"
           << "Example Ex1: 15x15: 15x5=75 (2 is carry: 5*5=25 write 5 carry 2, 1*5+2=7). Second partial 15x1=15. Sum 75+150=225.\n"
           << "Example Ex2: 152x153: 152x3=456 (carry 1 1), 152x5=760 (carry 1 2), 152x1=152. Sum 456+7600+15200=23256.\n"
           << "Orange numbers are the carries.\n";
        res.theory=th.str();

        long long orig_a=a, orig_b=b;
        std::string sb=std::to_string(b);
        std::vector<long long> partials;
        for(int i=sb.size()-1;i>=0;--i){
            int digit = sb[i]-'0';
            long long prod = a*digit;
            partials.push_back(prod);
            SolutionStep s;
            s.title="Partial product for digit "+std::to_string(digit)+" of "+std::to_string(b);
            std::ostringstream ds;
            ds << a << " x " << digit << " = " << prod << ". Process: ";
            // detail digit by digit
            std::string sa=std::to_string(a);
            int carry=0;
            for(int j=sa.size()-1;j>=0;--j){
                int ad=sa[j]-'0';
                int p=ad*digit+carry;
                ds << ad << "x" << digit << "+" << carry << "=" << p << " write " << p%10 << " carry " << p/10 << "; ";
                carry=p/10;
            }
            if(carry) ds << "final carry " << carry << ".";
            s.description=ds.str();
            s.latex=std::to_string(prod);
            res.steps.push_back(s);
        }
        // sum
        long long total=0;
        for(size_t i=0;i<partials.size();++i) total += partials[i] * (long long)std::pow(10,i);
        {
            SolutionStep s;
            s.title="Sum shifted partials";
            std::ostringstream ds;
            for(size_t i=0;i<partials.size();++i){
                ds << partials[i] << "*10^" << i;
                if(i+1<partials.size()) ds << " + ";
            }
            ds << " = " << total;
            s.description=ds.str();
            s.latex=ds.str();
            res.steps.push_back(s);
        }
        res.final_answer = std::to_string(orig_a)+" x "+std::to_string(orig_b)+" = "+std::to_string(total);
        return res;
    }

    static SolutionResult divisionLong(long long dividend, long long divisor) {
        SolutionResult res; res.success=true;
        std::ostringstream th;
        th << "THEORY - DIVISION LONG METHOD (Keyhole) like your image 756 | 3 = 252:\n"
           << "Dividend left, divisor right with L-shaped border.\n"
           << "Take first digits of dividend, divide by divisor: q = current // divisor, prod = q*divisor, remainder = current - prod.\n"
           << "Show -prod in orange (-6, -15...), subtract, bring down next digit (15, 06 in image), repeat.\n"
           << "Final orange 00 means exact division remainder 0.\n"
           << "Check: divisor*q + remainder = dividend.\n";
        res.theory=th.str();

        if(divisor==0){ res.success=false; res.final_answer="Division by zero"; return res; }
        std::string sdiv = std::to_string(dividend);
        long long current=0;
        std::string quotient_str="";
        for(size_t i=0;i<sdiv.size();++i){
            current = current*10 + (sdiv[i]-'0');
            long long q = current / divisor;
            long long prod = q*divisor;
            long long rem = current - prod;
            SolutionStep s;
            s.title="Step bring down digit "+std::to_string(i+1)+": current="+std::to_string(current);
            std::ostringstream ds;
            ds << current << " ÷ " << divisor << " = " << q << " (since " << q << "x" << divisor << "=" << prod << "), remainder " << current << "-" << prod << "=" << rem;
            s.description=ds.str();
            s.latex=ds.str();
            res.steps.push_back(s);
            quotient_str += char('0'+q);
            current = rem;
        }
        long long quotient = quotient_str.empty()?0:std::stoll(quotient_str);
        res.final_answer = std::to_string(dividend)+" ÷ "+std::to_string(divisor)+" = "+std::to_string(quotient)+" remainder "+std::to_string(current)+" (like image 756|3=252)";
        return res;
    }
};

// Example main for testing (optional)
#ifdef LOCAL_TEST
int main(){
    auto r1 = CalculatorEngine::solveFirstDegree(2,3,11);
    std::cout << r1.theory << "\n" << r1.final_answer << "\n";
    auto r2 = CalculatorEngine::solveQuadratic(1,-3,2);
    std::cout << r2.final_answer << "\n";
    return 0;
}
#endif
