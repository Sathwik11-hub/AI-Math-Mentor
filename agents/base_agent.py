"""
Base Agent class for multi-agent system
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from openai import OpenAI

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.client = None
        
    def _initialize_client(self):
        """Lazy initialization of OpenAI client"""
        if self.client is None:
            try:
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise
    
    def _call_llm(self, messages: list, temperature: float = 0.7) -> str:
        """
        Call OpenAI API
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            
        Returns:
            Response content
        """
        self._initialize_client()
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            raise
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Output data from the agent
        """
        pass
    
    def log_execution(self, input_data: Dict, output_data: Dict):
        """Log agent execution"""
        logger.info(f"Agent {self.name} executed successfully")
        logger.debug(f"Input: {input_data}")
        logger.debug(f"Output: {output_data}")
