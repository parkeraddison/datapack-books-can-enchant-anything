# Books Can Enchant Anything

A Minecraft data pack that lets any enchantment be applied to any item via enchanted book and anvil (or the `/enchant` command). Enchanting tables retain their vanilla behavior.

This means you can finally place Unbreaking on a flint and steel, Fire Aspect on a shovel, or Aqua Affinity on a mob head. Or more useful combinations, of course.

## How it works

Works by overriding every vanilla enchantment's `supported_items` attribute to a tag that contains every item in the game.

- `data/bcea/tags/item/all.json`: an item tag listing every item ID in the game (except `air`).
- `data/minecraft/enchantment/*.json`: a full copy of each vanilla enchantment
  definition with only the `supported_items` field replaced with `#bcea:all`.
  Everything else (effects, costs, weights, slots, `primary_items`) is untouched,
  so enchanting-table behavior is unchanged, only anvil/`/enchant` restrictions
  are lifted.

## Installation

Drop this folder into your world's `datapacks/` directory (or a resource-pack-style
zip of it), then run `/reload` or restart the world.

> [!NOTE]
> The items and enchantments in this pack are compiled directly from the vanilla client jar, in this case for **version 26.2**. Therefore, this pack does not work out-of-the-box with other versions of Minecraft and/or modded clients.
>
> The next section explains how to update this pack for your desired version of Minecraft. In the future, perhaps I will automate this as a CI/CD workflow so that all of the recent Minecraft versions are supported with a pre-compiled release.

## Updating for a new Minecraft version

The list of items and enchantments comes directly from a vanilla (or modded) client jar. Two scripts are included to regenerate this pack's contents so it can be easily updated for a new game version.

The scripts require Python 3 and no additional dependencies. Run these commands from the root of this pack's folder, passing the path to a vanilla client jar as an argument:


```shell
python3 scripts/update_item_tag.py /path/to/client.jar
python3 scripts/update_enchantments.py /path/to/client.jar
```

**`update_item_tag.py`** rebuilds `data/bcea/tags/item/all.json` from the jar's `assets/minecraft/items/*.json` item model list (every real item has one; `air` is excluded on purpose).

**`update_enchantments.py`** rebuilds `data/minecraft/enchantment/*.json` by copying each enchantment straight from the jar, then only modifying `supported_items` (changed to `#bcea:all`) and `primary_items` (added, set to the enchantment's original vanilla `supported_items`, if the jar's copy doesn't already have one). This way enchanting tables still only show the vanilla list of available enchants, while anvil/`/enchant` becomes fully permissive. It also warns about any enchantment `.json` present in the pack but missing from the jar, in case an enchantment was removed upstream.
