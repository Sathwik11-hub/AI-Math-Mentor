"""
Memory System for Self-Learning
Stores interactions and enables pattern reuse
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class MemorySystem:
    """Memory system for storing and retrieving past interactions"""
    
    def __init__(self):
        self.memory_dir = Config.MEMORY_DIR
        self.memory_dir.mkdir(exist_ok=True)
        self.interactions_file = self.memory_dir / "interactions.jsonl"
        self.corrections_file = self.memory_dir / "corrections.json"
        self._load_corrections()
    
    def _load_corrections(self):
        """Load learned corrections from file"""
        if self.corrections_file.exists():
            try:
                with open(self.corrections_file, 'r') as f:
                    self.corrections = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load corrections: {e}")
                self.corrections = {
                    "ocr_corrections": {},
                    "asr_corrections": {}
                }
        else:
            self.corrections = {
                "ocr_corrections": {},
                "asr_corrections": {}
            }
    
    def _save_corrections(self):
        """Save corrections to file"""
        try:
            with open(self.corrections_file, 'w') as f:
                json.dump(self.corrections, f, indent=2)
            logger.info("Corrections saved successfully")
        except Exception as e:
            logger.error(f"Failed to save corrections: {e}")
    
    def store_interaction(self, interaction: Dict[str, Any]) -> str:
        """
        Store a complete interaction
        
        Args:
            interaction: {
                "timestamp": str,
                "raw_input": str,
                "input_type": str,
                "parsed_problem": Dict,
                "retrieved_context": List[Dict],
                "solution": Dict,
                "verification": Dict,
                "explanation": Dict,
                "user_feedback": Optional[Dict]
            }
            
        Returns:
            Interaction ID
        """
        try:
            # Generate interaction ID
            interaction_id = hashlib.md5(
                f"{interaction.get('timestamp', '')}_{interaction.get('raw_input', '')}".encode()
            ).hexdigest()[:16]
            
            interaction['interaction_id'] = interaction_id
            
            # Append to interactions file (JSONL format)
            with open(self.interactions_file, 'a') as f:
                f.write(json.dumps(interaction) + '\n')
            
            logger.info(f"Stored interaction: {interaction_id}")
            return interaction_id
            
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
            return ""
    
    def get_interaction(self, interaction_id: str) -> Optional[Dict]:
        """Retrieve a specific interaction by ID"""
        try:
            if not self.interactions_file.exists():
                return None
            
            with open(self.interactions_file, 'r') as f:
                for line in f:
                    interaction = json.loads(line.strip())
                    if interaction.get('interaction_id') == interaction_id:
                        return interaction
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve interaction: {e}")
            return None
    
    def get_recent_interactions(self, n: int = 10) -> List[Dict]:
        """Get n most recent interactions"""
        try:
            if not self.interactions_file.exists():
                return []
            
            interactions = []
            with open(self.interactions_file, 'r') as f:
                for line in f:
                    interactions.append(json.loads(line.strip()))
            
            # Return most recent n
            return interactions[-n:] if len(interactions) > n else interactions
            
        except Exception as e:
            logger.error(f"Failed to get recent interactions: {e}")
            return []
    
    def find_similar_problems(self, problem_text: str, topic: str, n: int = 3) -> List[Dict]:
        """
        Find similar past problems
        
        Args:
            problem_text: Current problem text
            topic: Problem topic
            n: Number of similar problems to return
            
        Returns:
            List of similar past interactions
        """
        try:
            if not self.interactions_file.exists():
                return []
            
            # Simple similarity: same topic and keyword matching
            # In production, use embeddings for better similarity
            problem_keywords = set(problem_text.lower().split())
            
            similar = []
            with open(self.interactions_file, 'r') as f:
                for line in f:
                    interaction = json.loads(line.strip())
                    past_problem = interaction.get('parsed_problem', {})
                    
                    # Check topic match
                    if past_problem.get('topic') != topic:
                        continue
                    
                    # Check keyword overlap
                    past_text = past_problem.get('problem_text', '').lower()
                    past_keywords = set(past_text.split())
                    overlap = len(problem_keywords & past_keywords)
                    
                    if overlap > 2:  # At least 2 common words
                        interaction['similarity_score'] = overlap
                        similar.append(interaction)
            
            # Sort by similarity and return top n
            similar.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            return similar[:n]
            
        except Exception as e:
            logger.error(f"Failed to find similar problems: {e}")
            return []
    
    def store_user_correction(self, 
                            original: str, 
                            corrected: str, 
                            correction_type: str):
        """
        Store user corrections for OCR/ASR
        
        Args:
            original: Original text from OCR/ASR
            corrected: User-corrected text
            correction_type: 'ocr' or 'asr'
        """
        try:
            if correction_type == 'ocr':
                self.corrections['ocr_corrections'][original] = corrected
            elif correction_type == 'asr':
                self.corrections['asr_corrections'][original] = corrected
            
            self._save_corrections()
            logger.info(f"Stored {correction_type} correction: {original} -> {corrected}")
            
        except Exception as e:
            logger.error(f"Failed to store correction: {e}")
    
    def apply_learned_corrections(self, text: str, correction_type: str) -> str:
        """
        Apply learned corrections to new input
        
        Args:
            text: Input text
            correction_type: 'ocr' or 'asr'
            
        Returns:
            Corrected text
        """
        try:
            corrections_dict = (
                self.corrections.get('ocr_corrections', {}) 
                if correction_type == 'ocr' 
                else self.corrections.get('asr_corrections', {})
            )
            
            corrected_text = text
            for original, corrected in corrections_dict.items():
                if original in corrected_text:
                    corrected_text = corrected_text.replace(original, corrected)
                    logger.info(f"Applied correction: {original} -> {corrected}")
            
            return corrected_text
            
        except Exception as e:
            logger.error(f"Failed to apply corrections: {e}")
            return text
    
    def store_feedback(self, 
                      interaction_id: str, 
                      feedback: Dict[str, Any]):
        """
        Store user feedback for an interaction
        
        Args:
            interaction_id: ID of the interaction
            feedback: {
                "approved": bool,
                "correct_answer": Optional[str],
                "comments": Optional[str]
            }
        """
        try:
            # For simplicity, we'll append feedback as a new entry
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "interaction_id": interaction_id,
                "feedback": feedback
            }
            
            feedback_file = self.memory_dir / "feedback.jsonl"
            with open(feedback_file, 'a') as f:
                f.write(json.dumps(feedback_entry) + '\n')
            
            logger.info(f"Stored feedback for interaction: {interaction_id}")
            
        except Exception as e:
            logger.error(f"Failed to store feedback: {e}")
