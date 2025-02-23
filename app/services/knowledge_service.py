import json
import os
from typing import Dict

class KnowledgeService:
    def __init__(self):
        self.knowledge_base = self._load_initial_knowledge()
    
    def _load_initial_knowledge(self) -> Dict:
        """Load API documentation from text files."""
        knowledge = {
            'platforms': {},
            'documentation': {}
        }
        
        # Load platform documentation
        docs_dir = os.path.join(os.path.dirname(__file__), '../data/documentation')
        for filename in os.listdir(docs_dir):
            if filename.endswith('.txt'):
                platform_name = filename.replace('.txt', '')
                with open(os.path.join(docs_dir, filename), 'r') as f:
                    knowledge['documentation'][platform_name] = f.read()
        
        return knowledge
    
    def add_platform_knowledge(self, platform: str, documentation: dict):
        """Add or update platform documentation in the knowledge base."""
        if platform not in self.knowledge_base['platforms']:
            self.knowledge_base['platforms'][platform] = {}
            
        self.knowledge_base['platforms'][platform].update(documentation)
        self._persist_knowledge()
    
    def add_mapping_knowledge(self, source_platform: str, target_platform: str, mappings: dict):
        """Add or update mapping rules between platforms."""
        key = f"{source_platform}_to_{target_platform}"
        if key not in self.knowledge_base['mappings']:
            self.knowledge_base['mappings'][key] = {}
            
        self.knowledge_base['mappings'][key].update(mappings)
        self._persist_knowledge()
    
    def _persist_knowledge(self):
        """Persist knowledge base to JSON files."""
        platforms_dir = os.path.join(os.path.dirname(__file__), '../data/platforms')
        os.makedirs(platforms_dir, exist_ok=True)
        
        for platform, data in self.knowledge_base['platforms'].items():
            filepath = os.path.join(platforms_dir, f"{platform}.json")
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)