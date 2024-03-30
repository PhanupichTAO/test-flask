from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # หน้า page หลัก
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

