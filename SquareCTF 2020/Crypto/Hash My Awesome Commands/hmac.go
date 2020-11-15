package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"time"

	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
)

var commands = []string{
	"flag",
	"debug",
}

var debug = false

type HmacVerifier struct {
	codes map[string][]byte
}

func (h *HmacVerifier) verifyHmac(message string, check []byte) bool {
	start := time.Now()
	match := compare(h.codes[message], check)
	verifyTime := time.Since(start).Nanoseconds()

	if debug {
		fmt.Printf("took %d nanoseconds to verify hmac\n", verifyTime)
	}

	return match
}

func newHmacWrapper(key []byte) HmacVerifier {
	codes := map[string][]byte{}

	h := hmac.New(sha256.New, key)
	for _, command := range commands {
		h.Write([]byte(command))
		codes[command] = h.Sum(nil)
		h.Reset()
	}

	return HmacVerifier{codes: codes}
}

func main() {
	key, err := ioutil.ReadFile("data/hmac_key")
	if err != nil {
		fmt.Printf("unable to load key: %v", err)
		return
	}
	hmacWrapper := newHmacWrapper(key)

	reader := bufio.NewReader(os.Stdin)

	for {
		if debug {
			fmt.Println("-----------DEBUG MODE ENABLED-----------")
		}
		fmt.Print("Enter command: ")
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("unable to read input: %v\n", err)
			return
		}

		input = strings.TrimSpace(input)
		components := strings.Split(input, "|")
		if len(components) < 2 {
			fmt.Println("command must contain hmac signature")
			continue
		}

		command := components[0]
		check, err := base64.StdEncoding.DecodeString(components[1])
		if err != nil {
			fmt.Println("hmac must be base64")
			continue
		}

		if debug {
			fmt.Printf("command: %s, check: %s\n", command, components[1])
		}

		if !contains(commands, command) {
			fmt.Println("invalid command")
			continue
		}

		if !hmacWrapper.verifyHmac(command, check) {
			fmt.Println("invalid hmac")
			continue
		}

		switch command {
		case "debug":
			debug = !debug
			if debug {
				fmt.Println("debug mode enabled")
			} else {
				fmt.Println("debug mode disabled")
			}
		case "flag":
			flag, err := ioutil.ReadFile("data/flag")
			if err != nil {
				fmt.Printf("unable to load flag: %v", err)
				return
			}
			fmt.Println(string(flag))
		}
	}
}

func compare(s1, s2 []byte) bool {
	if len(s1) != len(s2) {
		return false
	}

	c := make(chan bool)

	// multi-threaded check to speed up comparison
	for i := 0; i < len(s1); i++ {
		go func(i int, co chan<- bool) {
			// avoid race conditions
			time.Sleep(time.Duration(((500*math.Pow(1.18, float64(i+1)))-500)/0.18) * time.Microsecond)
			co <- s1[i] == s2[i]
		}(i, c)
	}

	for i := 0; i < len(s1); i++ {
		if <-c == false {
			return false
		}
	}

	return true
}

func contains(l []string, s string) bool {
	for _, i := range l {
		if i == s {
			return true
		}
	}
	return false
}
