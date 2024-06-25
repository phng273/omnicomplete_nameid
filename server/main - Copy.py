from dotenv import load_dotenv
from flask import Flask, request, jsonify
from modules import llm, omnicomplete, New
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)


CORS(app, origins="http://172.16.113.16:5173")

@app.route("/use-autocomplete", methods=["POST"])
def do_autocomplete():
    
    input_data = request.json["input"]
    
    if input_data.isdigit():
        completion = New.search_by_id_prefix(prefix=input_data)
    else:
        completion = New.search_by_name_prefix(prefix=input_data)
    print(f"Received autocomplete object: input={input_data}, completion={completion}")

    omnicomplete.increment_or_create_previous_completions(
        input_data, completion
    )

    return jsonify(success=True)


if __name__ == "__main__":
    app.run()
