import io
import unittest
from lightning_alert import load_assets, get_quadkeys, asset_lookup
import unittest.mock


class TestLightningAlert(unittest.TestCase):

    def test_load_assets(self):
        expected_list = [{"assetName": "Chandler Bing",
                          "quadKey": "01111111111",
                          "assetOwner": "00001"},
                         {"assetName": "Joey Tribianni",
                         "quadKey": "02222222222", "assetOwner": "00002"}]
        self.assertEquals(load_assets('assets_test1.json'), expected_list)

    def test_load_assets_count(self):
        self.assertEquals(len(load_assets('assets_test1.json')), 2)

    def test_get_quadkey_count(self):
        self.assertEquals(len(get_quadkeys('lightning_test1.json')), 5)

    def test_get_quadkey_count_with_duplicates(self):
        self.assertEquals(len(get_quadkeys('lightning_test2.json')), 5)

    def test_get_quadkey(self):
        self.assertEquals(get_quadkeys('lightning_test1.json'),
                          {'311231321220', '033321132300', '032231233122',
                           '023112133022', '300012303123'})

    def test_get_quadkey_random(self):
        self.assertEquals(get_quadkeys('lightning_test1.json'),
                          {'033321132300', '311231321220', '300012303123',
                           '023112133022', '032231233122'})

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_asset_lookup_if_existing(self, mock_stdout):
        asset_lookup([{"assetName": "Name2",
                       "quadKey": "22222",
                       "assetOwner": "2"}], {'11111', '22222'})
        self.assertEqual(mock_stdout.getvalue().rstrip("\n"),
                         "lightning alert for 2:Name2")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_asset_lookup_if_not_existing(self, mock_stdout):
        asset_lookup([{"assetName": "Name3",
                       "quadKey": "33333",
                       "assetOwner": "3"}], {'11111', '22222'})
        # Assert if equal to ''
        self.assertEqual(mock_stdout.getvalue().rstrip("\n"), '')


if __name__ == "__main__":
    unittest.main()
