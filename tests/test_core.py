import unittest
from mamba_actuator.core import parse, simulate, Request

class TestMambaActuator(unittest.TestCase):
    def test_list(self):
        self.assertEqual(parse("lista las ventanas").action, "window.list")
    def test_close_requires_confirmation(self):
        req = parse("cierra la ventana de Blender")
        self.assertEqual((req.action, req.app, req.requires_confirmation), ("window.close", "blender", True))
        self.assertFalse(simulate(req)["executed"])
    def test_focus(self):
        self.assertEqual(parse("enfoca Blender").action, "window.focus")
    def test_launch(self):
        self.assertEqual(parse("abre Blender").action, "app.launch")
    def test_cancel(self):
        self.assertEqual(parse("detente").action, "queue.cancel")
    def test_unknown_denied(self):
        with self.assertRaises(ValueError):
            parse("borra todos mis archivos")
    def test_empty_denied(self):
        with self.assertRaises(ValueError):
            parse("   ")
    def test_non_dry_run_denied(self):
        req = Request("test", "window.close", "blender", dry_run=False)
        self.assertEqual(simulate(req)["status"], "denied")

if __name__ == "__main__":
    unittest.main()
