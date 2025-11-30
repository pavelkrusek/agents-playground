import asyncio
import time

from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, SseConnectionParams
from loguru import logger
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from adk_playground.core.mcp import get_mcp_tools

load_dotenv()


async def diagnose_stdio(toolset) -> None:
    """stdio MCP server (e.g. mcp-wikidata)."""
    conn = getattr(toolset, "_connection_params", None)
    if not isinstance(conn, StdioConnectionParams):
        logger.warning("Toolset {} is not stdio (StdioConnectionParams), skipping.", toolset)
        return

    server_params = conn.server_params

    logger.info(
        "\n=== MCP STDIO SERVER: command='{}' args={} cwd='{}' ===",
        server_params.command,
        server_params.args,
        server_params.cwd,
    )

    start = time.perf_counter()
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            init_latency = (time.perf_counter() - start) * 1000
            logger.info("✓ Initialized in {:.2f} ms", init_latency)

            tools_resp = await session.list_tools()
            tools = tools_resp.tools
            if not tools:
                logger.warning("‼ No tools reported by this MCP server.")
                return

            logger.info("Available tools:")
            for t in tools:
                logger.info("  • {}: {}", t.name, t.description or "")

            if any(t.name == "sparql_query" for t in tools):
                logger.info("\n⚙ Testing sparql_query...")

                query = """
                SELECT (COUNT(?item) AS ?count) WHERE {
                    ?item wdt:P31 wd:Q5 .
                }
                LIMIT 10
                """

                start = time.perf_counter()
                result = await session.call_tool(
                    "sparql_query",
                    {
                        "query": query,
                        "format": "json",
                    },
                )
                latency = (time.perf_counter() - start) * 1000

                logger.info("✓ SPARQL ok ({:.2f} ms)", latency)
                logger.info("  Result type: {}", type(result))
                logger.info("  Result repr: {}", repr(result)[:200])


async def diagnose_sse(toolset) -> None:
    """SSE MCP server (Wikipedia)."""
    conn = getattr(toolset, "_connection_params", None)
    if not isinstance(conn, SseConnectionParams):
        logger.warning("Toolset {} is not SSE (SseConnectionParams), skipping.", toolset)
        return

    url = conn.url
    logger.info("\n=== MCP SSE SERVER: url='{}' ===", url)

    start = time.perf_counter()
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            init_latency = (time.perf_counter() - start) * 1000
            logger.info("✓ Initialized in {:.2f} ms", init_latency)

            tools_resp = await session.list_tools()
            tools = tools_resp.tools
            if not tools:
                logger.warning("‼ No tools reported by this MCP SSE server.")
                return

            logger.info("Available tools:")
            for t in tools:
                logger.info("  • {}: {}", t.name, t.description or "")

            # Wikipedia: search
            if any(t.name == "search" for t in tools):
                logger.info("\n⚙ Testing Wikipedia search('Beethoven')...")
                start = time.perf_counter()
                result = await session.call_tool(
                    "search",
                    {
                        "query": "Beethoven",
                        "limit": 3,
                    },
                )
                latency = (time.perf_counter() - start) * 1000

                logger.info("✓ Wikipedia search ok ({:.2f} ms)", latency)
                output = getattr(result, "output", {})
                for r in output.get("results", []):
                    logger.info("   • {}", r.get("title"))

            # Wikipedia: page_extract
            if any(t.name == "page_extract" for t in tools):
                logger.info("\n⚙ Testing Wikipedia page_extract('Ludwig_van_Beethoven')...")
                start = time.perf_counter()
                result = await session.call_tool(
                    "page_extract",
                    {
                        "title": "Ludwig_van_Beethoven",
                        "sentences": 2,
                    },
                )
                latency = (time.perf_counter() - start) * 1000

                logger.info("✓ page_extract ok ({:.2f} ms)", latency)
                output = getattr(result, "output", {})
                extract = output.get("extract")
                if extract:
                    logger.info("  Extract: {}...", extract[:200])


async def main() -> None:
    logger.info("🔎 Starting MCP diagnostics...")

    toolsets = get_mcp_tools()
    if not toolsets:
        logger.error("‼ No MCP toolsets loaded! Check mcp.yaml / loader.")
        return

    logger.info("Found {} MCP toolset(s).", len(toolsets))

    for ts in toolsets:
        conn = getattr(ts, "_connection_params", None)

        if isinstance(conn, StdioConnectionParams):
            await diagnose_stdio(ts)
        elif isinstance(conn, SseConnectionParams):
            await diagnose_sse(ts)
        else:
            logger.warning(
                "Toolset {} - unknown type connection params ({}), skipping.",
                ts,
                type(conn),
            )

    logger.info("✅ MCP diagnostics finished.")


if __name__ == "__main__":
    asyncio.run(main())
