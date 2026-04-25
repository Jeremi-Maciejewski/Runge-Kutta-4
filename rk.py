import types, copy
import math
import matplotlib
import matplotlib.pyplot as plt

# Function that implements the Runge-Kutta algorithm of 4th order
# Arguments:
#   model - dict of symbol : code where symbol is a string representing a reagent and
#       code is a string with function code of said reagent.
#       Code strings should all use standardized symbols, i.e. if reagent A's function depends on
#       reagent B's count, code of reagent A should use reagent B's symbol written exactly the same,
#       to represent that value.
#   start - dict of symbol : num, where symbol is a string representing a reagent, same as in 'model',
#       and num is an initial number particles of that reagent.
#   step - float, a time step of the model (time which passes between each step of the algorithm)
#   timespan - a destiantion time of the simulation, i.e. a time, upon reaching which, the
#       algorithm stops execution. Time always starts as 0 and increases by 'step' on every step
#       of the algorithm.
def rk4(model : dict, start : dict, step : float, timespan : float):
    currstate = copy.deepcopy(start) # Current state of reactor, i.e. numbers of particles
    univ_globals = {"__builtins__":{}, "pow" : math.pow, "root" : lambda x, y : pow(x, 1/y),
                    "sqrt" : math.sqrt}

    time = 0 # Current time
    timetable = [0] # List of recorded points in time
    states = {symbol : [count] for symbol, count in start.items()} # dict of symbol : list of states

    while time+step <= timespan: # Repeat until we reach destination time
        k1s = [] # List of k1 values of all reagents
        for symbol in model: # Calculate k1 values by evaluating reagent functions
            k1 = eval(model[symbol], globals=univ_globals, locals=currstate)
            k1s.append(k1)

        del k1
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step/2 * k1(Xn)
        env_k1 = {list(model.keys())[i] : list(currstate.values())[i] + step/2 * k1s[i] for i in range(len(model))}

        k2s = [] # List of k2 values of all reagents
        for symbol in model:
            k2 = eval(model[symbol], globals=univ_globals, locals=env_k1)
            k2s.append(k2)

        del env_k1, k2
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step/2 * k2(Xn)
        env_k2 = {list(model.keys())[i] : list(currstate.values())[i] + step/2 * k2s[i] for i in range(len(model))}

        k3s = [] # List of k3 values of all reagents
        for symbol in model:
            k3 = eval(model[symbol], globals=univ_globals, locals=env_k2)
            k3s.append(k3)

        del env_k2, k3
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step * k3(Xn)
        env_k3 = {list(model.keys())[i] : list(currstate.values())[i] + step * k3s[i] for i in range(len(model))}

        k4s = [] # List of k4 values of all reagents
        for symbol in model:
            k4 = eval(model[symbol], globals=univ_globals, locals=env_k3)
            k4s.append(k4)


        # Calculate final reagent counts for this step and save them
        for i, symbol in enumerate(model):
            newstate = currstate[symbol] + step * (1/6) * (k1s[i] + 2*k2s[i] + 2*k3s[i] + k4s[i])

            states[symbol].append(newstate)
            currstate[symbol] = newstate

        # Update time
        time += step
        timetable.append(time)

        del k1s, k2s, k3s, k4s, k4, env_k3


    return timetable, states


# Function that draws a plot of single reagent's change in time
# Arguments:
#   reagentstates - List of particle counts of a reagent in various points in time.
#   timetable - List of points in time which correspond to values in 'reagentstates'.
#   name - Name of the reagent being considered.
#   file - (optional string) Name of image file to which to draw the plot.
#   labels - (optional dict) A dictionary of label texts. Use '$name$' to insert reagent name.
#       Recognized label keys: title, xaxis, yaxis
def draw_reagent_plot(reagentstates, timetable, name, file=None,
                        labels={"title" : "Number of particles of $name$ in time",
                                        "xaxis" : "Time", "yaxis" : "$name$ particles"}):

    plt.figure(figsize=(1360/60, 768/60), dpi=60) # ~HD resolution

    p = plt.plot(timetable, reagentstates)

    labels_repl = {k : v.replace("$name$", name) for k,v in labels.items()}

    plt.suptitle(labels_repl.get("title", ""), fontsize=24)
    plt.xlabel(labels_repl.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels_repl.get("yaxis", ""), fontsize=18)

    if file:
        plt.savefig(file)


# rk4 test
'''
mdl = {'A' : "10 - 2*pow(10, -4) * A * B", 'B' : "5*pow(10, -2) * A - 2*pow(10, -2) * B"}
start = {'A' : 100, 'B' : 200}
timetable, states = rk4(mdl, start, 6, 240)

print(timetable)
print(states)
labs = {"title" : "Liczba cząsteczek związku $name$ zależnie od czasu",
        "xaxis" : "Czas", "yaxis" : "Cząsteczki związku $name$"}

#draw_reagent_plot(states['A'], timetable, 'A', file="data/Test_plot_A.png", labels=labs)
#draw_reagent_plot(states['B'], timetable, 'B', file="data/Test_plot_B.png", labels=labs)
'''


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
