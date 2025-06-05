import threading
import time

from passive_equipment.handler_passive import HandlerPassive
from socket_cyg.socket_client import SocketClient


class HuaRunWei(HandlerPassive):

    def __init__(self):
        super().__init__(open_flag=True)

        self.scan_place_nut = SocketClient("192.168.0.151", 51236)
        self.scan_flatten = SocketClient("192.168.0.152", 51236)
        self.scan_check = SocketClient("192.168.0.153", 51236)

        self.monitor_scan_thread()

    def monitor_scan_thread(self):
        """监控扫码枪是否断连的线程."""

        def _monitor_scan():
            while True:
                if not self.scan_place_nut.is_connected:
                    self.scan_place_nut.connect()

                if not self.scan_flatten.is_connected:
                    self.scan_flatten.connect()

                if not self.scan_check.is_connected:
                    self.scan_check.connect()
                time.sleep(10)

        threading.Thread(target=_monitor_scan).start()

    def scan_data_logic(self, call_back: dict):
        """控制扫码枪进行扫码.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        dv_name = call_back.get("dv_name")
        self.logger.info("正在执行 %s 函数", call_back["operation_func"])
        if "nut" in dv_name:
            self.scan_place_nut.send_data("T".encode("utf-8"))
            data = self.scan_place_nut.socket.recv(1024)
        elif "flatten" in dv_name:
            self.scan_flatten.send_data("T".encode("utf-8"))
            data = self.scan_flatten.socket.recv(1024)
        else:
            self.scan_check.send_data("T".encode("utf-8"))
            data = self.scan_check.socket.recv(1024)
        data_str = data.strip().decode("utf-8")
        self.set_dv_value_with_name(dv_name, data_str)

