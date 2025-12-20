# Probability Concepts and Formulas

## Basic Probability

### Definition
P(E) = Number of favorable outcomes / Total number of outcomes
Where 0 ≤ P(E) ≤ 1

### Complement Rule
P(E') = 1 - P(E)

### Addition Rule
- Mutually Exclusive: P(A ∪ B) = P(A) + P(B)
- General: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

### Multiplication Rule
- Independent Events: P(A ∩ B) = P(A) · P(B)
- Dependent Events: P(A ∩ B) = P(A) · P(B|A)

## Conditional Probability

### Definition
P(B|A) = P(A ∩ B) / P(A), where P(A) > 0

### Bayes' Theorem
P(A|B) = [P(B|A) · P(A)] / P(B)

## Distributions

### Binomial Distribution
P(X = k) = C(n,k) · p^k · (1-p)^(n-k)
- n trials, k successes, probability p
- Mean: μ = np
- Variance: σ² = np(1-p)

### Expected Value
E(X) = Σ x · P(x)
E(aX + b) = aE(X) + b

### Variance
Var(X) = E(X²) - [E(X)]²

## Permutations and Combinations

### Permutations
P(n, r) = n!/(n-r)!
Number of ways to arrange r items from n items (order matters)

### Combinations
C(n, r) = n!/(r!(n-r)!)
Number of ways to choose r items from n items (order doesn't matter)

### Properties
- C(n, r) = C(n, n-r)
- C(n, 0) = C(n, n) = 1
- C(n, 1) = n

## Common Mistakes
- Confusing permutations with combinations
- Forgetting that probabilities must sum to 1
- Not checking for independence before using multiplication rule
- Incorrect application of conditional probability
- Using P(A|B) when P(B|A) is needed (and vice versa)

## Problem-Solving Tips
1. Identify if events are independent or dependent
2. Draw probability trees for complex problems
3. Check if probabilities sum to 1
4. Verify answer is between 0 and 1
5. Consider complement when calculating "at least one" problems
