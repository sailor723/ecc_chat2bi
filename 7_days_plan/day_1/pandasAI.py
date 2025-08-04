"""
Day 1: PandasAI Basic Implementation
====================================

English Description:
This file demonstrates the basic setup and usage of PandasAI with Azure OpenAI.
It shows how to use pai.chat() directly with a DataFrame, configure column descriptions,
enable verbose logging to see prompts, and execute natural language queries.

Key Features:
- Azure OpenAI LLM configuration
- Sample sales dataset with realistic data
- Column descriptions for enhanced data understanding
- Verbose logging for prompt inspection
- Multiple query examples demonstrating different analysis types
- Direct pai.chat() usage without SmartDataframe

中文描述：
此文件演示了PandasAI与Azure OpenAI的基本设置和使用。
它展示了如何直接使用pai.chat()与DataFrame、配置列描述、
启用详细日志记录以查看提示，并执行自然语言查询。

主要功能：
- Azure OpenAI LLM配置
- 包含真实数据的示例销售数据集
- 用于增强数据理解的列描述
- 用于提示检查的详细日志记录
- 演示不同分析类型的多个查询示例
- 直接使用pai.chat()而不使用SmartDataframe

Usage: python pandasAI.py
"""

import pandasai as pai
from pandasai_openai import AzureOpenAI
import os
import pandas as pd
# Note: pandasai.prompts structure has changed in newer versions
# We'll use a different approach to inspect prompts


api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")


llm = AzureOpenAI(
    azure_endpoint=api_endpoint,
    api_key=api_key,
    deployment_name=deployment_name,
    api_version=api_version,
)  # The name of your deployed model

pai.config.set({"llm": llm})

# Sample sales data
data = {
    "OrderID": [1, 2, 3, 4, 5],
    "CustomerID": ["C001", "C002", "C003", "C004", "C005"],
    "ProductCategory": ["Electronics", "Clothing", "Electronics", "Books", "Clothing"],
    "SalesAmount": [1200.50, 75.20, 850.00, 45.99, 120.75],
    "OrderDate": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
    "Region": ["East", "West", "North", "South", "East"],
}

df = pd.DataFrame(data)

# Convert to PandasAI DataFrame with column descriptions
pandasai_df = pai.DataFrame(
    df,
    name="sales_data",
    description="Sample sales data with order information",
    column_descriptions={
        "OrderID": "A unique identifier for each sales order.",
        "CustomerID": "Identifier for the customer who placed the order.",
        "ProductCategory": "The category of the product sold.",
        "SalesAmount": "The monetary value of the sale in USD.",
        "OrderDate": "The date when the order was placed.",
        "Region": "The geographical region where the sale occurred.",
    },
)

# Configure PandasAI with LLM
pai.config.set(
    {
        "llm": llm,
        "verbose": True,  # Enable verbose logging to see prompts
        "enforce_privacy": False,  # Allow seeing the generated code
        "enable_logging": True,  # Enable detailed logging
    }
)

# Example queries with prompt inspection
print("=== PandasAI Chat Examples with Prompt Inspection ===")

# Query 1: Basic text question
print("\n" + "=" * 50)
print("QUERY 1: What is the total sales amount?")
print("=" * 50)
response1 = pai.chat("What is the total sales amount?", pandasai_df)
print(f"RESPONSE: {response1}\n")

# Query 2: Data analysis
print("\n" + "=" * 50)
print("QUERY 2: Show me sales by product category")
print("=" * 50)
response2 = pai.chat("Show me sales by product category", pandasai_df)
print(f"RESPONSE: {response2}\n")

# Query 3: Complex analysis
print("\n" + "=" * 50)
print("QUERY 3: Which region has the highest average sales?")
print("=" * 50)
response3 = pai.chat("Which region has the highest average sales?", pandasai_df)
print(f"RESPONSE: {response3}\n")

print("=== End of Examples ===")

# Additional: Show how to inspect the prompt template
print("\n" + "=" * 50)
print("PROMPT TEMPLATE INSPECTION")
print("=" * 50)

# You can also create a custom prompt template to see the structure


# Show the default prompt template structure (current PandasAI version)
print("Default PandasAI Prompt Template Structure:")
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
