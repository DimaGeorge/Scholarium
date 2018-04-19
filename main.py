from flask import Flask
from blockchain import blockchain
from connection import connection
import settings

app = Flask(__name__)
app.register_blueprint(blockchain)
app.register_blueprint(connection)


if __name__ == '__main__':
	app.run(debug = True)
