# Food / digestion / excretion system, influenced by Endurance stat (not yet implemented)
# stats are End and Luk
from monsters.miscellaneous.Stats import Stats
from miscellaneous.Poop import Poop


class Stomach:

    def __init__(self, body, world):

        self.world = world # used for expelling waste!
        self.body = body

        self.type = str(body.whole_body.race) + " Stomach"
        self.weight = 3
        self.stats = Stats(0, 0, 2, 0, 0, 1)

        self.is_starving = False
        self.is_hungry = False
        self.hunger_max = 100
        self.hunger_cur = 80
        self.hunger_threshold = 60      # amount of hunger til creature will seek out food
        self.hunger_rate = 1            # hunger gain per tick

        self.contents = []
        self.digestion_rate = 4         # amount of nutrients absorbed from food per tick
        self.digestion_efficiency = 50   # influences the amount of waste material produced per tick (urine / feces)

        self.urine_max = 100
        self.urine_cur = 80
        self.fecal_max = 100
        self.fecal_cur = 80

    # function to eat food objects, called from World_Movement class on collision with food object when is_hungry equals True
    # food object is added to stomach content, food is_eaten variable is set to True and food's weight is added to stomach weight, which
    # will later be added to overall body weight on update
    def eat(self, food):

        self.contents.append(food)
        food.become_eaten()
        self.weight += food.weight

    # controls digestion of each food objects in stomach content
    def digest_food(self):
        # iterate through each food in stomach.content
        for food in self.contents:
            food_nutrition_cur = food.nutrition      # get food's current nutrition for hunger decrease calculation
            food.nutrition -= self.digestion_rate    # decrease the nutrition points in food by digestion rate
            if food.nutrition < 0:
                food.nutrition = 0  # if digestion rate would bring food nutrition to less than or equal to 0, simply set it to 0

            nutrition_gain = (food_nutrition_cur - food.nutrition) * (self.digestion_efficiency / 100)
            waste_gain = (food_nutrition_cur - food.nutrition) - nutrition_gain

            self.hunger_cur -= nutrition_gain   # decreases food's nutrition loss from hunger

            self.update_urine(waste_gain)
            self.update_fecal(waste_gain)

            if food.nutrition == 0:
                self.weight -= food.weight  # when food's nutrition is zero, remove it's weight from stomach, set food to destroyed and remove it
                food.is_destroyed = True    # from stomach contenta as food is fully digested and no longer exists in the stomach
                self.contents.remove(food)

    def defecate(self):
        poop = Poop(self.world, self.body.world_movement.x_center, self.body.world_movement.y_center)
        self.world.waste_container.append(poop)
        self.fecal_cur = 0

    def urinate(self):

        pass

# ----------------------------------------------------------------------------------------------------------------------
#   Display Functions

    def display_values_full(self):

        self.display_values()
        self.display_hunger_values_full
        self.stats.display_values()

    def display_hunger_values_full(self):
        self.display_hunger_values()
        self.display_waste_values()

    def display_waste_values(self):

        print("Urine: " + str(self.urine_cur) + "/" + str(self.urine_max))
        print("Fecal: " + str(self.fecal_cur) + "/" + str(self.fecal_max))

    def display_hunger_values(self):

        print("Hunger: " + str(self.hunger_cur) + "/" + str(self.hunger_max))
        print("Is Hungry: " + str(self.is_hungry))
        print("Is Starving: " + str(self.is_starving))
        print("Contents: " + str(self.contents))
        print("Digestion Rate: " + str(self.digestion_rate))

    def display_values(self):

        print("S T O M A C H")
        print("Type: " + str(self.type))
        print("Weight: " + str(self.weight))

# ----------------------------------------------------------------------------------------------------------------------
#   Update Functions

    def update_urine(self, waste_gain):
        if self.urine_cur + waste_gain >= self.urine_max:
            self.urine_cur += self.urine_max
            self.urinate()
        else:
            self.urine_cur += waste_gain

    def update_fecal(self, waste_gain):
        if self.fecal_cur + waste_gain >= self.fecal_max:
            self.fecal_cur += self.fecal_max
            self.defecate()
        else:
            self.fecal_cur += waste_gain

    def update_is_hungry(self):

        if self.hunger_cur >= self.hunger_threshold:
            self.is_hungry = True
        else:
            self.is_hungry = False

    def update_hunger_cur(self):

        if self.hunger_cur >= self.hunger_max:
            self.hunger_cur = self.hunger_max
            self.is_starving = True
        else:
            self.hunger_cur += self.hunger_rate
            self.is_starving = False
        # digest food if any in stomach
        if len(self.contents) > 0:
            self.digest_food()

    def update(self):

        self.update_hunger_cur()
        self.update_is_hungry()

