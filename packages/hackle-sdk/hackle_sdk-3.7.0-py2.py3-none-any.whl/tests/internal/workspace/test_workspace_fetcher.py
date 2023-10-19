import time
from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.concurrent.schedule.thread_scheduler import ThreadScheduler
from hackle.internal.workspace.http_workspace_fetcher import HttpWorkspaceFetcher
from hackle.internal.workspace.workspace import Workspace
from hackle.internal.workspace.workspace_fetcher import WorkspaceFetcher


class WorkspaceFetcherTest(TestCase):

    def setUp(self):
        self.http_workspace_fetcher = Mock(spec=HttpWorkspaceFetcher)
        self.http_workspace_fetcher.fetch_if_modified.return_value = None

    def __workspace_fetcher(
            self,
            http_workspace_fetcher=None,
            scheduler=ThreadScheduler(),
            polling_interval_seconds=10.0
    ):
        return WorkspaceFetcher(
            http_workspace_fetcher or self.http_workspace_fetcher,
            scheduler,
            polling_interval_seconds)

    def test__fetch__when_before_poll_then_return_none(self):
        # given
        sut = self.__workspace_fetcher()

        # when
        actual = sut.fetch()

        # then
        self.assertIsNone(actual)

    def test__fetch__when_workspace_is_fetched_then_return_that_workspace(self):
        # given
        workspace = Mock(spec=Workspace)
        self.http_workspace_fetcher.fetch_if_modified.return_value = workspace
        sut = self.__workspace_fetcher()

        # when
        sut.start()
        actual = sut.fetch()

        # then
        self.assertEqual(workspace, actual)

    def test__poll__fail_to_poll(self):
        # given
        self.http_workspace_fetcher.fetch_if_modified.side_effect = Mock(side_effect=Exception('fail'))
        sut = self.__workspace_fetcher()

        # when
        sut.start()
        actual = sut.fetch()

        # then
        self.assertIsNone(actual)

    def test__poll__success_to_poll(self):
        # given
        workspace = Mock(spec=Workspace)
        self.http_workspace_fetcher.fetch_if_modified.return_value = workspace
        sut = self.__workspace_fetcher()

        # when
        sut.start()
        actual = sut.fetch()

        # then
        self.assertEqual(workspace, actual)

    def test__poll__workspace_not_modified(self):
        # given
        workspace = Mock(spec=Workspace)
        self.http_workspace_fetcher.fetch_if_modified.side_effect = [workspace, None, None, None]
        sut = self.__workspace_fetcher(polling_interval_seconds=0.1)

        # when
        sut.start()
        time.sleep(0.35)
        actual = sut.fetch()

        # then
        self.assertEqual(workspace, actual)

    def test__start___poll(self):
        # given
        workspace = Mock(spec=Workspace)
        self.http_workspace_fetcher.fetch_if_modified.return_value = workspace
        sut = self.__workspace_fetcher()

        # when
        sut.start()
        actual = sut.fetch()

        # then
        self.assertEqual(workspace, actual)

    def test__start__scheduling(self):
        # given
        workspace = Mock(spec=Workspace)
        self.http_workspace_fetcher.fetch_if_modified.return_value = workspace
        sut = self.__workspace_fetcher(polling_interval_seconds=0.1)

        # when
        sut.start()
        time.sleep(0.55)

        # then
        self.assertEqual(6, self.http_workspace_fetcher.fetch_if_modified.call_count)
