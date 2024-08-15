import pygame
import sys
import socket
import threading

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Strategy Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Unit settings
unit_size = 20
unit_pos = [WIDTH // 2, HEIGHT // 2]
unit_speed = 5

# Network settings
HOST = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Handle incoming messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                unit_pos[0], unit_pos[1] = map(int, message.split(','))
        except:
            break

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Game loop
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle unit movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            unit_pos[0] -= unit_speed
        if keys[pygame.K_RIGHT]:
            unit_pos[0] += unit_speed
        if keys[pygame.K_UP]:
            unit_pos[1] -= unit_speed
        if keys[pygame.K_DOWN]:
            unit_pos[1] += unit_speed

        # Send unit position to the server
        client_socket.sendall(f'{unit_pos[0]},{unit_pos[1]}'.encode('utf-8'))

        # Fill the background
        window.fill(WHITE)

        # Draw the unit
        pygame.draw.rect(window, RED, (*unit_pos, unit_size, unit_size))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()