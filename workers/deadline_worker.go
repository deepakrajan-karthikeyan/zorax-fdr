package main

import (
	"container/heap"
	"fmt"
	"time"
)

type deadline struct {
	id       string
	due      time.Time
	priority int
	index    int
}

type deadlineQueue []*deadline

func (q deadlineQueue) Len() int { return len(q) }
func (q deadlineQueue) Less(i, j int) bool {
	if q[i].priority == q[j].priority {
		return q[i].due.Before(q[j].due)
	}
	return q[i].priority < q[j].priority
}
func (q deadlineQueue) Swap(i, j int) { q[i], q[j] = q[j], q[i]; q[i].index = i; q[j].index = j }
func (q *deadlineQueue) Push(item any) {
	entry := item.(*deadline)
	entry.index = len(*q)
	*q = append(*q, entry)
}
func (q *deadlineQueue) Pop() any {
	old := *q
	last := len(old) - 1
	entry := old[last]
	*q = old[:last]
	return entry
}

func main() {
	queue := &deadlineQueue{
		{ id: "ZRX-FDR-2025-0018", due: time.Now().AddDate(0, 0, 14), priority: 1 },
		{ id: "ZRX-FDR-2025-0012", due: time.Now().AddDate(0, 1, 7), priority: 2 },
	}
	heap.Init(queue)
	for queue.Len() > 0 {
		item := heap.Pop(queue).(*deadline)
		fmt.Printf("P%d %s due %s\n", item.priority, item.id, item.due.Format("2006-01-02"))
	}
}
