from flask import Flask, render_template

app = Flask(__name__)

@app.route('/check')
def check():
    return render_template('check.html')

if __name__ == '__main__':
    app.run(debug=True)
