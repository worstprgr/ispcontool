#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import socket


class PortUtils:
    def __init__(self):
        self.timeout: int = 1

    def con_check(self, hosts: list, port=80, test=False) -> bool:
        """
        Checks a list of server URLs if a specific port (default: 80) is available.
        If at least one server is available, it returns **True**. If no server is available,
        it returns **False**.
        :param hosts: **list** | list of server URLs
        :param port: **int** | a specific port (default 80)
        :param test: **bool** | if true, the method **__scan_port_test** gets called
        :return: **bool**
        """
        offline: int = 0
        for host in hosts:
            server_status: bool = self.scan_port(host, port, test)
            if not server_status:
                offline += 1

        if offline == len(hosts):
            return False
        else:
            return True

    def scan_port(self, host: str, port: int, test=False) -> bool:
        """
        Performs a connection to a specific port of a host.
        If you're changing this method, please adjust **__scan_port_test** too.
        :param host: **str** | example: google.off, facebook.on, x.off
        :param port: **int** | a specific port to connect
        :param test: **bool** | if true, the method **__scan_port_test** gets called
        :return: **bool**
        """
        if not test:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.timeout)
                    s.connect((host, port))
                return True
            except (socket.gaierror, socket.timeout):
                return False
        else:
            return self.__scan_port_test(host)

    @staticmethod
    def __scan_port_test(host: str) -> bool:
        """
        This method is an alternative mock for the method **scan_port** if
        an offline unit test is needed.
        If the URL ends with **.off** it returns **False**.
        If the URL ends with **.on** it returns **True**.
        :param host: **str** | example: google.off, facebook.on, x.off
        :return: **bool** | output depends if a URL ends with **.off** or **.on**
        """
        if host.endswith('.off'):
            # "simulating" socket.gaierror
            return False
        elif host.endswith('.on'):
            return True
        else:
            # "simulating" socket.gaierror
            return False


if __name__ == '__main__':
    hosts_list: list = ['google.com', 'x.com', 'facebook.com']
    vc = PortUtils()
    print(vc.con_check(hosts_list))
