from app import create_app, db
from flask_migrate import Migrate
from app.models import Post

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)


