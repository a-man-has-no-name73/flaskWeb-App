import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".npz"):
            # For now, return a demo message since TensorFlow isn't available on Python 3.13
            prediction = "🚀 Flask app is working! TensorFlow model will be added once Python 3.11/3.12 is available on Render."
        else:
            prediction = "❌ Please upload a valid .npz file."
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
