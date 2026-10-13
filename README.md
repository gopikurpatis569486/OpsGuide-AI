# OpsGuide AI - Source-Grounded Incident Assistant

An independent portfolio prototype aligned with AI application engineering, cloud diagnostics, API integration, and response validation. Built with Python's standard library and a browser UI. No package installation, paid service, API key, or network access is needed.

## Run (Python 3.10+)

Extract this folder, open a terminal inside it, and run:

```sh
python app.py
```

On Windows use `py app.py` if `python` is unavailable. Open http://127.0.0.1:8001. Stop with Ctrl+C. Choose a different port with `python app.py --port 8011`.

## Implemented

- 10 synthetic runbooks across Linux, IAM, Kubernetes, API, networking, power, cooling, and asset retirement.
- TF-IDF vectors with cosine similarity and ranked source identifiers.
- Source-grounded extractive response from the strongest matching runbook.
- Evidence threshold that declines weak or unknown questions.
- JSON API, responsive UI, and 20-query retrieval evaluation.

This is the retrieval and grounding stage of a RAG-style workflow. It does **not** implement generative LLM inference, semantic embeddings, agentic actions, AWS deployment, or authentication. The UI says extractive mode. Scores are similarities, not probabilities. Broad mixed-topic questions can retrieve an incomplete source.

## Architecture

Browser -> local HTTP JSON API -> query tokenization -> TF-IDF cosine ranking -> evidence threshold -> quoted runbook + source metadata. Data comes from `data/runbooks.json`; `engine.py` contains the scoring and response rules. No user query is persisted.

## Verify

```sh
python -m unittest -v
python evaluate.py
```

Evaluation cases are synthetic and derived from the same corpus, so the result is a demo regression metric, not independent accuracy on production incidents. Read `evaluation_results.json` for measured results. Add held-out paraphrases and unknown topics before making broader claims.

## API

- GET `/api/runbooks`: corpus.
- GET `/api/evaluation`: per-query results and top-1/recall@3.
- POST `/api/ask` with `{"question":"IAM access denied permission"}`.

## 60-second demo

1. Show the Kubernetes sample and open its evidence trail.
2. Click IAM denied and explain the source identifier and similarity score.
3. Enter `astronomy nebula telescope` to show refusal when evidence is absent.
4. Run evaluation and explain the synthetic test-set limitation.

## Next steps (not implemented)

Add independently authored test queries, approved private-document ingestion, embeddings, an optional LLM synthesis layer with citation validation, role-based access, and deployment. Keep secrets and employer documents out of the public repo.

## LinkedIn

Use `LINKEDIN_POST.txt` after running the demo and understanding the implementation. Upload the companion showcase PDF or dashboard screenshot; add your own repository link after publishing the files to GitHub. No public repository or hosted deployment is included.
