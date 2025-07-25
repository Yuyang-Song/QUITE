
import os
import sys
import json
import asyncio
import time
import argparse
import glob
sys.path.append('../')
sys.path.append('./')

from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
from src.utils.data_distribution import get_statistics_list, get_available_databases
from src.utils.get_data_statistics import get_data_statistics
from src.Rewrite_Middleware.middleware import DBMS
from src.utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue
from src.Query_Rewriter.finite_state_machine import QueryRewriter
from src.Hint_Recommender.injection import Hint_Recommender

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)   

def parse_arguments():
    """Parse parameters from command line or use default values"""
    parser = argparse.ArgumentParser(description="QUITE: Query Rewrite and Hint Recommendation System")
    
    # basic configuration
    parser.add_argument("--input_path", type=str, 
                       default=None,
                       help="Input JSON file path containing queries")
    parser.add_argument("--output_dir", type=str, 
                       default="/root/syy/QUITE/output",
                       help="Output directory for results")
    parser.add_argument("--schema_file", type=str, 
                       default=None,
                       help="Path to the schema file for the database")
    parser.add_argument("--max_iterations", type=int, default=2,
                       help="Maximum iteration loops for query rewriting")

    
    # Query Rewriter configuration
    parser.add_argument("--enable_rewriter", action="store_true", default=False,
                       help="Enable query rewriter")
    parser.add_argument("--save_rewriter_logs", action="store_true", default=False,
                       help="Save rewriter terminal logs to txt files")
    parser.add_argument("--rewriter_batch_size", type=int, default=3,
                       help="Batch size for rewriter (default: 3, forced to 1 if saving logs)")
    
    # Hint Recommender configuration
    parser.add_argument("--enable_recommender", action="store_true", default=False,
                       help="Enable hint recommender")
    parser.add_argument("--recommender_batch_size", type=int, default=3,
                       help="Batch size for recommender")
    
    return parser.parse_args()



