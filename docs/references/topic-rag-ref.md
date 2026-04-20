# Reference: RAG Beginner Guide

**Source:** https://dev.to/egepakten/what-is-rag-a-beginners-guide-to-retrieval-augmented-generation-with-a-full-pipeline-walkthrough-3djm

**Title:** What is RAG? A Beginner's Guide to Retrieval-Augmented Generation (With a Full Pipeline Walkthrough)

**Key Points:**
- RAG combines a parametric memory (LLM weights) with a non‑parametric memory (searchable document store) to improve factuality.
- Core pipeline: Load documents → Chunk → Embed → Store in vector DB → Retrieve relevant chunks → Generate answer with LLM.
- Embedding models (e.g., BGE, text‑embedding‑ada‑2) turn text chunks into vectors.
- Vector databases such as Chroma or Pinecone enable efficient similarity search.
- Hybrid search (vector + BM25) can boost accuracy.
- Motivations include LLM stale knowledge, hallucinations, and the need for up‑to‑date domain‑specific info.
- Practical tips: choose appropriate chunk size, batch embeddings, and tune index parameters (IVF‑PQ).