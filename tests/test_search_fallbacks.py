import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib import env, xiaohongshu, zhihu


BING_XHS_HTML = """
<html><body>
<li class="b_algo">
  <h2><a href="https://www.xiaohongshu.com/explore/abc123">小红书 AI 工具测评</a></h2>
  <p>这是一条来自小红书的公开搜索摘要。</p>
</li>
</body></html>
"""


BING_ZHIHU_HTML = """
<html><body>
<li class="b_algo">
  <h2><a href="https://www.zhihu.com/question/123456">知乎 AI 工具讨论</a></h2>
  <p>这是一条来自知乎的公开搜索摘要。</p>
</li>
</body></html>
"""


def test_xiaohongshu_site_search_fallback_parses_bing_html():
    with patch.object(xiaohongshu, "_fetch_html", return_value=BING_XHS_HTML):
        items = xiaohongshu._search_via_site_search("AI 工具", 5)

    assert len(items) == 1
    assert items[0]["title"] == "小红书 AI 工具测评"
    assert items[0]["source"] == "site-search-fallback"
    assert items[0]["url"].endswith("/abc123")


def test_zhihu_site_search_fallback_parses_bing_html():
    with patch.object(zhihu, "_fetch_html", return_value=BING_ZHIHU_HTML):
        items = zhihu._search_via_site_search("AI 工具", 5)

    assert len(items) == 1
    assert items[0]["title"] == "知乎 AI 工具讨论"
    assert items[0]["source"] == "site-search-fallback"
    assert items[0]["content_type"] == "question"


def test_xiaohongshu_diagnose_available_with_fallback_when_mcp_down():
    with patch("lib.http.get", side_effect=RuntimeError("mcp down")):
        with patch("lib.crawler_bridge.is_playwright_available", return_value=False):
            assert env.is_xiaohongshu_available({}) is True
