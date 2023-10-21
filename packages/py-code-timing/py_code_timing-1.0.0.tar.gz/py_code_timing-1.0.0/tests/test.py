'''
Test code for py_code_timing package

@author: Purple Elephant
'''

import sys
import time
import random

import py_code_timing as pct


#===============================================================================
# Pizza Making
#===============================================================================

@pct.timing
def make_pizza(pizza_type, toppings):
    """ test example """
    toppings = parse_list(toppings)
    
    make_pizza_base(pizza_type)
    
    say("   with {} toppings:", len(toppings))
    for tp in list(toppings):
        add_topping(tp)
    say("Pizza made!\n")
    nl(2)

@pct.timing 
def make_pizza_base(pizza_type):
    """ test example """
    pizza_type = norm(pizza_type)
    
    if pizza_type.startswith("thin"):
        pizza_type = "thin crust"
        dur = choose_duration(4, 7)
        
    elif pizza_type.startswith("thic"):
        pizza_type = "thick crust"
        dur = choose_duration(6, 10)
    
    else:
        errorf("Bad option for pizza base: {}", pizza_type)
    
    say("Making {} pizza base ...", pizza_type)  
    time_passes(dur)
 
@pct.timing
def add_topping(topping):
    """ test example """
    topping = norm(topping)
    
    if topping.startswith("moz") or topping.startswith("ch"):
        add_mozarella_topping()
        
    elif topping.startswith("tom"):
        add_tomato_topping()

    elif topping.startswith("anc"):
        add_anchovy_topping()
        
    elif topping.startswith("pep"):
        add_pepperoni_topping() 
        
    elif topping.startswith("tun"):
        add_tuna_topping() 
    
    else:
        errorf("Topping unavailable: {}", topping)

@pct.timing
def add_mozarella_topping():
    """ test example """
    say("      Adding mozarella cheese")
    dur = choose_duration(1, 3)
    time_passes(dur)

@pct.timing
def add_tomato_topping():
    """ test example """
    say("      Adding tomato")
    dur = choose_duration(1, 3)
    time_passes(dur)

@pct.timing
def add_anchovy_topping():
    """ test example """
    say("      Adding anchovy")
    dur = choose_duration(1, 3)
    time_passes(dur)

@pct.timing
def add_pepperoni_topping():
    """ test example """
    say("      Adding pepperoni")
    dur = choose_duration(1, 3)
    time_passes(dur)

@pct.timing
def add_tuna_topping():
    """ test example """
    say("      Adding tuna")
    dur = choose_duration(1, 3)
    time_passes(dur)


#-------------------------------------------------------------------------------
# Primary Tests
#-------------------------------------------------------------------------------
def test1(RUNS):
    """ test function """
    
    say("Test 1 -- Standard use of timing objs")
    nl(1)
    
    tobj = pct.CodeTiming()
    
    for i in range(RUNS):
        say("Run {} of {}", i+1, RUNS)
        tobj.start()
        say("Simple timing starts ....")
        
        time_passes(1)
        say("Timing sampled: {}", tobj.sample())
        
        time_passes(1.5)
        say("Timing done: {}", tobj.elapsed())
        nl(2)
    
    say("Stats:   {}", tobj.get_stats())
    say("Display: {}", tobj.display_stats())
    nl(2)

  
def test2(runs):
    """ test function """
    
    say("Test 2 -- Testing with-statement - runs = {}", runs)
    nl(1)
    
    for i in range(runs):
        say("Run {} of {}", i+1, runs)
        
        with pct.CodeTiming("TestCode"):
            
            say("First timing - 1 sec")
            time_passes(1)
            
            say("Second timing - 1.5 sec")
            time_passes(1.5)
            nl(2)
    
    say("Stats:   {}", pct.CodeTiming.get_stats_by_name("TestCode"))
    say("Display: {}", pct.CodeTiming.display_stats_by_name("TestCode"))
        
    nl(2)

def test3(runs):
    """ test function """
    #random.seed(74932423984)
    #random.seed(86750480638)
    random.seed(38384856747)
    
    say("Test 3 -- Making Pizza's")
    nl(1)
    
    base = parse_list("thick thin")
    toppings = parse_list("moz tom anch tun pep")

    pct.CodeTiming.reset_all()
    for i in range(runs):
        # Choose base ...
        my_base = random.choice(base)
        
        # Choose number of toppings
        my_num = random.randint(1, 5)
        
        # Choose toppings from list (without replacement)
        my_toppings = random.sample(toppings, my_num)
        
        say("Making pizza #{}", 1+i)
        make_pizza(my_base, my_toppings)
    
    print(pct.CodeTiming.display_all_stats(shape="ver"))
    nl(2)


#===============================================================================
# Functional Testing
# --- Tests of basic integrity and functionality
#===============================================================================
DURATION = 0.01

#-------------------------------------------------------------------------------
# Random Timing behaviour
#-------------------------------------------------------------------------------

def randomised_test(runs):
    random.seed(3753474569956)
    
    say("randomised test: runs = {}", runs)
    nl(2)

    tobj = pct.CodeTiming()

    for i in range(runs):
        duration = round(random.uniform(0.5, 1.0), 4)
        say("run: {}, duration = {}", i+1, duration)

        tobj.start()
        time.sleep(duration)
        time_elapsed = tobj.elapsed()
    
        say("Actual timing = {} ms", time_elapsed)
        nl(1)
        
    say("Stats:   {}", tobj.get_stats())
    say("Display: {}", tobj.display_stats())
    nl(2)
    

