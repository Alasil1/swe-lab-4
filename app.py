from flask import Flask
from routes.todo import todo_bp

app = Flask(__name__)

app.register_blueprint(todo_bp, url_prefix="/todo")
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error":"Resource not found "}),404

if __name__ =="__main__":
    app.run(port = 3000)