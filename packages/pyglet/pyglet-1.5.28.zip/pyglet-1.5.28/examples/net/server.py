import pyglet


server = pyglet.net.Server(address='0.0.0.0', port=1234)


connections = []


@server.event
def on_connection(connection):
    print(f"New clinet connected: {connection}")
    connections.append(connection)


pyglet.app.run()
