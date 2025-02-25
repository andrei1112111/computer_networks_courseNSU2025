import parser
import db

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route(methods=["POST", "GET"], rule='/parse')
def parse():
    url = request.args.get('url')
    if not url:
        return 'No url provided'

    if request.method == "POST":
        parsed = parser.parse_url(url)
        if not parsed:
            return jsonify({})

        db.insertDB(url=url, data=parsed)

        return jsonify(parsed)

    elif request.method == "GET":
        parsed = db.getDB(url)

        if not parsed:
            return jsonify({})

        return jsonify(parsed.data)


if __name__ == '__main__':
    app.run(debug=True)
