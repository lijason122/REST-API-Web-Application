from website import create_app, __init__, models, db
from flask_socketio import SocketIO, send
import datetime

# Setup
app = create_app()
socketio = SocketIO(app) # For user communication

# Chat Function
@socketio.on('message')
def handleMessage(msg):
    """
    The server handles the messages they get sent in and picks up the message event
    and broadcasts the same message out to all the chat clients
    """
    print('Message: ' + msg)

    message = models.History(message=msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)


# Start the web application (server)
if __name__ == '__main__':
    socketio.run(app, debug=True)
