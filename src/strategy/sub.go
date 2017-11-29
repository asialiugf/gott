package strategy

import "fmt"

type Strategy struct {
}

func (s *Strategy) Init() {
}

func (s *Strategy) OnTick(buff int) {
	fmt.Println("----------------OnTick:", buff)
}
func (s *Strategy) OnBar(buff int) {
	fmt.Println("----------------OnBar", buff)
}
