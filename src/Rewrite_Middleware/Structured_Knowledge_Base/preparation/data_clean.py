"""
Author: Yuyang Song
Created: 2024-10-19
Last Modified: 2025-07-24

Module: data_clean.py

This module provides data cleaning and processing capabilities for StackOverflow markdown files
related to SQL query rewriting. It leverages GPT models to analyze documents, categorize them
into different query optimization groups, and extract relevant information for knowledge base
construction.

The module processes markdown files containing StackOverflow questions and answers, determines
their usefulness for query rewriting, categorizes them into optimization groups, and extracts
structured information including question descriptions, query examples, and answer summaries.

Usage:
    # Initialize the cleaner with input and output directories
    input_dir = '/path/to/input/markdown/files'
    output_file = '/path/to/output/knowledge_base.json'
    
    # Create cleaner instance and run processing pipeline
    cleaner_instance = cleaner(input_dir, output_file)
    cleaner_instance.pipline()
    
    # The result will be saved as a JSON file containing:
    # - Categorized documents with group labels
    # - Question descriptions and examples
    # - Answer summaries and examples
"""

from openai import OpenAI
# from dotenv import load_dotenv
import json
import os
import json
from tqdm import tqdm
import textwrap
from datetime import datetime
import hashlib
import time


from pathlib import Path
import os
from dotenv import load_dotenv
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
from utils.llm_client import GPT

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[4]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path=LOAD_PATH)      
llm = GPT(
    api_key=os.getenv("ASSISTANT_MODEL_API_KEY"),
    model=os.getenv("ASSISTANT_MODEL"),
    base_url=os.getenv("ASSISTANT_MODEL_URL")
)




