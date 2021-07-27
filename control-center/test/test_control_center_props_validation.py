import unittest
from unittest.mock import patch
from jinja2 import Environment, FileSystemLoader
import confluent.docker_utils.dub as dub
import os
import random

# complete set
basic_props = dict(
    CONTROL_CENTER_BOOTSTRAP_SERVERS="bootstrap.servers",
    CONTROL_CENTER_ZOOKEEPER_CONNECT="zookeeper.connect",
    CONTROL_CENTER_DATA_DIR="confluent.controlcenter.data.dir"
)

# complete set
rf_props = dict(
    CONTROL_CENTER_INTERNAL_TOPICS_REPLICATION="confluent.controlcenter.internal.topics.replication",
    CONTROL_CENTER_COMMAND_TOPIC_REPLICATION="confluent.controlcenter.command.topic.replication",
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_REPLICATION="confluent.monitoring.interceptor.topic.replication",
    CONTROL_CENTER_METRICS_TOPIC_REPLICATION="confluent.metrics.topic.replication",
)

# complete set
required_props = {**basic_props, **rf_props}

# complete set
monitoring_props = dict(
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC="confluent.monitoring.interceptor.topic",
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS="confluent.monitoring.interceptor.topic.partitions",
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_RETENTION_MS="confluent.monitoring.interceptor.topic.retention.ms",
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_SKIP_BACKLOG_MINUTES="confluent.monitoring.interceptor.topic.skip.backlog.minutes"
)

# complete set
remaining_control_center_metrics_props = dict(
    CONTROL_CENTER_METRICS_TOPIC="confluent.metrics.topic",
    CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS="confluent.metrics.topic.retention.ms",
    CONTROL_CENTER_METRICS_TOPIC_PARTITIONS="confluent.metrics.topic.partitions",
    CONTROL_CENTER_METRICS_TOPIC_SKIP_BACKLOG_MINUTES="confluent.metrics.topic.skip.backlog.minutes"
)

# complete set
confluent_metrics_props = dict(
    CONFLUENT_METRICS_TOPIC="confluent.metrics.topic",
    CONFLUENT_METRICS_TOPIC_REPLICATION="confluent.metrics.topic.replication",
    CONFLUENT_METRICS_TOPIC_RETENTION_MS="confluent.metrics.topic.retention.ms",
    CONFLUENT_METRICS_TOPIC_PARTITIONS="confluent.metrics.topic.partitions",
    CONFLUENT_METRICS_TOPIC_SKIP_BACKLOG_MINUTES="confluent.metrics.topic.skip.backlog.minutes"
)

# incomplete set
c3_optional_props = dict(
    CONTROL_CENTER_ID="confluent.controlcenter.id",
    CONTROL_CENTER_NAME="confluent.controlcenter.name",
)

# incomplete set
metadata_props = dict(
    CONFLUENT_METADATA_BOOTSTRAP_SERVER_URLS="confluent.metadata.bootstrap.server.urls",
    CONFLUENT_METADATA_CLUSTER_REGISTRY_ENABLE="confluent.metadata.cluster.registry.enable",
)

# complete set
support_props = dict(
    CONFLUENT_SUPPORT_METRICS_ENABLE="confluent.support.metrics.enable",
    CONFLUENT_SUPPORT_METRICS_SEGMENT_ID="confluent.support.metrics.segment.id"
)

# complete set
other_props = dict(
    CONTROL_CENTER_LICENSE="confluent.license",
    PUBLIC_KEY_PATH="public.key.path"
)

# env_to_c3_prop_lookup: a map from environment property to correctly translated c3 property
env_to_c3_prop_lookup = {
    **required_props,
    **monitoring_props,
    **remaining_control_center_metrics_props,
    **confluent_metrics_props,
    **other_props,
    **c3_optional_props,
    **metadata_props,
    **support_props
}


