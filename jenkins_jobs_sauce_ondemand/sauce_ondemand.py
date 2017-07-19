# Copyright 2017 Zendesk, Inc.
# Copyright 2012 Hewlett-Packard Development Company, L.P.

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


"""
Builders define actions that the Jenkins job should execute.  Examples
include shell scripts or maven targets.  The ``builders`` attribute in
the :ref:`Job` definition accepts a list of builders to invoke.  They
may be components defined below, locally defined macros (using the top
level definition of ``builder:``, or locally defined components found
via the ``jenkins_jobs.builders`` entry point.

**Component**: builders
  :Macro: builder
  :Entry Point: jenkins_jobs.builders

Example::

  job:
    name: test_job

    builders:
      - shell: "make test"

"""

import logging
import xml.etree.ElementTree as XML

from jenkins_jobs.errors import InvalidAttributeError
from jenkins_jobs.errors import is_sequence
from jenkins_jobs.errors import JenkinsJobsException
from jenkins_jobs.modules.helpers import convert_mapping_to_xml



logger = logging.getLogger(__name__)


def sauce_ondemand(registry, xml_parent, data):
    """yaml: sauce-ondemand
    Allows you to integrate Sauce OnDemand with Jenkins.  You can
    automate the setup and tear down of Sauce Connect and integrate
    the Sauce OnDemand results videos per test. Requires the Jenkins
    :jenkins-wiki:`Sauce OnDemand Plugin <Sauce+OnDemand+Plugin>`.

    :arg bool enable-sauce-connect: launches a SSH tunnel from their cloud
        to your private network (default false)
    :arg str sauce-host: The name of the selenium host to be used.  For
        tests run using Sauce Connect, this should be localhost.
        ondemand.saucelabs.com can also be used to conenct directly to
        Sauce OnDemand,  The value of the host will be stored in the
        SAUCE_ONDEMAND_HOST environment variable.  (default '')
    :arg str sauce-port: The name of the Selenium Port to be used.  For
        tests run using Sauce Connect, this should be 4445.  If using
        ondemand.saucelabs.com for the Selenium Host, then use 4444.
        The value of the port will be stored in the SAUCE_ONDEMAND_PORT
        environment variable.  (default '')
    :arg bool launch-sauce-connect-on-slave: Whether to launch sauce connect
        on the slave. (default false)
    :arg str sauce-connect-options: Options to pass to sauce connect
        (default '')

    Example::

        wrappers:
          - sauce-ondemand-ng:
              enable-sauce-connect: true
              sauce-host: foo
              sauce-port: 8080
              credentials-id: ad7f5c34-6c5b-11e7-8e08-784f436e5c58
              native-app-package: foo/path
              webdriver-browsers:
                - Linuxfirefox32
                - Linuxfirefox44
              appium-browsers:
                - Linuxfirefox33
                - Linuxfirefox43
              use-latest-webbrowser-versions: false
              launch-sauce-connect-on-slave: true
              verbose-logging: true
              condition: always
              unique-tunnel-perbuild: false
              sauce-connect-path: /bin/sc
              sauce-connect-options: '-N'
    """
    sauce = XML.SubElement(xml_parent, 'hudson.plugins.sauce__ondemand.'
                           'SauceOnDemandBuildWrapper')
    mapping = [
        ('enable-sauce-connect', 'enableSauceConnect', False),
        ('native-app-package', 'nativeAppPackage', ''),
        ('sauce-host', 'seleniumHost', ''),
        ('sauce-port', 'seleniumPort', ''),
        ('credentials-id', 'credentialId', ''),
        ('launch-sauce-connect-on-slave', 'launchSauceConnectOnSlave', False),
        ('sauce-connect-path', 'sauceConnectPath', ''),
        ('sauce-connect-options', 'options', ''),
        ('verbose-logging', 'verboseLogging', False),
        ('use-latest-webbrowser-versions', 'useLatestVersion', False),
        ('unique-tunnel-perbuild', 'useGeneratedTunnelIdentifier', False),
    ]
    convert_mapping_to_xml(sauce, data, mapping, fail_required=True)

    webdriver_browsers = XML.SubElement(sauce, 'webDriverBrowsers')
    for browser in data.get('webdriver-browsers', []):
        XML.SubElement(webdriver_browsers, 'string').text = browser

    appium_browsers = XML.SubElement(sauce, 'appiumBrowsers')
    for browser in data.get('appium-browsers', []):
        XML.SubElement(appium_browsers, 'string').text = browser

    kind = data.get('condition', 'always')
    ctag = XML.SubElement(sauce, 'condition')
    core_prefix = 'org.jenkins_ci.plugins.run_condition.core.'
    if kind == "always":
        ctag.set('class', core_prefix + 'AlwaysRun')
    else:
        supportedConditions = ['always']
        raise InvalidAttributeError('condition',
                                    condition,
                                    )
