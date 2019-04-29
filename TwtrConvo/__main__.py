import sys
import argparse
from .twtrconvo import main

if __name__ == '__main__':
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description='Type a ticker!')
    parser.add_argument('-t', '--ticker', dest='ticker', action='store',
                        help='Ticker symbol that will be analyzed.')
    parser.add_argument('-b', '--build-dataset', dest='build',
                        action='store_true',
                        help='Build dataset (default will load saved set)')
    # Cast args to dict
    args = vars(parser.parse_args(sys.argv[1:]))

    main(**args)