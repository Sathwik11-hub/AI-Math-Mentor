"""Base Agent class for multi-agent system using Gemini"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time
import re

import google.generativeai as genai  # type: ignore[attr-defined]

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents using Gemini"""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self._model = None

    def _initialize_client(self) -> None:
        """Lazy initialization of Gemini client and model.

        Uses GEMINI_API_KEY and GEMINI_MODEL from Config.
        """
        if self._model is not None:
            return

        try:
            # Ensure we have a usable model name
            model_name = Config.GEMINI_MODEL or "gemini-1.5-flash"

            # Configure the client
            genai.configure(api_key=Config.GEMINI_API_KEY)  # type: ignore[attr-defined]

            # Create model instance
            self._model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
            logger.info(f"Initialized Gemini model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise

    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Convert chat-style messages into a single prompt string."""
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            parts.append(f"{role}: {content}")
        return "\n".join(parts)

    def _call_llm(self, messages: list, temperature: float = 0.7, max_retries: int = 3) -> str:
        """Call Gemini API with a chat-style message list with retry logic.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            temperature: Sampling temperature.
            max_retries: Maximum number of retry attempts for quota errors.

        Returns:
            Response content as string.
        """
        self._initialize_client()
        prompt = self._messages_to_prompt(messages)

        last_error = None
        for attempt in range(max_retries):
            try:
                response = self._model.generate_content(  # type: ignore[operator]
                    prompt,
                    generation_config={
                        "temperature": temperature,
                    },
                )
                # google-generativeai responses expose `.text` for the main content
                text = getattr(response, "text", None)
                if not text:
                    logger.error("Gemini response had no text content.")
                    raise ValueError("Gemini response had no text content.")
                return text
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Check if it's a quota error (429)
                if "429" in error_msg or "quota" in error_msg.lower():
                    # Try to extract retry delay from error message
                    retry_delay = self._extract_retry_delay(error_msg)
                    
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Quota exceeded. Retrying in {retry_delay} seconds "
                            f"(attempt {attempt + 1}/{max_retries})..."
                        )
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error(
                            f"Quota exceeded after {max_retries} attempts. "
                            "Please wait and try again later."
                        )
                        raise Exception(
                            f"API quota exceeded. You've used all 20 requests for today. "
                            f"Please wait {retry_delay} seconds or upgrade your plan at "
                            "https://ai.google.dev/gemini-api/docs/rate-limits"
                        )
                else:
                    # Non-quota error, raise immediately
                    logger.error(f"Error calling Gemini LLM: {e}")
                    raise
        
        # If we exhausted all retries, raise the last error
        if last_error:
            raise last_error
        raise Exception("Failed to call LLM after all retries")
    
    def _extract_retry_delay(self, error_msg: str) -> float:
        """Extract retry delay from error message or use exponential backoff.
        
        Args:
            error_msg: Error message from API
            
        Returns:
            Delay in seconds
        """
        # Try to extract "Please retry in X.XXs" from error message
        match = re.search(r'retry in ([\d.]+)s', error_msg)
        if match:
            return float(match.group(1))
        
        # Check for daily quota limit message
        if "GenerateRequestsPerDayPerProjectPerModel" in error_msg:
            logger.error("Daily quota limit reached (20 requests/day for free tier)")
            return 3600  # Wait 1 hour for daily quota
        
        # Default exponential backoff: 10 seconds
        return 10.0

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic

        Args:
            input_data: Input data for the agent

        Returns:
            Output data from the agent
        """
        raise NotImplementedError

    def log_execution(self, input_data: Dict, output_data: Dict) -> None:
        """Log agent execution"""
        logger.info(f"Agent {self.name} executed successfully")
        logger.debug(f"Input: {input_data}")
        logger.debug(f"Output: {output_data}")