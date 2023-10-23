""" cite your sources """

#from functools import wraps
#from itertools import chain
from types import MappingProxyType
from typing import Any
from typing import Callable
#from typing import Dict
from typing import Optional
from typing import Union
from typing import Iterable
from typing import Iterator
#from typing import Tuple
from typing import TypeVar
from typing import ParamSpec

from inspect import ismodule
from inspect import isfunction
from inspect import isclass
from inspect import getmembers
#from pyfunctional import pure
from peval import pure

#from iautil.oops import UnexpectedExecutionPathError
from iautil.predicates import is_nonempty_string

Authors = Union[str,Iterable[str]]
CitationFmt = Callable[[
    Optional[Authors],
    Optional[str],
    Optional[str],
    Optional[str]],str]
#Iter = Union[Iterable,Iterator]
T = TypeVar('T')
P = ParamSpec('P')

def citation(
    authors:Optional[Authors]=None,
    year:Optional[str]=None,
    title:Optional[str]=None,
    url:Optional[str]=None)->Callable[[Callable[P,T]],Callable[P,T]]:
    """ cite your sources """
    #@wraps(func)
    def decorator(func:Callable[P,T])->Callable[P,T]:
        # TADA only add if not None
        #func.__dict__['citation'] = {
        #func['citation'] = {
        #func.citation = {
        setattr(func, 'citation', {
            'authors': authors,
            'year': year,
            'title': title,
            'url': url,
        })
        return func
    return decorator

@pure
def format_mla_citation(
    authors: Optional[Authors]=None,
    year: Optional[str] = None,
    title: Optional[str] = None,
    url: Optional[str] = None) -> str:
    """ MLA format citation """
    authors_str:str = format_authors(authors, suffix='.')
    year_str:str = format_field(year, suffix='.')
    title_str:str = format_field(title, prefix='"', suffix='." ')
    url_str:str = format_field(url, prefix='<', suffix='>.')
    #return f'{authors_str} {year_str} {title_str} {url_str}'
    #return f'{authors_str} {year_str} {title_str} {url_str}'
    return join_format_strings(authors_str, year_str, title_str, url_str)

@pure
def format_apa_citation(
    authors: Optional[Authors]=None,
    year: Optional[str] = None,
    title: Optional[str] = None,
    url: Optional[str] = None) -> str:
    """ APA format citation """
    authors_str:str = format_authors(authors, suffix='.')
    year_str:str = format_field(year, prefix='(', suffix=')')
    title_str:str = format_field(title, suffix='. ')
    url_str:str = format_field(url, prefix='Retrieved from ', suffix='.')
    #return f'{authors_str} {year_str} {title_str} {url_str}'
    return join_format_strings(authors_str, year_str, title_str, url_str)

@pure
def format_chicago_citation(
    authors: Optional[Authors]=None,
    year: Optional[str] = None,
    title: Optional[str] = None,
    url: Optional[str] = None) -> str:
    """ Chicago/Turabian format citation """
    authors_str:str = format_authors(authors, suffix='.')
    year_str:str = format_field(year, prefix='(', suffix=')')
    title_str:str = format_field(title, suffix='. ')
    url_str:str = format_field(url, prefix='Available at ', suffix='.')
    #return f'{authors_str} {title_str} {year_str} {url_str}'
    return join_format_strings(authors_str, year_str, title_str, url_str)

@pure
def format_harvard_citation(
    authors: Optional[Authors]=None,
    year: Optional[str] = None,
    title: Optional[str] = None,
    url: Optional[str] = None) -> str:
    """ Harvard format citation """
    authors_str:str = format_authors(authors, suffix='.')
    year_str:str = format_field(year, prefix='(', suffix=')')
    title_str:str = format_field(title, suffix='. ')
    url_str:str = format_field(url, prefix='Available from: ', suffix='.')
    #return f'{authors_str} {year_str} {title_str} {url_str}'
    return join_format_strings(authors_str, year_str, title_str, url_str)

