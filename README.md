# Java Trace/Span Analysis Tool

AI-powered static analysis for Java projects to detect and suggest improvements for Trace/Span instrumentation (OpenTelemetry).  
This tool clones a Java repository, parses Java methods, checks for existing tracing, and uses OpenAI GPT to suggest instrumentation improvements **with complete modified Java method code**.  
Results are exported as a **Markdown report**.

---

## Features
- **Clone GitHub repositories** automatically.
- **Parse Java methods** using AST (`javalang`).
- **Detect Trace/Span instrumentation** (`tracer.spanBuilder`, `@WithSpan`).
- **Generate AI-powered suggestions** for adding instrumentation.
- **Output modified Java methods** with OpenTelemetry tracing.
- **Markdown report output** with method-by-method details.

---

## Project Structure
