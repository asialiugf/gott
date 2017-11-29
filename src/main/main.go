package main

import (
	"echo"
	"flag"
	_ "fmt"
	"github.com/nats-io/go-nats"
	"log"
	"runtime"
	"strategy"
	"time"
)

func usage() {
	log.Fatalf("Usage: nats-pub [-s server (%s)] <subject> <msg> \n", nats.DefaultURL)
}

func main() {
	runtime.GOMAXPROCS(16)
	dispatcher := NewDispatcher()
	stt := new(strategy.Strategy)
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

	/*
		可以订阅多级别数据
		比如订阅了 1F 5F 30F的数据
		那么，收到的数据结构如下：

		09:24:00  1F
		09:25:00  1F 5F
		09:26:00  1F
		09:27:00  1F
		09:28:00  1F
		09:29:00  1F
		09:30:00  1F 5F 30F

		即：在09:30:00时，会收到一个消息，里面包含 三个级别的数据。
	*/

	//-------------------- for pubsub connect to nats server --------------------------
	var urls = flag.String("s", nats.DefaultURL, "The nats server URLs (separated by comma)")
	flag.Usage = usage
	flag.Parse()

	args := flag.Args()
	if len(args) < 2 {
		usage()
	}

	msg := []byte(args[1])

	nc, err := nats.Connect(*urls)
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	//nc := nats_conn()
	echo.Nats_sub("abc", nc)
	time.Sleep(1000000)
	go echo.Nats_pub("abc", nc, msg)
	//-------------------- for pubsub connect to nats server end --------------------------
	for {
	}

	//runtime.Goexit() // 这一句有问题
}
