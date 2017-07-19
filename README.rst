Jenkins Job Builder SauceLabs Ondemand
--------------------------------------

A `Jenkins Job Builder` plugin to support configuring the `SourceLabs Ondemand` build wrapper:

.. code-block:: yaml

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

License
-------

Copyright 2017 Zendesk Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

.. _Jenkins Job Builder: https://docs.openstack.org/infra/jenkins-job-builder/
.. _Allure: http://allure.qatools.ru/
