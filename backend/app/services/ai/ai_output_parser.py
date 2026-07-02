import json
import re
from typing import Any


class AIOutputParser:
    """
    企业级 AI 输出解析器（防崩溃核心组件）
    """

    def parse(self, text: str) -> dict[str, Any]:
        """
        安全解析 AI 输出
        """

        if not text:
            return {}

        # =========================
        # Step 1：直接 JSON 解析
        # =========================
        try:
            return json.loads(text)
        except Exception:
            pass

        # =========================
        # Step 2：提取 JSON 区块
        # =========================
        try:
            match = re.search(r"\{.*\}", text, re.S)
            if match:
                return json.loads(match.group())
        except Exception:
            pass

        # =========================
        # Step 3：数组格式兜底
        # =========================
        try:
            match = re.search(r"\[.*\]", text, re.S)
            if match:
                return {"result": json.loads(match.group())}
        except Exception:
            pass

        # =========================
        # Step 4：最终兜底
        # =========================
        return {
            "title": "解析失败",
            "subtitle": "",
            "description": text[:300],
            "selling_points": []
        }


ai_output_parser = AIOutputParser()