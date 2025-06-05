"""
流程:
    操作员扫在页面上扫描大载具码、输入端口号
        S6F11 1008 NoState2WaitingForHost

    监控到 eap 发来的 S3F17
        ProceedWithCarrier:
            S6F11 1009 WaitingForHost2IdVerificationOk
        CancelCarrier:
            S6F11 1010 CancelCarrier

    eap 切换配方
        S2F41 pp_select
        S6F11 1011 pp_select_result

    eap 下发白名单和尾料信息
        S2F49

    页面显示尾料信息

    eap 尾料检查
        S6F11 1012 ResetBoxValidated   尾料盒检查  不需要, 设备根据白名单自己检查

        如果设备自检失败需要将检查失败的放到自定盒子, 然后发送自检查失败事件
            S6F11 1013 ResetModuleValidatedFailed   单个尾料产品自检查失败

        设备自检查成功发送检查成功事件
            S6F11 1014 ResetModuleValidatedPassed   单个尾料产品自检查成功

    开始包装
        S6F11 1015 PackingStarting
        S6F11 1016 ModuleValidationFailed  产品不在白名单事件
        S6F11 1017 ModuleValidationPassed  产品在白名单事件

    每个白色盒子包装完成
        S6F11 1018 BoxCompleted, 这个事件相当于请求打印标签
        更新XML文件
        问题: 打印机谁控制
            客户控制: 打印完成需要给我一个打印完成信号
            设备控制: 需要EAP给打印内容

    扫描包装盒标签
        S6F11 1019 LabelScanned, 扫描包装盒标签信息
        S2F41 validate_label  eap检查标签信息, 如果EAP检查失败设备报警人工取走NG标签盒子
        S6F11 1021 LabelFailBoxRemoved  人工拿走标签失败的盒子

    盒子放到工位后上传盒子工位信息
        S6F11 1020 BoxRemoved, 包装盒放到了指定工位

    工单结束
        上传XML文件到指定目录
        S6F11 1022 LotEnd

"""
from passive_equipment.handler_passive import HandlerPassive


class Infineon(HandlerPassive):

    def __init__(self):
        super().__init__()

    def _on_s02f49(self, handler, message):
        function = self.settings.streams_functions.decode(message)
        rcmd_name = function.get()
        self.send_response(
            self.stream_function(2, 50)({"HCACK": 0, "PARAMS": [["wwww", "wwww"]]}),
            message.header.system
        )
        self.lower_computer_instance.execute_write()

    def _on_s03f17(self, handler, message):
        self.send_response(
            self.stream_function(3, 18)({"CAACK": 0, "PARAMS": [[2, "dffdff"]]}),
            message.header.system
        )
