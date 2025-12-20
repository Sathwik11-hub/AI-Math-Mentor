# Calculus Concepts - Limits, Derivatives, and Basic Optimization

## Limits

### Definition
lim(x→a) f(x) = L means f(x) approaches L as x approaches a

### Basic Limit Rules
1. lim(x→a) c = c (constant)
2. lim(x→a) x = a
3. lim(x→a) [f(x) + g(x)] = lim f(x) + lim g(x)
4. lim(x→a) [f(x) · g(x)] = lim f(x) · lim g(x)
5. lim(x→a) [f(x)/g(x)] = lim f(x) / lim g(x), if lim g(x) ≠ 0

### Indeterminate Forms
- 0/0, ∞/∞: Use L'Hôpital's Rule
- 0·∞: Rewrite as 0/0 or ∞/∞
- ∞-∞, 0⁰, 1^∞, ∞⁰: Transform appropriately

### L'Hôpital's Rule
If lim f(x)/g(x) gives 0/0 or ∞/∞:
lim(x→a) f(x)/g(x) = lim(x→a) f'(x)/g'(x)

## Derivatives

### Definition
f'(x) = lim(h→0) [f(x+h) - f(x)]/h

### Basic Derivative Rules
1. d/dx(c) = 0
2. d/dx(x^n) = nx^(n-1)
3. d/dx(e^x) = e^x
4. d/dx(ln x) = 1/x, x > 0
5. d/dx(sin x) = cos x
6. d/dx(cos x) = -sin x

### Chain Rule
If y = f(g(x)), then dy/dx = f'(g(x)) · g'(x)

### Product Rule
d/dx[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)

### Quotient Rule
d/dx[f(x)/g(x)] = [f'(x)g(x) - f(x)g'(x)] / [g(x)]²

## Optimization

### Critical Points
f'(x) = 0 or f'(x) does not exist

### First Derivative Test
- f'(x) changes from + to -: Local maximum
- f'(x) changes from - to +: Local minimum
- f'(x) does not change sign: Not an extremum

### Second Derivative Test
At critical point x = c:
- f''(c) > 0: Local minimum
- f''(c) < 0: Local maximum
- f''(c) = 0: Inconclusive

### Constraints
Domain constraints must be satisfied: x > 0 for ln(x), x ≥ 0 for √x

### Common Mistakes
- Forgetting to check domain restrictions
- Not verifying critical points are in valid domain
- Confusing maxima and minima
- Ignoring endpoint values in closed intervals
