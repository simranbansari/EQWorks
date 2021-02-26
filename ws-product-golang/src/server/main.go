package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"sync"
	"time"
)

type counters struct {
	sync.Mutex
	view  int
	click int
}
type countersTwo struct {
	view  int
	click int
}

var (
	c = counters{}

	content = []string{"sports", "entertainment", "business", "education"}
)

var counters_map = make(map[string]countersTwo)

var mock_store = make(map[string]countersTwo)


func welcomeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Welcome to EQ Works 😎")
}

func viewHandler(w http.ResponseWriter, r *http.Request) {
	data := content[rand.Intn(len(content))]
	currTime := time.Now().Format("2006-01-02 15:04")
	fmt.Println(data)
	fmt.Println(currTime)

	key := data + ":" + currTime

	c.Lock()
	c.view++
	c.Unlock()

	counters_map[key] = countersTwo{view: c.view, click: c.click}

	err := processRequest(r)
	if err != nil {
		fmt.Println(err)
		w.WriteHeader(400)
		return
	}

	if rand.Intn(100) < 50 {
		processClick(data, currTime)
	}
}

func processRequest(r *http.Request) error {
	time.Sleep(time.Duration(rand.Int31n(50)) * time.Millisecond)
	return nil
}

func processClick(data string, currTime string) error {
	key := data + ":" + currTime

	c.Lock()
	c.click++
	c.Unlock()

	counters_map[key] = countersTwo{view: c.view, click: c.click}

	return nil
}

var statsHandlerStart = time.Now()
var statsNumCalls = 0

func statsHandler(w http.ResponseWriter, r *http.Request) {
	statsHandlerCurr := time.Now()

	diff := statsHandlerCurr.Sub(statsHandlerStart)

	if diff >= time.Second*10{
		statsNumCalls = 1
		statsHandlerStart = time.Now()

		if !isAllowed() {
			w.WriteHeader(429)
			return
		}
	}else{
		if statsNumCalls == 5{
			fmt.Fprint(w, "Too many requests")
		}else{
			statsNumCalls++
			if !isAllowed() {
				w.WriteHeader(429)
				return
			}
		}
	}
}

func isAllowed() bool {
	return true
}

func uploadCounters() error {
	return nil
}

func main() {

	http.HandleFunc("/", welcomeHandler)
	http.HandleFunc("/view/", viewHandler)
	http.HandleFunc("/stats/", statsHandler)

	go addToStore()

	log.Fatal(http.ListenAndServe(":8080", nil))
}

func addToStore(){

	tk := time.New_Ticker(5 * time.Second)

	for range tk.C{
		for key, value := range counters_map{
			mock_store[key] = countersTwo{view: value.view, click: value.click}
			delete(counters_map, key)
		}
		fmt.Println(mock_store)
	}

}
