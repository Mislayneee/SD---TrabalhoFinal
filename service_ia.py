from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time

app = Flask(__name__)
iris = load_iris()
model = RandomForestClassifier()
model.fit(iris.data, iris.target)

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    input_data = request.get_json()
    tempos = input_data.get("tempos", {})
    tempos["T4"] = time.time()

    features = np.array(input_data.get("features", [0, 0, 0, 0])).reshape(1, -1)
    prediction = model.predict(features)[0]
    target_name = iris.target_names[prediction]

    response = {
        "resposta": target_name,
        "tempos": tempos
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)