# Copyright 2023 Vincent Jacques


# start delvewheel patch
def _delvewheel_patch_1_5_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-lincs-0.10.0')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-lincs-0.10.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not ctypes.windll.kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError()))


_delvewheel_patch_1_5_1()
del _delvewheel_patch_1_5_1
# end delvewheel patch

__version__ = "0.10.0"

# I/O
from liblincs import DataValidationException

from liblincs import Criterion, Category, Problem

from liblincs import SufficientCoalitions, Model
from liblincs import Alternative, Alternatives

# Generation (incl. misclassification)
from liblincs import BalancedAlternativesGenerationException
from liblincs import generate_classification_problem, generate_mrsort_classification_model, generate_classified_alternatives, misclassify_alternatives

# Classification
from liblincs import classify_alternatives

# Learning
from liblincs import LearningFailureException

# Learning - weights-profiles-breed
from liblincs import LearnMrsortByWeightsProfilesBreed
from liblincs import InitializeProfilesForProbabilisticMaximalDiscriminationPowerPerCriterion
from liblincs import OptimizeWeightsUsingGlop, OptimizeWeightsUsingAlglib
from liblincs import ImproveProfilesWithAccuracyHeuristicOnCpu
try:
    from liblincs import ImproveProfilesWithAccuracyHeuristicOnGpu
    has_gpu = True
except ImportError:
    has_gpu = False
from liblincs import ReinitializeLeastAccurate
from liblincs import TerminateAtAccuracy
from liblincs import TerminateAfterSeconds, TerminateAfterSecondsWithoutProgress
from liblincs import TerminateAfterIterations, TerminateAfterIterationsWithoutProgress
from liblincs import TerminateWhenAny

# Learning - SAT by coalitions
from liblincs import LearnUcncsBySatByCoalitionsUsingMinisat

# Learning - SAT by separation
from liblincs import LearnUcncsBySatBySeparationUsingMinisat

# Learning - max-SAT by coalitions
from liblincs import LearnUcncsByMaxSatByCoalitionsUsingEvalmaxsat

# Learning - max-SAT by separation
from liblincs import LearnUcncsByMaxSatBySeparationUsingEvalmaxsat

# @todo(Feature, later) Accept learning and training set as Pandas DataFrame?
