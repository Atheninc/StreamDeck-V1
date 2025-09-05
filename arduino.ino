// Pro Micro: 4 boutons -> messages série pour OBS
const uint8_t PINS[4] = {2,3,4,5};
const char* MSGS[4] = {"SC1","SC2","SC3","SC4"};
const unsigned long DEBOUNCE=35;
const unsigned long BOOT_DELAY=1200;
int lastS[4]; unsigned long lastT[4];

void setup(){
  for(int i=0;i<4;i++){ pinMode(PINS[i], INPUT_PULLUP); lastS[i]=HIGH; lastT[i]=0; }
  delay(BOOT_DELAY);
  Serial.begin(115200);
}

void loop(){
  unsigned long now=millis();
  for(int i=0;i<4;i++){
    int s=digitalRead(PINS[i]);
    if(s!=lastS[i] && (now-lastT[i])>DEBOUNCE){
      lastT[i]=now;
      if(s==LOW){ Serial.println(MSGS[i]); }  // appui
      lastS[i]=s;
    }
  }
}