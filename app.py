from flask import Flask

from jackednroses.auth.auth import auth_bp
from jackednroses.edurec.edurec import edurec_bp
from jackednroses.general.general import general_bp
from jackednroses.luminus.luminus import luminus_bp
from jackednroses.uhms.uhms import uhms_bp

app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth") #authentication
app.register_blueprint(edurec_bp, url_prefix="/edurec") #edurec
app.register_blueprint(general_bp) #homepage
app.register_blueprint(luminus_bp, url_prefix="/luminus") #luminus
app.register_blueprint(uhms_bp, url_prefix="/uhms") #uhms
