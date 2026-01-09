"""
Host 控制三个下位机 secs 服务对接工厂.

    上料 plc
        1. 扫描大托盘发给工厂
            1. 扫描大托盘, host 收到 1008 NoState2WaitingForHost 事件  ok
            2. host 将 1008 NoState2WaitingForHost 事件发给工厂 ok
            3. 工厂下发 S3F17
                1. 收到 ProcessWithCarrier pallet_id, 给工厂上报 1009 WaitingForHost2IdVerificationOk ok
                2. 收到 CancelCarrier pallet_id, 给工厂上报 1024 PalletCancelled  ok
            4. 工厂下发 S2F41 PPSelect, 里面带有 产品的 ma 信息, 验证尾料盒子用的  ok
                1. host 通过 S2F41 给所有设备下发 PPSelect 远程命令  ok
                2. 给工厂上报 1011 PPSelectResult 事件  ok
            5. 工厂下发 S2F49 WhiteList 给 host  ok
                1. host 通过 S2F49 给所有设备下发 WhiteList 增强远程命令  ok
                2. 给工厂上报 1026 WhitelistLoaded 事件  ok

        2. 操作员将尾料盒子拿过来, 进行扫码验证, 设备自己验证, 验证的产品 ma 信息工厂会通过 PPSelect 下发
            1. 验证通过发送 1012 RestBoxValidated  ok
                1. 如果开启了 is_need_start_job 验证通过给工厂发送 1027 JobReady  ok
                    1.工厂通过 S2F41 下发 STARTJob, 然后给工厂发送 1015 PackingStarting  ok
                2. 如果关闭了 is_need_start_job 验证通过给工厂发送 1028 JobReadyWithoutAnswer 1015 PackingStarting  ok
            2. 验证失败发送 1033 RestBoxValidationFailed  ok

    将模块从黑盒子里拿到白盒子里 plc
        1. 机械手将带有模块的黑盒子拿到暂存位置

        2. 拿起产品进行 AOI 检查

        3. AOI 检查 通过的进行白名单检查, 检查通过放到白盒子了, 不通过的放到 NG 工位

    打标下料 plc
        1. 设备请求打印标签

        2. 打印出来的标签发给工厂进行验证

        3. 验证通过的下料, 第一个放到首盒工位, 尾盒放到尾盒工位

        4. 工单结束

"""
from passive_server.passive_host import HostPassive


class CellControl(HostPassive):
    """CellControl class."""

    def __init__(self):
        super().__init__()

    def _on_event_ControlStateChange(self, ce_id: int, reports: list):
        """接收到设备上报的 1001 控制状态变化事件.

        Args:
            ce_id: 事件 id.
            reports: 事件参数.
        """
        self.logger.info("ControlStateChange 事件id 是: %s", ce_id)
        pre_control_state = self.get_sv_value_with_name("ControlState")
        current_control_state = reports[0]["V"][0]
        if pre_control_state != current_control_state:
            self.set_sv_value_with_name("ControlState", current_control_state)
            self.send_s6f11("ControlStateChange")
            if current_control_state == 3:
                self.send_s6f11("EquipmentOffline")
            elif current_control_state == 7:
                self.send_s6f11("ControlStateOnlineLocal")
            elif current_control_state == 8:
                self.send_s6f11("ControlStateOnlineRemote")

    def _on_event_EquipmentOffline(self, ce_id: int, reports: list):
        """接收到设备上报的 1003 设备离线事件.

        Args:
            ce_id: 事件 id.
            reports: 事件参数.
        """

    def _on_event_ControlStateOnlineLocal(self, ce_id: int, reports: list):
        """接收到设备上报的 1004 控制状态变为 OnlineLocal 事件.

        Args:
            ce_id: 事件 id.
            reports: 事件参数.
        """

    def _on_event_ControlStateOnlineRemote(self, ce_id: int, reports: list):
        """接收到设备上报的 1004 控制状态变为 OnlineRemote 事件.

        Args:
            ce_id: 事件 id.
            reports: 事件参数.
        """

    def _on_event_ProcessStateChange(self, ce_id: int, reports: list):
        """接收到设备上报的 1002 控运行状态变化事件.

        Args:
            ce_id: 事件 id.
            reports: 事件参数.
        """
        self.logger.info("ProcessStateChange 事件id 是: %s", ce_id)
        pre_process_state = self.get_sv_value_with_name("process_state")
        current_process_state = reports[0]["V"][0]
        if pre_process_state != current_process_state:
            self.set_sv_value_with_name("process_state", current_process_state)
            self.send_s6f11("ProcessStateChange")
            self.set_sv_value_with_name("previous_process_state", current_process_state)
