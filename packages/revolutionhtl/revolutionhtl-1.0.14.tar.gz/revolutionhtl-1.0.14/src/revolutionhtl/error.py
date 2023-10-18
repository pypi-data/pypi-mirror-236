class InconsistentTrees(Exception):
    """Raised when input trees are not consistent when they should"""
    pass

class TreeDontExplainGraph(Exception):
    """Raised when a given tree doesn't explain a given graph"""
    pass

class NotProperlyColoredDigraph(Exception):
    """Raised when a suposed cBMG have different color sets in its connected components"""
    pass

class NotSinkFreeDigraph(Exception):
    """Raised when a suposed cBMG is not sink free"""
    pass

class MissedData(Exception):
    """Raised when trying to run a step in revolutionhtl.__main__ without providing the proper data"""
    pass

class ParameterError(Exception):
    """Raised when trying to run revolutionhtl.__main__ with a wrong parameter"""
    pass

# General errors
################
class DirectoryExist(Exception):
    """Raised when trying create a directory that already exists"""
    pass
