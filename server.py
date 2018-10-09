from flask import (
    Flask,
    render_template,
    request,
    abort,
    jsonify
)
import databaseConnection as db

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
# This is purely to see if the server is running, there is no website planned
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

@app.route('/insertEvent', methods=['POST'])
def add_event():
    print("got event")
    if not request.json:
        return jsonify({'status' : 'True', 'message':'Wrong document type'}), 400
    success = db.insertEvent(request.json)
    if not success:
        return jsonify({'status' : 'True', 'message':'Insertion not successful'}), 400
    return jsonify({'status' : 'True', 'message':'Insertion successful'}), 201


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)