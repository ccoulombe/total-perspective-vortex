#!/usr/bin/env python
"""
Tests for SLURM time format conversion utilities
"""

import unittest
from tpv.core.time_util import convert_slurm_time_format, process_slurm_parameters


class TestSlurmTimeFormatConversion(unittest.TestCase):
    
    def test_convert_days_hours_minutes_seconds_format(self):
        """Test conversion of days-hours:minutes:seconds format"""
        # 7 days = 168 hours
        self.assertEqual(convert_slurm_time_format("7-00:00:00"), "168:00:00")
        self.assertEqual(convert_slurm_time_format("1-12:30:45"), "36:30:45")
        self.assertEqual(convert_slurm_time_format("0-06:15:30"), "6:15:30")
        
    def test_convert_days_hours_format(self):
        """Test conversion of days-hours format"""
        # 7 days = 168 hours
        self.assertEqual(convert_slurm_time_format("7-00"), "168:00")
        self.assertEqual(convert_slurm_time_format("1-12"), "36:00")
        self.assertEqual(convert_slurm_time_format("0-06"), "6:00")
        
    def test_preserve_existing_formats(self):
        """Test that existing working formats are preserved"""
        # These formats should pass through unchanged
        self.assertEqual(convert_slurm_time_format("168:00:00"), "168:00:00")
        self.assertEqual(convert_slurm_time_format("12:30:45"), "12:30:45")
        self.assertEqual(convert_slurm_time_format("30"), "30")
        self.assertEqual(convert_slurm_time_format("45:30"), "45:30")
        
    def test_preserve_non_time_strings(self):
        """Test that non-time strings are preserved"""
        self.assertEqual(convert_slurm_time_format("hello-world"), "hello-world")
        self.assertEqual(convert_slurm_time_format("test-123-abc"), "test-123-abc")
        self.assertEqual(convert_slurm_time_format(""), "")
        
    def test_process_slurm_parameters_with_time_option(self):
        """Test processing of full parameter strings with --time option"""
        # Test the problematic case from the issue
        param = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --time=7-00:00:00 --partition=main"
        expected = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --time=168:00:00 --partition=main"
        self.assertEqual(process_slurm_parameters(param), expected)
        
        # Test days-hours format
        param = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --time=7-00 --partition=main"
        expected = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --time=168:00 --partition=main"
        self.assertEqual(process_slurm_parameters(param), expected)
        
        # Test that working format is preserved
        param = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --time=168:00:00 --partition=main"
        self.assertEqual(process_slurm_parameters(param), param)
        
    def test_process_slurm_parameters_multiple_time_options(self):
        """Test processing parameters with multiple --time options"""
        param = "--time=7-00:00:00 --other-option --time=1-12:30:00"
        expected = "--time=168:00:00 --other-option --time=36:30:00"
        self.assertEqual(process_slurm_parameters(param), expected)
        
    def test_process_slurm_parameters_no_time_option(self):
        """Test that parameters without --time are unchanged"""
        param = "--nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4096 --partition=main"
        self.assertEqual(process_slurm_parameters(param), param)
        
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with non-string input
        self.assertEqual(convert_slurm_time_format(None), None)
        self.assertEqual(convert_slurm_time_format(123), 123)
        self.assertEqual(process_slurm_parameters(None), None)
        self.assertEqual(process_slurm_parameters(123), 123)
        
        # Test with zero values
        self.assertEqual(convert_slurm_time_format("0-00:00:00"), "0:00:00")
        self.assertEqual(convert_slurm_time_format("0-00"), "0:00")
        
        # Test large values
        self.assertEqual(convert_slurm_time_format("365-00:00:00"), "8760:00:00")  # 365 days = 8760 hours


if __name__ == "__main__":
    unittest.main()