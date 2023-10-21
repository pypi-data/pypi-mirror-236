'''
Created: 1 Mar 2023
Updated: 30 Aug 2023

@author: Purple Elephant
'''

import sys
import time
import math
import functools


#===============================================================================
# Global Constants
# -- Using strings rather than Enums for simpler APIs
#===============================================================================
## TimeType
TOTAL_TIMETYPE =   "total timetype"
PROCESS_TIMETYPE = "process timetype"
THREAD_TIMETYPE =  "thread timetype"

## TimeUnit
SECONDS_TIMEUNIT =   "seconds _timeunit"
MILLISECS_TIMEUNIT = "millisecs _timeunit"

## Display shape options
DISPLAY_HORIZONTALLY = "horizontal"
DISPLAY_VERTICALLY =   "vertical"


#===============================================================================
# Class CodeTiming
#===============================================================================
class CodeTiming(object):
    """
    Class providing utilities for timing Python code.
    """
    
    # Records timing info per given name
    _NAMED_TIMING_DB = dict()
    
    # If not None, this sets the _timeunit globally
    GLOBAL_TIMEUNIT = None
    
    # If not None, this sets the timetype globally
    GLOBAL_TIMETYPE = None
    
    # Timeunit for function timing decorator.
    FUNCTION_TIMEUNIT = None 
    
    # Timetype for function timing decorator.
    FUNCTION_TIMETYPE = None 
    
    # Global enable
    GLOBAL_ENABLE = True

    def __init__(self, name="", timeunit=MILLISECS_TIMEUNIT, timetype=TOTAL_TIMETYPE, autostart=False):
        """
        CodeTiming constructor function
        """
        
        # Local flag
        self._is_enabled = CodeTiming.GLOBAL_ENABLE

        # Local alias for CodeTiming._NAMED_TIMING_DB
        self._timing_map = CodeTiming._NAMED_TIMING_DB

        # Ensure defined timing attributes timetype and timeunit
        if CodeTiming.GLOBAL_TIMETYPE:
            timetype = CodeTiming.GLOBAL_TIMETYPE
        
        elif not timetype:
            timetype = TOTAL_TIMETYPE
        
        if CodeTiming.GLOBAL_TIMEUNIT:
            timeunit = CodeTiming.GLOBAL_TIMEUNIT    
        
        elif not timeunit:
            timeunit = MILLISECS_TIMEUNIT

        # Define timing functions
        self._get_time = _time_measure(timetype)

        # Set the internal timing info object
        self._timing_info = _TimingInfo(timeunit, timetype, autostart, self._get_time())

        # setup timer_name and _timing_info
        self._timer_name = ""
        
        # Coordinate name and _timing_info
        self.set_name(name)


    #---------------------------------------------------------------------------
    # State setter methods
    #---------------------------------------------------------------------------
    @classmethod
    def reset_all(_):
        """
        Reset all named timimg objects
        """
        for tobj in CodeTiming._NAMED_TIMING_DB.values():
            # calculate relevant time fun
            time_fn = _time_measure(tobj.get_timekind())
            
            # perform reset (+ restart timing when autostart)
            tobj.reset(time_fn())

            
    def reset(self):
        """
        Resets this object (+ restart when autostart)
        """
        self._timing_info.reset(self._get_time())

            
    def set_autostart(self):
        """
        Set autostart to True - and initiate timing.
        
        Fails if timing has already started.
        """
        self._timing_info.set_autostart(self._get_time())
        
        return self


    def set_enabled(self, flag):
        """
        When CodeTiming.GLOBAL_ENABLE,
           set timing object enabled to flag.
        Otherwise, set enabled to false.
        """
        self._is_enabled = flag and CodeTiming.GLOBAL_ENABLE
        
        return self

 
    def set_name(self, new_name):
        """
        Gives an unnamed CodeTiming object a given name.
        Also ensures that timing info is consistent with DB.
        """
        if not self._is_enabled: return self
       
        if self._timer_name:
            # self._timer_name already defined
            if self._timer_name == new_name:
                # No change ..
                return self
            
            else:
                _errorf("CodeTiming.set_name: CodeTiming object already named '{}'", self._timer_name)
    
        if new_name:
            if not new_name.isidentifier():
                _errorf("CodeTiming: set_name - can only use identifiers to name timed objects: {}", new_name)
            
            # Set the time_name to new_name
            self._timer_name = new_name
            
            # Defines DB entry if name not in DB 
            if new_name not in self._timing_map:
                self._timing_map[new_name] = self._timing_info
                                            
            # Ensure that local object aligns with DB entry (Note: Thread safety)
            self._timing_info = self._timing_map[new_name]
            
        return self       
 

    #---------------------------------------------------------------------------
    # Timing methods
    #---------------------------------------------------------------------------
    def start(self):
        """
        Sets current start time.
        """
        if not self._is_enabled: return
        
        self._timing_info.set_start_time(self._get_time())
        

    def elapsed(self):
        """
        Initially calculates the elapsed time since the last start, and stops
        timing.
        
        If autostart is enabled, timing is then resumed.
        
        Returns event time.
        """
        if not self._is_enabled: return None
        
        value = self._timing_info.add_event(self._get_time())
        if value is None:
            # If value is None at this point, then no autostart is needed.
            # Hence, return None
            return None
         
        return value


    def sample(self):
        """
        Samples the elapsed time since the start time.  This does NOT update the
        current start time.  This can therefore be called multiple times
        without affecting the start.

        This means that sampling does _not_ contribute to the stats - only
        elapsed time does that.
        """
        if not self._is_enabled: return None
        
        return self._timing_info.sample(self._get_time())


    #---------------------------------------------------------------------------
    # Stats access methods
    #---------------------------------------------------------------------------
    def get_stats(self):
        """
        Returns _TimingInfo as a map with fields:
            mean, std_dev, max, min, events, total
        """
        return self._timing_info.get_stats()


    @classmethod
    def get_stats_by_name(_, name):
        """
        Returns named timing object _TimingInfo as a map with fields:
            mean, std_dev, max, min, events, total
        """
        return CodeTiming._fetch_timing_info(name).get_stats()


    @classmethod
    def get_all_stats(_):
        """
        Gets all (non-trivial) timing stats data into a map.
        This only includes named entries.
        """
        info_map = dict()
        
        for k, tinfo in CodeTiming._NAMED_TIMING_DB.items():
            if tinfo.get_event_count() > 0:
                info_map[k] = tinfo.get_stats()
                
        return info_map


    #---------------------------------------------------------------------------
    # Display
    #---------------------------------------------------------------------------
    def display_stats(self, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0):
        """
        Displays stats info:
            mean, std_dev, max, min, events, total
        
        Options:
        - name:  Name of timing object (if specified).
        
        - hms:   If True, gives timing info in hrs-mins-secs-millisecs
        - shape: Output either horizontally or vertically
        - skip:  Number of blank lines following
        """
        return self._timing_info.display(hms, shape, skip)


    @classmethod
    def display_stats_by_name(cls, name, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0):
        """
        Displays stats info for named timing object:
            mean, std_dev, max, min, events, total
        
        Argument:
        - name:  Name of timing object (if specified).
        
        Keywords:
        - hms:   If True, gives timing info in hrs-mins-secs-millisecs
        - shape: Output either horizontally or vertically
        - skip:  Number of blank lines following
        """
        return CodeTiming._fetch_timing_info(name).display(hms, shape, skip)

      
    @classmethod
    def display_all_stats(_, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0):
        """
        Displays all stats info:
            mean, std_dev, max, min, events, total
        
        Options:
        - hms:   If True, gives timing info in hrs-mins-secs-millisecs
        - shape: Output either horizontally or vertically
        - skip:  Number of blank lines separating entries
        """
        is_horizontal = False
        if _norm(shape).startswith("h"):
            is_horizontal = True
            
        timing_map = dict(CodeTiming._NAMED_TIMING_DB)
        
        result = ""
        
        if is_horizontal:
            # Horizontal format
            max_key_len = max( [ len(k) for k in timing_map.keys() ] )
            
            for k, tinfo in timing_map.items():
                if tinfo.get_event_count() > 0:
                    data_str = tinfo.display(hms, shape, skip)
                    result += _strf("  {} : {}", k.ljust(max_key_len), data_str)
        else:
            # Vertical format
            
            # Ensure skip >= 1
            skip = max(1, skip)
            
            for k, tinfo in timing_map.items():
                if tinfo.get_event_count() > 0:
                    result += _strf("name:    {}\n", k)
                    result += tinfo.display(hms, shape, skip)

        return result


    #---------------------------------------------------------------------------
    # Context Manager (for supporting the with-statement)
    #---------------------------------------------------------------------------
    def __enter__(self):
        self.start()
        return self


    def __exit__(self, _1, _2, _3):
        self.elapsed()

        # Exceptions gets propagated.
        return False


    #---------------------------------------------------------------------------
    # Private methods
    #---------------------------------------------------------------------------
    @classmethod
    def _fetch_timing_info(_, name):
        """
        Fetch's the relevant timing_info object by name.
        
        Fails if there is no CodeTiming object having the given non-trivial name
        """
        if not name:
            _errorf("CodeTiming : Empty name - can't locate anonymous timing objects.")
            
        try:
            return CodeTiming._NAMED_TIMING_DB[name]
        except:
            _errorf("CodeTiming: Unknown name for timer: '{}'", name)


