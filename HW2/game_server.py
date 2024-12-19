import socket

# Define server IP and PORT
SERVER_IP = "0.0.0.0"  # Listen on all available interfaces
SERVER_PORT = 49152    # Port number (must match the STM32 client's port)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_IP, SERVER_PORT))

# Start listening for incoming connections
server_socket.listen(1)  # Allows 1 client connection at a time (can be increased if needed)
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Initialize lists to store received data
# x_data, y_data, z_data = [], [], []

# Remove the plot setup
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
# line_x, = ax1.plot([], [], 'r-', label='X Data')
# line_y, = ax2.plot([], [], 'g-', label='Y Data')
# line_z, = ax3.plot([], [], 'b-', label='Z Data')
# ax1.set_xlim(0, 1000)
# ax1.set_ylim(-20, 20)
# ax2.set_xlim(0, 1000)
# ax2.set_ylim(-20, 20)
# ax3.set_xlim(0, 1000)
# ax3.set_ylim(-20, 20)
# ax1.set_title('X Data')
# ax1.set_xlabel('Time')
# ax1.set_ylabel('X Value (m/s^2)')
# ax1.legend()
# ax2.set_title('Y Data')
# ax2.set_xlabel('Time')
# ax2.set_ylabel('Y Value (m/s^2)')
# ax2.legend()
# ax3.set_title('Z Data')
# ax3.set_xlabel('Time')
# ax3.set_ylabel('Z Value (m/s^2)')
# ax3.legend()

def update_plot(frame):
    data = client_socket.recv(50)  # Buffer size of 50 bytes
    if not data:
        # If no data is received, the client has disconnected
        print("Client disconnected")
        return

    # Decode and print the received data
    received_message = data.decode('utf-8').strip().replace('\x00', '')
    print(f"Received from STM32: {received_message}")

# Remove FuncAnimation and plt.show()
# ani = FuncAnimation(fig, update_plot, interval=100)
# plt.tight_layout()
# plt.show()

# Replace with a loop to keep receiving data
while True:
    update_plot(None)

# Close the connection
client_socket.close()
server_socket.close()