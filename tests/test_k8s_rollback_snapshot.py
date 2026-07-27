import importlib.util, unittest
from pathlib import Path
from unittest.mock import patch
SCRIPT=Path(__file__).resolve().parents[1]/"tools/k8s_rollback_snapshot.py"
spec=importlib.util.spec_from_file_location("snapshot",SCRIPT); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
class Tests(unittest.TestCase):
    def test_commands_are_read_only(self):
        text=" ".join(" ".join(c) for c in module.build_commands("prod","api"))
        for forbidden in (" delete "," undo "," pause "," patch "," apply "):
            self.assertNotIn(forbidden,text)
    @patch.object(module,"execute",return_value=(0,"ok"))
    def test_report_contains_identity_and_output(self,_):
        report=module.collect("prod","api")
        self.assertIn("Deployment: `api`",report); self.assertIn("ok",report)
if __name__=="__main__": unittest.main()
