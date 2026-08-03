import os
import sys
import pytest

root = r'c:\Users\Admin\Documents\VYOM_v3'
os.chdir(root)
result = pytest.main(['-q', 'tests'])
print(f'PYTEST_EXIT={result}')
