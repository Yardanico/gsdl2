# Code taken from http://www.pygame.org/project-2D+Cellular+Automaton+Simulation-1944-.html
# Almost nothing changed, except - removed 3 fps clock, added gsdl2
try:
    import gsdl2 as pygame
except:
    import pygame
import random


class MapGrid():
    def __init__(self, map_width, map_height):

        # set map values
        self.map_width = map_width
        self.map_height = map_width

        # generate outside rooms
        self.outside_terrain_grid = self._generate_empty_noise_grid(self.map_width, self.map_height)

    def _generate_empty_noise_grid(self, map_width, map_height):
        '''
        creates a new 2d array with the given specs
        and filled with random 1s and 0s
        '''

        new_map_grid = [] # create our new list
        for x in range(map_width):
            new_map_grid.append([]) # add our columns to the array
            for y in range(map_height):
                new_map_grid[x].append(random.choice([0,1])) # fill in our rows

        return new_map_grid



    def _generate_outside_terrain(self, empty_outside_terrain_grid, number_of_generations):
        '''
        creates a bubble effect with cellular automaton
        '''
        grid = empty_outside_terrain_grid
        number_of_generations = number_of_generations

        for x in range(number_of_generations):
            next_grid = []
            for column_index, column in enumerate(grid):
                next_column = []
                next_grid.append(next_column)
                for tile_index, tile in enumerate(column):

                    # get the surrounding tile values for each tile
                    top_left = grid[column_index - 1][tile_index - 1]
                    top_mid = grid[column_index][tile_index - 1]
                    try:
                        top_right = grid[column_index + 1][tile_index - 1]
                    except IndexError:
                        top_right = 0
                    
                    center_left = grid[column_index - 1][tile_index]
                    center_mid = grid[column_index][tile_index]
                    try:
                        center_right = grid[column_index + 1][tile_index]
                    except IndexError:
                        center_right = 0

                    try:
                        bottom_left = grid[column_index - 1][tile_index + 1]
                    except IndexError:
                        bottom_left = 0
                    try:
                        bottom_mid = grid[column_index][tile_index + 1]
                    except IndexError:
                        bottom_mid = 0
                    try:
                        bottom_right = grid[column_index + 1][tile_index + 1]
                    except IndexError:
                        bottom_right = 0


                    close_neighbors = (top_mid + center_left + center_mid +
                                       center_right + bottom_mid)

                    far_neighbors = (top_left + top_right +
                                     bottom_left + bottom_right)

                    number_of_neighbors = close_neighbors + far_neighbors

                    # decide the what the next cell will be based on these rules
                    if number_of_neighbors > random.choice([3,4,5]):
                        next_cell = 1

                    else:
                        next_cell = 0

                    if close_neighbors > 3:
                        next_cell = 1

                    # create the new cell
                    next_column.append(next_cell)
            grid = next_grid

                    
                    
                    
        return next_grid



                    
if __name__ == '__main__':
    # general map stats
    map_width = 280
    map_height = 180

    # start with one generation
    tile_size = 3
    
    map_grid = MapGrid(map_width, map_height)
    #print map_grid.outside_terrain_grid

    pygame.init()

    screen = pygame.display.set_mode((map_width * tile_size,map_height * tile_size))
    
    one_tile = pygame.Surface((1, 1))
    one_tile.fill((0,0,0))
    zero_tile = pygame.Surface((1, 1))
    zero_tile.fill((255,255,255))
    colors = {0: zero_tile, 1: one_tile}

    background = pygame.Surface((map_width * tile_size,map_height * tile_size))

    clock = pygame.time.Clock()

    first_gen = True
    timer = 12
    
    running = True
    while running == True:
        clock.tick()  # there was 3 fps lock :)
        pygame.display.set_caption('2D Cellular Automaton Simulation 1.0 Mad Cloud Games - FPS: ' + str(clock.get_fps()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if first_gen:
            themap = map_grid.outside_terrain_grid
        else:
            themap = map_grid._generate_outside_terrain(themap, 1)

        for column_index, column in enumerate(themap):
            for tile_index, tile in enumerate(column):
                screen.blit(colors[tile], (tile_index * tile_size, column_index * tile_size))

        pygame.display.flip()

        if first_gen:
            timer -= 1
            if timer < 0:
                first_gen = False

    pygame.quit()
