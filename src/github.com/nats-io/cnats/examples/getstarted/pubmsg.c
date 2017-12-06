// Copyright 2017 Apcera Inc. All rights reserved.

#include <nats.h>

int main(int argc, char **argv)
{
    natsConnection      *conn = NULL;
	natsSubscription    *sub  = NULL;
    natsMsg             *msg  = NULL;
    natsMsg             *msg1  = NULL;
    natsStatus          s;

    const char* xxx = "Hello world!999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999";

    printf("Publishes a message on subject 'foo'\n");

    // Creates a connection to the default NATS URL
    s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);
    if (s == NATS_OK)
    {
        const char data[] = {104, 101, 108, 108, 111, 33};

        // Creates a message for subject "foo", no reply, and
        // with the given payload.
        s = natsMsg_Create(&msg, "foo", NULL, data, sizeof(data));
        s = natsMsg_Create(&msg, "foo", NULL, xxx, sizeof(xxx));
    }

    if (s == NATS_OK)
    {
        s = natsSubscription_NextMsg(&msg1, sub, 5000);
		printf("1111111111");
    }


    if (s == NATS_OK)
    {
        s = natsConnection_PublishMsg(conn, msg);
		printf("222222222222");
    }

    if (s == NATS_OK)
    {
        s = natsSubscription_NextMsg(&msg1, sub, 5000);
		printf("33333333333");
    }
    if (s == NATS_OK)
    {
        printf("Received msg: %s - %.*s\n",
               natsMsg_GetSubject(msg1),
               natsMsg_GetDataLength(msg1),
               natsMsg_GetData(msg1));
        natsMsg_Destroy(msg1);
    }






    // Anything that is created need to be destroyed
    natsMsg_Destroy(msg);
    natsMsg_Destroy(msg1);
    natsConnection_Destroy(conn);

    // If there was an error, print a stack trace and exit
    if (s != NATS_OK)
    {
        nats_PrintLastErrorStack(stderr);
        exit(2);
    }

    return 0;
}




