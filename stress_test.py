import requests


class StressTest:

    def run(self):
        with open('sample/invoice-cs-CZ.pdf', 'br') as file:
            content = file.read()
        for ii in range(1000):
            files = {'pdf_file': ('foobar.pdf', content, 'application/pdf')}
            response = requests.post('http://0.0.0.0:8000/api/v1/works/', files=files)
            print((response.status_code, response.json()))


if __name__ == '__main__':
    StressTest().run()
