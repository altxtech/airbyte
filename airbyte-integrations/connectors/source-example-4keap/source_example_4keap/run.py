#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from .source import SourceExample_4keap

def run():
    source = SourceExample_4keap()
    launch(source, sys.argv[1:])
