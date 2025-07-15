from app import app

# Vercel entry point
def handler(request):
    return app(request.environ, lambda *args: None)

# For Vercel compatibility
application = app

if __name__ == "__main__":
    app.run() 