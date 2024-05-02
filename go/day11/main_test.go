package main

import (
	"testing"
)

func Test_example_with_factor_2_should_be_374(t *testing.T) {
	expected := 374
	result := solution("./example.txt", 2)
	if result != expected {
		t.Errorf("'./example.txt' -> %v; need '%v'", result, expected)
	}
}

func Test_example_with_factor_10_should_be_1030(t *testing.T) {
	expected := 1030
	result := solution("./example.txt", 10)
	if result != expected {
		t.Errorf("'./example.txt' -> %v; need '%v'", result, expected)
	}
}

func Test_example_with_factor_100_should_be_8410(t *testing.T) {
	expected := 8410
	result := solution("./example.txt", 100)
	if result != expected {
		t.Errorf("'./example.txt' -> %v; need '%v'", result, expected)
	}
}
