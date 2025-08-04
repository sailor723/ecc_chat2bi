"""
Day 1: PandasAI Prompt Inspector
================================

English Description:
This is an advanced tool for inspecting and understanding how PandasAI generates
prompts for the LLM. It provides detailed logging setup, prompt template analysis,
custom prompt examples, and educational insights into PandasAI's internal workings.

Key Features:
- Comprehensive logging configuration to capture all prompts
- Analysis of the prompt template structure
- Examples of custom prompt creation
- Step-by-step prompt generation process
- Educational content about prompt engineering
- Debugging capabilities for prompt optimization

中文描述：
这是一个用于检查和理解PandasAI如何为LLM生成提示的高级工具。
它提供详细的日志设置、提示模板分析、自定义提示示例，
以及关于PandasAI内部工作原理的教育见解。

主要功能：
- 全面的日志配置以捕获所有提示
- 提示模板结构分析
- 自定义提示创建示例
- 逐步提示生成过程
- 关于提示工程的教育内容
- 用于提示优化的调试功能

Usage: python prompt_inspector.py
"""

import pandasai as pai
from pandasai_openai import AzureOpenAI
import os
import pandas as pd
import logging

# Set up logging to see the prompts
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize LLM
llm = AzureOpenAI(
    azure_endpoint=api_endpoint,
    api_key=api_key,
    deployment_name=deployment_name,
    api_version=api_version,
)

# Sample data
data = {
    "OrderID": [1, 2, 3, 4, 5],
    "CustomerID": ["C001", "C002", "C003", "C004", "C005"],
    "ProductCategory": ["Electronics", "Clothing", "Electronics", "Books", "Clothing"],
    "SalesAmount": [1200.50, 75.20, 850.00, 45.99, 120.75],
    "OrderDate": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
    "Region": ["East", "West", "North", "South", "East"],
}

df = pd.DataFrame(data)

# Column descriptions
column_descriptions = {
    "OrderID": "A unique identifier for each sales order.",
    "CustomerID": "Identifier for the customer who placed the order.",
    "ProductCategory": "The category of the product sold.",
    "SalesAmount": "The monetary value of the sale in USD.",
    "OrderDate": "The date when the order was placed.",
    "Region": "The geographical region where the sale occurred.",
}

print("=== PANDASAI PROMPT INSPECTOR ===")
print("This script will show you the actual prompts sent to the LLM\n")

# Initialize SmartDataframe with maximum verbosity
sdf = pai.SmartDataframe(
    df,
    config={
        "llm": llm,
        "column_descriptions": column_descriptions,
        "verbose": True,
        "enforce_privacy": False,
        "enable_logging": True,
        "max_retries": 1,  # Reduce retries for faster testing
    },
)

print("=== SENDING QUERY TO SEE PROMPT ===")
print("Query: 'What is the total sales amount?'")
print("=" * 50)

# This will trigger the prompt generation and you'll see it in the logs
response = sdf.chat("What is the total sales amount?")
print(f"\nFinal Response: {response}")

print("\n" + "=" * 50)
print("PROMPT TEMPLATE STRUCTURE")
print("=" * 50)

# Show the default prompt template structure (current PandasAI version)
print("Default PandasAI Prompt Template:")
print("-" * 30)
print("""
### Instructions
You are a Python data analyst assistant. Your task is to write a single, clean Python script to answer the user's question using the provided DataFrame `df`.

- You have access to the following dependencies: pandas, plotly.express, pyecharts.charts.
- The user has provided column descriptions. Use them to better understand the data.
- The final result should be assigned to the `result` variable.
- Do not add comments or extra explanations.
- You can only use the variable `df` which is already loaded.

### Data
The DataFrame `df` has the following structure:
{dataframe_head}

Column Descriptions:
{column_descriptions}

### Previous Conversation
{conversation_history}

### User Query
{user_query}

### Generated Python Code
```python
{code}
```
""")

print("\n" + "=" * 50)
print("CUSTOM PROMPT EXAMPLE")
print("=" * 50)

# Show how to create a custom prompt
custom_prompt = """
You are a Python data analyst assistant. Your task is to write a single, clean Python script to answer the user's question using the provided DataFrame `df`.

- You have access to the following dependencies: pandas, plotly.express, pyecharts.charts.
- The user has provided column descriptions. Use them to better understand the data.
- The final result should be assigned to the `result` variable.
- Do not add comments or extra explanations.
- You can only use the variable `df` which is already loaded.

### Data
The DataFrame `df` has the following structure:
{dataframe_head}

Column Descriptions:
{column_descriptions}

### Previous Conversation
{conversation_history}

### User Query
{user_query}

### Generated Python Code
```python
{code}
```
"""

print("Custom prompt template example:")
print("-" * 30)
print(custom_prompt)

print("\n" + "=" * 50)
print("HOW TO USE CUSTOM PROMPTS")
print("=" * 50)

# Show how to use custom prompts (updated for current PandasAI version)
print("Note: Custom prompts in current PandasAI version work differently.")
print("You can modify the system prompt through configuration instead.")


# You can use custom prompts like this:
# sdf = pai.SmartDataframe(df, config={
#     "llm": llm,
#     "column_descriptions": column_descriptions,
#     "custom_prompts": {"generate_response": CustomPrompt()}
# })

print("To use custom prompts, create a custom prompt class and pass it to the config.")
print("This allows you to control exactly what the LLM sees and how it responds.")
