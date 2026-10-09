from mcp.server.fastmcp import FastMCP
from .core import delegate, usage, insights

mcp = FastMCP('ai-router')

@mcp.tool()
def delegate_task(task: str, task_type: str = 'general', context: str = '', local_only: bool = True) -> dict:
    """Analyze a bounded task using a local AI by default. Types: code, tests, review, docs, general. Cloud requires local_only=false AND cloud_enabled=true. Never send secrets."""
    return delegate(task, task_type, context, local_only)

@mcp.tool()
def router_usage() -> dict:
    """Return UTC-day call counts and local budgets by provider."""
    return usage()

@mcp.tool()
def router_insights() -> dict:
    """Local-only observability: call totals, per-provider success rate, average latency, and a rough estimate of tokens offloaded to local/free providers. Computed from the local SQLite audit only; makes no network calls."""
    return insights()


def main():
    mcp.run(transport='stdio')

if __name__ == '__main__':
    main()
