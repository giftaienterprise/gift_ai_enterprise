import hashlib
import json
from typing import Any


class CacheKeyBuilder:
    """
    企业级 Cache Key Builder
    """

    CACHE_PREFIX = "gift_ai"

    def build(
        self,
        namespace: str,
        task_type: str,
        prompt_version: str,
        model_version: str,
        payload: dict[str, Any],
    ) -> str:
        payload_json = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

        payload_hash = hashlib.sha256(
            payload_json.encode("utf-8")
        ).hexdigest()

        return (
            f"{self.CACHE_PREFIX}:"
            f"{namespace}:"
            f"{task_type}:"
            f"{prompt_version}:"
            f"{model_version}:"
            f"{payload_hash}"
        )


cache_key_builder = CacheKeyBuilder()