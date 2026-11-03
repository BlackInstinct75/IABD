import re

import chromadb
import gradio as gr
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
collection = chromadb.PersistentClient(path="chroma_db").get_collection("db_sua")

# Para BM25 hacen falta todos los fragmentos en memoria
todos = collection.get(include=["documents", "metadatas"])
fragmentos = [
    {"id": i, "texto": t, **m}
    for i, t, m in zip(todos["ids"], todos["documents"], todos["metadatas"])
]


def palabras(texto):
    return re.findall(r"\d+(?:[.,]\d+)+|\w+", texto.lower())


bm25 = BM25Okapi([palabras(f["texto"]) for f in fragmentos])


def busqueda_vectorial(pregunta, n):
    q = embedder.encode_query([pregunta])
    r = collection.query(query_embeddings=q.tolist(), n_results=n)
    return [{"id": i, "texto": t, **m} for i, t, m in zip(r["ids"][0], r["documents"][0], r["metadatas"][0])]


def busqueda_palabras(pregunta, n):
    puntuaciones = bm25.get_scores(palabras(pregunta))
    mejores = sorted(range(len(fragmentos)), key=lambda i: puntuaciones[i], reverse=True)[:n]
    return [fragmentos[i] for i in mejores]


def buscar_normativa(consulta: str, n: int = 2) -> str:
    """Busca fragmentos del Documento Básico DB-SUA (Seguridad de utilización y
    accesibilidad) del Código Técnico de la Edificación.

    Combina una búsqueda semántica y una búsqueda por palabras clave, así que
    sirve tanto para preguntas en lenguaje natural como para números de
    apartado o de norma (por ejemplo, "apartado 4.3.4" o "UNE 41901").

    Args:
        consulta: Pregunta o términos que se quieren buscar en el documento.
        n: Número de fragmentos que devuelve cada tipo de búsqueda (entre 1 y 5).

    Returns:
        Los fragmentos encontrados, cada uno con su apartado y su página.
    """
    n = max(1, min(int(n), 5))
    resultados, vistos = [], set()
    for f in busqueda_vectorial(consulta, n) + busqueda_palabras(consulta, n):
        if f["id"] not in vistos:
            vistos.add(f["id"])
            resultados.append(f"[{f['apartado']}, pág. {f['pagina']}]\n{f['texto']}")
    return "\n\n---\n\n".join(resultados)


demo = gr.Interface(
    fn=buscar_normativa,
    inputs=[
        gr.Textbox(label="Consulta"),
        gr.Slider(1, 5, value=2, step=1, label="Fragmentos por búsqueda"),
    ],
    outputs=gr.Textbox(label="Fragmentos", lines=20),
    title="Buscador del DB-SUA",
    examples=[["¿Qué dice el apartado 4.3.4?", 2], ["¿Hace falta pararrayos?", 2]],
    api_name="buscar_normativa",
)

if __name__ == "__main__":
    demo.launch(mcp_server=True)