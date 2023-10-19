from abml.abml_helpers import convert_abaqus_constants
from abaqus import mdb
from abml.abml_logger import Logger

logger = Logger().get_logger(__name__)

class Abml_Contact_Controls():
    def __init__(self, model, name, **kwargs):
        self.model = model
        self.name = name
        self.kwargs = convert_abaqus_constants(**kwargs)

        self.create()

    def create(self):
        logger.debug("contact_control: {}".format(self.name))
        mdb.models[self.model].StdContactControl(name=self.name, **self.kwargs)
