# Copyright 2017 Apcera Inc. All rights reserved.

import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

async def run(loop):
    # Use borrowed connection for NATS then mount NATS Streaming
    # client on top.
    nc = NATS()
    await nc.connect(io_loop=loop)

    # Start session with NATS Streaming cluster.
    sc = STAN()
    await sc.connect("test-cluster", "client-123", nats=nc)

    # Synchronous Publisher, does not return until an ack
    # has been received from NATS Streaming.
    for i in range(0, 10):
        await sc.publish("foo", 'hello-{}'.format(i).encode())

    msgs = []
    future = asyncio.Future(loop=loop)
    def cb(msg):
        nonlocal msgs
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))
        msgs.append(msg)
        if len(msgs) >= 10:
            future.set_result(True)

    # Subscribe to get all messages since beginning.
    await sc.subscribe("foo", start_at='last_received', cb=cb)

    # Receive all stored values in order
    await sc.subscribe("foo", deliver_all_available=True, cb=cb)

    # Receive messages starting at a specific sequence number
    await sc.subscribe("foo", start_at="sequence", sequence=3, cb=cb)

    # Close NATS Streaming session
    await sc.close()

    # We are using a NATS borrowed connection so we need to close manually.
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
