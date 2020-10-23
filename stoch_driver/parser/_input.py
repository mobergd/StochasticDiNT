"""
parses the input file for keywords
"""

from .find import first_capture
from .find import all_captures
from .pattern import capturing
from .pattern import zero_or_more
from .pattern import one_or_more
from .pattern import series
from .pattern import escape
from .pattern import NONSPACE
from .pattern import SPACE
from .pattern import WILDCARD
from .pattern import INTEGER
from .pattern import FLOAT
from .pattern import LOGICAL
from .pattern import LINE_FILL
from .pattern import NONNEWLINE
from .pattern import NEWLINE


INPUT_SUPPORTED_SECTIONS = [
    'system_info',
    'directory_info'
]
INPUT_REQUIRED_SECTIONS = [
    'system_info',
    'directory_info'
]

SI_SUPPORTED_KEYWORDS = [
    'JobType',
    'Label',
    'NumAXM',
    'Reactants',
    'XColliders',
    'MColliders',
    'NAtomsA',
    'NAtomsX',
    'NAtomsM',
    'xX',
    'xA',
    'xM',
    'BList',
    'Temperature',
    'Steps',
]
DI_SUPPORTED_KEYWORDS = [
    'NTrajs',
    'Processors',
    'Potentials',
]

SI_REQUIRED_KEYWORDS = [
    'JobType',
    'NumAXM',
    'Reactants',
    'NAtomsA',
    'xA',
    'Temperature',
    'Steps',
]
DI_REQUIRED_KEYWORDS = [
    'NTrajs',
    'Processors',
    'Potentials',
]

def read_jobtype(input_string):
    """ 
    """
    pattern = ('JobType' +
               one_or_more(SPACE) + capturing(one_or_more(NONSPACE))) 
    block = _get_system_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None
    out='  '.join(keyword)

    return out

def read_label(input_string):
    """ 
    """
    pattern = ('Label' +
               one_or_more(SPACE) + capturing(one_or_more(NONSPACE))) 
    block = _get_system_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None
    out='  '.join(keyword)

    return out


def read_num_axm(input_string):
    """ 
    """
    pattern = ('NumAXM' +
               one_or_more(SPACE) + capturing(one_or_more(INTEGER)) +
               one_or_more(SPACE) + capturing(one_or_more(INTEGER)) +
               one_or_more(SPACE) + capturing(one_or_more(INTEGER)))
    block = _get_system_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None
    nA = keyword[0]
    nX = keyword[1]
    nM = keyword[2]

    return nA, nX, nM


def read_reactants(input_string,nA):
    """ 
    """
    a_line = _get_line(input_string,'Reactants', nA)

    assert a_line is not None
    out=' '.join(a_line)

    return out

def read_xcolliders(input_string,nX):
    """ 
    """
    x_line = _get_line(input_string,'XColliders', nX)

    assert x_line is not None
    out=' '.join(x_line)

    return out

def read_mcolliders(input_string,nM):
    """ 
    """
    m_line = _get_line(input_string,'MColliders', nM)

    assert m_line is not None
    out=' '.join(m_line)

    return out

def read_natoms_a(input_string,nA):
    """ 
    """
    a_line = _get_integer_line(input_string,'NAtomsA', nA)

    assert a_line is not None
    out=' '.join(a_line)

    return out

def read_natoms_x(input_string,nX):
    """ 
    """
    x_line = _get_integer_line(input_string,'NAtomsX', nX)

    assert x_line is not None
    out=' '.join(x_line)

    return out

def read_natoms_m(input_string,nM):
    """ 
    """
    m_line = _get_integer_line(input_string,'NAtomsM', nM)

    assert m_line is not None
    out=' '.join(m_line)

    return out


def read_xa(input_string,nA):
    """ 
    """
    a_line = _get_float_line(input_string,'xA', nA)

    assert a_line is not None
    out=' '.join(a_line)

    return out

def read_xx(input_string,nX):
    """ 
    """
    x_line = _get_float_line(input_string,'xX', nX)

    assert x_line is not None
    out=' '.join(x_line)

    return out

def read_xm(input_string,nM):
    """ 
    """
    m_line = _get_float_line(input_string,'xM', nM)

    assert m_line is not None
    out=' '.join(m_line)

    return out


