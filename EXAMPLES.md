# Example Problems for Testing AI Math Mentor

Test the system with these sample problems across different topics.

## Algebra Problems

### 1. Simple Quadratic Equation
**Problem:** Solve x² + 5x + 6 = 0

**Expected Output:**
- Topic: algebra
- Method: Factoring or quadratic formula
- Answer: x = -2 or x = -3

---

### 2. Quadratic with Discriminant
**Problem:** Find the roots of 2x² - 7x + 3 = 0

**Expected Output:**
- Topic: algebra
- Discriminant: D = 49 - 24 = 25
- Answer: x = 3 or x = 0.5

---

### 3. Linear System
**Problem:** Solve the system:
2x + 3y = 7
x - y = 1

**Expected Output:**
- Topic: algebra
- Method: Substitution or elimination
- Answer: x = 2, y = 1

---

## Calculus Problems

### 4. Basic Derivative
**Problem:** Find the derivative of f(x) = x³ + 2x² - 5x + 1

**Expected Output:**
- Topic: calculus
- Method: Power rule
- Answer: f'(x) = 3x² + 4x - 5

---

### 5. Chain Rule
**Problem:** Find the derivative of f(x) = sin(2x²)

**Expected Output:**
- Topic: calculus
- Method: Chain rule
- Answer: f'(x) = 4x·cos(2x²)

---

### 6. Limit Problem
**Problem:** Find lim(x→2) (x² - 4)/(x - 2)

**Expected Output:**
- Topic: calculus
- Method: Factoring or L'Hôpital's rule
- Answer: 4

---

### 7. Simple Optimization
**Problem:** Find the maximum value of f(x) = -x² + 4x + 1

**Expected Output:**
- Topic: calculus
- Critical point: x = 2
- Maximum value: f(2) = 5

---

## Probability Problems

### 8. Basic Probability
**Problem:** A fair die is rolled. What is the probability of getting an even number?

**Expected Output:**
- Topic: probability
- Favorable outcomes: {2, 4, 6} = 3
- Total outcomes: 6
- Answer: P = 3/6 = 1/2

---

### 9. Combinations
**Problem:** How many ways can you choose 3 students from a class of 10?

**Expected Output:**
- Topic: probability
- Method: Combinations C(10,3)
- Answer: 120

---

### 10. Conditional Probability
**Problem:** Two dice are rolled. What is the probability that the sum is 7?

**Expected Output:**
- Topic: probability
- Favorable outcomes: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6
- Total outcomes: 36
- Answer: P = 6/36 = 1/6

---

## Linear Algebra Problems

### 11. Matrix Multiplication
**Problem:** Multiply matrices A = [[1,2],[3,4]] and B = [[2,0],[1,3]]

**Expected Output:**
- Topic: linear_algebra
- Result: [[4,6],[10,12]]

---

### 12. Determinant
**Problem:** Find the determinant of matrix A = [[2,3],[1,4]]

**Expected Output:**
- Topic: linear_algebra
- Method: 2×2 determinant formula
- Answer: det(A) = 2(4) - 3(1) = 5

---

### 13. Vector Dot Product
**Problem:** Find the dot product of vectors a = (3, 4) and b = (2, -1)

**Expected Output:**
- Topic: linear_algebra
- Method: a·b = a₁b₁ + a₂b₂
- Answer: 3(2) + 4(-1) = 2

---

## OCR Test Problems (Image Input)

To test OCR, create images with these handwritten or typed problems:

1. "Solve: x² - 5x + 6 = 0"
2. "Find dy/dx if y = x³ + 2x"
3. "P(A∩B) if P(A)=0.5, P(B)=0.6, P(A∪B)=0.8"

---

## ASR Test Problems (Audio Input)

To test speech recognition, record these spoken problems:

1. "Solve x squared plus four x plus three equals zero"
2. "Find the derivative of x cubed"
3. "What is the probability of getting heads in a coin toss"

---

## Edge Cases to Test

### Problem with Constraints
**Problem:** Solve log(x + 2) = 1, where x is real

**Expected Behavior:**
- Parser should identify constraint: x > -2
- Verifier should check domain validity
- Answer: x = 8

---

### Ambiguous Problem
**Problem:** "Solve the equation"

**Expected Behavior:**
- Parser sets needs_clarification = true
- System requests more information
- HITL triggered

---

### Complex Problem (Should Trigger HITL)
**Problem:** "Find the integral of e^(x²) from 0 to infinity"

**Expected Behavior:**
- System may struggle (beyond basic calculus scope)
- Verifier confidence likely low
- HITL triggered for human review

---

## Testing HITL Features

### Low OCR Confidence Test
1. Upload a blurry or low-quality image
2. System should warn about low confidence
3. User should be able to edit extracted text

### Verification Failure Test
1. Submit a problem outside scope (e.g., advanced topology)
2. Verifier should have low confidence
3. HITL should be triggered

### Feedback Test
1. Solve any problem
2. Submit feedback with corrections
3. Check that feedback is stored in memory/

---

## Memory & Learning Tests

### Test Similar Problem Retrieval
1. Solve: x² + 5x + 6 = 0
2. Later solve: x² + 7x + 12 = 0
3. System should identify similar past problem
4. Check execution trace for "Memory Retrieval"

### Test OCR/ASR Correction Learning
1. Upload image with "x^2" misread as "x²2"
2. Correct it to "x²"
3. Upload similar image later
4. System should apply learned correction

---

## Performance Benchmarks

Expected response times (approximate):
- **Text input:** 10-20 seconds
- **Image input (OCR):** 20-30 seconds
- **Audio input (ASR):** 30-45 seconds

If slower:
- First run: Model downloads (1-2 minutes)
- Subsequent runs: Cached and faster

---

## Validation Checklist

After testing, verify:
- ✅ All 5 agents executed in trace
- ✅ RAG sources shown in UI
- ✅ Confidence scores displayed
- ✅ Step-by-step explanation provided
- ✅ HITL triggers when appropriate
- ✅ Feedback can be submitted
- ✅ Memory stores interactions
- ✅ Similar problems are found

---

## Troubleshooting Test Issues

### "No reliable reference found" in RAG
- **Cause:** Problem outside knowledge base scope
- **Expected:** System should say so explicitly
- **Not a bug:** Working as designed

### Solution seems incorrect
- **Action:** Submit feedback with correction
- **Purpose:** Tests feedback mechanism
- **Expected:** Feedback stored in memory/feedback.jsonl

### HITL triggered frequently
- **Cause:** Conservative confidence thresholds
- **Purpose:** Better safe than wrong
- **Adjustment:** Can lower thresholds in .env if needed
