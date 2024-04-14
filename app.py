from webframe import Serve
import json

app = Serve()
response = app.response
render_temp = app.render_temp


@app.route('/')
def home():
    return render_temp('index.html')


@app.route('/api/user', methods=['get'])
def user():
    data = {
        "user": [
            {"name": "mukit",
             "age": 24},
            {"name": "jhone",
             "age": 22},
            {"name": "helli",
             "age": 19},
            {"name": "Doe",
             "age": 21},
        ]
    }
    res = json.dumps(data)
    return response(res, 200)


@app.route('/api/hello')
def hello():
    return response(json.dumps({"message": 'hello'}), 200)


if __name__ == "__main__":
    app.run()
