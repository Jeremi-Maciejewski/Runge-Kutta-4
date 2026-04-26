import copy
import math
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
            k1 = eval(model[symbol], univ_globals, currstate)
            k1s.append(k1)

        del k1
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step/2 * k1(Xn)
        env_k1 = {list(model.keys())[i] : list(currstate.values())[i] + step/2 * k1s[i] for i in range(len(model))}

        k2s = [] # List of k2 values of all reagents
        for symbol in model:
            k2 = eval(model[symbol], univ_globals, env_k1)
            k2s.append(k2)

        del env_k1, k2
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step/2 * k2(Xn)
        env_k2 = {list(model.keys())[i] : list(currstate.values())[i] + step/2 * k2s[i] for i in range(len(model))}

        k3s = [] # List of k3 values of all reagents
        for symbol in model:
            k3 = eval(model[symbol], univ_globals, env_k2)
            k3s.append(k3)

        del env_k2, k3
        # For next step, the values of supplied reagent quantities need to be modified
        # X = Xn + step * k3(Xn)
        env_k3 = {list(model.keys())[i] : list(currstate.values())[i] + step * k3s[i] for i in range(len(model))}

        k4s = [] # List of k4 values of all reagents
        for symbol in model:
            k4 = eval(model[symbol], univ_globals, env_k3)
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

    plt.figure(figsize=(800/60, 480/60), dpi=60) # ~WVGA resolution

    # Draw line plot
    plt.plot(timetable, reagentstates)

    # Replace special elements in labels
    labels_repl = {k : v.replace("$name$", name) for k,v in labels.items()}

    # Draw other elements
    plt.suptitle(labels_repl.get("title", ""), fontsize=24)
    plt.xlabel(labels_repl.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels_repl.get("yaxis", ""), fontsize=18)

    # Optionally save to file
    if file:
        plt.savefig(file)


# Function that draws a plot of multiple reagents' change in time
# Arguments:
#   reagentstates - Dict of symbol : states where symbol is string, reagent's symbol and
#       states is a list of particle counts of that reagent in various points in time.
#
#   timetable - List of points in time which correspond to particle counts in values of 'reagentstates'.
#   name - Dict of symbol : name where symbol is string, reagent's symbol and name is a full
#       name of the reagent being considered.
#
#   file - (optional string) Name of image file to which to draw the plot.
#   labels - (optional dict) A dictionary of label texts. Recognized label keys: title, xaxis, yaxis
def draw_bundled_reagent_plot(reagentstates, timetable, names, file=None,
                                labels={"title" : "Number of particles of $name$ in time",
                                        "xaxis" : "Time", "yaxis" : "$name$ particles"}):

    plt.figure(figsize=(800/60, 480/60), dpi=60) # ~WVGA resolution

    # Color and line style options recognized by pyplot
    color_symbols = list("bgrcmyk")
    style_symbols = ['-', '--', '-.', ':']

    # Draw lines
    for idx, reagent in enumerate(reagentstates):
        # Choose line style and color in such way that ensures that every reagent gets a
        # unique combination
        try:
            col = color_symbols[idx % len(color_symbols)]
            style = style_symbols[idx // len(color_symbols)]

        except IndexError: # Too many reagents, too few line styles available
            raise ValueError("Cannot draw bundled plot - too many reagents!")

        plt.plot(timetable, reagentstates[reagent], style+col, label=names[idx])

    # Draw other elements
    plt.legend(loc=2, bbox_to_anchor=(1,1))
    plt.suptitle(labels.get("title", ""), fontsize=24)
    plt.xlabel(labels.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels.get("yaxis", ""), fontsize=18)

    plt.tight_layout() # Ensures that elements do not stick outside the image

    # Optionally save to file
    if file:
        plt.savefig(file)
