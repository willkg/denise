import os

from flask import Flask, send_from_directory


# Create the app
app = Flask(__name__)

# Handle settings--look at os.environ first
settings_key = 'DENISE_SETTINGS'.upper()
if os.environ.get(settings_key):
    app.config.from_envvar(settings_key, silent=True)
else:
    from denise import settings
    app.config.from_object(settings)

# Register error handlers
from denise.errors import register_error_handlers
register_error_handlers(app)

# Register views
from denise import views
app.register_blueprint(views.mod)


# Add the config to the context, so it's available in templates
@app.context_processor
def context_processor():
    return dict(config=app.config)


# Special rule for old browsers to correctly handle favicon.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')
