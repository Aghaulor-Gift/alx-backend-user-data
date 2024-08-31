#!/usr/bin/env python3
"""A  function called filter_datum that returns the log message obfuscated"""
import re

def filter_datum(fields, redaction, message, separator):
    """filter_datum that returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)})=([^\\{separator}]+)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
