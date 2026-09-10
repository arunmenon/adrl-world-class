import tempfile
import unittest
from pathlib import Path
from validation.core.templates import PromptTemplateLoader

class TestTemplateCompatibility(unittest.TestCase):
    def render(self, text, values):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'fixture.txt').write_text(text)
            return PromptTemplateLoader(root).render('fixture.txt', values)

    def test_escaped_braces_stay_literal(self):
        self.assertEqual(self.render('Literal {{task_type}}', {'task_type': 'intent'}), 'Literal {task_type}')

    def test_format_specifier_is_honored(self):
        self.assertEqual(self.render('Score: {score:.1f}', {'score': 3.14}), 'Score: 3.1')

    def test_missing_formatted_variable_raises(self):
        with self.assertRaises(KeyError):
            self.render('Score: {absent:.1f}', {})

    def test_simple_missing_variable_raises(self):
        with self.assertRaises(KeyError):
            self.render('{absent}', {})
