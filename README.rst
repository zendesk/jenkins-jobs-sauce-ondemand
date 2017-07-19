Jenkins Job Builder SauceLabs Ondemand
--------------------------------------

A `Jenkins Job Builder` plugin to support configuring the `Allure` reports publisher:

.. code-block:: yaml

    publishers:
      - allure:
          results:
            - results/allure-results
          properties:
            allure.issues.tracker.pattern: "http://github.com/allure-framework/allure-core/issues/%s"
          build-policy: unstable
          include-properties: false

License
-------

Copyright 2017 Zendesk Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

.. _Jenkins Job Builder: https://docs.openstack.org/infra/jenkins-job-builder/
.. _Allure: http://allure.qatools.ru/
