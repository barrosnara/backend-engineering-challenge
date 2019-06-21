import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from statistics import mean


def check_extension(filename, file_type):
    """
    :param filename: path of the file to be analysed
    :param file_type: states if we are analysing an input or a output file
    :return: an assertion error if the analysed file extension is not .json
    """
    try:
        assert filename.lower().endswith(".json")
    except AssertionError:
        print('Error! ' + file_type + ' file must be a json file')
        sys.exit(1)


def check_existence(filename):
    """
    :param filename: path of the file to be analysed
    :return: if the file exists or nor
    """
    return os.path.exists(filename)


def import_events(input_file):
    """
    :param input_file: path of the file to be analysed
    :return: (executes check extension)
             a message error if the input file does not exist;
             a IOError if the json file cannot be open/read;
             a list of dict containing the content of the input file, otherwise
    """
    imported_list = []
    check_extension(input_file, 'input')
    if not check_existence(input_file):
        print('Error! input file ' + input_file + ' does not exist')
        sys.exit(1)
    try:
        with open(input_file) as f:
            for line in f:
                imported_list.append(json.loads(line))
        return imported_list
    except IOError:
        print("Error! cannot open/read input file")
        sys.exit(1)


def check_window_size(window_size):
    """
    :param window_size: time window to be considered in the moving average calculation
    :return: an error message if its value is not a positive integer
    """
    if window_size <= 0:
        print("Error! window size must be greater than 0")
        sys.exit(1)


def convert_events_timestamp(events_list):
    """
    :param events_list: list of dict without properly formatted timestamps
    :return: list of dict with formatted timestamps: %Y-%m-%d %H:%M:%S.%f;
             an ValueError if it is not possible (i.e. the conversion failed)
    """
    try:
        for event in events_list:
            event['timestamp'] = datetime.strptime(str(event['timestamp']), '%Y-%m-%d %H:%M:%S.%f')
        return events_list
    except ValueError as ve:
        print("Error! cannot convert timestamp string to a valid datetime: " + str(ve))
        sys.exit(1)


def check_event_name(events_list):
    """
    :param events_list: list of dict to be analysed
    :return: an error message if a dict entry has event name diff than translation_delivered
    """
    for event in events_list:
        if event['event_name'] != 'translation_delivered':
            print("Error! input file should only contain translations delivered: " + event['event_name'])
            sys.exit(1)


def check_events_durations(events_list):
    """
    :param events_list: list of dict to be analysed
    :return: an error message if an dict entry has a duration which is not a non-negative int
    """
    for event in events_list:
        if event['duration'] >= 0 and isinstance(event['duration'], int):
            pass
        else:
            print("Error! duration has to be a non-negative integer: " + str(event['duration']))
            sys.exit(1)


def check_events(events_list, dict_keys_list):
    """
    :param events_list: list of dict to be analysed
    :param dict_keys_list: keys that the dict entries must have
    :return: an error message if the list is empty;
             an error message if the list of dict does not follow the expected structure (i.e. contains all keys);
             the execution of convert event timestamp and check event name and durations, otherwise
    """
    if not events_list:
        print("Error! input file is empty")
        sys.exit(1)
    else:
        for event in events_list:
            if all(key in event for key in dict_keys_list):
                events_list = convert_events_timestamp(events_list)
                check_event_name(events_list)
                check_events_durations(events_list)
            else:
                print("Error! input file does not follow the expected structure: " + str(event))
                sys.exit(1)


def sort_events_timestamp(events_list):
    """
    :param events_list: list of dict to be analysed
    :return: param sorted per timestamp
    """
    events_list_sorted = sorted(events_list, key=lambda k: k['timestamp'])
    return events_list_sorted


def check_client(events_list, client_name):
    """
    :param events_list: list of dict to be analysed
    :param client_name: client name to filter events
    :return: list of dict filtered by the specified client name;
             an error message if no event meets the condition
    """
    events_list_filtered = list(filter(lambda event: event['client_name'] == client_name, events_list))
    if len(events_list_filtered) > 0:
        return events_list_filtered
    else:
        print("Error! no results found for client name " + client_name)
        sys.exit(1)


def check_source_language(events_list, source_language, client_name):
    """
    :param events_list: list of dict to be analysed
    :param source_language: source language to filter events
    :param client_name: client name used to filter events, if it has been
    :return: list of dict filtered by source language;
             an error message if no event meets the condition(s)
    """
    events_list_filtered = list(filter(lambda event: event['source_language'] == source_language, events_list))
    if len(events_list_filtered) > 0:
        return events_list_filtered
    else:
        if client_name is not None:
            print("Error! no results found for client name " + client_name + ' and source language ' + source_language)
        else:
            print("Error! no results found for source language " + source_language)
        sys.exit(1)


def check_target_language(events_list, target_language, client_name, source_language):
    """
    :param events_list: list of dict to be analysed
    :param target_language: target language to filter events
    :param client_name: client name used to filter events, if it has been
    :param source_language: source language used to filter events, if it has been
    :return: list of dict filtered by target language;
             an error message if no event meets the condition(s)
    """
    events_list_filtered = list(filter(lambda event: event['target_language'] == target_language, events_list))
    if len(events_list_filtered) > 0:
        return events_list_filtered
    else:
        if client_name is not None or source_language is not None:
            if client_name is not None:
                if source_language is not None:
                    print("Error! no results found for client name " + client_name + ', source language ' +
                          source_language + ' and target language ' + target_language)
                else:
                    print("Error! no results found for client name " + client_name + ' and target language ' +
                          target_language)
            else:
                print("Error! no results found for source language " + source_language + ' and target language ' +
                      target_language)
        else:
            print("Error! no results found for target language " + target_language)
        sys.exit(1)


