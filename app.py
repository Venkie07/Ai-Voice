from flask import Flask, render_template, request, send_file, abort
from gtts import gTTS
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text")
    lang = request.form.get("lang")

    if not text:
        abort(400, "Text input is required")

    try:
        tts = gTTS(text=text, lang=lang)

        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        return send_file(
            audio_bytes,
            mimetype="audio/mpeg",
            as_attachment=False  # play in browser
        )

    except Exception as e:
        return f"Error generating audio: {str(e)}", 500


@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("text")
    lang = request.form.get("lang")

    if not text:
        abort(400, "Text input is required")

    try:
        tts = gTTS(text=text, lang=lang)

        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        return send_file(
            audio_bytes,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="voice.mp3"
        )

    except Exception as e:
        return f"Error generating audio: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)