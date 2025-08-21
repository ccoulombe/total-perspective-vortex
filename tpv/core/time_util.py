"""
Utility functions for handling time format conversions, particularly for SLURM time specifications.
"""
import re
import logging

log = logging.getLogger(__name__)


def convert_slurm_time_format(time_str: str) -> str:
    """
    Convert SLURM time formats with days to hours-only format for better Galaxy compatibility.
    
    Converts:
    - "days-hours:minutes:seconds" to "hours:minutes:seconds" 
    - "days-hours" to "hours:minutes"
    
    Leaves other formats unchanged.
    
    Args:
        time_str: Time specification string that may contain SLURM time format
        
    Returns:
        Converted time string with days converted to hours, or original string if no conversion needed
    """
    if not isinstance(time_str, str):
        return time_str
        
    # Pattern for days-hours:minutes:seconds format (e.g., "7-00:00:00")
    days_hms_pattern = r'(\d+)-(\d+):(\d+):(\d+)'
    # Pattern for days-hours format (e.g., "7-00")  
    days_h_pattern = r'(\d+)-(\d+)(?![:\d])'  # negative lookahead to avoid matching days-hours:minutes
    
    def replace_days_hms(match):
        days, hours, minutes, seconds = map(int, match.groups())
        total_hours = days * 24 + hours
        converted = f"{total_hours:d}:{minutes:02d}:{seconds:02d}"
        log.debug(f"Converted SLURM time format {match.group(0)} to {converted}")
        return converted
        
    def replace_days_h(match):
        days, hours = map(int, match.groups())
        total_hours = days * 24 + hours
        converted = f"{total_hours:d}:00"
        log.debug(f"Converted SLURM time format {match.group(0)} to {converted}")
        return converted
    
    # Apply conversions
    result = re.sub(days_hms_pattern, replace_days_hms, time_str)
    result = re.sub(days_h_pattern, replace_days_h, result)
    
    return result


def process_slurm_parameters(param_value: str) -> str:
    """
    Process parameter values that may contain SLURM time specifications.
    
    Detects --time= specifications and converts problematic day-hour formats
    to hours-only formats for better Galaxy compatibility.
    
    Args:
        param_value: Parameter string that may contain SLURM options
        
    Returns:
        Parameter string with SLURM time formats converted if needed
    """
    if not isinstance(param_value, str):
        return param_value
        
    # Pattern to find --time= specifications in parameter strings
    time_option_pattern = r'(--time=)([^\s]+)'
    
    def convert_time_option(match):
        prefix = match.group(1)  # "--time="
        time_value = match.group(2)  # the time specification
        converted_time = convert_slurm_time_format(time_value)
        return prefix + converted_time
    
    return re.sub(time_option_pattern, convert_time_option, param_value)