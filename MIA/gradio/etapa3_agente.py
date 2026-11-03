import asyncio
import sys

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

MODELO = "openrouter:deepseek/deepseek-v4.1-flash"

SISTEMA = """Eres el asistente técnico de un estudio de arquitectura. Respondes dudas
sobre el Documento Básico DB-SUA del Código Técnico de la Edificación.

- Busca siempre en el documento con la herramienta buscar_normativa antes de
  responder. No respondas de memoria.
- Cita el apartado y la página de cada dato que uses.
- Si el documento no responde la pregunta, dilo.
- Para cualquier cálculo, usa la herramienta correspondiente: no calcules tú.
- Responde en español, de forma breve."""


def calcular_pendiente(desnivel_m: float, longitud_m: float) -> str:
    """Calcula la pendiente de una rampa en porcentaje.

    Args:
        desnivel_m: Diferencia de altura que salva la rampa, en metros.
        longitud_m: Longitud de la rampa medida en horizontal, en metros.
    """
    if longitud_m <= 0:
        return "La longitud debe ser mayor que 0."
    return f"{desnivel_m / longitud_m * 100:.2f} %"


async def crear_agente():
    mcp = MultiServerMCPClient(
        {
            "buscador": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:7860/gradio_api/mcp/",
            }
        }
    )
    herramientas_mcp = await mcp.get_tools()

    return create_deep_agent(
        model=MODELO,
        tools=[calcular_pendiente, *herramientas_mcp],
        system_prompt=SISTEMA,
        # Los ficheros del agente (skills e informes) viven en esta carpeta
        backend=FilesystemBackend(root_dir="espacio_agente", virtual_mode=True),
        skills=["/skills/"],
    )


async def main(pregunta):
    agente = await crear_agente()
    resultado = await agente.ainvoke({"messages": [{"role": "user", "content": pregunta}]})

    for m in resultado["messages"]:
        for llamada in getattr(m, "tool_calls", None) or []:
            print(f"→ {llamada['name']}({llamada['args']})")
    print("\n" + resultado["messages"][-1].text)


if __name__ == "__main__":
    pregunta = " ".join(sys.argv[1:]) or (
        "Una rampa de un itinerario accesible salva 40 cm en 5 m de longitud. ¿Cumple?"
    )
    asyncio.run(main(pregunta))