def read_blist(input_string, nA):
    """ 
    """
    b_line = _get_float_line(input_string,'BList', nA)

    assert b_line is not None
    out=' '.join(b_line)

    return out

def read_temperature(input_string):
    """ 
    """

    pattern = ('Temperature' +
               one_or_more(SPACE) + 
               capturing(FLOAT))
    block = _get_system_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None
#    keyword = int(keyword)

    return keyword


def read_steps(input_string):
    """ 
    """

    pattern = ('Steps' +
               one_or_more(SPACE) + 
               capturing(INTEGER))
    block = _get_system_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None

    return keyword


def _get_line(input_string,check_string,num):
    """ grabs the line of text containing num entries
    """
    tmp = []
    for _ in range(int(num)):
        tmp.append(one_or_more(SPACE))
        tmp.append(capturing(NONSPACE))

    pattern = (str(check_string) + ''.join(tmp)
        )
    section = first_capture(pattern, input_string)

    assert section is not None

    return section

def _get_integer_line(input_string,check_string,num):
    """ grabs the line of text containing num entries
    """
    tmp = []
    for _ in range(int(num)):
        tmp.append(one_or_more(SPACE))
        tmp.append(capturing(INTEGER))

    pattern = (str(check_string) + ''.join(tmp)
        )
    section = first_capture(pattern, input_string)

    assert section is not None

    return section

def _get_float_line(input_string,check_string,num):
    """ grabs the line of text containing num entries
    """
    tmp = []
    for _ in range(int(num)):
        tmp.append(one_or_more(SPACE))
        tmp.append(capturing(FLOAT))

    pattern = (str(check_string) + ''.join(tmp)
        )
    section = first_capture(pattern, input_string)

    assert section is not None

    return section


def _get_system_info_section(input_string):
    """ grabs the section of text containing all of the job keywords
        for system info
    """
    pattern = (escape('$system_info') + LINE_FILL + NEWLINE +
               capturing(one_or_more(WILDCARD, greedy=False)) +
               escape('$end'))
    section = first_capture(pattern, input_string)

    assert section is not None

    return section


def read_ntrajs(input_string):
    """ 
    """

    pattern = ('NTrajs' +
               one_or_more(SPACE) + 
               capturing(INTEGER))
    block = _get_directory_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None

    return keyword

def read_nprocs(input_string):
    """ 
    """

    pattern = ('NProcs' +
               one_or_more(SPACE) + 
               capturing(INTEGER))
    block = _get_directory_info_section(input_string)

    keyword = first_capture(pattern, block)

    assert keyword is not None

    return keyword

#def read_potentials(input_string):


def _get_directory_info_section(input_string):
    """ grabs the section of text containing all of the job keywords
        for directory info
    """
    pattern = (escape('$directory_info') + LINE_FILL + NEWLINE +
               capturing(one_or_more(WILDCARD, greedy=False)) +
               escape('$end'))
    section = first_capture(pattern, input_string)

    assert section is not None

    return section


# Functions to check for errors in the input file

def check_system_info_keywords(input_string):
    """ obtains the keywords defined in the input by the user
    """
    section_string = _get_system_info_section(input_string)
    defined_keywords = _get_defined_keywords(section_string)

    # Check if keywords are supported
    if not all(keyword in SI_SUPPORTED_KEYWORDS
               for keyword in defined_keywords):
        raise NotImplementedError

    # Check if elements of keywords
    if not all(keyword in defined_keywords
               for keyword in SI_REQUIRED_KEYWORDS):
        raise NotImplementedError

    print("System Info Input:")
    print(section_string)


def check_directory_info_keywords(input_string):
    """ obtains the keywords defined in the input by the user
    """
    section_string = _get_directory_info_section(input_string)
    defined_keywords = _get_defined_keywords(section_string)

    # Check if keywords are supported
    if not all(keyword in DI_SUPPORTED_KEYWORDS
               for keyword in defined_keywords):
        raise NotImplementedError

    # Check if elements of keywords
    if not all(keyword in defined_keywords
               for keyword in DI_REQUIRED_KEYWORDS):
        raise NotImplementedError

    print("Directory Info Input:")
    print(section_string)


def _get_defined_keywords(section_string):
    """ gets a list of all the keywords defined in a section
    """

    defined_keys = []
    for line in section_string.splitlines():
        tmp = line.strip().split(' ')[0]
        defined_keys.append(tmp.strip())

    return defined_keys
