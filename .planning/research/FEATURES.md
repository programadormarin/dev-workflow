# Feature Landscape: CrewAI Multi-Agent Systems

**Domain:** AI Agent Orchestration
**Researched:** May 2026

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Multi-agent orchestration** | Core value proposition — coordinating multiple agents | High | CrewAI's primary feature; hierarchical (sequential/parallel) execution |
| **Agent definitions** | Fundamental building block | Medium | Role, goal, backstory, tools, memory |
| **Task definitions** | Work units for agents | Medium | Description, expected_output, agent assignment |
| **LLM integration** | Agents need reasoning capability | Medium | Native for OpenAI/Anthropic/Gemini/Azure/Bedrock |
| **Tool support** | Agents need to act | Medium | Built-in tools + custom via @tool decorator |
| **Memory** | Agents remember context | Medium | Short-term (agent), crew-level memory |
| **Async execution** | Non-blocking crew runs | Medium | `akickoff()` for native async, `kickoff_async()` for thread-based |
| **Streaming** | Real-time output | Low | `stream=True` on Crew for token-by-token output |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Human-in-the-loop** | Pause for approval mid-execution | High | `@human_feedback` decorator, flow pause/resume |
| **Knowledge sources** | RAG over documents | Medium | Built-in knowledge base integration |
| **Guardrails** | Output validation | Medium | Hallucination guardrail, custom validators |
| **Flow orchestration** | Beyond simple crews | High | CrewAI Flows for complex workflows with routing |
| **Observability** | Debugging and monitoring | Medium | OpenTelemetry support, enterprise platform |
| **Crew base** | Shared agent definitions | Low | Reusable agent templates via @CrewBase |
| **Tool repository** | Shared tool collections | Low | Central registry for tools across crews |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **LiteLLM dependency** | Security incident, PyPI quarantine 2025 | Use native provider extras (`crewai[openai]`, `crewai[anthropic]`) |
| **LangChain integration** | CrewAI is standalone now | Use native CrewAI APIs only |
| **Sync-only execution** | Modern systems need concurrency | Use `akickoff()` for true async |
| **Hardcoded LLM providers** | Lock-in, flexibility lost | Use configurable LLM class |
| **No type hints** | Maintenance nightmare | Use pyright for type checking from start |

## Feature Dependencies

```
Agent → Task → Crew (required order)
Crew.akickoff() → Async event loop (requires pytest-asyncio for testing)
LLM configuration → Native SDK extras (openai, anthropic, etc.)
Human feedback → Flow pause (requires persistence backend)
Knowledge → Vector store (optional, for RAG)
```

## MVP Recommendation

Prioritize:
1. **Multi-agent orchestration** — core value
2. **LLM integration** — agents need reasoning
3. **Basic tools** — file read/write, HTTP requests

Defer: Human-in-the-loop, Knowledge sources, Flow orchestration — these add complexity and are not needed for initial crew functionality

## Sources

- CrewAI Concepts: https://docs.crewai.com/concepts/agents
- CrewAI Learn: https://docs.crewai.com/learn/kickoff-async
- CrewAI GitHub: https://github.com/crewAIInc/crewAI