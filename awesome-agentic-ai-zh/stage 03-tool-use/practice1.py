# MODEL="gemma4:latest"   #回复有问题
# MODEL="llama3.2:latest"
MODEL="qwen2.5:3b"


# 需要：pip install openai
# 前置：ollama pull qwen2.5:3b && ollama serve
# Note: Stage 3+ 用 qwen2.5:3b（tool-use 穩定）、不是 gemma4:e4b
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Step 1: 定義 tool schema — OpenAI-compatible 格式包一層 {"type":"function", "function":{...}}
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查詢城市目前天氣（晴/雨/陰），回傳一個短字串。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名稱（如「台北」）"},
            },
            "required": ["city"],
        },
    },
}

# Step 2: 問問題、讓 LLM 自己決定要不要呼叫 tool
resp = client.chat.completions.create(
    model=MODEL,
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北現在有下雨嗎？"}],
)

# === 自我驗證 ===
msg = resp.choices[0].message
print("finish_reason:", resp.choices[0].finish_reason)
print("tool_calls:", msg.tool_calls)

assert msg.tool_calls, "預期 LLM 會選擇呼叫 tool（而非直接回答）"
tc = msg.tool_calls[0]
assert tc.function.name == "get_weather", f"預期呼叫 get_weather、實際 {tc.function.name}"
args = json.loads(tc.function.arguments)
assert args.get("city"), "預期 city 參數有值"
print(f"✅ 練習 1 通過 — qwen2.5:3b 正確選了 get_weather、帶 city='{args['city']}' 參數")