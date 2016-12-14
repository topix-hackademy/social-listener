from flask import redirect, Flask, jsonify, abort, request, make_response, url_for, render_template, flash
from process_manager import ProcessManager


app = Flask(__name__)
app.config.from_object(__name__)

pm = ProcessManager()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()