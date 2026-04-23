import types, copy
import matplotlib
import matplotlib.pyplot as plt


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

    # Pretty printing.
    def __str__(self):
        return("".join(['<', str(self.count), " particles of ", self.name, '>']))

    # Returns a set of all variables which are required by this Reagent's function.
    # These are variables which need to be supplied in .calculate()'s 'env' argument (as dict keys).
    # Note: Current Reagent's symbol always appears on output if it is assigned to, (it should be)
    #   even if the function does not depend on it - in which case it does not need to be passed to
    #   .calculate() (but can be, without any effect).
    #returns: set of strings - symbols of required variables
    def get_vars(self):
        return set(self.code.co_names)

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


# Sample code demonstrating how the Reagent class is used
'''
reagentA = Reagent("A = B * 3", 150, 'A', "Reagent A")
reagentB = Reagent("B = A + 6", 100, 'B', "Reagent B")

print(f"Reagents:\n{reagentA.symbol}: {reagentA}\n{reagentB.symbol}: {reagentB}")
print(f"\nReagent timetables:\n{reagentA.name}: {reagentA.timetable}\n{reagentB.name}: {reagentB.timetable}")
print(f"\nReagent dependencies:\n{reagentA.name}: {reagentA.get_vars()}\n{reagentB.name}: {reagentB.get_vars()}")

res_a = reagentA.calculate({reagentB.symbol : reagentB.count})
print(f"\nWhere {reagentA.name}'s function is {reagentA.symbol.lower()}: {reagentA.symbol.lower()}({reagentB.symbol}) = {res_a}")

res_b = reagentB.calculate({reagentA.symbol : reagentA.count})
print(f"Where {reagentB.name}'s function is {reagentB.symbol.lower()}: {reagentB.symbol.lower()}({reagentA.symbol}) = {res_b}")

print("\nTime elapsed: 6")
# Normally, of course, these functions' result would not be directly applied to particle count,
# since that way count of Reagent A is only dependent on count of Reagent B and not at all on its
# previous count - that's just an usage example, though
reagentA.change(6, to=res_a)
reagentB.change(6, to=res_b)

print(f"\nReagent timetables:\n{reagentA.name}: {reagentA.timetable}\n{reagentB.name}: {reagentB.timetable}")
'''

# Function that implements the Runge-Kutta algorithm of 4th order
# Arguments:
#   model - list of Reagent objects, specifies all reagents which take part in the reaction.
#       Reagent-s should all use standardized symbols, i.e. if Reagent A's function depends on
#       Reagent B's count, code of Reagent A should use Reagent B's symbol written exactly the same,
#       to represent that value.
#   step - float, a time step of the model (time which passes between each step of the algorithm)
def rk_4(model : list, step : float):
    return


# Function that draws a plot of single reagent's change in time
# Arguments:
#   reagent - Reagent object, specifies the reagent, change of which is to be plotted. Note that data
#       for change in time is taken from object's timetable member, so don't forget to populate that!
#
#   file - Name of image file to which to draw the plot.
#   labels - A dictionary of label texts. Use '$name$' to insert reagent name.
#       Recognized label keys: title, xaxis, yaxis
def draw_reagent_plot(reagent, file=None, labels={"title" : "Number of particles of $name$ in time",
                                        "xaxis" : "Time", "yaxis" : "$name$ particles"}):
    time = [record[0] for record in reagent.timetable]
    count = [record[1] for record in reagent.timetable]

    plt.figure(figsize=(1360/60, 768/60), dpi=60) # ~HD resolution

    p = plt.plot(time, count)

    labels_repl = {k : v.replace("$name$", reagent.name) for k,v in labels.items()}

    plt.suptitle(labels_repl.get("title", ""), fontsize=24)
    plt.xlabel(labels_repl.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels_repl.get("yaxis", ""), fontsize=18)

    if file:
        plt.savefig(file)


# Plotting test
'''
import random # Just for test purposes
reagentA = Reagent("A = B * 3", 150, 'A', "Cysteina")

for i in range(100):
    reagentA.change(i, by = random.randint(-5, 5))

draw_reagent_plot(reagentA, file="Testplot.png",
                    labels={"title" : "Liczba cząsteczek związku $name$ zależnie od czasu",
                            "xaxis" : "Czas", "yaxis" : "Cząsteczki związku $name$"})
'''
