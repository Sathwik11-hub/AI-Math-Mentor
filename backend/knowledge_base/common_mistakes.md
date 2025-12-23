# Common Mistakes in JEE Mathematics

## Algebra Mistakes

1. **Sign Errors in Quadratic Formula**
   - Forgetting negative sign: x = (-b ± √D)/(2a)
   - Incorrect: x = (b ± √D)/(2a)

2. **Inequality Sign Reversal**
   - Must reverse when multiplying/dividing by negative
   - Example: -2x > 4 → x < -2 (not x > -2)

3. **Exponent Rules**
   - (ab)ⁿ = aⁿbⁿ ✓
   - (a+b)ⁿ ≠ aⁿ + bⁿ ✗
   - a⁻ⁿ = 1/aⁿ (not -aⁿ)

4. **Factoring Errors**
   - x² - y² = (x+y)(x-y) ✓
   - x² + y² cannot be factored over reals

## Calculus Mistakes

1. **Domain Restrictions**
   - ln(x) requires x > 0
   - √x requires x ≥ 0
   - 1/x requires x ≠ 0
   - tan(x) undefined at x = π/2 + nπ

2. **Derivative of Composite Functions**
   - Must use chain rule
   - d/dx[f(g(x))] = f'(g(x))·g'(x)
   - Common error: d/dx[sin(x²)] ≠ cos(x²)
   - Correct: d/dx[sin(x²)] = cos(x²)·2x

3. **Critical Points**
   - Setting f'(x) = 0 finds candidates
   - Must verify they're maxima/minima
   - Don't forget endpoints in closed intervals

4. **L'Hôpital's Rule Misuse**
   - Only for 0/0 or ∞/∞ forms
   - Must differentiate numerator and denominator separately
   - lim f/g ≠ lim f'/g (incorrect)
   - lim f/g = lim (f'/g') (correct if 0/0 or ∞/∞)

## Probability Mistakes

1. **Independence Assumption**
   - Don't assume independence without verification
   - P(A∩B) = P(A)P(B) only if independent

2. **Conditional Probability Confusion**
   - P(A|B) ≠ P(B|A) in general
   - P(A|B) = P(A∩B)/P(B), not P(A)/P(B)

3. **Complement Errors**
   - P(at least one) = 1 - P(none)
   - P(exactly one) ≠ 1 - P(none)

4. **Permutation vs Combination**
   - Order matters → Permutation
   - Order doesn't matter → Combination

## Linear Algebra Mistakes

1. **Matrix Multiplication**
   - AB ≠ BA in general (not commutative)
   - Dimensions must be compatible: (m×n)(n×p) = (m×p)

2. **Determinant Properties**
   - det(AB) = det(A)det(B) ✓
   - det(A+B) ≠ det(A) + det(B) ✗

3. **Transpose Rules**
   - (AB)ᵀ = BᵀAᵀ (order reverses)
   - (AB)ᵀ ≠ AᵀBᵀ

4. **Zero Determinant**
   - If det(A) = 0, matrix is not invertible
   - System may have no solution or infinitely many

## General Mathematical Mistakes

1. **Square Root of Squares**
   - √(x²) = |x|, not x
   - √(a²+b²) ≠ a+b

2. **Fraction Operations**
   - 1/(a+b) ≠ 1/a + 1/b
   - a/(b+c) ≠ a/b + a/c

3. **Cancellation Errors**
   - Can only cancel common factors, not terms
   - (x+2)/(x+3) ≠ 2/3 (cannot cancel x)

4. **Verification**
   - Always substitute answer back into original equation
   - Check domain restrictions are satisfied
   - Verify extraneous solutions introduced by squaring