def setup_directories(output_dir: str, enable_rewriter: bool, enable_recommender: bool):
    """Set up output directories for rewriter and recommender"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    directories = {}
    
    if enable_rewriter:
        # QueryRewriter tmp 
        rewriter_temp_dir = output_path / "rewriter_temp"
        rewriter_temp_dir.mkdir(exist_ok=True)
        directories['rewriter_temp'] = rewriter_temp_dir
    
    if enable_recommender:
        # HintRecommender tmp
        recommender_temp_dir = output_path / "recommender_temp"
        recommender_temp_dir.mkdir(exist_ok=True)
        directories['recommender_temp'] = recommender_temp_dir
    
    directories['output'] = output_path
    return directories

def merge_batch_files(temp_dir: Path, output_dir: Path, final_filename: str):
    """merge all batch files into a single JSON file"""
    batch_files = sorted(glob.glob(str(temp_dir / "batch_*.json")))
    if not batch_files:
        print(f"No batch files found in {temp_dir}")
        return None
    
    merged_data = []
    for batch_file in batch_files:
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    merged_data.append(data)
        except Exception as e:
            print(f"Error reading {batch_file}: {e}")
    
    if merged_data:
        final_file_path = output_dir / final_filename
        with open(final_file_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Merged {len(batch_files)} batch files into {final_file_path}")
        print(f"📊 Total queries processed: {len(merged_data)}")
        return final_file_path
    return None

async def run_query_rewriter(args, directories, dbms, data_statistics, schema_file):
    """LLM-based Query Rewriter"""
    print("\n" + "="*60)
    print("🔄 Starting Query Rewriter")
    print("="*60)
    
    mq = MessageQueue(window_size=8)
    rewriter = QueryRewriter(mq, dbms, data_statistics, schema_file, args.max_iterations)
    
    # laod input data
    with open(args.input_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    
    # make sure the input data is a list
    actual_batch_size = 1 if args.save_rewriter_logs else args.rewriter_batch_size
    if args.save_rewriter_logs and args.rewriter_batch_size != 1:
        print(f"⚠️  Forcing batch size to 1 due to log saving requirement (was {args.rewriter_batch_size})")
    
    count = 0
    batch = 0
    result = []
    temp_dir = directories['rewriter_temp']
    
    print(f"📊 Processing {len(data)} queries with batch size {actual_batch_size}")
    print(f"📁 Temp directory: {temp_dir}")
    print(f"📝 Save logs: {'Yes' if args.save_rewriter_logs else 'No'}")
    print()  

    with tqdm(total=len(data), 
              desc="🔄 Query Rewriter Progress", 
              position=0, 
              leave=True,
              dynamic_ncols=True,
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
        
        for item in data:
            # update progress bar description
            pbar.set_description(f"🔄 Processing Query {count + 1}/{len(data)} (ID: {item.get('id', 'N/A')})")
            
            initial_sql = item["query"]
            
            rewriter.initial_sql = initial_sql
            start_time = time.time()

            rewritten_sql = await rewriter.run()
            
            end_time = time.time()
            rewrite_time = end_time - start_time
            
            tmp = {
                "id": item["id"],
                "original_query": item["query"],
                "rewritten_query": rewritten_sql,
                "time_cost": rewrite_time,
                "rewrite_suggestion": rewriter.optimization_advice
            }
            result.append(tmp)
            count += 1
            
            pbar.update(1)
            pbar.set_postfix({
                'Time': f'{rewrite_time:.2f}s',
                'Batch': batch + 1 if count % actual_batch_size == 0 else batch
            })
            
            await rewriter.clear()
            
            # save results in batches
            if count % actual_batch_size == 0 or count == len(data):
                batch += 1
                
                # save batch results to temporary directory
                json_file_path = temp_dir / f"batch_{batch}.json"
                with open(json_file_path, "w", encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                
                # if saving logs, write to txt file
                if args.save_rewriter_logs:
                    txt_file_path = temp_dir / f"batch_{batch}.txt"
                    with open(txt_file_path, "w", encoding='utf-8') as f:
                        f.write(f"Batch {batch} - Query Rewriter Logs\n")
                        f.write("="*50 + "\n\n")
                        for r in result:
                            f.write(f"Query ID: {r['id']}\n")
                            f.write(f"Original: {r['original_query']}\n")
                            f.write(f"Rewritten: {r['rewritten_query']}\n")
                            f.write(f"Time Cost: {r['time_cost']:.2f}s\n")
                            f.write(f"Suggestion: {r['rewrite_suggestion']}\n")
                            f.write(rewriter.terminal_output)
                            f.write("\n" + "-"*40 + "\n\n")
                
                await rewriter.clear_log()
                result = []  # clear result for next batch
        
        # update progress bar when done
        pbar.set_description("🔄 Query Rewriter Completed")
        pbar.set_postfix({'Status': 'Merging files...'})
    
    print(f"\n✅ Query Rewriter completed! Processed {count} queries in {batch} batches")
    
    # merge all batch files into output directory
    final_file = merge_batch_files(temp_dir, directories['output'], "rewritten_queries.json")
    return final_file

async def run_hint_recommender(args, directories, dbms, rewriter_output_file):
    """run query hint recommender"""
    print("\n" + "="*60)
    print("💡 Starting Hint Recommender")
    print("="*60)
    
    if not rewriter_output_file or not rewriter_output_file.exists():
        print("❌ No rewriter output file found. Skipping hint recommender.")
        return None
    
    recommender = Hint_Recommender(dbms, dbms.db_name)
    temp_dir = directories['recommender_temp']
    
    # load rewriter output data
    print(f"📖 Loading data from {rewriter_output_file}")
    ori_data = recommender.load_data_from_file(str(rewriter_output_file))
    if not ori_data:
        print("❌ No data loaded from rewriter output. Skipping hint recommender.")
        return None
    
    print(f"📊 Processing {len(ori_data)} queries with batch size {args.recommender_batch_size}")
    print(f"📁 Temp directory: {temp_dir}")
    print()  
    
    batch_count = 0
    result = []
    
    with tqdm(total=len(ori_data), 
              desc="💡 Hint Recommender Progress", 
              position=1, 
              leave=True,
              dynamic_ncols=True,
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
        
        for i, item in enumerate(ori_data):
            # update progress bar description
            pbar.set_description(f"💡 Processing Hint {i + 1}/{len(ori_data)} (ID: {item.get('id', 'N/A')})")
            
            start_time = time.time()
            
            hint_result = recommender.process_single_query(item["original_query"],item["rewritten_query"],item["id"])
            
            end_time = time.time()
            process_time = end_time - start_time
            
            result.append(hint_result)
            
            # update progress bar
            pbar.update(1)
            pbar.set_postfix({
                'Time': f'{process_time:.2f}s',
                'Batch': batch_count + 1 if (i + 1) % args.recommender_batch_size == 0 else batch_count
            })
            
            # save results in batches
            if (i + 1) % args.recommender_batch_size == 0 or i == len(ori_data) - 1:
                batch_count += 1
                batch_file = temp_dir / f"batch_{batch_count}.json"
                
                with open(batch_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                
                result = []
        
        # update progress bar when done
        pbar.set_description("💡 Hint Recommender Completed")
        pbar.set_postfix({'Status': 'Merging files...'})
    
    print(f"\n✅ Hint Recommender completed! Processed {len(ori_data)} queries in {batch_count} batches")
    
    # merge all batch files into output directory
    final_file = merge_batch_files(temp_dir, directories['output'], "recommended_hints.json")
    return final_file

async def main():
    print("🚀 QUITE System Starting...")
    
    try:
        args = parse_arguments()
    except SystemExit:
        # if no arguments are provided, use default values
        print("No command line arguments provided. Using default configuration. Process ends!")
        return
    
    print(f"📂 Input: {args.input_path}")
    print(f"📁 Output: {args.output_dir}")
    print(f"🔄 Rewriter: {'Enabled' if args.enable_rewriter else 'Disabled'}")
    print(f"💡 Recommender: {'Enabled' if args.enable_recommender else 'Disabled'}")
    
    if args.save_rewriter_logs:
        print(f"📝 Rewriter logs: Enabled (batch size forced to 1)")
    else:
        print(f"📝 Rewriter logs: Disabled (batch size: {args.rewriter_batch_size})")
    
    # set up output directories
    directories = setup_directories(args.output_dir, args.enable_rewriter, args.enable_recommender)
    print(f"\n📁 Directory structure created:")
    for key, path in directories.items():
        print(f"   {key}: {path}")

    ###########################################################
    # database and schema setup
    ###########################################################
    
    # obtain database name and statistics
    dbms = DBMS()
    DB_NAME = dbms.db_name
    data_statistics = None
    if DB_NAME in get_available_databases():
        data_statistics = get_statistics_list(DB_NAME)
    else:
        data_statistics = get_data_statistics()
    
    print(f"\n📊 Database {DB_NAME} statistics loaded")
    
    schema_file = args.schema_file
    with open(schema_file, 'r') as f:
        schema_content = f.read()
        if not schema_content.strip():
            raise ValueError(f"Schema file {schema_file} is empty or not found.")
        print(f"📋 Schema content loaded from {schema_file}")

    ###########################################################
    # QUITE System Execution
    ###########################################################
    # print(args.enable_rewriter, args.enable_recommender)
    rewriter_output_file = None
    recommender_output_file = None
    
    # run Query Rewriter
    if args.enable_rewriter:
        rewriter_output_file = await run_query_rewriter(args, directories, dbms, data_statistics, schema_file)
    
    # run Hint Recommender
    if not args.enable_rewriter:
        # if rewriter is not enabled, check if rewriter output file exists
        existing_file = directories['output'] / "rewritten_queries.json"
        if existing_file.exists():
            rewriter_output_file = existing_file
            print(f"📖 Using existing rewriter output: {existing_file}")
        else:
            print("❌ No existing rewriter output found. Cannot run recommender without rewriter data.")
            return
    
    if not rewriter_output_file:
        print("❌ No rewriter output available for recommender.")
        return
        
    recommender_output_file = await run_hint_recommender(args, directories, dbms, rewriter_output_file)

    ###########################################################
    # summary and output
    ###########################################################
    
    print("\n" + "="*60)
    print("🎉 QUITE System Completed!")
    print("="*60)
    
    if rewriter_output_file:
        print(f"📝 Query Rewriter Output: {rewriter_output_file}")
    
    if recommender_output_file:
        print(f"💡 Hint Recommender Output: {recommender_output_file}")
    
    print(f"📁 Output Directory: {directories['output']}")
    
    # list all output files
    output_files = list(directories['output'].glob("*.json"))
    if output_files:
        print(f"\n📊 Final output files:")
        for file in output_files:
            size = file.stat().st_size
            print(f"   {file.name}: {size:,} bytes")
    print("\n✨ Processing completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())