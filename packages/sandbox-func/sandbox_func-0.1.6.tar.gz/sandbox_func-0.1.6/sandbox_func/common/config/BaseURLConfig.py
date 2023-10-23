URL_DICT = {
    "LOCAL": "http://127.0.0.1:8080",
    "DEV": "http://cybotron-dev.yunzhangfang.com",
    "ALPHA": "http://cybotron-alpha.yunzhangfang.com",
    "BETA": "http://cybotron-beta.yunzhangfang.com",
    "PROD": "http://cybotron.yunzhangfang.com",
}


class BaseURLConfig:
    @staticmethod
    def get_api_base_url(env):
        if env == 'LOCAL':
            return URL_DICT[env]
        else:
            return URL_DICT[env] + "/cybotron-client"

    @staticmethod
    def get_domain_url(env):
        return URL_DICT[env]

    @staticmethod
    def get_env_list():
        return list(URL_DICT.keys())
