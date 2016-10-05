# Import a library of functions called 'pygame'
import gsdl2
from math import pi

# Initialize the game engine
gsdl2.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [400, 300]
screen = gsdl2.display.set_mode(size)

gsdl2.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = gsdl2.time.Clock()

while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in gsdl2.event.get():  # User did something
        if event.type == gsdl2.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    gsdl2.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    gsdl2.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    #gsdl2.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)

    # Draw a rectangle outline
    gsdl2.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)

    # Draw a solid rectangle
    gsdl2.draw.rect(screen, BLACK, [150, 10, 50, 20])

    # Draw an ellipse outline, using a rectangle as the outside boundaries
    #gsdl2.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)

    # Draw an solid ellipse, using a rectangle as the outside boundaries
    #gsdl2.draw.ellipse(screen, RED, [300, 10, 50, 20])

    # This draws a triangle using the polygon command
    gsdl2.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

    # Draw an arc as part of an ellipse.
    # Use radians to determine what angle to draw.
    #gsdl2.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)
    #pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi / 2, pi, 2)
    #pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3 * pi / 2, 2)
    #pygame.draw.arc(screen, RED, [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

    # Draw a circle
    gsdl2.draw.circle(screen, BLUE, [60, 250], 40)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    gsdl2.display.flip()

# Be IDLE friendly
gsdl2.quit()