#!/bin/bash

                                                                                                                                                                                                 
function Series                                                                                                                                                                               
{                                                                                                                                                                                                

                                                                                                                                                                                                 
### $1 ubicacion Seriess #####                                                                                                                                                                 


find $1 -type d | awk -F"/Series/" '{print $2}' | sed 1d #####| sed s/.$//


#Expansion_2/Series/Frasier
#Expansion_2/Series/Game Of Thrones
#Expansion_2/Series/Superman and Lois


                                                                                                                                                                                                 
find "$1" -type d > ListaTotal-find.txt                                                                                                                                        
cat ListaTotal-find.txt | awk -F"/Series/" '{print $2}'  > Lista-SERIES.txt                                                                                                                                             
                                                                                                                                                                                                 
## Expansion_2/Series/Game Of Thrones/Game of Thrones S01E01 2160p Blu-ray.mkv
## Expansion_2/Series/Game Of Thrones/Game of Thrones S01E02 2160p Blu-ray.mkv
                                                                                                                                                                                                 
                                                                                                                                                                                                 
                                                                                                                                                                                                 
i=$(cat Lista-find.txt | wc -l)                                                                                                                                                                  
j=1                                                                                                                                                                                              
                                                                                                                                                                                                 
                                                                                                                                                                                                 
    until [[ "$j" -gt "$i" ]]                                                                                                                                                                    
       do                                                                                                                                                                                        
         filmname=$(cat Lista-find.txt |  sed -n "$j"p | awk -F"/" '{print $NF}')  #### Game of Thrones S01E01 2160p Blu-ray.mkv ###                                                                                                              
         name=$(echo "$filmname" | awk -F" S" '{print $1}' ) 
         seasons=

                                                                                                                       
         year=$(echo "$filmname" | awk -F"(" '{print substr ($2,1,4)}')                                                                                                                          
         pixels=$(echo "$filmname" | awk -F")" '{print $2}' | awk -F" " '{print $1}')                                                                                                            
         format=$(echo "$filmname" | awk -F" " '{print $NF}' | sed 's/.mkv//g')                                                                                                                  
         group=$(cat Lista-find.txt | sed -n "$j"p | awk -F"/" '{print $(NF-1)}')      ### path anterior ###                                                                                     
         HDD=$(cat Lista-find.txt | sed -n "$j"p | awk -F"/" '{print $1}')      ### Disco ###                                                                                                    
         echo "|""$name""|""$year""|""$pixels""|""$format""|""$group""|""$HDD""|"                                                                                                                
       done                                      
}



function Peliculas
{

### $1 ubicacion peliculas #####                                                                                                  
                                                                                                                    
find "$1" -maxdepth 10 -name "*.mkv" > ListaTotal-find.txt                                                           
grep -v Series ListaTotal-find.txt  > Lista-find.txt                                                                

### Expansion_1/Sagas/Rambo/First Blood (1982) 1080p Remux.mkv
### Expansion_1/Sagas/Rambo/Rambo (2008) 1080p Remux.mkv

                                                                                                                                                        
                                                                                                                                                        
i=$(cat Lista-find.txt | wc -l)                                                                                                                         
j=1                                                                                                                                                     
                                                                                                                                                        
                                                                                                                                                        
    until [[ "$j" -gt "$i" ]]                                                                                                                           
       do                                                                                                                                               
         filmname=$(cat Lista-find.txt |  sed -n "$j"p | awk -F"/" '{print $NF}')                                                                       
         name=$(echo "$filmname" | awk -F"(" '{print $1}' | sed s/.$//)                                                                                 
         year=$(echo "$filmname" | awk -F"(" '{print substr ($2,1,4)}')                                                                                 
         pixels=$(echo "$filmname" | awk -F")" '{print $2}' | awk -F" " '{print $1}')                                                                   
         format=$(echo "$filmname" | awk -F" " '{print $NF}' | sed 's/.mkv//g') 
         group=$(cat Lista-find.txt | sed -n "$j"p | awk -F"/" '{print $(NF-1)}')      ### path anterior ###   
         HDD=$(cat Lista-find.txt | sed -n "$j"p | awk -F"/" '{print $1}')      ### Disco ###      
         echo "|""$name""|""$year""|""$pixels""|""$format""|""$group""|""$HDD""|"

##################################


         ####### Insercion en sqlite #######                                                                                                            
         
         #mysql -h 192.168.1.46 -P 3306 -u manilovic -pmani "manilovicdb" -e "insert into Peliculas (Nombre, Estreno, Resolucion, Formato, Grupo, Disco_Duro) values ('$name', '$year', '$pixels', '$format', '$group', '$HDD');"
	 	 echo "{ "Nombre":"$name",
		        "Estreno":"$year",
			"Resolucion":"$pixels",
			"Formato":"$format",
			"Grupo":"$group",
			"Disco_Duro":"$HDD"}"




         ##sqlite3 Peliculas.db "insert into Peliculas (Nombre, Estreno, Resolucion, Formato, Grupo, Disco_Duro) values ('$name', '$year', '$pixels', '$format', '$group', '$HDD')"
                  # if [ "$?" != "0" ]                                                                                                                        
                   #    then                                                                                                                                  
                    #   echo "Pelicula ya en BD, actulizarla? "s" o "n"?"                                                                                         
                     #  read -r respuesta                                                                                                                        
                      #      case $respuesta in                                                                                                               
                       #         s)                                                                                                                           
                        #            sqlite3 Peliculas.db  "update Peliculas set Estreno='$year', Resolucion='$pixels', Formato='$format', Grupo='$group', Disco_Duro='$HDD' where Nombre='$name'"
                         #           echo "Actualizado '$name', '$year', '$pixels', '$format', '$group', '$HDD')";;                                                                    
                          #      n)                                                                                                                                            
                           #         echo "No actualizado";;                                                                                                                   
                            #                                                                                                                                                  
                             #   *)  echo "error, inserte "s" o "n""                                                                                                           
                            # esac                                                                                                                                             
                  # fi                                                                                                                                                         
                                                                                                                                                                              
         ####### Insercion en sqlite #######                 

          ((j++))  
       done


rm ListaTotal-find.txt Lista-find.txt                                 

}


########### MAIN ############
                                                          
                                                              
  while [[ $1 = -* ]]; do                                     
  case "$1" in                                                
      -ser) SERIE=1;       shift ;;                           
      -pel) PELICULA=1;    shift ;;                                              
      *) echo "ERROR - Ningun argumento valido";exit 1;;                         
  esac                                                                           
  done                                                                 



if [[ $SERIE = 1 ]]
   then 
      Series "$1"
   else
      Peliculas "$1"

fi

