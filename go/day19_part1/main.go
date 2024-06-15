package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

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
	parts_str := strings.Split(blocks[1], "\n")

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

	parts := make(map[int]map[string]int)
	prop_regex := regexp.MustCompile(`(\w)=(\d+)`)

	// parse parts
	for part_number, line := range parts_str {
		attributes := strings.Split(line[1:len(line)-1], ",")
		parts[part_number] = make(map[string]int)

		for _, attribute := range attributes {
			matches := prop_regex.FindStringSubmatch(attribute)

			attr := matches[1]
			value, _ := strconv.Atoi(matches[2])
			parts[part_number][attr] = value
		}
	}

	accepted_parts := []int{}

	// apply rules to all parts
	for part_number, part := range parts {
		wf := "in"

		for {
			if wf == "R" {
				break
			}
			if wf == "A" {
				accepted_parts = append(accepted_parts, part_number)
				break
			}

			did_break := false
			for _, rule := range workflows[wf].rules {
				attr, comp, value, _ := rule.values()

				if comp == "<" {
					if part[attr] < value {
						wf = rule.workflow
						did_break = true
						break
					}
				} else {
					if part[attr] > value {
						wf = rule.workflow
						did_break = true
						break
					}
				}
			}
			if !did_break {
				wf = workflows[wf].final
			}
		}
	}

	// calculate sum of attributes
	total_sum := 0
	for _, part_number := range accepted_parts {
		for _, v := range parts[part_number] {
			total_sum += v
		}
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 19114
	fmt.Println(solution("./input.txt"))   // 398527
}
