from dotenv import load_dotenv
from flask import Flask, request, jsonify
from modules import llm, omnicomplete
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)


CORS(app, origins="http://172.16.113.16:5173")


@app.route("/get-autocomplete", methods=["POST"])
def get_autocomplete():
    input_data = request.json["input"]

    prompt = omnicomplete.build_omni_complete_prompt(
        input_data
    )

    print("prompt", prompt)

    response = llm.prompt_json(prompt)
    if input_data in response:
        response = response.replace(input_data, "")

    print("Response: ", response)

    return jsonify(response)


@app.route("/use-autocomplete", methods=["POST"])
def do_autocomplete():
    autocomplete_object = request.json
    input_data = autocomplete_object["input"]
    completion = autocomplete_object["completion"]

    print(f"Received autocomplete object: input={input_data}, completion={completion}")

    omnicomplete.increment_or_create_previous_completions(
        input_data, completion
    )

    return jsonify(success=True)


if __name__ == "__main__":
    app.run()
