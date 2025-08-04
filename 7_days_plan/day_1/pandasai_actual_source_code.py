"""
Actual PandasAI Chat Source Code
================================

English Description:
This file shows the actual open source code of PandasAI's chat method
from the official repository.

中文描述：
此文件显示PandasAI聊天方法的实际开源代码，
来自官方仓库。

Source: https://github.com/gventuri/pandas-ai
"""


def show_actual_source_code():
    """Show the actual source code of PandasAI chat method"""

    print("=" * 80)
    print("ACTUAL PANDASAI CHAT SOURCE CODE")
    print("=" * 80)

    print("""
    # ACTUAL SOURCE CODE FROM PANDASAI REPOSITORY
    # ===========================================
    
    # File: pandasai/smart_dataframe/__init__.py
    # Lines: 58-78
    
    def chat(self, query: str, output_type: Optional[str] = None):
        \"\"\"
        Run a query on the dataframe.
        Args:
            query (str): Query to run on the dataframe
            output_type (Optional[str]): Add a hint for LLM of which
                type should be returned by `analyze_data()` in generated
                code. Possible values: "number", "dataframe", "plot", "string":
                    * number - specifies that user expects to get a number
                        as a response object
                    * dataframe - specifies that user expects to get
                        pandas dataframe as a response object
                    * plot - specifies that user expects LLM to build
                        a plot
                    * string - specifies that user expects to get text
                        as a response object
        Raises:
            ValueError: If the query is empty
        \"\"\"
        return self._agent.chat(query, output_type)
    
    # File: pandasai/agent/base.py
    # Lines: 83-95
    
    def chat(self, query: str, output_type: Optional[str] = None):
        \"\"\"
        Start a new chat interaction with the assistant on Dataframe.
        \"\"\"
        if self._state.config.llm is None:
            raise ValueError(
                "PandasAI API key does not include LLM credits. Please configure an OpenAI or LiteLLM key. "
                "Learn more at: https://docs.pandas-ai.com/v3/large-language-models#how-to-set-up-any-llm%3F"
            )

        self.start_new_conversation()
        return self._process_query(query, output_type)
    
    # File: pandasai/agent/base.py
    # Lines: 260-284
    
    def _process_query(self, query: str, output_type: Optional[str] = None):
        \"\"\"Process a user query and return the result.\"\"\"
        query = UserQuery(query)
        self._state.logger.log(f"Question: {query}")
        self._state.logger.log(
            f"Running PandasAI with {self._state.config.llm.type} LLM..."
        )

        self._state.output_type = output_type
        try:
            self._state.assign_prompt_id()

            # Generate code
            code = self.generate_code_with_retries(query)

            # Execute code with retries
            result = self.execute_with_retries(code)

            self._state.logger.log("Response generated successfully.")
            # Generate and return the final response
            return result

        except CodeExecutionError:
            return self._handle_exception(code)
    
    # File: pandasai/agent/base.py
    # Lines: 102-113
    
    def generate_code(self, query: Union[UserQuery, str]) -> str:
        \"\"\"Generate code using the LLM.\"\"\"

        self._state.memory.add(str(query), is_user=True)

        self._state.logger.log("Generating new code...")
        prompt = get_chat_prompt_for_sql(self._state)

        code = self._code_generator.generate_code(prompt)
        self._state.last_prompt_used = prompt
        return code
    
    # File: pandasai/agent/base.py
    # Lines: 114-125
    
    def execute_code(self, code: str) -> dict:
        \"\"\"Execute the generated code.\"\"\"
        self._state.logger.log(f"Executing code: {code}")

        code_executor = CodeExecutor(self._state.config)
        code_executor.add_to_env("execute_sql_query", self._execute_sql_query)

        if self._sandbox:
            return self._sandbox.execute(code, code_executor.environment)

        return code_executor.execute_and_return_result(code)
    
    # File: pandasai/agent/base.py
    # Lines: 160-180
    
    def generate_code_with_retries(self, query: str) -> Any:
        \"\"\"Execute the code with retry logic.\"\"\"
        max_retries = self._state.config.max_retries
        attempts = 0
        try:
            return self.generate_code(query)
        except Exception as e:
            exception = e
            while attempts <= max_retries:
                try:
                    return self._regenerate_code_after_error(
                        self._state.last_code_generated, exception
                    )
                except Exception as e:
                    exception = e
                    attempts += 1
                    if attempts > max_retries:
                        self._state.logger.log(
                            f"Maximum retry attempts exceeded. Last error: {e}"
                        )
                        raise
                    self._state.logger.log(
                        f"Retrying Code Generation ({attempts}/{max_retries})..."
                    )
            return None
    
    # File: pandasai/agent/base.py
    # Lines: 182-205
    
    def execute_with_retries(self, code: str) -> Any:
        \"\"\"Execute the code with retry logic.\"\"\"
        max_retries = self._state.config.max_retries
        attempts = 0

        while attempts <= max_retries:
            try:
                result = self.execute_code(code)
                return self._response_parser.parse(result, code)
            except Exception as e:
                attempts += 1
                if attempts > max_retries:
                    self._state.logger.log(f"Max retries reached. Error: {e}")
                    raise
                self._state.logger.log(
                    f"Retrying execution ({attempts}/{max_retries})..."
                )
                code = self._regenerate_code_after_error(code, e)

        return None
    """)

    print("\n" + "=" * 80)
    print("KEY COMPONENTS IN ACTUAL SOURCE")
    print("=" * 80)

    print("""
    ACTUAL COMPONENTS USED:
    =======================
    
    1. SmartDataframe.chat() - Entry point that delegates to Agent
    2. Agent.chat() - Main chat method with LLM validation
    3. Agent._process_query() - Core processing logic
    4. Agent.generate_code() - Uses LLM to generate Python code
    5. Agent.execute_code() - Executes generated code safely
    6. Agent.generate_code_with_retries() - Retry logic for code generation
    7. Agent.execute_with_retries() - Retry logic for code execution
    8. Agent._regenerate_code_after_error() - Error recovery
    9. Agent._handle_exception() - Exception handling
    
    KEY DIFFERENCES FROM OUR SIMPLIFIED VERSION:
    ===========================================
    
    1. Uses Agent class instead of direct SmartDataframe methods
    2. Has sophisticated retry logic for both code generation and execution
    3. Uses CodeGenerator and CodeExecutor classes
    4. Has proper error handling and recovery mechanisms
    5. Uses ResponseParser for formatting results
    6. Supports sandbox execution for security
    7. Has memory management for conversation history
    8. Uses proper logging throughout the process
    """)

    print("\n" + "=" * 80)
    print("ACTUAL METHOD CALL SEQUENCE")
    print("=" * 80)

    print("""
    ACTUAL METHOD CALL SEQUENCE:
    ============================
    
    sdf.chat("What is the total sales amount?")
    ├── SmartDataframe.chat() - Entry point
    │   └── return self._agent.chat(query, output_type)
    │
    ├── Agent.chat() - Main chat method
    │   ├── Check if LLM is configured
    │   ├── self.start_new_conversation()
    │   └── return self._process_query(query, output_type)
    │
    ├── Agent._process_query() - Core processing
    │   ├── query = UserQuery(query)
    │   ├── self._state.assign_prompt_id()
    │   ├── code = self.generate_code_with_retries(query)
    │   ├── result = self.execute_with_retries(code)
    │   └── return result
    │
    ├── Agent.generate_code_with_retries() - Code generation with retries
    │   ├── self.generate_code(query)
    │   ├── self._state.memory.add(str(query), is_user=True)
    │   ├── prompt = get_chat_prompt_for_sql(self._state)
    │   ├── code = self._code_generator.generate_code(prompt)
    │   └── self._state.last_prompt_used = prompt
    │
    └── Agent.execute_with_retries() - Code execution with retries
        ├── self.execute_code(code)
        ├── code_executor = CodeExecutor(self._state.config)
        ├── result = code_executor.execute_and_return_result(code)
        └── return self._response_parser.parse(result, code)
    """)


