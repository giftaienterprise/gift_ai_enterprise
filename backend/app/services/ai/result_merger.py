class ResultMerger:
    """
    AI 结果合并器（企业级核心组件）
    """

    def merge(self, quick: dict, desc: dict, image: dict | None) -> dict:
        """
        合并多个 AI 结果为统一结构
        """

        return {
            "title": quick.get("title"),
            "tags": quick.get("tags", []),

            "description": desc.get("description"),
            "selling_points": desc.get("selling_points", []),

            "image": image,
        }


result_merger = ResultMerger()