@pure
def format_ieee_citation(
    authors: Optional[Authors]=None,
    year: Optional[str] = None,
    title: Optional[str] = None,
    url: Optional[str] = None) -> str:
    """ IEEE format citation """
    authors_str:str = format_authors(authors, suffix='.')
    year_str:str = format_field(year, suffix='.') # added by me
    title_str:str = format_field(title, suffix=',')
    url_str:str = format_field(url, prefix='[Online]. Available: ', suffix='.')
    #return f'{authors_str} {title_str} {year}. {url_str}'
    #return f'{authors_str} {title_str} {year_str} {url_str}'
    return join_format_strings(authors_str, year_str, title_str, url_str)

@pure
def join_format_strings(
    authors:str,
    year:str,
    title:str,
    url:str)->str:
    """ handle extra spaces """
    fields = (authors, year, title, url,)
    fields = filter(is_nonempty_string, fields)
    return ' '.join(fields)


@pure
def format_authors(
    authors: Optional[Authors],
    prefix: str = '',
    suffix: str = '') -> str:
    """ format author(s) helper """
    if not authors:
        return ''
    if isinstance(authors, str):
        authors_str = authors
    elif isinstance(authors, (Iterable,Iterator,)):
        assert not isinstance(authors, str)
        authors_str = ', '.join(authors)
    else:
        assert not isinstance(authors, list)
        authors_str = authors
    authors_str = f'{prefix}{authors_str}{suffix}' if authors_str else ''
    return authors_str

@pure
def format_field(
    field_value: Optional[str],
    prefix: str = '',
    suffix: str = '') -> str:
    """ format field helper """
    field_str:str = f'{prefix}{field_value}{suffix}' if field_value else ''
    return field_str

# TADA do the binding before the recursion
#def get_citations(
#    obj:Any,
#    citation_format:CitationFmt,
#    recurse:bool=True)->Iterable[str]:
#    """ (recursively) get citations from an object """
#    citation1:Iterable[str] = get_citations_leaf(obj, citation_format)
#    citation2:Iterable[str] = get_citations_loop(obj, citation_format, recurse)
#    return chain(citation1, citation2)
#
#def get_citations_loop(
#    obj:Any,
#    citation_format:CitationFmt,
#    recurse:bool)->Iterable[str]:
#    """ recursive loop """
#    if not recurse:
#        return ()
#    members:Any = getmembers(obj)
#    citations_helper:Callable[
#        [Tuple[str,Any]],
#        Iterable[str]] = get_citations_helper(citation_format)
#    citations:Iterable[Iterable[str]] = map(citations_helper, members)
#    return chain(*citations)
#
#def get_citations_helper(
#    citation_format:CitationFmt)->Callable[[Tuple[str,Any]],Iterable[str]]:
#    """ bind citation_format """
#    def citations_helper(
#        name_member:Tuple[str,Any])->Iterable[str]:
#        """ loop body """
#        _, member = name_member
#        if isfunction(member) and 'citation' in member.__dict__:
#            return get_citations_leaf(member, citation_format)
#        if ismodule(member) or isclass(member):
#            return get_citations(member, citation_format, recurse=True)
#        return ()
#        #raise UnexpectedExecutionPathError()
#    return citations_helper
#
#def get_citations_leaf(obj:Any, citation_format:CitationFmt)->Iterable[str]:
#    """ recursion leaf """
#    if 'citation' not in obj.__dict__:
#        return ()
#    citation_data:Dict[str,str] = obj.__dict__['citation']
#    citation_str:str = citation_format(**citation_data)
#    return (citation_str,)




def get_citations(
    obj: Any,
    citation_format: CitationFmt,
    recurse: bool = True,
    visited: Optional[set] = None
) -> Iterable[str]:
    """ (recursively) get citations from an object """
    if visited is None:
        visited = set()

    assert not isinstance(obj, MappingProxyType)
    if obj in visited:
        return

    visited.add(obj)

    if isfunction(obj) and 'citation' in obj.__dict__:
        yield from get_citations_leaf(obj, citation_format)
    elif (ismodule(obj) or isclass(obj)) and recurse:
        members = getmembers(obj)
        for _, member in members:
            yield from get_citations(member, citation_format, recurse, visited)


def get_citations_leaf(obj: Any, citation_format: CitationFmt) -> Iterable[str]:
    """ recursion leaf """
    if 'citation' not in obj.__dict__:
        return

    citation_data = obj.__dict__['citation'] # getattr ?
    citation_str = citation_format(**citation_data)
    yield citation_str
