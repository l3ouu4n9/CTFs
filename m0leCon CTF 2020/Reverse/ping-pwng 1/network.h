#pragma once
#include "player.h"
#include "defaults.h"
#include "encrypt.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>
#include <string.h>
#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#define SERVER_PORT 1024
#define BUFF_MAX_LEN 512 //in bytes
#define SERVER_DEFAULT_IP "127.0.0.1"
#define RECEIVE_FLAGS 0 
#define SEND_FLAGS 0 
#include <sys/time.h>

int64_t getTimeMillis3();
namespace proto {
    typedef enum proto_t {
        NO_PROTO, LOGIN, LOGIN_CONFIRM, LOGIN_NOT_CONFIRM, CLIENT_KEY, GAME_STARTS, FIN, PLAYER_POS, TEST, BALL, ENCRYPTED
    } proto_t;


    struct basic_packet {
        const proto_t proto;
        basic_packet() : proto(NO_PROTO) {}
        basic_packet(proto_t proto) : proto(proto) {}

    };


    struct login_packet : public basic_packet{
        char name[PLAYER_NAME_MAX_LENGTH];
        login_packet(const char n[PLAYER_NAME_MAX_LENGTH]) : basic_packet(LOGIN) {
            strncpy(name, n, PLAYER_NAME_MAX_LENGTH);
        }
    };


    struct login_confirm_packet : public basic_packet {
        bool isLeft;
        unsigned int player_id;
        rectangle starting_rectangle;
        char serverKey[KEY_LENGTH];
        login_confirm_packet(bool isLeft, unsigned int player_id, rectangle starting_rectangle, const char key[KEY_LENGTH])
            :  basic_packet(LOGIN_CONFIRM), isLeft(isLeft), player_id(player_id), starting_rectangle(starting_rectangle) {
              strncpy(serverKey, key, KEY_LENGTH);
            }


        static login_confirm_packet getPlayerLeftDefaultPacket(unsigned int player_id, const char key[KEY_LENGTH]) {

            return {
                true,
                player_id,
			    rectangle(
				    point(DEFAULT_PLAYER_LEFT_STARTING_X, DEFAULT_PLAYER_LEFT_STARTING_Y),
                    DEFAULT_PLAYER_STARTING_WIDTH,
				    DEFAULT_PLAYER_STARTING_HEIGHT
          ),
          key
            };
        }


        static login_confirm_packet getPlayerRightDefaultPacket(unsigned int player_id, const char key[KEY_LENGTH]) {
            return {
                false,
                player_id,
			    rectangle(
				    point(DEFAULT_PLAYER_RIGHT_STARTING_X, DEFAULT_PLAYER_RIGHT_STARTING_Y),
                    DEFAULT_PLAYER_STARTING_WIDTH,
				    DEFAULT_PLAYER_STARTING_HEIGHT
          ),
          key
            };
        }
    };

    struct player_pos_packet : public basic_packet {
        int x, y;
        player_pos_packet(double x, double y) : basic_packet(PLAYER_POS), x(x), y(y) {}
        void update(double new_x, double new_y) {
            x = new_x;
            y = new_y;
        }
    };

    struct game_starts_packet : public basic_packet {
        rectangle starting_rectangle;
        moving_circle ball;
        game_starts_packet(rectangle starting_rectangle, moving_circle ball) : basic_packet(GAME_STARTS), starting_rectangle(starting_rectangle), ball(ball) {

        }


        static game_starts_packet getPlayerRightDefaultPacket() {
            return {
                rectangle(point(DEFAULT_PLAYER_RIGHT_STARTING_X, DEFAULT_PLAYER_RIGHT_STARTING_Y)
                , DEFAULT_PLAYER_STARTING_WIDTH
		        , DEFAULT_PLAYER_STARTING_HEIGHT)
		        , moving_circle()
	        };
        }


        static game_starts_packet getPlayerLeftDefaultPacket() {
            return {
                rectangle(point(DEFAULT_PLAYER_LEFT_STARTING_X, DEFAULT_PLAYER_LEFT_STARTING_Y)
                , DEFAULT_PLAYER_STARTING_WIDTH
		        , DEFAULT_PLAYER_STARTING_HEIGHT)
		        , moving_circle()
	        };
        }
    };

