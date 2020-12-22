#include <bits/stdc++.h>

using namespace std;

void decrypt (uint16_t* v, uint16_t* k) {
    uint16_t v0=v[0], v1=v[1], sum=416, i;
    uint16_t delta=0xf00d;
    uint16_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];
    for (i=0; i<32; i++) {
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }
    v[0]=v0; v[1]=v1;
}

int main() {
  uint16_t encrypted[] = {12263, 64385, 17263, 21844, 59059, 40727, 12495, 21699, 58982, 30941, 52310, 2067, 52933, 47229, 28811, 45010, 3549, 61620};
  #pragma omp parallel for
  for(int i = 0;i<65536;i++){
    for(int j = 0;j<65536;j++){
      uint16_t ii = uint16_t(i);
      uint16_t jj = uint16_t(j);
      uint16_t key[] = {ii, jj, ii^jj, ii&jj};
      string s;
      for(int k = 0; k<18; k+=2){
        uint16_t v[] = {encrypted[k], encrypted[k+1]};
        decrypt(v,key);
        s += char(v[0]>>8);
        s += char(v[0]%256);
        s += char(v[1]>>8);
        s += char(v[1]%256);
      }
      if(s.find("ASIS{") != string::npos) cout<<s<<endl;
    }
  }

	return 0;
}