package main

import (
	"context"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"log"
	"net/http"

	"github.com/spiffe/spire/proto/spire/api/server/bundle/v1"
	"github.com/spiffe/spire/proto/spire/types"

	"google.golang.org/grpc"
)

const (
	port       = 8082
	socketPath = "unix:///tmp/spire-registration.sock"
)

type Bundler struct {
	client bundle.BundleClient
}

func NewBundler(ctx context.Context) (*Bundler, error) {
	conn, err := grpc.DialContext(ctx, socketPath, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}

	client := bundle.NewBundleClient(conn)

	return &Bundler{
		client: client,
	}, nil
}

func main() {
	bundler, err := NewBundler(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	server := &http.Server{
		Addr: fmt.Sprintf(":%d", port),
	}

	http.HandleFunc("/show", bundler.showHandler)
	http.HandleFunc("/add", bundler.addHandler)

	log.Printf("bundle server listening on port %d...", port)

	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}

func (r *Bundler) showHandler(resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	request := &bundle.GetBundleRequest{}
	response, err := r.client.GetBundle(req.Context(), request)
	if err != nil {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}
	authority := response.X509Authorities[0]
	certs, err := x509.ParseCertificates(authority.Asn1)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	for _, cert := range certs {
		if err := pem.Encode(resp, &pem.Block{Type: "CERTIFICATE", Bytes: cert.Raw}); err != nil {
			resp.WriteHeader(http.StatusInternalServerError)
			return
		}
	}
}

func (r *Bundler) addHandler(resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	var data map[string]string
	decoder := json.NewDecoder(req.Body)
	if err := decoder.Decode(&data); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	pemData, _ := pem.Decode([]byte(data["bundle"]))
	authority, err := x509.ParseCertificate(pemData.Bytes)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	newBundles := []*types.X509Certificate{
		{Asn1: authority.Raw},
	}

	request := &bundle.AppendBundleRequest{X509Authorities: newBundles}
	if _, err := r.client.AppendBundle(req.Context(), request); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}
