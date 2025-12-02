package main

import (
	"bufio"
	"errors"
	"fmt"
	"iter"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	lo uint64
	hi uint64
}

func CSVs(filename string) iter.Seq2[string, error] {
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
			if err != nil {
				yield("", err)
				return
			}

			values := strings.Split(text, ",")
			for _, v := range values {
				if !yield(v, err) {
					return
				}
			}
		}
	}
}

// Ranges takes an iterator over plain, unparsed ranges, and parses them.
func Ranges(src iter.Seq2[string, error]) iter.Seq2[Range, error] {
	return func(yield func(Range, error) bool) {
		for str, err := range src {
			var r Range
			if err != nil {
				yield(r, err)
				return
			}

			parts := strings.Split(str, "-")

			if len(parts) != 2 {
				yield(r, errors.New("too many parts"))
				return
			}

			rawLo, rawHi := parts[0], parts[1]

			lo, err := strconv.Atoi(rawLo)
			if err != nil {
				yield(r, err)
				return
			}

			hi, err := strconv.Atoi(rawHi)
			if err != nil {
				yield(r, err)
				return
			}

			r.lo = uint64(lo)
			r.hi = uint64(hi)
			if !yield(r, nil) {
				return
			}
		}
	}
}

func test(i uint64) bool {
	s := strconv.Itoa(int(i))

windowLoop:
	for j := 1; j < len(s); j++ {
		if len(s)%j != 0 {
			continue windowLoop
		}
		if len(s)/j < 2 {
			continue windowLoop
		}
		for k := 0; k < len(s); k++ {
			if s[k] != s[k%j] {
				continue windowLoop
			}
		}

		// a window was successful
		return true
	}

	return false
}

func main() {
	var sumPtOne uint64
	var sumPtTwo uint64
	for r, err := range Ranges(CSVs("input")) {
		if err != nil {
			panic(err)
		}

		/*	out:
			for i := r.lo; i < r.hi; i++ {
				s := strconv.Itoa(int(i))
				if len(s)%2 != 0 {
					continue
				}

				middle := len(s) / 2
				for j := 0; j < middle; j++ {
					if s[j] != s[j+middle] {
						continue out
					}
				}
				sumPtOne += i
			}*/

		for i := r.lo; i <= r.hi; i++ {

			if test(i) {
				fmt.Println(i)
				sumPtTwo += i
			}

		}
	}

	fmt.Println(sumPtOne, sumPtTwo)
}
