import asyncio
from agents.understand_code_agent import clone_repo, cleanup_repo, find_java_files, run_code_understanding
from agents.instrumentation_advisor_agent import run_instrumentation_advisor
from agents.observability_inspector_agent import inspect_observability
from agents.validation_agent import validate_observability
from agents.docbuilder_agent import generate_report
from dotenv import load_dotenv
load_dotenv()

async def main(repo_url, branch="main", output_path="trace_report.md"):
    tmp_dir = clone_repo(repo_url, branch)
    try:
        java_files = find_java_files(tmp_dir)
        methods, code_summary = await run_code_understanding(java_files, use_llm=True)
        advisor_results = await run_instrumentation_advisor(methods)
        results = [{"file": f, "methods": advisor_results} for f in java_files]
        generate_report(results, code_summary, output_path)
        print(f"[Done] Report saved: {output_path}")
    finally:
        cleanup_repo(tmp_dir)

if __name__ == "__main__":
    asyncio.run(main("https://github.com/jaygajera17/E-commerce-project-springBoot"))
