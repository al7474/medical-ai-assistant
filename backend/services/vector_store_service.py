"""
Vector Store Service for RAG implementation using FAISS.
Handles document embeddings storage and semantic search retrieval.
"""

from typing import List, Tuple, Optional
import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


class VectorStoreService:
    """
    Service for managing vector store operations with FAISS.
    Handles document embedding, storage, and retrieval for RAG.
    """
    
    def __init__(self, persist_directory: str = "data/vectorstore"):
        """
        Initialize the vector store service.
        
        Args:
            persist_directory: Directory to persist vector store data
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        try:
            self.embeddings = OpenAIEmbeddings()
            self.available = True
        except Exception as e:
            print(f"⚠️ OpenAI embeddings not available: {e}")
            self.embeddings = None
            self.available = False
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        self._vectorstore = None
    
    def is_available(self) -> bool:
        """Check if vector store service is available (requires OpenAI API key)."""
        return self.available and self.embeddings is not None
    
    def add_documents(
        self,
        documents: List[Document],
        user_id: int,
        collection_name: Optional[str] = None
    ) -> int:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of LangChain Document objects
            user_id: ID of the user who owns these documents
            collection_name: Optional name for the document collection
            
        Returns:
            Number of chunks created
        """
        if not self.is_available():
            raise RuntimeError("Vector store service not available. Configure OpenAI API key.")
        
        # Add metadata to documents
        for doc in documents:
            doc.metadata["user_id"] = user_id
            if collection_name:
                doc.metadata["collection"] = collection_name
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create or update vector store
        if self._vectorstore is None:
            self._vectorstore = FAISS.from_documents(chunks, self.embeddings)
        else:
            self._vectorstore.add_documents(chunks)
        
        # Persist to disk
        self._save_vectorstore(user_id)
        
        return len(chunks)
    
    def add_texts(
        self,
        texts: List[str],
        user_id: int,
        metadatas: Optional[List[dict]] = None
    ) -> int:
        """
        Add texts directly to the vector store.
        
        Args:
            texts: List of text strings to add
            user_id: ID of the user who owns these texts
            metadatas: Optional list of metadata dicts for each text
            
        Returns:
            Number of chunks created
        """
        if not self.is_available():
            raise RuntimeError("Vector store service not available. Configure OpenAI API key.")
        
        # Prepare metadata
        if metadatas is None:
            metadatas = [{"user_id": user_id} for _ in texts]
        else:
            for metadata in metadatas:
                metadata["user_id"] = user_id
        
        # Split texts into chunks
        docs = [Document(page_content=text) for text in texts]
        chunks = self.text_splitter.split_documents(docs)
        
        # Add metadata to chunks
        chunk_texts = [chunk.page_content for chunk in chunks]
        chunk_metadatas = [metadatas[0] for _ in chunks]  # Simplified metadata assignment
        
        # Create or update vector store
        if self._vectorstore is None:
            self._vectorstore = FAISS.from_texts(chunk_texts, self.embeddings, metadatas=chunk_metadatas)
        else:
            self._vectorstore.add_texts(chunk_texts, metadatas=chunk_metadatas)
        
        # Persist to disk
        self._save_vectorstore(user_id)
        
        return len(chunks)
    
    def search(
        self,
        query: str,
        user_id: int,
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """
        Search for relevant documents using semantic similarity.
        
        Args:
            query: Search query string
            user_id: ID of the user (for filtering)
            k: Number of results to return
            
        Returns:
            List of tuples (document, similarity_score)
        """
        if not self.is_available():
            return []
        
        # Load user's vector store if not already loaded
        if self._vectorstore is None:
            self._load_vectorstore(user_id)
        
        if self._vectorstore is None:
            return []
        
        # Perform similarity search with scores
        try:
            results = self._vectorstore.similarity_search_with_score(query, k=k)
            
            # Filter by user_id
            filtered_results = [
                (doc, score) for doc, score in results
                if doc.metadata.get("user_id") == user_id
            ]
            
            return filtered_results
        except Exception as e:
            print(f"Error during vector search: {e}")
            return []
    
    def search_by_user(
        self,
        query: str,
        user_id: int,
        k: int = 4,
        score_threshold: float = 0.7
    ) -> List[Document]:
        """
        Search for relevant documents for a specific user.
        Returns only documents above the score threshold.
        
        Args:
            query: Search query string
            user_id: ID of the user
            k: Number of results to return
            score_threshold: Minimum similarity score (0-1, lower is more similar for FAISS)
            
        Returns:
            List of relevant documents
        """
        results = self.search(query, user_id, k=k)
        
        # Filter by score threshold (FAISS uses distance, lower is better)
        # Convert to similarity score (1 - distance)
        filtered_docs = [
            doc for doc, score in results
            if score < (1 - score_threshold)  # Lower distance = higher similarity
        ]
        
        return filtered_docs
    
    def get_context_for_query(
        self,
        query: str,
        user_id: int,
        k: int = 3
    ) -> str:
        """
        Get formatted context from relevant documents for a query.
        
        Args:
            query: Search query string
            user_id: ID of the user
            k: Number of documents to retrieve
            
        Returns:
            Formatted context string
        """
        relevant_docs = self.search_by_user(query, user_id, k=k)
        
        if not relevant_docs:
            return ""
        
        # Format documents into context
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content.strip()
            context_parts.append(f"[Document {i} - {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def delete_user_documents(self, user_id: int) -> bool:
        """
        Delete all documents for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            True if successful
        """
        vectorstore_path = self._get_vectorstore_path(user_id)
        
        if vectorstore_path.exists():
            import shutil
            shutil.rmtree(vectorstore_path)
            
            # Clear loaded vectorstore if it's for this user
            if self._vectorstore is not None:
                self._vectorstore = None
            
            return True
        
        return False
    
    def _get_vectorstore_path(self, user_id: int) -> Path:
        """Get the path to user's vector store directory."""
        return self.persist_directory / f"user_{user_id}"
    
    def _save_vectorstore(self, user_id: int):
        """Save vector store to disk."""
        if self._vectorstore is None:
            return
        
        vectorstore_path = self._get_vectorstore_path(user_id)
        vectorstore_path.mkdir(parents=True, exist_ok=True)
        
        try:
            self._vectorstore.save_local(str(vectorstore_path))
        except Exception as e:
            print(f"Error saving vector store: {e}")
    
    def _load_vectorstore(self, user_id: int):
        """Load vector store from disk."""
        if not self.is_available():
            return
        
        vectorstore_path = self._get_vectorstore_path(user_id)
        
        if vectorstore_path.exists():
            try:
                self._vectorstore = FAISS.load_local(
                    str(vectorstore_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True  # Required for FAISS
                )
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self._vectorstore = None


# Factory function
def get_vector_store_service() -> VectorStoreService:
    """
    Factory function to create VectorStoreService instance.
    
    Returns:
        VectorStoreService instance
    """
    return VectorStoreService()
