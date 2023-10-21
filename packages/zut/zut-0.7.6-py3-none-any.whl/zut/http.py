from __future__ import annotations
import json
import logging
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zut.json import ExtendedJSONDecoder, ExtendedJSONEncoder

class JSONApiClient:
    base_url : str = None
    _force_trailing_slash: bool = False

    _default_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json; charset=utf-8',
    }

    _json_encoder_cls: type[json.JSONEncoder] = ExtendedJSONEncoder
    _json_decoder_cls: type[json.JSONDecoder] = ExtendedJSONDecoder
    
    _nonjson_error_maxlen = 400


    def __init__(self):
        self.logger = logging.getLogger(type(self).__module__ + '.' + type(self).__name__)


    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        pass


    def get(self, endpoint: str, *, params: dict = None):
        return self.request(endpoint, params=params)


    def post(self, endpoint: str, data, *, params: dict = None):
        return self.request(endpoint, data, params=params)
    

    def request(self, endpoint: str, data = None, *, method = None, params: dict = None):
        url = self._prepare_url(endpoint, params)

        headers = {**self._default_headers}

        authorization = self._get_authorization(url)
        if authorization:
            headers['Authorization'] = authorization
        
        if data is not None:
            if not method:
                method = 'POST'
            
            self.logger.debug(f'{method} {url}')
            request = Request(url,
                method=method,
                headers=headers,
                data=json.dumps(data, ensure_ascii=False, cls=self._json_encoder_cls).encode('utf-8'),
            )
        else:
            if not method:
                method = 'GET'
            
            self.logger.debug(f'{method} {url}')
            request = Request(url,
                method=method,
                headers=headers,
            )

        try:
            with urlopen(request) as response:
                return self._decode_response(response)
        except HTTPError as error:
            with error:
                http_data = self._decode_response(error)
            built_error = self._build_client_error(error, http_data)
        except URLError as error:
            built_error = self._build_client_error(error, None)

        if isinstance(built_error, Exception):
            raise built_error from None
        else:
            return built_error


    def _prepare_url(self, endpoint: str, params: dict = None):
        if '://' in endpoint:
            url = endpoint
        else:
            if not self.base_url:
                raise ValueError(f"invalid endpoint \"{endpoint}\": missing `base_url` attribute?")
            
            if endpoint.startswith('/'):
                if self.base_url.endswith('/'):                    
                    endpoint = endpoint[1:]
            else:
                if not self.base_url.endswith('/'):
                    endpoint = f'/{endpoint}'
            
            if getattr(self, '_force_trailing_slash', False) and not endpoint.endswith('/'):
                endpoint = f'{endpoint}/'

            url = f'{self.base_url}{endpoint}'

        if params:
            url += "?" + urlencode(params)
        
        return url
    

    def _get_authorization(self, url: str) -> str|None:
        pass


    def _decode_response(self, response):
        rawdata = response.read()
        try:
            strdata = rawdata.decode('utf-8')
        except UnicodeDecodeError:
            strdata = str(rawdata)
            if len(strdata) > self._nonjson_error_maxlen:
                strdata = strdata[0:self._nonjson_error_maxlen] + '…'
            return f"[non-utf-8] {strdata}"
        
        try:
            jsondata = json.loads(strdata, cls=self._json_decoder_cls)
        except json.JSONDecodeError:
            if len(strdata) > self._nonjson_error_maxlen:
                strdata = strdata[0:self._nonjson_error_maxlen] + '…'
            return f"[non-json] {strdata}"
        
        return jsondata


    def _build_client_error(self, error: URLError, http_data):
        if isinstance(error, HTTPError):
            return ApiClientError(error.reason, code=error.status, code_nature='status', data=http_data)
        else:
            return ApiClientError(error.reason, code=error.errno, code_nature='errno', data=http_data)
        

class ApiClientError(Exception):
    def __init__(self, message: str, *, code: int = None, code_nature = None, data = None):
        self.raw_message = message
        self.code = code
        self.code_nature = code_nature
        self.data = data

        super().__init__(self._raw_to_message())


    def _raw_to_message(self):
        message = self.raw_message

        if self.code:
            message = (message + ' ' if message else '') + f"[{self.code_nature or 'code'}: {self.code}]"
        
        if self.data:
            if isinstance(self.data, dict):
                for key, value in self.data.items():
                    message = (message + '\n' if message else '') + f"{key}: {value}"
            else:
                message = (message + '\n' if message else '') + str(self.data)

        return message
