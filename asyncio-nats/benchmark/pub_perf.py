import argparse, sys
import asyncio
import time
from random import randint
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout

DEFAULT_FLUSH_TIMEOUT = 30
DEFAULT_NUM_MSGS = 100000
DEFAULT_MSG_SIZE = 16
DEFAULT_BATCH_SIZE = 100
HASH_MODULO = 1000

def show_usage():
    message = """
Usage: pub_perf [options]

options:
    -n COUNT                         Messages to send (default: 100000}
    -s SIZE                          Message size (default: 16)
    -S SUBJECT                       Send subject (default: (test)
    -b BATCH                         Batch size (default: (100)
    """
    print(message)

def show_usage_and_die():
    show_usage()
    sys.exit(1)

@asyncio.coroutine
def main(loop):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--count', default=DEFAULT_NUM_MSGS, type=int)
    parser.add_argument('-s', '--size', default=DEFAULT_MSG_SIZE, type=int)
    parser.add_argument('-S', '--subject', default='test')
    parser.add_argument('-b', '--batch', default=DEFAULT_BATCH_SIZE, type=int)
    parser.add_argument('--servers', default=[], action='append')
    args = parser.parse_args()

    data = []
    for i in range(0, args.size):
        s = "%01x" % randint(0, 15)
        data.append(s.encode())
    payload = b''.join(data)

    servers = args.servers
    if len(args.servers) < 1:
        servers = ["nats://127.0.0.1:4222"]
    opts = { "servers": servers, "io_loop": loop }

    # Make sure we're connected to a server first..
    nc = NATS()
    try:
        yield from nc.connect(**opts)
    except Exception as e:
        sys.stderr.write("ERROR: {0}".format(e))
        show_usage_and_die()

    # Start the benchmark
    start = time.time()
    to_send = args.count

    print("Sending {0} messages of size {1} bytes on [{2}]".format(
        args.count, args.size, args.subject))
    while to_send > 0:
        for i in range(0, args.batch):
            to_send -= 1
            yield from nc.publish(args.subject, payload)
            if (to_send % HASH_MODULO) == 0:
                sys.stdout.write("#")
                sys.stdout.flush()
            if to_send == 0:
                break

        # Minimal pause in between batches sent to server
        yield from asyncio.sleep(0.00001, loop=loop)

    # Additional roundtrip with server to try to ensure everything has been sent already.
    try:
        yield from nc.flush(DEFAULT_FLUSH_TIMEOUT)
    except ErrTimeout:
        print("Server flush timeout after {0}".format(DEFAULT_FLUSH_TIMEOUT))

    elapsed = time.time() - start
    mbytes = "%.1f" % (((args.size * args.count)/elapsed) / (1024*1024))
    print("\nTest completed : {0} msgs/sec ({1}) MB/sec".format(
        args.count/elapsed,
        mbytes))
    yield from nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
