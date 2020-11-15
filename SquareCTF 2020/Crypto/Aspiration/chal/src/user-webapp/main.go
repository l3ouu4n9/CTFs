package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"path"
	"strings"

	"github.com/google/uuid"
	"github.com/gorilla/sessions"
	"github.com/spiffe/go-spiffe/v2/spiffeid"
	"github.com/spiffe/go-spiffe/v2/spiffetls/tlsconfig"
	"github.com/spiffe/go-spiffe/v2/svid/x509svid"
	"github.com/spiffe/go-spiffe/v2/workloadapi"
)

const (
	port          = 8080
	statusUrl     = "https://user-service:8090/status"
	registerUrl   = "http://spire-server:8080/register"
	showBundleUrl = "https://user-service:8090/show_bundle"
	addBundleUrl  = "https://user-service:8090/add_bundle"
	socketPath    = "unix:///tmp/agent.sock"
	homePage      = "index.html"
)

var (
	flagProviderSpiffeID = spiffeid.Must("square.ctf.chal", "flagService")
	userProviderSpiffeID = spiffeid.Must("square.ctf.chal", "userService")

	key   = []byte("super-secret-key")
	store = sessions.NewCookieStore(key)
)

func main() {
	server := &http.Server{
		Addr: fmt.Sprintf(":%d", port),
	}
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/status", statusHandler)
	http.HandleFunc("/register", registerHandler)

	http.HandleFunc("/admin/bundle/show", showBundleHandler)
	http.HandleFunc("/admin/bundle/add", addBundleHandler)

	log.Printf("Webapp listening on port %d...", port)

	err := server.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}

func homeHandler(resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodGet {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadFile(homePage)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	if _, err := fmt.Fprint(resp, string(body)); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func genericUserHandler(url string, resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	x509Src, bundleSrc, err := getCertData(req)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	data, err := getUserData(url, x509Src, bundleSrc)
	if err != nil {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}

	if _, err := fmt.Fprint(resp, string(data)); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func getUserData(url string, x509Src x509svid.Source, bundleSrc *workloadapi.BundleSource) ([]byte, error) {
	client := http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsconfig.MTLSClientConfig(x509Src, bundleSrc, tlsconfig.AuthorizeID(userProviderSpiffeID)),
		},
	}

	resp, err := client.Get(url)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		return nil, err
	}

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return data, nil
}

func getCertData(req *http.Request) (x509svid.Source, *workloadapi.BundleSource, error) {
	session, _ := store.Get(req, "session")
	if _, ok := session.Values["identifier"]; !ok {
		return nil, nil, fmt.Errorf("no identifier set")
	}

	x509Src, err := workloadapi.NewX509Source(req.Context(),
		workloadapi.WithDefaultX509SVIDPicker(func(svids []*x509svid.SVID) *x509svid.SVID {
			for _, svid := range svids {
				if strings.HasPrefix(svid.ID.Path(), "/"+session.Values["identifier"].(string)) {
					return svid
				}
			}
			return nil
		}),
		workloadapi.WithClientOptions(
			workloadapi.WithAddr(socketPath),
		),
	)
	if err != nil {
		return nil, nil, err
	}
	if svid, err := x509Src.GetX509SVID(); err != nil || svid == nil {
		return nil, nil, fmt.Errorf("missing x509 svid")
	}

	bundleSrc, err := workloadapi.NewBundleSource(req.Context(),
		workloadapi.WithClientOptions(
			workloadapi.WithAddr(socketPath),
		),
	)
	if err != nil {
		return nil, nil, err
	}

	return x509Src, bundleSrc, nil
}

func statusHandler(resp http.ResponseWriter, req *http.Request) {
	genericUserHandler(statusUrl, resp, req)
}

func showBundleHandler(resp http.ResponseWriter, req *http.Request) {
	genericUserHandler(showBundleUrl, resp, req)
}

func addBundleHandler(resp http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	x509Src, bundleSrc, err := getCertData(req)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	client := http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsconfig.MTLSClientConfig(x509Src, bundleSrc, tlsconfig.AuthorizeID(userProviderSpiffeID)),
		},
	}

	response, err := client.Post(addBundleUrl, "application/json", req.Body)
	if err != nil || response.StatusCode != http.StatusOK {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}

func registerHandler(resp http.ResponseWriter, req *http.Request) {
	session, _ := store.Get(req, "session")
	if session.IsNew {
		session.Values["identifier"] = uuid.New().String()
	}

	if err := session.Save(req, resp); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		log.Printf("Error setting session cookie: %v", err)
		return
	}

	if req.Method != http.MethodPost {
		resp.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	var userData map[string]string
	decoder := json.NewDecoder(req.Body)
	if err := decoder.Decode(&userData); err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	if _, ok := userData["user"]; !ok {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	user := userData["user"]
	if user == "" {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
	if path.Base(user) == "admin" {
		resp.WriteHeader(http.StatusUnauthorized)
		return
	}

	data := map[string]string{
		"session": session.Values["identifier"].(string),
		"user":    user,
	}
	jsonData, err := json.Marshal(data)
	if err != nil {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}

	response, err := http.Post(registerUrl, "application/json", bytes.NewBuffer(jsonData))
	if err != nil || response.StatusCode != http.StatusOK {
		resp.WriteHeader(http.StatusInternalServerError)
		return
	}
}
