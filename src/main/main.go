package main

import (
	_ "fmt"
	"strategy"
)

func main() {
	dispatcher := NewDispatcher() //不用多说了吧，代码很清楚了
	stt := new(strategy.Strategy)
	// new() 出来的，是一个指针
	listener_tick := NewListener("tick", 1, stt.OnTick)
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
}