def show_actual_imports():
    """Show the actual imports used in PandasAI"""

    print("\n" + "=" * 80)
    print("ACTUAL IMPORTS USED IN PANDASAI")
    print("=" * 80)

    print("""
    # File: pandasai/smart_dataframe/__init__.py
    # Actual imports:
    
    import uuid
    from functools import cached_property
    from typing import Any, List, Optional, Union
    
    import pandas as pd
    
    from ..agent import Agent
    from ..config import Config
    from ..dataframe import DataFrame
    from ..helpers.logger import Logger
    
    # File: pandasai/agent/base.py
    # Actual imports:
    
    import traceback
    import warnings
    from typing import Any, List, Optional, Union
    
    import pandas as pd
    
    from ..config import Config
    from ..core.code_execution.base import CodeExecutor
    from ..core.code_generation.base import CodeGenerator
    from ..core.response_parser.base import ResponseParser
    from ..dataframe import DataFrame, VirtualDataFrame
    from ..exceptions import (
        CodeExecutionError,
        InvalidLLMOutputType,
        MissingVectorStoreError,
    )
    from ..llm.base import LLM
    from ..memory.base import Memory
    from ..prompts.base import BasePrompt
    from ..sandbox.base import Sandbox
    from ..state import AgentState
    from ..vectorstore.base import VectorStore
    from .query_builder.base import BaseQueryBuilder
    from .state import AgentState
    from .user_query import UserQuery
    """)


if __name__ == "__main__":
    # Show actual source code
    show_actual_source_code()

    # Show actual imports
    show_actual_imports()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("This shows the actual open source code from PandasAI repository.")
    print(
        "The real implementation is much more sophisticated than our simplified version,"
    )
    print("with proper error handling, retry logic, and security measures.")
    print("\nSource: https://github.com/gventuri/pandas-ai")
