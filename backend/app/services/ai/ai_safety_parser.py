import json
from typing import Any


class AISafetyParser:
    """
    AI输出安全解析器（企业级核心组件）
    """

    def parse_json(self, text: str) -> dict[str, Any]:
        """
        将 AI 输出安全解析为 JSON
        """

        if not text:
            return {}

        try:
            # 1. 直接解析
            return json.loads(text)
        except Exception:
            pass

        try:
            # 2. 提取 JSON 区块
            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                json_str = text[start:end + 1]
                return json.loads(json_str)

        except Exception:
            pass

        # 3. 兜底
        return {
            "title": "解析失败",
            "subtitle": "",
            "description": text[:200],
            "selling_points": []
        }


ai_safety_parser = AISafetyParser()