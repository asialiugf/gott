// Copyright 2012-2016 Apcera Inc. All rights reserved.

package main

import (
	"flag"
	_ "fmt"
	"github.com/nats-io/go-nats"
	"log"
	"runtime"
	"time"
)

// NOTE: Use tls scheme for TLS, e.g. nats-pub -s tls://demo.nats.io:4443 foo hello

var conn nats.Conn

func printMsg(m *nats.Msg, i int) {
	log.Printf("[#%d] ----------------   fuck!! -----------  Received on [%s]: '%s'\n", i, m.Subject, string(m.Data))
}

func usage() {
	log.Fatalf("Usage: nats-pub [-s server (%s)] <subject> <msg> \n", nats.DefaultURL)
}

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

func nats_pub(subj string, nc *nats.Conn) {
	log.Printf("---------------   fuck!! -----------  ")

	flag.Usage = usage
	flag.Parse()

	args := flag.Args()
	if len(args) < 2 {
		usage()
	}

	msg := []byte(args[1])

	go nc.Publish(subj, msg)
	go nc.Flush()
	go nc.Publish("kkk", msg)
	go nc.Flush()

	x := runtime.NumGoroutine()
	log.Printf("runtime.NumGoroutine(): '%d'\n", x)

	if err := nc.LastError(); err != nil {
		log.Fatal(err)
	} else {
		log.Printf("Published [%s] : '%s'\n", subj, msg)
	}

	time.Sleep(10000000000000)
	log.Printf("---- after time.Sleep()")
}

func nats_sub(subj string, nc *nats.Conn) string {

	i := 0
	nc.Subscribe(subj, func(msg *nats.Msg) {
		i += 1
		printMsg(msg, i)
	})
	nc.Flush()

	if err := nc.LastError(); err != nil {
		log.Fatal(err)
	}

	log.Printf("Listening on [%s]\n", subj)

	return string(msg.Data)

	//runtime.Goexit()
}
