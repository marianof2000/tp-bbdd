import asyncio

from app.mcp_server import mcp


def test_mcp_exposes_only_read_only_tools() -> None:
    """Precondiciones: el servidor MCP puede construirse sin abrir la base.
    Postcondiciones: publica sólo las seis herramientas de consulta declaradas.
    """

    async def list_tools():
        return await mcp.list_tools()

    tools = asyncio.run(list_tools())

    assert {tool.name for tool in tools} == {
        "buscar_libros",
        "buscar_libros_por_autor",
        "buscar_socios",
        "consultar_disponibilidad",
        "listar_prestamos_vencidos",
        "obtener_estadisticas_biblioteca",
    }
    assert all(tool.annotations.read_only_hint is True for tool in tools)
    assert all(tool.annotations.destructive_hint is False for tool in tools)
