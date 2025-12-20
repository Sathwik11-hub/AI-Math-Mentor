"""
Verifier/Critic Agent - Verifies solution correctness and identifies issues
"""
import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class VerifierAgent(BaseAgent):
    """Verifier Agent - Checks solution correctness and validity"""
    
    def __init__(self):
        super().__init__(
            name="VerifierAgent",
            role="Verifies mathematical correctness and domain validity"
        )
        self.confidence_threshold = Config.VERIFIER_CONFIDENCE_THRESHOLD
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify solution correctness
        
        Args:
            input_data: {
                "parsed_problem": Dict,
                "solution": Dict from SolverAgent
            }
            
        Returns:
            {
                "is_correct": bool,
                "confidence": float,
                "issues_found": List[str],
                "requires_hitl": bool,
                "verification_details": str
            }
        """
        try:
            parsed_problem = input_data.get("parsed_problem", {})
            solution = input_data.get("solution", {})
            
            problem_text = parsed_problem.get("problem_text", "")
            final_answer = solution.get("final_answer", "")
            steps = solution.get("steps", [])
            
            logger.info(f"Verifying solution: {final_answer[:100]}...")
            
            system_prompt = """You are a Verifier Agent for JEE-level mathematics.
Your critical job is to verify solution correctness and identify any issues.

You must check:
1. Mathematical correctness (substitution verification)
2. Domain validity:
   - √x requires x ≥ 0
   - log(x) requires x > 0
   - division requires denominator ≠ 0
   - tan(x) undefined at x = π/2 + nπ
3. Constraint satisfaction (from problem statement)
4. Common mistake patterns:
   - Sign errors
   - Inequality reversals
   - Domain violations
   - Incorrect formula application
5. Logical consistency of steps

Be STRICT and thorough. If unsure, flag for human review.

STRICT OUTPUT FORMAT (JSON only):
{
  "is_correct": true/false,
  "confidence": 0.95,
  "issues_found": ["issue1", "issue2"] or [],
  "requires_hitl": false,
  "verification_details": "detailed explanation of verification"
}

Set requires_hitl to true if:
- Confidence < 0.8
- Critical issues found
- Domain violations detected
- Cannot verify answer
"""
            
            user_prompt = f"""Verify this solution:

Problem: {problem_text}
Constraints: {parsed_problem.get('constraints', [])}

Solution Steps:
{chr(10).join(steps)}

Final Answer: {final_answer}

Perform thorough verification. Return ONLY the JSON output."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self._call_llm(messages, temperature=0.2)
            
            # Extract JSON from response
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    output = json.loads(json_str)
                else:
                    output = json.loads(response)
                
                # Ensure requires_hitl is set based on confidence threshold
                confidence = output.get('confidence', 0.5)
                if confidence < self.confidence_threshold:
                    output['requires_hitl'] = True
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Response was: {response}")
                output = {
                    "is_correct": False,
                    "confidence": 0.3,
                    "issues_found": ["Failed to parse verification results"],
                    "requires_hitl": True,
                    "verification_details": response[:500]
                }
            
            self.log_execution(input_data, output)
            return output
            
        except Exception as e:
            logger.error(f"Error in VerifierAgent: {e}")
            return {
                "is_correct": False,
                "confidence": 0.0,
                "issues_found": [f"Error in verification: {str(e)}"],
                "requires_hitl": True,
                "verification_details": f"Error: {str(e)}"
            }
