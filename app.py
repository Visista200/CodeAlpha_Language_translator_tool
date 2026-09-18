from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():

    try:
        data = request.get_json()

        text = data.get("text", "").strip()
        source = data.get("source", "en")
        target = data.get("target", "te")

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter some text."
            }), 400

        # MyMemory API
        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{source}|{target}"
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()

        # Get translated text
        translated_text = result["responseData"]["translatedText"]

        return jsonify({
            "success": True,
            "translation": translated_text
        })

    except requests.exceptions.RequestException as e:

        print("API Error:", e)

        return jsonify({
            "success": False,
            "error": "Translation service is currently unavailable."
        }), 500

    except Exception as e:

        print("Translation Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)