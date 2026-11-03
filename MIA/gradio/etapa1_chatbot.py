import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODELO = "deepseek/deepseek-v4.1-flash"

cliente = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

SISTEMA = (
    "Eres un asistente que ayuda a un estudio de arquitectura con dudas sobre "
    "el Código Técnico de la Edificación. Responde en español, de forma breve. "
    "Si no estás seguro de un dato, dilo."
)


def texto(contenido):
    """Gradio guarda el contenido de cada mensaje como una lista de partes."""
    if isinstance(contenido, str):
        return contenido
    return "".join(p.get("text", "") for p in contenido if p.get("type") == "text")


def responder(mensaje, historial):
    mensajes = [{"role": "system", "content": SISTEMA}]
    for m in historial:
        mensajes.append({"role": m["role"], "content": texto(m["content"])})
    mensajes.append({"role": "user", "content": mensaje})

    respuesta = cliente.chat.completions.create(
        model=MODELO,
        messages=mensajes,
        stream=True,
    )

    texto_respuesta = ""
    for trozo in respuesta:
        if trozo.choices and trozo.choices[0].delta.content:
            texto_respuesta += trozo.choices[0].delta.content
            yield texto_respuesta


demo = gr.ChatInterface(
    fn=responder,
    title="Asistente DB-SUA",
    examples=[
        "¿Qué altura mínima debe tener una barandilla?",
        "¿Qué pendiente máxima puede tener una rampa accesible de 5 m?",
    ],
)

if __name__ == "__main__":
    demo.launch()