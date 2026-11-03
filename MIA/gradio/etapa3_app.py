import gradio as gr

from etapa3_agente import crear_agente

agente = None


def texto(contenido):
    if isinstance(contenido, str):
        return contenido
    return "".join(p.get("text", "") for p in contenido if p.get("type") == "text")


async def responder(mensaje, historial):
    global agente
    if agente is None:
        agente = await crear_agente()

    # Solo pasamos al agente los mensajes de la conversación, no los de las herramientas
    mensajes = [
        {"role": m["role"], "content": texto(m["content"])}
        for m in historial
        if not (m.get("metadata") or {}).get("title")
    ]
    mensajes.append({"role": "user", "content": mensaje})

    pasos = []
    async for actualizacion in agente.astream({"messages": mensajes}, stream_mode="updates"):
        for nodo in actualizacion.values():
            if not nodo or "messages" not in nodo:
                continue
            for m in nodo["messages"]:
                for llamada in getattr(m, "tool_calls", None) or []:
                    pasos.append(
                        gr.ChatMessage(
                            content=str(llamada["args"]),
                            metadata={"title": f"🔧 {llamada['name']}"},
                        )
                    )
                    yield pasos
                if m.type == "ai" and m.text and not getattr(m, "tool_calls", None):
                    yield pasos + [gr.ChatMessage(content=m.text)]


demo = gr.ChatInterface(
    fn=responder,
    title="Asistente DB-SUA",
    examples=[
        "Una rampa de un itinerario accesible salva 40 cm en 5 m de longitud. ¿Cumple?",
        "¿Qué dice el apartado 4.3.4?",
        "Hazme un informe de cumplimiento de una barandilla de 85 cm en un balcón a 4 m de altura.",
    ],
)

if __name__ == "__main__":
    demo.launch(server_port=7861)