# Java Agent Test – Observability & Multi-Agent Orchestration

## Overview
This project demonstrates a **multi-agent system** designed to enhance Java application observability, validation, and documentation through LLM-based code analysis and static inspection tools. It is designed to work with enterprise environments, CI/CD pipelines, and future integrations with external systems like Slack, Jira, and ServiceNow.

---

## Key Features

### 1. Observability Inspector Agent
- Detects missing instrumentation (e.g., missing `Trace`/`Span`) in Java code.
- Uses rule engines (Checkstyle, SpotBugs) and future OpenTelemetry rule integrations.
- Standardizes evaluation based on enterprise observability rules.

### 2. Validation Agent
- Validates code changes for observability and documentation compliance.
- Designed for CI/CD integration with pass/fail scoring.

### 3. DocBuilder Agent
- Generates human-friendly documentation:
  - Mermaid diagrams
  - UML call relationship diagrams
  - Auto-updated `README.md`
- Future integration with enterprise knowledge bases (e.g., internal wiki).

### 4. Orchestrator Agent
- Manages scheduling and execution of multiple agents.
- Supports context memory for multi-file analysis.
- Planned task queue and async execution support.

### 5. Tool Integration (Future)
- Integration with enterprise tools:
  - Jira / ServiceNow (ticketing)
  - Slackbot (notifications)
  - CI/CD hooks
