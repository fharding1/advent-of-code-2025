package main

import (
	"bufio"
	"errors"
	"fmt"
	"iter"
	"os"
	"strconv"
)

type Direction bool

const (
	Left  Direction = false
	Right Direction = true
)

type Instruction struct {
	dir    Direction
	amount uint64
}

// Lines reads a file line by line and yields each line and any potential errors. A caller must read until
func Lines(filename string) iter.Seq2[string, error] {
	return func(yield func(string, error) bool) {
		f, err := os.Open(filename)
		if err != nil {
			yield("", err)
			return
		}
		defer f.Close()

		scanner := bufio.NewScanner(f)
		for scanner.Scan() {
			text := scanner.Text()
			err := scanner.Err()
			if !yield(text, err) {
				return
			}
			if err != nil {
				return
			}
		}
	}
}

// Directions takes an iterator over plain, unparsed instructions, and parses them.
func Directions(src iter.Seq2[string, error]) iter.Seq2[Instruction, error] {
	return func(yield func(Instruction, error) bool) {
		for line, err := range src {
			var instr Instruction
			if err != nil {
				yield(instr, err)
				return
			}

			if len(line) < 2 {
				yield(instr, errors.New("too short"))
				return
			}

			rawDir := line[0]
			rest, err := strconv.Atoi(line[1:])
			if err != nil {
				yield(instr, err)
			}

			if rawDir == 'R' {
				instr.dir = Right
			}
			instr.amount = uint64(rest)
			yield(instr, nil)
		}
	}
}

func main() {
	var dial int64 = 50
	var count uint

	for dir, err := range Directions(Lines("input")) {
		if err != nil {
			panic(err)
		}
		sign := -1
		if dir.dir == Right {
			sign = 1
		}
		val := sign * int(dir.amount)
		dial = (dial + int64(val)) % 100
		if dial == 0 {
			count++
		}
	}

	fmt.Println(count)
}
