
from docling.document_converter import DocumentConverter
from pathlib import Path
import urllib.request
import re
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
import chromadb

Path("docs").mkdir(exist_ok=True)
pdf_path = Path("docs/DB-SUA.pdf")

if not pdf_path.exists():
    urllib.request.urlretrieve(
        "https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf",
        pdf_path
    )

print(f"{pdf_path}: {pdf_path.stat().st_size / 1e6:.1f} MB")

converter = DocumentConverter()
result = converter.convert(pdf_path)
doc = result.document

markdown = doc.export_to_markdown()
Path("docs/DB-SUA.md").write_text(markdown, encoding="utf-8")

print(f"{len(markdown)} caracteres")
doc.save_as_json("docs/DB-SUA.json")
print(markdown[:1000])





embedder = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

pregunta = ["¿A qué altura tiene que estar la barandilla de un balcón?"]
textos = [
    "Las barreras de protección tendrán, como mínimo, una altura de 0,90 m cuando la diferencia de cota que protegen no exceda de 6 m.",
    "El pasamanos estará a una altura comprendida entre 90 y 110 cm.",
    "La instalación de alumbrado de emergencia funcionará durante una hora, como mínimo.",
]

q = embedder.encode_query(pregunta)
d = embedder.encode_document(textos)

print("Forma de los vectores:", q.shape, d.shape)
print("Similitud:", embedder.similarity(q, d))

def fragmentar_por_caracteres(texto, tamano=800, solapamiento=100):
    fragmentos = []
    inicio = 0
    while inicio < len(texto):
        fragmentos.append(texto[inicio:inicio + tamano])
        inicio += tamano - solapamiento
    return fragmentos

fijos = fragmentar_por_caracteres(markdown)
print(f"{len(fijos)} fragmentos")
print(fijos[20])



tokenizer = HuggingFaceTokenizer.from_pretrained(
    model_name="Qwen/Qwen3-Embedding-0.6B",
    max_tokens=256
)
chunker = HybridChunker(tokenizer=tokenizer)
chunks = list(chunker.chunk(dl_doc=doc))

print(f"{len(chunks)} fragmentos")

fragmentos = []
for i, chunk in enumerate(chunks):
    fragmentos.append({
        "id": f"sua-{i}",
        "texto": chunker.contextualize(chunk=chunk),
        "apartado": " > ".join(chunk.meta.headings or []),
        "pagina": chunk.meta.doc_items[0].prov[0].page_no,
    })

print(fragmentos[67])

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="db_sua",
    configuration={"hnsw": {"space": "cosine"}}
)

textos = [f["texto"] for f in fragmentos]
embeddings = embedder.encode_document(textos, batch_size=16, show_progress_bar=True)

collection.upsert(
    ids=[f["id"] for f in fragmentos],
    documents=textos,
    embeddings=embeddings.tolist(),
    metadatas=[{"apartado": f["apartado"], "pagina": f["pagina"]} for f in fragmentos],
)

print(f"{collection.count()} fragmentos en la colección")

def busqueda_vectorial(pregunta, n=3):
    q = embedder.encode_query([pregunta])
    r = collection.query(
        query_embeddings=q.tolist(),
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )
    resultados = []
    for id_, texto, meta, dist in zip(r["ids"][0], r["documents"][0], r["metadatas"][0], r["distances"][0]):
        resultados.append({"id": id_, "texto": texto, "similitud": 1 - dist, **meta})
    return resultados

for r in busqueda_vectorial("¿Hace falta poner pararrayos en un edificio?"):
    print(f"[{r['similitud']:.2f}] {r['apartado']} (pág. {r['pagina']})")
    print("   ", r["texto"][:150].replace("\n", " "), "...")


q = embedder.encode_query(["altura del pasamanos"])
r = collection.query(
    query_embeddings=q.tolist(),
    n_results=3,
    where={"pagina": {"$lte": 20}},
)
for meta in r["metadatas"][0]:
    print(meta)

for r in busqueda_vectorial("¿Qué dice el apartado 4.3.4?"):
    print(f"[{r['similitud']:.2f}] {r['apartado']} (pág. {r['pagina']})")


def palabras(texto):
    return re.findall(r"\d+(?:[.,]\d+)+|\w+", texto.lower())

print(palabras("Según el apartado 4.3.4, la altura será de 0,90 m"))

bm25 = BM25Okapi([palabras(f["texto"]) for f in fragmentos])

def busqueda_palabras(pregunta, n=3):
    puntuaciones = bm25.get_scores(palabras(pregunta))
    mejores = sorted(range(len(fragmentos)), key=lambda i: puntuaciones[i], reverse=True)[:n]
    return [fragmentos[i] for i in mejores]

for f in busqueda_palabras("¿Qué dice el apartado 4.3.4?"):
    print(f"{f['apartado']} (pág. {f['pagina']})")

def busqueda_hibrida(pregunta, n=2):
    resultados = []
    vistos = set()
    for f in busqueda_vectorial(pregunta, n) + busqueda_palabras(pregunta, n):
        if f["id"] not in vistos:
            vistos.add(f["id"])
            resultados.append(f)
    return resultados

for pregunta in ["¿Qué dice el apartado 4.3.4?", "¿Hace falta poner pararrayos en un edificio?"]:
    print(pregunta)
    for f in busqueda_hibrida(pregunta):
        print(f"   {f['apartado']} (pág. {f['pagina']})")