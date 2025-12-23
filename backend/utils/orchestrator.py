"""
Main Orchestrator - Coordinates all agents and system components
"""
from datetime import datetime
from typing import Dict, Any, List, Optional

from agents.parser_agent import ParserAgent
from agents.intent_router_agent import IntentRouterAgent
from agents.solver_agent import SolverAgent
from agents.verifier_agent import VerifierAgent
from agents.explainer_agent import ExplainerAgent
from rag.rag_pipeline import RAGPipeline
from memory.memory_system import MemorySystem
from utils.input_handlers import ImageInputHandler, AudioInputHandler, TextInputHandler
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class MathMentorOrchestrator:
    """Main orchestrator for AI Math Mentor system"""
    
    def __init__(self):
        # Initialize agents
        self.parser_agent = ParserAgent()
        self.intent_router_agent = IntentRouterAgent()
        self.solver_agent = SolverAgent()
        self.verifier_agent = VerifierAgent()
        self.explainer_agent = ExplainerAgent()
        
        # Initialize RAG and Memory
        self.rag_pipeline = RAGPipeline()
        self.memory_system = MemorySystem()
        
        # Initialize input handlers
        self.image_handler = ImageInputHandler()
        self.audio_handler = AudioInputHandler()
        self.text_handler = TextInputHandler()
        
        # Execution trace for UI
        self.execution_trace = []
        
        logger.info("MathMentorOrchestrator initialized")
    
    def initialize_rag(self):
        """Initialize RAG pipeline (create vector store)"""
        try:
            logger.info("Initializing RAG pipeline...")
            self.rag_pipeline.create_vector_store()
            logger.info("RAG pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}")
            raise
    
    def process_input(self, 
                     input_data: Any, 
                     input_type: str) -> Dict[str, Any]:
        """
        Process multimodal input
        
        Args:
            input_data: Image, audio, or text input
            input_type: 'image', 'audio', or 'text'
            
        Returns:
            Processing result with extracted text and metadata
        """
        self.execution_trace.append({
            "stage": "Input Processing",
            "status": "started",
            "type": input_type
        })
        
        try:
            if input_type == "image":
                result = self.image_handler.process_image(input_data)
                processed_text = result.get("extracted_text", "")
            elif input_type == "audio":
                result = self.audio_handler.process_audio(input_data)
                processed_text = result.get("transcript", "")
            else:  # text
                result = self.text_handler.process_text(input_data)
                processed_text = result.get("processed_text", "")
            
            # Apply learned corrections
            if input_type in ["image", "audio"]:
                correction_type = "ocr" if input_type == "image" else "asr"
                processed_text = self.memory_system.apply_learned_corrections(
                    processed_text, correction_type
                )
                result['corrected_text'] = processed_text
            
            self.execution_trace.append({
                "stage": "Input Processing",
                "status": "completed",
                "confidence": result.get("confidence", 1.0),
                "needs_hitl": result.get("needs_hitl", False)
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            self.execution_trace.append({
                "stage": "Input Processing",
                "status": "error",
                "error": str(e)
            })
            raise
    
    def solve_problem(self, 
                     raw_text: str, 
                     input_type: str,
                     user_edited: bool = False) -> Dict[str, Any]:
        """
        Main problem-solving pipeline
        
        Args:
            raw_text: Problem text (possibly user-edited)
            input_type: Origin of input
            user_edited: Whether user edited the text
            
        Returns:
            Complete solution with all agent outputs
        """
        self.execution_trace = []  # Reset trace
        timestamp = datetime.now().isoformat()
        
        try:
            # Stage 1: Parse Problem
            logger.info("Stage 1: Parsing problem...")
            self.execution_trace.append({
                "stage": "Parser Agent",
                "status": "started"
            })
            
            parsed_problem = self.parser_agent.execute({
                "raw_text": raw_text,
                "input_type": input_type
            })
            
            self.execution_trace.append({
                "stage": "Parser Agent",
                "status": "completed",
                "output": parsed_problem
            })
            
            # Note if clarification is flagged (but continue solving)
            needs_clarification_flag = parsed_problem.get("needs_clarification", False)
            if needs_clarification_flag:
                logger.warning("Problem flagged for clarification, but will attempt to solve anyway")
                self.execution_trace.append({
                    "stage": "Clarification Notice",
                    "status": "warning",
                    "message": "Problem may be ambiguous but proceeding with best interpretation"
                })
            
            # Stage 2: Check for similar past problems
            logger.info("Stage 2: Checking memory for similar problems...")
            similar_problems = self.memory_system.find_similar_problems(
                parsed_problem.get("problem_text", ""),
                parsed_problem.get("topic", ""),
                n=3
            )
            
            self.execution_trace.append({
                "stage": "Memory Retrieval",
                "status": "completed",
                "similar_found": len(similar_problems)
            })
            
            # Stage 3: RAG Retrieval
            logger.info("Stage 3: Retrieving relevant knowledge...")
            self.execution_trace.append({
                "stage": "RAG Retrieval",
                "status": "started"
            })
            
            rag_context = self.rag_pipeline.retrieve(
                parsed_problem.get("problem_text", "")
            )
            
            self.execution_trace.append({
                "stage": "RAG Retrieval",
                "status": "completed",
                "documents_retrieved": len(rag_context)
            })
            
            # Stage 4: Intent Routing
            logger.info("Stage 4: Determining solution strategy...")
            self.execution_trace.append({
                "stage": "Intent Router Agent",
                "status": "started"
            })
            
            strategy = self.intent_router_agent.execute({
                "parsed_problem": parsed_problem
            })
            
            self.execution_trace.append({
                "stage": "Intent Router Agent",
                "status": "completed",
                "output": strategy
            })
            
            # Stage 5: Solve Problem
            logger.info("Stage 5: Solving problem...")
            self.execution_trace.append({
                "stage": "Solver Agent",
                "status": "started"
            })
            
            solution = self.solver_agent.execute({
                "parsed_problem": parsed_problem,
                "strategy": strategy,
                "rag_context": rag_context
            })
            
            self.execution_trace.append({
                "stage": "Solver Agent",
                "status": "completed",
                "confidence": solution.get("confidence", 0.0)
            })
            
            # Stage 6: Verify Solution
            logger.info("Stage 6: Verifying solution...")
            self.execution_trace.append({
                "stage": "Verifier Agent",
                "status": "started"
            })
            
            verification = self.verifier_agent.execute({
                "parsed_problem": parsed_problem,
                "solution": solution
            })
            
            self.execution_trace.append({
                "stage": "Verifier Agent",
                "status": "completed",
                "output": verification
            })
            
            # Stage 7: Generate Explanation
            logger.info("Stage 7: Generating explanation...")
            self.execution_trace.append({
                "stage": "Explainer Agent",
                "status": "started"
            })
            
            explanation = self.explainer_agent.execute({
                "parsed_problem": parsed_problem,
                "solution": solution,
                "verification": verification
            })
            
            self.execution_trace.append({
                "stage": "Explainer Agent",
                "status": "completed"
            })
            
            # Store interaction in memory
            interaction = {
                "timestamp": timestamp,
                "raw_input": raw_text,
                "input_type": input_type,
                "parsed_problem": parsed_problem,
                "retrieved_context": rag_context,
                "solution": solution,
                "verification": verification,
                "explanation": explanation,
                "similar_problems": [p.get('interaction_id') for p in similar_problems]
            }
            
            interaction_id = self.memory_system.store_interaction(interaction)
            
            # Prepare result
            result = {
                "status": "success",
                "interaction_id": interaction_id,
                "parsed_problem": parsed_problem,
                "strategy": strategy,
                "solution": solution,
                "verification": verification,
                "explanation": explanation,
                "rag_sources": [
                    {"source": doc["source"], "content": doc["content"][:200]}
                    for doc in rag_context
                ],
                "similar_problems": similar_problems,
                "execution_trace": self.execution_trace,
                "requires_hitl": verification.get("requires_hitl", False),
                "needs_clarification": needs_clarification_flag  # Add clarification flag
            }
            
            logger.info(f"Problem solved successfully. Interaction ID: {interaction_id}")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in solve_problem: {e}")
            
            # Check if it's a quota error
            if "quota" in error_msg.lower() or "429" in error_msg:
                self.execution_trace.append({
                    "stage": "Error",
                    "status": "quota_exceeded",
                    "error": "API quota exceeded"
                })
                return {
                    "status": "quota_exceeded",
                    "message": "⚠️ **API Quota Exceeded**\n\n"
                              "You've reached the free tier limit of **20 requests per day**.\n\n"
                              "**Options:**\n"
                              "1. ⏰ Wait for the quota to reset (quotas reset automatically)\n"
                              "2. 🔑 Get a new API key at https://aistudio.google.com/apikey\n"
                              "3. 💳 Upgrade to a paid plan at https://ai.google.dev/pricing\n\n"
                              "**Monitor your usage:** https://ai.dev/usage?tab=rate-limit",
                    "execution_trace": self.execution_trace
                }
            
            self.execution_trace.append({
                "stage": "Error",
                "status": "failed",
                "error": str(e)
            })
            return {
                "status": "error",
                "message": str(e),
                "execution_trace": self.execution_trace
            }
    
    def submit_feedback(self, 
                       interaction_id: str, 
                       feedback: Dict[str, Any]):
        """
        Submit user feedback for an interaction
        
        Args:
            interaction_id: ID of the interaction
            feedback: User feedback data
        """
        try:
            self.memory_system.store_feedback(interaction_id, feedback)
            logger.info(f"Feedback submitted for interaction: {interaction_id}")
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
    
    def store_correction(self, 
                        original: str, 
                        corrected: str, 
                        correction_type: str):
        """
        Store OCR/ASR correction
        
        Args:
            original: Original text
            corrected: Corrected text
            correction_type: 'ocr' or 'asr'
        """
        try:
            self.memory_system.store_user_correction(
                original, corrected, correction_type
            )
            logger.info(f"Correction stored: {correction_type}")
        except Exception as e:
            logger.error(f"Error storing correction: {e}")
