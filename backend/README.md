# AI Math Mentor - Backend

A production-grade multi-agent system for solving JEE-level mathematics problems using Gemini AI.

## Features

- 🤖 **Multi-agent architecture** with specialized agents for parsing, solving, and verification
- 📸 **Multimodal input support**: Text, Image (OCR), and Audio (ASR)
- 📖 **RAG-based knowledge retrieval** for mathematical concepts
- ✅ **Verification and guardrails** for reliable answers
- 👤 **Human-in-the-loop** for low-confidence predictions
- 🧠 **Self-learning memory system** for continuous improvement

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Gemini API key from Google AI Studio

### 2. Installation

```bash
# From project root
cd /Users/sathwikadigoppula/AI-Math-Mentor-2
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### 4. Validation

Test that all components are working:

```bash
cd backend
python3 validate.py
```

You should see:
```
✅ All imports successful!
✅ Basic functionality tests passed!
✅ All knowledge base files present!
🎉 All validation tests passed!
```

### 5. Run the App

```bash
cd backend
streamlit run app.py
```

The app will start at `http://localhost:8501`.

## Usage

1. **Initialize System**: Click the "🚀 Initialize System" button in the sidebar
2. **Choose Input Method**:
   - **Text**: Directly type or paste your math problem
   - **Image**: Upload an image with a math problem (OCR will extract text)
   - **Audio**: Upload an audio file describing the problem (ASR will transcribe)
3. **Solve**: Click "🚀 Solve Problem" to get the solution

## Recent Fixes

### Streamlit Deprecation Warning (Fixed)
- Changed `use_column_width=True` to `use_container_width=True` in image display
- No more deprecation warnings in Streamlit

### OCR 0% Confidence Issue (Fixed)
- Updated `ImageInputHandler.process_image()` to properly handle Streamlit `UploadedFile` objects
- Now correctly converts uploaded files to PIL Images before OCR processing
- OCR should now properly extract text from uploaded images

## Project Structure

```
backend/
├── agents/              # Multi-agent system components
│   ├── base_agent.py
│   ├── parser_agent.py
│   ├── intent_router_agent.py
│   ├── solver_agent.py
│   ├── verifier_agent.py
│   └── explainer_agent.py
├── knowledge_base/      # Mathematical knowledge for RAG
├── memory/              # Learning and corrections storage
├── rag/                 # RAG pipeline implementation
├── utils/               # Configuration and orchestration
│   ├── config.py
│   ├── input_handlers.py
│   ├── logger.py
│   └── orchestrator.py
├── app.py              # Streamlit UI
└── validate.py         # Validation script
```

## Configuration Options

Edit `.env` to customize:

```env
# AI Model
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-flash

# Confidence Thresholds
OCR_CONFIDENCE_THRESHOLD=0.7
ASR_CONFIDENCE_THRESHOLD=0.7
VERIFIER_CONFIDENCE_THRESHOLD=0.8

# RAG Settings
RAG_TOP_K=3
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Logging
LOG_LEVEL=INFO
```

## Troubleshooting

### "GEMINI_API_KEY is required"
- Make sure you've created a `.env` file in the project root
- Verify your Gemini API key is set correctly
- Restart the app after changing `.env`

### OCR returns empty text
- Ensure the image is clear and well-lit
- Try images with printed text rather than handwritten
- The system will show a warning if confidence is low - you can manually edit the extracted text

### "Model not found" errors
- Check that `GEMINI_MODEL` in `.env` is set to a valid model (e.g., `gemini-1.5-flash`)
- Verify your API key has access to the specified model

## Support

For issues or questions, check the main project documentation or open an issue on GitHub.