class cleaner():
    """
    Main data cleaning and processing class for StackOverflow markdown files.
    
    This class orchestrates the entire data cleaning pipeline, from reading markdown
    files to categorizing content and extracting structured information for SQL
    query rewriting knowledge base construction.
    
    The cleaner processes StackOverflow questions and answers related to SQL
    optimization, categorizes them into different optimization groups, and extracts
    relevant information including question descriptions, query examples, and
    answer summaries.
    
    Attributes:
        input_file_dir (str): Directory path containing input markdown files
        save_file_dir (str): File path for saving processed results
        llm (GPT): GPT client instance for document analysis
        money (float): Total cost accumulator for processing
    """
    def __init__(self, input_file_dir, save_file_dir):
        """
        Initialize the cleaner with input and output paths.
        
        Args:
            input_file_dir (str): Directory containing markdown files to process
            save_file_dir (str): File path where results will be saved as JSON
        """
        self.input_file_dir = input_file_dir
        self.save_file_dir = save_file_dir
        self.llm = llm  # Use the global LLM instance for document analysis
    
    def read_json_files(self, json_file_path):
        """
        Read and parse JSON files containing official database documentation.
        
        This method reads JSON files from official database documentation
        (Calcite, Oracle, SQL Server) and prepares them for processing.
        
        Args:
            json_file_path (str): Path to the JSON file to read
            
        Returns:
            list: List containing the parsed JSON data
            
        Note:
            Returns empty list if file doesn't exist or can't be parsed
        """
        documents = []
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    documents.append(content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file {json_file_path}: {e}")
            except Exception as e:
                print(f"Error reading JSON file {json_file_path}: {e}")
        return documents
    
    def read_md_files(self, md_file_path):
        """
        Read and parse markdown files from the specified path.
        
        This method reads markdown files containing StackOverflow questions
        and answers, preparing them for GPT analysis.
        
        Args:
            md_file_path (str): Path to the markdown file to read
            
        Returns:
            list: List containing the file content as strings
            
        Note:
            Returns empty list if file doesn't exist or can't be read
        """
        documents = []
        if os.path.exists(md_file_path):
            with open(md_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
        return documents

    def con_prompt1_official(self, data):
        """
        Construct the first-stage prompt for official documentation classification.
        
        This prompt instructs GPT to analyze official database documentation
        and extract relevant rewrite rules and strategies.
        
        Args:
            data (dict/list): The official documentation content to analyze
            doc_type (str): Type of documentation (calcite, oracle, sql_server)
            
        Returns:
            str: Formatted prompt for GPT analysis
        """
        prompt = textwrap.dedent(f"""
        <mission>
        you are an experienced DBA, you are skilled in SQL analyisis and optimization. 
        Your missison is to help the user to judge whether this doc is useful for the query rewrite. And give a divided doc group based on the content.
        You are given a query rewrite related document, please fellow the steps below.
        Let's think step by step:
        
        <steps>
        1. determine whether this document is useful for query rewrite accrording to the <doc>.
        2. if useful, divide the document into different groups based on the content.The groups are as follows:
            - [Predicate_Pushdown_and_Sinmplification]: The document contains the information about Predicate Pushdown and Sinmplification.
            - [Constant_Folding]: The document contains the information about Constant Folding.
            - [Query_Merging_and_Flattening]: The document contains the information about Query merging and Flattening.
            - [Join_Optimization]: The document contains the information about Join optimization.
            - [Subquery_Optimization]: The document contains the information about Subquery optimization.
            if not useful, fill null instead.
        3. return the answer strickly according to the <json format>.
        
        <doc>
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        <json format>
        {{
            {{useful}} :  {{flag}} // True or False
            {{group}} : {{name}}  //Fill the group name of the document, if not useful, fill null.
        }}
        """)
        return prompt
    
    def con_prompt1(self, data):
        """
        Construct the first-stage prompt for document usefulness classification.
        
        This prompt instructs GPT to determine whether a StackOverflow document
        is useful for query rewriting and categorize it into specific optimization
        groups if useful.
        
        Args:
            data (str): The document content to analyze
            
        Returns:
            str: Formatted prompt for GPT analysis
            
        Note:
            The prompt defines 5 main categories for SQL optimization:
            - Predicate_Pushdown_and_Simplification
            - Constant_Folding  
            - Query_Merging_and_Flattening
            - Join_Optimization
            - Subquery_Optimization
        """
        prompt = textwrap.dedent(f"""
        <mission>
        you are an experienced DBA, you are skilled in SQL analyisis and optimization. 
        Your missison is to help the user to judge whether this doc is useful for the query rewrite. And give a divided doc group based on the content.
        You are given a query rewrite related document, please fellow the steps below.
        Let's think step by step:
        
        <steps>
        1. determine whether this document is useful for query rewrite accrording to the <doc>.
        2. if useful, divide the document into different groups based on the content.The groups are as follows:
            - [Predicate_Pushdown_and_Sinmplification]: The document contains the information about Predicate Pushdown and Sinmplification.
            - [Constant_Folding]: The document contains the information about Constant Folding.
            - [Query_Merging_and_Flattening]: The document contains the information about Query merging and Flattening.
            - [Join_Optimization]: The document contains the information about Join optimization.
            - [Subquery_Optimization]: The document contains the information about Subquery optimization.
            if not useful, fill null instead.
        3. return the answer strickly according to the <json format>.
        
        <doc>
        {data}
        
        <json format>
        {{
            {{useful}} :  {{flag}} // True or False
            {{group}} : {{name}}  //Fill the group name of the document, if not useful, fill null.
        }}
        """)
        return prompt
    
    def con_prompt2(self, data, tag):
        """
        Construct the second-stage prompt for detailed content extraction.
        
        This prompt instructs GPT to summarize and extract specific information
        from documents that were classified as useful in the first stage.
        It focuses on extracting question descriptions, query examples, and
        answer summaries relevant to the identified optimization category.
        
        Args:
            data (str): The document content to analyze
            tag (str): The optimization category tag assigned in stage 1
            
        Returns:
            str: Formatted prompt for detailed content extraction
            
        Note:
            The prompt extracts four key components:
            - Question description related to the optimization category
            - SQL query examples from questions (if any)
            - Summary of answers related to the category
            - SQL query examples from answers (if any)
        """
        prompt = textwrap.dedent(f"""
        <mission>
        you are an experienced DBA, you are skilled in SQL analyisis and optimization. 
        Your mission is to sunmmarize the content of the document and give a brief description of the document. This document comes from stackoveflow and contains the question desctiption and the answer user given.
        You are given a query rewrite related document, please fellow the steps below.
        Let's think step by step:
        
        <steps>
        1. Read this document for query rewrite accrording to the <doc> and the doc's type in <tag>.
        2. Summarize the Question desciption based related to the tag. If the question desciption contains the query example, pick it.
        3. Summarize the Answer based related to the tag. If the answer contains the query example, pick it. If there are multiple answers, please summarize all of them.
        4. return the answer strickly according to the <json format>.
        
        <doc>
        {data}
        
        <tag>
        {tag}
        
        <json format>
        {{
            {{Question_description}} :  {{description}} // The question description related to the tag.
            {{Question_query_example}} : {{example}}  // The question query example,if not exists, fill None.
            {{Answer_summary}} : {{summary}}  // The answer summary related to the tag.
            {{Answer_query_example}} : {{example}}  // The answer query example, if not exists, fill None.
        }}
        """)
        return prompt
        
    
    def process_official_docs(self):
        """
        Process official database documentation files.
        
        This method processes JSON files containing official documentation
        from various database systems (Calcite, Oracle, SQL Server) and
        extracts rewrite rules and strategies.
        
        Returns:
            list: List of processed official documentation entries
        """
        official_results = []
        
        # Official documentation files to process
        official_docs = {
            'calcite': './data/calcite.json',
            'oracle': './data/oracle.json', 
            'sql_server': './data/sql_server.json',
            'sql_query': './data/sql_query.json'
        }
        
        # Use tqdm for progress tracking
        for doc_type, file_path in tqdm(official_docs.items(), desc="Processing official docs", unit="doc"):
            if os.path.exists(file_path):
                print(f"📚 Processing official documentation: {doc_type}")
                
                # Read the official documentation
                doc_data = self.read_json_files(file_path)
                if not doc_data:
                    print(f"❌ No data found in {doc_type}")
                    continue
                    
                # Process with GPT
                for item in doc_data[0]:  # Iterate through each item in the array
                    prompt = self.con_prompt1_official(item)
                    try:
                        print(f"🤖 Analyzing {doc_type} item: {item.get('method', 'Unknown')}...")
                        res = self.llm.get_LLM_response(prompt, json_format=True)
                        
                        # Handle string response that may contain JSON
                        if isinstance(res, str):
                            # Extract JSON from the response if needed
                            try:
                                import re
                                json_match = re.search(r'```json\s*(\{.*?\})\s*```', res, re.DOTALL)
                                if json_match:
                                    json_str = json_match.group(1)
                                    res = json.loads(json_str)
                                else:
                                    # Try to find JSON without code blocks
                                    json_match = re.search(r'(\{[^}]*"useful"[^}]*\})', res, re.DOTALL)
                                    if json_match:
                                        json_str = json_match.group(1)
                                        res = json.loads(json_str)
                                    else:
                                        print(f"❌ No JSON found in response")
                                        continue
                            except json.JSONDecodeError as e:
                                print(f"❌ Failed to parse JSON: {e}")
                                continue
                        
                        # Process the single entry response
                        useflag = res.get('useful', False)
                        group = res.get('group', None)
                        
                        if useflag == True:
                            # Handle useful documents even if group is null
                            if group is None:
                                print(f"⚠️ {item.get('method', 'Unknown')}: Useful but no specific group assigned")
                                # Skip this entry as it doesn't fit our categorization
                                continue
                            else:
                                # Process documents with valid groups
                                official_entry = {
                                    "group": group,
                                    "question_description": item.get('method', 'N/A'),  # Use original method name
                                    "question_query_example": None,  # Official docs may not have specific examples
                                    "answer_summary": item.get('description', 'N/A'),  # Use original description
                                    "answer_query_example": None,
                                    "source": f"official_{doc_type}"
                                }
                                official_results.append(official_entry)
                                print(f"✅ {item.get('method', 'Unknown')}: Useful entry extracted (Group: {group})")
                        else:
                            print(f"⚠️ {item.get('method', 'Unknown')}: Not useful for query rewrite")
                            
                    except Exception as e:
                        print(f"❌ Error processing {item.get('method', 'Unknown')}: {e}")
                        continue
            else:
                print(f"❌ Official documentation file not found: {file_path}")
        
        return official_results
    
    def read_json_files_from_folder(self, folder_path):
        """
        Read all JSON files from a folder and generate IDs for each document.
        
        This method processes JSON files in the specified folder, ensures each
        document has a unique ID, and converts them to the standard document
        format for knowledge base storage.
        
        Args:
            folder_path (str): Path to the folder containing JSON files
            
        Returns:
            list: List of processed documents, each with an 'id' field
            
        Note:
            - Automatically generates SHA256 hash-based IDs for documents without IDs
            - Handles both single objects and arrays in JSON files
            - Updates original files to include generated IDs
            - Removes duplicate documents based on content hash
        """
        start_time = time.time()
        documents = []
        existing_ids = set()

        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return []

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
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

                            # Save this object as an independent document
                            doc_json_str = json.dumps(item, ensure_ascii=False)
                            doc_hash_id = hashlib.sha256(doc_json_str.encode('utf-8')).hexdigest()
                            if doc_hash_id not in existing_ids:
                                documents.append({
                                    "id": item_id,
                                    "content": doc_json_str
                                })
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
                            documents.append({
                                "id": item_id,
                                "content": doc_json_str
                            })
                            existing_ids.add(doc_hash_id)

                    # Write the processed file back to ensure all items have IDs
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        end_time = time.time()
        print(f"Read {len(documents)} documents in {(end_time - start_time):.2f} seconds.")
        return documents

    def process_documents_with_id_generation(self):
        """
        Process current result files and generate IDs for each document in standard format.
        
        This method reads existing result files, generates unique IDs for each document,
        and converts them to the standard format required by the knowledge base system.
        Each document is transformed into the format: {"id": "...", "content": "..."}
        
        Returns:
            bool: True if processing was successful, False otherwise
            
        Note:
            - Generates SHA256 hash-based unique IDs for each document
            - Converts documents to standard knowledge base format
            - Overwrites the original file with processed documents
        """
        try:
            # Read the current result file
            if not os.path.exists(self.save_file_dir):
                print(f"❌ Result file does not exist: {self.save_file_dir}")
                return False

            with open(self.save_file_dir, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Generate ID and standard format for each document
            documents_with_id = []
            for item in data:
                # Generate unique ID
                generated_id = hashlib.sha256(json.dumps(item, ensure_ascii=False).encode('utf-8')).hexdigest()
                
                # Create standard format document
                doc_with_id = {
                    "id": generated_id,
                    "content": json.dumps(item, ensure_ascii=False)
                }
                documents_with_id.append(doc_with_id)
            
            # Save processed documents
            output_path = save_document_file_dir
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(documents_with_id, file, ensure_ascii=False, indent=4)
            
            print(f"✅ Successfully processed {len(documents_with_id)} documents")
            print(f"📁 Output file: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error processing documents: {e}")
            return False
    
    def pipline(self):
        """
        Execute the complete data processing pipeline.
        
        This is the main processing method that orchestrates the entire workflow:
        1. Processes official database documentation (Calcite, Oracle, SQL Server)
        2. Reads all markdown files from the input directory (StackOverflow)
        3. For each file, determines usefulness for query rewriting
        4. If useful, categorizes into optimization groups
        5. Extracts detailed information including questions and answers
        6. Combines official docs and StackOverflow data
        7. Saves final results to JSON files
        8. Tracks processing costs throughout the pipeline
        
        The pipeline uses a two-stage GPT analysis for StackOverflow data:
        - Stage 1: Document classification and categorization
        - Stage 2: Detailed content extraction and summarization
        
        Official documentation is processed separately with specialized prompts.
        
        Results are saved incrementally to prevent data loss and include
        cost tracking information.
        
        Raises:
            Exception: If file I/O operations fail or GPT API calls fail
        """
        # Initialize results list
        result = []
        
        # Step 1: Process official documentation first
        print("📋 Step 1: Processing Official Documentation")
        official_results = self.process_official_docs()
        result.extend(official_results)
        
        # Step 2: Process StackOverflow markdown files
        print("📋 Step 2: Processing StackOverflow Files")
        stackoverflow_results = []
        iteration = 0
        successful_files = 0
        failed_files = 0
        useful_files = 0
        total_files = 0
        
        if os.path.exists(self.input_file_dir):
            files = [f for f in os.listdir(self.input_file_dir) if f.endswith(".md")]
            # Sort files to ensure consistent processing order (question_0, question_1, etc.)
            files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]) if x.startswith('question_') and '_' in x else float('inf'))
            total_files = len(files)
            
            # Main progress bar for all files
            with tqdm(total=total_files, desc="📄 Processing files", unit="file") as pbar:
                for filename in files:
                    pbar.set_description(f"📄 Processing: {filename[:30]}...")
                    iteration += 1
                    
                    # Read markdown file content
                    data = self.read_md_files(os.path.join(self.input_file_dir, filename))
                    
                    if not data:
                        failed_files += 1
                        pbar.set_postfix({
                            'Success': successful_files, 
                            'Useful': useful_files, 
                            'Failed': failed_files
                        })
                        pbar.update(1)
                        continue
                    
                    try:
                        # Stage 1: Determine usefulness and categorization
                        pbar.set_description(f"🤖 GPT Analysis: {filename[:25]}...")
                        prompt = self.con_prompt1(data)
                        res = self.llm.get_LLM_response(prompt, json_format=True)
                        
                        # Handle string response that may contain JSON
                        if isinstance(res, str):
                            # Extract JSON from the response if needed
                            try:
                                import re
                                json_match = re.search(r'```json\s*(\{.*?\})\s*```', res, re.DOTALL)
                                if json_match:
                                    json_str = json_match.group(1)
                                    res = json.loads(json_str)
                                else:
                                    # Try to find JSON without code blocks
                                    json_match = re.search(r'(\{[^}]*"useful"[^}]*\})', res, re.DOTALL)
                                    if json_match:
                                        json_str = json_match.group(1)
                                        res = json.loads(json_str)
                                    else:
                                        tqdm.write(f"❌ {filename}: No JSON found in response")
                                        successful_files += 1  # Count as processed even if failed
                                        continue
                            except json.JSONDecodeError as e:
                                tqdm.write(f"❌ {filename}: Failed to parse JSON: {e}")
                                successful_files += 1  # Count as processed even if failed
                                continue
                        
                        useflag = res.get('useful', False)
                        group = res.get('group', None)
                        
                        if useflag == True:
                            if group is None:
                                # Document is useful but doesn't fit our categorization
                                tqdm.write(f"⚠️ {filename}: Useful but no specific group assigned")
                                # Don't count as useful since we need categorized content
                            else:
                                useful_files += 1
                                pbar.set_description(f"📝 Extracting: {filename[:25]}...")
                                
                                # Stage 2: Extract detailed information
                                prompt = self.con_prompt2(data, group)
                                res = self.llm.get_LLM_response(prompt, json_format=True)
                                
                                # Handle string response that may contain JSON
                                if isinstance(res, str):
                                    # Extract JSON from the response if needed
                                    try:
                                        import re
                                        json_match = re.search(r'```json\s*(\{.*?\})\s*```', res, re.DOTALL)
                                        if json_match:
                                            json_str = json_match.group(1)
                                            res = json.loads(json_str)
                                        else:
                                            # Try to find JSON without code blocks
                                            json_match = re.search(r'(\{[^}]*"Question_description"[^}]*\})', res, re.DOTALL)
                                            if json_match:
                                                json_str = json_match.group(1)
                                                res = json.loads(json_str)
                                            else:
                                                tqdm.write(f"❌ {filename}: No JSON found in stage 2 response")
                                                continue
                                    except json.JSONDecodeError as e:
                                        tqdm.write(f"❌ {filename}: Failed to parse stage 2 JSON: {e}")
                                        continue
                                
                                # Extract structured information
                                question_description = res.get('Question_description', 'N/A')
                                question_query_example = res.get('Question_query_example', None)
                                answer_summary = res.get('Answer_summary', 'N/A')
                                answer_query_example = res.get('Answer_query_example', None)
                                
                                # Structure the extracted data
                                stackoverflow_entry = {
                                    "group": group,
                                    "question_description": question_description,
                                    "question_query_example": question_query_example,
                                    "answer_summary": answer_summary,
                                    "answer_query_example": answer_query_example,
                                    "source": "stackoverflow"
                                }
                                stackoverflow_results.append(stackoverflow_entry)
                            
                        successful_files += 1
                        
                    except Exception as e:
                        failed_files += 1
                        tqdm.write(f"❌ Error processing {filename}: {e}")

                    # Update progress bar with current stats
                    pbar.set_postfix({
                        'Success': successful_files, 
                        'Useful': useful_files, 
                        'Failed': failed_files
                    })
                    pbar.update(1)

                    # Save intermediate results periodically (every 10 files)
                    if iteration % 10 == 0:
                        pbar.set_description("💾 Saving intermediate results...")
                        current_results = result + stackoverflow_results
                        try:
                            with open(self.save_file_dir, 'w', encoding='utf-8') as file:
                                json.dump(current_results, file, indent=4, ensure_ascii=False)
                        except Exception as e:
                            tqdm.write(f"⚠️ Error saving intermediate results: {e}")
        else:
            print(f"❌ StackOverflow directory not found: {self.input_file_dir}")

        # Combine all results and provide final summary
        result.extend(stackoverflow_results)
        
        
        # Group distribution
        group_stats = {}
        for entry in result:
            group = entry.get('group', 'unknown')
            group_stats[group] = group_stats.get(group, 0) + 1
        
        print("\n📈 Group Distribution:")
        for group, count in sorted(group_stats.items()):
            print(f"  • {group}: {count} entries")
        
        # Save final results
        print(f"\n💾 Saving final results to: {self.save_file_dir}")
        try:
            with open(self.save_file_dir, 'w', encoding='utf-8') as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
            print("✅ Final save completed successfully!")
        except Exception as e:
            print(f"❌ Error saving final results: {e}")
            return
        
                
# Configuration and execution section
# Default paths for processing StackOverflow markdown files and official docs
input_file_dir = './data/ur_folder'  # Modify this to your own data directory
save_file_dir = '../storage/ur_knowledge_base.json'  # Output JSON file path, modify to your own knowledge base file
save_document_file_dir = '../storage/ur_document_store.json'  # Document store cache file path, modify to your own document store file

# Initialize the cleaner
clean = cleaner(input_file_dir, save_file_dir)

# Execution options:
# 1. Complete data cleaning pipeline
clean.pipline()

# 2. Process existing result files and generate IDs (for knowledge base)
print("📋 Processing existing result files, generating knowledge base format...")
clean.process_documents_with_id_generation()
                    
        
    
    