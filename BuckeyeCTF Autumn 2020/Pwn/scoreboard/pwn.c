#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define LINE_MAX 256

#define SHORT_NAME_LEN 8
#define TEAM_NAME_LEN 32
#define FLAG_SIZE 64
#define MESSAGE_SIZE 256
#define PLAYER_NAME_LEN 64
#define NUM_PLAYING 11

struct {
  char scoreboard_message[MESSAGE_SIZE];
  char default_datafile[MESSAGE_SIZE];
} status;


struct team {
  char name[TEAM_NAME_LEN];
  char short_name[SHORT_NAME_LEN];
  int score;
  struct player* players_on_field[NUM_PLAYING];
};

struct player {
  char name[PLAYER_NAME_LEN];
  short number;
};

struct team team1, team2;

void read_team(struct team *t, FILE *f) {
    fgets(t->name, TEAM_NAME_LEN, f);
    t->name[strlen(t->name)-1] = '\0';
    fgets(t->short_name, TEAM_NAME_LEN, f);
    t->short_name[strlen(t->short_name)-1] = '\0';

    // Read in players
    t->score = 0;
    char name[PLAYER_NAME_LEN] = "\0";
    int idx = 0;
    do {
      char *ret = fgets(name, PLAYER_NAME_LEN, f);
      name[strlen(name)-1] = '\0';
      if (ret == NULL) break;
      struct player *p = malloc(sizeof(struct player));
      strcpy(p->name, name);
      fscanf(f, "%hd ", &(p->number));
      t->players_on_field[idx++] = p;
      if (idx == NUM_PLAYING) break;
    } while (strlen(name) > 1);
}
void read_file() {
  FILE *f = fopen(status.default_datafile, "r");
  
  if (f) {
    read_team(&team1, f);
    read_team(&team2, f);
    fclose(f);
  }
  printf("Done.\n");
}

struct team* pick_team() {
  printf("[0] %s\n", team1.name);
  printf("[1] %s\n", team2.name);
  printf("Pick team (enter 0 or 1): ");
  
  int selection = 0;
  scanf("%d", &selection);
  getc(stdin);

  if (selection == 0) {
    return &team1;
  } else {
    return &team2;
  }
}

void update_team() {
  struct team *t = pick_team();
  printf("Enter new team name: ");
  fgets(t->name, TEAM_NAME_LEN, stdin);
  t->name[strlen(t->name)-1] = '\0';
  
  printf("Enter new team abbreviation: ");
  fgets(t->short_name, TEAM_NAME_LEN, stdin);
  t->short_name[strlen(t->short_name)-1] = '\0';
}

void substitute() {
  struct team *t = pick_team();
  for (int i=0; i<NUM_PLAYING; i++) {
    printf("[%d] %s\n", i, t->players_on_field[i]->name);
  }
  printf("Pick player [0-%d]: ", NUM_PLAYING-1);
  int selection = 0;
  scanf("%d", &selection);
  getc(stdin);

  printf("Enter substitute player name: ");

  char name[PLAYER_NAME_LEN] = "\0";
  char *ret = fgets(name, PLAYER_NAME_LEN, stdin);
  name[strlen(name)-1] = '\0';

  struct player *p = malloc(sizeof(struct player));
  strcpy(p->name, name);

  printf("Enter substitute player number: ");
  scanf("%hd", &(p->number));
  getc(stdin);

  free(t->players_on_field[selection]);
  t->players_on_field[selection] = p;
}

void print_team(struct team *t) {
  printf("%s: %d\n", t->name, t->score);
  for (int i=0; i<NUM_PLAYING; i++) {
    printf("- #%hd %s\n", t->players_on_field[i]->number, t->players_on_field[i]->name);
  }
  printf("\n");
}

void show() {
  printf("%s %d - %s %d\n\n", team1.short_name, team1.score, team2.short_name, team2.score);
  printf("Message: %s", status.scoreboard_message);
  print_team(&team1);
  print_team(&team2);
}

void score() {
  struct team *t = pick_team();
  printf("# of points to add: \n");
  int add;
  scanf("%d", &add);
  getc(stdin);
  t->score += add;
  printf("%s %d - %s %d\n\n", team1.short_name, team1.score, team2.short_name, team2.score);
}

void menu() {
  puts("Commands:");
  puts("\tscore - give a team points");
  puts("\tshow - show the scoreboard");
  puts("\tsubstitution - replace a player on the field with another");
  puts("\tteam - update team info");
  puts("\tmessage - update scoreboard message");
  puts("\treset - reset to match defaults file");
  puts("\tquit - exit the program");
}

void message() {
  printf("Please enter the new message: ");
  fgets(status.scoreboard_message, MESSAGE_SIZE, stdin);
}


int main(int argc, char **argv) {

  setvbuf(stdout, 0, 2, 0);

  char buf[LINE_MAX];
  strcpy(status.default_datafile, "default.txt");

  read_file();
   
  puts("***************************************\n");
  puts("**     SCOREBOARD UPDATING SYSTEM    **\n");
  puts("***************************************\n");
  printf("Scoreboard: Ohio Stadium.\n");
  
  menu();

  while(1) {
    puts("\nEnter your command:");

    if(fgets(buf, LINE_MAX, stdin) == NULL)
      break;

    if(!strncmp(buf, "score", 5)){
      score();
    } 
    else if(!strncmp(buf, "show", 4)){
      show();
    } 
    else if(!strncmp(buf, "substitution", 12)){
      substitute();
    } 
    else if(!strncmp(buf, "team", 4)){
      update_team();
    } 
    else if(!strncmp(buf, "message", 7)){
      message();
    } 
    else if(!strncmp(buf, "reset", 5)){
      read_file();
    }
    else if(!strncmp(buf, "quit", 4)){
      return 0;
    }
    else{
      puts("Invalid option");
      menu();
    }
  }
}
