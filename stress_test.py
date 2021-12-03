import sys
from time import sleep, time

import requests


class StressTest:

    def run(self):
        calls_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 100
        print(f'Will call POST no works endpoint {calls_count} times')
        now = time()

        with open('sample/invoice-cs-CZ.pdf', 'br') as file:
            content = file.read()

        last_id = 0
        for ii in range(calls_count):
            files = {'pdf_file': ('foobar.pdf', content, 'application/pdf')}
            response = requests.post('http://0.0.0.0:8000/api/v1/works/', files=files)
            data = response.json()
            if 'id' not in data:
                print((response.status_code, data))
                break
            last_id = data['id']
            if ii % 100 == 0:
                print(f'Called POST on works endpoint {ii} times')

        print(f'Calls finished in {round(time() - now, 2)}s, with {last_id=}')
        if not last_id:
            return

        while True:
            print(f'Waiting for celery to process all works...', end='\r', flush=True)
            response = requests.get(f'http://0.0.0.0:8000/api/v1/works/{last_id}/')
            data = response.json()
            if 'status' not in data:
                print((response.status_code, data))
                break
            if data['status'] == 'done':
                print('')
                print('Done')
                break
            sleep(1)
        print(f'All finished in {round(time() - now, 2)}s')


if __name__ == '__main__':
    StressTest().run()
