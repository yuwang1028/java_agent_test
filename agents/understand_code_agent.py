import os
import shutil
import tempfile
import javalang
#from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI

# ==== 1. Init optional LLM ====
llm = ChatVertexAI(model_name="gemini-2.5-pro", temperature=0.2)

# ==== 2. Repo operations ====
def clone_repo(repo_url, branch="main"):
    tmp_dir = tempfile.mkdtemp()
    print(f"[CodeUnderstanding] Cloning {repo_url} -> {tmp_dir}")
    from git import Repo
    Repo.clone_from(repo_url, tmp_dir, branch=branch)
    return tmp_dir

def cleanup_repo(tmp_dir):
    shutil.rmtree(tmp_dir)

# ==== 3. Find java files ====
def find_java_files(base_dir):
    java_files = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(root, f))
    return java_files

# ==== 4. Analyze code structure ====
def parse_java_methods(java_code):
    tree = javalang.parse.parse(java_code)
    methods = []
    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        body = node.body.__str__() if node.body else ""
        methods.append({
            "name": node.name,
            "has_trace": "tracer.spanBuilder" in body or "@WithSpan" in body,
            "content": body
        })
    return methods

# ==== 5. Optional: generate call graph / class diagram via LLM ====
def generate_code_summary_with_llm(all_methods):
    combined_code = "\n".join([m["content"] for m in all_methods])
    prompt = f"""
You are a Java expert.
Analyze the following code and create:
1. A high-level call graph or component interaction summary.
2. Important classes and their roles.

Code:
{combined_code}

Return a concise description.
"""
    response = llm.invoke(prompt)
    return response.content

# ==== 6. Run ====
async def run_code_understanding(java_files, use_llm=True):
    all_methods = []
    for file in java_files:
        with open(file, "r", encoding="utf-8") as f:
            java_code = f.read()
        methods = parse_java_methods(java_code)
        all_methods.extend(methods)
    llm_summary = generate_code_summary_with_llm(all_methods) if use_llm else None
    return all_methods, llm_summary
