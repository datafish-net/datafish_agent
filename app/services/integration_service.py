from typing import Dict
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class IntegrationService:
    def __init__(self):
        # Only pass supported parameters
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  
            temperature=0,
            api_key=api_key,
            max_retries=3,
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def execute(self, source_platform: str, target_platform: str, source_token: str, target_token: str) -> Dict:
        """Execute integration between platforms using AI."""
        try:
            # Load platform documentation
            source_docs = self._load_documentation(source_platform)
            target_docs = self._load_documentation(target_platform)
            
            # Add tokens to environment for generated code to use
            os.environ[f'{source_platform.upper()}_TOKEN'] = source_token
            os.environ[f'{target_platform.upper()}_TOKEN'] = target_token
            
            # First, generate code to fetch sample data from both platforms
            sample_data_code = self._generate_sample_data_code(
                source_platform,
                target_platform,
                source_docs,
                target_docs
            )
            
            # Execute sample data fetching code
            sample_data = self._execute_sample_data_code(sample_data_code)
            
            if 'error' in sample_data:
                return sample_data
            
            # Now generate integration code with sample data understanding
            code = self._generate_integration_code(
                source_platform, 
                target_platform,
                source_docs, 
                target_docs,
                sample_data
            )
            
            # Execute generated code
            result = self._execute_generated_code(code)
            
            # Clean up environment variables
            os.environ.pop(f'{source_platform.upper()}_TOKEN', None)
            os.environ.pop(f'{target_platform.upper()}_TOKEN', None)
            
            return result
            
        except Exception as e:
            # Clean up environment variables in case of error
            os.environ.pop(f'{source_platform.upper()}_TOKEN', None)
            os.environ.pop(f'{target_platform.upper()}_TOKEN', None)
            return {'error': f"Integration failed: {str(e)}"}
    
    def _load_documentation(self, platform: str) -> str:
        """Load platform documentation from file."""
        docs_path = os.path.join(
            os.path.dirname(__file__), 
            f'../data/documentation/{platform}_documentation.txt'
        )
        with open(docs_path, 'r') as f:
            return f.read()
    
    def _generate_sample_data_code(
        self,
        source_platform: str,
        target_platform: str,
        source_docs: str,
        target_docs: str
    ) -> Dict:
        """Generate code to fetch sample data from both platforms."""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert system integrator. Generate Python code to fetch sample data from both platforms.
            The code should return example data structures that will help understand the mapping between platforms.
            Return the code as a JSON object with the following structure:
            {
                "source_fetch_code": "async Python code to fetch sample data from source",
                "target_fetch_code": "async Python code to fetch sample data from target",
                "requirements": ["list of required packages"]
            }"""),
            HumanMessage(content=f"""
            Generate code to fetch sample data from {source_platform} and {target_platform}.

            Source Platform ({source_platform}) Documentation:
            {source_docs}

            Target Platform ({target_platform}) Documentation:
            {target_docs}

            Requirements:
            1. Use environment variables for tokens ({source_platform.upper()}_TOKEN and {target_platform.upper()}_TOKEN)
            2. Include proper error handling
            3. Use async/await for API calls
            4. Include type hints
            5. Fetch representative sample data from both platforms
            
            Generate production-ready Python code that can be executed directly.
            """)
        ])
        
        response = self.llm.invoke(prompt)
        return response.content

    def _generate_integration_code(
        self, 
        source_platform: str, 
        target_platform: str,
        source_docs: str,
        target_docs: str,
        sample_data: Dict
    ) -> Dict:
        """Generate integration code using LangChain."""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert system integrator. Generate Python code for integrating between different platforms.
            Analyze the API documentation and sample data structures to create a complete integration solution.
            Include all necessary API calls, data transformation, and error handling.
            Return only the executable Python code as a JSON object with the following structure:
            {
                "fetch_code": "async Python code to fetch data from source",
                "transform_code": "Python code to transform data",
                "upload_code": "async Python code to upload to target",
                "requirements": ["list of required packages"]
            }"""),
            HumanMessage(content=f"""
            Create an integration between {source_platform} and {target_platform}.

            Source Platform ({source_platform}) Documentation:
            {source_docs}

            Target Platform ({target_platform}) Documentation:
            {target_docs}

            Source Platform Sample Data Structure:
            {sample_data['source_sample']}

            Target Platform Sample Data Structure:
            {sample_data['target_sample']}

            Requirements:
            1. Use environment variables for tokens ({source_platform.upper()}_TOKEN and {target_platform.upper()}_TOKEN)
            2. Include proper error handling
            3. Use async/await for API calls
            4. Include type hints
            5. Transform data to match target platform's schema based on the sample data structures
            
            Generate production-ready Python code that can be executed directly.
            """)
        ])
        
        response = self.llm.invoke(prompt)
        return response.content

    def _execute_sample_data_code(self, code: Dict) -> Dict:
        """Execute code to fetch sample data from both platforms."""
        import tempfile
        import importlib.util
        import asyncio
        
        # Create temporary module
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
            # Write all code sections
            f.write(code['source_fetch_code'] + '\n')
            f.write(code['target_fetch_code'] + '\n')
            
            # Write main execution function
            f.write("""
async def fetch_sample_data():
    try:
        # Fetch sample data from both platforms
        source_sample = await fetch_source_sample()
        target_sample = await fetch_target_sample()
        
        return {
            'source_sample': source_sample,
            'target_sample': target_sample
        }
    except Exception as e:
        return {'error': str(e)}
            """)
        
        try:
            # Import generated module
            spec = importlib.util.spec_from_file_location("sample_data_fetcher", f.name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Execute sample data fetching
            result = asyncio.run(module.fetch_sample_data())
            
            # Cleanup
            os.unlink(f.name)
            
            return result
            
        except Exception as e:
            return {'error': f"Sample data fetching failed: {str(e)}"}

    def _execute_generated_code(self, code: Dict) -> Dict:
        """Execute AI-generated integration code."""
        import tempfile
        import importlib.util
        import asyncio
        
        # Create temporary module
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
            # Write all code sections
            f.write(code['fetch_code'] + '\n')
            f.write(code['transform_code'] + '\n')
            f.write(code['upload_code'] + '\n')
            
            # Write main execution function
            f.write("""
async def execute_integration(source_data):
    try:
        # Fetch additional data if needed
        fetch_result = await fetch_data(source_data)
        
        # Transform the data
        transformed_data = transform_data(fetch_result)
        
        # Upload to target platform
        result = await upload_data(transformed_data)
        return result
    except Exception as e:
        return {'error': str(e)}
            """)
        
        try:
            # Import generated module
            spec = importlib.util.spec_from_file_location("generated_integration", f.name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Execute integration
            result = asyncio.run(module.execute_integration())
            
            # Cleanup
            os.unlink(f.name)
            
            return result
            
        except Exception as e:
            return {'error': f"Integration execution failed: {str(e)}"}

    def create_chain(self, retriever):
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
        )