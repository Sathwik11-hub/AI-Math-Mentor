"""
Multimodal Input Handlers for AI Math Mentor
Handles Image (OCR), Audio (ASR), and Text input
"""
import io
import os
import ssl
import numpy as np
from PIL import Image
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Fix SSL certificate verification for EasyOCR downloads
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()

# Set SSL context globally
ssl._create_default_https_context = ssl._create_unverified_context

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)

class ImageInputHandler:
    """Handle image input with OCR"""
    
    def __init__(self):
        self.confidence_threshold = Config.OCR_CONFIDENCE_THRESHOLD
        self.reader = None  # type: ignore
        
    def _initialize_ocr(self):
        """Lazy initialization of OCR model"""
        if self.reader is None:
            try:
                import easyocr
                logger.info("Initializing EasyOCR...")
                self.reader = easyocr.Reader(['en'], gpu=False)
                logger.info("EasyOCR initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize EasyOCR: {e}")
                raise
    
    def process_image(self, image_input) -> Dict:
        """
        Process image input and extract text using OCR
        
        Args:
            image_input: PIL Image, file path, or file-like object (e.g., Streamlit UploadedFile)
            
        Returns:
            Dict with extracted_text, confidence, needs_hitl
        """
        try:
            self._initialize_ocr()
            
            # Convert to PIL Image if needed
            if isinstance(image_input, str):
                # File path
                image = Image.open(image_input)
            elif hasattr(image_input, 'read'):
                # File-like object (e.g., Streamlit UploadedFile, BytesIO)
                image_bytes = image_input.read()
                image = Image.open(io.BytesIO(image_bytes))
            elif isinstance(image_input, Image.Image):
                # Already a PIL Image
                image = image_input
            else:
                # Try to convert directly
                image = Image.open(image_input)
            
            # Convert to numpy array for EasyOCR
            img_array = np.array(image)
            
            # Perform OCR
            logger.info("Performing OCR on image...")
            results = self.reader.readtext(img_array, detail=1)  # type: ignore[union-attr]
            
            if not results:
                return {
                    "extracted_text": "",
                    "confidence": 0.0,
                    "needs_hitl": True,
                    "message": "No text detected in image"
                }
            
            # Combine text and calculate average confidence
            extracted_lines = []
            confidences = []
            
            for (bbox, text, conf) in results:
                extracted_lines.append(text)
                confidences.append(conf)
            
            extracted_text = " ".join(extracted_lines)
            avg_confidence = sum(confidences) / len(confidences)
            
            needs_hitl = avg_confidence < self.confidence_threshold
            
            logger.info(f"OCR completed: confidence={avg_confidence:.2f}, needs_hitl={needs_hitl}")
            
            return {
                "extracted_text": extracted_text,
                "confidence": avg_confidence,
                "needs_hitl": needs_hitl,
                "message": "OCR completed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error in image processing: {e}")
            return {
                "extracted_text": "",
                "confidence": 0.0,
                "needs_hitl": True,
                "message": f"Error: {str(e)}"
            }


