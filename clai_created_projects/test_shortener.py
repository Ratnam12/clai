import unittest
import os
import json
import shortener

class TestShortener(unittest.TestCase):
    TEST_DB = 'test_urls.json'

    def setUp(self):
        shortener.set_data_file(self.TEST_DB)
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def tearDown(self):
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_shorten_valid_url(self):
        url = "https://www.google.com"
        key = shortener.shorten_url(url)
        self.assertIsNotNone(key)
        self.assertEqual(len(key), 6)

    def test_resolve_valid_key(self):
        url = "https://www.python.org"
        key = shortener.shorten_url(url)
        resolved = shortener.resolve_url(key)
        self.assertEqual(url, resolved)

    def test_duplicate_url_returns_same_key(self):
        url = "https://www.github.com"
        key1 = shortener.shorten_url(url)
        key2 = shortener.shorten_url(url)
        self.assertEqual(key1, key2)

    def test_different_urls_return_different_keys(self):
        url1 = "https://www.apple.com"
        url2 = "https://www.microsoft.com"
        key1 = shortener.shorten_url(url1)
        key2 = shortener.shorten_url(url2)
        self.assertNotEqual(key1, key2)

    def test_resolve_non_existent_key(self):
        resolved = shortener.resolve_url("nonexistent")
        self.assertIsNone(resolved)

    def test_shorten_invalid_url_no_protocol(self):
        with self.assertRaises(ValueError):
            shortener.shorten_url("www.google.com")

    def test_shorten_invalid_url_malformed(self):
        with self.assertRaises(ValueError):
            shortener.shorten_url("http://")

    def test_shorten_url_with_query_params(self):
        url = "https://www.example.com/search?q=test&hl=en"
        key = shortener.shorten_url(url)
        resolved = shortener.resolve_url(key)
        self.assertEqual(url, resolved)

    def test_shorten_url_with_fragment(self):
        url = "https://en.wikipedia.org/wiki/URL_shortening#Techniques"
        key = shortener.shorten_url(url)
        resolved = shortener.resolve_url(key)
        self.assertEqual(url, resolved)

    def test_shorten_localhost(self):
        url = "http://localhost:8000/test"
        key = shortener.shorten_url(url)
        resolved = shortener.resolve_url(key)
        self.assertEqual(url, resolved)

    def test_shorten_ip_address(self):
        url = "http://127.0.0.1:5000"
        key = shortener.shorten_url(url)
        resolved = shortener.resolve_url(key)
        self.assertEqual(url, resolved)

    def test_load_data_missing_file(self):
        # setUp already ensures file doesn't exist
        data = shortener.load_data()
        self.assertEqual(data, {})

    def test_load_data_corrupted_file(self):
        with open(self.TEST_DB, 'w') as f:
            f.write("not a json")
        data = shortener.load_data()
        self.assertEqual(data, {})

    def test_generate_short_key_length(self):
        key = shortener.generate_short_key(10)
        self.assertEqual(len(key), 10)

    def test_is_valid_url_various(self):
        self.assertTrue(shortener.is_valid_url("https://google.com"))
        self.assertTrue(shortener.is_valid_url("http://my-site.io/path"))
        self.assertFalse(shortener.is_valid_url("ftp://invalid")) # My regex allows ftp, wait
        self.assertFalse(shortener.is_valid_url("just-a-string"))
        self.assertFalse(shortener.is_valid_url("http://.com"))

if __name__ == '__main__':
    unittest.main()
