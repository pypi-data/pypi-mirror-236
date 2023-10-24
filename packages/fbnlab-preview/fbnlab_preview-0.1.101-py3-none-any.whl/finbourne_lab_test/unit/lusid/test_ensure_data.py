import unittest
import lumipy as lm
import os
from finbourne_lab.lusid import LusidClient
import shortuuid
import finbourne_lab.lusid.ensure as ensure
import lusid.models as models


class TestPropertiesData(unittest.TestCase):

    properties_data = ensure.PropertiesData(quiet=False)

    def test_ensure_property_definitions(self):

        from lusid.models.property_definition import PropertyDefinition
        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        domain = "Instrument"
        n_props = 50
        response = self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        type_expected = PropertyDefinition
        self.assertTrue(isinstance(response, type_expected))

    def test_build_properties(self):
        scope = f"fbnlab-ut-prop"
        domain = "Instrument"
        n_props = 2
        properties_actual = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)

        from lusid import PropertyValue

        properties_expected = [
            models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop0',
                value=PropertyValue(metric_value=models.MetricValue(value=0))
            ),
            models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop1',
                value=PropertyValue(metric_value=models.MetricValue(value=100))
            )
        ]

        self.assertEqual(properties_expected, properties_actual)


class TestInstrumentData(unittest.TestCase):

    properties_data = ensure.PropertiesData(quiet=False)
    instrument_data = ensure.InstrumentData(quiet=False)
    lm_client = lm.get_client()
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    def test_ensure_instrument_data_ensure_does_upsert_new_instruments_without_properties(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5

        response = self.instrument_data.ensure(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        metadata_actions_type_expected = "CreatedInstruments"
        metadata_actions_type_actual = response['metadata']['actions'][0]["type"]
        self.assertEqual(metadata_actions_type_expected, metadata_actions_type_actual)

    def test_ensure_instrument_data_ensure_does_not_upsert_already_existing_instruments_without_properties(self):

        scope = f"fbnlab-ut-test"
        id_prefix = f"fbnlab-ut-test"
        n_inst = 5

        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')}
            )
            for i in range(n_inst)
        }
        self.client.instruments_api.upsert_instruments(
            request_body=instruments,
            scope=scope,
            _preload_content=False)

        # attempt to recreate the already existing instruments
        response_actual = self.instrument_data.ensure(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        response_expected = True
        self.assertEqual(response_actual, response_expected)

    def test_ensure_instrument_data_ensure_does_upsert_new_instruments_with_properties(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5
        n_props = 1
        domain = "Instrument"

        self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        properties = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)
        response = self.instrument_data.ensure(
            n_insts=n_inst,
            id_prefix=id_prefix,
            scope=scope,
            properties=properties
        )
        metadata_actions_type_expected = "CreatedInstruments"
        metadata_actions_type_actual = response['metadata']['actions'][0]["type"]
        self.assertEqual(metadata_actions_type_expected, metadata_actions_type_actual)

    def test_ensure_instruments_does_not_upsert_already_existing_instruments(self):

        scope = f"fbnlab-ut-test"
        id_prefix = f"fbnlab-ut-test"
        n_inst = 5
        n_props = 1
        domain = "Instrument"

        self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        properties = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)

        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                properties=properties
            )
            for i in range(n_inst)
        }

        self.client.instruments_api.upsert_instruments(
            request_body=instruments,
            scope=scope,
            _preload_content=False)

        # attempt to recreate the already existing instruments
        response_actual = self.instrument_data.ensure(
            n_insts=n_inst,
            id_prefix=id_prefix,
            scope=scope,
            properties=properties
        )
        response_expected = True
        self.assertEqual(response_actual, response_expected)
