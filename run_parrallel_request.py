import logging
import multiprocessing
import time
import pandas as pd
import requests
import os

warray = []
result_queue = []
# Number of requests you want to simulate
num_iteration = 50


def run_requests(file_name, r_no, ls, link="https://rogue-gamer-ryt.github.io/react-foreign-exchange/"):
    """
    function to download a particular file
    """
    try:
        # Giving cookies obtained from the browser post log in
        headers = {
            "Cookie": "csrftoken=ARKbU6sCkVJKKD6taM7L5x3ju1YCutyv0JptLxzBLCXr7ejSCyepcMMzRTlU61Bz;",
            'Accept-Encoding': None
        }
        start_process = time.clock()
        response = requests.get(link, stream=True, headers=headers, verify=False)
        response_recieved = time.clock()
        # Downloading the static file
        with open(file_name, "wb") as py_js:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    py_js.write(chunk)
        file_written = time.clock()
        server_wait_time = response_recieved - start_process
        download_time = file_written - response_recieved
        print(f"Server wait time: {server_wait_time}s")
        print(f"Download Time:  {download_time}s")
        ls.append(["Request: " + str(r_no), server_wait_time, download_time])
        # Deletes the downloaded file
        os.remove(file_name)
        print("\n")
    except Exception as e:
        logging.error("Unable to access link %s" % str(e))
    result_queue.append(1)


if __name__ == "__main__":
    mgr = multiprocessing.Manager()
    ls = mgr.list()
    link = ""
    for i in range(num_iteration):
        p1 = multiprocessing.Process(target=run_requests, args=("s{}.js".format(str(i)), i + 1, ls))
        warray.append(p1)
    for i in warray:
        i.start()
    for i in warray:
        i.join()
    # Columns to be populated for the report generated post running the load test
    df = pd.DataFrame(list(ls), columns=["Request No.", "Server wait time", "Download time"])
    writer = pd.ExcelWriter('requests_analysis.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    print("Done!")
