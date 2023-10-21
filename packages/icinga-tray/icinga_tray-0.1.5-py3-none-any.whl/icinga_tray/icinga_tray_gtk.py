import icinga_tray.icinga_fetcher as icinga_fetcher
import json
import keyring
import sys
import webbrowser
from appdirs import user_config_dir
from os.path import join
from plyer import notification
from plyer.utils import platform
import importlib.resources
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, AppIndicator3, GObject

def get_data(resource):
    return str(importlib.resources.files("icinga_tray") / resource)


def send_notification(title, content, urgency):
    if platform == "win":
        ext = "ico"
    else:
        ext = "png"
    if urgency == "ok":
        icon = f"img/notification_ok.{ext}"
    elif urgency == "warn":
        icon = f"img/notification_warn.{ext}"
    elif urgency == "crit":
        icon = f"img/notification_crit.{ext}"
    else:
        icon = f"img/notification_unkown.{ext}"

    notification.notify(title=title, message=content, app_icon=get_data(icon))


def is_false(s):
    if s == "0" or s.lower() == "false" or s.lower() == "no":
        return True
    return False


class IcingaTrayIconGtk():
    def load_config(self):
        config_path = join(user_config_dir("icinga-tray", "icinga-tray"), "config.json")
        try:
            self.config = json.load(open(config_path))
        except FileNotFoundError:
            window = Gtk.Window()
            dialog = Gtk.MessageDialog(
                    transient_for=window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="No configuration found"
                    )
            dialog.format_secondary_text(
                    f"Please make sure that {config_path} exists!"
                    )
            dialog.run()
            exit()
        except json.decoder.JSONDecodeError:
            window = Gtk.Window()
            dialog = Gtk.MessageDialog(
                    transient_for=window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="No valid configuration found"
                    )
            dialog.format_secondary_text(
                    f"Please make sure that {config_path} is valid json!"
                    )
            dialog.run()
            exit()

        self.interval = 10000
        if "interval" in self.config:
            self.interval = self.config["interval"]
        self.fetcher = icinga_fetcher.IcingaFetcher(self.config)
        self.data = None

        if "ssl_verify" in self.config and is_false(self.config["ssl_verify"]):
            self.config["ssl_verify"] = False
        else:
            self.config["ssl_verify"] = True

        if "use_keyring" in self.config and is_false(self.config["use_keyring"]):
            self.config["use_keyring"] = False
        else:
            self.config["use_keyring"] = True

        self.notifications = True
        if "notifications" in self.config and is_false(self.config["notifications"]):
            self.notifications = False

    # def __init__(self):
        # self.app = QtWidgets.QApplication(sys.argv)

    def init_icon(self):
        print("INIT ICONS")
        # define icon paths
        self.ICON_OK_PATH = get_data("img/icinga_ok.png")
        self.ICON_WARN_PATH = get_data("img/icinga_warn.png")
        self.ICON_CRIT_PATH = get_data("img/icinga_crit.png")
        self.ICON_UNKNOWN_PATH = get_data("img/icinga_unknown.png")
        self.ICON_OFF_PATH = get_data("img/icinga_off.png")
        # define icons
        self.ICON_OK = Gtk.Image.new_from_file(self.ICON_OK_PATH)
        self.ICON_WARN = Gtk.Image.new_from_file(self.ICON_WARN_PATH)
        self.ICON_CRIT = Gtk.Image.new_from_file(self.ICON_CRIT_PATH)
        self.ICON_UNKNOWN = Gtk.Image.new_from_file(self.ICON_UNKNOWN_PATH)
        self.ICON_OFF = Gtk.Image.new_from_file(self.ICON_OFF_PATH)
        
        self.get_credentials()
        self.init_menu()
        
        self.indicator = AppIndicator3.Indicator.new(
                "Icinga Tray",
                self.ICON_OK_PATH,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
                )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)
        self.updateIcon()

    def init_menu(self):
        self.menu = Gtk.Menu()

        self.menu_entries = []
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)
        exit_action = Gtk.MenuItem(label="Exit")
        exit_action.connect("activate", quit)
        self.menu.append(exit_action)
        self.menu.show_all()
        self.DEFAULT_ITEMS = [sep, exit_action]

    def issue_notifications(self, data):
        """Check which states have changed and issue the corresponding
        notifications."""
        for lvl in ["ok", "warn", "crit", "unknown"]:
            for entry in self.data[lvl]:
                if entry not in data[lvl]:
                    if entry in data["ok"]:
                        send_notification(
                            f"OK: {entry}", data["ok"][entry]["msg"], "ok"
                        )
                    elif entry in data["warn"]:
                        send_notification(
                            f"WARN: {entry}", data["warn"][entry]["msg"], "warn"
                        )
                    elif entry in data["crit"]:
                        send_notification(
                            f"CRIT: {entry}", data["crit"][entry]["msg"], "crit"
                        )
                    elif entry in data["unknown"]:
                        send_notification(
                            f"CRIT: {entry}", data["unknown"][entry]["msg"], "unknown"
                        )

    def get_password_from_prompt(self):
        # """A wrapper to prompt for the password."""
        # self.fetcher.config["password"], ok = QtWidgets.QInputDialog().getText(
            # QtWidgets.QWidget(),
            # "Icinga-Tray",
            # "Password:",
            # echo=QtWidgets.QLineEdit.EchoMode.Password,
        # )
        return ok

    def get_credentials(self):
        """Get the correct credentials, check the system keyring first, if there
        is no entry/it is not working, prompt for password."""
        self.fetcher.config["password"] = None
        # fetch keyring and correct entry
        if self.config["use_keyring"]:
            keyring.get_keyring()
            if "keyring_backend" in self.config:
                if self.config["keyring_backend"] == "secretservice":
                    keyring.set_keyring(keyring.backends.SecretService.Keyring())
                    keyring.get_keyring()
            self.fetcher.config["password"] = keyring.get_password(
                "icinga-tray", self.config["user"]
            )

        # Test the stored password. if it does not work remove it and continue
        # To prompt
        if (
            self.fetcher.config["password"] is not None
            and self.fetcher.send_request("list/hosts") is None
        ):
            self.fetcher.config["password"] = None

        # if no (working) password was found, prompt for password until the user
        # enters a working one or presses cancel. If a working password is
        # entered, write to the system keyring
        if self.fetcher.config["password"] is None:
            ok = self.get_password_from_prompt()
            while self.fetcher.send_request("list/hosts") is None and ok:
                ok = self.get_password_from_prompt()
            if ok and self.config["use_keyring"]:
                keyring.set_password(
                    "icinga-tray", self.config["user"], self.fetcher.config["password"]
                )

    def clear_menu_actions(self):
        for entry in self.menu_entries+self.DEFAULT_ITEMS:
            self.menu.remove(entry)


        self.menu_entries = []

    def populate_menu(self, states):
        """Add all warnings to the menu"""
        self.clear_menu_actions()

        for state in ["unknown", "crit", "warn"]:
            if state == "unknown":
                icon = self.ICON_UNKNOWN
                desc = "Unknown"
            elif state == "crit":
                icon = self.ICON_CRIT
                desc = "Critical"
            else:
                icon = self.ICON_WARN
                desc = "Warning"

            if states[state] != 0:
                sep = Gtk.SeparatorMenuItem(label=desc)
                self.menu_entries.append(sep)

                for entry in self.data[state]:
                    item = Gtk.ImageMenuItem(
                            label=f'{entry}: {self.data[state][entry]["msg"]}'
                           )
                    item.set_image(icon)
                    url = self.data[state][entry]["url"]
                    item.connect("activate", lambda x, url=url: webbrowser.open(url))
                    self.menu_entries.append(item)

        if states["ignore"] != 0:
            self.menu_entries.append(Gtk.SeparatorMenuItem())
            ign = Gtk.MenuItem(label=f'services ignored: {states["ignore"]}')
            ign.set_sensitive(False)
            self.menu_entries.append(ign)
        for e in self.menu_entries+self.DEFAULT_ITEMS:
            print(f"add {e} to menu")
            self.menu.append(e)
        self.menu.show_all()

    def updateIcon(self):
        """periodically checks Icinga for the current status, update the icon
        and context menu."""
        data = self.fetcher.get_data()
        if not data or data is None:
            self.setIcon(self.ICON_OFF_PATH)
            if data is False:
                msg = "Can not connect to icinga"
            else:
                msg = "An error occured connecting to icinga"
            action = Gtk.ImageMenuItem(label=msg)
            action.set_image(self.ICON_OFF)
            self.menu_entries.append(action)
            self.menu.append(action)
        else:

            if self.data == data:
                return

            if self.data is not None and self.notifications is True:
                self.issue_notifications(data)

            self.data = data
            icon = self.ICON_OK_PATH
            states = {k: len(data[k]) for k in data}

            # set Icon According to highest level
            if states["unknown"] != 0:
                icon = self.ICON_UNKNOWN_PATH
            elif states["crit"] != 0:
                icon = self.ICON_CRIT_PATH
            elif states["warn"] != 0:
                icon = self.ICON_WARN_PATH

            self.populate_menu(states)
            self.setIcon(icon)
            self.updateToolTip(states)
    
    def updateToolTip(self, states):
        """write the current count for ok/warn/crit into the tooltip"""
        tip = []
        for s in ["ok", "warn", "crit"]:
            if states[s] != 0:
                tip.append(f"{s}: {states[s]}")
        if states["ignore"] > 0:
            tip.append(f'({states["ignore"]})')
        self.indicator.set_title(", ".join(tip))

    def startclocktimer(self):
        GObject.timeout_add(self.interval, self.updateIcon())

    def exit(self):
        Gtk.main_quit()

    def setIcon(self, icon):
        print(f'SET ICON: {icon}')
        print(self.indicator)
        self.indicator.set_icon(icon)

    def main(self):
        self.load_config()
        self.init_icon()
        Gtk.main()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    IcingaTrayIcon().main()
