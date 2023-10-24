from finbourne_lab.lusid.client import LusidClient
from finbourne_lab.common.ensure import BaseData
from lusid.exceptions import ApiException
import lusid.models as models
from urllib3.response import HTTPResponse
from lumipy.common import indent_str
from typing import Union
from lumipy import get_client
import os


class BaseLusidData(BaseData):
    """Base class for lusid data ensure steps.

    You are required to implement the ensure and check_data methods.
    """

    def __init__(self, quiet: bool):
        """The constructor of the base lusid data class.

        Args:
            quiet (bool): whether to switch off log messages.
        """
        lm_client = get_client()
        client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])
        self.client = client
        super().__init__(quiet)

    def check_data(self, **kwargs):
        pass

    def write_data(self, **kwargs) -> Union[HTTPResponse, ApiException, bool]:
        pass

    def ensure(self, **kwargs):
        self.log(f'Checking data {kwargs}')
        if self.check_data(**kwargs):
            self.log('Data are present. Ready to go!')
            return True

        self.log('Data not ready. Writing...')
        response = self.write_data(**kwargs)
        if isinstance(response, HTTPResponse):
            response_data = response.json()
            if response_data['failed']:
                failed_type = response_data['failed'][0]['type']
                failed_detail = response_data['failed'][0]['detail']
                failed_error_details = response_data['failed'][0]['errorDetails']
                err_msgs = f"{failed_type}\n{failed_detail}\n{failed_error_details}"
                raise ValueError(f'Write failed!\n{indent_str(err_msgs)}')
        elif isinstance(response, ApiException):
            raise ValueError(f'Write failed!\n{indent_str(str(response))}')
        else:
            response_data = response

        self.log('Data written. Ready to go!')
        return response_data


class PortfolioData(BaseLusidData):

    def check_data(self, **kwargs):
        pass

    def write_data(self, **kwargs):
        pass

    def ensure(self, **kwargs):
        pass


class InstrumentData(BaseLusidData):

    def check_data(self, n_insts, id_prefix, scope="default", properties=None):

        property_keys = []
        if properties is not None:
            property_keys = [prop.key for prop in properties]
        identifiers = [f"{id_prefix}_{i}" for i in range(n_insts)]
        instrument_api = self.client.instruments_api
        response = instrument_api.get_instruments(
            "ClientInternal",
            request_body=identifiers,
            scope=scope,
            property_keys=property_keys,
            _preload_content=False
        )
        response_data = response.json()
        # (not response_data['failed']) will be True if data present and there was no failure
        return not response_data['failed']

    def write_data(self, n_insts, id_prefix, scope="default", properties=None):

        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                properties=properties
            )
            for i in range(n_insts)
        }

        return self.client.instruments_api.upsert_instruments(
            request_body=instruments,
            scope=scope,
            _preload_content=False)

    def ensure(self, n_insts, id_prefix, scope="default", properties=None):
        return super().ensure(
            n_insts=n_insts,
            id_prefix=id_prefix,
            scope=scope,
            properties=properties
        )


class HoldingsData(BaseLusidData):

    def check_data(self, **kwargs):
        pass

    def write_data(self, **kwargs):
        pass

    def ensure(self, **kwargs):
        pass


class TxnsData(BaseData):

    def check_data(self, **kwargs):
        pass

    def write_data(self, **kwargs):
        pass

    def ensure(self, **kwargs):
        pass


class PropertiesData(BaseLusidData):

    def check_data(self, n_props, scope, domain):

        for i in range(n_props):
            try:
                self.client.property_defs_api.get_property_definition(
                    domain=domain,
                    scope=scope,
                    code=f"test_prop{i}"
                )
            except ApiException as e:
                return False
        return True

    def write_data(self, n_props, scope, domain):
        """ Build a number of property objects for a certain scope and domain.

                Args:
                    n_props: number of properties to build
                    scope: scope where the properties wil be created
                    domain: domain of the entity the properties belong to

                Returns:
                """

        responses = []

        for i in range(n_props):
            try:
                property_definition = models.CreatePropertyDefinitionRequest(
                    domain=domain,
                    scope=scope,
                    life_time="Perpetual",
                    code=f"test_prop{i}",
                    value_required=False,
                    data_type_id=models.ResourceId("system", "number"),
                    display_name="test_property"
                )
                # create the property
                responses.append(self.client.property_defs_api.create_property_definition(
                    create_property_definition_request=property_definition))
            except ApiException as e:
                return e

        return responses[0]

    def ensure(self, n_props, scope, domain):
        return super().ensure(n_props=n_props, scope=scope, domain=domain)

    @staticmethod
    def build_properties(n_props, scope, domain):
        from lusid import PropertyValue

        properties = [
            models.ModelProperty(
                key=f'{domain}/{scope}/test_prop{i}',
                value=PropertyValue(metric_value=models.MetricValue(value=i * 100))
            )
            for i in range(n_props)
        ]
        return properties
