"""
Turkish Sentiment Analyzer
---------------------------
A lexicon-based sentiment analysis tool for Turkish text.
Classifies input as Positive, Negative, or Neutral and explains the result.

Motivation: Most NLP sentiment tools are built for English. As a native Turkish
speaker working in NLP and translation, I built this to process Turkish medical,
legal and general-domain texts — a gap that matters in real localization work.

Author : Talha Umut Kulu
GitHub : https://github.com/tumut-k
"""

# ── Lexicons ──────────────────────────────────────────────────────────────────
# Hand-curated seed lists. A production version would use a full lexicon such as
# SentiTurkNet, but this illustrates the core pipeline clearly.

POSITIVE_WORDS = {
    # General positive
    "iyi", "güzel", "harika", "mükemmel", "başarılı", "mutlu", "olumlu",
    "doğru", "faydalı", "etkili", "verimli", "sağlıklı", "kolay", "hızlı",
    "temiz", "güvenli", "güvenilir", "kaliteli", "değerli", "önemli",
    "gelişmiş", "modern", "uygun", "rahat", "net", "açık", "başarı",
    # Medical / clinical positive
    "iyileşme", "iyileşti", "düzeldi", "stabil", "normal", "negatif",
    "remisyon", "taburcu", "ağrısız",
    # Legal / formal positive
    "onaylandı", "kabul", "geçerli", "yetkilendirildi", "hak",
}

NEGATIVE_WORDS = {
    # General negative
    "kötü", "berbat", "hatalı", "yanlış", "zararlı", "tehlikeli", "zor",
    "yavaş", "kirli", "riskli", "güvensiz", "kalitesiz", "değersiz",
    "ciddi", "ağır", "acı", "üzücü", "endişe", "sorun", "problem",
    "yetersiz", "eksik", "başarısız", "olumsuz", "rahatsız", "gergin",
    # Medical / clinical negative
    "ağrı", "şikayet", "semptom", "komplikasyon", "enfeksiyon", "kronik",
    "akut", "kötüleşti", "kötüleşme", "pozitif", "anormal", "acil",
    "yoğun", "kritik", "ameliyat", "kanama", "ateş", "bulantı",
    # Legal / formal negative
    "red", "reddedildi", "ihlal", "suç", "ceza", "dava", "kaçak",
}

# Negation words that flip the sentiment of the following word
NEGATION_WORDS = {"değil", "yok", "olmaz", "olmadı", "hayır", "hiç", "asla"}

# Intensifiers that strengthen the next word's sentiment score
INTENSIFIERS = {"çok", "son derece", "oldukça", "fazla", "aşırı", "tam"}


# ── Core analysis ─────────────────────────────────────────────────────────────

def analyze(text: str) -> dict:
    """
    Analyze the sentiment of a Turkish text string.

    Returns a dict with:
        label       : 'Positive', 'Negative', or 'Neutral'
        score       : net sentiment score (positive − negative word count)
        positive_hits : list of positive words found
        negative_hits : list of negative words found
        negated_hits  : list of words whose sentiment was flipped by negation
        explanation : human-readable summary
    """
    tokens = text.lower().split()

    positive_hits = []
    negative_hits = []
    negated_hits  = []
    score = 0

    for i, token in enumerate(tokens):
        # Check if the previous token is a negation word
        negated = (i > 0 and tokens[i - 1] in NEGATION_WORDS)

        if token in POSITIVE_WORDS:
            if negated:
                negative_hits.append(token)
                negated_hits.append(token)
                score -= 1
            else:
                positive_hits.append(token)
                score += 1

        elif token in NEGATIVE_WORDS:
            if negated:
                positive_hits.append(token)
                negated_hits.append(token)
                score += 1
            else:
                negative_hits.append(token)
                score -= 1

    # Determine label
    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    # Build explanation
    parts = []
    if positive_hits:
        parts.append(f"positive signals: {', '.join(set(positive_hits))}")
    if negative_hits:
        parts.append(f"negative signals: {', '.join(set(negative_hits))}")
    if negated_hits:
        parts.append(f"negation applied to: {', '.join(set(negated_hits))}")
    if not parts:
        parts.append("no sentiment-bearing words found in lexicon")

    explanation = " | ".join(parts)

    return {
        "label":         label,
        "score":         score,
        "positive_hits": list(set(positive_hits)),
        "negative_hits": list(set(negative_hits)),
        "negated_hits":  list(set(negated_hits)),
        "explanation":   explanation,
    }


# ── Pretty printer ────────────────────────────────────────────────────────────

def print_result(text: str, result: dict) -> None:
    label_icon = {"Positive": "[+]", "Negative": "[-]", "Neutral": "[~]"}
    icon = label_icon[result["label"]]

    print("─" * 60)
    print(f"Text    : {text}")
    print(f"Result  : {icon} {result['label']}  (score: {result['score']:+d})")
    print(f"Why     : {result['explanation']}")
    print("─" * 60)


# ── Demo ──────────────────────────────────────────────────────────────────────

DEMO_SENTENCES = [
    # Medical
    "Hasta iyileşme sürecinde olup durumu stabil görünmektedir.",
    "Hastada ciddi enfeksiyon ve ateş semptomları gözlemlendi.",
    "Ağrı değil, sadece hafif bir rahatsızlık hissediyor.",
    # Legal
    "Başvuru onaylandı ve geçerli kabul edildi.",
    "Belge ihlal nedeniyle reddedildi.",
    # General
    "Bu proje oldukça verimli ve başarılı sonuçlar verdi.",
    "Çok kötü bir deneyimdi, hiç güvenli değildi.",
    "Bugün toplantı yapıldı.",  # Neutral — no sentiment words
]


def run_demo():
    print("\nTurkish Sentiment Analyzer — Demo Run")
    print("=" * 60)
    for sentence in DEMO_SENTENCES:
        result = analyze(sentence)
        print_result(sentence, result)
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Analyse text passed as a command-line argument
        user_text = " ".join(sys.argv[1:])
        result = analyze(user_text)
        print_result(user_text, result)
    else:
        run_demo()