#===============================================================================
# Decorator function
#===============================================================================
def timing(func):
    """
    Decorator function to add timing to a particular function, so that all
    (outermost) calls are timed.
    """
    # Create an initially anonymous timing object
    # --- The timeunit and timetype is set by the 
    tobj = CodeTiming(timeunit=CodeTiming.FUNCTION_TIMEUNIT, timetype=CodeTiming.FUNCTION_TIMETYPE)
    
    @functools.wraps(func)
    def timing_wrapper(*args, **kwargs):
        """
        Decorator wrapper
        """
        tobj.set_name(func.__name__)   # add _correct_ name to tobj
        tobj.start()                   # start timing
        
        try:
            # Run the code being timed
            value = func(*args, **kwargs)
        
            tobj.elapsed()             # stop timing
            return value
        
        except Exception as exn:
            tobj.elapsed()             # stop timing
            raise exn

    return timing_wrapper


#===============================================================================
# Internal class _TimingInfo
#===============================================================================
class _TimingInfo(object):
    """
    Internal utility class for processing timing data.

    --- Timing info provided externally (from calling context).
        --- Ensures time measurement is controlled by calling context.
    
    --- Uses amortised calculation of mean and std_dev
        --- No timing values need be accumulated
    """
    def __init__(self, timeunit, timetype, autostart, time_now):
        # setup stats calculations
        self._start_time = None
        self._level = 0    # nesting level

        self._event_count = 0

        self._sum = 0
        self._sum_squares = 0

        self._max = -1
        self._min = -1
        
        # setup timetype
        self._timetype = timetype
        
        # setup autostart
        self._autostart = autostart
        
        # setup conversion function
        self._conv_fn = None
        
        # cached calculated values
        self._mean_cache = None
        self._std_dev_cache = None
        
        # Final initialisations
        
        # init conversion function
        self._set_conv_fn(timeunit)
        
        # init autostart
        if self._autostart:
            self.set_start_time(time_now)
        
        
    def reset(self, time_now):
        """
        Resets the object, forgetting all stats so far.  Also restarts timing
        when autostart is enabled.
        """
        self._start_time = time_now if self._autostart else None
        self._level = 0    # reentrant level

        self._event_count = 0

        self._sum = 0
        self._sum_squares = 0

        self._max = -1
        self._min = -1
        
        # cached calculated values
        self._mean_cache = None     
        self._std_dev_cache = None

        
    def get_event_count(self):
        return self._event_count

    
    def get_timekind(self):
        return self._timetype


    def set_start_time(self, time_now):
        if self._level == 0:
            self._start_time = time_now
        
        if self._autostart:
            return
        
        self._incr_level()
    
    
    def set_autostart(self, time_now):
        if self._autostart:
            return

        if self._timing_started():
            _errorf("set_autostart: Can't set autolevel mode once timing has started.")

        self._autostart = True      
        self.set_start_time(time_now)


    def add_event(self, time_now):
        """
        Calculate the event interval and update info.
        """        
        # Check if timing not currently running
        if self._start_time is None:
            # Timing not running - nothing to do
            return None
        
        # Measure event duration since start time
        event = (time_now - self._start_time)
        
        # Clear cached values        
        self._mean_cache = None     
        self._std_dev_cache = None
        
        # Process levels
        self._decr_level()
        
        if self._level > 0:
            #  Current _level too high - no result to process
             return None
        
        assert self._level == 0
        
        # Process event
        self._sum += event
        self._sum_squares += (event * event)

        self._event_count += 1

        if event > self._max:
            self._max = event

        if self._min < 0 or event < self._min:
            self._min = event
        
        # Reset timing ...
        # --- restarts timing if in autostart mode
        self._start_time = time_now if self._autostart else None
        
        # Finally, return measured duration 
        return self._conv_fn(event)


    def sample(self, time_now):
        """
        Returns time sample since current start-time
        """
        if self._start_time is None:
            return None
        else:
            return self._conv_fn(time_now - self._start_time)


    def get_stats(self):
        """
        Returns timing stats as a map with defined fields:

            mean, std_dev, max, min, events, total
        """
        
        return {"mean":     self._conv_fn( self._calc_mean() ),
                "std_dev":  self._conv_fn( self._calc_std_dev() ),
                "max":      self._conv_fn( self._max ),
                "min":      self._conv_fn( self._min ),
                "events":   self._event_count,
                "total":    self._conv_fn( self._sum )
               }


    #---------------------------------------------------------------------------
    # Display
    #---------------------------------------------------------------------------
    def display(self, hms=True, shape=DISPLAY_HORIZONTALLY, skip=0):
        """
        Displays stats info:
            mean, std_dev, max, min, events, total
        
        Options:
        - hms:   If True, gives timing info in hrs-mins-secs-millisecs
        - shape: Output either horizontally or vertically
        - skip:  Number of blank lines following
        """
        # Use horizontal or vertical format?
        is_horizontal = False
        if _norm(shape).startswith("h"):
            is_horizontal = True
            
        events_str = str(self._event_count)
        
        if hms:
            # Use hms format
            mean_str =    _show_time_hms(_to_millisecs( self._calc_mean() ))
            std_dev_str = _show_time_hms(_to_millisecs( self._calc_std_dev() ))
            max_str =     _show_time_hms(_to_millisecs( self._max ))
            min_str =     _show_time_hms(_to_millisecs( self._min ))
            total_str =   _show_time_hms(_to_millisecs( self._sum ))
            
        else:
            # Use 'bare' timing format
            unit_mark = " secs" if timeunit.startswith("s") else " msecs"
            
            mean_str =     str(self._conv_fn( self._calc_mean() )) + unit_mark
            std_dev_str =  str(self._conv_fn( self._calc_std_dev() )) + unit_mark
            max_str =      str(self._conv_fn( self._max )) + unit_mark
            min_str =      str(self._conv_fn( self._min )) + unit_mark
            total_str =    str(self._conv_fn( self._sum )) + unit_mark
        
        result = ""
        if is_horizontal:
            result += _strf("mean: {}, ",             mean_str)
            result += _strf("std_dev: (+ or -) {}, ", std_dev_str)
            result += _strf("max: {}, ",              max_str)
            result += _strf("min: {}, ",              min_str)
            result += _strf("events: {}, ",           events_str)
            result += _strf("total: {}\n",            total_str)

        else:
            result += _strf("mean:    {}\n",          mean_str)
            result += _strf("std_dev: (+ or -) {}\n", std_dev_str)
            result += _strf("max:     {}\n",          max_str)
            result += _strf("min:     {}\n",          min_str)
            result += _strf("events:  {}\n",          events_str)
            result += _strf("total:   {}\n",          total_str)
        
        # Add blank lines ...
        result += "\n"*skip
        
        return result


    #---------------------------------------------------------------------------
    # Private methods
    #---------------------------------------------------------------------------
    def _set_conv_fn(self, timeunit):
        """
        Provides timeunit conversion function
        """
        if self._conv_fn:
            return
                    
        timeunit = _norm(timeunit)
        
        if timeunit.startswith("m"):
            # milliseconds
            self._conv_fn = _to_millisecs

        elif timeunit.startswith("s"):
            # seconds
            self._conv_fn = _to_seconds
            
        else:
            _errorf("CodeTiming: Unrecognised time unit: {}", timeunit)


    def _timing_started(self):
        """
        Returns True if timing has started
        """
        return self._event_count > 0 or self._start_time is not None
    
    
        
    def _calc_mean(self):
        """
        Calculation of Average
        """
        if self._mean_cache is not None:
            # return cached _mean_cache
            return self._mean_cache
        
        self._mean_cache = 0.0
        
        if self._event_count >= 1:
            self._mean_cache = self._sum / self._event_count
            return self._mean_cache

        return self._mean_cache


    def _calc_std_dev(self):
        """
        Calculation of Standard Deviation
        """
        if self._std_dev_cache is not None:
            return self._std_dev_cache
        
        self._std_dev_cache = 0.0
        
        if self._event_count > 1:
            mean = self._calc_mean()
            
            sqrs_mean = (self._sum_squares / self._event_count)
            mean_sqrd = (mean * mean)
            
            variance = sqrs_mean - mean_sqrd
            
            self._std_dev_cache = math.sqrt(variance)
            return self._std_dev_cache

        return self._std_dev_cache


    #---------------------------------------------------------------------------
    # Level handling
    # --- Provides support for timing recursive/reentrant code.
    # --- Ensures that only outermost calls of recursive code is timed.
    #---------------------------------------------------------------------------
    def _incr_level(self):
        self._level += 1


    def _decr_level(self):
        if self._level > 0:
            self._level -= 1
        else:
            self._level = 0


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# UTILITIES
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _to_millisecs(tim): return int(round(1000 * tim))
def _to_seconds(tim):   return round(tim, 3)
def _to_none(_):      return None


