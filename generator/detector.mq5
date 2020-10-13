int MA_handle;
double up_buffer[];
double down_buffer[];
int socket = INVALID_HANDLE; 
int handle;
//+------------------------------------------------------------------+ //wprsisignal FOREX HUNTER MT52 event 
input int up_buffer_number = 1;
input int down_buffer_number = 0;
input string indicator = "event"; 
input bool TESTING = true;
bool VAR_UP = false;
bool VAR_DOWN = false;
 input int v0; input int v1; input int v2;bool DETECTION_ACTIVATED = true;
int OnInit(){
   if(!TESTING) socket = Socket_Connect();
        handle=iCustom(NULL,0,indicator,v0,v1,v2);   handle=iCustom(NULL,0,indicator); //wprsisignal 
   return(INIT_SUCCEEDED);
}
void OnDeinit(const int reason){
   Socket_Close(socket);
}

void OnTick(){
   Main();
}  

void Main(){
   datetime now = TimeCurrent();
   datetime three_days = now - 86400;                 
   int up = CopyBuffer(handle,up_buffer_number,three_days,now,up_buffer);
   int down = CopyBuffer(handle,down_buffer_number,three_days,now,down_buffer);
   //Print("Down: "+IntegerToString(down)+" Up: "+IntegerToString(up));
   if(up>0){
      if(up_buffer[up-1]!=EMPTY_VALUE && up_buffer[up-1]!=0){
         VAR_UP = true;
      }
   }
   if(down>0){   
      if(down_buffer[down-1]!=EMPTY_VALUE && down_buffer[down-1]!=0){
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

void call(int up){
   if(!TESTING){
      Socket_Send(socket,"UP|"+_Symbol);
      Print("UP signal sent"+" UP | "+_Symbol+" | "+IntegerToString(_Period));
      VAR_UP = false;
   }else{
      Print("buffer_count: "+IntegerToString(up)+" | Up Arrow: "+DoubleToString(up_buffer[up-1]));
      VAR_UP = false;
   }
}
void put(int down){
   if(!TESTING){
      Socket_Send(socket,"DOWN|"+_Symbol);
      Print("Down signal sent"+"DOWN | "+_Symbol+" | "+IntegerToString(_Period));
      VAR_DOWN=false;      
   }else{
      Print("buffer_count: "+IntegerToString(down)+"Down Arrow: "+DoubleToString(down_buffer[down-1]));
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
  
int Socket_Connect(){
   ResetLastError();
   int h_socket = SocketCreate(SOCKET_DEFAULT);
  
   if(h_socket != INVALID_HANDLE){
      if(SocketConnect(h_socket,"127.0.0.1",8888,2000)){
         Print("Connected to Socket Server"); 
      }else{
         Print("Fail connected to Socket Server. error code : ", GetLastError()); 
      }  
   }else{
      Print("Fail SocketCreate error code : ", GetLastError()); 
   }
  return h_socket; 
}

int Socket_Send(int socket_handle,string str_data){
   if(socket_handle == INVALID_HANDLE) return 0; 
   
   uchar bytes[]; 
   int byte_size = StringToCharArray(str_data,bytes)-1; 
   
   return SocketSend(socket_handle,bytes,byte_size);
      
}

void Socket_Close(int socket_handle){
   if(socket_handle != INVALID_HANDLE){
      SocketClose(socket_handle);
      socket = INVALID_HANDLE; 
      Print("Socket Closed");      
   }
}