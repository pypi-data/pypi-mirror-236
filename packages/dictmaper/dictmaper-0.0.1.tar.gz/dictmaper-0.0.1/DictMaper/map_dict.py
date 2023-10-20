import ast
from DictMaper.utils import recursive_get


class MapDict:

    def __init__(self,
                 output: dict,
                 context: dict,
                 vars: dict,
                 default="-"
                 ) -> None:

        self.output = output
        self.context = context
        self.vars = vars
        self.default = default

    def process(self) -> dict:
        self.map_init_vars()
        self.process_data()
        return self.result

    def map_init_vars(self) -> dict:
        for key, value in self.vars.items():
            data = recursive_get(self.context, value, default=self.default)
            if isinstance(data, (int, float)):
                data = '{:,.0f}'.format(data).replace(',', '.')
            self.vars[key] = data
        return self.vars

    def process_data(self):
        data_to_map_str = str(self.output)
        for key, val in self.vars.items():
            data_to_map_str = data_to_map_str.replace(
                "{" + key + "}", str(val))
        self.result = ast.literal_eval(data_to_map_str)
