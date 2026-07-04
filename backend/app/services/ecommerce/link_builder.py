from urllib.parse import quote


def build_purchase_url(name: str, platform: str = "taobao") -> str:
    keyword = quote(name.strip())
    if platform == "jd":
        return f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8"
    return f"https://s.taobao.com/search?q={keyword}"


def default_platform_links(name: str) -> dict[str, str]:
    return {
        "taobao": build_purchase_url(name, "taobao"),
        "jd": build_purchase_url(name, "jd"),
    }
