import os
import json
import psutil
from datetime import datetime
from .wine_helpers.WineHelper import WineHelper


class Monitoring:
    def __init__(self, conf, log):
        self.conf = conf
        self.wine_helper = WineHelper()
        self._log = log

    # ==================================================================================== #
    #                                Helper Functions                                      #
    # ==================================================================================== #
    def read_file(self, file):
        with open(file, "r") as file:
            return json.load(file)

    def clean_files(self):
        for file in ["account_info.json", "symbol.json", "terminal_info"]:
            if os.path.exists(file):
                os.remove(file)

    def log(self, msg):
        json_data = {"msg": msg}
        self._log(msg, "lifecycle", json_data)

    # ==================================================================================== #
    #                               MT5 Functions                                          #
    # ==================================================================================== #
    def terminate_mt5(self, mt5_path_to_terminate):
        # Get a list of running processes
        process_list = list(psutil.process_iter(attrs=["pid", "name", "exe"]))
        terminated = False

        # Iterate through the list and get the executable location for each process
        for process in process_list:
            name = process.info["name"]
            if name == "terminal64.exe":
                process_obj = psutil.Process(process.info["pid"])
                cmdline = process_obj.cmdline()
                # print(name, ": ", cmdline[0])
                if mt5_path_to_terminate == cmdline[0]:
                    self.log("Terminating MT5")
                    process_obj.terminate()
                    terminated = True
        return terminated

    def mt5_is_terminal_init(self, terminal_path):
        return self.wine_helper.initialize(terminal_path)[0] == 200

    def mt5_init(self, terminal_path):
        is_initialized = self.mt5_is_terminal_init(terminal_path)
        while not is_initialized:
            self.log("MT5 is not initialized. Will init now.")
            self.mt5_login()
            is_initialized = self.mt5_is_terminal_init(terminal_path)
        return is_initialized

    def mt5_login(self):
        server = self.conf["server"]["title"]
        login = self.conf["login"]
        password = self.conf["password"]

        return not self.wine_helper.login(server, login, password)[1] == ""

    def mt5_get_account(self):
        account = self.wine_helper.account_info()
        if account[0] == 200:
            return self.read_file("account_info.json")
        else:
            self.log("Failed to get account")
            return None

    # ==================================================================================== #
    #                               DWX Functions                                          #
    # ==================================================================================== #
    def is_dwx_attached(self):
        print("DWX attached still not implemented")
        return True
        path = self.conf["MT5_directory_path"] + "DWX/Status_Time"
        with open(path, "r") as file:
            now = datetime.utcnow()
            date_format = "%Y.%m.%d %H:%M:%S"
            first_line = file.readline().rstrip("\n")
            # Convert the string to datetime
            date_object = datetime.strptime(first_line, date_format)

            diff = now - date_object
            if diff.seconds > 5:
                return False
            return True

    # ================================================================================ #
    #                                Health Check                                      #
    # ================================================================================ #
    def check_health(self, terminal_path):
        self.log("Checking the HEALTH of terminal")
        status = {}

        # ================================================================================ #
        # Reset Terminal Status
        # ================================================================================ #
        self.terminate_mt5(terminal_path)

        # ================================================================================ #
        # Initialize
        # ================================================================================ #
        logged_in = self.mt5_init(terminal_path)

        # ================================================================================ #
        # Get Terminal Info
        # ================================================================================ #

        terminal_info = self.read_file("terminal_info.json")

        status["terminal_info"] = terminal_info
        status["ea_trade_allowed"] = terminal_info["trade_allowed"]
        status["logged_in"] = logged_in
        status["account_info"] = "Failed to get account info"

        # ================================================================================ #
        # ================================================================================ #
        if logged_in:
            # Get Account Info
            account = self.mt5_get_account()
            status["account_info"] = account

        # ================================================================================ #
        # Check EA Status
        # ================================================================================ #
        status["dwx_attached"] = self.is_dwx_attached()

        # Remove the created json files
        self.clean_files()

        self.status = status
        self.log(json.dumps(self.status))
        return status
