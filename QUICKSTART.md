# 🚀 Quick Start Guide - AI Math Mentor

Get started with AI Math Mentor in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git (for cloning)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sathwik11-hub/AI-Math-Mentor.git
cd AI-Math-Mentor
```

### Step 2: Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** First installation takes 2-5 minutes (downloading models and dependencies).

### Step 4: Configure API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 5: Validate Installation

Run the validation script:
```bash
python validate.py
```

You should see:
```
✅ All validation tests passed!
```

### Step 6: Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Problem

Let's solve your first problem!

1. **Initialize System:**
   - Click "🚀 Initialize System" in the sidebar
   - Wait ~30 seconds for RAG pipeline setup (first time only)

2. **Enter a Problem:**
   - Select "Text" input method
   - Type: `Solve x² + 5x + 6 = 0`
   - Click "🚀 Solve Problem"

3. **Review Results:**
   - See step-by-step solution
   - Check agent execution trace
   - View RAG sources used
   - Read student-friendly explanation

4. **Provide Feedback:**
   - Go to "💬 Feedback" tab
   - Approve or provide corrections
   - Submit feedback for learning

## Test Different Input Methods

### Text Input (Simplest)
```
Problem: Find the derivative of x³ + 2x²
```

### Image Input (OCR)
1. Create/download an image with handwritten math problem
2. Select "Image" input method
3. Upload the image
4. Click "🔍 Extract Text from Image"
5. Review and edit extracted text
6. Click "🚀 Solve Problem"

### Audio Input (ASR)
1. Record yourself saying: "Solve x squared plus three x plus two equals zero"
2. Select "Audio" input method
3. Upload the audio file
4. Click "🎧 Transcribe Audio"
5. Review and edit transcript
6. Click "🚀 Solve Problem"

## Understanding the UI

### Main Tabs

**📝 Solve Problem**
- Input selection (Text/Image/Audio)
- Problem submission
- Solution display
- RAG sources panel

**📊 Execution Trace**
- See all 7 stages of processing
- Agent outputs and confidence scores
- Timing information
- Debug information

**💬 Feedback**
- Approve/reject solutions
- Submit correct answers
- Provide comments
- Help system learn

### Key Indicators

**Confidence Colors:**
- 🟢 Green (≥80%): High confidence
- 🟡 Orange (60-80%): Medium confidence
- 🔴 Red (<60%): Low confidence - HITL triggered

**HITL Warnings:**
- ⚠️ Yellow warning: Review recommended
- Shows when:
  - OCR/ASR confidence < 70%
  - Verifier confidence < 80%
  - Problem is ambiguous

## Sample Problems by Topic

### Algebra
```
1. Solve 2x² - 7x + 3 = 0
2. Solve the system: 2x + 3y = 7, x - y = 1
3. Simplify (x+2)(x-3)
```

### Calculus
```
1. Find the derivative of sin(2x²)
2. Calculate lim(x→2) (x²-4)/(x-2)
3. Find the maximum of f(x) = -x² + 4x + 1
```

### Probability
```
1. What is P(sum=7) when rolling two dice?
2. Choose 3 students from 10. How many ways?
3. If P(A)=0.5, P(B)=0.6, P(A∪B)=0.8, find P(A∩B)
```

### Linear Algebra
```
1. Multiply: [[1,2],[3,4]] × [[2,0],[1,3]]
2. Find determinant of [[2,3],[1,4]]
3. Dot product of (3,4) and (2,-1)
```

## Common First-Time Issues

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "OPENAI_API_KEY not found"
**Solution:**
- Ensure `.env` file exists in project root
- Check API key is correct
- Try: `export OPENAI_API_KEY=your_key` (temporary)

### Issue: "Failed to initialize RAG"
**Solution:**
- Check internet connection (downloads embeddings)
- Ensure `knowledge_base/` directory exists
- Try clicking "🔄 Reinitialize RAG"

### Issue: Slow first problem
**Solution:**
- Normal! First run downloads models (~1-2 min)
- Subsequent problems are faster (10-20 sec)
- Models are cached after first use

### Issue: OCR not working
**Solution:**
```bash
pip install easyocr
```
**Note:** EasyOCR downloads ~100MB on first use

### Issue: Audio not working
**Solution:**
```bash
pip install openai-whisper
```
**Note:** Whisper downloads models based on size (tiny: ~40MB, base: ~140MB)

## Performance Tips

### Faster Response Times
1. Use **text input** instead of image/audio when possible
2. Set `WHISPER_MODEL=tiny` in `.env` for faster ASR
3. Reduce `RAG_TOP_K=2` for fewer retrievals
4. Use GPT-3.5-turbo instead of GPT-4 (less accurate but faster)

### Cost Optimization
1. GPT-4: ~$0.03-0.05 per problem
2. GPT-3.5-turbo: ~$0.002-0.005 per problem
3. Monitor usage: https://platform.openai.com/usage

### Memory Management
- System stores all interactions in `memory/`
- Periodically archive old interactions to save space
- Each interaction: ~5-10KB

## Next Steps

### Learn More
- **Full Documentation:** See [README.md](README.md)
- **Architecture Details:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Example Problems:** See [EXAMPLES.md](EXAMPLES.md)
- **Deployment Guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

### Try Advanced Features
1. **Memory Learning:**
   - Solve similar problems
   - System finds past solutions
   - Check execution trace for "Memory Retrieval"

2. **HITL Workflow:**
   - Upload blurry image
   - System triggers review
   - Edit extracted text
   - Submit correction

3. **Feedback Loop:**
   - Provide corrections
   - System learns from feedback
   - Applied to future problems

### Customize
Edit `.env` to adjust:
- Model selection (GPT-4, GPT-3.5-turbo)
- Confidence thresholds
- RAG parameters
- Whisper model size

## Troubleshooting Command

If anything breaks, try this complete reset:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove cached data
rm -rf vector_store/ memory/*.json logs/

# Reinstall everything
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Revalidate
python validate.py

# Restart app
streamlit run app.py
```

