import urllib.parse

import feedparser
import requests


GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search"


def build_google_news_rss_url(query: str, lang: str = "ko", region: str = "KR") -> str:
    """
    구글 뉴스 RSS 검색 URL 생성.

    :param query: 검색 키워드
    :param lang: 언어 코드 (예: 'ko')
    :param region: 지역 코드 (예: 'KR')
    """
    params = {
        "q": query,
        "hl": f"{region.lower()}-{lang}",  # 예: 'kr-ko'
        "gl": region,
        "ceid": f"{region}:{lang}",
    }
    return f"{GOOGLE_NEWS_RSS_URL}?{urllib.parse.urlencode(params)}"


def fetch_news_feed(query: str, max_results: int = 10):
    """
    구글 뉴스에서 RSS 피드를 가져와 파싱한다.

    :param query: 검색 키워드
    :param max_results: 가져올 뉴스 개수
    :return: 기사 정보 딕셔너리 리스트
    """
    url = build_google_news_rss_url(query)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[에러] 뉴스 요청 중 문제가 발생했습니다: {e}")
        return []

    feed = feedparser.parse(response.content)

    articles = []
    for entry in feed.entries[:max_results]:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = entry.get("summary", "").strip()
        published = getattr(entry, "published", "").strip()

        articles.append(
            {
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
            }
        )

    return articles


def summarize_article_text(text: str, max_sentences: int = 2) -> str:
    """
    아주 단순한 요약: 문장 단위로 잘라 앞부분만 보여준다.
    (추후에 실제 요약 모델/오픈 API를 붙일 수 있도록 구조만 분리)
    """
    # 뉴스 RSS 요약은 HTML 태그가 포함될 수 있어 간단히 제거
    import re

    cleaned = re.sub(r"<.*?>", " ", text)
    cleaned = " ".join(cleaned.split())

    # 마침표 기준으로 문장 분리 (아주 러프함)
    sentences = [s.strip() for s in re.split(r"[.!?。？！]", cleaned) if s.strip()]

    if not sentences:
        return cleaned

    return " ".join(sentences[:max_sentences])


def show_articles_with_summary(articles):
    if not articles:
        print("관련 뉴스를 찾지 못했어요. 키워드를 바꿔서 다시 시도해 주세요.")
        return

    print()
    print("=" * 80)
    print(f"총 {len(articles)}개의 뉴스를 찾았어요.")
    print("=" * 80)

    for idx, article in enumerate(articles, start=1):
        print(f"\n[{idx}] {article['title']}")
        if article.get("published"):
            print(f"    - 날짜: {article['published']}")
        print(f"    - 링크: {article['link']}")

        summary = summarize_article_text(article.get("summary", "") or article["title"])
        print(f"    - 요약: {summary}")


def chat_loop():
    print("뉴스 요약 챗봇입니다.")
    print("키워드를 입력하면 관련된 최신 뉴스 10개를 구글 뉴스에서 찾아 요약해 드려요.")
    print("종료하려면 'exit', 'quit', '종료' 중 하나를 입력하세요.\n")

    while True:
        query = input("검색할 키워드를 입력하세요: ").strip()
        if not query:
            continue

        if query.lower() in {"exit", "quit"} or query in {"종료", "끝"}:
            print("챗봇을 종료합니다. 이용해 주셔서 감사합니다.")
            break

        print(f"\n'{query}' 관련 뉴스를 검색 중입니다. 잠시만 기다려 주세요...\n")
        articles = fetch_news_feed(query, max_results=10)
        show_articles_with_summary(articles)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    chat_loop()

