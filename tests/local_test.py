import unittest
import os

from prudentia.domain import Box
from prudentia.local import LocalProvider


class TestLocalProvider(unittest.TestCase):
    def setUp(self):
        self.tests_path = os.path.dirname(os.path.realpath(__file__))
        self.provider = LocalProvider()

    def test_provision_sample_task(self):
        r_box = Box('local-testbox', self.tests_path + '/../examples/boxes/tasks.yml', 'tasks-host', '127.0.0.1')
        self.provider.add_box(r_box)

        self.provider.provision(r_box)
        self.assertEqual(self.provider.provisioned, True)

        self.provider.provision(r_box, 'uname', 'shuffle')
        self.assertEqual(self.provider.provisioned, True)

        self.provider.remove_box(r_box)

    def test_should_list_tag(self):
        e_box = Box('simple-box', self.tests_path + '/dev.yml', 'hostname', '0.0.0.0')
        self.provider.load_tags(e_box)
        self.assertEqual(self.provider.tags.has_key(e_box.name), True)
        self.assertEqual(self.provider.tags[e_box.name], ['one'])

    def test_should_not_list_tags_if_box_not_exists(self):
        ne_box = Box('simple-box-2', 'xxx.yml', 'ssh-hostname', '0.0.0.0')
        self.provider.load_tags(ne_box)
        self.assertEqual(self.provider.tags.has_key(ne_box.name), False)

    def test_set_var(self):
        var_name = 'var_name'
        var_value = 'var_value'
        self.provider.set_var(var_name, var_value)
        self.assertEqual(self.provider.extra_vars[var_name], var_value)
        var_overwritten = "var_overwritten"
        self.provider.set_var(var_name, var_overwritten)
        self.assertEqual(self.provider.extra_vars[var_name], var_overwritten)
