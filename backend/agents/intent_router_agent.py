"""
Intent Router Agent - Selects solution strategy and tools
"""
import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IntentRouterAgent(BaseAgent):
    """Intent Router Agent - Routes problems to appropriate solution strategies"""
    
    def __init__(self):
        super().__init__(
            name="IntentRouterAgent",
            role="Determines solution strategy and required tools"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine solution strategy based on parsed problem
        
        Args:
            input_data: {
                "parsed_problem": Dict from ParserAgent
            }
            
        Returns:
            {
                "strategy": str,
                "tools": List[str],
                "approach": str,
                "confidence": float
            }
        """
        try:
            parsed_problem = input_data.get("parsed_problem", {})
            topic = parsed_problem.get("topic", "unknown")
            problem_text = parsed_problem.get("problem_text", "")
            
            logger.info(f"Routing problem with topic: {topic}")
            
            system_prompt = """You are an Intent Router Agent for a JEE-level math mentor.
Your job is to analyze a parsed problem and determine the best solution strategy and tools.

Available strategies:
- symbolic_manipulation: Use SymPy for algebraic manipulation
- numerical_computation: Use Python/NumPy for numerical calculations
- step_by_step_derivation: Derivatives, limits, integrals
- probability_analysis: Combinatorics, probability calculations
- matrix_operations: Linear algebra computations

Available tools:
- sympy: Symbolic mathematics
- numpy: Numerical computations
- scipy: Scientific computing
- manual: Step-by-step manual solving

STRICT OUTPUT FORMAT (JSON only):
{
  "strategy": "name of primary strategy",
  "tools": ["tool1", "tool2"],
  "approach": "detailed approach description",
  "confidence": 0.9
}
"""
            
            user_prompt = f"""Determine the solution strategy for this problem:

Topic: {topic}
Problem: {problem_text}
Variables: {parsed_problem.get('variables', [])}
Equations: {parsed_problem.get('equations', [])}

Return ONLY the JSON output."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self._call_llm(messages, temperature=0.3)
            
            # Extract JSON from response
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    output = json.loads(json_str)
                else:
                    output = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                # Return default strategy
                output = {
                    "strategy": "manual",
                    "tools": ["manual"],
                    "approach": "Solve step-by-step manually",
                    "confidence": 0.5
                }
            
            self.log_execution(input_data, output)
            return output
            
        except Exception as e:
            logger.error(f"Error in IntentRouterAgent: {e}")
            return {
                "strategy": "manual",
                "tools": ["manual"],
                "approach": f"Error in routing: {str(e)}",
                "confidence": 0.0
            }
