from flask import Flask
from blockchain import blockchain
import settings

app = Flask(__name__)
app.register_blueprint(blockchain)



if __name__ == '__main__':
	app.run(debug = True)
