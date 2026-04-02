from endstone           import ColorFormat
from endstone.boss      import BarColor, BossBar, BarStyle
from endstone.command   import Command, CommandSender
from endstone.plugin    import Plugin

class Bossbar(Plugin):
    api_version = "0.11"

    commands = {
        "bossbar-add": {
            "description": "Creates a boss bar.",
            "usages": ["/bossbar-add <id: str> <name: str>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-color": {
            "description": "Sets the color for a boss bar.",
            "usages": ["/bossbar-color <id: str> (pink|blue|red|green|yellow|purple|rebecca_purple|white)<color: BarColor>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-get": {
            "description": "Gets a boss bar.",
            "usages": ["/bossbar-get <id: str> (players|value|visible)[value: BossProperty]"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-list": {
            "description": "Lists all boss bars.",
            "usages": ["/bossbar-list"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-name": {
            "description": "Sets the name for a boss bar.",
            "usages": ["/bossbar-name <id: str> <name: json>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-players": {
            "description": "Sets the player(s) for a boss bar.",
            "usages": ["/bossbar-players <id: str> <targets: target>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-remove": {
            "description": "Removes a boss bar.",
            "usages": ["/bossbar-remove <id: str>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-style": {
            "description": "Sets the style for a boss bar.",
            "usages": ["/bossbar-style <id: str> (solid|segmented_6|segmented_10|segmented_12|segmented_20)<style: BarStyle>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-value": {
            "description": "Sets the value for a boss bar. (0-100)",
            "usages": ["/bossbar-value <id: str> <value: int>"],
            "permissions": ["bossbar.command.bossbar"]
        },
        "bossbar-visible": {
            "description": "Sets the visibility for a boss bar.",
            "usages": ["/bossbar-visible <id: str> <visible: bool>"],
            "permissions": ["bossbar.command.bossbar"]
        },
    }

    permissions = {
        "bossbar.command.bossbar": {
            "description": "Allows users to use the /bossbar command.",
            "default": "op"
        }
    }

    _bossbars: dict[str, BossBar] = {}

    def _resolve_id(self, raw: str) -> str:
        return raw if ":" in raw else f"minecraft:{raw}"

    def _get_bar(self, sender: CommandSender, bar_id: str) -> BossBar | None:
        bar = self._bossbars.get(bar_id)

        if bar is None:
            sender.send_message(f"{ColorFormat.RED}Boss bar '{bar_id}' does not exist.")
        return bar

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        name = command.name

        if name == "bossbar-add":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-add <id> <name>")
                return False

            bar_id      = self._resolve_id(args[0])
            bar_name    = " ".join(args[1:])

            if bar_id in self._bossbars:
                sender.send_message(f"{ColorFormat.RED}A boss bar with id '{bar_id}' already exists.")
                return False

            bar                     = self.server.create_boss_bar(bar_name, BarColor.WHITE, BarStyle.SOLID)
            self._bossbars[bar_id]  = bar

            sender.send_message(f"{ColorFormat.GREEN}Created boss bar [{bar_id}].")

        elif name == "bossbar-color":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-color <id> <color>.")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            color_map = {
                "pink":             BarColor.PINK,
                "blue":             BarColor.BLUE,
                "red":              BarColor.RED,
                "green":            BarColor.GREEN,
                "yellow":           BarColor.YELLOW,
                "purple":           BarColor.PURPLE,
                "rebecca_purple":   BarColor.REBECCA_PURPLE,
                "white":            BarColor.WHITE,
            }

            color = color_map.get(args[1].lower())

            if color is None:
                sender.send_message(f"{ColorFormat.RED}Unknown color '{args[1]}'. Valid: {', '.join(color_map)}")
                return False

            bar.color = color

            sender.send_message(f"{ColorFormat.GREEN}Set color of [{bar_id}] to {args[1]}.")

        elif name == "bossbar-get":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-get <id> <players|value|visible>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            prop = args[1].lower()

            if prop == "value":
                sender.send_message(f"{ColorFormat.GREEN}Boss bar [{bar_id}] value: {int(bar.progress * 100)}")
            elif prop == "visible":
                sender.send_message(f"{ColorFormat.GREEN}Boss bar [{bar_id}] visible: {bar.is_visible}")
            elif prop == "players":
                names = [p.name for p in bar.players]
                sender.send_message(f"{ColorFormat.GREEN}Boss bar [{bar_id}] players: {', '.join(names) if names else 'none'}")
            else:
                sender.send_message(f"{ColorFormat.RED}Valid properties: players, value, visible")
                return False

        elif name == "bossbar-list":
            if not self._bossbars:
                sender.send_message(f"{ColorFormat.GRAY}There are no boss bars.")
            else:
                ids = ", ".join(self._bossbars.keys())
                sender.send_message(f"{ColorFormat.GREEN}There are {len(self._bossbars)} boss bar(s): {ids}")

        elif name == "bossbar-name":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-name <id> <name>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            bar_name    = " ".join(args[1:])
            bar.title   = bar_name

            sender.send_message(f"{ColorFormat.GREEN}Updated name of boss bar [{bar_id}] to '{bar_name}'.")

        elif name == "bossbar-players":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-players <id> <targets>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            targets = args[1:]
            online  = {p.name: p for p in self.server.online_players}

            bar.remove_all()

            added = []

            for t in targets:
                player = online.get(t)

                if player:
                    bar.add_player(player)
                    added.append(t)

            sender.send_message(f"{ColorFormat.GREEN}Set players of [{bar_id}] to: {', '.join(added) if added else 'none'}.")

        elif name == "bossbar-remove":
            if len(args) < 1:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-remove <id>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            bar.remove_all()
            del self._bossbars[bar_id]

            sender.send_message(f"{ColorFormat.GREEN}Removed boss bar [{bar_id}].")

        elif name == "bossbar-style":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-style <id> <style>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            style_map   = { "solid": BarStyle.SOLID, "segmented_6": BarStyle.SEGMENTED_6, "segmented_10": BarStyle.SEGMENTED_10, "segmented_12": BarStyle.SEGMENTED_12, "segmented_20": BarStyle.SEGMENTED_20 }
            style       = style_map.get(args[1].lower())

            if style is None:
                sender.send_message(f"{ColorFormat.RED}Unknown style '{args[1]}'. Valid: {', '.join(style_map)}")
                return False

            bar.style = style

            sender.send_message(f"{ColorFormat.GREEN}Set style of [{bar_id}] to {args[1]}.")

        elif name == "bossbar-value":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-value <id> <value>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            try:
                value = int(args[1])

                if not (0 <= value <= 100):
                    raise ValueError
            except ValueError:
                sender.send_message(f"{ColorFormat.RED}Value must be an integer between 0 and 100.")
                return False

            bar.progress = float(value / 100)

            sender.send_message(f"{ColorFormat.GREEN}Set value of [{bar_id}] to {value}.")

        elif name == "bossbar-visible":
            if len(args) < 2:
                sender.send_message(f"{ColorFormat.RED}Usage: /bossbar-visible <id> <true|false>")
                return False

            bar_id  = self._resolve_id(args[0])
            bar     = self._get_bar(sender, bar_id)

            if bar is None:
                return False

            if args[1].lower() not in ("true", "false"):
                sender.send_message(f"{ColorFormat.RED}Visible must be 'true' or 'false'.")
                return False

            bar.is_visible = args[1].lower() == "true"

            sender.send_message(f"{ColorFormat.GREEN}Set visibility of [{bar_id}] to {args[1].lower()}.")

        return True

    def on_load(self) -> None:
        self.logger.info("on_load")

    def on_enable(self) -> None:
        self.logger.info("on_enable")

    def on_disable(self) -> None:
        self.logger.info("on_disable")