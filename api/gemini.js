const GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent";

module.exports = async function handler(req, res) {
  // CORS: Vercel에 배포된 프론트와 같은 도메인에서 오면 동일 출처이지만, 다른 도메인에서 호출할 수 있도록 허용
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const apiKey = process.env.GeminiAPIKey1;
  if (!apiKey) {
    return res.status(500).json({
      error: "Gemini API 키가 설정되지 않았습니다. Vercel 대시보드 → Settings → Environment Variables에서 GeminiAPIKey1을 설정하세요.",
    });
  }

  let body;
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  } catch (e) {
    return res.status(400).json({ error: "Invalid JSON body" });
  }

  const { prompt, extraSystemText } = body;
  if (!prompt) {
    return res.status(400).json({ error: "prompt is required" });
  }

  const systemText =
    "당신은 한국어로 답변하는 뉴스 요약/설명 도우미입니다. 주어진 기사 정보만 기반으로 답하고, 모르는 내용은 모른다고 말하세요." +
    (extraSystemText ? "\n\n추가 지시: " + extraSystemText : "");

  const geminiBody = {
    contents: [{ parts: [{ text: prompt }] }],
    systemInstruction: { parts: [{ text: systemText }] },
  };

  try {
    const geminiRes = await fetch(
      `${GEMINI_API_URL}?key=${encodeURIComponent(apiKey)}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(geminiBody),
      }
    );

    const data = await geminiRes.json();

    if (!geminiRes.ok) {
      const msg = data.error?.message || JSON.stringify(data.error) || String(geminiRes.status);
      return res.status(geminiRes.status).json({
        error: `Gemini API 오류 (상태: ${geminiRes.status}): ${msg}`,
      });
    }

    if (data.error) {
      return res.status(500).json({
        error: "Gemini API 오류: " + (data.error.message || JSON.stringify(data.error)),
      });
    }

    const text =
      data.candidates?.[0]?.content?.parts?.[0]?.text ?? "";

    return res.status(200).json({ text });
  } catch (err) {
    console.error("Gemini API proxy error:", err);
    return res.status(500).json({
      error: "서버 오류: " + (err.message || "Unknown error"),
    });
  }
}
