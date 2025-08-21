//***************************************************************************************************
//****************************CONTROLANDO O ARDUINO/ESP32 VIA O EXCEl.*******************************
//*******************VERSÃO DO EXCEL PREPARADA PARA RODAR TANTO EM 32 OU 64 BITS*********************
//***OS EXEMPLOS DO PROGRAMA DO EXCEL DEVEM SER CONSTRUIDOS APARTIR DO EXEMPLO CONTIDO NESTA PASTA***
//*O PROGRMA ESCRITO PARA O EXCEL CONTEM UMA MACRO E O MESMO DEVE SER GRAVADO COM A TERMINAÇAO xlsm**
//*****************************ARQUIVOS DO EXCEL COM SUPORTE DE MACRO********************************
//***************************************************************************************************

//******DEFINIÇÕES DE HARDWARE
#define LED  13                     //*****(Arduino 13)   *****(ESP32  2)

//*******DEFINIÇÃO DE VARIAVEIS
char Letra [] = {'A','B','C','D'};  //Colunas do Excel
long int N_Pontos = 4096;                   
float Seno, Sen;
int N_Blink_A = 5;
int i,jj,opcao,pot;
int Tempo = 50;
float volt;              

           void setup() 
        {
              Serial.begin(9600);
              pinMode(LED, OUTPUT); 
          
        }


void loop() 

  {
                  if (Serial.available()>0)  
                              
               {
                     opcao = Serial.read();    
               }
                 
         switch(opcao)
         
     {


        case 'A':
             
             for( i=0; i < N_Blink_A; i= i+1)
                    {
                         digitalWrite(LED, HIGH);
                         delay(Tempo);
                         digitalWrite(LED, LOW);
                         delay(Tempo);
                    }
                        opcao=100;       
                        break;
                        
      

             case 'B': //Envia dados para as Celulas A e B do Excel

             Serial.println("RESETROW");       //Volta para a primeira celula do Excel
             digitalWrite(LED, HIGH);
             jj=1;                             //Variavel responsavel pela troca de linha
             
             for( i=0; i < N_Pontos; i= i+1)
                    {
                        //Seno = 10.0*sin(i/1.0)+5.0*sin(i*0.94/1.0);
                         pot = analogRead(0);
                         volt = 10.0*pot/1023.0;
                         Serial.print("CELL,SET,");        //Especifica a Celula do Excel
                         Serial.print (Letra [0]);         //Especifica a Coluna  (*A*)
                         Serial.print (jj);                //Especifica a Linha
                         Serial.print(",");
                         Serial.println (i);               //Envia o Dado pata a Celula Especificada
                         Serial.print("CELL,SET,");
                         Serial.print (Letra [1]);         ///Especifica a Coluna (*B*)
                         Serial.print (jj);
                         Serial.print(",");
                         Serial.println (volt,2);
                         //Serial.println (Seno,2);        
                         jj=jj+1;                          //Evolução das Linhas     
                         delay(Tempo);       
                   }
                        digitalWrite(LED, LOW);
                        opcao=100;       
                        break;


          case 'C': //Envia dados para as Celulas C e D

               Serial.println("RESETROW");
               digitalWrite(LED, HIGH);
               jj=1;
             
              for( i=0; i < N_Pontos; i= i+1)
                    {
                         Sen = 5.0*pow(2.71,(-i/1000.0))*sin(i/3.0);
                         
                         Serial.print("CELL,SET,");
                         Serial.print (Letra [2]);       //(*C*)
                         Serial.print (jj);
                         Serial.print(",");
                         Serial.println (i);
                         
                         Serial.print("CELL,SET,");      //(*D*)
                         Serial.print (Letra [3]);
                         Serial.print (jj);
                         Serial.print(",");
                         Serial.println (Sen,2);   
                         jj=jj+1;            

                    }
                        digitalWrite(LED, LOW);
                        opcao=100;       
                        break;



              case 'D':    
                        //************ZERANDO A PLANILHA******************
                        
                        Serial.println("RESETROW");
                        Serial.println("CLEARDATA");
                        Serial.println("RESETROW");
                        
                        digitalWrite(LED, HIGH);
                        delay(500);
                        digitalWrite(LED, LOW);
                       
                        opcao=100;
                        break;
                        
              
              
                      
                   default:
                   delay(1);                
     }

}          



  

       
