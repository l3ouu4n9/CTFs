#include <ESP8266WiFi.h>
#include <strings.h>
#include <GDBStub.h>



//ssid, wifipass, flag, PASSWORD
#include "credentials.h"
#include "webpage.h"

#define GPIO_PIN 2 // Can be changed when configuring the LEDs.
static int on = 1; // Tracks the state of the GPIO pin.
int debugmode = 0;	//are we deboooooging



void send_website(WiFiClient &client) {
    String response = String(HTTP_RESPONSE_HEADER) + WEBSITE_HTML + "\r\n\r\n";
    client.println(response);
    client.flush();
}

void send_message_response(WiFiClient &client, char *str) {
    String response = String(HTTP_RESPONSE_HEADER) + "<!DOCTYPE HTML>" +
                      "<html>" + str + "</html>\r\n\r\n";
    client.println(response);
    client.flush();
}

void send_error_response(WiFiClient &client, int code, char *message) {
    String error_message = String(code) + " " + message;
    String response = String("HTTP/1.1 ") + error_message +
                      "\r\nContent-Type: text/html; charset=utf-8\r\n" +
                      "Connection: close\r\n\r\n" + "<!DOCTYPE HTML>" +
                      "<html>" + error_message + "</html>\r\n\r\n";
    client.println(response);
    client.flush();
}

void send_flag(WiFiClient &client) {
    String response = String(HTTP_RESPONSE_HEADER) + "<!DOCTYPE HTML>" +
                      "<html>" + flag + "</html>\r\n\r\n";
    client.println(response);
    client.flush();
}

char *check_password(char *p) {
    char *out;
//    Serial.println("\npasswod!");
//    Serial.println(p);
    if (!strcmp(p, PASSWORD)) {
        on = !on;
        digitalWrite(GPIO_PIN, on);
        out = "Correct! Switching a light.";
//        Serial.println(p);
    } else {
        out = "Incorrect! No light 4u!!!";
    }

    return out;
}

void handle_request(WiFiClient &client, char *request) {
    char *line = strtok(request, "\n");
    if (!line) {
        send_error_response(client, 400, "Bad Request");
        return;
    }

    char *token = strtok(line, " ");
    if (!token || strncmp(token, "GET", strlen("GET"))) {
        send_error_response(client, 400, "Bad Request");
        return;
    }

    token = strtok(NULL, " ");
    if (!token) {
        send_error_response(client, 400, "Bad Request");
    } else if (!strcmp(token, "/") || !strcmp(token, "/index.html") ||
               !strcmp(token, "index.html") || !strcmp(token, "/index")) {
        send_website(client);
    } else if (strstr(token, "/check_password") == token) {
        char *subtoken = strtok(token, "?");
        subtoken = strtok(NULL, "?");
        if (strstr(subtoken, "password=") != subtoken) {
            send_error_response(client, 400, "Bad Request");
            return;
        }
        subtoken = strtok(subtoken, "=");
        subtoken = strtok(NULL, "=");
        if (!subtoken) {
            send_error_response(client, 400, "Bad Request");
        } else {
            char password[32];
            strcpy(password, subtoken);
            password[31] = '\0';
            send_message_response(client, check_password(password));
        }
        return;
    } else if (strstr(token, "/ping") == token) {
        send_message_response(client, "pong");
    } else {
        send_error_response(client, 404, "Not Found");
    }
    return;
}

void handle_connection(WiFiClient &client) {
    String request = "";
    while (client.connected()) {
        if (client.available()) {
            String line = client.readStringUntil('\r');
            request += line;
            if (line.length() == 1 && line[0] == '\n') {
                char *r = (char*)request.c_str();
                handle_request(client, r);
//		free(r);
                break;
            }
        }
    }
}

WiFiServer server(80);

void setup() {
    Serial.begin(115200);
	if(debugmode){
		gdbstub_init();
		Serial.printf("\nDebugging\n", send_flag);
	}

    pinMode(GPIO_PIN, OUTPUT);

    Serial.printf("Connecting to %s ", ssid);
    digitalWrite(GPIO_PIN, LOW);
    WiFi.begin(ssid, wifipass);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println(" connected");
    digitalWrite(GPIO_PIN, HIGH);

    server.begin();
    Serial.printf("Web server started, open %s in a web browser\n",
                  WiFi.localIP().toString().c_str());
}

void loop() {
    WiFiClient client = server.available();
    // wait for a client (web browser) to connect
    if (client) {
        Serial.println("\n[Client connected]");
        handle_connection(client);
        client.stop();
//        Serial.println("[Client disonnected]");
    }
}
