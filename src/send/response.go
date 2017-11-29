package main

import "fmt"

type Response struct {
}

func (s *Response) Init() {
}

func (s *Response) OnTick(buff int) {
	fmt.Println("----------------OnTick:", buff)
}
func (s *Response) OnBar(buff int) {
	fmt.Println("----------------OnBar", buff)
}
