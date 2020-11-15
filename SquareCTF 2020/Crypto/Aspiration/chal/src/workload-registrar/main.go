package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/spiffe/go-spiffe/v2/spiffeid"
	"github.com/spiffe/spire/proto/spire/api/registration"
	"github.com/spiffe/spire/proto/spire/common"

	"google.golang.org/grpc"
)

const (
	port       = 8080
	socketPath = "unix:///tmp/spire-registration.sock"
)

type Registrar struct {
	client registration.RegistrationClient
}

func NewRegistrar(ctx context.Context) (*Registrar, error) {
	conn, err := grpc.DialContext(ctx, socketPath, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}

	client := registration.NewRegistrationClient(conn)

	return &Registrar{
		client: client,
	}, nil
}

func main() {
	registrar, err := NewRegistrar(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	server := &http.Server{
		Addr: fmt.Sprintf(":%d", port),
	}
	http.HandleFunc("/register", registrar.registerHandler)

	log.Printf("workload registrar listening on port %d...", port)

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}

func (r *Registrar) registerHandler(resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	var data map[string]string
	decoder := json.NewDecoder(req.Body)
	if err := decoder.Decode(&data); err != nil {
		resp.WriteHeader(http.StatusBadRequest)
		return
	}
	if sess, ok := data["session"]; !ok || sess == "" {
		resp.WriteHeader(http.StatusBadRequest)
		return
	}
	if user, ok := data["user"]; !ok || user == "" {
		resp.WriteHeader(http.StatusBadRequest)
		return
	}

	svid := spiffeid.Must("square.ctf.chal", data["session"], data["user"])
	entry := &common.RegistrationEntry{
		ParentId: "spiffe://square.ctf.chal/spire/agent/x509pop/92f92fbbce08117db276ca7d3cf0dd683ff55df5",
		SpiffeId: svid.String(),
		Selectors: []*common.Selector{
			{
				Type:  "unix",
				Value: "user:root",
			},
		},
	}

	if _, err := r.client.CreateEntry(req.Context(), entry); err != nil {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}
}
