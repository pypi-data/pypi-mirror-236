from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.http.http_client import HttpClient
from hackle.internal.http.http_headers import HttpHeaders
from hackle.internal.http.http_response import HttpResponse
from hackle.internal.model.sdk import Sdk
from hackle.internal.workspace.http_workspace_fetcher import HttpWorkspaceFetcher
from tests.resources.test_resource_reader import read_resource


class HttpWorkspaceFetcherTest(TestCase):

    def test__when_exception_on_http_call_then_raise_exception(self):
        # given
        http_client = Mock(spec=HttpClient)
        http_client.execute.side_effect = Mock(side_effect=Exception('fail'))

        # when
        sut = HttpWorkspaceFetcher('localhost', Sdk('test_key', 'test_name', 'test_version'), http_client)
        with self.assertRaises(Exception) as actual:
            sut.fetch_if_modified()

        # then
        self.assertEqual('fail', str(actual.exception))

    def test__when_workspace_config_is_not_modified_then_return_none(self):
        # given
        http_client = Mock(spec=HttpClient)
        http_client.execute.return_value = HttpResponse.of(304)

        # when
        sut = HttpWorkspaceFetcher('localhost', Sdk('test_key', 'test_name', 'test_version'), http_client)
        actual = sut.fetch_if_modified()

        # then
        self.assertIsNone(actual)

    def test__when_http_call_is_not_success_then_raise_exception(self):
        # given
        http_client = Mock(spec=HttpClient)
        http_client.execute.return_value = HttpResponse.of(500)

        # when
        sut = HttpWorkspaceFetcher('localhost', Sdk('test_key', 'test_name', 'test_version'), http_client)
        with self.assertRaises(Exception) as actual:
            sut.fetch_if_modified()

        # then
        self.assertEqual('Http status code: 500', str(actual.exception))

    def test__when_successful_fetch_then_return_workspace(self):
        # given
        http_client = Mock(spec=HttpClient)
        body = read_resource('workspace_config.json')
        http_client.execute.return_value = HttpResponse.of(200, body)

        # when
        sut = HttpWorkspaceFetcher('localhost', Sdk('test_key', 'test_name', 'test_version'), http_client)
        actual = sut.fetch_if_modified()

        # then
        self.assertIsNotNone(actual)
        self.assertIsNotNone(actual.get_experiment_or_none(5))

    def test__last_modified(self):
        http_client = Mock(spec=HttpClient)
        body = read_resource('workspace_config.json')
        http_client.execute.side_effect = [
            HttpResponse.of(200, body,
                            HttpHeaders.builder().add("Last-Modified", "LAST_MODIFIED_HEADER_VALUE").build()),
            HttpResponse.of(304)
        ]

        sut = HttpWorkspaceFetcher('localhost', Sdk('test_key', 'test_name', 'test_version'), http_client)

        self.assertIsNotNone(sut.fetch_if_modified())
        self.assertIsNone(http_client.execute.call_args[0][0].headers.get('If-Modified-Since'))

        self.assertIsNone(sut.fetch_if_modified())
        self.assertEqual('LAST_MODIFIED_HEADER_VALUE',
                         http_client.execute.call_args[0][0].headers.get('If-Modified-Since'))
