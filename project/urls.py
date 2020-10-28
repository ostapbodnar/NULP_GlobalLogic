from . import app


@app.route('/')
def index():
    return '<a href="/api/v1/hello-world-3">hello world</a>'


@app.route("/api/v1/hello-world-3")
def hello_world():
    return "Hello World 3"
