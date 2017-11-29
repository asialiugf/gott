// Copyright 2012-2016 Apcera Inc. All rights reserved.

package echo

import (
	_ "flag"
	_ "fmt"
	"github.com/nats-io/go-nats"
	"log"
	"runtime"
	"time"
)

// NOTE: Use tls scheme for TLS, e.g. nats-pub -s tls://demo.nats.io:4443 foo hello

var conn nats.Conn

func printMsg(m *nats.Msg) {
	log.Printf("[#] ----------------   fuck!! -----------  Received on [%s]: '%s'\n", m.Subject, string(m.Data))
}

/*
func nats_conn() *nats.Conn {
	nc := new(nats.Conn)
	//nc := new(nats.Conn)
	runtime.GOMAXPROCS(2)
	var urls = flag.String("s", nats.DefaultURL, "The nats server URLs (separated by comma)")

	//log.SetFlags(0)
	flag.Usage = usage
	flag.Parse()

	args := flag.Args()
	if len(args) < 2 {
		usage()
	}

	nc, err := nats.Connect(*urls)
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()
	return nc
}
*/

func Nats_pub(subj string, nc *nats.Conn, buff []byte) {
	log.Printf("---------------   Nats_pub!! -----------  ")

	go nc.Publish(subj, buff)
	go nc.Flush()
	go nc.Publish("kkk", buff)
	go nc.Flush()

	x := runtime.NumGoroutine()
	log.Printf("runtime.NumGoroutine(): '%d'\n", x)

	if err := nc.LastError(); err != nil {
		log.Fatal(err)
	} else {
		log.Printf("Published [%s] : '%s'\n", subj, buff)
	}

	time.Sleep(10000000000000)
	log.Printf("---- after time.Sleep()")
}

func mywork(msg *nats.Msg) {
	printMsg(msg)
}

func Nats_sub(subj string, nc *nats.Conn) {

	nc.Subscribe(subj, mywork)
	nc.Flush()

	if err := nc.LastError(); err != nil {
		log.Fatal(err)
	}

	log.Printf("Listening on [%s]\n", subj)

	//runtime.Goexit()
}