## Getting Help

### Check Logs
```bash
# View today's logs
cat logs/$(date +%Y%m%d)_math_mentor.log

# Watch logs in real-time
tail -f logs/$(date +%Y%m%d)_math_mentor.log
```

### Debug Mode
Set in `.env`:
```
LOG_LEVEL=DEBUG
```

### Report Issues
GitHub Issues: https://github.com/Sathwik11-hub/AI-Math-Mentor/issues

Include:
- Error message
- Steps to reproduce
- Python version (`python --version`)
- OS (Windows/Mac/Linux)
- Logs (if relevant)

## Success Criteria

You're ready when you can:
- ✅ Solve a text problem in <20 seconds
- ✅ Extract text from an image with OCR
- ✅ Transcribe an audio problem
- ✅ See all 5 agents in execution trace
- ✅ View RAG sources in results
- ✅ Submit feedback successfully
- ✅ See similar problems found in memory

## What's Happening Behind the Scenes

When you submit a problem:

1. **Input Processing** (1-5s)
   - Text/OCR/ASR extraction
   - Confidence scoring
   - Apply learned corrections

2. **Parser Agent** (2-3s)
   - Structures the problem
   - Identifies topic and variables
   - Checks for ambiguity

3. **Memory Check** (0-1s)
   - Searches past problems
   - Finds similar solutions

4. **RAG Retrieval** (1-2s)
   - Queries knowledge base
   - Retrieves relevant formulas
   - Returns top-3 sources

5. **Intent Router** (2-3s)
   - Determines strategy
   - Selects tools (SymPy, etc.)

6. **Solver Agent** (5-8s)
   - Applies ReAct reasoning
   - Generates step-by-step solution
   - Uses symbolic/numerical tools

7. **Verifier Agent** (3-5s)
   - Checks correctness
   - Validates constraints
   - Triggers HITL if needed

8. **Explainer Agent** (3-5s)
   - Creates explanation
   - Highlights concepts
   - Provides tips

9. **Memory Storage** (0-1s)
   - Saves interaction
   - Updates corrections

**Total: ~10-30 seconds**

## Congratulations! 🎉

You're now ready to use AI Math Mentor. Start solving problems and enjoy the learning experience!

For detailed documentation, see the full [README.md](README.md).
