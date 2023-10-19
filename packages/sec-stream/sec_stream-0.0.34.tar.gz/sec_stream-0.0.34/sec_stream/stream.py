import requests, json, time, lxml, importlib.resources
from threading import Thread
from bs4 import BeautifulSoup
from sec_stream import tickers  # load tickers (string)

# class to stream company filings from the SEC
class FilingStream(Thread):
    # headers - dict .. companies - dict {'ticker':[forms wanted]} .. delay - float
    def __init__(self, headers={}, companies={}, delay=2, track_all = False, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # make sure companies and formtypes are all uppercase
        self.companies = {key.upper(): [x.upper() for x in value] for key, value in companies.items()}
        self.ciks = self.__match_ciks(self.companies)  # create dict matching cik to ticker
        self.track_all = track_all # track all companies

        self.thread_delay = delay
        self.thread_stop = False
        self.thread_paused = False

        self.latestUrl = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb' \
                         '=&owner=include&start=0&count=40&output=atom'
        self.latestFiling = None
        self.newFilings = []
        self.headers = headers  # need User-Agent to scrape SEC
        if 'User-Agent' not in headers:
            self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
                                         'like Gecko) Chrome/99.0.4844.84 Safari/537.36 '

    # create dict of ciks as keys and tickers as values
    def __match_ciks(self, companies: dict) -> dict:
        cikDict = {}

        data = json.loads(tickers.tickers)
        for ticker in companies:
            if ticker in data:  # key: cik, val: ticker
                cikDict[str(data[ticker]['cik'])] = ticker
            else:
                raise Exception(f"Ticker {ticker} unknown")
        return cikDict

    # grab filings from SEC, if there are new, add them to latestFilings
    def __check_filings(self) -> dict:
        content = requests.get(self.latestUrl, headers=self.headers).content
        soup = BeautifulSoup(content, features='xml')
        filings = soup.find_all('entry')
        if self.latestFiling is None:  # initial entry
            self.latestFiling = filings[0]
            print("setting first initial filing")
        if self.latestFiling == filings[0]:
            return {}  # no new filings return empty

        currentFilings = {}
        for filing in filings:
            if filing == self.latestFiling:  # no more new entries
                break
            cik = str(int(filing.find('id').text.split('-')[1][7:]))

            try:
                if cik in self.ciks or self.track_all:  # check if filing is one we track
                    ticker = self.ciks[cik] if not self.track_all else "forms"
                    title = filing.find('title').text
                    form = title.split('-')[0].strip()
                    acceptedForms = self.companies[ticker] if not self.track_all else []
                    if len(acceptedForms) == 0 or form in acceptedForms or self.track_all:  # check if form is accepted
                        link = filing.find('link')['href']
                        date = filing.find('updated').text
                        if ticker not in currentFilings:
                            currentFilings[ticker] = []
                        currentFilings[ticker].append({'link': link, 'date': date, 'form': form})

            except Exception as e:
                print(e)

        self.latestFiling = filings[0]  # set new latestFiling
        # add to new filings if there are more than one
        if len(currentFilings) > 0:
            self.newFilings.append(currentFilings)

    def run(self):
        while not self.thread_stop:
            while not self.thread_paused:
                self.__check_filings()
                time.sleep(self.thread_delay)
            time.sleep(0.5)

    # stop the thread
    def stop(self):
        self.thread_stop = False

    def pause(self):
        self.thread_paused = True

    def unpause(self):
        self.thread_paused = False

    # return the latest batch of filings
    def get_filings(self) -> dict:
        if len(self.newFilings) == 0:
            return {}  # no new filings
        return self.newFilings.pop(0)

    def test(self):
        print(self.companies)
        print(self.ciks)
        print(self.__check_filings())
        print(self.__check_filings())


if __name__ == '__main__':
    companies = {'aapl': ["10-q"], 'MSFT': [], 'ACAD': []}
    stream = FilingStream(companies=companies, track_all=True)
    stream.start()
    while True:
        filings = stream.get_filings()
        if(len(filings) > 0):
            print(filings)
        time.sleep(5)