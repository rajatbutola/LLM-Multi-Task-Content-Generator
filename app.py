from flask import Flask, render_template, request
from datetime import datetime, timedelta
from model import generate_blog, generate_summary, generate_email

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def _compute_return_date(start_date_str, duration_days_str):
    """If return_date is empty but duration provided, compute it."""
    if not start_date_str or not duration_days_str:
        return ""
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        dur = int(duration_days_str)
        # Return on the day after 'dur' days off
        ret = start + timedelta(days=dur)
        return ret.strftime("%Y-%m-%d")
    except Exception:
        return ""

@app.route("/generate", methods=["POST"])
def generate():
    try:
        task = request.form.get("task")
        topic = request.form.get("topic") or ""
        keywords = request.form.get("keywords").split(",") if request.form.get("keywords") else []
        tone = request.form.get("tone") or "professional"
        text = request.form.get("text") or ""

        if task == "blog":
            content = generate_blog(topic, keywords, tone)

        elif task == "summary":
            content = generate_summary(text) if text else "Please provide the text you want to summarize."

        elif task == "email":
            # New email fields
            recipient_name = request.form.get("recipient_name") or "Manager"
            reason = request.form.get("reason") or ""
            start_date = request.form.get("start_date") or ""
            duration_days = request.form.get("duration_days") or ""
            return_date = request.form.get("return_date") or ""
            handover_name = request.form.get("handover_name") or ""
            handover_contact = request.form.get("handover_contact") or ""

            # If duration is given but no return date, compute it
            if not return_date and duration_days and start_date:
                return_date = _compute_return_date(start_date, duration_days)

            content = generate_email(
                subject=topic or "Leave Application",
                tone=tone,
                recipient_name=recipient_name,
                reason=reason,
                start_date=start_date,
                duration_days=duration_days,
                return_date=return_date,
                handover_name=handover_name,
                handover_contact=handover_contact,
            )

        else:
            content = "Task not supported."

        return render_template("result.html", topic=topic, content=content, task=task)

    except Exception as e:
        return render_template("result.html", topic="", content=f"Error: {e}", task="error"), 200

if __name__ == "__main__":
    app.run(debug=True)
