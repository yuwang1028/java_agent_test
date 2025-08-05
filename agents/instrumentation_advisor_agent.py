import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import asyncio

# ==== 0. Load env ====
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
os.environ["OPENAI_API_KEY"] = openai_api_key

# ==== 1. Output Model ====
class InstrumentationSuggestion(BaseModel):
    method: str = Field(..., description="Java method name")
    has_trace: bool = Field(..., description="Whether Trace/Span exists")
    suggestion: str = Field(..., description="Instrumentation recommendation")
    modified_code: str = Field(..., description="Full modified Java method code with OpenTelemetry")

parser = PydanticOutputParser(pydantic_object=InstrumentationSuggestion)

# ==== 2. LLM ====
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

# ==== 3. Prompt ====
def build_prompt(method_name: str, method_code: str):
    escaped_code = method_code.replace("{", "{{").replace("}", "}}")
    return f"""
You are an expert Java developer focusing on observability.

Analyze the following Java method:
- Detect if Trace/Span instrumentation exists.
- If missing, add OpenTelemetry instrumentation using tracer.spanBuilder and span.end().

Return STRICT JSON ONLY with ALL fields filled:
{{
  "method": "{method_name}",
  "has_trace": true/false,
  "suggestion": "Short description of what to add",
  "modified_code": "COMPLETE Java method WITH OpenTelemetry instrumentation"
}}

Even if Trace already exists, still output full Java method code in `modified_code`.

Method code:
{escaped_code}

{parser.get_format_instructions()}
"""

async def process_method(method):
    try:
        prompt = build_prompt(method["name"], method["content"])
        response = await llm.ainvoke(prompt)
        parsed = parser.parse(response.content)
        # ===== Ensure modified_code always has value =====
        if not parsed.modified_code.strip():
            parsed.modified_code = method["content"]
        return parsed
    except Exception as e:
        return InstrumentationSuggestion(
            method=method["name"],
            has_trace=method["has_trace"],
            suggestion=f"Error while processing method: {str(e)}",
            modified_code=method["content"]
        )

async def run_instrumentation_advisor(methods):
    tasks = [asyncio.create_task(process_method(m)) for m in methods]
    return await asyncio.gather(*tasks)
