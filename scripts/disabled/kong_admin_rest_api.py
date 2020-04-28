# -*- encoding: utf-8 -*-

from lib.common import save_script_result
import requests


ports_to_check = 8001    # 默认服务端口


def do_check(self, url):
    if url != '/':
        return

    if self.conn_pool and self.index_headers.get('Server', '').startswith('kong/'):
        save_script_result(self, '200', self.base_url, 'Kong Admin Rest API')

    if self.port == 8001:   # 如果已经维护了 8001 端口的 HTTP连接池，上面的逻辑已经完成扫描
        return

    if 8001 not in self.ports_open:    # 如果8001端口不开放
        return

    # 如果输入的是一个非标准端口的HTTP服务
    # 那么，需要单独对8001端口进行检测

    resp = requests.get('http://%s:8001/' % self.host)
    headers = resp.headers
    if headers.get('Server', '').startswith('kong/'):
        save_script_result(self, resp.status_code, 'http://%s:8001' % self.host, 'Kong Admin Rest API')
