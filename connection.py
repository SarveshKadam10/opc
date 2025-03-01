# use opcua to connect opc()
from opcua import Client

# Kepware OPC UA server (No security)
url = "opc.tcp://192.168.4.227:49320"

# Created a client instance
client = Client(url)

# Timeout set
client.secure_channel_timeout = 600000 # 600 sec
client.session_timeout = 60000  # 60 sec

# Connection made
client.connect()
print("Connected to Kepware OPC UA Server")

# Got the node/tag
node1 = client.get_node("ns=2;s=Channel1.Device1.rand1")
node2 = client.get_node("ns=2;s=Channel1.Device1.rand2")
node3 = client.get_node("ns=2;s=Channel1.Device1.rand3")
node4 = client.get_node("ns=2;s=Channel1.Device1.rand4")