try:
    import gsdl2 as pygame
except:
    import pygame

pygame.init()
pygame.display.set_mode((320,240))

clock = pygame.time.Clock()
fps_values = []
for _ in range(50000):
    clock.tick()
    fps = clock.get_fps()
    fps_values.append(fps)
    pygame.display.flip()

fps = sum(fps_values)/float(len(fps_values))
print("Average FPS is " + str(fps) if fps!=float('inf') else "Average fps is bigger than 10000 :)")