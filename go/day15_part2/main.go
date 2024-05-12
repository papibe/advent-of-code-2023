package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type OrderDict struct {
	dict map[string]int
	keys []string
}

func (d *OrderDict) add(label string, lens int) {
	_, is_in_dict_already := (*d).dict[label]
	if !is_in_dict_already {
		(*d).keys = append((*d).keys, label)
	}
	(*d).dict[label] = lens
}

func (d *OrderDict) del(label string) {
	_, is_in_dict_already := (*d).dict[label]
	if !is_in_dict_already {
		return
	}

	label_index := -1
	for index, klabel := range (*d).keys {
		if klabel == label {
			label_index = index
			break
		}
	}
	(*d).keys = append((*d).keys[:label_index], (*d).keys[label_index+1:]...)
	delete((*d).dict, label)
}

func (d OrderDict) get(label string) (int, bool) {
	value, ok := d.dict[label]
	return value, ok
}

func (d OrderDict) len() int {
	return len(d.dict)
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")
	line := lines[0]

	box := []OrderDict{}
	for i := 0; i < 256; i++ {
		box = append(box, OrderDict{make(map[string]int), []string{}})
	}

	for _, seq := range strings.Split(line, ",") {
		value := 0
		if seq[len(seq)-1] == '-' {
			label := seq[:len(seq)-1]
			for _, char := range label {
				value += int(char)
				value *= 17
				value %= 256
			}
			_, is_in_label := box[value].get(label)
			if is_in_label {
				box[value].del(label)
			}

		} else {
			lens, _ := strconv.Atoi(string(seq[len(seq)-1]))
			label := seq[:len(seq)-2]
			for _, char := range label {
				value += int(char)
				value *= 17
				value %= 256
			}
			box[value].add(label, lens)
		}

	}

	total := 0
	for index, dict := range box {
		if dict.len() > 0 {
			slot := 1
			for _, label := range dict.keys {
				lens := dict.dict[label]
				total += (index + 1) * slot * lens
				slot += 1
			}
		}
	}

	return total
}

func main() {
	fmt.Println(solution("./example.txt")) // 145
	fmt.Println(solution("./input.txt"))   // 244981
}
