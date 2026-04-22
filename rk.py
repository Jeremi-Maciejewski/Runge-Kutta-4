import types, copy

# Class for objects representing reagents in a chemical reaction
class Reagent:
    code : types.CodeType # Code of a function describing the reagent's dynamics
    count : int # Current number of reagent's particles
    symbol : str # Symbol of the reagent - this is also the variable name to which the code assigns
    name : str # Pretty name of the reagent, for visualization
    # A list of 2-element tuples such that the 1st element specifies a timestamp (float) and 2nd
    # a number of particles at that moment in time (int)
    timetable : list

    # Object constructor.
    # Arguments:
    #   code - text specifying the code. This is compile()'d to produce the member 'code'.
    #       Should assign its result to a local variable with name identical to 'symbol'.
    #   initial - integer, an initial number of reagent's particles. Assigned to member 'count'.
    #   symbol - string, symbol (variable name) of th reagent, should be assigned to in code.
    #       Becomes the member 'symbol'.
    #   name - string, optional, defaults to symbol, a pretty name of the reagent, for visualization.
    def __init__(self, code, initial, symbol, name=None):
        assert type(code) is str
        assert type(initial) is int
        assert type(symbol) is str
        assert type(name) is str or name is None

        self.code = compile(code, '<string>', "exec")
        self.count = initial
        self.symbol = symbol
        if name is not None:
            self.name = name
        else:
            self.name = symbol

        self.timetable = [(0.0, initial)]


    # Register a new state of the reagent.
    # Note, one and only one of 'by' and 'to' needs to be specified.
    # Arguments:
    #   time - float, a time at which this state occured.
    #   by - integer, optional, how the number of particles changed, e.g. -2 -> 2 particles were removed.
    #   to - integer, optional, to what destination number did the count of particles change.
    def change(self, time, by=None, to=None):
        if by is None and to is None:
            raise ValueError("Neither 'by' nor 'to' were specified!")
        elif by is not None and to is not None:
            raise ValueError("Both 'by' and 'to' were specified, don't know which to use!")
        elif by is not None:
            assert type(by) is int
            newc = self.count + int(by)
        else:
            assert type(to) is int
            newc = int(to)

        assert type(time) is float or type(time) is int
        self.timetable.append((float(time), newc))
        self.count = newc


    # Calculate the value of reagent's function for a given set of parameters.
    # Arguments:
    #   env - dict, specifies key-value pairs such as var : value
    #       where var is a variable present in object's code and value is its value to use in
    #       calculations.
    #
    # returns: (type unknown) Value which object's code assigns to its symbol (value of reagent's function)
    def calculate(self, env):
        env_new = copy.deepcopy(env)

        exec(self.code, env_new)

        if not env_new.get(self.symbol):
            raise AttributeError(f"The object's code does not create local variable '{self.symbol}' (as specified by member 'symbol'). This means that the object is internally corrupted - either discard it or recreate with valid parameters.")

        return(env_new[self.symbol])


# Sample code which demonstrates how code objects could be created and used
'''
text = "b=a*2"
code = compile(text, '<string>', "exec")

env = {'a':12}
exec(code, env)
print(env['b'])
'''


# Function that implements the Runge-Kutta algorithm of 4th order
def rk_4(model : list, step : float):
    return


# Function that draws a plot of single reagent's change in time
def draw_reagent_plot():
    return
