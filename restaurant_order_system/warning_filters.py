import warnings
import re

# Create a filter to suppress specific warnings
class SuppressDeprecationWarnings:
    def __init__(self):
        self.pattern = re.compile(r'pkg_resources is deprecated as an API')
    
    def __enter__(self):
        self._original_filters = warnings.filters[:]
        warnings.filterwarnings('ignore', category=UserWarning, message=self.pattern)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        warnings.filters = self._original_filters

# Apply the filter immediately when the module is imported
with SuppressDeprecationWarnings():
    pass
