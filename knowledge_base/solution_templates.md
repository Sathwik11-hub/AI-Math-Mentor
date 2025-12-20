# Solution Templates for Common Problem Types

## Quadratic Equation Template

**Problem Type:** Solve ax² + bx + c = 0

**Step-by-Step Approach:**
1. Identify coefficients: a, b, c
2. Calculate discriminant: D = b² - 4ac
3. Check discriminant value:
   - D > 0: Two real distinct roots
   - D = 0: One repeated root
   - D < 0: Complex roots
4. Apply quadratic formula: x = (-b ± √D)/(2a)
5. Simplify and verify by substitution

**Example:**
Solve x² + 5x + 6 = 0
- a=1, b=5, c=6
- D = 25 - 24 = 1 > 0
- x = (-5 ± 1)/2
- x = -2 or x = -3
- Verify: (-2)² + 5(-2) + 6 = 0 ✓

## Limit Problem Template

**Problem Type:** Find lim(x→a) f(x)

**Step-by-Step Approach:**
1. Direct substitution: Try f(a)
2. If defined, that's the limit
3. If 0/0 or ∞/∞:
   - Try algebraic simplification
   - Try L'Hôpital's rule: lim f/g = lim f'/g'
4. If ∞-∞, 0·∞: Transform to 0/0 or ∞/∞
5. Verify limit from both sides if needed

**Example:**
lim(x→2) (x²-4)/(x-2)
- Direct: 0/0 (indeterminate)
- Factor: (x+2)(x-2)/(x-2) = x+2
- Limit: 2+2 = 4

## Derivative Problem Template

**Problem Type:** Find f'(x)

**Step-by-Step Approach:**
1. Identify function type
2. Apply appropriate rule:
   - Power rule: d/dx(xⁿ) = nxⁿ⁻¹
   - Product rule: (fg)' = f'g + fg'
   - Quotient rule: (f/g)' = (f'g-fg')/g²
   - Chain rule: [f(g(x))]' = f'(g(x))·g'(x)
3. Simplify result
4. Check domain restrictions

**Example:**
f(x) = x²sin(x)
- Product rule: f'(x) = 2x·sin(x) + x²·cos(x)
- Simplified: f'(x) = x(2sin(x) + x·cos(x))

## Probability Problem Template

**Problem Type:** Find P(Event)

**Step-by-Step Approach:**
1. Identify sample space
2. Count total outcomes
3. Identify favorable outcomes
4. Check if events are independent
5. Apply appropriate formula:
   - Basic: P(E) = favorable/total
   - Addition: P(A∪B) = P(A) + P(B) - P(A∩B)
   - Multiplication: P(A∩B) = P(A)·P(B|A)
6. Verify 0 ≤ P ≤ 1

**Example:**
Two dice rolled, find P(sum = 7)
- Sample space: 36 outcomes
- Favorable: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6
- P(sum=7) = 6/36 = 1/6

## Optimization Problem Template

**Problem Type:** Find maximum/minimum of f(x)

**Step-by-Step Approach:**
1. Find f'(x)
2. Set f'(x) = 0 to find critical points
3. Check domain restrictions
4. Apply first or second derivative test:
   - f''(x) > 0: minimum
   - f''(x) < 0: maximum
5. Check endpoints if closed interval
6. Verify answer satisfies constraints

**Example:**
Maximize f(x) = -x² + 4x + 1
- f'(x) = -2x + 4 = 0 → x = 2
- f''(x) = -2 < 0 → maximum at x = 2
- Maximum value: f(2) = -4 + 8 + 1 = 5

## Matrix Equation Template

**Problem Type:** Solve Ax = b

**Step-by-Step Approach:**
1. Write augmented matrix [A|b]
2. Check if det(A) ≠ 0
3. If invertible:
   - Find A⁻¹
   - Compute x = A⁻¹b
4. If not invertible:
   - Use Gaussian elimination
   - Check for no solution or infinitely many
5. Verify solution: Ax = b

**Example:**
[[2,1],[1,3]][x,y]ᵀ = [5,8]ᵀ
- det(A) = 6-1 = 5 ≠ 0
- A⁻¹ = (1/5)[[3,-1],[-1,2]]
- x = A⁻¹b = (1/5)[[3,-1],[-1,2]][[5],[8]]
- x = (1/5)[[7],[11]] = [7/5, 11/5]ᵀ
