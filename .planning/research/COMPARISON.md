# Comparison: Code Execution Strategies for AI Agents

**Context:** Security-critical decision for production CrewAI deployment
**Recommendation:** Docker-based execution with fail-closed fallback

## Quick Comparison

| Criterion | Docker (Default) | Daytona | RestrictedPython | Unsafe Mode |
|-----------|-----------------|---------|-----------------|-------------|
| Isolation | Container (shared kernel) | MicroVM (hardware) | Process (Python-level) | None (host) |
| Startup Latency | ~200ms | ~20ms | ~10ms | ~0ms |
| CVE Resistance | MEDIUM (kernel exploit) | HIGH | LOW (introspection escape) | NONE (direct RCE) |
| Daemon Required | Yes (Docker) | No | No | No |
| Production Ready | YES | EMERGING | NO | NEVER |
| Community Support | Primary | Growing | Deprecated | Not recommended |

## Detailed Analysis

### Option 1: Docker (CodeInterpreterTool Default) - RECOMMENDED
**Strengths:**
- Hardware isolation from host
- Well-understood security model
- Native CrewAI support
- Supports arbitrary dependencies

**Weaknesses:**
- Requires Docker daemon (not available in all environments)
- Silent fallback to restricted sandbox if Docker unavailable
- Container escape possible via kernel exploits
- ~200ms startup overhead

**Best for:** Production deployments where Docker is available

### Option 2: Daytona Sandbox - ALTERNATIVE
**Strengths:**
- Hardware-level isolation (QEMU microVMs)
- No daemon required
- Faster startup (~20ms vs 200ms)
- Network disabled by default
- Fresh VM per execution, no state leakage

**Weaknesses:**
- Less community adoption than Docker
- Linux-only primary (macOS/Windows limited)
- Newer, less battle-tested

**Best for:** CI/CD environments, macOS deployments, stronger isolation needs

### Option 3: RestrictedPython (Sandbox Fallback) - AVOID
**Strengths:**
- No external dependencies
- Fast startup

**Weaknesses:**
- Python introspection allows sandbox escape (CVE-2026-4516)
- Blocks fundamental modules making it impractical
- Not a real security boundary

**Best for:** Absolutely nothing in production

### Option 4: Unsafe Mode - NEVER USE
**Strengths:**
- Fastest, simplest

**Weaknesses:**
- Direct RCE via prompt injection (CVE-2026-4516)
- No isolation whatsoever
- Same process as host

**Best for:** Development only with zero external input

## Recommendation

**Primary:** Docker-based CodeInterpreterTool with explicit configuration:
```python
from crewai_tools import CodeInterpreterTool

code_interpreter = CodeInterpreterTool(
    unsafe_mode=False,  # Explicit: never use unsafe
    # No fallback - fail closed
)
```

**Fail-Closed Pattern:**
```python
def execute_code_safely(code: str) -> str:
    tool = CodeInterpreterTool(unsafe_mode=False)
    try:
        return tool._run(code=code)
    except Exception as e:
        # Fail closed: don't silently fall back
        raise SecurityError(f"Code execution unavailable: {e}")
```

**Alternative:** If Docker unavailable, use Daytona:
```python
from crewai_tools import DaytonaPythonTool

tool = DaytonaPythonTool(
    persistent=False,  # Ephemeral per execution
    # No unsafe mode option
)
```

## Sources

- [CodeInterpreterTool Documentation](https://docs.crewai.com/tools/ai-ml/codeinterpretertool) - HIGH
- [CVE-2026-4516 Details](https://github.com/crewAIInc/crewAI/issues/4516) - HIGH
- [exec-sandbox Feature Request](https://github.com/crewAIInc/crewAI/issues/4702) - MEDIUM
- [sandlock Feature Request](https://github.com/crewAIInc/crewAI/issues/5150) - MEDIUM