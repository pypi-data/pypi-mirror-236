__version__ = "0.0.9"
from .nbs import NotebookAggregator, NotebookFinder, NotebookLoader, NotebookLogger, NotebookPrefixer, NotebookViewer
from .nbs.utils import (
    nextint, str2int, int2str, find_nb, read_nb, read_cell,
    fmt_cell, fmt_cells, show_nb, 
)

from .magic import SkipMagic
__all__ = [
    'NotebookAggregator', 'NotebookFinder', 'NotebookLoader', 
    'NotebookLogger', 'NotebookPrefixer', 'NotebookViewer',
    
    'SkipMagic',
    
    'nextint', 'str2int', 'int2str', 'find_nb', 'read_nb', 'read_cell',
    'fmt_cell', 'fmt_cells', 'show_nb', 
]
