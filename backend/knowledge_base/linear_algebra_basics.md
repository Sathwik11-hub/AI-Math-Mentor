# Linear Algebra Basics

## Vectors

### Vector Operations
- Addition: (a₁, a₂) + (b₁, b₂) = (a₁+b₁, a₂+b₂)
- Scalar Multiplication: k(a₁, a₂) = (ka₁, ka₂)
- Dot Product: a·b = a₁b₁ + a₂b₂ + ... + aₙbₙ

### Vector Properties
- Magnitude: |v| = √(v₁² + v₂² + ... + vₙ²)
- Unit Vector: v̂ = v/|v|
- Angle between vectors: cos θ = (a·b)/(|a||b|)

### Orthogonality
Vectors a and b are orthogonal if a·b = 0

## Matrices

### Matrix Operations
- Addition: Add corresponding elements
- Scalar Multiplication: Multiply each element by scalar
- Matrix Multiplication: (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ

### Properties
- (AB)C = A(BC) - Associative
- A(B+C) = AB + AC - Distributive
- Generally AB ≠ BA - Not commutative

### Transpose
(A^T)ᵢⱼ = Aⱼᵢ
Properties:
- (A^T)^T = A
- (AB)^T = B^T A^T

## Determinants

### 2×2 Matrix
|A| = ad - bc for A = [[a,b],[c,d]]

### 3×3 Matrix (Sarrus Rule or Cofactor Expansion)
For expansion along first row:
|A| = a₁₁C₁₁ + a₁₂C₁₂ + a₁₃C₁₃

### Properties
- |AB| = |A||B|
- |A^T| = |A|
- If |A| = 0, matrix is singular (non-invertible)

## System of Linear Equations

### Matrix Form
Ax = b

### Solution Methods
1. Gaussian Elimination
2. Matrix Inversion: x = A⁻¹b (if A is invertible)
3. Cramer's Rule (for small systems)

### Inverse Matrix
AA⁻¹ = A⁻¹A = I
For 2×2: A⁻¹ = (1/|A|) [[d,-b],[-c,a]]

## Linear Independence

### Definition
Vectors v₁, v₂, ..., vₙ are linearly independent if:
c₁v₁ + c₂v₂ + ... + cₙvₙ = 0 only when all cᵢ = 0

## Common Mistakes
- Incorrect matrix multiplication order
- Forgetting that matrix multiplication is not commutative
- Sign errors in determinant calculation
- Division by zero when determinant is zero
- Incorrect transpose calculation

## Domain Constraints
- Matrix multiplication: columns of A must equal rows of B
- Inverse exists only if determinant ≠ 0
- Vector dot product requires same dimensions
