package main

import (
	"strconv"
	"testing"
)

func Test_OrderDict_1(t *testing.T) {
	d := OrderDict{make(map[string]int), []string{}}

	d.add("a", 1)

	value, ok := d.get("a")

	if value != 1 || !ok {
		t.Errorf("OrderDict -> (%v, %v); need '(%v, %v)'", value, ok, 1, true)
	}
}

func Test_OrderDict_2(t *testing.T) {
	d := OrderDict{make(map[string]int), []string{}}

	d.add("a", 1)

	d.del("a")

	value, ok := d.get("a")
	_ = value

	if ok {
		t.Errorf("OrderDict -> %v; need %v", ok, false)
	}

	len := d.len()
	if len != 0 {
		t.Errorf("OrderDict.len() -> %v; need 0", len)
	}
}

func Test_OrderDict_3(t *testing.T) {
	d := OrderDict{make(map[string]int), []string{}}

	d.add("a", 1)
	d.add("b", 2)
	d.add("c", 3)

	d.del("b")

	value, ok := d.get("b")
	_ = value

	if ok {
		t.Errorf("OrderDict -> %v; need %v", ok, false)
	}

	len := d.len()
	if len != 2 {
		t.Errorf("OrderDict.len() -> %v; need 2", len)
	}

	expected_keys := []string{"a", "c"}

	i := 0
	for _, key := range d.keys {
		if key != d.keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, d.keys[i])
		}
		if key != expected_keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, expected_keys[i])
		}

		i += 1
	}

}

func Test_OrderDict_4(t *testing.T) {
	d := OrderDict{make(map[string]int), []string{}}

	d.add("a", 1)
	d.add("b", 2)
	d.add("c", 3)

	d.del("c")

	value, ok := d.get("c")
	_ = value

	if ok {
		t.Errorf("OrderDict -> %v; need %v", ok, false)
	}

	len := d.len()
	if len != 2 {
		t.Errorf("OrderDict.len() -> %v; need 2", len)
	}

	expected_keys := []string{"a", "b"}

	i := 0
	for _, key := range d.keys {
		if key != d.keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, d.keys[i])
		}
		if key != expected_keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, expected_keys[i])
		}

		i += 1
	}

}

func Test_OrderDict_5(t *testing.T) {
	d := OrderDict{make(map[string]int), []string{}}

	d.add("a", 1)
	d.add("b", 2)
	d.add("c", 3)

	d.del("a")

	value, ok := d.get("a")
	_ = value

	if ok {
		t.Errorf("OrderDict -> %v; need %v", ok, false)
	}

	len := d.len()
	if len != 2 {
		t.Errorf("OrderDict.len() -> %v; need 2", len)
	}

	expected_keys := []string{"b", "c"}

	i := 0
	for _, key := range d.keys {
		if key != d.keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, d.keys[i])
		}
		if key != expected_keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, expected_keys[i])
		}

		i += 1
	}

}

func Test_OrderDict_6(t *testing.T) {

	insert_keys := []string{"1", "2", "3", "4", "5", "6", "7"}
	delete_keys := []string{"2", "4", "6"}
	expect_keys := []string{"1", "3", "5", "7"}
	_ = delete_keys

	// create order dict
	d := OrderDict{make(map[string]int), []string{}}
	value := 1
	for _, key := range insert_keys {
		d.add(key, value)
		value += 1
	}

	// check length
	length := d.len()
	if length != 7 {
		t.Errorf("OrderDict.len() -> %v; need 7", length)
	}

	// check key, value
	for _, key := range d.keys {
		value := d.dict[key]
		int_key, _ := strconv.Atoi(key)
		if value != int_key {
			t.Errorf("OrderDict -> (%v, %v); need (%v, %v)", key, value, key, int_key)
		}
	}

	// delete keys
	for _, key := range delete_keys {
		d.del(key)
	}

	// check len
	length = d.len()
	expected_len := len(insert_keys) - len(delete_keys)
	if length != expected_len {
		t.Errorf("OrderDict.len() -> %v; need %v", length, expected_len)
	}

	// check if delete values are there
	for _, key := range delete_keys {
		_, ok := d.get(key)
		if ok {
			t.Errorf("OrderDict -> key %v should not be here", key)
		}
	}

	// check order
	i := 0
	for _, key := range d.keys {
		if key != d.keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, d.keys[i])
		}
		if key != expect_keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, expect_keys[i])
		}

		i += 1
	}

}

func Test_OrderDict_7(t *testing.T) {

	insert_keys := []string{"1", "2", "3", "4", "5", "6", "7"}
	delete_keys := []string{"1", "3", "5", "7"}
	expect_keys := []string{"2", "4", "6"}
	// _ = delete_keys

	// create order dict
	d := OrderDict{make(map[string]int), []string{}}
	value := 1
	for _, key := range insert_keys {
		d.add(key, value)
		value += 1
	}

	// check length
	length := d.len()
	if length != 7 {
		t.Errorf("OrderDict.len() -> %v; need 7", length)
	}

	// check key, value
	for _, key := range d.keys {
		value := d.dict[key]
		int_key, _ := strconv.Atoi(key)
		if value != int_key {
			t.Errorf("OrderDict -> (%v, %v); need (%v, %v)", key, value, key, int_key)
		}
	}

	// delete keys
	for _, key := range delete_keys {
		d.del(key)
	}

	// check len
	length = d.len()
	expected_len := len(insert_keys) - len(delete_keys)
	if length != expected_len {
		t.Errorf("OrderDict.len() -> %v; need %v", length, expected_len)
	}

	// check if delete values are there
	for _, key := range delete_keys {
		_, ok := d.get(key)
		if ok {
			t.Errorf("OrderDict -> key %v should not be here", key)
		}
	}

	// check order
	i := 0
	for _, key := range d.keys {
		if key != d.keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, d.keys[i])
		}
		if key != expect_keys[i] {
			t.Errorf("OrderDict -> key %v = %v; need %v", i, key, expect_keys[i])
		}

		i += 1
	}

}
