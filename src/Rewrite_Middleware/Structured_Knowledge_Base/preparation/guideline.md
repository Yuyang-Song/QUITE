**Option 1: Use Our Pre-built Knowledge Base**
```bash
# The knowledge base is ready to use at:
src/Rewrite_Middleware/Structured_Knowledge_Base/storage/knowledge_base.json
```

**Option 2: Build Your Own Knowledge Base**

1. **Prepare your data sources:**
```bash
# Navigate to preparation directory
cd src/Rewrite_Middleware/Structured_Knowledge_Base/preparation/
```

2. **Organize your data files:**
   - Place your markdown files in `data/your_folder/` (replace `your_folder` with your actual folder name)
   - Place your JSON files in `data/` (e.g., `calcite.json`, `oracle.json`, `sql_server.json`)

3. **Configure and run the data processing pipeline:**
```bash
# Edit the configuration paths in data_clean.py:
# - input_file_dir: Path to your markdown data folder
# - save_file_dir: Output path for knowledge base JSON
# - save_document_file_dir: Output path for document store

# Run the data cleaning pipeline
python data_clean.py
```

4. **Update system configuration files:**
**Files to modify:**
- [`knowledge_base.py`](src/Rewrite_Middleware/Structured_Knowledge_Base/knowledge_base.py)
- [`middleware.py`](src/Rewrite_Middleware/middleware.py)