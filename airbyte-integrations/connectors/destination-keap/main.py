#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from destination_keap import DestinationKeap

if __name__ == "__main__":
    DestinationKeap().run(sys.argv[1:])
