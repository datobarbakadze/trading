#include <socket-library-mt4-mt5.mqh>
double up_buffer[];
double down_buffer[];
ClientSocket * socket = NULL;
double handle;
ushort my_port = 8888;
//----------------------------------------------------

input int up_buffer_number = 1;
input int down_buffer_number = 0;
input string indicator = "event"; 
input bool TESTING = true;
bool VAR_UP = false;
bool VAR_DOWN = false;
 input int v0; input int v1;
int OnInit(){
   if(!TESTING) socket = new ClientSocket(my_port );
        handle=iCustom(NULL,0,indicator,v0,v1,0,0);
   return(INIT_SUCCEEDED);
}
void OnDeinit(const int reason){
   delete socket;
   socket = NULL;
}
void OnTick(){
   if(!TESTING && !socket.IsSocketConnected()) socket = new ClientSocket(my_port);
   Main();
}

void Main(){
   datetime now = TimeCurrent();
   datetime three_days = now - 86400;                 
   double up = iCustom(NULL,0,indicator,up_buffer_number,0);
   double down = iCustom(NULL,0,indicator,down_buffer_number,0);
   //Print("Down: "+IntegerToString(down)+" Up: "+IntegerToString(up));
   if(up>0){
      if(up!=EMPTY_VALUE && up!=0){
         VAR_UP = true;
      }
   }
   if(down>0){   
      if(down!=EMPTY_VALUE && down!=0){
         VAR_DOWN = true;
      }
   }
      
   if(isNewBar()){
      Print("new bar");
      if(VAR_UP==true){
         Print("up");
         call(up);
      }
      if(VAR_DOWN==true){
         Print("down");
         put(down);
      }
   }
}


void call(double up){
   if(!TESTING){
      socket.Send("UP|"+_Symbol);
      Print("UP signal sent"+" UP | "+_Symbol+" | "+IntegerToString(_Period));
      VAR_UP = false;
   }else{
      Print("buffer_count: "+DoubleToStr(up)+" | Up Arrow: "+DoubleToString(up));
      VAR_UP = false;
   }
}
void put(double down){
   if(!TESTING){
      socket.Send("DOWN|"+_Symbol);
      Print("Down signal sent"+"DOWN | "+_Symbol+" | "+IntegerToString(_Period));
      VAR_DOWN=false;      
   }else{
      Print("buffer_count: "+DoubleToStr(down)+"Down Arrow: "+DoubleToString(down));
      VAR_DOWN=false;   
   }
}

bool isNewBar(){
   //--- memorize the time of opening of the last bar in the static variable
   static datetime last_time=0;
   //--- current time
   datetime lastbar_time=SeriesInfoInteger(Symbol(),Period(),SERIES_LASTBAR_DATE);

   //--- if it is the first call of the function
   if(last_time==0){
   //--- set the time and exit
      last_time=lastbar_time;
      return(false);
   }

   //--- if the time differs
   if(last_time!=lastbar_time){
   //--- memorize the time and return true
      last_time=lastbar_time;
      return(true);
   }
   //--- if we passed to this line, then the bar is not new; return false
   return(false);
} 
