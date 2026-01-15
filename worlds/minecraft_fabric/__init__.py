import math
from typing import Mapping, Any

from BaseClasses import ItemClassification, Item
from worlds.AutoWorld import World
from worlds.minecraft_fabric.item_filler import create_items
from worlds.minecraft_fabric.items import item_table, end_index, traps_index, filler_index, bl_progression_index, \
    useful_index
from worlds.minecraft_fabric.locations import location_table
from worlds.minecraft_fabric.options import FMCOptions
from worlds.minecraft_fabric.region import create_regions, connect_entrances


class FabricMinecraftWorld(World):
    game = "Minecraft Fabric"
    options_dataclass = FMCOptions
    options: FMCOptions
    topology_present = True

    item_name_to_id = {
        item.name: item.item_id for item in item_table
    }

    location_name_to_id = location_table


    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    def create_regions(self):
        create_regions(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        from Utils import visualize_regions
        state = self.multiworld.get_all_state()
        state.update_reachable_regions(self.player)

        reachable_regions = state.reachable_regions[self.player]
        unreachable_regions: set[Region] = set()  # type: ignore
        for regionb in self.multiworld.regions:
            if regionb not in reachable_regions:
                unreachable_regions.add(regionb)

        visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml", show_entrance_names=True,
                          regions_to_highlight=unreachable_regions)

        return {
            "randomize_swim": self.options.randomize_swim.value,
            "randomize_sprint": self.options.randomize_sprint.value
        }

    def connect_entrances(self) -> None:
        connect_entrances(self)

    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        create_items(self)
