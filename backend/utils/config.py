"""
Configuration management for AI Math Mentor
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for AI Math Mentor"""
    
    # Gemini / LLM Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    # Default to gemini-2.0-flash (latest fast model) with models/ prefix
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    
    # Confidence Thresholds
    OCR_CONFIDENCE_THRESHOLD = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.7"))
    ASR_CONFIDENCE_THRESHOLD = float(os.getenv("ASR_CONFIDENCE_THRESHOLD", "0.7"))
    VERIFIER_CONFIDENCE_THRESHOLD = float(os.getenv("VERIFIER_CONFIDENCE_THRESHOLD", "0.8"))
    
    # Whisper Configuration
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    
    # RAG Configuration
    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Directories
    MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "./memory"))
    VECTOR_STORE_DIR = Path(os.getenv("VECTOR_STORE_DIR", "./vector_store"))
    KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
    LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Supported Topics
    SUPPORTED_TOPICS = ["algebra", "calculus", "probability", "linear_algebra"]
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env file")
        
        # Create necessary directories
        cls.MEMORY_DIR.mkdir(exist_ok=True)
        cls.VECTOR_STORE_DIR.mkdir(exist_ok=True)
        cls.KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
        cls.LOG_DIR.mkdir(exist_ok=True)
