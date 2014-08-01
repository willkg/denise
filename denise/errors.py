from flask import render_template


def register_error_handlers(app):
    """Registers all the error handlers for an app"""
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_server_error)


def error(code, message, template):
    """A generic error handler"""
    return render_template(template, message=message), code


def not_found(message=None):
    """A generic 404 handler"""
    message = message or 'Page not found.'
    return error(404, message, 'errors/404.html')


def internal_server_error(message=None):
    """A generic 500 handler"""
    message = message or 'Something went wrong.'
    return error(500, message, 'errors/500.html')
