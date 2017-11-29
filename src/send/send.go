package main

import (
	"echo"
	"flag"
	_ "fmt"
	"github.com/nats-io/go-nats"
	"log"
	"runtime"
	"time"
)

func main() {
	runtime.GOMAXPROCS(16)
	dispatcher := NewDispatcher()
	stt := new(Response)
	listener_tick := NewListener("tick", 1, stt.OnTick) // new() 出来的，是一个指针
	listener_bar := NewListener("bar", 2, stt.OnBar)

	dispatcher.AddListener(listener_tick)
	dispatcher.AddListener(listener_bar)

	ev := NewEvent("bar", 2, 0)
	ev.Type = listener_tick.ID
	ev.Buff = 3
	dispatcher.DispatchEvent(ev)
	ev.Type = listener_bar.ID
	ev.Buff = 4
	dispatcher.DispatchEvent(ev)

	//-------------------- for pubsub connect to nats server --------------------------
	var urls = flag.String("s", nats.DefaultURL, "The nats server URLs (separated by comma)")
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

	//nc := nats_conn()
	go echo.Nats_sub("abc", nc)
	time.Sleep(1000000)
	go echo.Nats_pub("abc", nc)
	//-------------------- for pubsub connect to nats server end --------------------------
	for {
	}
}