    struct test_packet : public basic_packet{
        char c;
        int i;
        test_packet() : basic_packet(TEST), c('S'), i(666) {}
    };

    struct ball_packet : public basic_packet {
        moving_circle ball;
        ball_packet(moving_circle ball) : basic_packet(proto::BALL) {
            this->ball = ball;
        }
        void update(moving_circle* ball) {
            this->ball = *ball;
        }
    };
    struct encrypted_packet : public basic_packet{
      int64_t sendTime;
      int32_t sender;
      void* buff;
      int32_t sigLen;
      void* sig;
      int32_t len;
      encrypted_packet(ball_packet* pack, string serverKey, int cryptoSock) : basic_packet(ENCRYPTED){
        buff=malloc(sizeof(*pack));
        if(buff==NULL){
          sender=-1;
          return;
        }
        ball_packet p = *pack;
        memcpy(buff, pack, sizeof(*pack));
        sender=1;
        len=sizeof(*pack);
        sendTime=getTimeMillis3();
        sigLen=enc(buff, len, serverKey, cryptoSock,&sig);
      }
      encrypted_packet(player_pos_packet* pack, int a):basic_packet(ENCRYPTED){
        buff=malloc(sizeof(*pack));
        if(buff==NULL){
          sender=-1;
          return;
        }
        player_pos_packet p = *pack;
        memcpy(buff, pack, sizeof(*pack));
        sender=0;
        len=sizeof(*pack);
        sigLen=0;
        sendTime=getTimeMillis3();
        sig=NULL;
      }
      encrypted_packet(void* buf, int leng):basic_packet(ENCRYPTED){
        if(leng<20){
          sendTime=0;
          sender=-1;
          len=0;
          sigLen=0;
          return;
        }
        memcpy(&sendTime, buf, sizeof(int64_t));
        memcpy(&len,((char*)buf)+sizeof(int64_t),sizeof(int32_t));
        buff=malloc(len);
        if(buff==NULL){
          sender=-1;
          return;
        }
        memcpy(&sender,((char*)buf)+sizeof(int64_t)+sizeof(int32_t), sizeof(int32_t));
        if(len+sigLen+(sizeof(int32_t)*5)<leng){
          sender=-1;
          return;
        }
        memcpy(buff,((char*)buf)+sizeof(int64_t)+sizeof(int32_t)*2, len);
        memcpy(&sigLen, ((char*)buf)+sizeof(int64_t)+sizeof(int32_t)*2+len, sizeof(int32_t));
        if(sigLen==0){
          sig=NULL;
        }else{
          sig=malloc(sigLen);
          if(sig==NULL){
            sigLen=0;
            return;
          }
          memcpy(sig, ((char*)buf)+sizeof(int64_t)+sizeof(int32_t)*2+len+sizeof(int32_t), sigLen);
        }
      }
      void* serialize(){
        void* tmp = malloc(this->len+sizeof(int32_t)*3+sizeof(int64_t)+max(this->sigLen, 0));
        if(tmp==NULL){
          return NULL;
        }
        memcpy(tmp, &(this->sendTime), sizeof(int64_t));
        memcpy(((char*)tmp)+sizeof(int64_t), &(this->len), sizeof(int32_t));
    	memcpy(((char*)tmp)+sizeof(int64_t)+sizeof(int32_t), &(this->sender), sizeof(int32_t));
    	memcpy(((char*)tmp)+sizeof(int64_t)+sizeof(int32_t)*2, this->buff, this->len);
        memcpy(((char*)tmp)+sizeof(int64_t)+sizeof(int32_t)*2+this->len, &(this->sigLen), sizeof(int32_t));
        if(this->sigLen!=0){
          memcpy(((char*)tmp)+sizeof(int64_t)+sizeof(int32_t)*2+this->len+sizeof(int32_t), (this->sig), this->sigLen);
        }
        return tmp;
      }
    };
    const char* getProtoName(const proto_t& p);
}

size_t send_packet(int sock, const void* buf, size_t size, struct sockaddr_in &target);
size_t receive_packet(int sock, void* buf, size_t size, struct sockaddr_in &source);
