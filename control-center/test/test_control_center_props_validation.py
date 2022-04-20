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

# incomplete set
monitoring_props = dict(
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC="confluent.monitoring.interceptor.topic",
    CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS="confluent.monitoring.interceptor.topic.partitions"
)

# incomplete set
control_center_metrics_props = dict(
    CONTROL_CENTER_METRICS_TOPIC="confluent.metrics.topic",
    CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS="confluent.metrics.topic.retention.ms"
)

# incomplete set
confluent_metrics_props = dict(
    CONFLUENT_METRICS_TOPIC="confluent.metrics.topic",
    CONFLUENT_METRICS_TOPIC_REPLICATION="confluent.metrics.topic.replication",
    CONFLUENT_METRICS_TOPIC_RETENTION_MS="confluent.metrics.topic.retention.ms",
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

# incomplete set
support_props = dict(
    CONFLUENT_SUPPORT_METRICS_ENABLE="confluent.support.metrics.enable",
    CONFLUENT_SUPPORT_METRICS_SEGMENT_ID="confluent.support.metrics.segment.id"
)

# complete set
special_props = dict(
    CONTROL_CENTER_LICENSE="confluent.license",
    PUBLIC_KEY_PATH="public.key.path"
)

# env_to_c3_prop_lookup: a map from environment property to correctly translated c3 property
env_to_c3_prop_lookup = {
    **required_props,
    **monitoring_props,
    **control_center_metrics_props,
    **confluent_metrics_props,
    **special_props,
    **c3_optional_props,
    **metadata_props,
    **support_props
}


class PropsTranslationTest(unittest.TestCase):
    # test_env: a map from environment property to its expected value
    test_env = None

    # filled_template: a list of translated c3 property to its actual value
    # e.x. [ [ 'prop1','val1' ], [ 'prop2','val2' ] ]
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
        # ['confluent.controlcenter.id', '1']
        cls.filled_template = list(line.split("=") for line in actual)

    @classmethod
    def configure_partially(cls, props):
        # always randomly choose 1 prop from the list of props
        configured_props = [random.choice(list(props.keys()))]
        not_configured_props = props.keys() - configured_props
        return configured_props, not_configured_props

    @classmethod
    def check_translations(cls, env_props):
        # assume env_prop = 'CONTROL_CENTER_ID'
        for env_prop in env_props:
            # c3_prop is the correct c3 prop translation, which is 'confluent.controlcenter.id'
            c3_prop = env_to_c3_prop_lookup[env_prop]
            # assume expected_val = '9999'
            expected_val = cls.test_env[env_prop]
            # check if in the template file, confluent.controlcenter.id = 9999 as well
            cls.check_single_translation(c3_prop, expected_val)

    @classmethod
    def check_single_translation(cls, c3_prop, expected_val):
        # The translation from docker prop to c3 prop was correct, now assert the
        # value of the prop is correct.
        assert [c3_prop, expected_val] in cls.filled_template, \
            "For property %s expected val %s. This is the actual filled template: %s" \
            % (c3_prop, expected_val, cls.filled_template)

    @classmethod
    def check_filled_template_length(cls, expected_len=0):
        actual_len = len(cls.filled_template)
        assert expected_len == actual_len, \
            "filled template expected length %s, got %s" % (expected_len, actual_len)

    def test_missing_required_properties(self):
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

            # all required props show up, regardless of if they are configured or not
            self.check_filled_template_length(expected_len=len(required_props))

            # required props that are configured show up with actual values
            self.check_translations(env_props=configured_props)

            # required props that are not configured show up with empty string
            for not_configured_prop in not_configured_props:
                c3_prop = env_to_c3_prop_lookup[not_configured_prop]
                assert [c3_prop, ""] in self.filled_template, \
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
        self.set_up_test_env(test_env_props=configured_props)

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # required props show up regardless of if they are configured or not;
            # however, optional props only show up if they are actually configured.
            self.check_filled_template_length(
                expected_len=len(required_props) + len(configured_props))

            # optional props that are configured show up with actual values
            self.check_translations(env_props=configured_props)

            # optional props that are not configured shouldn't show up at all
            actual_props = [li[0] for li in self.filled_template]
            for not_configured_prop in not_configured_props:
                c3_prop = env_to_c3_prop_lookup[not_configured_prop]
                assert c3_prop not in actual_props, "property %s shouldn't be set" % c3_prop

    def test_rf_properties_precedence(self):
        """
        Testing SET_PROPERTIES's logic of precedence.

        1. Test that replication factor properties default to CONTROL_CENTER_REPLICATION_FACTOR

            pass if confluent.controlcenter.internal.topics.replication
                    confluent.controlcenter.command.topic.replication
                    confluent.metrics.topic.replication
                    confluent.monitoring.interceptor.topic.replication
            default to use CONTROL_CENTER_REPLICATION_FACTOR when they're not set.

        2. Test that replication factor properties use their own value

            pass if the four rf props use their own value when corresponding env variable is set,
            even though CONTROL_CENTER_REPLICATION_FACTOR is present as well.

        :return: pass if both tests pass
        """
        # 1. Test that replication factor properties default to CONTROL_CENTER_REPLICATION_FACTOR
        self.set_up_test_env(test_env_props=['CONTROL_CENTER_REPLICATION_FACTOR'])

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # required props show up regardless of if they are configured or not;
            # rf props are part of the required props.
            self.check_filled_template_length(expected_len=len(required_props))

            # check that all rf props default to the value of CONTROL_CENTER_REPLICATION_FACTOR
            for rf_prop in rf_props.keys():
                self.check_single_translation(
                    c3_prop=rf_props[rf_prop],
                    expected_val=self.test_env['CONTROL_CENTER_REPLICATION_FACTOR'])

        # 2. Test that replication factor properties use their own value
        self.set_up_test_env(test_env_props=['CONTROL_CENTER_REPLICATION_FACTOR'] + list(rf_props.keys()))

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # required props show up regardless of if they are configured or not;
            # rf props are part of the required props.
            self.check_filled_template_length(expected_len=len(required_props))

            # check that all rf props use their own value even though CONTROL_CENTER_REPLICATION_FACTOR is configured
            for rf_prop in rf_props.keys():
                self.check_single_translation(
                    c3_prop=rf_props[rf_prop],
                    expected_val=self.test_env[rf_prop])

    def test_metrics_rf_properties_precedence(self):
        """
        Testing SET_PROPERTIES's logic of precedence, specifically metrics rf props.

        Test that confluent.metrics.topic.replication respect the following precedence:
            CONTROL_CENTER_METRICS_TOPIC_REPLICATION >
                CONFLUENT_METRICS_TOPIC_REPLICATION >
                    CONTROL_CENTER_REPLICATION_FACTOR

        :return: pass if confluent.metrics.topic.replication respects the precedence
        """
        # 1. Test CONTROL_CENTER_METRICS_TOPIC_REPLICATION should take precedence
        self.set_up_test_env(
            test_env_props=[
                'CONTROL_CENTER_METRICS_TOPIC_REPLICATION',
                'CONFLUENT_METRICS_TOPIC_REPLICATION',
                'CONTROL_CENTER_REPLICATION_FACTOR'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # required props show up regardless of if they are configured or not;
            # rf props are part of the required props.
            self.check_filled_template_length(expected_len=len(required_props))

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.replication',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_REPLICATION'])

        # 2. Test CONFLUENT_METRICS_TOPIC_REPLICATION should take precedence
        self.set_up_test_env(
            test_env_props=[
                'CONFLUENT_METRICS_TOPIC_REPLICATION',
                'CONTROL_CENTER_REPLICATION_FACTOR'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            # required props show up regardless of if they are configured or not;
            # rf props are part of the required props.
            self.check_filled_template_length(expected_len=len(required_props))

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.replication',
                expected_val=self.test_env['CONFLUENT_METRICS_TOPIC_REPLICATION'])

    def test_bad_prefix_properties(self):
        """
        Testing SET_PROPERTIES_WITH_SKIP_PROP_CHECK's logic of checking bad prefix.

        Test that SET_PROPERTIES_WITH_SKIP_PROP_CHECK avoids adding properties that start with
        CONTROL_CENTER_METRICS_ (aka. confluent.controlcenter.metrics.) and those that start with
        CONTROL_CENTER_MONITORING_INTERCEPTOR_ (aka. confluent.controlcenter.monitoring.interceptor.)
        because these properties are special cases and are falsely translated, even though they
        have the regular prefix CONTROL_CENTER_.

        :return: pass if SET_PROPERTIES_WITH_SKIP_PROP_CHECK avoids adding properties with bad prefix.
        """
        self.set_up_test_env(
            test_env_props=[
                # translated because ok prefix (logic of SET_PROPERTIES_WITH_ENV_TO_PROPS)
                'CONTROL_CENTER_METRICS_TOPIC',
                # translated because ok prefix but overwritten by the prev prop (logic of SET_PROPERTIES_WITH_ENV_TO_PROPS)
                'CONFLUENT_METRICS_TOPIC',
                # falsely translated because it starts with CONTROL_CENTER_ but not CONTROL_CENTER_METRIC_ (logic of SET_PROPERTIES_WITH_SKIP_PROP_CHECK)
                'CONTROL_CENTER_METRIC_TOPIC',
                # won't get translated because bad prefix
                'CONFLUENT_METRIC_TOPIC',
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=len(required_props) + 2)

            self.check_single_translation(
                c3_prop='confluent.metrics.topic',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC'])

            self.check_single_translation(
                c3_prop='confluent.controlcenter.metric.topic',
                expected_val=self.test_env['CONTROL_CENTER_METRIC_TOPIC'])

    def test_metrics_properties_precedence(self):
        """
        Testing SET_PROPERTIES_WITH_ENV_TO_PROPS_WITH_TWO_PREFIXES's logic of precedence.

        Test that SET_PROPERTIES_WITH_ENV_TO_PROPS_WITH_TWO_PREFIXES respects the precedence of
        primary_env_prefix >>> secondary_env_prefix, and that the same property is not set twice.

        :return: pass if
            - confluent.metrics.topic is only set with CONTROL_CENTER_METRICS_TOPIC. We shouldn't
              find it being translated twice.
            - confluent.metrics.topic.partitions is only set with CONTROL_CENTER_METRICS_TOPIC_PARTITIONS
            - confluent.metrics.topic.retention.ms is only set with CONFLUENT_METRICS_TOPIC_RETENTION_MS
        """
        self.set_up_test_env(
            test_env_props=[
                # CONTROL_CENTER_METRICS_ takes precedence
                'CONTROL_CENTER_METRICS_TOPIC',
                'CONFLUENT_METRICS_TOPIC',

                # CONTROL_CENTER_METRICS_ takes precedence
                'CONTROL_CENTER_METRICS_TOPIC_PARTITIONS',

                # CONFLUENT_METRICS_ takes precedence
                'CONFLUENT_METRICS_TOPIC_RETENTION_MS'
            ]
        )

        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=len(required_props) + 3)

            self.check_single_translation(
                c3_prop='confluent.metrics.topic',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC'])

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.partitions',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_PARTITIONS'])

            self.check_single_translation(
                c3_prop='confluent.metrics.topic.retention.ms',
                expected_val=self.test_env['CONFLUENT_METRICS_TOPIC_RETENTION_MS'])

    def test_comprehensive(self):
        """
        Testing SET_PROPERTIES, SET_PROPERTIES_WITH_ENV_TO_PROPS, and
        SET_PROPERTIES_WITH_SKIP_PROP_CHECK 's logic combined.

        Test the properties translation comprehensively.

        :return: pass if all properties' translation and precedence are correct
        """
        # rf props should ignore "CONTROL_CENTER_REPLICATION_FACTOR" because of precedence
        configured_rf_props = list(rf_props.keys()) + ["CONTROL_CENTER_REPLICATION_FACTOR"]

        # metrics props should ignore "CONFLUENT_METRICS_*" because of precedence
        configured_metrics_props = list(control_center_metrics_props.keys()) + \
            list(confluent_metrics_props.keys())

        # monitoring props should be partially set because they're optional props
        configured_monitoring_props, _ = self.configure_partially(monitoring_props)

        # other props should ignore "CONTROL_CENTER_CONFLUENT_LICENSE" because of precedence and
        # should be partially set because they're optional props
        configured_other_props = list(special_props.keys()) + ["CONTROL_CENTER_CONFLUENT_LICENSE"]

        # c3 optional props should be partially set because they're optional props
        configured_c3_optional_props, _ = self.configure_partially(c3_optional_props)

        # metadata props should be partially set because they're optional props
        configured_metadata_props, _ = self.configure_partially(metadata_props)

        # support props should be partially set because they're optional props
        configured_support_props, _ = self.configure_partially(support_props)

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
                        control_center_metrics_props.keys(),
                        configured_monitoring_props,
                        special_props,
                        configured_c3_optional_props,
                        configured_metadata_props,
                        configured_support_props]

            self.check_filled_template_length(expected_len=sum([len(li) for li in to_check]))

            for li in to_check:
                self.check_translations(env_props=li)

    def test_comprehensive_concrete_example(self):
        self.set_up_test_env(
            test_env_props=[
                # copied from cp-all-in-one
                'CONTROL_CENTER_BOOTSTRAP_SERVERS',
                'CONTROL_CENTER_KSQL_KSQLDB1_URL',
                'CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL',
                'CONTROL_CENTER_SCHEMA_REGISTRY_URL',
                'CONTROL_CENTER_SCHEMA_REGISTRY_BASIC_AUTH_CREDENTIALS_SOURCE',
                'CONTROL_CENTER_SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO',
                'CONTROL_CENTER_CONNECT_CONNECT-DEFAULT_CLUSTER',
                'CONTROL_CENTER_STREAMS_SECURITY_PROTOCOL',
                'CONTROL_CENTER_STREAMS_SASL_JAAS_CONFIG',
                'CONTROL_CENTER_STREAMS_SASL_MECHANISM',
                'CONTROL_CENTER_REPLICATION_FACTOR',
                'CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_REPLICATION',
                'CONTROL_CENTER_INTERNAL_TOPICS_REPLICATION',
                'CONTROL_CENTER_COMMAND_TOPIC_REPLICATION',
                'CONTROL_CENTER_METRICS_TOPIC_REPLICATION',
                'CONFLUENT_METRICS_TOPIC_REPLICATION',
                'CONTROL_CENTER_STREAMS_NUM_STREAM_THREADS',
                'CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS',
                'CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS',
                'CONTROL_CENTER_METRICS_TOPIC_MAX_MESSAGE_BYTES',

                # special props
                'CONTROL_CENTER_LICENSE',
                'CONTROL_CENTER_CONFLUENT_LICENSE',
                'PUBLIC_KEY_PATH',

                # props with bad prefix
                'CONTROL_CENTER_METRIC_TOPIC',
                'CONTROL_CENTER_MONITORING_TOPIC',

                # metrics topic precedence
                'CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS',
                'CONFLUENT_METRICS_TOPIC_RETENTION_MS'
            ]
        )
        with patch.dict('os.environ', self.test_env):
            self.fill_template()

            self.check_filled_template_length(expected_len=25)

            # copied from cp-all-in-one
            self.check_single_translation(
                c3_prop='bootstrap.servers',
                expected_val=self.test_env['CONTROL_CENTER_BOOTSTRAP_SERVERS'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.ksql.ksqldb1.url',
                expected_val=self.test_env['CONTROL_CENTER_KSQL_KSQLDB1_URL'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.ksql.ksqldb1.advertised.url',
                expected_val=self.test_env['CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.schema.registry.url',
                expected_val=self.test_env['CONTROL_CENTER_SCHEMA_REGISTRY_URL'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.schema.registry.basic.auth.credentials.source',
                expected_val=self.test_env['CONTROL_CENTER_SCHEMA_REGISTRY_BASIC_AUTH_CREDENTIALS_SOURCE'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.schema.registry.basic.auth.user.info',
                expected_val=self.test_env['CONTROL_CENTER_SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.connect.connect-default.cluster',
                expected_val=self.test_env['CONTROL_CENTER_CONNECT_CONNECT-DEFAULT_CLUSTER'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.streams.security.protocol',
                expected_val=self.test_env['CONTROL_CENTER_STREAMS_SECURITY_PROTOCOL'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.streams.sasl.jaas.config',
                expected_val=self.test_env['CONTROL_CENTER_STREAMS_SASL_JAAS_CONFIG'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.streams.sasl.mechanism',
                expected_val=self.test_env['CONTROL_CENTER_STREAMS_SASL_MECHANISM'])
            self.check_single_translation(
                c3_prop='confluent.monitoring.interceptor.topic.replication',
                expected_val=self.test_env['CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_REPLICATION'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.internal.topics.replication',
                expected_val=self.test_env['CONTROL_CENTER_INTERNAL_TOPICS_REPLICATION'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.command.topic.replication',
                expected_val=self.test_env['CONTROL_CENTER_COMMAND_TOPIC_REPLICATION'])
            self.check_single_translation(
                c3_prop='confluent.metrics.topic.replication',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_REPLICATION'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.streams.num.stream.threads',
                expected_val=self.test_env['CONTROL_CENTER_STREAMS_NUM_STREAM_THREADS'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.internal.topics.partitions',
                expected_val=self.test_env['CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS'])
            self.check_single_translation(
                c3_prop='confluent.monitoring.interceptor.topic.partitions',
                expected_val=self.test_env['CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS'])
            self.check_single_translation(
                c3_prop='confluent.metrics.topic.max.message.bytes',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_MAX_MESSAGE_BYTES'])

            # special props
            self.check_single_translation(
                c3_prop='confluent.license',
                expected_val=self.test_env['CONTROL_CENTER_LICENSE'])
            self.check_single_translation(
                c3_prop='public.key.path',
                expected_val=self.test_env['PUBLIC_KEY_PATH'])

            # props with bad prefix
            self.check_single_translation(
                c3_prop='confluent.controlcenter.metric.topic',
                expected_val=self.test_env['CONTROL_CENTER_METRIC_TOPIC'])
            self.check_single_translation(
                c3_prop='confluent.controlcenter.monitoring.topic',
                expected_val=self.test_env['CONTROL_CENTER_MONITORING_TOPIC'])

            # metrics topic precedence
            self.check_single_translation(
                c3_prop='confluent.metrics.topic.retention.ms',
                expected_val=self.test_env['CONTROL_CENTER_METRICS_TOPIC_RETENTION_MS'])

            # required props that weren't configured get empty string
            self.check_single_translation(
                c3_prop='confluent.controlcenter.data.dir',
                expected_val="")
            self.check_single_translation(
                c3_prop='zookeeper.connect',
                expected_val="")
