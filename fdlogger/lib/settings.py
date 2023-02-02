"""Settings Dialog Class"""

import logging
import os
import pkgutil
from pathlib import Path
from json import dumps, loads
from PyQt5 import QtWidgets, uic


class Settings(QtWidgets.QDialog):
    """Settings dialog"""

    def __init__(self, parent=None):
        """initialize dialog"""
        super().__init__(parent)
        self.logger = logging.getLogger("__name__")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            datefmt="%H:%M:%S",
            fmt="[%(asctime)s] %(levelname)s %(module)s - %(funcName)s Line %(lineno)d:\n%(message)s",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if Path("./debug").exists():
            # if True:
            self.logger.setLevel(logging.DEBUG)
            print("debugging on")
        else:
            self.logger.setLevel(self.logger.warning)
        self.working_path = os.path.dirname(
            pkgutil.get_loader("fdlogger").get_filename()
        )
        data_path = self.working_path + "/data/settings.ui"
        uic.loadUi(data_path, self)
        self.buttonBox.accepted.connect(self.save_changes)
        self.preference = None
        self.setup()

    def setup(self):
        """setup dialog"""
        with open("./fd_preferences.json", "rt", encoding="utf-8") as file_descriptor:
            self.preference = loads(file_descriptor.read())
            self.logger.info("reading: %s", self.preference)
            self.useqrz_radioButton.setChecked(bool(self.preference.get("useqrz")))
            self.usehamdb_radioButton.setChecked(bool(self.preference.get("usehamdb")))
            self.usehamqth_radioButton.setChecked(
                bool(self.preference.get("usehamqth"))
            )
            self.lookup_user_name_field.setText(
                self.preference.get("lookupusername")
                if self.preference.get("lookupusername")
                else ""
            )
            self.lookup_password_field.setText(
                self.preference.get("lookuppassword")
                if self.preference.get("lookuppassword")
                else ""
            )
            self.cloudlogapi_field.setText(
                self.preference.get("cloudlogapi")
                if self.preference.get("cloudlogapi")
                else ""
            )
            self.cloudlogurl_field.setText(
                self.preference.get("cloudlogurl")
                if self.preference.get("cloudlogurl")
                else ""
            )
            self.rigcontrolip_field.setText(
                self.preference.get("CAT_ip") if self.preference.get("CAT_ip") else ""
            )
            self.rigcontrolport_field.setText(
                str(
                    self.preference.get("CAT_port")
                    if self.preference.get("CAT_port")
                    else ""
                )
            )
            self.usecloudlog_checkBox.setChecked(bool(self.preference.get("cloudlog")))
            self.userigctld_radioButton.setChecked(
                bool(self.preference.get("userigctld"))
            )
            self.useflrig_radioButton.setChecked(bool(self.preference.get("useflrig")))
            self.markerfile_field.setText(
                self.preference.get("markerfile")
                if self.preference.get("markerfile")
                else ""
            )
            self.generatemarker_checkbox.setChecked(
                bool(self.preference.get("usemarker"))
            )
            self.cwip_field.setText(
                self.preference.get("cwip") if self.preference.get("cwip") else ""
            )
            self.cwport_field.setText(
                str(
                    self.preference.get("cwport")
                    if self.preference.get("cwport")
                    else ""
                )
            )
            self.usecwdaemon_radioButton.setChecked(
                bool(self.preference.get("cwtype") == 1)
            )
            self.usepywinkeyer_radioButton.setChecked(
                bool(self.preference.get("cwtype") == 2)
            )
            self.connect_to_server.setChecked(bool(self.preference.get("useserver")))
            self.multicast_group.setText(
                self.preference.get("multicast_group")
                if self.preference.get("multicast_group")
                else ""
            )
            self.multicast_port.setText(
                str(
                    self.preference.get("multicast_port")
                    if self.preference.get("multicast_port")
                    else ""
                )
            )
            self.interface_ip.setText(
                self.preference.get("interface_ip")
                if self.preference.get("interface_ip")
                else ""
            )

            self.send_n1mm_packets.setChecked(
                bool(self.preference.get("send_n1mm_packets"))
            )
            self.n1mm_station_name.setText(
                self.preference.get("n1mm_station_name")
                if self.preference.get("n1mm_station_name")
                else ""
            )
            self.n1mm_operator.setText(
                self.preference.get("n1mm_operator")
                if self.preference.get("n1mm_operator")
                else ""
            )
            self.n1mm_ip.setText(
                self.preference.get("n1mm_ip") if self.preference.get("n1mm_ip") else ""
            )
            self.n1mm_radioport.setText(
                str(self.preference.get("n1mm_radioport"))
                if self.preference.get("n1mm_radioport")
                else ""
            )
            self.n1mm_contactport.setText(
                str(self.preference.get("n1mm_contactport"))
                if self.preference.get("n1mm_contactport")
                else ""
            )
            self.n1mm_lookupport.setText(
                str(self.preference.get("n1mm_lookupport"))
                if self.preference.get("n1mm_lookupport")
                else ""
            )
            self.n1mm_scoreport.setText(
                str(self.preference.get("n1mm_scoreport"))
                if self.preference.get("n1mm_scoreport")
                else ""
            )

    def save_changes(self):
        """
        Write preferences to json file.
        """

        self.preference["useqrz"] = self.useqrz_radioButton.isChecked()
        self.preference["usehamdb"] = self.usehamdb_radioButton.isChecked()
        self.preference["usehamqth"] = self.usehamqth_radioButton.isChecked()
        self.preference["lookupusername"] = self.lookup_user_name_field.text()
        self.preference["lookuppassword"] = self.lookup_password_field.text()
        self.preference["cloudlog"] = self.usecloudlog_checkBox.isChecked()
        self.preference["cloudlogapi"] = self.cloudlogapi_field.text()
        self.preference["cloudlogurl"] = self.cloudlogurl_field.text()
        self.preference["CAT_ip"] = self.rigcontrolip_field.text()
        self.preference["CAT_port"] = int(self.rigcontrolport_field.text())
        self.preference["userigctld"] = self.userigctld_radioButton.isChecked()
        self.preference["useflrig"] = self.useflrig_radioButton.isChecked()
        self.preference["markerfile"] = self.markerfile_field.text()
        self.preference["usemarker"] = self.generatemarker_checkbox.isChecked()
        self.preference["cwip"] = self.cwip_field.text()
        self.preference["cwport"] = int(self.cwport_field.text())
        self.preference["cwtype"] = 0
        if self.usecwdaemon_radioButton.isChecked():
            self.preference["cwtype"] = 1
        if self.usepywinkeyer_radioButton.isChecked():
            self.preference["cwtype"] = 2
        self.preference["useserver"] = self.connect_to_server.isChecked()
        self.preference["multicast_group"] = self.multicast_group.text()
        self.preference["multicast_port"] = self.multicast_port.text()
        self.preference["interface_ip"] = self.interface_ip.text()

        self.preference["send_n1mm_packets"] = self.send_n1mm_packets.isChecked()
        self.preference["n1mm_station_name"] = self.n1mm_station_name.text()
        self.preference["n1mm_operator"] = self.n1mm_operator.text()
        self.preference["n1mm_ip"] = self.n1mm_ip.text()
        self.preference["n1mm_radioport"] = self.n1mm_radioport.text()
        self.preference["n1mm_contactport"] = self.n1mm_contactport.text()
        self.preference["n1mm_lookupport"] = self.n1mm_lookupport.text()
        self.preference["n1mm_scoreport"] = self.n1mm_scoreport.text()

        try:
            self.logger.info("save_changes:")
            with open(
                "./fd_preferences.json", "wt", encoding="utf-8"
            ) as file_descriptor:
                file_descriptor.write(dumps(self.preference, indent=4))
                self.logger.info("writing: %s", self.preference)
        except IOError as exception:
            self.logger.critical("save_changes: %s", exception)
