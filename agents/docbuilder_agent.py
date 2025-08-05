from datetime import datetime

def generate_report(results, code_summary, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Java Trace/Span Analysis Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if code_summary:
            f.write("## Code Structure Summary\n")
            f.write(f"{code_summary}\n\n")
        for file_result in results:
            f.write(f"## File: {file_result['file']}\n")
            for method in file_result['methods']:
                f.write(f"### Method: {method.method}\n")
                f.write(f"- Has Trace: {method.has_trace}\n")
                f.write(f"#### Suggestion:\n")
                f.write(f"{method.suggestion}\n\n")
                if hasattr(method, "modified_code"):
                    f.write(f"#### Modified Code Example:\n")
                    f.write("```java\n")
                    f.write(f"{method.modified_code}\n")
                    f.write("```\n\n")
