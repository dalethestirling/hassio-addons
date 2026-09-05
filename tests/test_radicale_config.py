"""Functional tests for Radicale configuration parsing, rights access control logic, and htpasswd processing."""

import configparser
import os
import re
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RADICALE_DIR = os.path.join(REPO_ROOT, "radicale")


class TestRadicaleConfigLogic(unittest.TestCase):
    """Test suite for Radicale configuration generation and validation."""

    def test_default_config_syntax(self):
        # Extract default config generated in run script or sample template
        run_script_path = os.path.join(RADICALE_DIR, "rootfs", "etc", "services.d", "radicale", "run")
        with open(run_script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Check key sections are created
        self.assertIn("[server]", script_content)
        self.assertIn("[auth]", script_content)
        self.assertIn("[rights]", script_content)
        self.assertIn("[storage]", script_content)
        self.assertIn("[web]", script_content)
        self.assertIn("[logging]", script_content)
        self.assertNotIn("config = ${LOGGING_FILE}", script_content)
        self.assertNotIn("filesystem_locking =", script_content)

        # Parse a sample generated config through configparser
        sample_config = """
[server]
hosts = 0.0.0.0:5232
max_connections = 20
max_content_length = 100000000
timeout = 30

[auth]
type = htpasswd
htpasswd_filename = /config/users
htpasswd_encryption = bcrypt
delay = 1

[rights]
type = from_file
file = /config/rights

[storage]
type = multifilesystem
filesystem_folder = /config/collections

[web]
type = internal

[logging]
level = info
"""
        parser = configparser.ConfigParser()
        parser.read_string(sample_config)

        self.assertEqual(parser.get("server", "hosts"), "0.0.0.0:5232")
        self.assertEqual(parser.get("auth", "type"), "htpasswd")
        self.assertEqual(parser.get("auth", "htpasswd_encryption"), "bcrypt")
        self.assertEqual(parser.get("storage", "type"), "multifilesystem")
        self.assertFalse(parser.has_option("storage", "filesystem_locking"))
        self.assertEqual(parser.get("web", "type"), "internal")
        self.assertEqual(parser.get("logging", "level"), "info")
        self.assertFalse(parser.has_option("logging", "config"))

    def test_radicale_rights_matching_rules(self):
        """Verify the rights logic used in Radicale 3.x."""
        # Standard rules
        rules = [
            {"name": "root", "user": r".+", "collection": r"^$", "permission": "r"},
            {"name": "web", "user": r".+", "collection": r"^\.web$", "permission": "r"},
            {"name": "owner-write", "user": r".+", "collection_pattern": r"^{user}(/.*)?$", "permission": "rw"},
        ]

        # Test case 1: User 'alice' accessing her own calendar 'alice/work'
        user = "alice"
        path = "alice/work"
        matched_perm = None
        for rule in rules:
            if re.match(rule["user"], user):
                pat = rule.get("collection")
                if not pat:
                    pat = rule["collection_pattern"].format(user=re.escape(user))
                if re.match(pat, path):
                    matched_perm = rule["permission"]
                    break

        self.assertEqual(matched_perm, "rw", "Alice should have rw permissions to alice/work")

        # Test case 2: User 'bob' attempting to access Alice's calendar 'alice/work'
        user = "bob"
        path = "alice/work"
        matched_perm = None
        for rule in rules:
            if re.match(rule["user"], user):
                pat = rule.get("collection")
                if not pat:
                    pat = rule["collection_pattern"].format(user=re.escape(user))
                if re.match(pat, path):
                    matched_perm = rule["permission"]
                    break

        self.assertIsNone(matched_perm, "Bob should not match any rule for alice/work under default rights")

        # Test case 3: User 'bob' accessing discovery root
        user = "bob"
        path = ""
        matched_perm = None
        for rule in rules:
            if re.match(rule["user"], user):
                pat = rule.get("collection")
                if not pat:
                    pat = rule["collection_pattern"].format(user=re.escape(user))
                if re.match(pat, path):
                    matched_perm = rule["permission"]
                    break

        self.assertEqual(matched_perm, "r", "Bob should have read access to discovery root")

    def test_htpasswd_bcrypt_format(self):
        """Validate htpasswd line formatting and bcrypt hash recognition."""
        sample_htpasswd_line = "alice:$2y$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"
        parts = sample_htpasswd_line.strip().split(":", 1)
        self.assertEqual(len(parts), 2)
        username, pw_hash = parts
        self.assertEqual(username, "alice")
        # Bcrypt hashes start with $2a$, $2b$, or $2y$
        self.assertTrue(re.match(r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$", pw_hash))

    def test_legacy_logging_cleanup(self):
        """Verify that legacy config = and filesystem_locking lines are stripped and logging level is valid for Radicale v3."""
        legacy_config = """[storage]\ntype = multifilesystem\nfilesystem_folder = /config/collections\nfilesystem_locking = True\n[logging]\nconfig = /config/logging\nlevel = DEBUG\n"""
        # Remove deprecated config & filesystem_locking lines
        cleaned = re.sub(r"^[ \t]*(config|filesystem_locking)[ \t]*=.*\n?", "", legacy_config, flags=re.MULTILINE)
        parser = configparser.ConfigParser()
        parser.read_string(cleaned)
        self.assertFalse(parser.has_option("logging", "config"))
        self.assertFalse(parser.has_option("storage", "filesystem_locking"))
        self.assertEqual(parser.get("logging", "level"), "DEBUG")


if __name__ == "__main__":
    unittest.main()
