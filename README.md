# endstone-bossbar

A plugin that brings the `/bossbar` command to Endstone servers.

## Installation

1. Download the latest release
2. Place it in your server's `plugins` directory
3. Restart your server

## Commands

| Command | Description |
|---|---|
| `/bossbar-add <id> <name>` | Creates a new boss bar |
| `/bossbar-remove <id>` | Removes a boss bar |
| `/bossbar-name <id> <name>` | Sets the name of a boss bar |
| `/bossbar-color <id> <color>` | Sets the color (`pink`, `blue`, `red`, `green`, `yellow`, `purple`, `rebecca_purple`, `white`) |
| `/bossbar-style <id> <style>` | Sets the style (`solid`, `segmented_6`, `segmented_10`, `segmented_12`, `segmented_20`) |
| `/bossbar-value <id> <value>` | Sets the fill value (0–100) |
| `/bossbar-visible <id> <true\|false>` | Shows or hides a boss bar |
| `/bossbar-players <id> <targets>` | Sets which players see a boss bar |
| `/bossbar-get <id> <players\|value\|visible>` | Gets a property of a boss bar |
| `/bossbar-list` | Lists all active boss bars |

## Example
```text
/bossbar-add event:raid Raid
/bossbar-color event:raid red
/bossbar-style event:raid segmented_10
/bossbar-value event:raid 100
/bossbar-players event:raid @a
/bossbar-visible event:raid true
```

## Support

For issues or questions, open an issue on GitHub or find me on Endstone's Discord - @sprixvy.
