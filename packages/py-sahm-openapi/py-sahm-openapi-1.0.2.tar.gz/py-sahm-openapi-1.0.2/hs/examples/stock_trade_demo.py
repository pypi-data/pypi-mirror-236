# -*- coding: utf-8 -*-
import cmd
import threading
import time

from hs.api.trading_api import TradingAPI
from hs.common.common_utils import now_to_str
from hs.common.protobuf_utils import parse_payload
from hs.api.constant import ExchangeType, EntrustBS, EntrustType, ModelResult, EntrustEX, SessionType, CondTrackType, \
    AlgoEntrustType, AlgoStrategyType, AlgoStrategySensitivityType, AlgoActionType, DataType, RateType, StatusCode
import json


class StockTradeDemo(object):
    """股票交易类接口独立Demo程序"""

    def __init__(self, **kwargs):
        self._trading_api = TradingAPI(**kwargs)
        self._login_account = self._trading_api.get_login_code_mobile()
        self._timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._trading_api.is_alive()

    def get_token(self):
        """Query platform token"""
        return self._trading_api.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._trading_api.start(p_token)
        return self

    def query_portfolio_list(self, args: str = '') -> ModelResult:
        """Query Portfolio List"""
        exchange_type_list = self.str_to_json(args)
        if exchange_type_list is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.query_portfolio_list(exchange_type_list)
        if model_result.is_success:
            print(f"Portfolio list:{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_fund_info(self, args: str = '') -> ModelResult:
        """Query Fund Info"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')
        model_result = self._trading_api.query_fund_info(exchange_type=param.get('exchange_type', ''),
                                                         portfolio=param.get('portfolio', ''))
        if model_result.is_success:
            print(f"portfolio list:{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_position_list(self, args: str = '') -> ModelResult:
        """Query Position List"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')
        model_result = self._trading_api.query_position_list(exchange_type=param.get('exchange_type', ''),
                                                             portfolio=param.get('portfolio', ''))
        if model_result.is_success:
            print(f"position list：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_max_buying_power(self, args: str = '') -> ModelResult:
        """"Query max buying power"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')
        model_result = self._trading_api.query_max_buying_power(exchange_type=param.get('exchange_type', ''),
                                                                portfolio=param.get('portfolio', ''),
                                                                order_type=param.get('order_type', ''),
                                                                stock_code=param.get('stock_code', ''),
                                                                order_price=param.get('order_price', ''),
                                                                order_id=param.get('order_id', ''))
        if model_result.is_success:
            print(f"max buying power info：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def place_order(self, args: str = '') -> ModelResult:
        """Place Oder"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.place_order(exchange_type=param.get('exchange_type', ''),
                                                     portfolio=param.get('portfolio', ''),
                                                     order_type=param.get('order_type', ''),
                                                     stock_code=param.get('stock_code', ''),
                                                     order_price=param.get('order_price', ''),
                                                     order_qty=param.get('order_qty', ''),
                                                     order_side=param.get('order_side', ''),
                                                     validity=param.get('validity', ''),
                                                     expiry_date=param.get('expiry_date', ''),
                                                     session_type=param.get("session_type", ''),
                                                     display_size=param.get("display_size", ''),
                                                     )
        if model_result.is_success:
            print(f"order id：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def modify_order(self, args: str = '') -> ModelResult:
        """Modify Order"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.modify_order(order_id=param.get('order_id', ''),
                                                      exchange_type=param.get('exchange_type', ''),
                                                      portfolio=param.get('portfolio', ''),
                                                      order_qty=param.get('order_qty', ''),
                                                      stock_code=param.get('stock_code', ''),
                                                      validity=param.get('validity', ''),
                                                      order_price=param.get('order_price', ''),
                                                      expiry_date=param.get("expiry_date", ''),
                                                      display_size=param.get("display_size", ''))
        if model_result.is_success:
            print(f"order id：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_oder(self, args: str = '') -> ModelResult:
        """Cancel Order"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.cancel_order(order_id=param.get('order_id', ''),
                                                      portfolio=param.get('portfolio', ''),
                                                      exchange_type=param.get('exchange_type', ''))
        if model_result.is_success:
            print(f"order id：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_today_order_list(self, args: str = '') -> ModelResult:
        """Query Today Order List"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.query_today_order_list(exchange_type=param.get('exchange_type', ''),
                                                                portfolio=param.get('portfolio', ''),
                                                                limit=param.get('limit', ''),
                                                                order_status_list=param.get("order_status_list", ''))
        if model_result.is_success:
            print(f"order list：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_history_order_list(self, args: str = '') -> ModelResult:
        """Query history Order List"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.query_history_order_list(exchange_type=param.get('exchange_type', ''),
                                                                  portfolio=param.get('portfolio', ''),
                                                                  start_date=param.get('start_date', ''),
                                                                  end_date=param.get('end_date', ''),
                                                                  offset=param.get('offset', ''),
                                                                  limit=param.get('limit', ''),
                                                                  order_status_list=param.get("order_status_list", None))
        if model_result.is_success:
            print(f"order list：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_cash_statement_list(self, args: str = '') -> ModelResult:
        """Query cash statement List"""
        param = self.str_to_json(args)
        if param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._trading_api.query_cash_statement_list(portfolio=param.get('portfolio', ''),
                                                                   exchange_type=param.get('exchange_type', ''),
                                                                   start_date=param.get("start_date", ''),
                                                                   end_date=param.get("end_date", ''),
                                                                   flow_direction=param.get("flow_direction", ''),
                                                                   flow_type_category_list=param.get("flow_type_category_list", []),
                                                                   offset=param.get("offset", ''),
                                                                   limit=param.get("limit", '')
                                                                   )
        if model_result.is_success:
            print(f"cash statement list：{model_result.get_model()}")
        else:
            print(f"fail to query, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def trade_subscribe(self):
        """trade_subscribe"""
        model_result = self._trading_api.trade_subscribe()
        if model_result.is_success:
            print(f"Trade subscribe success")
        else:
            print(f"trade subscribe failed: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def trade_cancel_subscribe(self):
        """trade_cancel_subscribe"""
        model_result = self._trading_api.trade_cancel_subscribe()
        if model_result.is_success:
            print(f"Trade cancel subscribe success")
        else:
            print(f"trade cancel subscribe failed: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def notify_callback(self, pb_notify):
        """
        定义处理消息推送的callback
        :param pb_notify  参考 PBNotify.proto
        """
        print(f"trading notify_callback，pb_notify：{pb_notify}，payload：{parse_payload(pb_notify)}")

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._trading_api.add_notify_callback(self.notify_callback)
        return self

    def stop(self):
        """退出业务API上下文环境"""
        # self._timer_threading.cancel()
        self._trading_api.stop()

    def str_to_json(self, param: str = ''):
        if not str:
            return None
        try:
            return json.loads(param)
        except Exception as ex:
            print("self.str_to_json:%s", ex)
        return None

    def timer_callback(self, interval=30):
        """"
        增加线程接口轮询，维持登录态
        """
        self._timer_threading = threading.Timer(interval, self.timer_callback, (interval,))
        self._timer_threading.setDaemon(False)
        self._timer_threading.start()
        self.query_portfolio_list("""["S", "P"]""")


class TradeInterfaceTestCmd(cmd.Cmd):
    intro = "Trade Interface test system, enter help or ? to view help. \n"
    prompt = "$>"

    def __init__(self, invoker: StockTradeDemo):
        super().__init__()
        self.invoker_instance = invoker

    def do_trade_subscribe(self, args: str = ''):
        """trade_subscribe"""
        self.invoker_instance.trade_subscribe()

    def do_trade_cancel_subscribe(self, args: str = ''):
        """trade_cancel_subscribe"""
        self.invoker_instance.trade_cancel_subscribe()

    def do_query_portfolio_list(self, args: str = ''):
        """query_portfolio_list ["S", "P"]"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_portfolio_list(args)

    def do_query_fund_info(self, args: str = ''):
        """query_fund_info {"exchange_type":"S", "portfolio":"138926816"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_fund_info(args)

    def do_query_position_list(self, args: str = ''):
        """query_position_list {"exchange_type":"S", "portfolio":"138926816"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_position_list(args)

    def do_query_max_buying_power(self, args: str = ''):
        """query_max_buying_power {"exchange_type":"S", "portfolio":"138926816", "order_type":"3", "stock_code":"2222.SA", "order_price":"10", "order_id":"123"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_max_buying_power(args)

    def do_place_order(self, args: str = ''):
        """place_order {"exchange_type":"S", "portfolio":"138926816", "order_type":"3", "stock_code":"2222.SA", "order_price":"10", "order_qty":"10", "order_side":"3", "validity":"1"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.place_order(args)

    def do_modify_order(self, args: str = ''):
        """modify_order {"exchange_type":"S", "portfolio":"138926816", "order_type":3, stock_code:"2222.SA", "order_price":10, "order_qty":10, "order_side":3, "validity":1}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.modify_order(args)

    def do_cancel_oder(self, args: str = ''):
        """cancel_oder {"exchange_type":"S", "portfolio":"138926816", "order_id":1234}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.cancel_oder(args)

    def do_query_today_order_list(self, args: str = ''):
        """query_today_order_list {"exchange_type":"S", "portfolio":"138926816", "limit":"10"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_today_order_list(args)

    def do_query_history_order_list(self, args: str = ''):
        """query_history_order_list {"exchange_type":"S", "portfolio":"138926816", "start_date":"20230710", "end_date":"20230901", "offset":"0", "limit":"10"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_history_order_list(args)

    def do_query_cash_statement_list(self, args: str = ''):
        """query_cash_statement_list {"exchange_type":"S", "portfolio":"138926816", "start_date":"20230710", "end_date":"20230901", "offset":"0", "limit":"10"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_cash_statement_list(args)

    def do_stop(self, empty_arg: str):
        """stop"""
        self.invoker_instance.stop()
        exit(0)

def start_trade_test(login_mobile: str, login_passwd: str, trading_passwd: str):
    # 1、配置启动参数
    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                            "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                            "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ENCRYPT_RSA_PRIVATEKEY = """MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKr24lt+FMSEzGzP
                              CMmc+LCaaRoymseEwNdQGYc4FFSpkBKdEKhcEXndInkkqcjpNMTByTRqzLIR/qYA
                              TuNWl6uCs8Ck5w8aHyDwmb6+72SyAa0LSfWoYRGKA/eps3efrK4uyzrsOvIafwPf
                              pXG8Q5Z+2yBDrRwVI8YM9lOzAlFZAgMBAAECgYAlzAlFQv2iaN2tHKSLtkmA+dJM
                              uW1guOfNcmcCbxKHmSlCBDl/j0NJ1urdL47d3TkOWu15yjbRE4th9eV6+1TyeKTl
                              1JQ9TdA4/NG70aqU25P/ZTSkbuG0MRBBZIsKEQTJrKcei2cIKoIb+QwvBwzwUkXl
                              aRbUgMvhSNLL7l8IRQJBANE8hcGrOi0XXWQJmYfLcGRbWajwp09uf5OaB/T1mFyq
                              z6ehAw0TtUx/zaoX0bgaOdWTCDg4eDp3HEQJWDYyLAMCQQDRLJ/6kpqr8pm1ipqU
                              pzR0gWYb+WhLF8vraoLoD688zuacxvhqJEtjriPLtzcvOHHA+KleedwHeacRs34/
                              7YRzAkBrHqEb1Z2jGCMn5AJGE1EnD92HMC137QpDdsg8EMBAMPK+zx/QwhY/Y+7W
                              9frYVhTl0rCSl9Z1mCVQb7hJhsYhAkBet4JJiJEZQ2Vu2zBcF8qc5utBx5H+Tuw7
                              0aMtSczkEBxE6aQbDAxHOtdiq7gFXd3Er9ShvzRu/hs03L5SXE8ZAkAEdRkRzQnc
                              ruq7ueQAvGsczg2wuNNh4EXIfq2krXLS3riN0SSeXejF9+FL8wEExwPpdLVBR+JT
                              eDr7onfVE+FX
                              """
    params = {
        "rsa_public_key": ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "http://quantapi-feature.alsahm.com",
        "login_country_code": "SAU",
        # If it is a mobile phone number in Hong Kong or the United States, it needs to be modified to the
        # corresponding area code. Area code query：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD
        # %97%E5%85%B8
        "login_mobile": login_mobile,  # 登录账号无需加区号
        "login_passwd": login_passwd,
        "trading_passwd": trading_passwd,
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 2、初始化交易API对象、增加消息推送回调函数
    trade_demo = StockTradeDemo(**params).add_notify_callback()
    # trade_demo = StockTradeDemo(**params)
    # 3、执行HTTP登录、获取token及连接ip port
    token = trade_demo.get_token()
    # 4、启动交易API上下文，并会初始化连接、交易登录
    trade_demo.start(token)
    # 5、检查连接状态
    is_alive = trade_demo.check_alive()

    if is_alive:
        # 增加线程接口轮询，维持登录态
        # trade_demo.timer_callback(interval=30)
        test_cmd = TradeInterfaceTestCmd(trade_demo)
        try:
            test_cmd.cmdloop()
        except Exception as ex:
            print("Exception %s", ex)
            test_cmd.cmdloop()
    else:
        # This function will exit the transaction login and disconnect the TCP link
        trade_demo.stop()
        exit(1)


if __name__ == '__main__':
    start_trade_test(login_mobile='611000229', login_passwd='Hst11111', trading_passwd='111111')
