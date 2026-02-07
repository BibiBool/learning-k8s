from src.provider import app

# Alias for WSGI compliance
application = app

if  __name__ == '__main__':
    app.run()