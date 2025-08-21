#!/usr/bin/env python
"""
Test script to reproduce the SLURM time format issue described in issue #163
"""

import os
import tempfile
import unittest
from tests.test_mapper_basic import TestMapperBaseTestCase


class TestSlurmTimeFormat(TestMapperBaseTestCase):
    
    def test_slurm_time_format_days_hours_minutes_seconds(self):
        """Test SLURM time format: days-hours:minutes:seconds (e.g., 7-00:00:00)"""
        config_content = """
global:
  default_inherits: default

tools:
  default:
    cores: 1
    mem: 1
    params:
      native_specification: "--time=7-00:00:00"

destinations:
  slurm:
    runner: slurm
"""
        
        with tempfile.NamedTemporaryFile("w+t", suffix=".yml", delete=False) as tmp_file:
            tmp_file.write(config_content)
            tmp_file.flush()
            
            try:
                tool = self._get_tool("test_tool")
                user = self._get_user("test_user")
                destination = self._map_to_destination(tool, user, tpv_config_path=tmp_file.name)
                
                # Should be able to map without error
                self.assertEqual(destination.id, "slurm")
                # The native_specification should be properly evaluated
                self.assertEqual(destination.params["native_specification"], "--time=7-00:00:00")
                
            finally:
                os.unlink(tmp_file.name)

    def test_slurm_time_format_days_hours(self):
        """Test SLURM time format: days-hours (e.g., 7-00)"""
        config_content = """
global:
  default_inherits: default

tools:
  default:
    cores: 1
    mem: 1
    params:
      native_specification: "--time=7-00"

destinations:
  slurm:
    runner: slurm
"""
        
        with tempfile.NamedTemporaryFile("w+t", suffix=".yml", delete=False) as tmp_file:
            tmp_file.write(config_content)
            tmp_file.flush()
            
            try:
                tool = self._get_tool("test_tool")
                user = self._get_user("test_user")
                destination = self._map_to_destination(tool, user, tpv_config_path=tmp_file.name)
                
                # Should be able to map without error
                self.assertEqual(destination.id, "slurm")
                # The native_specification should be properly evaluated
                self.assertEqual(destination.params["native_specification"], "--time=7-00")
                
            finally:
                os.unlink(tmp_file.name)

    def test_slurm_time_format_hours_minutes_seconds_working(self):
        """Test SLURM time format that currently works: hours:minutes:seconds (e.g., 168:00:00)"""
        config_content = """
global:
  default_inherits: default

tools:
  default:
    cores: 1
    mem: 1
    params:
      native_specification: "--time=168:00:00"

destinations:
  slurm:
    runner: slurm
"""
        
        with tempfile.NamedTemporaryFile("w+t", suffix=".yml", delete=False) as tmp_file:
            tmp_file.write(config_content)
            tmp_file.flush()
            
            try:
                tool = self._get_tool("test_tool")
                user = self._get_user("test_user")
                destination = self._map_to_destination(tool, user, tpv_config_path=tmp_file.name)
                
                # Should be able to map without error
                self.assertEqual(destination.id, "slurm")
                # The native_specification should be properly evaluated
                self.assertEqual(destination.params["native_specification"], "--time=168:00:00")
                
            finally:
                os.unlink(tmp_file.name)


if __name__ == "__main__":
    unittest.main()