import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate_package.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class LinkTests(unittest.TestCase):
    def test_distribution_hashes_only_for_verified_skill_files(self):
        old = validator.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            validator.ROOT = Path(tmp)
            try:
                (validator.ROOT / 'SKILL.md').write_text('sample')
                data = {'schema_version': 1, 'repository': 'https://github.com/yzyboeing/flight-doc-translate',
                        'builder_repository': 'https://github.com/yzyboeing/flight-notes-toolkit',
                        'name': 'flight-doc-translate', 'version': '1.0.0', 'visibility': 'public',
                        'commit': 'a' * 40, 'builder_commit': 'b' * 40,
                        'files': {'SKILL.md': hashlib.sha256(b'sample').hexdigest()}}
                path = validator.ROOT / 'SOURCE.json'
                path.write_text(json.dumps(data))
                self.assertTrue(validator.valid_distribution_metadata(path))
                (validator.ROOT / 'SKILL.md').write_text('changed')
                self.assertFalse(validator.valid_distribution_metadata(path))
                data['files'] = {'../outside': '0' * 64}
                path.write_text(json.dumps(data))
                self.assertFalse(validator.valid_distribution_metadata(path))
            finally:
                validator.ROOT = old

    def test_external_link_is_not_local_but_missing_local_link_fails(self):
        old = validator.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            validator.ROOT = Path(tmp)
            try:
                (validator.ROOT / 'SKILL.md').write_text('entry')
                (validator.ROOT / 'README.md').write_text('[remote](https://example.invalid/rules.md)')
                self.assertEqual(validator.markdown_links(), [])
                (validator.ROOT / 'README.md').write_text('[local](missing.md)')
                self.assertEqual(len(validator.markdown_links()), 1)
            finally:
                validator.ROOT = old


if __name__ == '__main__':
    unittest.main()
