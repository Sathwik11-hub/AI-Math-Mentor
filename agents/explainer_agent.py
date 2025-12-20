"""
Explainer/Tutor Agent - Provides student-friendly explanations
"""
import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExplainerAgent(BaseAgent):
    """Explainer Agent - Creates student-friendly explanations"""
    
    def __init__(self):
        super().__init__(
            name="ExplainerAgent",
            role="Provides clear, student-friendly explanations"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate student-friendly explanation
        
        Args:
            input_data: {
                "parsed_problem": Dict,
                "solution": Dict,
                "verification": Dict
            }
            
        Returns:
            {
                "explanation": str,
                "key_concepts": List[str],
                "common_mistakes": List[str],
                "tips": List[str]
            }
        """
        try:
            parsed_problem = input_data.get("parsed_problem", {})
            solution = input_data.get("solution", {})
            verification = input_data.get("verification", {})
            
            problem_text = parsed_problem.get("problem_text", "")
            topic = parsed_problem.get("topic", "")
            steps = solution.get("steps", [])
            final_answer = solution.get("final_answer", "")
            
            logger.info("Generating student-friendly explanation...")
            
            system_prompt = """You are an Explainer/Tutor Agent for JEE-level mathematics.
Your job is to create clear, student-friendly explanations that help students understand the solution.

You must:
1. Explain WHY each step is taken, not just WHAT
2. Highlight key concepts used
3. Point out common mistakes to avoid
4. Provide helpful tips and intuition
5. Use simple, encouraging language
6. Connect to known formulas and theorems

Your explanation should help a JEE student learn, not just copy the answer.

STRICT OUTPUT FORMAT (JSON only):
{
  "explanation": "detailed step-by-step explanation in friendly language",
  "key_concepts": ["concept1", "concept2"],
  "common_mistakes": ["mistake1 to avoid", "mistake2 to avoid"],
  "tips": ["helpful tip 1", "helpful tip 2"]
}
"""
            
            user_prompt = f"""Create a student-friendly explanation for this solution:

Problem: {problem_text}
Topic: {topic}

Solution Steps:
{chr(10).join(steps)}

Final Answer: {final_answer}

Make it clear, encouraging, and educational. Return ONLY the JSON output."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self._call_llm(messages, temperature=0.5)
            
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
                logger.debug(f"Response was: {response}")
                output = {
                    "explanation": response[:1000],
                    "key_concepts": [topic],
                    "common_mistakes": [],
                    "tips": []
                }
            
            self.log_execution(input_data, output)
            return output
            
        except Exception as e:
            logger.error(f"Error in ExplainerAgent: {e}")
            return {
                "explanation": f"Error generating explanation: {str(e)}",
                "key_concepts": [],
                "common_mistakes": [],
                "tips": []
            }
