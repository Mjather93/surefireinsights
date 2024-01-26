"""
 Collect performance data using psutil which has cross-platform compatibility.
 Author: Dan Corless
 Version: 0.0.1
 https://psutil.readthedocs.io/en/latest
"""
import traceback
import datetime
import logging
import multiprocessing
import time
import process_metrics
from get_report_fk import report_fk


def execute_process_metrics(
        args,
        interval,
        end_time,
        threads
):
    args = args.split(',')
    criteria = args[1]
    print(interval, end_time, threads)
    # start finding process ids where the process matches the criteria.
    extractor = process_metrics.ProcessPerformanceExtractor(criteria)
    matching_ids = extractor.get_matching_process_ids()
    # start a loop and a threadpool to find process id information.
    finished = False
    logging.info(f"The monitoring will run until: {end_time}")
    try:
        while not finished:
            current_time = datetime.datetime.now()
            if current_time >= end_time:
                finished = True
                break
            with multiprocessing.Pool(processes=threads) as pool:
                metrics_data = pool.starmap(process_metrics.ProcessPerformanceExtractor.collect_metrics,
                                            [(process, criteria) for process in matching_ids])
            # Flatten the list of lists to prepare for the insert.
            flat_metrics_data = [item for sublist in metrics_data for item in sublist]
            print(flat_metrics_data)
            # insert the data into the DB
            process_metrics.ProcessPerformanceExtractor.insert_into_database(flat_metrics_data, report_fk)
            print(f"Waiting between polls for {interval} seconds.")
            time.sleep(interval)
    except Exception as e:
        logging.error(f"Error raised: {e}")
        logging.error(traceback.print_stack())
