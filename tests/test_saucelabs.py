# Joint copyright:
#  - Copyright 2012,2013 Wikimedia Foundation
#  - Copyright 2012,2013 Antoine "hashar" Musso
#  - Copyright 2013 Arnaud Fabre
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from testscenarios.testcase import TestWithScenarios
from testtools import TestCase

from jenkins_jobs.modules import wrappers
from tests.base import BaseTestCase
from tests.base import get_scenarios


class TestCaseModulePublishers(TestWithScenarios, BaseTestCase, TestCase):
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')
    scenarios = get_scenarios(fixtures_path)
    klass = wrappers.Wrappers
