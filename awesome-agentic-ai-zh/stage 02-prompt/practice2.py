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

# 中文情緒分類（正面 / 負面 / 中立）
TEST_SET = [
    ("這部電影超讚、看完想再看一次！", "正面"),
    ("劇情無聊、演員演技尷尬。", "負面"),
    ("這是一部 2019 年的電影。", "中立"),
    ("我不確定喜不喜歡、可能再想想。", "中立"),
    ("第一集很不錯但第二集就崩了。", "負面"),
    ("看完心情很好、推薦！", "正面"),
]

FEW_SHOT_EXAMPLES = """
範例：
input: 這家餐廳的牛排好吃到讓我哭出來。
output: 正面

input: 服務生態度很差、我再也不會來了。
output: 負面

input: 這家店位於新北市三重區。
output: 中立
"""

# 兩種條件共用同一段「任務說明」；few-shot 只多加範例——這樣對比才乾淨，量到的是「範例」本身的效果，而不是「終於告訴模型要做什麼」。
TASK = "把下面的句子分類成「正面 / 負面 / 中立」其中一個，只輸出這三個詞其中之一、不要多餘文字。\n\n"


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    r = client.chat.completions.create(
        model=MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip().splitlines()[0]


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f" {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正確 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正確 {c3}/{n} = {c3/n:.0%}")

# === 自我驗證 ===
# 兩種條件都給了同樣的任務說明，所以這裡量的是「範例本身」帶來的差異。
# few-shot 不保證每次都贏（看 model / 題目 / 抽樣），所以不硬性要求 c3 >= c0。
assert n == 6 and 0 <= c0 <= n and 0 <= c3 <= n, "兩種條件都要各跑完 6 題"
print(f"\n✅ 練習 2 通過 — 0-shot {c0}/{n}、3-shot {c3}/{n}；few-shot 淨提升 {c3 - c0} 題（可能為 0 甚至負，都算正常）（本機 $0）")
print("💡 觀察：有了任務說明，0-shot 就有基本盤；few-shot 的價值在「釘住輸出格式」+ 示範模稜兩可案例（如 '中立'）的判準")
print("💡 小 model（gemma4:e4b）對格式更敏感，所以 few-shot 的幫助通常比 Claude 明顯——但仍非保證，要跑了才知道")