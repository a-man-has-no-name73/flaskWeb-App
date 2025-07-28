# Alternative app.py for deployment issues
# Use this if the main app.py fails to deploy due to TensorFlow issues

import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".npz"):
            # Fallback response when model can't load
            prediction = "⚠️ Model loading temporarily disabled for deployment. App structure is working!"
        else:
            prediction = "❌ Please upload a valid .npz file."
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
