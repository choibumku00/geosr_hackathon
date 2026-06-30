import os
import sys

# scripts/ 디렉터리를 import 경로에 추가 (모듈은 형제 import 사용)
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
