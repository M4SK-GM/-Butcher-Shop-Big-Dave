from flask import Flask, render_template

app = Flask(__name__)


def main():
    @app.route('/')
    def index():
        return render_template('index.html', title='Основная')
    app.run()


if __name__ == '__main__':
    main()
