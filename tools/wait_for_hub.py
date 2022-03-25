# Copyright (c) 2022 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""\
Sleep until WorkflowHub is ready or the timeout is reached.
"""

import argparse
import time

import requests
from requests.exceptions import ConnectionError


DEFAULT_URL = "https://workflowhub.eu"


def main(args):
    print(f"Waiting {args.timeout} seconds for {args.url}")
    start = time.time()
    while True:
        elapsed = round(time.time() - start)
        try:
            requests.get(args.url).status_code
        except ConnectionError:
            time.sleep(1)
        else:
            print(f"{args.url} ready after {elapsed} seconds")
            break
        if elapsed >= args.timeout:
            print("Timeout reached")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url", metavar="URL", default=DEFAULT_URL,
                        help="WorkflowHub URL")
    parser.add_argument("-t", "--timeout", type=int, metavar="INT", default=120,
                        help="timeout in seconds")
    main(parser.parse_args())