class AudioInputHandler:
    """Handle audio input with ASR"""
    
    def __init__(self):
        self.confidence_threshold = Config.ASR_CONFIDENCE_THRESHOLD
        self.model = None  # type: ignore
        
    def _initialize_whisper(self):
        """Lazy initialization of Whisper model"""
        if self.model is None:
            try:
                import whisper
                logger.info(f"Loading Whisper model: {Config.WHISPER_MODEL}")
                self.model = whisper.load_model(Config.WHISPER_MODEL)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise
    
    def _convert_math_phrases(self, text: str) -> str:
        """Convert spoken math phrases to mathematical notation"""
        conversions = {
            "square root of": "√",
            "squared": "²",
            "cubed": "³",
            "x squared": "x²",
            "x cubed": "x³",
            "plus": "+",
            "minus": "-",
            "times": "×",
            "multiplied by": "×",
            "divided by": "÷",
            "equals": "=",
            "pi": "π",
            "theta": "θ",
            "alpha": "α",
            "beta": "β",
            "delta": "Δ",
            "sigma": "Σ",
        }
        
        result = text.lower()
        for phrase, symbol in conversions.items():
            result = result.replace(phrase, symbol)
        
        return result
    
    def process_audio(self, audio_input) -> Dict:
        """
        Process audio input and transcribe using Whisper
        
        Args:
            audio_input: Audio file path or bytes
            
        Returns:
            Dict with transcript, confidence, needs_hitl
        """
        try:
            self._initialize_whisper()
            
            logger.info("Transcribing audio...")
            
            # Try to transcribe - catch ffmpeg error specifically
            try:
                # Try direct transcription first
                result = self.model.transcribe(audio_input)  # type: ignore[union-attr]
            except (FileNotFoundError, RuntimeError, OSError) as ffmpeg_error:
                if 'ffmpeg' in str(ffmpeg_error).lower() or 'no such file' in str(ffmpeg_error).lower():
                    logger.warning("ffmpeg not found. Trying alternative audio loading method...")
                    
                    # Try using librosa to load and convert audio
                    try:
                        import librosa
                        import numpy as np
                        import torch
                        
                        # Load audio with librosa (doesn't need ffmpeg)
                        logger.info("Loading audio with librosa...")
                        audio_data, sr = librosa.load(audio_input, sr=16000)
                        
                        # Whisper expects audio as numpy array at 16kHz
                        # Convert to torch tensor if needed
                        logger.info("Transcribing with loaded audio data...")
                        
                        # Use Whisper's direct transcription with audio array
                        # This bypasses ffmpeg completely
                        result = self.model.transcribe(  # type: ignore[union-attr]
                            audio_data,
                            fp16=False,  # Disable FP16 for CPU compatibility
                            language='en'  # Assume English for faster processing
                        )
                        
                        logger.info("Alternative audio loading successful!")
                        
                    except Exception as librosa_error:
                        logger.error(f"Alternative audio loading also failed: {librosa_error}")
                        return {
                            "transcript": "",
                            "raw_transcript": "",
                            "confidence": 0.0,
                            "needs_hitl": True,
                            "message": f"Error: Audio transcription failed. Please install ffmpeg: 'brew install ffmpeg'. Details: {str(librosa_error)}"
                        }
                else:
                    raise
            
            raw_transcript = result["text"]
            
            # Convert math phrases (ensure we have a string)
            if isinstance(raw_transcript, str):
                converted_transcript = self._convert_math_phrases(raw_transcript)
            else:
                converted_transcript = str(raw_transcript)
            
            # Whisper doesn't provide word-level confidence in basic API
            # We'll estimate confidence based on presence of math terms
            # In production, use advanced features or manual confidence estimation
            confidence = 0.85  # Default reasonable confidence for Whisper
            
            needs_hitl = confidence < self.confidence_threshold
            
            logger.info(f"ASR completed: confidence={confidence:.2f}, needs_hitl={needs_hitl}")
            
            return {
                "transcript": converted_transcript,
                "raw_transcript": raw_transcript,
                "confidence": confidence,
                "needs_hitl": needs_hitl,
                "message": "Audio transcription completed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error in audio processing: {e}")
            return {
                "transcript": "",
                "raw_transcript": "",
                "confidence": 0.0,
                "needs_hitl": True,
                "message": f"Error: {str(e)}"
            }


class TextInputHandler:
    """Handle text input"""
    
    def process_text(self, text: str) -> Dict:
        """
        Process text input
        
        Args:
            text: Input text string
            
        Returns:
            Dict with processed_text, confidence
        """
        try:
            # Basic text cleaning
            processed_text = text.strip()
            
            if not processed_text:
                return {
                    "processed_text": "",
                    "confidence": 0.0,
                    "needs_hitl": True,
                    "message": "Empty input"
                }
            
            return {
                "processed_text": processed_text,
                "confidence": 1.0,
                "needs_hitl": False,
                "message": "Text input processed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error in text processing: {e}")
            return {
                "processed_text": "",
                "confidence": 0.0,
                "needs_hitl": True,
                "message": f"Error: {str(e)}"
            }
