"""
  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import cfnlint.helpers
import json
from cfnlint.rules.resources.properties.Required import Required  # pylint: disable=E0401
from ... import BaseRuleTestCase


class TestResourceConfiguration(BaseRuleTestCase):
    """Test Resource Properties"""
    def setUp(self):
        """Setup"""
        super(TestResourceConfiguration, self).setUp()
        self.collection.register(Required())

    def test_file_positive(self):
        """Test Positive"""
        self.helper_file_positive()

    def test_file_negative(self):
        """Test failure"""
        self.helper_file_negative('fixtures/templates/bad/properties_required.yaml', 12)

    def test_file_negative_generic(self):
        """Generic Test failure"""
        self.helper_file_negative('fixtures/templates/bad/generic.yaml', 8)


class TestSpecifiedCustomResourceRequiredProperties(TestResourceConfiguration):
    """Test Custom Resource Required Properties when override spec is provided"""
    def setUp(self):
        """Setup"""
        super(TestSpecifiedCustomResourceRequiredProperties, self).setUp()
        # Add a Spec override that specifies the Custom::SpecifiedCustomResource type
        with open('fixtures/templates/override_spec/custom.json') as fp:
            custom_spec = json.load(fp)
        cfnlint.helpers.set_specs(custom_spec)
        # Reset Spec override after test
        self.addCleanup(cfnlint.helpers.initialize_specs)

    # ... all TestResourceConfiguration test cases are re-run with override spec ...

    def test_file_negative(self):
        """Test failure"""
        # Additional Custom::SpecifiedCustomResource failure detected with custom spec
        self.helper_file_negative('fixtures/templates/bad/properties_required.yaml', 13)
