# Turkish Sentiment Analyzer

A lexicon-based sentiment analysis tool for Turkish text. Classifies input as **Positive**, **Negative**, or **Neutral** — and explains *why*.

---

## Motivation

Most NLP sentiment tools are built for English. Turkish is a morphologically rich, agglutinative language, and off-the-shelf English tools perform poorly on it. As a native Turkish speaker working in NLP and professional translation (medical, legal, technical domains), I built this to fill a real gap in my localization workflows.

This project is a first step toward a full bilingual sentiment pipeline for Turkish–English document pairs.

---

## How it works

1. Tokenizes the input text (lowercased, whitespace split)
2. Looks up each token against curated **positive** and **negative** lexicons
3. Checks for **negation words** (`değil`, `yok`, `asla`...) that flip the next token's polarity
4. Computes a net sentiment **score** (positive hits − negative hits)
5. Returns a label (`Positive` / `Negative` / `Neutral`) with a plain-language explanation

```
Text    : Hasta iyileşme sürecinde olup durumu stabil görünmektedir.
Result  : [+] Positive  (score: +2)
Why     : positive signals: iyileşme, stabil
```

---

## Example output

```
────────────────────────────────────────────────────────────
Text    : Başvuru onaylandı ve geçerli kabul edildi.
Result  : [+] Positive  (score: +2)
Why     : positive signals: onaylandı, geçerli

────────────────────────────────────────────────────────────
Text    : Hastada ciddi enfeksiyon ve ateş semptomları gözlemlendi.
Result  : [-] Negative  (score: -3)
Why     : negative signals: ciddi, enfeksiyon, semptom

────────────────────────────────────────────────────────────
Text    : Ağrı değil, sadece hafif bir rahatsızlık hissediyor.
Result  : [~] Neutral  (score: 0)
Why     : negation applied to: ağrı | negative signals: rahatsızlık
```

---

## How to run

**Option 1 — Google Colab (recommended)**
1. Open `sentiment_analyzer.py` and copy the contents into a Colab cell
2. Run the cell — no installation needed (no external dependencies)
3. Call `analyze("Metninizi buraya yazın")` with your own text

**Option 2 — Local**
```bash
git clone https://github.com/tumut-k/turkish-sentiment-analyzer
cd turkish-sentiment-analyzer

# Run the demo
python sentiment_analyzer.py

# Analyse your own text
python sentiment_analyzer.py "Hasta durumu kritik ve acil müdahale gerekiyor."
```

No `pip install` needed — the script uses only the Python standard library.

---

## Domains covered

The lexicon includes seed words from three domains matching my professional translation experience:

| Domain | Example positive | Example negative |
|--------|-----------------|-----------------|
| General | iyi, başarılı, güvenli | kötü, tehlikeli, sorun |
| Medical | iyileşme, stabil, negatif | ağrı, enfeksiyon, kritik |
| Legal | onaylandı, geçerli, hak | reddedildi, ihlal, ceza |

---

## Limitations & next steps

- The current lexicon is a **seed list** — coverage is intentionally narrow to keep the logic transparent
- A production version would use [SentiTurkNet](https://github.com/nrslts/SentiTurkNet) or a transformer model fine-tuned on Turkish (e.g., BERTurk)
- Turkish morphology means `iyileşmedi`, `iyileşemedi`, `iyileşemeyecekti` all derive from `iyileş` — future versions will add a morphological stemmer
- Planned: bilingual output showing EN↔TR sentiment alignment for parallel corpora

---

## About

Built by **Talha Umut Kulu**, a professional translator/interpreter (500,000+ words across medical, legal and technical domains) currently transitioning into NLP. This project reflects the real-world gap I encounter when working with Turkish source documents in localization pipelines.

- GitHub: [github.com/tumut-k](https://github.com/tumut-k)
- LinkedIn: [linkedin.com/in/tumutk](https://linkedin.com/in/tumutk)
