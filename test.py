import inline_tests

import inspect
import sys


classes = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['inline_tests']) if inspect.isclass(cls_obj)]
print(classes)