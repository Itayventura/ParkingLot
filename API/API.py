import requests
import json
import os

API_KEY = '4fa757bfab88957'
# API_KEY = '814a6f074588957'


class Language:
    Arabic = 'ara'
    Bulgarian = 'bul'
    Chinese_Simplified = 'chs'
    Chinese_Traditional = 'cht'
    Croatian = 'hrv'
    Danish = 'dan'
    Dutch = 'dut'
    English = 'eng'
    Finnish = 'fin'
    French = 'fre'
    German = 'ger'
    Greek = 'gre'
    Hungarian = 'hun'
    Korean = 'kor'
    Italian = 'ita'
    Japanese = 'jpn'
    Norwegian = 'nor'
    Polish = 'pol'
    Portuguese = 'por'
    Russian = 'rus'
    Slovenian = 'slv'
    Spanish = 'spa'
    Swedish = 'swe'
    Turkish = 'tur'


class API:
    def __init__(
            self, api_key=API_KEY, overlay=False, language=Language.English, **kwargs
    ):
        """
        :param api_key: API key string
        :param language: document language
        :param **kwargs: other settings to API
        """
        self.payload = {
            'isOverlayRequired': overlay,
            'apikey': api_key,
            'language': language,
            **kwargs
        }

    def ocr_file(self, fp):
        """ :param fp: Your file path & name.
            :return: parsed text from image - plate number identified from the picture.
            """
        if not os.path.exists(fp):
            return ""
        with open(fp, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={fp: f},
                              data=self.payload,
                              )
            json_data = json.loads(r.text)
            parsedResults = json_data.get('ParsedResults')
            if parsedResults:
                for elem in json_data.get('ParsedResults'):
                    return elem.get('ParsedText')
        return ""

    def ocr_url(self, url):
        """
        :param url: Image url.
        :return: parsed text from image - identified plate number.
        """

        payload = {'url': url,
                   'isOverlayRequired': self.payload['isOverlayRequired'],
                   'apikey': self.payload['apikey'],
                   'language': self.payload['language'],
                   }
        r = requests.post('https://api.ocr.space/parse/image',
                          data=payload,
                          )
        json_data = json.loads(r.text)
        parsedResults = json_data.get('ParsedResults')
        if parsedResults:
            for elem in json_data.get('ParsedResults'):
                return elem.get('ParsedText')
        return ""
