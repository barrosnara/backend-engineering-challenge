import unittest
import unbabel_cli
import os
import datetime


class TestUnbabel_cli(unittest.TestCase):
    """
        Unit tests for unbabel_cli methods
    """

    def setUp(self):
        self.events_list = [{'client_name': 'easyjet',
                              'duration': 20,
                              'event_name': 'translation_delivered',
                              'nr_words': 30,
                              'source_language': 'en',
                              'target_language': 'fr',
                              'timestamp': '2018-12-26 18:11:08.509654',
                              'translation_id': '5aa5b2f39f7254a75aa5'},
                             {'client_name': 'easyjet',
                              'duration': 31,
                              'event_name': 'translation_delivered',
                              'nr_words': 30,
                              'source_language': 'en',
                              'target_language': 'fr',
                              'timestamp': '2018-12-26 18:15:19.903159',
                              'translation_id': '5aa5b2f39f7254a75aa4'},
                             {'client_name': 'booking',
                              'duration': 54,
                              'event_name': 'translation_delivered',
                              'nr_words': 100,
                              'source_language': 'en',
                              'target_language': 'fr',
                              'timestamp': '2018-12-26 18:23:19.903159',
                              'translation_id': '5aa5b2f39f7254a75bb33'}]

    @classmethod
    def setUpClass(self):
        self.dict_keys = ["timestamp", "translation_id", "source_language", "target_language", "client_name",
                          "event_name", "nr_words", "duration"]
        self.timestamp_error = [{'client_name': 'easyjet',
                                 'duration': 20,
                                 'event_name': 'translation_delivered',
                                 'nr_words': 30,
                                 'source_language': 'en',
                                 'target_language': 'fr',
                                 'timestamp': '2018-12-26',
                                 'translation_id': '5aa5b2f39f7254a75aa5'}]
        self.name_error = [{'client_name': 'easyjet',
                            'duration': 20,
                            'event_name': 'translation_requested',
                            'nr_words': 30,
                            'source_language': 'en',
                            'target_language': 'fr',
                            'timestamp': '2018-12-26 18:11:08.509654',
                            'translation_id': '5aa5b2f39f7254a75aa5'}]
        self.duration_error_1 = [{'client_name': 'easyjet',
                                  'duration': 20.5,
                                  'event_name': 'translation_delivered',
                                  'nr_words': 30,
                                  'source_language': 'en',
                                  'target_language': 'fr',
                                  'timestamp': '2018-12-26 18:11:08.509654',
                                  'translation_id': '5aa5b2f39f7254a75aa5'}]
        self.duration_error_2 = [{'client_name': 'easyjet',
                                  'duration': -1,
                                  'event_name': 'translation_delivered',
                                  'nr_words': 30,
                                  'source_language': 'en',
                                  'target_language': 'fr',
                                  'timestamp': '2018-12-26 18:11:08.509654',
                                  'translation_id': '5aa5b2f39f7254a75aa5'}]
        self.empty_list = []
        self.keys_error = [{'client_name': 'easyjet',
                            'duration': 20,
                            'event_name': 'translation_delivered',
                            'source_language': 'en',
                            'target_language': 'fr',
                            'timestamp': '2018-12-26 18:11:08.509654',
                            'translation_id': '5aa5b2f39f7254a75aa5'}]
        self.events_not_sorted = [{'client_name': 'easyjet',
                                    'duration': 31,
                                    'event_name': 'translation_delivered',
                                    'nr_words': 30,
                                    'source_language': 'en',
                                    'target_language': 'fr',
                                    'timestamp': datetime.datetime(2018, 12, 26, 18, 15, 19, 903159),
                                    'translation_id': '5aa5b2f39f7254a75aa4'},
                                   {'client_name': 'easyjet',
                                    'duration': 20,
                                    'event_name': 'translation_delivered',
                                    'nr_words': 30,
                                    'source_language': 'en',
                                    'target_language': 'fr',
                                    'timestamp': datetime.datetime(2018, 12, 26, 18, 11, 8, 509654),
                                    'translation_id': '5aa5b2f39f7254a75aa5'},
                                   {'client_name': 'booking',
                                    'duration': 54,
                                    'event_name': 'translation_delivered',
                                    'nr_words': 100,
                                    'source_language': 'en',
                                    'target_language': 'fr',
                                    'timestamp': datetime.datetime(2018, 12, 26, 18, 23, 19, 903159),
                                    'translation_id': '5aa5b2f39f7254a75bb33'}]
        self.events_filter_client = [{'client_name': 'booking',
                                      'duration': 54,
                                      'event_name': 'translation_delivered',
                                      'nr_words': 100,
                                      'source_language': 'en',
                                      'target_language': 'fr',
                                      'timestamp': '2018-12-26 18:23:19.903159',
                                      'translation_id': '5aa5b2f39f7254a75bb33'}]
        self.convert_events_timestamp = [{'client_name': 'easyjet',
                                          'duration': 20,
                                          'event_name': 'translation_delivered',
                                          'nr_words': 30,
                                          'source_language': 'en',
                                          'target_language': 'fr',
                                          'timestamp': datetime.datetime(2018, 12, 26, 18, 11, 8, 509654),
                                          'translation_id': '5aa5b2f39f7254a75aa5'},
                                         {'client_name': 'easyjet',
                                          'duration': 31,
                                          'event_name': 'translation_delivered',
                                          'nr_words': 30,
                                          'source_language': 'en',
                                          'target_language': 'fr',
                                          'timestamp': datetime.datetime(2018, 12, 26, 18, 15, 19, 903159),
                                          'translation_id': '5aa5b2f39f7254a75aa4'},
                                         {'client_name': 'booking',
                                          'duration': 54,
                                          'event_name': 'translation_delivered',
                                          'nr_words': 100,
                                          'source_language': 'en',
                                          'target_language': 'fr',
                                          'timestamp': datetime.datetime(2018, 12, 26, 18, 23, 19, 903159),
                                          'translation_id': '5aa5b2f39f7254a75bb33'}]
        self.output_list = [{'average_delivery_time': 0, 'date': datetime.datetime(2018, 12, 26, 18, 11)},
                            {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 12)},
                            {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 13)},
                            {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 14)},
                            {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 15)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 16)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 17)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 18)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 19)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 20)},
                            {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 21)},
                            {'average_delivery_time': 31, 'date': datetime.datetime(2018, 12, 26, 18, 22)},
                            {'average_delivery_time': 31, 'date': datetime.datetime(2018, 12, 26, 18, 23)},
                            {'average_delivery_time': 42.5, 'date': datetime.datetime(2018, 12, 26, 18, 24)}]
        self.output_list_20 = [{'average_delivery_time': 0, 'date': datetime.datetime(2018, 12, 26, 18, 11)},
                                {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 12)},
                                {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 13)},
                                {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 14)},
                                {'average_delivery_time': 20, 'date': datetime.datetime(2018, 12, 26, 18, 15)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 16)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 17)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 18)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 19)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 20)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 21)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 22)},
                                {'average_delivery_time': 25.5, 'date': datetime.datetime(2018, 12, 26, 18, 23)},
                                {'average_delivery_time': 35, 'date': datetime.datetime(2018, 12, 26, 18, 24)}]

    @classmethod
    def tearDownClass(self):
        os.remove('output_file.json')

    def test_check_extension(self):
        result = unbabel_cli.check_extension('events.json', 'input')
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_extension('events.txt', 'input')
            self.assertEqual(cm.exception, 1)

        result = unbabel_cli.check_extension('unbabel_cli_output.json', 'output')
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_extension('unbabel_cli_output', 'output')
            self.assertEqual(cm.exception, 1)

    def test_check_existence(self):
        result = unbabel_cli.check_existence('events.json')
        self.assertTrue(result)

        result = unbabel_cli.check_existence('not_exists.json')
        self.assertFalse(result)

    def test_import_events(self):
        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.import_events('not_exists.json')
            self.assertEqual(cm.exception, 1)

        result = unbabel_cli.import_events('events.json')
        self.assertEqual(result, self.events_list)

        # e.g. file without permission to read
        # with self.assertRaises(SystemExit) as cm:
        #    unbabel_cli.import_events('cannot_read.json')
        #    self.assertEqual(cm.exception, 1)

    def test_check_window_size(self):
        result = unbabel_cli.check_window_size(10)
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_window_size(0)
            self.assertEqual(cm.exception, 1)

    def test_convert_events_timestamp(self):
        result = unbabel_cli.convert_events_timestamp(self.events_list)
        self.assertEqual(result, self.convert_events_timestamp)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.convert_events_timestamp(self.timestamp_error)
            self.assertEqual(cm.exception, 1)

    def test_check_event_name(self):
        result = unbabel_cli.check_event_name(self.events_list)
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_event_name(self.name_error)
            self.assertEqual(cm.exception, 1)

    def test_check_events_durations(self):
        result = unbabel_cli.check_events_durations(self.events_list)
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_events_durations(self.duration_error_1)
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_events_durations(self.duration_error_2)
            self.assertEqual(cm.exception, 1)

    def test_check_events(self):
        result = unbabel_cli.check_events(self.events_list, self.dict_keys)
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_events(self.empty_list, self.dict_keys)
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_events(self.keys_error, self.dict_keys)
            self.assertEqual(cm.exception, 1)

    def test_sort_events_timestamp(self):
        result = unbabel_cli.sort_events_timestamp(self.events_not_sorted)
        self.assertEqual(result, self.convert_events_timestamp)

    def test_check_client(self):
        result = unbabel_cli.check_client(self.events_list, 'booking')
        self.assertEqual(result, self.events_filter_client)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_client(self.events_list, 'uniplaces')
            self.assertEqual(cm.exception, 1)

    def test_check_source_language(self):
        result = unbabel_cli.check_source_language(self.events_filter_client, 'en', 'booking')
        self.assertEqual(result, self.events_filter_client)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_source_language(self.events_filter_client, 'fr', 'booking')
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_source_language(self.events_list, 'fr', None)
            self.assertEqual(cm.exception, 1)

    def test_check_target_language(self):
        result = unbabel_cli.check_target_language(self.events_filter_client, 'fr', 'booking', 'en')
        self.assertEqual(result, self.events_filter_client)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_target_language(self.events_filter_client, 'it', 'booking', 'en')
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_target_language(self.events_filter_client, 'it', None, 'en')
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_target_language(self.events_filter_client, 'it', 'booking', None)
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_target_language(self.events_filter_client, 'it', None, None)
            self.assertEqual(cm.exception, 1)

    def test_filter_events(self):
        result = unbabel_cli.filter_events(self.events_list, 'booking', None, None)
        self.assertEqual(result, self.events_filter_client)

        result = unbabel_cli.filter_events(self.events_list, 'booking', 'en', None)
        self.assertEqual(result, self.events_filter_client)

        result = unbabel_cli.filter_events(self.events_list, 'booking', None, 'fr')
        self.assertEqual(result, self.events_filter_client)

        result = unbabel_cli.filter_events(self.events_list, 'booking', 'en', 'fr')
        self.assertEqual(result, self.events_filter_client)

    def test_find_min_max_timestamp(self):
        result_min, result_max = unbabel_cli.find_min_max_timestamp(self.convert_events_timestamp)
        self.assertEqual(result_min, datetime.datetime(2018, 12, 26, 18, 11))
        self.assertEqual(result_max, datetime.datetime(2018, 12, 26, 18, 24))

    def test_moving_average(self):
        result = unbabel_cli.moving_average(self.convert_events_timestamp, 10)
        print(result)
        self.assertEqual(result, self.output_list)

        result = unbabel_cli.moving_average(self.convert_events_timestamp, 20)
        print(result)
        self.assertEqual(result, self.output_list_20)

    def test_check_output_file(self):
        result = unbabel_cli.check_output_file('output_file.json')
        self.assertEqual(result, None)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_output_file('check_output_file.txt')
            self.assertEqual(cm.exception, 1)

        with self.assertRaises(SystemExit) as cm:
            unbabel_cli.check_output_file('unbabel_cli_output.json')
            self.assertEqual(cm.exception, 1)

    def test_perform_export(self):
        result = unbabel_cli.perform_export(self.output_list, 'output_file.json')
        self.assertEqual(result, None)

        result = unbabel_cli.perform_export(self.output_list, None)
        self.assertEqual(result, None)

        # e.g. folder without permission to write
        # with self.assertRaises(SystemExit) as cm:
        #    unbabel_cli.perform_export(self.output_list, None)
        #    self.assertEqual(cm.exception, 1)


if __name__ == "__main__":
    unittest.main()
