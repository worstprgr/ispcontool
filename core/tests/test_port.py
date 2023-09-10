"""
Had to use a hack, to inject the **core** folder to the sys.path.
Although the module **sysextend** isn't in use, it still imports the
whole content.
"""
import sysextend
import unittest
from core import portutils
import core.logger

log = core.logger.Logger(__file__)
log.file_save = False
p = portutils.PortUtils()
online_mode = False


class TestVerifyConnection(unittest.TestCase):
    def test_scan_port(self):
        """
        Testing the ability to scan a port.

        **Info:**
        This test contains two modes: offline and online testing.
        Offline means, that the method **__scan_port_test** gets called.
        Basically it's a mock method that bypasses the port connection via
        the socket library.
        """
        # GIVEN
        port = 80
        url_online = [
            'google.com',
            'test.on'
        ]
        url_offline = [
            '1h1dh8012d13d.kr',
            'test.off'
        ]
        url_special_chars = [
            '=12!+-:;*^',
            '()!)("/§*.com'
        ]

        if online_mode:
            index = 0
            test_mode = False
        else:
            index = 1
            test_mode = True

        # WHEN
        scenario1 = p.scan_port(url_online[index], port, test=test_mode)
        scenario2 = p.scan_port(url_offline[index], port, test=test_mode)
        scenario3 = p.scan_port(url_special_chars[0], port, test=test_mode)
        scenario4 = p.scan_port(url_special_chars[1], port, test=test_mode)

        # THEN
        self.assertEqual(True, scenario1)
        self.assertEqual(False, scenario2)
        self.assertEqual(False, scenario3)
        self.assertEqual(False, scenario4)

    def test_con_check(self):
        """
        Testing the ability if the method **con_check** returns:

        * True -> if at least one server is online
        * False -> if no server is online

        **Info:**
        This test contains two modes: offline and online testing.
        Offline means, that the method **__scan_port_test** gets called.
        Basically it's a mock method that bypasses the port connection via
        the socket library.
        """
        # GIVEN
        urls_all_online = [
            'google.com',
            'test.on',
            'x.com',
            'test.on',
            'facebook.com',
            'test.on'
        ]
        urls_two_online = [
            'google.com',
            'test.on',
            'x.com',
            'test.on',
            'asdhjk123yxbnm.gov',
            'test.off'
        ]
        urls_one_online = [
            'google.com',
            'test.on',
            'koksdnkls7282.it',
            'test.off',
            'asdhjk123yxbnm.kr',
            'test.off'
        ]
        urls_zero_online = [
            'ndsakkfdb3421ucfbn.com',
            'test.off',
            'koksdnkls7282.co.uk',
            'test.off',
            'asdhjk123yxbnm.xyz',
            'test.off'
        ]

        if online_mode:
            start = 0
            test_mode = False
        else:
            start = 1
            test_mode = True

        # WHEN
        scenario1 = p.con_check(urls_all_online[start::2], test=test_mode)
        scenario2 = p.con_check(urls_two_online[start::2], test=test_mode)
        scenario3 = p.con_check(urls_one_online[start::2], test=test_mode)
        scenario4 = p.con_check(urls_zero_online[start::2], test=test_mode)

        # THEN
        self.assertEqual(True, scenario1)
        self.assertEqual(True, scenario2)
        self.assertEqual(True, scenario3)
        self.assertEqual(False, scenario4)


if __name__ == '__main__':
    unittest.main()
