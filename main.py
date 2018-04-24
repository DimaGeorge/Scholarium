from flask import Flask
from blockchain import blockchain
from connection import connection
from subscription import subscription
import settings

app = Flask(__name__)
app.register_blueprint(blockchain)
app.register_blueprint(connection)
app.register_blueprint(subscription)


if __name__ == '__main__':
	app.run(debug = True, host="0.0.0.0")
