"""CC-CEDICT example."""

import json

from pycccedict.cccedict import CcCedict

def main():
    """Main."""
    cccedict = CcCedict()
    cccedict.get_entry('猫')

if __name__ == "__main__":
    main()
