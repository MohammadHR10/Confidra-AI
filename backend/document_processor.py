import json
import os
import re
from typing import List, Dict, Any
from datetime import datetime

class DocumentProcessor:
    def __init__(self, data_file="data/contract.json"):
        self.data_file = data_file
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing contract data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.contracts = json.load(f)
        else:
            self.contracts = []
    
    def save_data(self):
        """Save contract data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.contracts, f, indent=2)
    
    def extract_clauses_from_text(self, text: str, document_name: str, sensitivity: str = "public") -> List[Dict[str, Any]]:
        """
        Extract clauses from document text using pattern matching
        This is a simple implementation - could be enhanced with NLP
        """
        clauses = []
        
        # Split text into sections based on numbered items or clear breaks
        sections = self._split_into_sections(text)
        
        for i, section in enumerate(sections):
            if section.strip():
                clause_data = self._analyze_clause(section, document_name, sensitivity)
                if clause_data:
                    clauses.append(clause_data)
        
        return clauses
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into meaningful sections"""
        # Split by numbered sections (1., 2., etc.)
        numbered_sections = re.split(r'\n\d+\.\s+', text)
        
        # If no numbered sections, split by paragraphs
        if len(numbered_sections) <= 1:
            numbered_sections = text.split('\n\n')
        
        # Clean up sections
        sections = []
        for section in numbered_sections:
            cleaned = section.strip()
            if len(cleaned) > 20:  # Only keep substantial sections
                sections.append(cleaned)
        
        return sections
    
    def _analyze_clause(self, clause_text: str, document_name: str, sensitivity: str) -> Dict[str, Any]:
        """Analyze a clause and determine its properties"""
        clause_lower = clause_text.lower()
        
        # Determine clause type and sensitivity based on content
        clause_type = self._determine_clause_type(clause_lower)
        final_sensitivity = self._determine_sensitivity(clause_lower, sensitivity)
        
        return {
            "clause": clause_text[:200] + "..." if len(clause_text) > 200 else clause_text,
            "full_text": clause_text,
            "sensitivity": final_sensitivity,
            "type": clause_type,
            "document": document_name,
            "timestamp": datetime.now().isoformat()
        }
    
    def _determine_clause_type(self, clause_text: str) -> str:
        """Determine the type of clause based on content"""
        if any(word in clause_text for word in ['salary', 'compensation', 'pay', 'bonus', 'equity']):
            return "compensation"
        elif any(word in clause_text for word in ['vacation', 'pto', 'sick', 'holiday', 'leave']):
            return "benefits"
        elif any(word in clause_text for word in ['confidential', 'proprietary', 'trade secret', 'non-disclosure']):
            return "confidentiality"
        elif any(word in clause_text for word in ['termination', 'notice', 'severance']):
            return "termination"
        elif any(word in clause_text for word in ['duties', 'responsibilities', 'job', 'position']):
            return "job_description"
        elif any(word in clause_text for word in ['location', 'hours', 'work', 'office']):
            return "work_conditions"
        else:
            return "general"
    
    def _determine_sensitivity(self, clause_text: str, default_sensitivity: str) -> str:
        """Determine sensitivity level based on content"""
        # Check for highly sensitive financial information
        if any(word in clause_text for word in ['$', 'salary', 'bonus', 'equity', 'stock', 'rsu']):
            return "protected"
        
        # Check for confidential information
        if any(word in clause_text for word in ['confidential', 'proprietary', 'trade secret', 'personal']):
            return "protected"
        
        # Check for public information
        if any(word in clause_text for word in ['job title', 'start date', 'location', 'hours', 'benefits']):
            return "public"
        
        return default_sensitivity
    
    def process_document(self, text: str, filename: str, sensitivity: str = "public") -> Dict[str, Any]:
        """Process a complete document and add it to the knowledge base"""
        try:
            # Extract clauses from the document
            clauses = self.extract_clauses_from_text(text, filename, sensitivity)
            
            # Add clauses to the contract data
            self.contracts.extend(clauses)
            
            # Save updated data
            self.save_data()
            
            return {
                "success": True,
                "clauses_added": len(clauses),
                "document": filename,
                "message": f"Successfully processed {len(clauses)} clauses from {filename}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to process document {filename}"
            }
    
    def get_public_clauses(self) -> List[str]:
        """Get all public clauses for context"""
        return [contract["clause"] for contract in self.contracts if contract["sensitivity"] == "public"]
    
    def get_protected_clauses(self) -> List[str]:
        """Get all protected clauses"""
        return [contract["clause"] for contract in self.contracts if contract["sensitivity"] == "protected"]
    
    def search_clauses(self, query: str, include_protected: bool = False) -> List[Dict[str, Any]]:
        """Search for relevant clauses based on query"""
        query_lower = query.lower()
        relevant_clauses = []
        
        for contract in self.contracts:
            if contract["sensitivity"] == "public" or (include_protected and contract["sensitivity"] == "protected"):
                if any(word in contract["full_text"].lower() for word in query_lower.split()):
                    relevant_clauses.append(contract)
        
        return relevant_clauses

# Global instance
doc_processor = DocumentProcessor()
