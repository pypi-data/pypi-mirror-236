from finbourne_lab.lusid.client import LusidClient
from finbourne_lab.common.ensure import BaseData


class BaseLusidData(BaseData):
    """Base class for lusid data ensure steps.

    You are required to implement the ensure and check_data methods.
    """

    def __init__(self, client: LusidClient, quiet: bool):
        """The constructor of the base lusid data class.

        Args:
            client (LusidClient): finbourne_lab lusid client instance to use.
            quiet (bool): whether to switch off log messages.
        """
        self.client = client
        super().__init__(quiet)
