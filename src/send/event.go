package main

type Event struct {
	Name   string
	ID     int
	Type   int // Must be Listener's ID
	Series uint64
	Buff   int
}

/*
 E.Type should be the Listener's ID
*/
func NewEvent(name string, id int, etype int) *Event {
	E := new(Event)
	E.Name = name
	E.ID = id
	E.Type = etype
	E.Series = 0
	return E
}
