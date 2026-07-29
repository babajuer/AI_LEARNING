# MODEL="gemma4:latest"   #回复有问题
# MODEL="llama3.2:latest"
MODEL="qwen2.5:3b"

# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 5 個 iteration、每一輪 prompt 都比前一輪更具體
PROMPTS = {
    "v1 模糊": "寫一段介紹 ReAct 的文字。",
    "v2 加目標讀者": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。",
    "v3 加格式": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落。",
    "v4 加 example 要求": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落、結尾舉一個具體例子（譬如查天氣）。",
    "v5 加禁忌": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落、結尾舉一個具體例子（譬如查天氣）。不要用「賦能」「驅動」「智能」這類空泛詞彙。",
}

outputs = {}
for label, prompt in PROMPTS.items():
    r = client.chat.completions.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = r.choices[0].message.content
    outputs[label] = text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === 自我驗證 ===
v1_len, v5_len = len(outputs["v1 模糊"]), len(outputs["v5 加禁忌"])
banned_words = ("賦能", "驅動", "智能")
v5_has_banned = any(w in outputs["v5 加禁忌"] for w in banned_words)
assert v5_len > 0, "v5 必須有輸出"
assert not v5_has_banned, f"v5 應該避免禁忌詞、實際含: {[w for w in banned_words if w in outputs['v5 加禁忌']]}"
print(f"\n✅ 練習 4 通過 — v5 長度 {v5_len}、無禁忌詞（本機 $0）")
print(f"💡 觀察：v1 ({v1_len} chars) 通常比 v5 ({v5_len} chars) 「鬆」、加約束會逼 prompt 收斂")
print("💡 用 gemma4:e4b 跑這題特別有感——小 model 對 prompt 質量極敏感、5 輪 refine 的差距會比 Claude 更明顯")