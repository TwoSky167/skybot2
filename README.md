# 뉴스 요약 챗봇

키워드를 입력하면 **구글 뉴스에서 관련 뉴스 10개**를 찾아 제목·날짜·링크·요약을 보여 주는 챗봇입니다.

---

## HTML 버전 (Python 없이 사용)

**설치 없이** 브라우저만 있으면 됩니다.

1. 폴더에서 **`index.html`** 파일을 더블클릭해서 브라우저로 엽니다.
2. 검색창에 키워드(예: 인공지능, 삼성전자)를 입력하고 **검색** 버튼을 누릅니다.
3. 관련 뉴스 10개가 제목, 날짜, 링크, 요약과 함께 표시됩니다.

> **참고:** 뉴스 데이터는 Google News RSS를 사용하며, 브라우저에서 CORS 제한을 피하기 위해 공개 프록시(AllOrigins)를 거칩니다. 인터넷 연결이 필요합니다.

---

## Python 버전 (선택)

Python이 설치되어 있다면 콘솔에서도 사용할 수 있습니다.

### 준비물

- Python 3.9 이상
- `pip` 또는 `python -m pip` 사용 가능

### 설치 및 실행

```bash
cd "c:\Users\aaaa\Desktop\챗봇"
python -m pip install -r requirements.txt
python news_chatbot.py
```

콘솔에 키워드를 입력하면 같은 방식으로 뉴스 10개가 출력됩니다. 종료하려면 `exit`, `quit`, `종료`, `끝` 중 하나를 입력하세요.

---

## 동작 방식

- **Google News RSS** 주소로 키워드 검색을 요청합니다.
- HTML 버전: 브라우저에서 RSS를 가져와 XML로 파싱한 뒤, 상위 10개 기사의 제목·링크·발행일·요약(description)을 보여 줍니다.
- Python 버전: `requests` + `feedparser`로 RSS를 받아 파싱한 뒤 동일하게 10개를 출력합니다.

---

## Vercel 배포

1. [Vercel](https://vercel.com)에 로그인 후 **Add New → Project**에서 이 저장소(또는 폴더)를 연결합니다.
2. **Project Name**을 **영문 소문자, 숫자, 하이픈(-), 밑줄(_)만** 사용해 지정합니다.  
   예: `news-chatbot` 또는 `news_chatbot`  
   한글(챗봇)이나 그 밖의 특수문자는 사용하지 마세요.  
   → "The name contains invalid characters" 오류는 보통 프로젝트 이름에 한글/특수문자가 들어갈 때 발생합니다.
3. **Environment Variables** 설정  
   - **Settings → Environment Variables**에서 변수 추가  
   - **Name:** `GeminiAPIKey1`  
   - **Value:** 본인의 Gemini API 키  
   - 이렇게 하면 배포된 사이트에서는 API 키 입력 없이 AI 요약/대화를 사용할 수 있습니다.
4. **Deploy**를 누르면 정적 사이트 + 서버리스 API(`/api/gemini`)가 함께 배포됩니다.  
   `vercel.json`에 `"name": "news-chatbot"`이 들어 있어, 프로젝트 이름을 지정해 두었습니다.

---

## 확장 아이디어

- 키워드 자동 추천
- 여러 키워드 한 번에 비교
- 뉴스 감성 분석(긍정/부정)
