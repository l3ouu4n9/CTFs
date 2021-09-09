package main

import (
	"fmt"
	"github.com/google/uuid"
)

func main() {
	ids := []string{
    	"33085482-e985-11eb-b0ba-5e91c0efb80a",
		"33085484-e985-11eb-b0ba-5e91c0efb80a",
		"33085489-e985-11eb-b0ba-5e91c0efb80a",
		"3308548d-e985-11eb-b0ba-5e91c0efb80a",
		"3308548f-e985-11eb-b0ba-5e91c0efb80a",
		"313e98e5-e985-11eb-b0ba-5e91c0efb80a",
		"313e98e8-e985-11eb-b0ba-5e91c0efb80a",
		"313e98ed-e985-11eb-b0ba-5e91c0efb80a",
		"313e98ef-e985-11eb-b0ba-5e91c0efb80a",
		"313e98f1-e985-11eb-b0ba-5e91c0efb80a",
		"2f74bc34-e985-11eb-b0ba-5e91c0efb80a",
		"2f74bc36-e985-11eb-b0ba-5e91c0efb80a",
		"2f74bc39-e985-11eb-b0ba-5e91c0efb80a",
		"2f74bc3d-e985-11eb-b0ba-5e91c0efb80a",
		"2f74bc3f-e985-11eb-b0ba-5e91c0efb80a",
		"2daafb13-e985-11eb-b0ba-5e91c0efb80a",
		"2daafb15-e985-11eb-b0ba-5e91c0efb80a",
		"2daafb19-e985-11eb-b0ba-5e91c0efb80a",
		"2daafb1e-e985-11eb-b0ba-5e91c0efb80a",
		"2daafb20-e985-11eb-b0ba-5e91c0efb80a",
		"2be13ec4-e985-11eb-b0ba-5e91c0efb80a",
		"2be13eca-e985-11eb-b0ba-5e91c0efb80a",
		"2be13ecc-e985-11eb-b0ba-5e91c0efb80a",
		"2be13ed0-e985-11eb-b0ba-5e91c0efb80a",
		"2be13ed2-e985-11eb-b0ba-5e91c0efb80a",
	}
	var lastsec, lastnsec int64
	for i, id := range ids {
		uid, _ := uuid.Parse(id)
		sec, nsec := uid.Time().UnixTime()
		if i > 1 {
			fmt.Printf("secdiff: %d hundred nsecdiff: %d\n", lastsec-sec, (lastnsec-nsec)/100)
		}
		lastsec = sec
		lastnsec = nsec
	}
}