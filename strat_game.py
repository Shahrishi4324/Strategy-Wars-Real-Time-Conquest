import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Strategy Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load sounds
pygame.mixer.init()
resource_sound = pygame.mixer.Sound('resource_collect.wav')
build_sound = pygame.mixer.Sound('build_structure.wav')

# Unit settings
unit_size = 20
unit_pos = [WIDTH // 2, HEIGHT // 2]
unit_speed = 5

# AI settings
ai_units = [[random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20)] for _ in range(5)]

# Resources settings
resources = [[random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20)] for _ in range(10)]

# Game loop
def main():
    clock = pygame.time.Clock()
    fog = pygame.Surface((WIDTH, HEIGHT))
    fog.fill(BLACK)
    fog.set_alpha(180)
    font = pygame.font.Font(None, 36)

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

        # Check for resource collection
        for resource in resources[:]:
            if (unit_pos[0] < resource[0] + 20 and unit_pos[0] + unit_size > resource[0] and
                unit_pos[1] < resource[1] + 20 and unit_pos[1] + unit_size > resource[1]):
                resources.remove(resource)
                resource_sound.play()

        # Fill the background
        window.fill(WHITE)

        # Draw resources
        for resource in resources:
            pygame.draw.rect(window, GREEN, (*resource, 20, 20))

        # Draw the AI units
        for ai in ai_units:
            pygame.draw.rect(window, BLUE, (*ai, unit_size, unit_size))

        # Draw the player's unit
        pygame.draw.rect(window, RED, (*unit_pos, unit_size, unit_size))

        # Draw the fog of war
        window.blit(fog, (0, 0))

        # Display resource count
        text = font.render(f'Resources: {len(resources)}', True, BLACK)
        window.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
