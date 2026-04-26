from pathlib import Path
import copy
import re
import yaml

# Regex used to find parameter placeholders like {p1}, {k2} in equations
_PARAMETER_PATTERN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


# Function that loads YAML configuration file with model definition
def load_config(path: str | Path) -> dict:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku config: {path}")

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Ensure YAML root is a dictionary
    if not isinstance(config, dict):
        raise ValueError("Plik YAML musi zawierać słownik na najwyższym poziomie.")

    validate_config(config)
    return config


# Function that performs basic validation of YAML structure
def validate_config(config: dict):
    required_sections = ["simulation", "variables", "equations"]

    # Check required sections
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Brakuje sekcji '{section}' w pliku YAML.")

    simulation = config["simulation"]

    # Check simulation parameters
    if "step" not in simulation:
        raise ValueError("Brakuje 'simulation.step'.")
    if "timespan" not in simulation:
        raise ValueError("Brakuje 'simulation.timespan'.")

    variables = config["variables"]
    equations = config["equations"]

    # Ensure variables are defined correctly
    if not isinstance(variables, dict) or not variables:
        raise ValueError("Sekcja 'variables' musi być niepustym słownikiem.")

    for symbol, data in variables.items():
        if "initial" not in data:
            raise ValueError(f"Zmienna '{symbol}' nie ma pola 'initial'.")
        if symbol not in equations:
            raise ValueError(f"Brakuje równania dla zmiennej '{symbol}'.")


# Function that returns available scenario names
def scenario_names(config: dict) -> list[str]:
    return list(config.get("scenarios", {}).keys())


# Function that applies selected scenario:
# overrides parameters and initial values
def apply_scenario(config: dict, scenario_name: str | None) -> tuple[dict, str]:
    cfg = copy.deepcopy(config)

    if scenario_name is None:
        return cfg, ""

    scenarios = cfg.get("scenarios", {})

    # Check if scenario exists
    if scenario_name not in scenarios:
        available = ", ".join(scenarios.keys()) or "brak"
        raise ValueError(
            f"Nie znaleziono scenariusza '{scenario_name}'. Dostępne: {available}"
        )

    scenario = scenarios[scenario_name]
    description = scenario.get("description", "")

    # Override model parameters (e.g. d2, p2, p3)
    parameter_overrides = scenario.get("parameters", {})
    cfg.setdefault("parameters", {}).update(parameter_overrides)

    # Override initial values (e.g. PTEN = 0)
    initial_overrides = scenario.get("initial", {})
    for symbol, value in initial_overrides.items():
        if symbol not in cfg["variables"]:
            raise ValueError(f"Scenariusz próbuje zmienić nieznaną zmienną '{symbol}'.")
        cfg["variables"][symbol]["initial"] = value

    return cfg, description


# Function that replaces parameter placeholders {p1}, {k2}, etc.
# with actual numeric values
def replace_parameter_placeholders(expression: str, parameters: dict) -> str:
    def replace(match):
        name = match.group(1)

        if name not in parameters:
            raise ValueError(
                f"Równanie używa parametru '{{{name}}}', ale nie ma go w sekcji parameters."
            )

        return repr(float(parameters[name]))

    return _PARAMETER_PATTERN.sub(replace, expression)


# Function that builds inputs for rk4():
# model - dict symbol : equation string
# start - dict symbol : initial value
# step - integration step
# timespan - simulation duration
# labels - names for plots
# description - scenario description
def build_inputs(config: dict, scenario_name: str | None = None):
    cfg, description = apply_scenario(config, scenario_name)

    variables = cfg["variables"]
    equations = cfg["equations"]
    parameters = cfg.get("parameters", {})

    model = {}
    start = {}
    labels = {}

    # Build model equations and initial values
    for symbol, data in variables.items():
        raw_equation = equations[symbol]

        # Replace parameters in equation
        model[symbol] = replace_parameter_placeholders(raw_equation, parameters)

        # Initial value of variable
        start[symbol] = float(data["initial"])

        # Label for plots
        labels[symbol] = data.get("label", symbol)

    step = float(cfg["simulation"]["step"])
    timespan = float(cfg["simulation"]["timespan"])

    # Validate simulation parameters
    if step <= 0:
        raise ValueError("Krok całkowania 'step' musi być dodatni.")
    if timespan <= 0:
        raise ValueError("Czas symulacji 'timespan' musi być dodatni.")

    return model, start, step, timespan, labels, description