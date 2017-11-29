package main

import (
	_ "container/list"
	"fmt"
)

type ListenerFunc func(int)
type Listener struct {
	Name  string
	ID    int
	Serve ListenerFunc
}

type Dispatcher struct {
	Listeners map[int]*Listener
}

func NewListener(name string, id int, serve ListenerFunc) *Listener {
	L := new(Listener)
	L.Name = name
	L.ID = id
	L.Serve = serve
	return L
}

func NewDispatcher() *Dispatcher {
	p := new(Dispatcher)
	return p
}
func (this *Dispatcher) AddListener(L *Listener) {
	if this.Listeners == nil {
		this.Listeners = make(map[int]*Listener)
	}
	this.Listeners[L.ID] = L
}

func (this *Dispatcher) DispatchEvent(e *Event) {
	fmt.Println("OnBar", e.Buff)
	this.Listeners[e.Type].Serve(e.Buff)
	fmt.Println("e.Type", e.Type)
	fmt.Println(this.Listeners[e.Type].Name)
	fmt.Println(this.Listeners[e.Type].ID)
}
