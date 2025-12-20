# Testing Checklist for AI Math Mentor

Use this checklist to verify all system functionality before deployment.

## Pre-Testing Setup

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid `OPENAI_API_KEY`
- [ ] Validation script passes (`python validate.py`)
- [ ] Application launches successfully (`streamlit run app.py`)

## Core Functionality Tests

### 1. System Initialization
- [ ] System initializes without errors
- [ ] RAG pipeline creates vector store successfully
- [ ] Knowledge base documents loaded (6 files)
- [ ] Sidebar shows "System Ready" status

### 2. Text Input
- [ ] Can enter text in text area
- [ ] Simple problem solves successfully
  - Test: `Solve x² + 5x + 6 = 0`
  - Expected: x = -2 or x = -3
- [ ] Complex problem handled
  - Test: `Find derivative of x³ + 2x² - 5x + 1`
  - Expected: 3x² + 4x - 5
- [ ] Empty input handled gracefully
- [ ] Invalid input (non-math text) handled

### 3. Image Input (OCR)
- [ ] File upload widget appears
- [ ] Can upload PNG/JPG files
- [ ] Image displays correctly
- [ ] "Extract Text" button works
- [ ] Text extraction completes
- [ ] Confidence score displayed
- [ ] Low confidence triggers warning
- [ ] Extracted text can be edited
- [ ] Edited text can be solved

**Test Cases:**
- [ ] Clear, typed text image (high confidence)
- [ ] Handwritten problem (medium confidence)
- [ ] Blurry or low quality (low confidence, HITL trigger)

### 4. Audio Input (ASR)
- [ ] File upload widget appears
- [ ] Can upload audio files (WAV, MP3)
- [ ] Audio player displays
- [ ] "Transcribe Audio" button works
- [ ] Transcription completes
- [ ] Math phrase conversion works
  - "x squared" → x²
  - "square root of" → √
- [ ] Confidence score displayed
- [ ] Transcript can be edited

**Test Case:**
- [ ] Record: "Solve x squared plus five x plus six equals zero"
- [ ] Expected transcript: "Solve x² + 5x + 6 = 0" (or similar)

## Multi-Agent System Tests

### 5. Parser Agent
- [ ] Executes successfully
- [ ] Identifies correct topic (algebra/calculus/probability/linear_algebra)
- [ ] Extracts variables correctly
- [ ] Identifies constraints
- [ ] Extracts equations
- [ ] Returns confidence score
- [ ] Sets needs_clarification when appropriate
  - Test: "Solve the equation" (ambiguous)
  - Expected: needs_clarification = true

### 6. Intent Router Agent
- [ ] Executes successfully
- [ ] Selects appropriate strategy
- [ ] Lists required tools
- [ ] Provides approach description
- [ ] Returns confidence score

### 7. Solver Agent
- [ ] Executes successfully
- [ ] Provides step-by-step solution
- [ ] Shows intermediate reasoning
- [ ] Gives final answer
- [ ] Returns confidence score
- [ ] Uses SymPy when appropriate

### 8. Verifier Agent
- [ ] Executes successfully
- [ ] Checks mathematical correctness
- [ ] Validates domain constraints
- [ ] Identifies issues if present
- [ ] Returns confidence score
- [ ] Triggers HITL when confidence low
- [ ] Sets requires_hitl appropriately

### 9. Explainer Agent
- [ ] Executes successfully
- [ ] Provides clear explanation
- [ ] Lists key concepts
- [ ] Highlights common mistakes
- [ ] Offers helpful tips

## RAG Pipeline Tests

### 10. Knowledge Retrieval
- [ ] Retrieves relevant documents
- [ ] Returns top-K results (default: 3)
- [ ] Shows sources in UI
- [ ] Displays content preview
- [ ] Citations accurate
- [ ] Handles queries with no matches gracefully

**Test Queries:**
- [ ] "quadratic equation" → algebra_formulas.md
- [ ] "derivative" → calculus_concepts.md
- [ ] "probability" → probability_concepts.md
- [ ] "matrix" → linear_algebra_basics.md

### 11. Vector Store
- [ ] Creates successfully on first run
- [ ] Saves to disk (./vector_store/)
- [ ] Loads from disk on subsequent runs
- [ ] "Reinitialize RAG" button works
- [ ] Handles missing knowledge base gracefully

