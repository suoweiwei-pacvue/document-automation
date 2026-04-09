"""Embedding model configuration using LiteLLM for gateway compatibility."""

import logging
from typing import Optional

import numpy as np
from langchain_core.embeddings import Embeddings

from src.config import Settings

logger = logging.getLogger(__name__)


class GatewayEmbeddings(Embeddings):
    """LiteLLM-compatible embeddings that work with Pacvue LLM Gateway."""

    def __init__(self, model: str, api_key: str, api_base: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        import litellm
        results = []
        batch_size = 20  # 批量大小设置为20，提高请求效率
        for i in range(0, len(texts), batch_size):
            batch = texts[i: i + batch_size]
            # LLM接口通常有单条文本长度限制，这里做截断
            batch = [t[:8000] if len(t) > 8000 else t for t in batch]
            response = litellm.embedding(
                model=self.model,        # 使用实例指定的embedding模型
                input=batch,             # 当前批次文本
                api_key=self.api_key,    # LLM网关的api key
                api_base=self.api_base,  # 可选网关base
            )
            # response.data是一个包含每个文本embedding的列表
            for item in response.data:
                results.append(item["embedding"])
        return results

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


def get_embeddings(settings: Settings) -> Embeddings:
    return GatewayEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
        api_base=settings.openai_api_base or None,
    )
