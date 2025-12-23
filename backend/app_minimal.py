"""
AI Math Mentor - Minimal Working Version
Tests basic Gemini API functionality without complex agents
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Page configuration
st.set_page_config(
    page_title="Math Mentor (Minimal)",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 AI Math Mentor - Minimal Test Version")
st.markdown("*Simple version to test Gemini API connection*")

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in environment")
    st.info("💡 Add GEMINI_API_KEY to your .env file")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)  # type: ignore[attr-defined]
    model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
    model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
    st.success(f"✅ Connected to {model_name}")
except Exception as e:
    st.error(f"❌ Failed to configure Gemini: {e}")
    st.stop()

# Sidebar with examples
with st.sidebar:
    st.header("📚 Example Problems")
    
    examples = {
        "Quadratic Equation": "Solve x² + 5x + 6 = 0",
        "Derivative": "Find the derivative of f(x) = x³ + 2x² - 5x + 1",
        "Probability": "A bag contains 5 red balls and 3 blue balls. If you draw one ball at random, what is the probability it's red?",
        "Linear Equation": "Solve for x: 3x + 7 = 22",
        "Factoring": "Factor x² - 9"
    }
    
    for name, problem in examples.items():
        if st.button(name):
            st.session_state.problem = problem

# Main content
st.header("Enter Your Math Problem")

# Get problem text
if 'problem' in st.session_state:
    problem_text = st.text_area(
        "Problem:",
        value=st.session_state.problem,
        height=150,
        help="Type or edit your math problem here"
    )
else:
    problem_text = st.text_area(
        "Problem:",
        placeholder="Example: Solve x² + 5x + 6 = 0",
        height=150,
        help="Type your math problem here"
    )

# Solve button
if st.button("🚀 Solve Problem", type="primary", disabled=not problem_text):
    if not problem_text.strip():
        st.warning("⚠️ Please enter a problem first")
    else:
        with st.spinner("🤖 Solving problem..."):
            try:
                # Create a focused prompt for math problems
                prompt = f"""You are an expert mathematics tutor. Solve the following problem step-by-step.

Problem: {problem_text}

Provide:
1. **Analysis**: Identify the type of problem and relevant concepts
2. **Step-by-Step Solution**: Show each step clearly with explanations
3. **Final Answer**: State the final answer clearly
4. **Verification** (if applicable): Check your answer

Use clear mathematical notation and explain your reasoning at each step."""

                # Call Gemini
                response = model.generate_content(prompt)
                
                # Display solution
                st.success("✅ Solution Generated!")
                
                # Show the solution
                st.markdown("### 📝 Solution")
                st.markdown(response.text)
                
                # Show metadata
                with st.expander("🔍 Debug Info"):
                    st.write(f"**Model used:** {model_name}")
                    st.write(f"**Problem length:** {len(problem_text)} characters")
                    st.write(f"**Response length:** {len(response.text)} characters")
                
            except Exception as e:
                st.error(f"❌ Error solving problem: {str(e)}")
                
                # Show detailed error in expander
                with st.expander("🔍 Error Details"):
                    import traceback
                    st.code(traceback.format_exc())
                
                # Provide helpful suggestions
                st.info("""
                💡 **Troubleshooting Tips:**
                - Check if your API key is valid
                - Verify you have API quota remaining
                - Try a simpler problem
                - Check your internet connection
                """)

# Footer
st.divider()
st.markdown("""
**Note:** This is a minimal test version that uses direct Gemini API calls.  
Once this works, you can use the full version with multi-agent system and RAG.

**Status:**
- ✅ API Connection: Working
- ⏳ Multi-Agent System: Use `app.py` for full version
- ⏳ RAG Knowledge Base: Use `app.py` for full version
- ⏳ Memory & Learning: Use `app.py` for full version
""")