def _norm(arg):
    """ Produces a normalised string (lower-case) """
    if not isinstance(arg, str):
        arg = repr(arg)
    return arg.strip().lower()


def _time_measure(time_type):
    """
    Provides time measurement function
    """
    time_type = _norm(time_type)
    
    if time_type.startswith("to"):
        # TOTAL_TIMETYPE:
        return time.time

    elif time_type.startswith("p"):
        # PROCESS_TIMETYPE:
        return time.process_time

    elif time_type.startswith("th"):
        # THREAD_TIMETYPE:
        return time.thread_time

    _errorf("CodeTiming: Unrecognised time measurement type: {}", time_type)

#-------------------------------------------------------------------------------
# Show millisecs in hms format
#-------------------------------------------------------------------------------
def _show_time_hms(millis):
    """
    Display timings in hms format
    
    Examples:
        4s 23ms            (4023 msecs)
        2h 14m 31s 257ms   (8071257 msecs)
    """
    if not millis:
        return "0ms"
    
    if millis < 1000:
        return _strf("{}ms", millis)

    secs = millis // 1000
    frac = millis % 1000
    
    if secs < 60:
        return _strf("{}s {}ms", secs, frac)
    
    mins = secs // 60
    secs = secs % 60
    
    if mins < 60:
        return _strf("{}m {}s {}ms", mins, secs, frac)
    
    hrs = mins // 60
    mins = mins % 60
    return _strf("{}h {}m {}s {}ms", hrs, mins, secs, frac)


#-------------------------------------------------------------------------------
# Formatted strings -- and output
#-------------------------------------------------------------------------------
def _strf(format_string, *items):
    if not items:
        return format_string
    else:
        return format_string.format(*items)


# def _bytesf(format_string, *items):
#     return _strf(format_string, *items).encode()


def _printf(format_string, *items):
    """
    Outputs formatted string - with implicit newline
    """
    print(_strf(format_string, *items))


def _nl(count=1):
    """ newline operator """
    if count < 1:
        return
    
    print("\n"*count)


#------------------------------------------------------------------------
# Errors
#------------------------------------------------------------------------
def _error(msg):
    print("**** " + msg + " ... exiting")
    sys.exit(1)


def _errorf(format_string, *items):
    msg = _strf(format_string, *items)
    _error(msg)