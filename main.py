from flask import Flask
from blockchain import blockchain
from connection import connection
from subscription import subscription
from actor import actor
from certificate import certificate
from claim import claim
from revoke import revoke
from verification import verification
import settings



app = Flask(__name__)
app.register_blueprint(blockchain)
app.register_blueprint(connection)
app.register_blueprint(subscription)
app.register_blueprint(actor)
app.register_blueprint(certificate)
app.register_blueprint(claim)
app.register_blueprint(revoke)
app.register_blueprint(verification)


if __name__ == '__main__':
	app.run(debug = True, host="0.0.0.0")
