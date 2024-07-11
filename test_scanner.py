import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import scanner

class TestScanner(unittest.TestCase):

    @patch('scanner.create_log')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_creating_folder_path(self, mock_exists, mock_makedirs, mock_create_log):
        path = "test_folder"
        scanner.creating_folder_path(path)
        mock_makedirs.assert_called_once_with(path)
        mock_create_log.assert_called_with(f"\n[*] Folder Created Successfully...{path}\n", "yellow")

    @patch('scanner.create_log')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True)
    def test_creating_folder_path_exists(self, mock_exists, mock_makedirs, mock_create_log):
        path = "test_folder"
        with self.assertRaises(SystemExit):
            scanner.creating_folder_path(path)
        mock_create_log.assert_called_with("\nTarget Folder Already Exists...\n", "red")

    @patch('requests.get')
    def test_detect_http_or_https(self, mock_get):
        url = 'example.com'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = 'http://example.com'
        mock_get.return_value = mock_response
        self.assertEqual(scanner.detect_http_or_https(url), 'http://example.com')
        
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        self.assertEqual(scanner.detect_http_or_https(url), 'Unknown')

    @patch('requests.get')
    def test_fetch_urls_from_wayback(self, mock_get):
        target = 'example.com'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            ["original"],
            ["http://example.com/1"],
            ["http://example.com/2"]
        ]
        mock_get.return_value = mock_response
        urls = scanner.fetch_urls_from_wayback(target)
        self.assertEqual(urls, ['http://example.com/1', 'http://example.com/2'])

    @patch('builtins.open', new_callable=mock_open)
    def test_write_results_to_file(self, mock_file):
        filename = 'test.txt'
        domain_to_ip = '127.0.0.1'
        ports = [80, 443]
        vulns = ['CVE-1234', 'CVE-5678']
        cpes = ['cpe:/a:test']
        scanner.write_results_to_file(filename, domain_to_ip, ports, vulns, cpes)
        mock_file.assert_called_once_with(filename, 'w', encoding='utf-8')
        mock_file().write.assert_any_call("[ ✔ ] [IP]: 127.0.0.1\n")

    @patch('tkinter.scrolledtext.ScrolledText')
    def test_create_log(self, mock_scrolledtext):
        mock_log_text = mock_scrolledtext.return_value
        message = "Test message"
        color = "cyan"
        scanner.log_text = mock_log_text
        scanner.create_log(message, color)
        mock_log_text.after.assert_any_call(0, mock_log_text.insert, "end", message, color)
        mock_log_text.after.assert_any_call(0, mock_log_text.see, "end")

if __name__ == '__main__':
    unittest.main()
