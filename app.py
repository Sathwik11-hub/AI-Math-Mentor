"""
Streamlit UI for AI Math Mentor
Main application interface
"""
import streamlit as st
from datetime import datetime
import os
from pathlib import Path

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
</style>
""", unsafe_allow_html=True)


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


def initialize_system():
    """Initialize the math mentor system"""
    try:
        with st.spinner("Initializing AI Math Mentor..."):
            # Validate config
            Config.validate()
            
            # Create orchestrator
            orchestrator = MathMentorOrchestrator()
            
            # Initialize RAG
            orchestrator.initialize_rag()
            
            st.session_state.orchestrator = orchestrator
            st.session_state.initialized = True
            st.success("✅ System initialized successfully!")
            
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        logger.error(f"Initialization error: {e}")
        st.info("💡 Make sure you have set OPENAI_API_KEY in your .env file")


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
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Controls")
        
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
    
    # Check if system is initialized
    if not st.session_state.initialized:
        st.warning("⚠️ Please initialize the system using the sidebar button")
        st.info("💡 Make sure you have created a `.env` file with your `OPENAI_API_KEY`")
        return
    
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
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                
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
                        # Save audio temporarily
                        temp_path = f"/tmp/{audio_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(audio_file.read())
                        
                        result = st.session_state.orchestrator.process_input(
                            temp_path, "audio"
                        )
                        
                        st.session_state.extracted_text = result.get("transcript", "")
                        confidence = result.get("confidence", 0.0)
                        
                        st.markdown(f"**ASR Confidence:** {display_confidence(confidence)}", 
                                  unsafe_allow_html=True)
                        
                        if result.get("needs_hitl"):
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
