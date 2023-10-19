import unittest
from unittest.mock import patch, MagicMock
from ..KodiakMDNsLocate import MyListener, find_kodiak_ip_addresses


class TestMyListener(unittest.TestCase):
    def test_add_service(self):
        listener = MyListener()
        zeroconf = MagicMock()
        info = MagicMock()
        info.addresses = [b'\xc0\xa8\x01\x01']  # IP address 192.168.1.1
        zeroconf.get_service_info.return_value = info

        listener.add_service(zeroconf, "_kodiak._tcp.local.", "KodiakService")
        self.assertEqual(listener.found_ip_addresses, ["192.168.1.1"])

    def test_update_service(self):
        listener = MyListener()
        listener.update_service()  # Just to test the method without any actual assertions


class TestFindKodiakIPAddresses(unittest.TestCase):
    @patch("KodiakMDNsLocate.Zeroconf")
    @patch("KodiakMDNsLocate.ServiceBrowser")
    def test_find_kodiak_ip_addresses(self, mock_service_browser, mock_zeroconf):
        listener = MyListener()
        mock_service_browser.return_value = listener
        zeroconf = mock_zeroconf.return_value

        ip_addresses = find_kodiak_ip_addresses(runtime=1)

        self.assertEqual(ip_addresses, listener.found_ip_addresses)
        mock_zeroconf.assert_called_once()
        mock_service_browser.assert_called_once_with(zeroconf, "_kodiak._tcp.local.", listener)


if __name__ == '__main__':
    unittest.main()
