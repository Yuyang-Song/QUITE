from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from datetime import datetime
import os
import json
import hashlib
from pathlib import Path
import pickle
import time
import textwrap
import logging
from typing import List, Dict

# Setup project paths
from src.utils.path_config import PROJECT_ROOT, setup_python_path, load_project_env
setup_python_path()
load_project_env()

class Structured_Knowledge_Base:
    def __init__(self, folder_path, json_file_path, document_store_path=None):
        self.open_api_key = Secret.from_token(os.getenv("ASSISTANT_MODEL_API_KEY"))  # Get the API key from the environment variable
        self.model = os.getenv("ASSISTANT_MODEL")
        self.api_base_url = os.getenv("ASSISTANT_MODEL_URL")
        self.folder_path = folder_path
        self.json_file_path = json_file_path

        # Set document_store cache path
        if document_store_path is None:
            base_dir = os.path.dirname(json_file_path)
            base_name = os.path.basename(json_file_path).split('.')[0]
            self.document_store_path = os.path.join(base_dir, f"{base_name}_document_store.pkl")
        else:
            self.document_store_path = document_store_path

        # Try to load document_store from cache
        if not self.load_document_store_from_cache():
            print("Building new document store...")
            # If cache loading fails, execute the original loading and indexing process
            self.document_store = InMemoryDocumentStore()
            documents = self.load_documents_from_file()
            self.document_store.write_documents(documents)
            # Save the constructed document_store to cache
            self.save_document_store_to_cache()

    def _compute_json_file_hash(self):
        """Compute the hash of the JSON file to detect if it has been modified."""
        if not os.path.exists(self.json_file_path):
            return None
            
        try:
            with open(self.json_file_path, 'rb') as f:
                file_content = f.read()
            return hashlib.md5(file_content).hexdigest()
        except Exception as e:
            print(f"Error computing JSON file hash: {e}")
            return None
    
    def save_document_store_to_cache(self):
        """Save document_store to cache file."""
        try:
            # Create metadata containing document content hash
            json_hash = self._compute_json_file_hash()
            
            # Optimize: Get documents once and use list comprehension
            documents = self.document_store.filter_documents()
            document_count = len(documents)
            
            # # For large document sets, consider using a more efficient approach
            # if document_count > 1000:
            #     print(f"Large document set detected ({document_count} docs), optimizing cache process...")
            
            # Use list comprehension for better performance
            documents_data = [
                {
                    "id": doc.id,
                    "content": doc.content,
                    "meta": getattr(doc, 'meta', {})
                }
                for doc in documents
            ]
            
            cache_data = {
                "documents_data": documents_data,
                "metadata": {
                    "json_hash": json_hash,
                    "created_at": datetime.now().isoformat(),
                    "document_count": document_count
                }
            }

            # Save to file with optimization for large files
            print(f"Saving {document_count} documents to cache...")
            with open(self.document_store_path, 'wb') as f:
                pickle.dump(cache_data, f, protocol=pickle.HIGHEST_PROTOCOL)
                
            print(f"Saved document store to {self.document_store_path}")
            print(f"Document count: {document_count}")
            return True
        except Exception as e:
            print(f"Error saving document store: {e}")
            return False

    def load_document_store_from_cache(self):
        """Load document_store from cache file."""
        if not os.path.exists(self.document_store_path):
            print(f"Document store cache file not found: {self.document_store_path}")
            return False
            
        try:
            # Load cache data 
            with open(self.document_store_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if it's the old format (with document_store) or new format (with documents_data)
            if "document_store" in cache_data:
                # Old format - try to use it but it might be empty
                document_store = cache_data["document_store"]
                metadata = cache_data["metadata"]
                
                # Check if the old document store actually has documents
                if len(document_store.filter_documents()) == 0:
                    print("Cached document store is empty, rebuilding...")
                    return False
                    
                self.document_store = document_store
            elif "documents_data" in cache_data:
                # New format - rebuild document store from documents data
                documents_data = cache_data["documents_data"]
                metadata = cache_data["metadata"]
                
                # Verify if JSON file hash matches
                current_json_hash = self._compute_json_file_hash()
                if current_json_hash != metadata["json_hash"]:
                    print("JSON file has changed since document store was cached. Rebuilding store.")
                    return False

                # Rebuild document store from cached documents
                self.document_store = InMemoryDocumentStore()
                document_count = len(documents_data)
                
                # Optimize: Use list comprehension for better performance
                if document_count > 1000:
                    print(f"Loading large document set ({document_count} docs)...")
                
                documents = [
                    Document(
                        id=doc_data["id"], 
                        content=doc_data["content"],
                        meta=doc_data.get("meta", {})
                    )
                    for doc_data in documents_data
                ]
                
                # Write all documents at once
                self.document_store.write_documents(documents)
            else:
                print("Invalid cache format")
                return False
            
            print(f"Loaded document store from cache with {metadata['document_count']} documents.")
            print(f"Cache created at: {metadata['created_at']}")
            return True
            
        except Exception as e:
            print(f"Error loading document store from cache: {e}")
            return False
            
    def refresh_document_store(self):
        """Force rebuild document_store"""
        print("Refreshing document store...")
        self.document_store = InMemoryDocumentStore()
        documents = self.load_documents_from_file()
        self.document_store.write_documents(documents)
        self.save_document_store_to_cache()
        print("Document store refreshed")

    # Save documents to local JSON file
    def save_documents_to_file(self, documents):
        documents_data = [{"id": doc.id, "content": doc.content} for doc in documents]
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            json.dump(documents_data, file, ensure_ascii=False, indent=4)

    # Load documents from local JSON file
    def load_documents_from_file(self):
        print("Loading documents from file...")
        documents = []
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                documents_data = json.load(file)
                for doc_data in documents_data:
                    documents.append(Document(id=doc_data["id"], content=doc_data["content"]))

        return documents

    # Read all JSON files from the folder
    def read_json_files_from_folder(self):
        start_time = time.time()
        documents = []
        existing_ids = set()

        if not os.path.exists(self.folder_path):
            print(f"Error: The folder '{self.folder_path}' does not exist.")
            return []

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # If it's an array, process each item individually
                    if isinstance(data, list):
                        for item in data:
                            if 'id' not in item or not item['id']:
                                generated_id = hashlib.sha256(json.dumps(item, ensure_ascii=False).encode('utf-8')).hexdigest()
                                item['id'] = generated_id
                            item_id = item['id']

                            # Save this object as a separate Document
                            doc_json_str = json.dumps(item, ensure_ascii=False)
                            doc_hash_id = hashlib.sha256(doc_json_str.encode('utf-8')).hexdigest()
                            if doc_hash_id not in existing_ids:
                                documents.append(Document(content=doc_json_str, id=item_id))
                                existing_ids.add(doc_hash_id)
                    # If it's a single object
                    elif isinstance(data, dict):
                        if 'id' not in data or not data['id']:
                            generated_id = hashlib.sha256(json.dumps(data, ensure_ascii=False).encode('utf-8')).hexdigest()
                            data['id'] = generated_id
                        item_id = data['id']

                        doc_json_str = json.dumps(data, ensure_ascii=False)
                        doc_hash_id = hashlib.sha256(doc_json_str.encode('utf-8')).hexdigest()
                        if doc_hash_id not in existing_ids:
                            documents.append(Document(content=doc_json_str, id=item_id))
                            existing_ids.add(doc_hash_id)

                    # Write the processed file back, ensuring all have IDs
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        end_time = time.time()
        print(f"Read {len(documents)} documents in {(end_time - start_time):.2f} seconds.")
        return documents

    def format_suggestion(self, suggestion) -> List[Dict[str, str]]:
        """
        Format the suggestion field by parsing it into a structured JSON format and removing unnecessary symbols.
        :param suggestion: The original suggestion to be formatted (which may be a string, list, or other types)
        :return: The formatted suggestion field (as a list of JSON objects)
        """
        import re
        
        try:
            # Handle empty values
            if not suggestion:
                return [{"suggestion": "No suggestion available"}]

            # Normalize to string
            if isinstance(suggestion, list):
                text = ''.join(str(item) for item in suggestion)
            else:
                text = str(suggestion)
            
            if not text.strip():
                return [{"suggestion": "No suggestion content"}]

            # Extract JSON content - Simplified using regular expressions
            text = text.strip()

            # Try to extract content surrounded by ```json...``` or ```...```
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Try to extract JSON starting from the first { or [
                brace_match = re.search(r'[{\[].*[}\]]', text, re.DOTALL)
                if brace_match:
                    json_content = brace_match.group(0)
                else:
                    json_content = text

            # Try to parse JSON
            try:
                parsed = json.loads(json_content)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]
                else:
                    return [{"suggestion": str(parsed)}]
            except json.JSONDecodeError:
                # JSON parsing failed, try to extract suggestion field
                suggestions = re.findall(r'"suggestion"\s*:\s*"([^"]*)"', json_content)
                if suggestions:
                    return [{"suggestion": s} for s in suggestions]

                # Last resort: return cleaned text
                return [{"suggestion": json_content}]
                
        except Exception as e:
            print(f"Error in format_suggestion: {e}")
            return [{"suggestion": str(suggestion)}]


    def retrieval(self,input_sql, suggestion_tuple):
        # Establish RAG pipeline
        # Handle both 'origin_suggestion' and 'produced_suggestion' keys for compatibility
        suggestion_text = suggestion_tuple.get("origin_suggestion") or suggestion_tuple.get("produced_suggestion", "")
        
        question = textwrap.dedent(f"""
        find the potential rewrite strageties for the sql query: {input_sql} and its suggestions are: {suggestion_text}.
        Please notice that the suggestion group reffered to the rewritten strataegie classification: {suggestion_tuple["group"]}.
        """)

        prompt_template = textwrap.dedent("""
        You are an experienced DBA and specialized in Query rewrite process of query optimization. 
        You have been given a SQL query to optimize from Question part.
        Note that you shouldn't have to directly rewrite the original sql, but to find and summarize the potential rewrite strageties for the sql query and its suggestion, make the strageties clear and simple.
                        
        Your work is to retrieval and summarize the documents related to its suggestion to find the rewrite optimization stratages.
        Note that you should summarize and return the most relevant and efficient stratages no more than two in the answer. Make your explain clear and simple.

                   
        Documents:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        Question: {{question}}

        Answer:
        You must return the answer in the following json format:
        {
                "suggestion": //   
        },
            ... //If more suggestions are needed, add more objects in the json array.          
        """)

        retriever = InMemoryBM25Retriever(document_store=self.document_store)
        # retriever = InMemoryEmbeddingRetriever(document_store=self.document_store)
        prompt_builder = PromptBuilder(template=prompt_template)
        llm = OpenAIGenerator(api_key = self.open_api_key, model = self.model, api_base_url = self.api_base_url)

        rag_pipeline = Pipeline()
        rag_pipeline.add_component("retriever", retriever)
        rag_pipeline.add_component("prompt_builder", prompt_builder)
        rag_pipeline.add_component("llm", llm)
        rag_pipeline.connect("retriever", "prompt_builder.documents")
        rag_pipeline.connect("prompt_builder", "llm")

        # First get retriever results separately for logging
        retriever_results = retriever.run(query=question)
        retrieved_docs = retriever_results.get("documents", [])
        
        # Write retrieved document IDs to log file
        try:
            log_file = PROJECT_ROOT / "output" / "knowledge_retrieval.log"
            log_file.parent.mkdir(exist_ok=True)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - Knowledge retrieval executed\n")
                f.write(f"{timestamp} - Query: {question}\n")
                
                doc_ids = [doc.id for doc in retrieved_docs if hasattr(doc, 'id') and doc.id]
                if doc_ids:
                    f.write(f"{timestamp} - Retrieved document IDs: {doc_ids}\n")
                else:
                    f.write(f"{timestamp} - No document IDs found, doc count: {len(retrieved_docs)}\n")
                    f.write(f"{timestamp} - Retriever results keys: {list(retriever_results.keys())}\n")
                    if retrieved_docs:
                        f.write(f"{timestamp} - First doc sample: {str(retrieved_docs[0])[:100]}...\n")
                    
        except Exception as e:
            print(f"Logging error: {e}")
            log_file = PROJECT_ROOT / "output" / "knowledge_retrieval.log"
            log_file.parent.mkdir(exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - Logging error: {str(e)}\n")

        # Run the full pipeline
        results = rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
            }
        )
        
        return results["llm"]["replies"]
