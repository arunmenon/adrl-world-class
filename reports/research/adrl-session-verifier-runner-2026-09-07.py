import importlib.util, os, sys, unittest
from pathlib import Path
sys.path.insert(0, os.getcwd())
name = sys.argv[1]
expected = int(sys.argv[2])
path = Path(__file__).parent / name
spec = importlib.util.spec_from_file_location("operator_checks", path)
try:
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite = unittest.TestLoader().loadTestsFromModule(module)
    if suite.countTestCases() != expected:
        raise RuntimeError("Unexpected check count")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
except Exception:
    raise SystemExit(2)
if result.errors or result.skipped or result.expectedFailures or result.unexpectedSuccesses:
    raise SystemExit(2)
raise SystemExit(1 if result.failures else 0)
