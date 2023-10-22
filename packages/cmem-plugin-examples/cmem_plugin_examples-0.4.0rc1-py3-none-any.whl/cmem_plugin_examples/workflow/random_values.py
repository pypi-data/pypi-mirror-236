"""Random values workflow plugin module"""
import uuid
from collections import OrderedDict
from secrets import token_hex, token_urlsafe

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import (Plugin,
                                                          PluginParameter, Icon)
from cmem_plugin_base.dataintegration.entity import (Entities, Entity,
                                                     EntityPath, EntitySchema)
from cmem_plugin_base.dataintegration.parameter.choice import \
    ChoiceParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.ports import FixedNumberOfInputs, FixedSchemaPort

RANDOM_FUNCTIONS = OrderedDict(
    [
        ("token_urlsafe", "Return a random URL-safe text string."),
        ("token_hex", "Return a random text string, in hexadecimal."),
    ]
)


@Plugin(
    label="Random Values",
    icon=Icon(file_name="custom.svg", package=__package__),
    plugin_id="Example-RandomValues",
    description="Generates random values of X rows a Y values.",
    documentation="""
This example workflow operator python plugin from the cmem-plugin-examples package
generates random values.

The values are generated in X rows a Y values. Both parameter can be specified:

- 'number_of_entities': How many rows do you need.
- 'number_of_values': How many values per row do you need.

In addition to that, the random function parameter allows you to choose the used
randomness function and string_length parameter defines how long the output string
is.
""",
    parameters=[
        PluginParameter(
            name="random_function",
            default_value="token_urlsafe",
            label="Function",
            param_type=ChoiceParameterType(RANDOM_FUNCTIONS),
        ),
        PluginParameter(
            name="string_length",
            label="String Length",
            description="How long (in characters) should each value be.",
        ),
        PluginParameter(
            name="number_of_entities",
            label="Entities (Rows)",
            description="How many rows will be created per run.",
        ),
        PluginParameter(
            name="number_of_values",
            label="Values (Columns)",
            description="How many values are created per entity / row.",
        ),
    ],
)
class RandomValues(WorkflowPlugin):
    """Example Workflow Plugin: Random Values"""

    def __init__(
        self,
        random_function: str,
        string_length: int = 16,
        number_of_entities: int = 10,
        number_of_values: int = 5,
    ) -> None:
        if random_function not in RANDOM_FUNCTIONS.keys():
            raise ValueError("Unknown random function value.")
        self.random_function = random_function

        if string_length < 1:
            raise ValueError("String Length needs to be a positive integer.")
        self.string_length = string_length

        if number_of_entities < 1:
            raise ValueError("Entities (Rows) needs to be a positive integer.")
        self.number_of_entities = number_of_entities

        if number_of_values < 1:
            raise ValueError("Values (Columns) needs to be a positive integer.")
        self.number_of_values = number_of_values

        # Output schema
        self.schema = self.generate_output_schema()

        # Input and output ports
        self.input_ports = FixedNumberOfInputs([])
        self.output_port = FixedSchemaPort(self.schema)

    def execute(
        self, inputs=(), context: ExecutionContext = ExecutionContext()
    ) -> Entities:
        self.log.info("Start creating random values.")

        # create the entities
        entities = self.generate_entities()
        number_of_values = self.number_of_entities * self.number_of_values
        self.log.info(f"Happy to serve {number_of_values} random values.")

        return Entities(entities=entities, schema=self.schema)

    def create_value(self) -> str:
        "Generate a single random value."
        if self.random_function == "token_urlsafe":
            return token_urlsafe(self.string_length)
        if self.random_function == "token_hex":
            return token_hex(self.string_length)
        raise ValueError("Unknown random function value.")

    def generate_output_schema(self) -> EntitySchema:
        """Generate the output schema."""
        paths = []
        for path_no in range(self.number_of_values):
            path_uri = f"https://example.org/vocab/RandomValuePath{path_no}"
            paths.append(EntityPath(path=path_uri))
        return EntitySchema(
            type_uri="https://example.org/vocab/RandomValueRow",
            paths=paths,
        )

    def generate_entities(self):
        """Generate entities"""
        for _ in range(self.number_of_entities):
            entity_uri = f"urn:uuid:{str(uuid.uuid4())}"
            values = []
            for _ in range(self.number_of_values):
                values.append([self.create_value()])
            yield Entity(uri=entity_uri, values=values)
