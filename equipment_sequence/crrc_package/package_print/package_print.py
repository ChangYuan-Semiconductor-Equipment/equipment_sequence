from passive_equipment.handler_passive import HandlerPassive
from webservice_api.webservice_api import WebserviceAPI
from zebra_api.zebra_api import ZebraPrinterClient

from crrc_package.package_print.database_table_model import ProductLinkPlastic
from crrc_package.package_print.zpl_command import zpl_code


class PackagePrint(HandlerPassive):

    def __init__(self):
        super().__init__()
        # self.webservice_api = WebserviceAPI("http://10.96.141.69:7456/M1AutoPackageNotLogo.asmx?wsdl")
        # self.zebra = ZebraPrinterClient("192.168.250.85", 7001)

    def label_print_request(self, call_back: dict):
        """包装盒请求打码.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        self.logger.info("正在执行 %s 函数", call_back["operation_func"])
        labels_info_package = self.get_dv_value_with_name("labels_info_package")
        self.logger.info("当前所有的一次标签码: %s", labels_info_package)
        instances = self.mysql.query_data_by_values(ProductLinkPlastic, "label_info_one", labels_info_package)
        product_code_list = [instance.as_dict_specify()["product_code"] for instance in instances]
        self.logger.info("当前要包装的所有产品码是: %s", product_code_list)
        # self.zebra.send_zpl(zpl_code)
