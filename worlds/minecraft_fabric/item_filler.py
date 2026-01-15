import math

from BaseClasses import Item
from worlds.minecraft_fabric import bl_progression_index, useful_index, traps_index, item_table


def create_items(self):
    total_items = len(self.multiworld.get_unfilled_locations(self.player))

    # Progression Items ############################################################################################

    if self.options.randomize_swim:
        total_items = self.add_to_pool(0, total_items)
    if self.options.randomize_sprint:
        total_items = self.add_to_pool(1, total_items)

    progressive_index = 2

    # Progressive Tools
    total_items = self.add_multiple_to_pool(progressive_index, 4, total_items)
    # Progressive Weapons
    total_items = self.add_multiple_to_pool(progressive_index + 1, 4, total_items)
    # Progressive Smelting
    total_items = self.add_multiple_to_pool(progressive_index + 2, 2, total_items)
    # Progressive Armor
    total_items = self.add_multiple_to_pool(progressive_index + 3, 5, total_items)
    # Progressive Archery
    total_items = self.add_multiple_to_pool(progressive_index + 4, 2, total_items)

    # Single Check Progressive Items
    for i in range(bl_progression_index + 1, useful_index + 1):
        total_items = self.add_to_pool(i, total_items)

    # Trap Items ###################################################################################################
    trap_weights = []
    trap_weights += self.add_trap_weight(traps_index + 1, self.options.reverseControlsTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 2, self.options.invertedMouseTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 3, self.options.iceTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 4, self.options.randomEffectTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 5, self.options.stunTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 6, self.options.tntTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 7, self.options.teleportTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 8, self.options.beeTrapWeight)
    trap_weights += self.add_trap_weight(traps_index + 9, self.options.literatureTrapWeight)
    trap_count = 0 if (len(trap_weights) == 0) else math.ceil(
        total_items * (self.options.trap_fill_percentage.value / 100.0))

    for i in range(trap_count):
        trap_item = self.random.choice(trap_weights)
        self.multiworld.itempool.append(Item(trap_item.name, trap_item.item_type, trap_item.item_id, self.player))
        total_items -= 1

    # Filler Items #####################################################################################################
    while total_items > 0:
        total_items = self.add_to_pool(self.random.randint(useful_index + 1, traps_index), total_items)



def add_multiple_to_pool(self, index: int, count: int, total_items: int):
    for i in range(count):
        total_items = self.add_to_pool(index, total_items)
    return total_items

def add_to_pool(self, index: int, total_items: int):
    self.multiworld.itempool.append(
        Item(item_table[index].name, item_table[index].item_type, item_table[index].item_id, self.player)
    )
    total_items -= 1
    return total_items

def add_trap_weight(self, index, weight):
    return [item_table[index]] * weight