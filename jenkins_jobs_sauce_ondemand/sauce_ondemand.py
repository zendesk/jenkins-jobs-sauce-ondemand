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
    :arg str override-username: If set then api-access-key must be set.
        Overrides the username from the global config. (default '')
    :arg str override-api-access-key: If set then username must be set.
        Overrides the api-access-key set in the global config. (default '')
    :arg str starting-url: The value set here will be stored in the
        SELENIUM_STARTING_ULR environment variable.  Only used when type
        is selenium. (default '')
    :arg str type: Type of test to run (default selenium)

        :type values:
          * **selenium**
          * **webdriver**
    :arg list platforms: The platforms to run the tests on.  Platforms
        supported are dynamically retrieved from sauce labs.  The format of
        the values has only the first letter capitalized, no spaces, underscore
        between os and version, underscore in internet_explorer, everything
        else is run together.  If there are not multiple version of the browser
        then just the first version number is used.
        Examples: Mac_10.8iphone5.1 or Windows_2003firefox10
        or Windows_2012internet_explorer10 (default '')
    :arg bool launch-sauce-connect-on-slave: Whether to launch sauce connect
        on the slave. (default false)
    :arg str https-protocol: The https protocol to use (default '')
    :arg str sauce-connect-options: Options to pass to sauce connect
        (default '')

    Example::

      wrappers:
        - sauce-ondemand:
            enable-sauce-connect: true
            sauce-host: foo
            sauce-port: 8080
            override-username: foo
            override-api-access-key: 123lkj123kh123l;k12323
            type: webdriver
            platforms:
              - Linuxandroid4
              - Linuxfirefox10
              - Linuxfirefox11
            launch-sauce-connect-on-slave: true
    """
    sauce = XML.SubElement(xml_parent, 'hudson.plugins.sauce__ondemand.'
                           'SauceOnDemandBuildWrapper')
    XML.SubElement(sauce, 'enableSauceConnect').text = str(data.get(
        'enable-sauce-connect', False)).lower()
    host = data.get('sauce-host', '')
    XML.SubElement(sauce, 'seleniumHost').text = host
    port = data.get('sauce-port', '')
    XML.SubElement(sauce, 'seleniumPort').text = port
    # Optional override global authentication
    username = data.get('override-username')
    key = data.get('override-api-access-key')
    if username and key:
        cred = XML.SubElement(sauce, 'credentials')
        XML.SubElement(cred, 'username').text = username
        XML.SubElement(cred, 'apiKey').text = key
    atype = data.get('type', 'selenium')
    info = XML.SubElement(sauce, 'seleniumInformation')
    if atype == 'selenium':
        url = data.get('starting-url', '')
        XML.SubElement(info, 'startingURL').text = url
        browsers = XML.SubElement(info, 'seleniumBrowsers')
        for platform in data['platforms']:
            XML.SubElement(browsers, 'string').text = platform
        XML.SubElement(info, 'isWebDriver').text = 'false'
        XML.SubElement(sauce, 'seleniumBrowsers',
                       {'reference': '../seleniumInformation/'
                        'seleniumBrowsers'})
    if atype == 'webdriver':
        browsers = XML.SubElement(info, 'webDriverBrowsers')
        for platform in data['platforms']:
            XML.SubElement(browsers, 'string').text = platform
        XML.SubElement(info, 'isWebDriver').text = 'true'
        XML.SubElement(sauce, 'webDriverBrowsers',
                       {'reference': '../seleniumInformation/'
                        'webDriverBrowsers'})
    XML.SubElement(sauce, 'launchSauceConnectOnSlave').text = str(data.get(
        'launch-sauce-connect-on-slave', False)).lower()
    protocol = data.get('https-protocol', '')
    XML.SubElement(sauce, 'httpsProtocol').text = protocol
    options = data.get('sauce-connect-options', '')
    XML.SubElement(sauce, 'options').text = options
