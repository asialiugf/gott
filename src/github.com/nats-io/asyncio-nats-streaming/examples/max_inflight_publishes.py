# Copyright 2017 Apcera Inc. All rights reserved.

import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

import time

async def run(loop):
    nc = NATS()
    sc = STAN()
    await nc.connect(io_loop=loop)
    await sc.connect("test-cluster", "client-123", max_pub_acks_inflight=512, nats=nc)

    acks = []
    msgs = []
    async def cb(msg):
        nonlocal sc
        print("Received a message on subscription (seq: {} | recv: {}): {}".format(msg.sequence, len(msgs), msg.data))
        msgs.append(msg)
        await sc.ack(msg)

    # Use manual acking and have message redelivery be done
    # if we do not ack back in 1 second.
    await sc.subscribe("foo", start_at='first', cb=cb, manual_acks=True, ack_wait=1)

    async def ack_handler(ack):
        nonlocal acks
        acks.append(ack)
        print("Received ack: {} | recv: {}".format(ack.guid, len(acks)))

    for i in range(0, 2048):
        before = time.time()
        await sc.publish("foo", b'hello-world', ack_handler=ack_handler)
        after = time.time()
        lag = after-before

        # Async publishing will have backpressured applied if too many
        # published commands are inflight without an ack still.
        if lag > 0.001:
            print("lag at {} : {}".format(lag, i))

    for i in range(0, 5):
        await asyncio.sleep(1, loop=loop)

    await sc.close()
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
