"""
Solver Agent - Solves mathematical problems using ReAct-style reasoning
"""
import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import setup_logger
import sympy as sp

logger = setup_logger(__name__)


class SolverAgent(BaseAgent):
    """Solver Agent - Solves math problems with step-by-step reasoning"""
    
    def __init__(self):
        super().__init__(
            name="SolverAgent",
            role="Solves mathematical problems using ReAct reasoning"
        )
    
    def _execute_sympy_tool(self, code: str) -> str:
        """Execute SymPy code safely"""
        try:
            # Create a restricted namespace
            namespace = {
                'sp': sp,
                'Symbol': sp.Symbol,
                'symbols': sp.symbols,
                'solve': sp.solve,
                'simplify': sp.simplify,
                'expand': sp.expand,
                'factor': sp.factor,
                'diff': sp.diff,
                'integrate': sp.integrate,
                'limit': sp.limit,
                'sqrt': sp.sqrt,
                'log': sp.log,
                'exp': sp.exp,
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'pi': sp.pi,
                'oo': sp.oo,
                'Matrix': sp.Matrix,
                'det': lambda m: m.det(),
            }
            
            # Execute code
            exec(code, namespace)
            result = namespace.get('result', 'No result variable defined')
            return str(result)
        except Exception as e:
            return f"Error executing code: {str(e)}"
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve mathematical problem with ReAct-style reasoning
        
        Args:
            input_data: {
                "parsed_problem": Dict from ParserAgent,
                "strategy": Dict from IntentRouterAgent,
                "rag_context": List[Dict] from RAG
            }
            
        Returns:
            {
                "steps": List[str],
                "final_answer": str,
                "reasoning": str,
                "confidence": float,
                "tool_calls": List[Dict]
            }
        """
        try:
            parsed_problem = input_data.get("parsed_problem", {})
            strategy = input_data.get("strategy", {})
            rag_context = input_data.get("rag_context", [])
            
            problem_text = parsed_problem.get("problem_text", "")
            topic = parsed_problem.get("topic", "")
            
            logger.info(f"Solving problem: {problem_text[:100]}...")
            
            # Format RAG context
            context_str = "\n\n".join([
                f"Reference from {doc['source']}:\n{doc['content'][:500]}"
                for doc in rag_context[:2]
            ])
            
            system_prompt = f"""You are a Solver Agent for JEE-level mathematics.
You solve problems using ReAct-style reasoning: Thought -> Action -> Observation -> repeat.

Topic: {topic}
Strategy: {strategy.get('approach', 'step-by-step solving')}

Reference Knowledge:
{context_str}

You must:
1. Think through the problem step-by-step
2. Use SymPy tools when helpful (provide Python code)
3. Verify each step
4. Provide clear reasoning
5. Give final answer

STRICT OUTPUT FORMAT (JSON only):
{{
  "steps": [
    "Step 1: Identify the equation...",
    "Step 2: Apply quadratic formula...",
    ...
  ],
  "final_answer": "x = -2 or x = -3",
  "reasoning": "detailed explanation of solution process",
  "confidence": 0.95,
  "sympy_code": "optional Python/SymPy code used"
}}
"""
            
            user_prompt = f"""Solve this problem:

Problem: {problem_text}
Variables: {parsed_problem.get('variables', [])}
Constraints: {parsed_problem.get('constraints', [])}
Equations: {parsed_problem.get('equations', [])}

Provide step-by-step solution. Return ONLY the JSON output."""
            
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
                
                # If SymPy code is provided, execute it
                if 'sympy_code' in output and output['sympy_code']:
                    sympy_result = self._execute_sympy_tool(output['sympy_code'])
                    output['sympy_result'] = sympy_result
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Response was: {response}")
                output = {
                    "steps": ["Failed to parse solution steps"],
                    "final_answer": "Error in solving",
                    "reasoning": response[:500],
                    "confidence": 0.3
                }
            
            self.log_execution(input_data, output)
            return output
            
        except Exception as e:
            logger.error(f"Error in SolverAgent: {e}")
            return {
                "steps": [],
                "final_answer": "Error occurred during solving",
                "reasoning": f"Error: {str(e)}",
                "confidence": 0.0
            }
