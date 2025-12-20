"""
Parser Agent - Converts raw input to structured problem
"""
import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ParserAgent(BaseAgent):
    """Parser Agent - Structures raw math problems"""
    
    def __init__(self):
        super().__init__(
            name="ParserAgent",
            role="Cleans input and structures math problems"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw input into structured problem format
        
        Args:
            input_data: {
                "raw_text": str,
                "input_type": "text|image|audio"
            }
            
        Returns:
            {
                "problem_text": str,
                "topic": str,
                "variables": List[str],
                "constraints": List[str],
                "equations": List[str],
                "needs_clarification": bool,
                "confidence": float,
                "reasoning": str
            }
        """
        try:
            raw_text = input_data.get("raw_text", "")
            input_type = input_data.get("input_type", "text")
            
            logger.info(f"Parsing input: {raw_text[:100]}...")
            
            system_prompt = """You are a Parser Agent for a JEE-level math mentor system.
Your job is to analyze raw mathematical problem text and structure it into a standard format.

You must:
1. Clean OCR/ASR noise
2. Standardize mathematical notation
3. Identify the topic (algebra, calculus, probability, or linear_algebra)
4. Extract variables, constraints, and equations
5. Detect if the problem is ambiguous or needs clarification

STRICT OUTPUT FORMAT (JSON only):
{
  "problem_text": "cleaned problem statement",
  "topic": "algebra|calculus|probability|linear_algebra",
  "variables": ["x", "y"],
  "constraints": ["x > 0", "x is real"],
  "equations": ["x^2 + 5x + 6 = 0"],
  "needs_clarification": false,
  "confidence": 0.95,
  "reasoning": "brief explanation of parsing decisions"
}

If the problem is unclear, incomplete, or ambiguous, set needs_clarification to true.
Only work with JEE-level topics: algebra, calculus (basic), probability, linear algebra.
"""
            
            user_prompt = f"""Parse this mathematical problem:

Raw Input: {raw_text}
Input Type: {input_type}

Return ONLY the JSON output, no additional text."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self._call_llm(messages, temperature=0.3)
            
            # Extract JSON from response
            try:
                # Try to find JSON in response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    parsed_output = json.loads(json_str)
                else:
                    parsed_output = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Response was: {response}")
                # Return a default structure
                parsed_output = {
                    "problem_text": raw_text,
                    "topic": "unknown",
                    "variables": [],
                    "constraints": [],
                    "equations": [],
                    "needs_clarification": True,
                    "confidence": 0.3,
                    "reasoning": "Failed to parse problem structure"
                }
            
            self.log_execution(input_data, parsed_output)
            return parsed_output
            
        except Exception as e:
            logger.error(f"Error in ParserAgent: {e}")
            return {
                "problem_text": input_data.get("raw_text", ""),
                "topic": "unknown",
                "variables": [],
                "constraints": [],
                "equations": [],
                "needs_clarification": True,
                "confidence": 0.0,
                "reasoning": f"Error: {str(e)}"
            }
