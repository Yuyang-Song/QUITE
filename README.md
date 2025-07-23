# QUITE: A Query Rewrite System Beyond Rules with LLM Agents

## Table of Contents
- [System Overview](#system-overview)
- [Quick Start](#quick-start)
- [Experimental Results](#experimental-results)
- [Rewrite Beyond Rules Discussion](#rewrite-beyond-rules-discussion)
- [Code Structure](#code-structure)

<!-- - [Citation](#citation) -->
## System Overview
<p align="center">
    <img src="figures/overview.png" width="1000px">
</p>

QUITE (<u>QU</u>ery rewr<u>ITE</u>) is a training-free and feedback-aware system based on LLM agents that rewrites SQL queries into semantically equivalent forms with significantly better performance, covering a broader range of query patterns and rewrite strategies.

The figure above presents the query rewrite workflow:

### 🚀 Key Features
- **Training-Free**: No machine learning model training required
- **Multi-Agent Architecture**: Specialized agents for reasoning, verification, and decision-making
- **Feedback-Aware**: Iterative refinement based on execution plan analysis
- **Broad Coverage**: Supports complex query patterns beyond traditional rule-based systems
- **Memory Management**: Efficient context management to prevent hallucinations
## Environment Setup
The following instructions have been tested on Ubuntu 22.04 and PostgreSQL v14.13, Python 3.12.



### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-repo/QUITE.git
cd QUITE
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

<!-- For the Rewrite Middleware dependencies installation, you can check the official document to find help. We use [SQLSolver SIGMOD'24](https://github.com/SJTU-IPADS/SQLSolver) as the start point of our hybrid SQL Corrector, [haystack](https://github.com/deepset-ai/haystack) to build our knowledge base. -->

<!-- 3. **Database Setup:**
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
\q
```

4. **Load Benchmark Data:**
```bash
# For TPC-H benchmark
cd dataset/schemas
psql -d your_database_name -f tpch.sql

# For DSB benchmark  
psql -d your_database_name -f dsb.sql

# For Calcite benchmark
psql -d your_database_name -f calcite.sql
``` -->

## Quick Start

### Step 1: Configuration Setup

#### 1.1 Set up your OpenAI API keys and URL for LLM Agents

Create a `.env` file in the `config_file/` directory. Our default base LLM selection is as follows:

```bash
# config_file/.env
# LLM Model API Configuration
REASONING_MODEL_API_KEY = [your_api_key_here]
REASONING_MODEL = deepseek-r1
REASONING_MODEL_URL = [your_model_url_here]

DECISION_MODEL_API_KEY = [your_api_key_here]
DECISION_MODEL = claude-3-7-sonnet-20250219
DECISION_MODEL_URL = [your_model_url_here]

ASSISTANT_MODEL_API_KEY = [your_api_key_here]
ASSISTANT_MODEL = claude-3-7-sonnet-20250219
ASSISTANT_MODEL_URL = [your_model_url_here]

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# Project Configuration
PROJECT_ROOT=/path/to/QUITE
```

#### 1.2 Test Each Module

Test DBMS connection, LLM platform connection and the Rewrite Middleware Components:

```bash
# Test database connection and middleware tools
python test_module.py

# Test specific components
python src/Rewrite_Middleware/Structured_Knowledge_Base/scripts/test.py
```

### Step 2: Prepare Input Queries

#### 2.1 Use Provided Query Sets

QUITE includes three benchmark query sets:

```bash
# TPC-H queries
dataset/queries/tpch.json      # Test queries

# DSB queries  
dataset/queries/dsb_test.json

# Calcite queries
dataset/queries/calcite_test.json
```

#### 2.2 Prepare Custom Queries

Create your own query file in JSON format:

```json
[
    {
        "id": 1,
        "query": "SELECT * FROM customer WHERE c_acctbal > 1000",
        "description": "Simple customer filter query"
    },
    {
        "id": 2, 
        "query": "SELECT c_name, SUM(o_totalprice) FROM customer JOIN orders ON c_custkey = o_custkey GROUP BY c_name",
        "description": "Customer order aggregation"
    }
]
```

### Step 3: Execute QUITE to Rewrite SQL Queries

#### 3.1 Run the Main System

```bash
# Run with default configuration
python run_QUITE.py

# Run with custom parameters
python run_QUITE.py --input dataset/queries/tpch_test.json --output output/my_results --max_iterations 3
```

#### 3.2 Monitor the Process

The system will display real-time progress:

```
====================================================================
🗄️  Starting Database Statistics Collection
====================================================================
🔗 Database: your_database_name
📊 Getting list of tables in public schema...
✅ Found 8 tables. Starting table scan...

######################################################################################

=== Start Parallel Reasoning (Number of Threads: 2) ===
## Worker 0: Start Reasoning Stage ===
## Worker 1: Start Reasoning Stage ===
...
```

### Step 4: View the Rewrite Results

#### 4.1 Output Structure

Results are saved in the `output/` directory:

```
output/
├── batch_1.json          # Rewritten queries batch 1
├── batch_1.txt           # Detailed logs batch 1  
├── batch_2.json          # Rewritten queries batch 2
├── batch_2.txt           # Detailed logs batch 2
└── ...
```

#### 4.2 Result Format

Each JSON file contains:

```json
[
    {
        "id": 1,
        "original_query": "SELECT * FROM customer WHERE c_acctbal > 1000",
        "rewritten_query": "SELECT * FROM customer WHERE c_acctbal > 1000.0",
        "time_cost": 2.34,
        "rewrite_suggestion": "Added explicit decimal notation for numeric comparison"
    }
]
```

#### 4.3 Performance Analysis

Use the provided analysis tools:

```bash
# Analyze rewrite effectiveness  
python scripts/analyze_results.py --input output/batch_1.json

# Compare performance improvements
python scripts/performance_comparison.py --original queries.json --rewritten output/batch_1.json
```


## Experimental Results
### Baselines:
We compare QUITE with state-of-the-art methods:
- **[LearnedRewrite SIGMOD'22](https://www.vldb.org/pvldb/vol15/p46-li.pdf)**: A machine learning-based query rewrite system leverages MCTS to search the optimized set of rewrite rules in [Apache Calcite](https://github.com/apache/calcite).
- **[LLM-R² VLDB'24](https://www.vldb.org/pvldb/vol18/p53-yuan.pdf)**: An LLM-based query rewrite system that prepares high-quality rewrite demonstrations for LLM to select the optimized set of rewrite rules in [Apache Calcite](https://github.com/apache/calcite).
- **[R-Bot ArXiv'25](https://arxiv.org/pdf/2412.01661)**: An LLM-based query rewrite system
- **LLM Agent (SOTA Models)**: Pure agent approach compared to our system's agent template in [`utils/agent_template.py`](src/utils/agent_template.py).


### Performance Results
We compare QUITE with state-of-the-art methods on different benchmarks (TPC-H, DSB and Calcite) and metrics (query execution latency, rewritten equivalence rate and rewritten improvement rate). We present the core results in this repository. For more details, please refer to our paper.
<p align="center">
    <img src="figures/query_latency.png" width="1000px">
</p>
<p align="center">
    <img src="figures/rewritten_rate.png" width="1000px">
</p>


## Rewrite Beyond Rules Discussion
We have collected and analyzed a set of high-impact rewrite examples and integrated them into our [TPC-H examples](./example/TPC-H), [DSB examples](./example/DSB) and [Calcite examples](./example/Calcite)

In the course of rewriting with QUITE, we discovered a range of strategies previously unmodeled by our rule set. These newly identified techniques can be found in our more detailed [Appendix](./documents/Detailed_Appendix.pdf).




## Code Structure
#### 🔧 Core Modules
- **`src/Query_Rewriter/`**: Main query rewriting engine
  - `finite_state_machine.py`: Finite state machine orchestrating the complete rewrite workflow
  - `agent_definition.py`: Definitions for Reasoning, Assistant, and Decision agents
  - `memory_buffer.py`: Memory management to prevent context overflow and hallucinations

#### 🛠️ Middleware Components  
- **`src/Rewrite_Middleware/`**: Database interaction and verification tools
  - `middleware.py`: Core tools including DBMS_EXPLAIN_Tool, DBMS_Syntax_Tool, Knowledge_Base_Tool
  - `Agent_Memory_Buffer/`: Advanced memory management for agent context
  - `Structured_Knowledge_Base/`: Knowledge retrieval and management system

#### 💡 Intelligent Recommendation
- **`src/Hint_Recommender/`**: Optimization hint generation system
  - `main.py`: Entry point for hint recommendation workflow
  - `gpt.py`: GPT-based hint generation engine
  - `tools.py`: Utility functions for hint processing and validation

#### 🔧 Utilities
- **`src/utils/`**: Shared utilities and base classes
  - `agent_template.py`: Base classes for LLM agents (MessageQueue, MemoryWindow, etc.)
  - `llm_client.py`: Unified LLM client interface supporting multiple models
  - `data_distribution.py`: Database statistics storage and management
  - `get_data_statistics.py`: Automated database profiling and statistics collection

#### 📊 Data & Configuration
- **`dataset/`**: Benchmark datasets and schemas for evaluation
- **`config_file/`**: Environment configuration and API keys
- **`example/`**: Sample queries and usage examples
- **`experiments_results/`**: Experimental results and performance analysis

#### 🚀 Entry Points
- **`run_QUITE.py`**: Main script to execute the complete rewrite pipeline
- **`test_module.py`**: Comprehensive testing suite for all components

```
QUITE/
├── config_file/
│   └── .env                           # Environment configuration file
├── dataset/
│   ├── queries/
│   │   ├── tpch_test.json            # TPC-H test queries
│   │   ├── tpch_hard.json            # TPC-H complex queries
│   │   ├── dsb_test.json             # DSB benchmark queries
│   │   └── calcite_test.json         # Calcite benchmark queries
│   └── schemas/
│       ├── tpch.sql                  # TPC-H database schema
│       ├── dsb.sql                   # DSB database schema
│       └── calcite.sql               # Calcite database schema
├── src/
│   ├── Query_Rewriter/
│   │   ├── finite_state_machine.py  # Main FSM orchestrating rewrite process
│   │   ├── agent_definition.py      # LLM agent role definitions
│   │   └── memory_buffer.py         # Agent memory management system
│   ├── Rewrite_Middleware/
│   │   ├── middleware.py            # Core database interaction tools
│   │   ├── Agent_Memory_Buffer/
│   │   │   └── memory_buffer.py     # Enhanced memory management
│   │   └── Structured_Knowledge_Base/
│   │       └── scripts/
│   │           └── test.py          # Knowledge base testing utilities
│   ├── Hint_Recommender/
│   │   ├── main.py                  # Hint recommendation entry point
│   │   ├── gpt.py                   # GPT client for hint generation
│   │   ├── GPT_request.py          # GPT API request handler
│   │   └── tools.py                 # Utility tools for hint processing
│   └── utils/
│       ├── agent_template.py        # Base agent template classes
│       ├── llm_client.py           # LLM client interface
│       ├── data_distribution.py     # Database statistics management
│       └── get_data_statistics.py   # Database statistics collection
├── example/
│   ├── TPC-H/                       # TPC-H query examples
│   ├── DSB/                         # DSB query examples
│   └── Calcite/                     # Calcite query examples
├── experiments_results/
│   ├── tpch/                        # TPC-H experimental results
│   ├── dsb/                         # DSB experimental results
│   └── calcite/                     # Calcite experimental results
├── output/                          # Generated rewrite results
├── figures/
│   └── overview.png                 # System architecture diagram
├── run_QUITE.py                     # Main execution script
├── test_module.py                   # Comprehensive testing suite
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```
<!-- ## Citation
If you use this codebase, or otherwise found our work valuable, please cite:
```
@article{song2025quite,
  title={QUITE: A Query Rewrite System Beyond Rules with LLM Agents},
  author={Song, Yuyang and Yan, Hanxu and Lao, Jiale and Wang, Yibo and Li, Yufei and Zhou, Yuanchun and Wang, Jianguo and Tang, Mingjie},
  journal={arXiv preprint arXiv:2506.07675},
  year={2025}
}
``` -->

