import json
import logging
import re
import uuid

from app.core.config import settings
from app.schemas.advisor import RecommendRequest, RecommendResponse, RecommendedGift
from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ecommerce.link_builder import build_purchase_url, default_platform_links


logger = logging.getLogger(__name__)

FALLBACK_GIFTS = [
    {
        "name": "定制名字项链",
        "price_yuan": 358,
        "emoji": "📿",
        "reason": "把 TA 的名字戴在离心最近的地方",
        "match": "96% 专属感强",
        "meaning": "专属感是最好的礼物",
        "tip": "支持中文/英文刻字",
        "tags": ["定制", "饰品"],
    },
    {
        "name": "香薰蜡烛礼盒",
        "price_yuan": 268,
        "emoji": "🕯️",
        "reason": "营造温暖、放松的氛围",
        "match": "88% 适合大多数场合",
        "meaning": "气息是记忆的锚点",
        "tip": "可选无烟大豆蜡材质",
        "tags": ["浪漫", "家居"],
    },
    {
        "name": "蓝牙音箱",
        "price_yuan": 399,
        "emoji": "🎵",
        "reason": "用音乐陪伴日常",
        "match": "92% 实用又体面",
        "meaning": "音乐是记忆的载体",
        "tip": "支持蓝牙 5.0",
        "tags": ["音乐", "实用"],
    },
]


class GiftRecommendationService:
    def recommend(self, data: RecommendRequest) -> RecommendResponse:
        platform = data.platform if data.platform in {"taobao", "jd"} else "taobao"

        if not settings.DEEPSEEK_API_KEY:
            gifts = self._build_gifts(FALLBACK_GIFTS, platform)
            return RecommendResponse(
                success=True,
                combo_title="精选礼物方案",
                relation=data.relation,
                scene=data.scene,
                budget=data.budget,
                gifts=gifts,
                source="fallback",
                error="DEEPSEEK_API_KEY is not configured",
            )

        prompt = f"""
请为以下送礼需求推荐 3 个具体可购买的礼物，只输出 JSON，不要 markdown：

送礼对象：{data.relation}
场合：{data.scene}
预算：{data.budget}
补充信息：{data.note or "无"}

输出格式：
{{
  "combo_title": "方案标题",
  "gifts": [
    {{
      "name": "商品名称",
      "price_yuan": 299,
      "emoji": "🎁",
      "reason": "一句话推荐理由",
      "match": "95% 符合需求",
      "meaning": "送礼寓意",
      "tip": "购买小贴士",
      "tags": ["标签1", "标签2"]
    }}
  ]
}}
"""

        try:
            content = deepseek_ai_service.chat(
                prompt=prompt,
                system_prompt=(
                    "你是专业送礼顾问。推荐真实可在中国电商平台搜索购买的礼物，"
                    "名称要具体，价格单位为元，必须返回合法 JSON。"
                ),
            )
            payload = self._parse_json(content)
            raw_gifts = payload.get("gifts") or FALLBACK_GIFTS
            gifts = self._build_gifts(raw_gifts[:3], platform)
            return RecommendResponse(
                success=True,
                combo_title=str(payload.get("combo_title") or "AI 推荐方案"),
                relation=data.relation,
                scene=data.scene,
                budget=data.budget,
                gifts=gifts,
                source="deepseek",
            )
        except Exception as exc:
            logger.exception("Gift recommendation failed")
            gifts = self._build_gifts(FALLBACK_GIFTS, platform)
            return RecommendResponse(
                success=True,
                combo_title="精选礼物方案",
                relation=data.relation,
                scene=data.scene,
                budget=data.budget,
                gifts=gifts,
                source="fallback",
                error=str(exc),
            )

    def _build_gifts(self, raw_gifts: list, platform: str) -> list[RecommendedGift]:
        items: list[RecommendedGift] = []
        for index, raw in enumerate(raw_gifts):
            name = str(raw.get("name") or f"推荐礼物{index + 1}").strip()
            price_yuan = raw.get("price_yuan", raw.get("price", 0))
            try:
                price = int(float(price_yuan) * 100)
            except (TypeError, ValueError):
                price = 0
            links = default_platform_links(name)
            items.append(
                RecommendedGift(
                    id=str(raw.get("id") or uuid.uuid4().hex[:8]),
                    name=name,
                    price=price,
                    emoji=str(raw.get("emoji") or "🎁"),
                    reason=str(raw.get("reason") or ""),
                    match=str(raw.get("match") or ""),
                    meaning=str(raw.get("meaning") or ""),
                    tip=str(raw.get("tip") or ""),
                    tags=list(raw.get("tags") or []),
                    purchase_url=links.get(platform, build_purchase_url(name, platform)),
                    platform=platform,
                    platform_links=links,
                )
            )
        return items

    def _parse_json(self, content: str) -> dict:
        text = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
        if fenced:
            text = fenced.group(1).strip()
        return json.loads(text)


gift_recommendation_service = GiftRecommendationService()
