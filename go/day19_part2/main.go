package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Part map[string]*[2]int

func (p Part) clone() Part {
	np := make(Part)
	for k, v := range p {
		np[k] = &[2]int{v[0], v[1]}
	}
	return np
}

type DequeKey struct {
	wf   string
	part Part
}

type Deque []*DequeKey

func (q *Deque) append(dk *DequeKey) {
	(*q) = append((*q), dk)
}

func (q Deque) isEmpty() bool {
	return len(q) == 0
}

func (q *Deque) popleft() (string, Part) {
	item := (*q)[0]
	(*q) = (*q)[1:]
	return item.wf, item.part
}

type Rule struct {
	attr     string
	comp     string
	value    int
	workflow string
}

type Workflow struct {
	rules []Rule
	final string
}

func (r Rule) values() (string, string, int, string) {
	return r.attr, r.comp, r.value, r.workflow
}

func solution(filename string) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	blocks := strings.Split(content, "\n\n")

	workflows_str := strings.Split(blocks[0], "\n")
	workflows := make(map[string]*Workflow)

	wf_regex := regexp.MustCompile(`(\w+){(.*)}`)
	rule_regex := regexp.MustCompile(`(\w)([><])(\d+):(\w+)`)

	// parse rules
	for _, line := range workflows_str {
		matches := wf_regex.FindStringSubmatch(line)

		name := matches[1]
		rules := strings.Split(matches[2], ",")
		workflows[name] = &Workflow{[]Rule{}, ""}

		for _, rule := range rules {
			match := rule_regex.FindStringSubmatch(rule)
			if len(match) > 0 {
				attr := match[1]
				comp := match[2]
				value, _ := strconv.Atoi(match[3])
				workflow := match[4]

				workflows[name].rules = append(workflows[name].rules, Rule{attr, comp, value, workflow})
			} else {
				workflows[name].final = rule
			}
		}
	}

	var initial_part = Part{
		"x": {1, 4000},
		"m": {1, 4000},
		"a": {1, 4000},
		"s": {1, 4000},
	}
	queue := Deque{&DequeKey{"in", initial_part}}
	accepted_parts := []Part{}

	// apply rules in a BFS-style
	for !queue.isEmpty() {
		wf, part := queue.popleft()

		if wf == "R" {
			continue
		}
		if wf == "A" {
			accepted_parts = append(accepted_parts, part)
			continue
		}

		for _, rule := range workflows[wf].rules {
			attr, comp, value, workflow := rule.values()

			if comp == "<" {
				new_part := part.clone()
				new_part[attr][1] = min(new_part[attr][1], value-1)
				if part[attr][0] <= part[attr][1] {
					queue.append(&DequeKey{workflow, new_part})
				}
				part[attr][0] = max(part[attr][0], value)
			} else if comp == ">" {
				new_part := part.clone()
				new_part[attr][0] = max(new_part[attr][0], value+1)
				if part[attr][0] <= part[attr][1] {
					queue.append(&DequeKey{workflow, new_part})
				}
				part[attr][1] = min(part[attr][1], value)
			} else {
				fmt.Println("WTF!")
			}
		}
		ranges_in_order := true
		for _, value := range part {
			lower, upper := value[0], value[1]
			if lower > upper {
				ranges_in_order = false
				break
			}
		}
		if ranges_in_order {
			queue = append(queue, &DequeKey{workflows[wf].final, part.clone()})
		}
	}

	// calculate sum of attributes
	total_sum := 0
	for _, part := range accepted_parts {
		total := 1
		for _, value := range part {
			lower, upper := value[0], value[1]
			if upper >= lower {
				total *= upper - lower + 1
			}
		}
		total_sum += total
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 167409079868000
	fmt.Println(solution("./input.txt"))   // 133973513090020
}
