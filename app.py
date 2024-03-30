from flask import Flask, render_template
app = Flask(__name__)






@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':         # รับไฟล์ของ post จาก index.html 
    return None

@app.route('/', methods=['GET'])
def index():
    # หน้า page หลัก
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