class PropsTranslationTest(unittest.TestCase):
    # test_env: a map from environment property to its expected value
    test_env = None

    # filled_template: a map from translated c3 property to its actual value
    filled_template = None

    @classmethod
    def set_up_test_env(cls, test_env_props):
        cls.test_env = dict()
        for test_env_prop in test_env_props:
            # each property has a unique value. for example, { 'CONTROL_CENTER_ID' : '9999' }
            cls.test_env[test_env_prop] = str(random.randint(0, 10000))

    @classmethod
    def fill_template(cls):
        template_file = "/etc/confluent/docker/control-center.properties.template"

        j2_env = Environment(
            loader=FileSystemLoader(searchpath="../include"),
            trim_blocks=True)
        j2_env.globals['env_to_props'] = dub.env_to_props
        template = j2_env.get_template(template_file)

        # fill the template with environment variable, split each line, filter out
        # the empty lines, then convert to a list
        actual = list(filter(None, template.render(env=os.environ).splitlines()))

        # split each property. for example line confluent.controlcenter.id=1 becomes
        # { 'confluent.controlcenter.id' : '1' }
        cls.filled_template = dict(line.split("=") for line in actual)

    @classmethod
    def configure_partially(cls, props, sample_size=2):
        configured_props = random.sample(props.keys(), sample_size)
        not_configured_props = list(set(props.keys()) - set(configured_props))
        return configured_props, not_configured_props

    @classmethod
    def check_translations(cls, env_props):
        for env_prop in env_props:
            c3_prop = env_to_c3_prop_lookup[env_prop]
            expected_val = cls.test_env[env_prop]
            cls.check_single_translation(c3_prop, expected_val)

    @classmethod
    def check_single_translation(cls, c3_prop, expected_val):
        try:
            # The translation from docker prop to c3 prop was correct, now assert the
            # value of the prop is correct.
            actual_val = cls.filled_template[c3_prop]
            assert expected_val == actual_val, \
                "for property %s expected val %s, got %s" % (c3_prop, expected_val, actual_val)
        except KeyError:
            # The translation from docker prop to c3 prop was incorrect.
            assert False, "wrong property translation to %s" % c3_prop

    @classmethod
    def check_filled_template_length(cls, expected_len=0):
        actual_len = len(cls.filled_template)
        assert expected_len == actual_len, \
            "filled template expected length %s, got %s" % (expected_len, actual_len)

    def test_missing_required_props(self):
        """
        Testing SET_PROPERTIES's logic of required vs. not required.

        Test that when no environment variable is set, required properties are set with empty
        string.

        :return: pass if when no environment variable is set, required properties are set with ""
        """
        configured_props, not_configured_props = self.configure_partially(required_props)
        self.set_up_test_env(test_env_props=configured_props)

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # only required properties show up
            self.check_filled_template_length(expected_len=len(required_props))

            # some are set with their values
            self.check_translations(env_props=configured_props)

            # some are set with empty string
            for not_configured_prop in not_configured_props:
                c3_prop = env_to_c3_prop_lookup[not_configured_prop]

                assert self.filled_template[c3_prop] == "", \
                    "required property %s should be empty since no environment variable is set"

    def test_missing_optional_properties(self):
        """
        Testing SET_PROPERTIES's logic of required vs. not required.

        Test that when no environment variable is set, optional properties are not set at all.

        Important to note: this test only uses monitoring_props to test that optional properties
        are not set if no environment variable is present. However, the same logic is applicable to
        other_props, "CONFLUENT_METADATA_*", "CONFLUENT_SUPPORT_*", "CONTROL_CENTER_*" properties
        as well.

        :return: pass if when no environment variable is set, optional properties are not set
        """
        configured_props, not_configured_props = self.configure_partially(monitoring_props)
        self.set_up_test_env(test_env_props=list(required_props.keys()) + configured_props)

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(
                expected_len=len(required_props) + len(configured_props))

            self.check_translations(env_props=basic_props.keys())

            self.check_translations(env_props=configured_props)

            for not_configured_prop in not_configured_props:
                c3_prop = env_to_c3_prop_lookup[not_configured_prop]

                assert c3_prop not in self.filled_template, \
                    "optional property %s shouldn't be set" % c3_prop

    def test_rf_properties_use_default(self):
        """
        Testing SET_PROPERTIES's logic of precedence.

        Test that replication factor properties default to CONTROL_CENTER_REPLICATION_FACTOR

        :return: pass if confluent.controlcenter.internal.topics.replication
                         confluent.controlcenter.command.topic.replication
                         confluent.metrics.topic.replication
                         confluent.monitoring.interceptor.topic.replication
                      default to use CONTROL_CENTER_REPLICATION_FACTOR when they're not set.
        """
        self.set_up_test_env(
            test_env_props=list(basic_props.keys()) + [
                'CONTROL_CENTER_REPLICATION_FACTOR'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=len(required_props))

            self.check_translations(env_props=basic_props.keys())

            for rf_prop in rf_props.values():
                self.check_single_translation(
                    c3_prop=rf_prop,
                    expected_val=self.test_env['CONTROL_CENTER_REPLICATION_FACTOR'])

    def test_metrics_rf_property_respects_precedence(self):
        """
        Testing SET_PROPERTIES's logic of precedence.

        Test that confluent.metrics.topic.replication respect the following precedence:
            CONTROL_CENTER_METRICS_TOPIC_REPLICATION >
                CONFLUENT_METRICS_TOPIC_REPLICATION >
                    CONTROL_CENTER_REPLICATION_FACTOR

        :return: pass if confluent.metrics.topic.replication respects the precedence
        """
        # CONTROL_CENTER_METRICS_TOPIC_REPLICATION should take precedence
        self.set_up_test_env(
            test_env_props=list(basic_props.keys()) + [
                'CONTROL_CENTER_METRICS_TOPIC_REPLICATION',
                'CONFLUENT_METRICS_TOPIC_REPLICATION',
                'CONTROL_CENTER_REPLICATION_FACTOR'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=len(required_props))

            self.check_translations(env_props=basic_props.keys())

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.replication',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_REPLICATION'])

        # CONFLUENT_METRICS_TOPIC_REPLICATION should take precedence
        self.set_up_test_env(
            test_env_props=list(basic_props.keys()) + [
                'CONFLUENT_METRICS_TOPIC_REPLICATION',
                'CONTROL_CENTER_REPLICATION_FACTOR'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=len(required_props))

            self.check_translations(env_props=basic_props.keys())

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.replication',
                expected_val=self.test_env['CONFLUENT_METRICS_TOPIC_REPLICATION'])

        # for when only CONTROL_CENTER_REPLICATION_FACTOR is set, see unit test
        # test_rf_properties_use_default

    def test_remaining_metrics_props_respect_precedence(self):
        """
        Testing SET_PROPERTIES's logic of precedence.

        Test that the remaining metrics-related properties also respect the following precedence:
        CONTROL_CENTER_METRICS_* > CONFLUENT_METRICS_*

        :return: pass if remaining metrics-related properties also respect the precedence
        """
        self.set_up_test_env(
            test_env_props=list(required_props.keys()) + [
                # confluent.metrics.topic uses CONTROL_CENTER_METRICS_* since it takes precedence
                'CONTROL_CENTER_METRICS_TOPIC', 'CONFLUENT_METRICS_TOPIC',
                # confluent.metrics.topic.retention.ms uses CONTROL_CENTER_METRICS_*
                'CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS',
                # confluent.metrics.topic.partitions uses CONFLUENT_METRICS_*
                'CONFLUENT_METRICS_TOPIC_PARTITIONS',
                # confluent.metrics.topic.skip.backlog.minutes not set at all
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # 3 more extra properties: metrics.topic, metrics.topic.retention.ms, metrics.partitions
            self.check_filled_template_length(expected_len=len(required_props) + 3)

            self.check_translations(env_props=basic_props.keys())

            self.check_single_translation(
                c3_prop='confluent.metrics.topic',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC']
            )

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.retention.ms',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS']
            )

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.partitions',
                expected_val=self.test_env['CONFLUENT_METRICS_TOPIC_PARTITIONS']
            )

            assert 'confluent.metrics.topic.skip.backlog.minutes' not in self.filled_template

    def test_comprehensive(self):
        """
        Testing SET_PROPERTIES and SET_PROPERTIES_WITH_ENV_TO_PROPS's logic combined.

        Test the properties translation comprehensively.

        :return: pass if all properties' translation and precedence are correct
        """
        # rf props should ignore "CONTROL_CENTER_REPLICATION_FACTOR" because of precedence
        configured_rf_props = list(rf_props.keys()) + ["CONTROL_CENTER_REPLICATION_FACTOR"]

        # metrics props should ignore "CONFLUENT_METRICS_*" because of precedence
        configured_metrics_props = list(remaining_control_center_metrics_props.keys()) + \
            list(confluent_metrics_props.keys())

        # monitoring props should be partially set because they're optional props
        configured_monitoring_props, _ = self.configure_partially(monitoring_props)

        # other props should ignore "CONTROL_CENTER_CONFLUENT_LICENSE" because of precedence and
        # should be partially set because they're optional props
        configured_other_props = list(other_props.keys()) + ["CONTROL_CENTER_CONFLUENT_LICENSE"]

        # c3 optional props should be partially set because they're optional props
        configured_c3_optional_props, _ = self.configure_partially(c3_optional_props, sample_size=1)

        # metadata props should be partially set because they're optional props
        configured_metadata_props, _ = self.configure_partially(metadata_props, sample_size=1)

        # support props should be partially set because they're optional props
        configured_support_props, _ = self.configure_partially(support_props, sample_size=1)

        self.set_up_test_env(test_env_props=list(basic_props.keys()) +
                             configured_rf_props +
                             configured_metrics_props +
                             configured_monitoring_props +
                             configured_other_props +
                             configured_c3_optional_props +
                             configured_metadata_props +
                             configured_support_props)

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            to_check = [basic_props.keys(),
                        rf_props.keys(),
                        remaining_control_center_metrics_props.keys(),
                        configured_monitoring_props,
                        other_props,
                        configured_c3_optional_props,
                        configured_metadata_props,
                        configured_support_props]

            self.check_filled_template_length(expected_len=sum([len(li) for li in to_check]))

            for li in to_check:
                self.check_translations(env_props=li)

