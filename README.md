# QUITE: A Query Rewrite System Beyond Rules with LLM Agents

## Table of Contents
- [System Overview](#system-overview)
- [Quick Start](#quick-start)
- [Experimental Results](#experimental-results)
- [Code Structure](#code-structure)
<!-- - [Citation](#citation) -->
## System Overview
<p align="center">
    <img src="figures/overview.png" width="1000px">
</p>

QUITE (<u>QU</u>ery rewr<u>ITE</u>) is a training-free and feedback-aware system based on LLM agents that rewrites SQL queries into semantically equivalent forms with significantly better performance, covering a broader range of query patterns and rewrite strategies.

The figure above presents the query rewrite workflow:

## Environment Setup
The following instructions have been tested on Ubuntu 22.04 and PostgreSQL v14.13, Python 3.12.

Install the QUITE dependencies:
```
pip install -r requirements.txt
```

For LLM agent tool dependencies installation, you can check the official document to find help. We use [SQLSolver SIGMOD'24](https://github.com/SJTU-IPADS/SQLSolver) as the start point of our SQL Corrector, [haystack](https://github.com/deepset-ai/haystack) to build our knowledge base.

Benchmark Preparation:
```

```


## Quick Start
### Step 1: Preparation for QUITE
#### 1.1 Set up your OpenAI API keys and URL for LLM Agents


#### 1.x Test Each Module
Test each rewrite middleware by using the following scripts:
```
python src/module_test.py
```

### Step 2: Prepare for Input Quries





### Step 3: Execute the QUITE to rewrite SQL queries



### Step 4: View the rewrite results:



## Experimental Results
### Baselines:
We compare QUITE with state-of-the-art methods:
- [LearnedRewrite SIGMOD'22](https://www.vldb.org/pvldb/vol15/p46-li.pdf): A machine learning-based query rewrite system leverages MCTS to search the optimized set of rewrite rules in [Apache Calcite](https://github.com/apache/calcite).
- [LLM-R² VLDB'24](https://www.vldb.org/pvldb/vol18/p53-yuan.pdf): An LLM-based query rewrite system that prepares high-quality rewrite demonstrations for LLM to select the optimized set of rewrite rules in [Apache Calcite](https://github.com/apache/calcite).
- [R-Bot ArXiv'25](https://arxiv.org/pdf/2412.01661): An LLM-based query rewrite system 
- LLM Agent (SOTA Models): We achieve the pure agent to rewrite quries in [code](), compared to our system's agent template in [utils/agent_template.py]().


### Results

## Code Structure

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

