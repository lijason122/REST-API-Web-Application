from website import create_app
from flask_socketio import SocketIO, send

# Setup
app = create_app()
#socketio = SocketIO(app) # For user communication

# Chat Function
# To be implemented

# Start the web application (server)
if __name__ == '__main__':
    app.run(debug=True)
