"""
Streamlit UI for AI Math Mentor
Main application interface with User API Key Input
"""
import streamlit as st
from datetime import datetime
import os
from pathlib import Path
import re

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from utils.orchestrator import MathMentorOrchestrator
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Math Mentor",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stAlert {
        margin-top: 1rem;
    }
    .trace-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .confidence-high {
        color: green;
        font-weight: bold;
    }
    .confidence-medium {
        color: orange;
        font-weight: bold;
    }
    .confidence-low {
        color: red;
        font-weight: bold;
    }
    /* API Key Configuration Box */
    .api-key-box {
        background-color: #FFFFFF !important;
        border: 3px solid #4CAF50;
        border-radius: 12px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .api-key-header {
        color: #1a1a1a !important;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: none;
    }
    .api-instructions {
        background-color: #FFFFFF !important;
        color: #1a1a1a !important;
        border: 2px solid #2196F3;
        border-left: 6px solid #2196F3;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .api-instructions b {
        color: #000000 !important;
        font-weight: 700;
    }
    .api-instructions ul {
        color: #1a1a1a !important;
        margin-left: 20px;
    }
    .api-instructions li {
        color: #1a1a1a !important;
        margin: 8px 0;
    }
    /* Force dark text in all API sections */
    .api-key-box * {
        color: #1a1a1a !important;
    }
    .api-instructions * {
        color: #1a1a1a !important;
    }
    /* Streamlit input labels in API section */
    div[data-testid="stVerticalBlock"] > div:has(.api-key-box) label {
        color: #1a1a1a !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def validate_api_key(api_key: str, provider: str) -> tuple[bool, str]:
    """
    Validate API key format
    
    Args:
        api_key: The API key string
        provider: 'gemini' or 'openai'
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not api_key or api_key.strip() == "":
        return False, "API key cannot be empty"
    
    api_key = api_key.strip()
    
    if provider == "gemini":
        # Gemini API keys start with 'AIzaSy' and are 39 characters long
        if not api_key.startswith("AIzaSy"):
            return False, "Gemini API key should start with 'AIzaSy'"
        if len(api_key) != 39:
            return False, f"Gemini API key should be 39 characters long (yours is {len(api_key)})"
        if not re.match(r'^AIzaSy[A-Za-z0-9_-]{33}$', api_key):
            return False, "Invalid Gemini API key format"
            
    elif provider == "openai":
        # OpenAI API keys start with 'sk-' and are typically 51 characters
        if not api_key.startswith("sk-"):
            return False, "OpenAI API key should start with 'sk-'"
        if len(api_key) < 40:
            return False, "OpenAI API key seems too short"
        if not re.match(r'^sk-[A-Za-z0-9]{48}$', api_key):
            return False, "Invalid OpenAI API key format"
    
    return True, ""


def render_api_key_input():
    """
    Render the API key input section
    Returns True if valid API key is provided, False otherwise
    """
    st.markdown('<div class="api-key-box">', unsafe_allow_html=True)
    st.markdown('<p class="api-key-header">🔑 API Key Configuration</p>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div class="api-instructions">
    <b>⚠️ IMPORTANT: API Key Required</b><br>
    This application requires a valid API key to function. Each user must provide their own API key.
    <br><br>
    <b>Supported Providers:</b>
    <ul>
        <li><b>Google Gemini</b> (Recommended) - Free tier: 20 requests/day</li>
        <li><b>OpenAI</b> - Requires paid account</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Provider selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        provider = st.selectbox(
            "Select AI Provider",
            options=["gemini", "openai"],
            format_func=lambda x: "Google Gemini" if x == "gemini" else "OpenAI",
            help="Choose which AI provider you want to use"
        )
    
    with col2:
        if provider == "gemini":
            st.info("💡 Get your free Gemini API key at: https://aistudio.google.com/apikey")
        else:
            st.info("💡 Get your OpenAI API key at: https://platform.openai.com/api-keys")
    
    # API Key input
    api_key = st.text_input(
        f"Enter your {provider.upper()} API Key",
        type="password",
        placeholder=f"Paste your {provider.upper()} API key here...",
        help=f"Your {provider.upper()} API key will be used for this session only and not stored permanently",
        key="user_api_key_input"
    )
    
    # Validation and confirmation
    if api_key:
        is_valid, error_message = validate_api_key(api_key, provider)
        
        if is_valid:
            st.success(f"✅ Valid {provider.upper()} API key detected!")
            
            # Show key preview (first 8 and last 4 characters)
            key_preview = f"{api_key[:8]}...{api_key[-4:]}"
            st.caption(f"Key preview: `{key_preview}`")
            
            # Store in session state
            st.session_state.user_api_key = api_key
            st.session_state.api_provider = provider
            st.session_state.api_key_validated = True
            
            st.markdown('</div>', unsafe_allow_html=True)
            return True
        else:
            st.error(f"❌ {error_message}")
            st.session_state.api_key_validated = False
    else:
        st.warning("⚠️ Please enter your API key to continue")
        st.session_state.api_key_validated = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    return False


def initialize_session_state():
    """Initialize session state variables"""
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'interaction_id' not in st.session_state:
        st.session_state.interaction_id = None
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'user_api_key' not in st.session_state:
        st.session_state.user_api_key = None
    if 'api_provider' not in st.session_state:
        st.session_state.api_provider = None
    if 'api_key_validated' not in st.session_state:
        st.session_state.api_key_validated = False
        st.session_state.initialized = False
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'interaction_id' not in st.session_state:
        st.session_state.interaction_id = None
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""


def initialize_system():
    """Initialize the math mentor system with user's API key"""
    try:
        with st.spinner("Initializing AI Math Mentor with your API key..."):
            # Override Config with user's API key
            if st.session_state.user_api_key:
                os.environ['GEMINI_API_KEY'] = st.session_state.user_api_key
                Config.GEMINI_API_KEY = st.session_state.user_api_key
                
                # Set model based on provider
                if st.session_state.api_provider == "gemini":
                    Config.GEMINI_MODEL = "models/gemini-2.5-flash"
                    st.info(f"🤖 Using Google Gemini: {Config.GEMINI_MODEL}")
                elif st.session_state.api_provider == "openai":
                    # For OpenAI integration (future implementation)
                    st.warning("⚠️ OpenAI support coming soon! Using Gemini for now.")
                    Config.GEMINI_MODEL = "models/gemini-2.5-flash"
            
            # Validate config
            Config.validate()
            
            # Create orchestrator
            orchestrator = MathMentorOrchestrator()
            
            # Initialize RAG
            orchestrator.initialize_rag()
            
            st.session_state.orchestrator = orchestrator
            st.session_state.initialized = True
            st.success("✅ System initialized successfully with your API key!")
            
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        logger.error(f"Initialization error: {e}")
        
        # Check if it's an API key issue
        if "API key" in str(e) or "authentication" in str(e).lower():
            st.error("� There seems to be an issue with your API key. Please check:")
            st.markdown("""
            - Ensure the API key is correct and complete
            - Verify the API key is active and has quota available
            - Check if the API key has the necessary permissions
            """)
        else:
            st.info("💡 If the error persists, try refreshing the page and entering your API key again")


def display_confidence(confidence: float) -> str:
    """Display confidence with color coding"""
    if confidence >= 0.8:
        return f'<span class="confidence-high">{confidence:.2%}</span>'
    elif confidence >= 0.6:
        return f'<span class="confidence-medium">{confidence:.2%}</span>'
    else:
        return f'<span class="confidence-low">{confidence:.2%}</span>'


def main():
    """Main application"""
    st.title("🧮 AI Math Mentor")
    st.markdown("*Your reliable JEE-level mathematics companion with multimodal support*")
    
    initialize_session_state()
    
    # ========================================
    # STEP 1: API KEY INPUT (REQUIRED FIRST)
    # ========================================
    st.markdown("---")
    has_valid_api_key = render_api_key_input()
    st.markdown("---")
    
    # Block further interaction until API key is provided
    if not has_valid_api_key:
        st.warning("⚠️ **Please provide a valid API key above to continue**")
        st.info("""
        **Why do I need an API key?**
        
        This application uses AI models from Google Gemini or OpenAI to solve mathematical problems.
        Each user must provide their own API key to:
        
        - ✅ Ensure fair usage and quota management
        - ✅ Maintain security and privacy
        - ✅ Allow personalized access to AI services
        - ✅ Track your own usage and costs
        
        **How to get an API key:**
        1. **Google Gemini** (Free): Visit https://aistudio.google.com/apikey
        2. **OpenAI** (Paid): Visit https://platform.openai.com/api-keys
        """)
        st.stop()  # Stop execution until API key is provided
    
    # ========================================
    # STEP 2: SYSTEM INITIALIZATION
    # ========================================
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Controls")
        
        # Show API key status
        st.success(f"🔑 API Key: {st.session_state.api_provider.upper()}")
        key_preview = f"{st.session_state.user_api_key[:8]}...{st.session_state.user_api_key[-4:]}"
        st.caption(f"Key: `{key_preview}`")
        
        st.divider()
        
        if not st.session_state.initialized:
            if st.button("🚀 Initialize System", type="primary"):
                initialize_system()
        else:
            st.success("✅ System Ready")
            
            if st.button("🔄 Reinitialize RAG"):
                with st.spinner("Reinitializing RAG..."):
                    st.session_state.orchestrator.initialize_rag()
                st.success("RAG reinitialized!")
        
        st.divider()
        st.header("📚 About")
        st.markdown("""
        **AI Math Mentor** is a production-grade system for solving JEE-level math problems.
        
        **Features:**
        - 📸 Image input (OCR)
        - 🎤 Audio input (ASR)
        - ⌨️ Text input
        - 🤖 Multi-agent reasoning
        - 📖 RAG-based knowledge retrieval
        - ✅ Verification & guardrails
        - 👤 Human-in-the-loop
        - 🧠 Self-learning memory
        
        **Supported Topics:**
        - Algebra
        - Calculus (basics)
        - Probability
        - Linear Algebra
        """)
    
    # ========================================
    # STEP 3: CHECK SYSTEM INITIALIZATION
    # ========================================
    if not st.session_state.initialized:
        st.info("👈 **Please click 'Initialize System' in the sidebar to begin**")
        st.markdown("""
        ### Getting Started:
        1. ✅ Your API key has been validated
        2. 👈 Click **"Initialize System"** in the sidebar
        3. 🚀 Start solving math problems!
        
        The system will:
        - Load the RAG knowledge base
        - Initialize all AI agents
        - Prepare the multimodal input handlers
        """)
        return
    
    # ========================================
    # STEP 4: PROBLEM SOLVING INTERFACE
    # ========================================
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Solve Problem", "📊 Execution Trace", "💬 Feedback"])
    
    with tab1:
        st.header("Input Method")
        
        input_method = st.radio(
            "Choose input method:",
            ["Text", "Image", "Audio"],
            horizontal=True
        )
        
        problem_text = None
        input_type = None
        
        if input_method == "Text":
            problem_text = st.text_area(
                "Enter your math problem:",
                height=150,
                placeholder="Example: Solve x² + 5x + 6 = 0"
            )
            input_type = "text"
            
        elif input_method == "Image":
            uploaded_file = st.file_uploader(
                "Upload an image with the problem:",
                type=["png", "jpg", "jpeg"]
            )
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image", width="stretch")
                
                if st.button("🔍 Extract Text from Image"):
                    with st.spinner("Processing image with OCR..."):
                        result = st.session_state.orchestrator.process_input(
                            uploaded_file, "image"
                        )
                        
                        st.session_state.extracted_text = result.get("extracted_text", "")
                        confidence = result.get("confidence", 0.0)
                        
                        st.markdown(f"**OCR Confidence:** {display_confidence(confidence)}", 
                                  unsafe_allow_html=True)
                        
                        if result.get("needs_hitl"):
                            st.warning("⚠️ Low confidence detected. Please review and edit the text.")
                
                if st.session_state.extracted_text:
                    problem_text = st.text_area(
                        "Extracted text (edit if needed):",
                        value=st.session_state.extracted_text,
                        height=150
                    )
                    input_type = "image"
                    
        elif input_method == "Audio":
            audio_file = st.file_uploader(
                "Upload an audio file:",
                type=["wav", "mp3", "m4a", "ogg"]
            )
            
            if audio_file is not None:
                st.audio(audio_file)
                
                if st.button("🎧 Transcribe Audio"):
                    with st.spinner("Transcribing audio with Whisper..."):
                        # Reset file pointer before reading
                        audio_file.seek(0)
                        # Save audio temporarily
                        temp_path = f"/tmp/{audio_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(audio_file.read())
                        
                        result = st.session_state.orchestrator.process_input(
                            temp_path, "audio"
                        )
                        
                        st.session_state.extracted_text = result.get("transcript", "")
                        confidence = result.get("confidence", 0.0)
                        message = result.get("message", "")
                        
                        st.markdown(f"**ASR Confidence:** {display_confidence(confidence)}", 
                                  unsafe_allow_html=True)
                        
                        if result.get("needs_hitl"):
                            if "ffmpeg" in message:
                                st.error(f"❌ {message}")
                                st.info("""
                                **To fix this issue:**
                                1. Install Homebrew (if not installed): 
                                   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
                                2. Install ffmpeg: `brew install ffmpeg`
                                3. Restart the app
                                
                                See `INSTALL_FFMPEG.md` for more details.
                                """)
                            else:
                                st.warning("⚠️ Low confidence detected. Please review and edit the transcript.")
                        
                        # Clean up temp file
                        os.remove(temp_path)
                
                if st.session_state.extracted_text:
                    problem_text = st.text_area(
                        "Transcript (edit if needed):",
                        value=st.session_state.extracted_text,
                        height=150
                    )
                    input_type = "audio"
        
        # Solve button
        if problem_text and st.button("🚀 Solve Problem", type="primary"):
            with st.spinner("Solving problem... This may take a moment."):
                result = st.session_state.orchestrator.solve_problem(
                    problem_text, 
                    input_type or "text"
                )
                
                st.session_state.current_result = result
                st.session_state.interaction_id = result.get("interaction_id")
        
        # Display results
        if st.session_state.current_result:
            result = st.session_state.current_result
            
            if result.get("status") == "needs_clarification":
                st.warning("⚠️ The problem needs clarification")
                st.json(result.get("parsed_problem"))
            
            elif result.get("status") == "quota_exceeded":
                st.error("⚠️ API Quota Exceeded")
                st.markdown(result.get("message", ""))
                
                # Show helpful tips
                with st.expander("💡 What can I do?"):
                    st.markdown("""
                    **Free Tier Limits:**
                    - 20 requests per day for Gemini 2.5 Flash
                    - Quota resets automatically every 24 hours
                    
                    **Quick Solutions:**
                    1. **Wait**: Quota resets automatically
                    2. **Get a new API key**: https://aistudio.google.com/apikey
                    3. **Upgrade**: Consider a paid plan for higher limits
                    
                    **Check Usage:**
                    - Monitor at: https://ai.dev/usage?tab=rate-limit
                    """)
                
            elif result.get("status") == "error":
                st.error(f"❌ Error: {result.get('message')}")
                
            elif result.get("status") == "success":
                st.success("✅ Problem solved!")
                
                # Display HITL warning if needed
                if result.get("requires_hitl"):
                    st.warning("⚠️ Human review recommended - verification confidence is low")
                
                # Solution display
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📋 Solution")
                    
                    solution = result.get("solution", {})
                    
                    # Display steps
                    st.markdown("**Step-by-step solution:**")
                    for i, step in enumerate(solution.get("steps", []), 1):
                        st.markdown(f"{i}. {step}")
                    
                    # Final answer
                    st.markdown("---")
                    st.markdown(f"**Final Answer:** `{solution.get('final_answer', 'N/A')}`")
                    
                    # Confidence
                    conf = solution.get("confidence", 0.0)
                    st.markdown(f"**Solution Confidence:** {display_confidence(conf)}", 
                              unsafe_allow_html=True)
                    
                    # Verification
                    st.markdown("---")
                    verification = result.get("verification", {})
                    if verification.get("is_correct"):
                        st.success("✅ Solution verified as correct")
                    else:
                        st.warning("⚠️ Verification found issues")
                    
                    if verification.get("issues_found"):
                        st.markdown("**Issues:**")
                        for issue in verification["issues_found"]:
                            st.markdown(f"- {issue}")
                    
                    # Explanation
                    st.markdown("---")
                    st.subheader("📖 Explanation")
                    explanation = result.get("explanation", {})
                    st.markdown(explanation.get("explanation", ""))
                    
                    if explanation.get("key_concepts"):
                        st.markdown("**Key Concepts:**")
                        for concept in explanation["key_concepts"]:
                            st.markdown(f"- {concept}")
                    
                    if explanation.get("tips"):
                        st.markdown("**Tips:**")
                        for tip in explanation["tips"]:
                            st.markdown(f"💡 {tip}")
                
                with col2:
                    st.subheader("📚 RAG Sources")
                    for source in result.get("rag_sources", []):
                        with st.expander(f"📄 {source['source']}"):
                            st.text(source['content'])
                    
                    st.subheader("🔍 Parsed Problem")
                    parsed = result.get("parsed_problem", {})
                    st.json({
                        "topic": parsed.get("topic"),
                        "variables": parsed.get("variables"),
                        "constraints": parsed.get("constraints")
                    })
    
    with tab2:
        st.header("📊 Agent Execution Trace")
        
        if st.session_state.current_result:
            trace = st.session_state.current_result.get("execution_trace", [])
            
            for i, step in enumerate(trace, 1):
                with st.expander(f"Stage {i}: {step.get('stage', 'Unknown')}", 
                               expanded=(step.get('status') == 'error')):
                    st.json(step)
        else:
            st.info("Solve a problem to see the execution trace")
    
    with tab3:
        st.header("💬 Provide Feedback")
        
        if st.session_state.interaction_id:
            st.markdown(f"**Interaction ID:** `{st.session_state.interaction_id}`")
            
            col1, col2 = st.columns(2)
            
            with col1:
                approved = st.radio(
                    "Was the solution correct?",
                    ["✅ Approved", "❌ Rejected"],
                    horizontal=True
                )
            
            with col2:
                correct_answer = st.text_input(
                    "Correct answer (if different):",
                    placeholder="Leave empty if solution was correct"
                )
            
            comments = st.text_area(
                "Additional comments:",
                placeholder="Any feedback or suggestions..."
            )
            
            if st.button("Submit Feedback", type="primary"):
                feedback = {
                    "approved": approved == "✅ Approved",
                    "correct_answer": correct_answer if correct_answer else None,
                    "comments": comments if comments else None,
                    "timestamp": datetime.now().isoformat()
                }
                
                st.session_state.orchestrator.submit_feedback(
                    st.session_state.interaction_id,
                    feedback
                )
                
                st.success("✅ Feedback submitted! Thank you for helping improve the system.")
        else:
            st.info("Solve a problem first to provide feedback")


if __name__ == "__main__":
    main()
