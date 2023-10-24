#
# Copyright 2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
from abc import abstractmethod, abstractproperty
import socket

from splunksplwrapper.exceptions.search import SearchFailure
from splunksplwrapper.exceptions.wait import WaitTimedOut
from splunksplwrapper.manager.object import ItemFromManager


class Job(ItemFromManager):
    """
    Job handles the individual searches that spawn jobs. This manager has the
    ability to stop, pause, finalize, etc jobs. You can also retrieve
    different data about the job such as event count.
    """

    _SECONDS_BETWEEN_JOB_IS_DONE_CHECKS = 0.1
    _DEFAULT_TIMEOUT_SECONDS_VALUE = 5400

    @abstractmethod
    def get_results(self, **kwargs):
        pass

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def is_failed(self):
        pass

    @abstractmethod
    def get_messages(self):
        pass

    @abstractproperty
    def sid(self):
        pass

    def wait(self, timeout=None):
        """
        Waits for this search to finish.

        @param timeout: The maximum time to wait in seconds. None or 0
                        means no limit, None is default.
        @type timeout: int
        @return: self
        @rtype: L{SDKJobWrapper}
        @raise WaitTimedOut: If the search isn't done after
                                  C{timeout} seconds.
        """
        self.logger.debug("Waiting for job to finish.")
        if timeout is None or timeout <= 0:
            self.logger.debug("Timeout was set to default one")
            timeout = self._DEFAULT_TIMEOUT_SECONDS_VALUE

        start_time = time.time()
        is_done = False
        while not is_done:
            try:
                is_done = self.is_done()
                if not is_done and self.is_failed():
                    self.logger.warning(
                        f"job {self.sid} failed. error message: {self.get_messages()}"
                    )
                    break
            except AttributeError as e:
                self.logger.debug(str(e))
            except socket.gaierror as e:  # Retry mechanism for temporary network issues
                self.logger.warning(str(e))

            if not is_done:
                _check_if_wait_has_timed_out(start_time, timeout)
                time.sleep(self._SECONDS_BETWEEN_JOB_IS_DONE_CHECKS)

        self.logger.debug("Job %s wait is done." % self.sid)
        return self

    def check_message(self):
        if self.get_messages():
            message = self.get_messages()
            for key in message:
                if key == "error":
                    raise SearchFailure(message[key])


def _check_if_wait_has_timed_out(start_time, timeout):
    if _wait_timed_out(start_time, timeout):
        raise WaitTimedOut(timeout)


def _wait_timed_out(start_time, timeout):
    return time.time() > start_time + timeout