## Human-in-the-Loop Tests

### 12. HITL Triggers
- [ ] Low OCR confidence triggers HITL (< 0.7)
- [ ] Low ASR confidence triggers HITL (< 0.7)
- [ ] Ambiguous problem triggers HITL
- [ ] Low verifier confidence triggers HITL (< 0.8)
- [ ] Warning message displayed clearly

### 13. HITL Actions
- [ ] Problem can be edited after extraction
- [ ] Edited problem solves successfully
- [ ] System uses edited version (not original)

## Memory & Learning Tests

### 14. Interaction Storage
- [ ] Interactions saved to memory/interactions.jsonl
- [ ] File created if doesn't exist
- [ ] Each interaction has unique ID
- [ ] Timestamp recorded
- [ ] All agent outputs stored

### 15. Similar Problem Retrieval
- [ ] System finds past similar problems
- [ ] Similarity shown in execution trace
- [ ] Memory retrieval stage displays count

**Test:**
- [ ] Solve: x² + 5x + 6 = 0
- [ ] Then solve: x² + 7x + 12 = 0
- [ ] Check trace shows similar problem found

### 16. Corrections Learning
- [ ] OCR corrections can be stored
- [ ] ASR corrections can be stored
- [ ] Corrections saved to memory/corrections.json
- [ ] Corrections applied to future inputs

**Test:**
- [ ] Upload image with "x²2" (OCR error)
- [ ] Correct to "x²"
- [ ] Submit feedback
- [ ] Future "x²2" automatically corrected

## UI/UX Tests

### 17. User Interface
- [ ] Page loads without errors
- [ ] Sidebar displays correctly
- [ ] All tabs accessible (Solve, Trace, Feedback)
- [ ] Input method selector works
- [ ] Buttons respond to clicks
- [ ] Loading spinners show during processing
- [ ] Results display properly formatted

### 18. Solution Display
- [ ] Steps listed clearly
- [ ] Final answer highlighted
- [ ] Confidence score shown with color coding
  - Green: ≥80%
  - Orange: 60-80%
  - Red: <60%
- [ ] Verification status shown
- [ ] Issues listed if found
- [ ] Explanation formatted well

### 19. Execution Trace
- [ ] All 7+ stages shown
- [ ] Each stage has status (started/completed/error)
- [ ] Timing information included
- [ ] Confidence scores displayed
- [ ] Expandable details work
- [ ] JSON formatted properly

### 20. RAG Sources Panel
- [ ] Sources listed in right column
- [ ] Source names shown
- [ ] Content preview displayed
- [ ] Expandable for full content
- [ ] Multiple sources handled

### 21. Feedback Tab
- [ ] Interaction ID displayed
- [ ] Approve/Reject radio buttons work
- [ ] Correct answer input field works
- [ ] Comments text area works
- [ ] Submit button works
- [ ] Success message shows
- [ ] Feedback saved to memory/feedback.jsonl

## Topic-Specific Tests

### 22. Algebra Problems
- [ ] Quadratic equations: x² + 5x + 6 = 0
- [ ] Linear systems: 2x + 3y = 7, x - y = 1
- [ ] Inequalities: -2x > 4
- [ ] Polynomials: Factor x² - 5x + 6

### 23. Calculus Problems
- [ ] Derivatives: d/dx(x³ + 2x²)
- [ ] Limits: lim(x→2) (x²-4)/(x-2)
- [ ] Chain rule: d/dx(sin(2x²))
- [ ] Optimization: Maximize -x² + 4x + 1

### 24. Probability Problems
- [ ] Basic: P(even) on die roll
- [ ] Combinations: C(10,3)
- [ ] Two events: P(sum=7) on two dice

### 25. Linear Algebra Problems
- [ ] Matrix multiplication: [[1,2],[3,4]] × [[2,0],[1,3]]
- [ ] Determinant: det([[2,3],[1,4]])
- [ ] Dot product: (3,4) · (2,-1)

## Error Handling Tests

### 26. API Errors
- [ ] Invalid API key handled gracefully
- [ ] Rate limit errors handled
- [ ] Network errors handled
- [ ] Error message user-friendly

