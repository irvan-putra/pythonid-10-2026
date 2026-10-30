FitRAG: RAG that learns from feedback
=====================================

Problem: RAG grounds an LLM in external knowledge, but once
deployed it is static and cannot learn from user feedback.
Small models in resource-constrained settings need to keep adapting.

The "implicit behavioral layer" (adapter weights, retrieval indices,
prompt templates) has no lifecycle management. FitRAG adds one:
- feedback -> training data, via counterfactual training signals
- parameter-efficient adaptation, via LoRA fine-tuning
- zero-downtime deployment, via hot-swappable adapters

On a 20-query quantum-computing QA benchmark (5 ablation studies):
- RAG retrieval: 15.7% shorter responses
- LoRA fine-tuning: 11.0% longer, domain-specific outputs
- feedback loop: 18.1% more concise responses
- full pipeline: ROUGE-1 0.171, LLM-as-judge score 0.80
