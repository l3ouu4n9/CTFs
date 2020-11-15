package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/spiffe/go-spiffe/v2/spiffeid"
	"github.com/spiffe/go-spiffe/v2/spiffetls/tlsconfig"
	"github.com/spiffe/go-spiffe/v2/workloadapi"
)

const (
	port       = 8090
	socketPath = "unix:///tmp/agent.sock"
)

var (
	flagSpiffeID = spiffeid.Must("square.ctf.chal", "flag")
)

func main() {
	ctx := context.Background()
	x509Src, err := workloadapi.NewX509Source(ctx,
		workloadapi.WithClientOptions(
			workloadapi.WithAddr(socketPath),
		),
	)
	if err != nil {
		log.Fatal(err)
	}

	bundleSrc, err := workloadapi.NewBundleSource(ctx,
		workloadapi.WithClientOptions(
			workloadapi.WithAddr(socketPath),
		),
	)
	if err != nil {
		log.Fatal(err)
	}

	server := &http.Server{
		Addr:      fmt.Sprintf(":%d", port),
		TLSConfig: tlsconfig.MTLSServerConfig(x509Src, bundleSrc, tlsconfig.AuthorizeID(flagSpiffeID)),
	}
	http.HandleFunc("/flag", flagHandler)

	log.Printf("flag service listening on port %d...", port)

	err = server.ListenAndServeTLS("", "")
	if err != nil {
		log.Fatal(err)
	}
}

func flagHandler(resp http.ResponseWriter, req *http.Request) {
	_, err := fmt.Fprint(resp, "flag{-------------------}")
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}
