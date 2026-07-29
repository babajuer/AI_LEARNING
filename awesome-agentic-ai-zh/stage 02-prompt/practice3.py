# MODEL="gemma4:latest"   #回复有问题
# MODEL="llama3.2:latest"
MODEL="qwen2.5:3b"


# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

QUESTION = "小明有 3 顆蘋果。他給了小華 1 顆、又從媽媽那邊拿到 5 顆、然後吃了 2 顆。請問現在剩幾顆？"
ANSWER = 5 # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """範例：
Q: 一隻雞有 2 隻腳。3 隻雞跟 1 個人共有幾隻腳？
A: 讓我一步一步算。3 隻雞 × 2 隻腳 = 6 隻腳。1 個人有 2 隻腳。總共 6 + 2 = 8 隻腳。答案是 8。
"""


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def extract_number(text: str) -> int | None:
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


# A. 純 prompt
out_a = ask(QUESTION); ans_a = extract_number(out_a)

# B. + Let's think step by step
out_b = ask(QUESTION + "\nLet's think step by step."); ans_b = extract_number(out_b)

# C. + CoT example
out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:"); ans_c = extract_number(out_c)

for label, out, ans in [("A 純 prompt", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] 答案={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === 自我驗證 ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
assert correct >= 1, f"3 種 prompt 至少要 1 種答對、實際 {correct}/3"
# 小 model 對 CoT 依賴性更高、放寬條件：B 或 C 至少 1 對（vs Anthropic Path B 要求嚴格）
assert ans_b == ANSWER or ans_c == ANSWER, "B (step-by-step) 或 C (CoT example) 至少一種要答對 — CoT 對小 model 是基本功"
print(f"\n✅ 練習 3 通過 — {correct}/3 答對（本機 $0）")
print(f"💡 觀察小 model：A 純 prompt 通常答錯、B/C 加 CoT 後明顯改善——比 Claude 更能凸顯 CoT 重要性")