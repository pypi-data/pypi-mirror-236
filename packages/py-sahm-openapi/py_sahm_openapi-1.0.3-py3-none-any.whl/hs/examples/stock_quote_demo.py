# -*- coding: utf-8 -*-
import json
import threading

from hs.api.constant import ModelResult, DataType, Direction, ExRightFlag, CycType, SecurityParam, HQSubscribeTopicId, \
    MktTmType, DepthBookType, OptionPriceFlag, OptionType, ExchangeType, SaudiOrderBookType, StatusCode
from hs.api.quote_api import QuoteAPI
from hs.common.protobuf_utils import parse_payload, proto_to_dict
import cmd


class StockQuoteDemo(object):
    """Stock quotes interface independent Demo program"""

    def __init__(self, **kwargs):
        self._quote_api = QuoteAPI(**kwargs)
        self._login_account = self._quote_api.get_login_code_mobile()
        self._timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._quote_api.is_alive()

    def get_token(self):
        """获取平台Token"""
        return self._quote_api.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._quote_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._quote_api.add_notify_callback(self.notify_callback)
        return self

    def query_hq_basic_qot(self, args=None) -> ModelResult:
        """Query basic stock quotes in batches"""
        if args is None:
            args = {"exchange_type": "S", "security_list": """[{"data_type": 60000, "stock_code": "2222.SA"}]"""}
        json_params = self.str_to_json(args)
        if json_params is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')
        exchange_type = json_params.get('exchange_type', '')
        security_list = list()
        for security in json_params.get('security_list', []):
            security_list.append(SecurityParam(security.get('data_type'), security.get('stock_code')))

        model_result = self._quote_api.query_hq_basic_qot(exchange_type=exchange_type, security_list=security_list)
        if model_result.is_success:
            print(f"login account: {self._login_account}, hq basic quote：{model_result.get_model()}")
        else:
            print(
                f"fail to query hq basic quote, code: {model_result.code}, msg: {model_result.msg}, login account: {self._login_account}")
        return model_result

    def query_saudi_hq_order_book(self, args: str = '') -> ModelResult:
        """Query saudi stock order book"""
        if not args:
            args = {"order_book_type": "MBO", "security_param": {"data_type": 60000, "stock_code": "2222.SA"}}
            print(f"use default argument->{args}")
        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')
        order_book_type = json_param.get('order_book_type')
        data_type = json_param.get('security_param', {}).get('data_type')
        stock_code = json_param.get('security_param', {}).get('stock_code')

        model_result = self._quote_api.query_saudi_hq_order_book(
            security_param=SecurityParam(data_type=data_type, stock_code=stock_code), order_book_type=order_book_type)
        if model_result.is_success:
            print(f"order book：{model_result.get_model()}")
        else:
            print(f"fail to query order book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_us_hq_order_book(self, args: str = '') -> ModelResult:
        """Query us stock order book"""
        if not args:
            args = {"depth_book_type": 2, "mkt_tm_type": 1,
                    "security_param": {"data_type": 20000, "stock_code": "BABA"}}
            print(f"use default argument->{args}")
        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        depth_book_type = json_param.get('depth_book_type')
        mkt_tm_type = json_param.get('mkt_tm_type')
        security_param = SecurityParam(data_type=json_param.get('security_param', {}).get('data_type', ''),
                                       stock_code=json_param.get('security_param', {}).get('stock_code', ''))
        model_result = self._quote_api.query_us_hq_order_book(
            security_param=security_param, mkt_tm_type=mkt_tm_type,
            depth_book_type=depth_book_type)
        if model_result.is_success:
            print(f"order book：{model_result.get_model()}")
        else:
            print(f"fail to query order book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_ticker(self, args: str = '') -> ModelResult:
        """Query the recent ticker list"""
        if not args:
            args = {"exchange_type": "P", "limit": 10, "security_param": {"data_type": 20000, "stock_sode": "BABA"}}
            print(f"use default argument->{args}")

        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        exchange_type = json_param.get('exchange_type', '')
        limit = json_param.get('limit')
        security_param = SecurityParam(data_type=json_param.get('security_param', {}).get('data_type'),
                                       stock_code=json_param.get('security_param', {}).get('stock_sode'))
        model_result = self._quote_api.query_hq_ticker(exchange_type=exchange_type,
                                                       security_param=security_param,
                                                       limit=limit)
        if model_result.is_success:
            print(f"hq ticker：{model_result.get_model()}")
        else:
            print(f"fail to query hq ticker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_kline(self, args: str = '') -> ModelResult:
        """Query KL info"""
        if not args:
            args = {"exchange_type": "S", "limit": 10, "start_date": '20230907', "direction": 0, "ex_right_flag": 0,
                    "cyc_type": 2, "security_param": {"data_type": 60000, "stock_code": "2222.SA"}}
            print(f"use default argument->{args}")
        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        security_param = SecurityParam(json_param.get('security_param', {}).get('data_type'),
                                       json_param.get('security_param', {}).get('stock_code'))

        model_result = self._quote_api.query_hq_kline(exchange_type=json_param.get('exchange_type', ''),
                                                      security_param=security_param,
                                                      start_date=json_param.get('start_date', ''),
                                                      direction=json_param.get('direction', None),
                                                      ex_right_flag=json_param.get('ex_right_flag', None),
                                                      cyc_type=json_param.get('cyc_type', None),
                                                      limit=json_param.get('limit', 100))
        if model_result.is_success:
            print(f"hq kline：{model_result.get_model()}")
        else:
            print(f"fail to query hq kline, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_time_share(self, args: str = '') -> ModelResult:
        """ Query timeshare data"""
        if not args:
            args = {"exchange_type": "P", "security_param": {"data_type": 20000, "stock_code": "BABA"}}
            print(f"use default argument->{args}")

        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        security_param = SecurityParam(json_param.get('security_param', {}).get('data_type'),
                                       json_param.get('security_param', {}).get('stock_code'))
        model_result = self._quote_api.query_hq_time_share(exchange_type=json_param.get('exchange_type', ''),
                                                           security_param=security_param)
        if model_result.is_success:
            print(f"hq time share：{model_result.get_model()}")
        else:
            print(f"fail to query hq time share, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_option_expire_date_list(self, args: str = ''):
        """Query us option chain expiration date list"""
        if not args:
            args = {"stock_sode": "BABA"}
            print(f"use default argument->{args}")

        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._quote_api.query_us_option_expire_date_list(stock_code=json_param['stock_sode'])
        if model_result.is_success:
            print(f"query option expire date list：{model_result.get_model()}")
        else:
            print(f"fail to query option expire date list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_option_code_list(self, args: str = ''):
        """Query us option chain code list"""
        if not args:
            args = {"stock_sode": "BABA", "expire_date": "2023/09/07", "flag_in_out": 1, "option_type": "C"}
            print(f"use default argument->{args}")
        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        model_result = self._quote_api.query_us_option_code_list(stock_code=json_param.get('stock_code', ''),
                                                                 expire_date=json_param.get('expire_date', ''),
                                                                 flag_in_out=json_param.get('flag_in_out', None),
                                                                 option_type=json_param.get('option_type', ''))
        if model_result.is_success:
            print(f"query option code list：{model_result.get_model()}")
        else:
            print(f"fail to query option code list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def hq_subscribe_qot(self, args: str = ''):
        """订阅基础行情推送消息"""
        if not args:
            args = {"topic_id": "1036", "security_list": [{"data_type": 2000, "stock_code": "SINA"}]}
            print(f"use default argument->{args}")

        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        security_list = list()
        for security in json_param['security_list']:
            security_list.append(SecurityParam(security.gte('data_type', ''), security.get('stock_code', '')))

        model_result = self._quote_api.hq_subscribe(topic_id=json_param.get('topic_id', None),
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅基础行情推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe basic_qot, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_qot(self, args: str = ''):
        """取消订阅基础行情推送消息"""
        if not args:
            args = {"topic_id": "1036", "security_list": [{"data_type": 20000, "stock_code": "SINA"}]}
            print(f"use default argument->{args}")

        json_param = self.str_to_json(args)
        if json_param is None:
            return ModelResult(False, StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION, '')

        security_list = list()
        for security in json_param['security_list']:
            security_list.append(SecurityParam(security.gte('data_type', ''), security.get('stock_code', '')))
        model_result = self._quote_api.hq_unsubscribe(topic_id=json_param['topic_id'],
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅基础行情推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe basic_qot, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def notify_callback(self, pb_notify):
        """
        定义处理消息推送的callback
        :param pb_notify  参考 PBNotify.proto
        notifyMsgType:
        OrderBookNotifyMsgType = 20001
        BrokerQueueNotifyMsgType = 20002
        BasicQotNotifyMsgType = 20003
        TickerNotifyMsgType = 20004
        """
        print(
            f"hq_notify_callback，notifyMsgType：{pb_notify.notifyMsgType}，pb_notify：{pb_notify}，payload：{parse_payload(pb_notify)}")

    def timer_callback(self, interval=30):
        """"
        增加线程接口轮询，维持登录态
        """
        self._timer_threading = threading.Timer(interval, self.timer_callback, (interval,))
        self._timer_threading.setDaemon(False)
        self._timer_threading.start()
        self.query_hq_basic_qot("""{"exchange_type": "S", "security_list": [{"data_type": 60000, "stock_code": "2222.SA"}]}""")

    def stop(self):
        """退出业务API上下文环境"""
        # self._timer_threading.cancel()
        self._quote_api.stop()

    def str_to_json(self, param: str = ''):
        if not str:
            return None
        try:
            return json.loads(param)
        except Exception as ex:
            print("self.str_to_json:%s", ex)
        return None


class InterfaceTestCmd(cmd.Cmd):
    intro = "Quote Interface test system, enter help or ? to view help. \n"
    prompt = "$>"

    def __init__(self, invoker: StockQuoteDemo):
        super().__init__()
        self.invoker_instance = invoker

    def do_query_hq_basic_qot(self, args: str = ''):
        """query_hq_basic_qot {"exchange_type": "S", "security_list": [{"data_type": 60000, "stock_code":"2222.SA"}]}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_hq_basic_qot(args)

    def do_query_saudi_hq_order_book(self, args: str = ''):
        """query_saudi_hq_order_book {"order_book_type": "MBO", "security_param": {"data_type": 60000, "stock_code":"2222.SA"}}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_saudi_hq_order_book(args)

    def do_query_us_hq_order_book(self, args: str = ''):
        """query_us_hq_order_book {"depth_book_type": 2, "mkt_tm_type": 1,"security_param": {"data_type": 20000, "stock_code": "BABA"}}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_us_hq_order_book(args)

    def do_query_hq_ticker(self, args: str = ''):
        """query_hq_ticker {"exchange_type": "P", "limit": 10, "security_param": {"data_type": 20000, "stock_sode": "BABA"}}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_hq_ticker(args)

    def do_query_hq_kline(self, args: str = ''):
        """query_hq_kline {"exchange_type": "P", "limit": 10, "start_date": "20230907", "direction": 0, "ex_right_flag": 0, "cyc_type": 2, "security_param": {"data_type": 60000, "stock_sode": "2222.SA"}}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_hq_kline(args)

    def do_query_hq_time_share(self, args: str = ''):
        """query_hq_time_share {"exchange_type": "P", "security_param": {"data_type": 20000, "stock_code": "BABA"}}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_hq_time_share(args)

    def do_query_option_expire_date_list(self, args: str = ''):
        """query_option_expire_date_list {"stock_sode": "BABA"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_option_expire_date_list(args)

    def do_query_option_code_list(self, args: str = ''):
        """query_option_code_list {"stock_sode": "BABA", "expire_date": "2023/09/07", "flag_in_out": 1, "option_type": "C"}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.query_option_code_list(args)

    def do_hq_subscribe_qot(self, args: str = ''):
        """hq_subscribe_qot {"topic_id": "1036", "security_list": [{"data_type": 20000, "stock_code": "SINA"}]}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.hq_subscribe_qot(args)

    def do_hq_unsubscribe_qot(self, args: str = ''):
        """hq_unsubscribe_qot {"topic_id": "1036", "security_list": [{"data_type": 2000, "stock_code": "SINA"}]}"""
        if not args:
            print("Please enter your arguments or help <command> to query")
            return
        self.invoker_instance.hq_unsubscribe_qot(args)

    def do_stop(self, empty_arg: str):
        """stop"""
        print("Stop server, close connection....")
        self.invoker_instance.stop()
        exit(1)

    def emptyline(self):
        print("Please enter your command")
        return cmd.Cmd.emptyline(self)


def start_quote_test(login_mobile: str, login_passwd: str):
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
        "login_domain": "http://quantapi-feature.alsahm.com",  # 生产环境domain为：https://openapi.hstong.com
        "login_country_code": "SAU",
        # 如果为香港或美国地区手机号，需要修改为对应区域编码，区域编码查询：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8
        "login_mobile": login_mobile,  # 登录账号无需加区号
        "login_passwd": login_passwd,
        "trading_passwd": "<Trade password>",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 2、初始化行情API对象、增加消息推送回调函数
    quote_demo = StockQuoteDemo(**params).add_notify_callback()
    # 3、执行HTTP登录、获取token及连接ip port
    token = quote_demo.get_token()
    # 4、启动行情API上下文，并会初始化连接、交易登录
    quote_demo.start(token)
    # 5、检查连接状态
    is_alive = quote_demo.check_alive()

    if is_alive:
        # 增加线程接口轮询
        # quote_demo.timer_callback(interval=30)
        test_cmd = InterfaceTestCmd(quote_demo)
        try:
            test_cmd.cmdloop()
        except Exception as e:
            print("Exception %s", e)
            test_cmd.cmdloop()

    else:
        # This function will exit the transaction login and disconnect the TCP link
        quote_demo.stop()
        exit(1)


if __name__ == '__main__':
    start_quote_test(login_mobile='611000229', login_passwd='Hst11111')
