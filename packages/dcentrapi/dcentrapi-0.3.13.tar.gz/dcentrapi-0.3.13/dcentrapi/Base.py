class Base:
    def __init__(self, stage, username=None, key=None):
        self.__version__ = "0.3.13"  # update here and in setup.py

        if stage == "develop":
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://test-api.dcentralab.com/"
            self.web3index_url = "https://test-api.web3index.info/"
        if stage == "staging":
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://staging.dcentralab.com/"
            self.web3index_url = "https://staging-api.web3index.info/"
        if stage == "preprod":
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://preprod-api.dcentralab.com/"
            self.web3index_url = "https://preprod-api.web3index.info/"
        if stage == "main":
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://main-api.dcentralab.com/"
            self.web3index_url = "https://api.web3index.info/"
        if stage == "staging-api":
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://staging-api.dcentralab.com/"
            self.web3index_url = "https://staging-api.web3index.info/"


class DapiError:
    def __init__(self, response, exception):
        self.response = response
        self.exception = exception