def filter_events(events_list, client_name, source_language, target_language):
    """
    :param events_list: list of dict to be analysed
    :param client_name: client name to filter events
    :param source_language: source language to filter events
    :param target_language: target language to filter events
    :return: (executes event filtering based on user selection)
             a list of dict filtered by client name, source and target languages (when requested)
    """
    events_list_filtered = events_list
    if client_name is not None:
        events_list_filtered = check_client(events_list_filtered, client_name)
    if source_language is not None:
        events_list_filtered = check_source_language(events_list_filtered, source_language, client_name)
    if target_language is not None:
        events_list_filtered = check_target_language(events_list_filtered, target_language, client_name,
                                                     source_language)
    return events_list_filtered


def find_min_max_timestamp(events_list):
    """
    :param events_list: list of dict to be analysed
    :return: the time range to be considered in the moving average calculation:
             min timestamp - oldest value of timestamp events (truncated to minutes)
             max timestamp - newest value of timestamp events + 1 (truncated to minutes)
    """
    timestamps_list = [event['timestamp'] for event in events_list]
    min_timestamp = min(timestamps_list).replace(second=0, microsecond=0)
    max_timestamp = max(timestamps_list).replace(second=0, microsecond=0) + timedelta(seconds=60)
    return min_timestamp, max_timestamp


def moving_average(events_list, window_size):
    """
    :param events_list: list of dict to be analysed
    :param window_size: time window (in minutes) to be considered on the moving average calculation
    :return: (executes the function which determines the time range to be analysed)
             a list of dict containing the aggregated output (average delivery time per minute)
    """
    results_list = []
    min_timestamp, max_timestamp = find_min_max_timestamp(events_list)
    iterator = min_timestamp
    while iterator <= max_timestamp:
        events_on_window_size = list(filter(lambda event: iterator - timedelta(seconds=window_size * 60)
                                                          <= event['timestamp'] <= iterator, events_list))
        average_delivery_time = 0
        if len(events_on_window_size) > 0:
            average_delivery_time = mean(event['duration'] for event in events_on_window_size)
        dict_entry = {'date': iterator, 'average_delivery_time': average_delivery_time}
        results_list.append(dict_entry)
        iterator = iterator + timedelta(seconds=60)
    return results_list


def check_output_file(output_file):
    """
    :param output_file: path to where the results gonna be exported
    :return: (executes de extension checker)
             an error message if the selected output file already exists (does not overwrite)
    """
    check_extension(output_file, 'output')
    if check_existence(output_file):
        print('Error! output file ' + output_file + ' already exists')
        sys.exit(1)


def perform_export(results_list, output_file):
    """
    :param results_list: list of dict containing the aggregated output (average delivery time per list)
    :param output_file: path to where the results gonna be exported
    :return: export results to unbabel_cli_output.json, if the user did not select an output file path
             (overwrite if the file already exists);
             exports to the user selection (after executing the output file checker), otherwise;
             an IOError message if it cannot open/write the output file
    """
    if output_file is None:
        output_file = "unbabel_cli_output.json"
    else:
        check_output_file(output_file)
    try:
        with open(output_file, 'w') as outfile:
            for line in results_list:
                json.dump(line, outfile, default=str)
                outfile.write('\n')
    except IOError:
        print("Error! cannot open/write output file")
        sys.exit(1)


if __name__ == '__main__':
    # initialize keys which define the dict structure
    dict_keys = ["timestamp", "translation_id", "source_language", "target_language", "client_name", "event_name",
                 "nr_words", "duration"]

    # create parser to read arguments from command line
    parser = argparse.ArgumentParser()
    # add the input arguments
    parser.add_argument('--input_file', required=True, type=str, dest="input_file",
                        help="path to a json file containing the stream of events to be analysed")
    parser.add_argument('--window_size', required=True, type=int, dest="window_size",
                        help="time window (in minutes) to be considered on the moving average calculation")
    parser.add_argument('--output_file', default=None, type=str, dest="output_file",
                        help="path to where the aggregated output is going to be export (json file)")
    parser.add_argument('--client_name', default=None, type=str, dest="client_name",
                        help="specify a client name in order to calculated his KPI")
    parser.add_argument("--source_language", default=None, type=str, dest="source_language",
                        help="specify a source language in order to calculate its KPI ")
    parser.add_argument("--target_language", default=None, type=str, dest="target_language",
                        help="specify a target language in order to calculate its KPI")

    args = parser.parse_args()

    # import events
    events = import_events(args.input_file)
    # check required args values
    check_window_size(args.window_size)
    check_events(events, dict_keys)
    # sort events based on timestamp
    events = sort_events_timestamp(events)
    # filter events based on optional args
    events = filter_events(events, args.client_name, args.source_language, args.target_language)
    # calculates the KPI
    results = moving_average(events, args.window_size)
    # exports results to json file
    perform_export(results, args.output_file)
