import os
import json
import shutil
from time import sleep
import pandas as pd
from datetime import datetime, timedelta

from ..DB import DB
from ..tg_send import tg_send
from .dwx_client import dwx_client
from ..Monitoring import Monitoring
from .equity.s3 import upload_files_to_s3
from ..wine_helpers.WineHelper import wine_helper
from .equity.calculate_equity import calculate_equity
from .equity.load_and_concat_data import load_and_concat_data

from ..logger_opensearch import LoggerOpenSearch


class Base:
    def __init__(
        self,
        USER,
        conf=None,
        use_dynamo=True,
        table_name=None,
        region_name="us-east-2",
        inform=True,
        should_update_equity=False,
        min_days=30,
        is_mt5=True,
    ):
        self.reset_data_folder()
        self.should_update_equity = should_update_equity
        self.data = {}
        self.USER = USER
        self.inform = inform
        self.wine_helper = wine_helper
        self.is_mt5 = is_mt5

        if conf is not None:
            self.conf = conf
        if use_dynamo:
            self.conf = DB(table_name, region_name).get_DB_settings_for_user(USER)
        if self.conf is None:
            raise ValueError("Could not load a proper conf file")

        if "open_search_host" in self.conf:
            if self.conf["open_search_host"] != "":
                self.logger = LoggerOpenSearch(
                    self.conf["open_search_host"], self.conf["open_search_region"]
                )

        self.assets = self.conf["assets"]
        self.min_days = min_days

    def init(self):
        if self.is_mt5:
            self.healthy = self.check_health()
        else:
            self.healthy = True

        if self.healthy:
            self.dwx = dwx_client(
                self,
                self.conf["MT5_directory_path"],
                0.005,  # sleep_delay
                10,  # max_retry_command_seconds
                verbose=False,
            )
            self.reset_dwx()

            self.connect_to_terminal()
            if self.is_mt5:
                self.get_contracts()

            self.request_historical_ohlc(days=self.min_days)

            while True:
                sleep(1)

    def reset_data_folder(self):
        folder_path = "./data"  # Replace with the actual path of the folder

        # Remove the folder and its contents
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            # print(f"Folder '{folder_path}' and its contents have been removed.")

        # Recreate the folder
        os.makedirs(folder_path)
        # print(f"Folder '{folder_path}' has been recreated.")

    def reset_dwx(self):
        self.dwx.subscribe_symbols_bar_data([])

    def connect_to_terminal(self):
        self.dwx.start()
        # Second sleep is needed to give it time to reload the keys
        sleep(1)

        self.completed_initial_load = False

    def get_terminal_path(self):
        original_path = self.conf["MT5_directory_path"]
        components = original_path.split("/")
        path = "/".join(components[:-3])
        path = path + "/terminal64.exe"
        return path

    def check_health(self):
        self.monitor = Monitoring(self.conf, self.log)
        health = self.monitor.check_health(self.get_terminal_path())

        if not health["ea_trade_allowed"]:
            print("EA Trade is not allowed")
            tg_send("ERROR: EA Trade is not allowed", conf)
            return False

        if not health["dwx_attached"]:
            print("DWX is not attached to chart")
            tg_send("ERROR: DWX is not attached", conf)
            return False

        return True

    # ===================================================================== #
    #                            Event Methods                           #
    # ===================================================================== #
    def request_historic_trades(self):
        if self.healthy:
            self.dwx.get_historic_trades(1000)
        else:
            print("System is not in healthy state")

    def subscribe_to_contracts_tick(self):
        print(self.contracts)
        print([sym[0] for sym in self.contracts])
        if self.healthy:
            self.dwx.subscribe_symbols([sym[0] for sym in self.contracts])
        else:
            print("System is not in healthy state")

    def subscribe_to_contracts_ohlc(self):
        if self.healthy:
            self.dwx.subscribe_symbols_bar_data(self.contracts)
        else:
            print("System is not in healthy state")

    # ===================================================================== #
    #                            Contract Methods                           #
    # ===================================================================== #

    def read_file(self, file):
        with open(file, "r") as file:
            return json.load(file)

    def get_contract_for_symbol(self, symbol):
        response = wine_helper.get_symbol(symbol)
        if response[0] == 200:
            data = self.read_file("symbol.json")
            return data["name"]

    def get_contracts(self):
        contracts_loaded = False
        contracts = []

        while not contracts_loaded:
            for asset in self.conf["assets"]:
                response = wine_helper.get_symbol(asset["title"])
                if response[0] == 200:
                    data = self.read_file("symbol.json")
                    timeframe = self.wine_helper.get_mt5_timeframe(asset["timeframe"])
                    contracts.append([data["name"], timeframe])

            self.contracts = contracts
            if len(self.contracts) != len(self.conf["assets"]):
                self.log("Failed to load all contracts")
            else:
                self.log("All contracts loaded")
                contracts_loaded = True
            sleep(1)

        json_data = {"msg": f"Monitored Contracts: {self.contracts}"}
        self.log(json_data["msg"], "lifecycle", json_data)
        return contracts

    # ===================================================================== #
    #                              Data Methods                             #
    # ===================================================================== #
    def log(self, msg=None, os_table=None, os_json_data=None):
        if msg is not None:
            tg_send(msg, self.conf)
        if self.logger is not None:
            if os_table is not None:
                if os_json_data is not None:
                    os_json_data["user"] = self.USER
                    self.logger.log(os_table, os_json_data)

    def on_message(self, message):
        if message["type"] == "ERROR":
            msg = (
                message["type"],
                "|",
                message["error_type"],
                "|",
                message["description"],
            )
            if self.inform:
                self.log(msg)
        elif message["type"] == "INFO":
            print(message["type"], "|", message["message"])

    # ===================================================================== #
    #                              OHLC Methods                             #
    # ===================================================================== #
    def request_historical_ohlc(self, days=30):
        for asset in self.contracts:
            self.request_single_historical_ohlc(asset, days=days)

    def request_single_historical_ohlc(self, asset, days=30):
        end = datetime.now()
        start = end - timedelta(days=days)  # last 30 days
        self.dwx.get_historic_data(
            asset[0],
            asset[1],
            start.timestamp(),
            end.timestamp(),
        )

    # ===================================================================== #
    #                              TRADE Methods                            #
    # ===================================================================== #
    def on_order_event(self):
        self.dwx.open_orders

    # ===================================================================== #
    #                              Storage Methods                            #
    # ===================================================================== #
    def on_historic_trades(self):
        print("On Historic Trades")
        trades = self.dwx.historic_trades.copy()
        trades = pd.DataFrame.from_dict(trades, orient="index")
        user = self.conf["user"]
        trades.to_parquet(f"./data/{user}_trades.parquet")
        self.historical_trades = trades
        self.event_historic_trades()

    def on_historic_data(self, symbol, time_frame, new_data):
        print("HIST DATA | ", symbol, time_frame, f"{datetime.now()}")

        data = pd.DataFrame.from_dict(new_data, orient="index")
        data.index = pd.to_datetime(data.index, format="%Y.%m.%d %H:%M")
        user = self.conf["user"]
        DATA_FILE = f"data/{user}_{symbol}-{time_frame}.parquet"
        load_and_concat_data(data, DATA_FILE)

        if os.path.exists(DATA_FILE):
            # Execution methods
            self.data[f"{symbol}-{time_frame}"] = pd.read_parquet(DATA_FILE)

        else:
            self.log(
                msg=f"File {DATA_FILE} does not exist in loading historic data for {symbol}-{time_frame}",
                os_table="errors",
                os_json_data={
                    "msg": f"File {DATA_FILE} does not exist in loading historic data for {symbol}-{time_frame}"
                },
            )

    def on_bar_data(
        self, symbol, timeframe, time, open_price, high, low, close_price, tick_volume
    ):
        print("==================================")
        print("NEW BAR | ", symbol, timeframe, datetime.utcnow(), time)
        name = f"{symbol}-{timeframe}"

        if name in self.data.keys():
            newdf = pd.DataFrame(
                {
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "close": close_price,
                    "tick_volume": tick_volume,
                },
                index=[time],
            )

            newdf.index = pd.to_datetime(newdf.index, format="%Y.%m.%d %H:%M")

            # Concatenate the dataframes
            df = pd.concat([self.data[name], newdf])
            duplicated_index = df.index.duplicated(keep="last")
            df = df[~duplicated_index]
            self.data[name] = df

            # save the dataframe
            user = self.conf["user"]
            DATA_FILE = f"data/{user}_{symbol}-{timeframe}.parquet"
            self.data[name].to_parquet(DATA_FILE, index=True)

            # Execute the user specified function
            self.event_new_bar(symbol, timeframe, df)

            if self.should_update_equity:
                self.update_equity()
        else:
            print(f"{name} not in self.data.keys()")
            self.log(
                os_table="errors",
                os_json_data={"msg": f"{name} not in self.data.keys()"},
            )

    def on_tick(self, symbol, bid, ask):
        now = datetime.utcnow()

    # ===================================================================== #
    #                              Equity Related Methods                   #
    # ===================================================================== #
    def update_equity(self):
        print("updating equity")
        user = self.conf["user"]
        for asset in self.contracts:
            trades = pd.read_parquet(f"./data/{user}_trades.parquet")
            data = pd.read_parquet(f"./data/{user}_{asset[0]}-{asset[1]}.parquet")
            equity = calculate_equity(trades, data)
            equity.to_parquet(f"./data/{user}_{asset[0]}-{asset[1]}_equity.parquet")
        upload_files_to_s3()

    # ===================================================================== #
    #                              Methods to override                            #
    # ===================================================================== #
    def event_historic_trades(self):
        print("Historic Trades fetched")
        print(self.historical_trades)

    def event_new_bar(self):
        print("New Bar Data fetched")
