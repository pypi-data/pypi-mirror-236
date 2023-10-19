from unittest import TestCase, mock
from unittest.mock import Mock

from hackle.internal.http.http_client import HttpClient
from hackle.internal.http.http_request import HttpRequest
from hackle.internal.model.sdk import Sdk
from tests.internal.time.test_clock import FixedClock


class HttpClientTest(TestCase):

    @mock.patch('requests.request')
    def test_execute(self, mock_request):
        # given
        sdk = Sdk('test_key', 'test_name', 'test_version')
        clock = FixedClock(42, 43)
        sut = HttpClient(sdk, clock)

        response = Mock()
        response.status_code = 200
        response.content = bytes("{'a': 'b'}", 'utf-8')
        response.headers = {}

        mock_request.return_value = response

        request = HttpRequest.builder().url('localhost').build()

        # when
        actual = sut.execute(request)

        # then
        self.assertEqual(200, actual.status_code)
        self.assertEqual("{'a': 'b'}", actual.body)
        args = mock_request.call_args
        self.assertEqual('GET', args[0][0])
        self.assertEqual('localhost', args[0][1])
        self.assertEqual(
            {
                'X-HACKLE-SDK-KEY': 'test_key',
                'X-HACKLE-SDK-NAME': 'test_name',
                'X-HACKLE-SDK-VERSION': 'test_version',
                'X-HACKLE-SDK-TIME': '42'
            },
            args[1]['headers']
        )
        self.assertEqual(10, args[1]['timeout'])
