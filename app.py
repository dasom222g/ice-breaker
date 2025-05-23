from flask import Flask, render_template, request, jsonify

from ice_breaker import ice_break

app = Flask(__name__)  # Flask 애플리케이션 초기화


# 메인페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    req = request.form  # form데이터인 경우
    name = req.get('name')
    # Agent 연결
    info_data, pic_url = ice_break(name=name)
    return jsonify({
        'data': info_data,
        'pic_url': pic_url
    })


if __name__ == '__main__':
    print('Hello world')
    app.run(host='0.0.0.0', port=8080, debug=True)
