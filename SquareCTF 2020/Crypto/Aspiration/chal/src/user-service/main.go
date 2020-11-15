package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"path"

	"github.com/spiffe/go-spiffe/v2/spiffeid"
	"github.com/spiffe/go-spiffe/v2/spiffetls/tlsconfig"
	"github.com/spiffe/go-spiffe/v2/workloadapi"
)

const (
	port       = 8090
	socketPath = "unix:///tmp/agent.sock"

	showBundleUrl = "http://spire-server:8082/show"
	addBundleUrl  = "http://spire-server:8082/add"
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

	trustDomain, err := spiffeid.TrustDomainFromString("square.ctf.chal")
	if err != nil {
		log.Fatal(err)
	}

	server := &http.Server{
		Addr:      fmt.Sprintf(":%d", port),
		TLSConfig: tlsconfig.MTLSServerConfig(x509Src, bundleSrc, tlsconfig.AuthorizeMemberOf(trustDomain)),
	}
	http.HandleFunc("/status", statusHandler)
	http.HandleFunc("/show_bundle", showBundleHandler)
	http.HandleFunc("/add_bundle", addBundleHandler)

	log.Printf("user service listening on port %d...", port)

	err = server.ListenAndServeTLS("", "")
	if err != nil {
		log.Fatal(err)
	}
}

func adminMatcher(id spiffeid.ID) error {
	if path.Base(id.Path()) != "admin" {
		return fmt.Errorf("not an admin")
	}
	return nil
}

func statusHandler(resp http.ResponseWriter, req *http.Request) {
	user := path.Base(req.TLS.PeerCertificates[0].URIs[0].Path)

	if _, err := fmt.Fprintf(resp, "hello %s, you're registered", user); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func showBundleHandler(resp http.ResponseWriter, req *http.Request) {
	svid, err := spiffeid.FromURI(req.TLS.PeerCertificates[0].URIs[0])
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	if adminMatcher(svid) != nil {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}

	response, err := http.Post(showBundleUrl, "application/json", nil)
	if err != nil || response.StatusCode != http.StatusOK {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	data, err := ioutil.ReadAll(response.Body)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	if _, err := resp.Write(data); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func addBundleHandler(resp http.ResponseWriter, req *http.Request) {
	svid, err := spiffeid.FromURI(req.TLS.PeerCertificates[0].URIs[0])
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	if adminMatcher(svid) != nil {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}

	response, err := http.Post(addBundleUrl, "application/json", req.Body)
	if err != nil || response.StatusCode != http.StatusOK {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}