### 27. Input Validation
- [ ] Large files rejected (> 10MB)
- [ ] Invalid file types rejected
- [ ] Malformed input handled
- [ ] Empty input handled

### 28. Edge Cases
- [ ] Very long problems (> 1000 chars)
- [ ] Special characters in math notation
- [ ] Multiple equations in one problem
- [ ] Out-of-scope topics (advanced math)

## Performance Tests

### 29. Response Times
- [ ] Text input: < 30 seconds
- [ ] Image input: < 60 seconds
- [ ] Audio input: < 90 seconds
- [ ] No timeouts or hangs
- [ ] Progress indicators work

### 30. Resource Usage
- [ ] Memory usage reasonable (< 2GB)
- [ ] CPU usage acceptable
- [ ] No memory leaks over multiple problems
- [ ] Caching works (subsequent runs faster)

## Integration Tests

### 31. End-to-End Workflows

**Workflow 1: Text → Solution → Feedback**
- [ ] Enter text problem
- [ ] Solve successfully
- [ ] View all agent outputs
- [ ] Check RAG sources
- [ ] Submit positive feedback
- [ ] Verify stored in memory

**Workflow 2: Image → Edit → Solution**
- [ ] Upload image
- [ ] Extract text (confidence shown)
- [ ] Edit extracted text
- [ ] Solve edited version
- [ ] Verify uses edited text

**Workflow 3: Low Confidence → HITL → Solution**
- [ ] Upload poor quality image or audio
- [ ] HITL warning appears
- [ ] Edit/correct input
- [ ] Solve successfully
- [ ] Submit correction
- [ ] Verify correction stored

**Workflow 4: Memory Reuse**
- [ ] Solve Problem A
- [ ] Solve similar Problem B
- [ ] Check trace shows similar problem found
- [ ] Verify past solution referenced

## Security Tests

### 32. Data Security
- [ ] API keys not exposed in UI
- [ ] API keys not in logs
- [ ] User input sanitized
- [ ] No code injection possible
- [ ] File uploads validated

## Deployment Tests (if deploying)

### 33. Pre-Deployment
- [ ] All tests above pass
- [ ] No sensitive data in repo
- [ ] .env.example provided
- [ ] .gitignore configured correctly
- [ ] README complete and accurate

### 34. Platform-Specific (Streamlit Cloud)
- [ ] App deploys successfully
- [ ] Secrets configured
- [ ] Public URL accessible
- [ ] All features work in cloud
- [ ] Logs accessible

## Documentation Tests

### 35. Documentation Completeness
- [ ] README.md comprehensive
- [ ] QUICKSTART.md clear and accurate
- [ ] ARCHITECTURE.md detailed
- [ ] DEPLOYMENT.md covers all platforms
- [ ] EXAMPLES.md helpful
- [ ] Code comments adequate

## Final Validation

### 36. Complete System Test
- [ ] Fresh installation on new machine works
- [ ] Validation script passes
- [ ] Can solve 3 problems (one per input method)
- [ ] All agents execute in trace
- [ ] RAG sources displayed
- [ ] Feedback submitted successfully
- [ ] Memory stores data correctly

### 37. User Acceptance
- [ ] UI intuitive for target users
- [ ] Error messages helpful
- [ ] Solutions accurate
- [ ] Explanations educational
- [ ] Performance acceptable
- [ ] System reliable

## Issue Tracking

### Known Issues
Track any issues found during testing:

| Issue | Severity | Status | Notes |
|-------|----------|--------|-------|
| Example: Slow first load | Low | Known | Models download on first run |
|  |  |  |  |

### Test Results Summary

**Date:** ___________

**Tester:** ___________

**Environment:**
- OS: ___________
- Python Version: ___________
- Browser: ___________

**Results:**
- Total Tests: ___ / 37 sections
- Passed: ___
- Failed: ___
- Blocked: ___

**Overall Status:** ☐ PASS ☐ FAIL ☐ NEEDS WORK

**Notes:**
___________________________________
___________________________________
___________________________________

## Sign-Off

By completing this checklist, I verify that the AI Math Mentor system has been thoroughly tested and is ready for:

- [ ] Development use
- [ ] Demo presentation
- [ ] Production deployment
- [ ] User release

**Signature:** ___________________ **Date:** ___________
