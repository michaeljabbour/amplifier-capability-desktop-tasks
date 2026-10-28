#!/usr/bin/env python3
"""Meaningful local functional checks; no provider calls or production activation."""
import asyncio
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

sys.path.insert(0,str(ROOT/'modules/tool-cua'))
from amplifier_module_tool_cua.backends.fixture import FixtureBackend
from amplifier_module_tool_cua.models import ActionStatus
class Gate(unittest.TestCase):
    def test_fixture_observation_and_action_are_distinct(self):
        async def scenario():
            b=FixtureBackend();r=await b.semantic_tree();self.assertEqual(r.status,ActionStatus.SUCCESS);self.assertEqual(b.action_log,[])
            await b.click(350,500);self.assertEqual(b.action_log,[{'action':'click','x':350,'y':500,'button':'left'}])
            screen=await b.screenshot();self.assertIn('screenshot_base64',screen.data)
        asyncio.run(scenario())

if __name__=='__main__':unittest.main(verbosity=2)
