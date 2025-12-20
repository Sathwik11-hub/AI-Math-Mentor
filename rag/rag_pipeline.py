"""
RAG (Retrieval-Augmented Generation) Pipeline
Handles knowledge base management, chunking, embedding, and retrieval
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class RAGPipeline:
    """RAG Pipeline for knowledge retrieval"""
    
    def __init__(self):
        self.config = Config
        self.vector_store = None
        self.embeddings = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        
    def _initialize_embeddings(self):
        """Initialize embedding model"""
        if self.embeddings is None:
            try:
                logger.info("Initializing embedding model...")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
                logger.info("Embedding model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize embeddings: {e}")
                raise
    
    def load_knowledge_base(self) -> List[Document]:
        """Load all knowledge base documents"""
        documents = []
        kb_dir = Config.KNOWLEDGE_BASE_DIR
        
        if not kb_dir.exists():
            logger.warning(f"Knowledge base directory not found: {kb_dir}")
            return documents
        
        logger.info(f"Loading knowledge base from {kb_dir}")
        
        for file_path in kb_dir.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path.name,
                        "type": "knowledge_base"
                    }
                )
                documents.append(doc)
                logger.info(f"Loaded {file_path.name}")
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        logger.info(f"Loaded {len(documents)} documents from knowledge base")
        return documents
    
    def create_vector_store(self, force_recreate: bool = False):
        """Create or load vector store"""
        vector_store_path = Config.VECTOR_STORE_DIR / "faiss_index"
        
        # Try to load existing vector store
        if not force_recreate and vector_store_path.exists():
            try:
                logger.info("Loading existing vector store...")
                self._initialize_embeddings()
                self.vector_store = FAISS.load_local(
                    str(vector_store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Vector store loaded successfully")
                return
            except Exception as e:
                logger.warning(f"Failed to load vector store: {e}. Creating new one...")
        
        # Create new vector store
        logger.info("Creating new vector store...")
        self._initialize_embeddings()
        
        # Load and chunk documents
        documents = self.load_knowledge_base()
        if not documents:
            logger.warning("No documents loaded from knowledge base")
            return
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
        # Create vector store
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # Save vector store
        Config.VECTOR_STORE_DIR.mkdir(exist_ok=True)
        self.vector_store.save_local(str(vector_store_path))
        logger.info(f"Vector store saved to {vector_store_path}")
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve (default from config)
            
        Returns:
            List of dicts with content and metadata
        """
        if self.vector_store is None:
            logger.warning("Vector store not initialized. Creating...")
            self.create_vector_store()
        
        if self.vector_store is None:
            logger.error("Failed to create vector store")
            return []
        
        k = k or Config.RAG_TOP_K
        
        try:
            logger.info(f"Retrieving top-{k} documents for query: {query[:100]}...")
            docs = self.vector_store.similarity_search(query, k=k)
            
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "metadata": doc.metadata
                })
            
            logger.info(f"Retrieved {len(results)} documents")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def retrieve_with_scores(self, query: str, k: Optional[int] = None) -> List[Dict]:
        """
        Retrieve relevant documents with similarity scores
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of dicts with content, metadata, and scores
        """
        if self.vector_store is None:
            self.create_vector_store()
        
        if self.vector_store is None:
            return []
        
        k = k or Config.RAG_TOP_K
        
        try:
            docs_and_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            results = []
            for doc, score in docs_and_scores:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents with scores: {e}")
            return []
