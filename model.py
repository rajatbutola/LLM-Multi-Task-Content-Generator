from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    LogitsProcessorList,
    MinLengthLogitsProcessor,
)
import torch
import re

# -----------------------------
# Device
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"


# -----------------------------
# Helpers
# -----------------------------
def _prep_tokenizer_pad(tokenizer):
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer

def _bad_word_ids(tokenizer, strs):
    seqs = []
    for s in strs:
        ids = tokenizer.encode(s, add_special_tokens=False)
        if ids:
            seqs.append(ids)
    return seqs if seqs else None

def _tidy_email(text: str) -> str:
    text = text.strip()
    # Remove list artifacts
    text = re.sub(r"^\s*[-•\d]+\s*[\.\)]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    # Greeting
    if not re.search(r"^(Dear|Hello|Hi)\b", text, re.I):
        text = "Dear Manager,\n\n" + text
    # Sign-off
    if not re.search(r"\b(Sincerely|Best regards|Kind regards|Regards)\b", text, re.I):
        text = text.rstrip() + "\n\nBest regards,\n[Your Name]"
    return text


# -----------------------------
# Models
# -----------------------------
models = {
    "blog": {
        "model": AutoModelForCausalLM.from_pretrained(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        ).to(device).eval(),
        "tokenizer": _prep_tokenizer_pad(
            AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        ),
    },
    "summarize": {
        "model": AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-small"
        ).to(device).eval(),
        "tokenizer": AutoTokenizer.from_pretrained("google/flan-t5-small"),
    },
    "email": {
        "model": AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-base"
        ).to(device).eval(),
        "tokenizer": AutoTokenizer.from_pretrained("google/flan-t5-base"),
    },
}


# -----------------------------
# Generation functions
# -----------------------------
@torch.inference_mode()
def generate_blog(topic, keywords, tone, max_new_tokens=250, temperature=0.7):
    model = models["blog"]["model"]
    tokenizer = models["blog"]["tokenizer"]

    kw = ", ".join([k.strip() for k in keywords]) if keywords else "None"
    prompt = (
        f"### Task: Write a blog post\n"
        f"### Topic: {topic}\n"
        f"### Keywords: {kw}\n"
        f"### Tone: {tone}\n"
        f"### Requirements: 3–6 short paragraphs, clear structure, no preamble.\n\n"
        f"Blog post:\n"
    )

    enc = tokenizer(prompt, return_tensors="pt").to(device)
    out = model.generate(
        **enc,
        do_sample=True,
        temperature=temperature,
        top_p=0.9,
        max_new_tokens=max_new_tokens,
        repetition_penalty=1.05,
        no_repeat_ngram_size=3,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    new_tokens = out[0][enc["input_ids"].shape[-1]:]
    text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    return text


@torch.inference_mode()
def generate_summary(text, max_new_tokens=1610):
    model = models["summarize"]["model"]
    tokenizer = models["summarize"]["tokenizer"]

    prompt = f"Summarize this text clearly and concisely:\n\n{text}\n\nSummary:"
    enc = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
    out = model.generate(
        **enc,
        max_new_tokens=max_new_tokens,
        num_beams=4,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        early_stopping=True,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True).strip()


@torch.inference_mode()
def generate_email(
    subject: str,
    tone: str,
    recipient_name: str,
    reason: str,
    start_date: str,
    duration_days: str,
    return_date: str,
    handover_name: str,
    handover_contact: str,
    max_new_tokens: int = 220,
):
    """Generate a clear 2-paragraph leave request using explicit fields."""
    model = models["email"]["model"]
    tokenizer = models["email"]["tokenizer"]

    # Guard strings
    recipient = recipient_name or "Manager"
    reason = reason or "personal reasons"
    start_date = start_date or "[start date]"
    duration_days = duration_days or ""
    return_date = return_date or "[return date]"
    handover_name = handover_name or ""
    handover_contact = handover_contact or ""

    duration_line = f" for {duration_days} days" if duration_days else ""
    handover_line = ""
    if handover_name or handover_contact:
        if handover_name and handover_contact:
            handover_line = f" {handover_name} ({handover_contact}) will cover urgent matters in my absence."
        elif handover_name:
            handover_line = f" {handover_name} will cover urgent matters in my absence."
        elif handover_contact:
            handover_line = f" A colleague at {handover_contact} will cover urgent matters in my absence."

    prompt = (
        f"Write a {tone} leave request email.\n"
        f"Subject: {subject}\n"
        f"To: {recipient}\n"
        f"Reason: {reason}\n"
        f"Start date: {start_date}\n"
        f"Duration (days): {duration_days}\n"
        f"Expected return date: {return_date}\n"
        f"Handover: {handover_line.strip() if handover_line else 'N/A'}\n"
        f"Constraints:\n"
        f"- Two short paragraphs (no bullets, no numbered lists, no attachments).\n"
        f"- Include reason, start date, expected return date{duration_line}, and explicit approval request.\n"
        f"- Offer to provide handover/support; include the handover sentence if provided.\n"
        f"- Professional tone; 120–180 words.\n"
        f"- Start with 'Dear {recipient},' and end with a polite sign-off.\n\n"
        f"Email:\n"
    )

    enc = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

    banned = _bad_word_ids(
        tokenizer,
        ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0.", "- ", "• ", "Attached", "attached"]
    )
    processors = LogitsProcessorList(
        [MinLengthLogitsProcessor(60, eos_token_id=tokenizer.eos_token_id)]
    )

    out = model.generate(
        **enc,
        max_new_tokens=max_new_tokens,
        num_beams=5,
        length_penalty=1.0,
        no_repeat_ngram_size=5,
        early_stopping=True,
        bad_words_ids=banned,
        logits_processor=processors,
    )
    text = tokenizer.decode(out[0], skip_special_tokens=True).strip()
    return _tidy_email(text)
