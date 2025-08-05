import os
import shutil
import tempfile
import javalang
from datetime import datetime
from git import Repo
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# ==== 0. Load environment variables ====
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
os.environ["OPENAI_API_KEY"] = openai_api_key

# ==== 1. Define output data structure ====
class TraceSuggestion(BaseModel):
    method: str = Field(..., description="Method name")
    has_trace: bool = Field(..., description="Whether Trace/Span already exists")
    suggestion: str = Field(..., description="Trace/Span recommendation")

parser = PydanticOutputParser(pydantic_object=TraceSuggestion)

# ==== 2. Initialize OpenAI model ====
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

# ==== 3. Prompt template ====
prompt_template = f"""
Analyze the following Java method and check if it has Trace/Span instrumentation.
Output must be in JSON format.
Method name: {{method}}
Method code:
{{code}}

{parser.get_format_instructions()}
"""


# ==== 4. Clone Git repository ====
def clone_repo(repo_url, branch="main"):
    tmp_dir = tempfile.mkdtemp()
    print(f"Cloning {repo_url} to {tmp_dir}")
    Repo.clone_from(repo_url, tmp_dir, branch=branch)
    return tmp_dir

# ==== 5. Find Java files ====
def find_java_files(base_dir):
    java_files = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))
    return java_files

# ==== 6. Parse Java methods ====
def analyze_java_code(java_code):
    tree = javalang.parse.parse(java_code)
    methods = []
    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        body = node.body.__str__() if node.body else ""
        has_trace = "tracer.spanBuilder" in body or "@WithSpan" in body
        methods.append({
            "name": node.name,
            "has_trace": has_trace,
            "content": body
        })
    return methods

# ==== 7. Generate Trace/Span suggestion ====
def generate_trace_suggestions(method):
    """Generate Trace/Span suggestions with OpenTelemetry instrumentation example"""
    try:
        prompt = f"""
Analyze the following Java method and check if it has Trace/Span instrumentation.

1. Determine if Trace/Span instrumentation already exists (e.g., tracer.spanBuilder, @WithSpan).
2. If missing, provide:
   - Explanation of where instrumentation should be added.
   - The modified method code with OpenTelemetry instrumentation (use tracer.spanBuilder and span.end()).

Return output strictly in JSON format:
{{
  "method": "{method['name']}",
  "has_trace": true/false,
  "suggestion": "short text description",
  "modified_code": "instrumented Java method code"
}}

Method code:
{method['content'].replace("{","{{").replace("}","}}")}

{parser.get_format_instructions()}
"""
        response = llm.invoke(prompt)
        return parser.parse(response.content)
    except Exception as e:
        print(f"[Error] Failed to process method {method['name']}: {e}")
        return TraceSuggestion(
            method=method['name'],
            has_trace=False,
            suggestion=f"Error occurred: {e}"
        )



# ==== 8. Generate Markdown report ====
def generate_report(results, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Java Trace/Span Analysis Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for file_result in results:
            f.write(f"## File: {file_result['file']}\n")
            for method in file_result['methods']:
                f.write(f"### Method: {method.method}\n")
                f.write(f"- Has Trace: {method.has_trace}\n")
                f.write(f"#### Suggestion:\n")
                f.write(f"{method.suggestion}\n\n")

# ==== 9. Main workflow ====
def scan_repo(repo_url, branch="main", output_path="trace_report.md"):
    tmp_dir = clone_repo(repo_url, branch)
    try:
        java_files = find_java_files(tmp_dir)
        results = []
        for file in java_files:
            print(f"Analyzing file: {file}")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    java_code = f.read()
                methods = analyze_java_code(java_code)
                parsed_methods = []
                for m in methods:
                    suggestion = generate_trace_suggestions(m)
                    parsed_methods.append(suggestion)
                results.append({"file": file, "methods": parsed_methods})
            except Exception as e:
                print(f"[Error] Failed to process file {file}: {e}")
                results.append({"file": file, "methods": [
                    TraceSuggestion(
                        method="N/A",
                        has_trace=False,
                        suggestion=f"File-level error: {e}"
                    )
                ]})
        generate_report(results, output_path)
        print(f"Report generated: {output_path}")
    finally:
        shutil.rmtree(tmp_dir)

# ==== 10. Run the script ====
if __name__ == "__main__":
    # Replace with your own Git repository URL
    scan_repo("https://github.com/jaygajera17/E-commerce-project-springBoot", branch="main", output_path="trace_report.md")
