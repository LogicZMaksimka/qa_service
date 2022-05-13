from flask import Flask, request, jsonify
from deeppavlov import build_model, configs

app = Flask(__name__)

retrive_gen_model = build_model(configs.squad.coqa_with_bpr_generative_qa_infer, download=False)

def generate_answer(question: str) -> str:
    answers = retrive_gen_model([question])
    return answers[0]

@app.route("/", methods=["POST"])
def response():
    question = request.json.get("question")
    if question is None or question == '':
        return "Error"
    answer = generate_answer(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)