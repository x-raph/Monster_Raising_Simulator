# 妖怪牧場
import pygame, sys
from monsters.Slime import Slime
from food.Berry import Berry
from monsters.miscellaneous.Activity_Level import Activity_Level
import time


class World:

    def __init__(self):
        pygame.init()  # initiate pygame
        self.FPS = 60
        self.food_container = []
        self.width = 800
        self.height = 600
        self.surface = pygame.display.set_mode((self.width, self.height))  # pygame.Surface object for the window
        self.surface_color = (245, 245, 220)
        self.surface.fill(self.surface_color)
        self.update_counter = 0
        pygame.display.set_caption('Yōkai Ranch')
        self.time_start = time.time()

    def update_food_container(self):
        for food in self.food_container:
            if food.is_destroyed:
                self.food_container.remove(food)


World = World()
slime = Slime('Monokai', World)

day_tracker = 0





while True:  # main game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # create food
            if event.key == pygame.K_f:
                if len(World.food_container) < 50:
                    berry = Berry(World)
                    World.food_container.append(berry)

            # set all food is_destroyed to True
            if event.key == pygame.K_d:
                for food in World.food_container:
                    food.destroy()

            if event.key == pygame.K_a:
                if slime.body.stamina.activity_level.name == 'Sleep':
                    slime.body.stamina.activity_level = Activity_Level['Rest']
                elif slime.body.stamina.activity_level.name == 'Rest':
                    slime.body.stamina.activity_level = Activity_Level['Idle']
                elif slime.body.stamina.activity_level.name == "Idle":
                    slime.body.stamina.activity_level = Activity_Level['Light']
                elif slime.body.stamina.activity_level.name == "Light":
                    slime.body.stamina.activity_level = Activity_Level['Moderate']
                elif slime.body.stamina.activity_level.name == "Moderate":
                    slime.body.stamina.activity_level = Activity_Level['Heavy']
                elif slime.body.stamina.activity_level.name == "Heavy":
                    slime.body.stamina.activity_level = Activity_Level['Sleep']


    if World.update_counter == World.FPS:
        World.surface.fill(World.surface_color)
        slime.update()
        for each in World.food_container:
            each.update()
            each.display_location()
        print("----------------------------------------")
        print("TIME ELAPSED: " + str(round(time.time() - World.time_start, 0)) + " " + " seconds")
        print("----------------------------------------")
        #print(World.food_container)
        slime.display_values()
        slime.body.world_movement.display_closest_food()
        World.update_counter = 0




    World.update_food_container()



    #World.surface.fill(World.surface_color)
    #slime.update()
    #slime.display_values()


    pygame.display.update()
    pygame.time.Clock().tick(World.FPS)
    World.update_counter += 1