#-------------------------------------------------------------------------------
# Nesting behaviour
#-------------------------------------------------------------------------------
def nesting_test():
    """
    Tests nesting behaviour
    
    --- timing of inner blocks are ignored
    --- Only outermost timing is counted.
    """
    
    say("Nesting behaviour test\n")
    
    tobj = pct.CodeTiming()
    time_passes(DURATION)
    
    say("Nesting level 1")
    say("1st START")
    tobj.start()
    
    time_passes(DURATION)

    say("Nesting level 2")
    say("2nd START")
    tobj.start()
    
    time_passes(DURATION)
  
    say("Ending level 2")
    time_spent = tobj.elapsed()
    say("time_spent = {}", time_spent)
  
    time_passes(DURATION)
    
    say("Ending level 1")
    time_spent = tobj.elapsed()   
    say("time_spent = {}", time_spent)
    
    say("Stats:   {}", tobj.get_stats())
    say("Display: {}", tobj.display_stats())
    nl(2)

    

#-------------------------------------------------------------------------------
# Autostart behaviour
#-------------------------------------------------------------------------------
def autostart_test():
    """
    Tests autostart behaviour
    
    --- timing of inner blocks are ignored
    --- Only outermost timing is counted.
    """

    say("Autostart behaviour test\n")
    
    tobj = pct.CodeTiming(autostart=True)
    
    say("Duration start ...")
    time_passes(DURATION)
    tobj.elapsed()
    
    
    say("Duration start ...")
    time_passes(DURATION)
    tobj.elapsed()
    
    say("Duration start ...")
    time_passes(DURATION)
    tobj.elapsed()
    
    say("Stats:   {}", tobj.get_stats())
    say("Display: {}", tobj.display_stats())
    nl(2)

#-------------------------------------------------------------------------------
# Function tracing and recursion
#-------------------------------------------------------------------------------
DURATION = 0.01


@pct.timing
def rec_fun1(n):
    
    #say("rec_fun1: n = {}", n)

    if n < 1:
        return 1
    
    count = 0
    for _ in range(n):
        time_passes(DURATION)
        count += rec_fun1(n-1)
    
    return count

@pct.timing
def rec_fun2(n):
    #say("rec_fun2: n = {}", n)

    if n < 1:
        return 1
    
    count = 0
    for _ in range(rec_fun2(n-1)):
        time_passes(DURATION)
        count += n
    
    return count


def recursion_test(arg):
    say("Recursion function test - arg = {}", arg)
    
    pct.CodeTiming.reset_all()
    
    tobj = pct.CodeTiming("total")
    
    tobj.start()
    result1 = rec_fun1(arg)
    tobj.elapsed()
    
    say("Result: rec_fun1({}) = {}", arg, result1)
    
    tobj.start()
    result2 = rec_fun2(arg)
    tobj.elapsed()
    
    say("Result: rec_fun2({}) = {}", arg, result2)
    
    print(pct.CodeTiming.display_all_stats())
    nl(2)




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Tools
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#@pct.timing
def time_passes(seconds):
    """ utility """
    #say("Time passes ... {} secs\n", seconds)
    time.sleep(seconds)


def choose_duration(low, high):
    """ Samples normal dist. specified by endpoints: low, high """
    mu = (low+high)/2
    sdev = abs(high-low)/2

    return abs(round(random.gauss(mu, sdev), 3))
    

def norm(s):
    """ Produces a normalised string (lower-case) """
    if not isinstance(s, str):
        s = repr(s)
    return s.strip().lower()


def parse_list(arg):
    """
    Takes list of strings or a single string,
    normalises to a list of lower-case strings
    """
    if isinstance(arg, str):
        return norm(arg).split()
    
    result = []
    for ss in arg:
        result += norm(ss).split()
        
    return result

#-------------------------------------------------------------------------------
# Formatted strings -- and output
#-------------------------------------------------------------------------------
def strf(format_string, *items):
    """ utility """
    if not items:
        return format_string
    else:
        return format_string.format(*items)

# def _bytesf(format_string, *items):
#     return strf(format_string, *items).encode()

def say(format_string, *items):
    """
    Outputs formatted string - with implicit newline
    """
    print(strf(format_string, *items))

def nl(count=1):
    """ newline operator """
    if count < 1:
        return
    
    print("\n"*count)


#-------------------------------------------------------------------------------
# Errors
#-------------------------------------------------------------------------------
def error(msg):
    """ utility """
    print("**** " + msg + " ... exiting")
    sys.exit(1)

def errorf(format_string, *items):
    """ utility """
    msg = strf(format_string, *items)
    error(msg)


#===============================================================================
# Execution hook
#===============================================================================
if __name__ == "__main__":
    # RAND_RUNS = 30
    # randomised_test(RAND_RUNS)
    #
    # nesting_test()
    #
    # autostart_test()
    #
    # ARG = 5
    # recursion_test(ARG)
    
    RUNS = 10
    #test1(RUNS)
    #test2(RUNS)
    #test3(RUNS)

    
    pass
