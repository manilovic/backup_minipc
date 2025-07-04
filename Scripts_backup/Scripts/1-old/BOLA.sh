#!/bin/bash                                                      
           



function CHECK
{
if [ -z "$nombre_TMDB" ]
    then
        date +"%c || Formato no correcto, no hay nombre TMDB ||" >> LogsJM/APIRename.txt
        echo  "|| Formato no correcto, no hay nombre TMDB ||"
        echo >> LogsJM/APIRename.txt
	echo
        exit 0
fi 

}


function PATH_FILE
{
 path=$(echo "$name" | rev | cut -d"/" -f 2- | rev)
 if [[ "$path" == "$name" ]] # por si no hay path
    then
	path=""
    else
	path="$path"/
 fi
 date +"%c || path=$path" >> LogsJM/APIRename.txt
 echo "|| path=$path ||"

}

function MOVE
{
 if mv "$name" "$FILE";
	 then
	    date +"%c || Fichero Nuevo || $FILE ||" >> LogsJM/APIRename.txt
	    echo "|| Fichero Movido || $FILE ||"
	    chmod 644 "$FILE"
         else
            date +"%c || ERROR || $FILE ||" >> LogsJM/APIRename.txt
	    echo "|| ERROR || $FILE ||"
 fi
}



function S01E01

{
   parte1=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="(S[0-9][0-9]E[0-9][0-9])" '{print $1}')
   parte2=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="(S[0-9][0-9]E[0-9][0-9])" '{print $2}')

   ####
   if [[ -z $parte1 ]]
       then
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte2"//g) 
       else
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte1"//g | sed s/"$parte2"//g) 
 
   fi
   ####
   season=$(echo "$season_episode" | awk '{print substr($0,2,2)}')
   episode=$(echo "$season_episode" | awk '{print substr($0,5,2)}')

   date +"%c || season=$season episode=$episode" >> LogsJM/APIRename.txt

}


function 1x01
{
   parte1=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="([0-9][x-X][0-9][0-9])" '{print $1}')
   parte2=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="([0-9][x-X][0-9][0-9])" '{print $2}')
   ####
   if [[ -z $parte1 ]]
       then
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte2"//g) 
       else
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte1"//g | sed s/"$parte2"//g) ### 2x03 
   fi
   ####
   season=$(echo "$season_episode" | awk '{print substr($0,1,1)}')
   episode=$(echo "$season_episode" | awk '{print substr($0,3,2)}')
   season_episode=S0"$season"E"$episode"

   date +"%c || season=$season episode=$episode" >> LogsJM/APIRename.txt
}


function 01x01
{
   parte1=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="([0-9][0-9][x-X][0-9][0-9])" '{print $1}')
   parte2=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="([0-9][0-9][x-X][0-9][0-9])" '{print $2}')
   ####
   if [[ -z $parte1 ]]
       then
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte2"//g) 
       else
          season_episode=$(echo "$name" | awk -F "/" '{print $NF}' | sed s/"$parte1"//g | sed s/"$parte2"//g)  
   fi
   ####
   season=$(echo "$season_episode" | awk '{print substr($0,2,2)}')
   episode=$(echo "$season_episode" | awk '{print substr($0,5,2)}')
   season_episode=S"$season"E"$episode"
   
   date +"%c || season=$season episode=$episode" >> LogsJM/APIRename.txt

}


####################################################




function Serie
{
	
#Expansion_2/Series/Star Wars: The Clone Wars (2008) - S02E01 - El robo del holocrón (816p).mkv
#carpeta=Expansion2/Series/

serie=$(echo "$name" |  awk -F"/" '{print $NF}' | awk -v FS="(\ \-\ S[0-9][0-9]E[0-9][0-9])" '{print $1}')
echo "$serie"
titulo=$(echo "$name" |  awk -F"/" '{print $NF}' | awk -v FS="(\([0-9][0-9][0-9][0-9]\)\ -\ )" '{print $2}')
echo "$titulo"

mkdir "$path""$serie" 2> /dev/null

FILE="$path""$serie"/"$titulo"
date +"%c || Renombrando || $FILE ||" >> LogsJM/APIRename.txt
echo "|| Renombrando || $FILE ||"

MOVE


}



function Pelicula
{

# $name es el fichero

#### TMDB API ####

curl -s "https://api.themoviedb.org/3/search/movie?api_key=2c0b5982e078e255ed5be3bba4c3064b&query=$nombre_TMDB&language=es" | jq -r '.results[0] | .title,.release_date,.original_title,.vote_average' > ttt.txt

titulo_TMDB=$(sed -n 1p ttt.txt)
date_TMDB=$( sed -n 2p ttt.txt | awk -F"-" '{print $1}')
titulo_original=$(sed -n 3p ttt.txt)
nota_TMDB=$(sed -n 4p ttt.txt); nota_TMDB=$(echo "scale=0; $nota_TMDB*10/1" | bc)

date +"%c || Titulo original || $titulo_original || $titulo_TMDB ||" >> LogsJM/APIRename.txt
echo "|| Titulo original || $titulo_original || $titulo_TMDB ||"


# curl -s https://www.rottentomatoes.com/m/avatar_the_way_of_water | grep -e audiencescore -e tomatometerscore


echo "|| Checking Mediainfo ||"
#### MEDIAINFO ####
medianame=$(mediainfo echo "$name" | sed 's/\ /\\\ /g' | sed 's/\&/\\&/g' | sed s/\(/\\\\\(/g | sed s/\)/\\\\\)/g | grep -e ^Height -e ^Original | awk -F":" '{print $2}')

pixelsmediainfo=$(echo "$medianame" | awk -F"pixels" '{print $1}' | sed s/\\\\\ //g | sed -n 1p)
       if [[ "$pixelsmediainfo" -lt 800 ]]
           then
              pixelsmediainfo="<800"
              formato="Rip"
           else
              if  [[ "$pixelsmediainfo" -ge 800 ]] && [[ "$pixelsmediainfo" -lt 1080 ]]
                 then
                   formato="Rip" ##pixels se queda como esta##
                 else
                   if [[ "$medianame" == *Blu-ray* ]]
                      then
                        formato="Blu-ray"
                      else
                          if  [[ "$pixelsmediainfo" -gt 1080 ]] && [[ "$pixelsmediainfo" -lt 2160 ]]
                             then
                               formato="Rip"
                             else
                               formato="Remux"
                          fi
                  fi
             fi
        fi


ext=$(echo "$name" | awk -F"/" '{print $NF}'); ext=${ext: -3}
FILE=""$path""$titulo_TMDB" ("$date_TMDB") "$nota_TMDB"% "$pixelsmediainfo"p "$formato"."$ext""

date +"%c || Renombrando || $FILE ||" >> LogsJM/APIRename.txt
echo "|| Renombrando || $FILE ||"

MOVE

rm ttt.txt

}



function Episodio
{

#Expansion_2/Series/El Pacificador/El pacificador S01E02 pppp.mkv

#### TMDB API ####

curl -s "https://api.themoviedb.org/3/search/tv?api_key=2c0b5982e078e255ed5be3bba4c3064b&language=es&query=$nombre_TMDB" | jq -r '.results[0] | .id,.name,.first_air_date,.original_name' > ttt.txt

#110492
#El Pacificador
#2022-01-13
#Peacemaker

### 12609

id_TMDB=12609
serie_TMDB="Dragon Ball"
date_TMDB=1989
serie_original=$(sed -n 4p ttt.txt)


date +"%c || Serie Titulo original || $serie_original || $serie_TMDB ||" >> LogsJM/APIRename.txt
echo "|| Serie Titulo original || $serie_original || $serie_TMDB ||"

#### temporada y episodio - ambos formatos####
formato_serie=$(echo "$name" | awk -F"/" '{print $NF}' | grep -e 'S[0-9][0-9]E[0-9][0-9]' -e  '- Temporada' -e '[0-9][x-X][0-9][0-9]' -e '[0-9][0-9][x-X][0-9][0-9]')

date +"%c || Formato serie= $formato_serie " >> LogsJM/APIRename.txt
echo "|| Formato serie= $formato_serie" 



if [[ -z $formato_serie ]]
	then
           season=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="(Cap|])" '{print $3}' |  awk '{print substr($0,2,1)}')     #.103
	   episode=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS="(Cap|])" '{print $3}' |  awk '{print substr($0,3,2)}')    #.103
           season_episode=S0"$season"E"$episode"
	   date +"%c mal $season_episode" >> LogsJM/APIRename.txt

        else
		if [[ $formato_serie ==  *[0-9][xX][0-9][0-9]* ]]
	          then
                        1x01
			date +"%c || Camino XxXX ||" >> LogsJM/APIRename.txt
		  else
			S01E01
			date +"%c || Camino SXXEXX ||" >> LogsJM/APIRename.txt
		fi
fi


pixels=$(mediainfo echo "$name" | grep -e ^Height -e ^Original | awk -F":" '{print $2}'  | awk -F"pixels" '{print $1}' | sed s/\ //g | sed -n 1p)
formato=$(mediainfo echo "$name" | grep -e ^Height -e ^Original | awk -F":" '{print $2}'  | awk -F"pixels" '{print $1}' | sed s/\ //g | sed -n 2p)


season=01
#episode=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS=".mkv" '{print $1}' |  awk -v FS="\ S01E" '{print $2}')
episode=$(echo "$name" | awk -F "/" '{print $NF}' | awk -v FS=".mkv" '{print $1}' | awk -v FS="S01E" '{print $2}')



titulo_ep_nuevo=$(curl -s "https://api.themoviedb.org/3/tv/$id_TMDB/season/$season/episode/$episode?api_key=2c0b5982e078e255ed5be3bba4c3064b&language=es" | jq -r '.name')
ext=$(echo "$name" | awk -F"/" '{print $NF}'); ext=${ext: -3}

#FILE=""$path""$serie_TMDB" ("$date_TMDB") - "$season_episode" - "$titulo_ep_nuevo" ("$pixels"p Blu-ray)."$ext"" 
FILE=""$path"S"$season"E"$episode" - "$titulo_ep_nuevo" ("$pixels"p "$formato")."$ext"" 


echo "|| Renombrando || $FILE ||"
date +"%c || Renombrando || $FILE ||" >> LogsJM/APIRename.txt


MOVE

rm ttt.txt

}

 
##### MAIN #####

while getopts "e:s:p:h:m" option
do
  case $option in
    s) carpeta=("$OPTARG");opt=0;date +"%c || -s Carpeta seleccionada || $OPTARG ||" >> LogsJM/APIRename.txt ;;
    p) pelicula=("$OPTARG");opt=1;date +"%c || -p Pelicula seleccionada || $OPTARG ||" >> LogsJM/APIRename.txt ;;
    e) episodio=("$OPTARG");opt=2;date +"%c || -e Episodio seleccionado || $OPTARG ||" >> LogsJM/APIRename.txt ;;
    m) monitor=1;date +"%c || -m Monitor seleccionado ||" >> LogsJM/APIRename.txt ;;
    *)  echo "Usar:";
	echo "  -e Episodios sueltos (Ubicación)";
	echo "  -s Serie (Ubicacion y palabras busqueda, hay que pasar antes el filtro -e)"; 
	echo "  -p Peliculas (Ubicación)";
	echo "  -m Script Monitor";;
  esac
done

##

if [[ $opt == 0 ]]
        then
		busqueda=$(echo "$@" | awk -v FS="$carpeta" '{print $2}' |   sed 's/\ /\*/g' | sed 's/$/*/g')
		echo "$busqueda"
		date +"%c || Busqueda episodios || $busqueda ||" >> LogsJM/APIRename.txt 
		echo  "|| Busqueda episodios || $busqueda ||" 
		find "$carpeta" -maxdepth 1 -iname "$busqueda" | while read -r name ### $name del episodio completo
			do
				PATH_FILE
				Serie
			done
		GET http://192.168.1.44:32400/library/sections/1/refresh?X-Plex-Token=vNPXH9_dPaA46GFyTCgP  ## Series
		   
fi


##

if [[ $opt == 1 ]]
        then
	   find "$pelicula" -name "*.avi" -o -name "*.mkv" -o -name "*.mp4" | while read -r name ### $name de la pelicula
              do 
                 date +"%c || Fichero || $name ||" >> LogsJM/APIRename.txt
		 echo  "|| Fichero || $name ||" 		 
		 nombre_TMDB=$(echo "$name" | awk -F"/" '{print $NF}' | sed 's/\.\|\[\|\_\|(\|)/\ /g' | awk -v FS="(\ [0-9][0-9][0-9][0-9]\ )" '{print $1}' | awk -F"4K" '{print $1}' | awk -F"BD" '{print $1}' |  awk -F"MicroHD" '{print $1}' | awk -F"DVD" '{print $1}' | awk -F"M1080" '{print $1}' | sed 's/\ /+/g')
		 CHECK
		 PATH_FILE
		 Pelicula
		 if [[  $monitor = 1 ]]
                    then
		       MONITOR Expansion_2/Varios/
		 fi
               done
	    GET http://192.168.1.44:32400/library/sections/2/refresh?X-Plex-Token=vNPXH9_dPaA46GFyTCgP  ## Varios
fi

##

if [[ $opt == 2 ]]
        then
	    find "$episodio" -name "*.avi" -o -name "*.mkv" -o -name "*.mp4" | while read -r name    ### Episodio
               do 
                 date +"%c || Fichero || $name ||" >> LogsJM/APIRename.txt
		 echo  "|| Fichero || $name ||" 
		 nombre_TMDB=$(echo "$name" | awk -F"/" '{print $NF}' | sed s'/\./\ /g' | awk -v FS="(\([0-9][0-9][0-9][0-9]\))" '{print $1}' | awk -v FS="(S[0-9][0-9]E[0-9][0-9])" '{print $1}' | awk -F"- Temporada" '{print $1}' | awk -v FS="([0-9][x-X][0-9][0-9])" '{print $1}' | awk -v FS="([0-9][0-9][x-X][0-9][0-9])" '{print $1}'  | sed 's/\ /+/g')
                 #CHECK         
		 PATH_FILE
		 Episodio
		 if [[  $monitor = 1 ]]
                    then
		       MONITOR Expansion_2/Series/
		 fi
	       done
	   GET http://192.168.1.44:32400/library/sections/1/refresh?X-Plex-Token=vNPXH9_dPaA46GFyTCgP  ## Series
fi

date +"%c || Proceso ejecutado con exito ||" >> LogsJM/APIRename.txt
echo  "|| Proceso ejecutado con exito ||" 
echo >> LogsJM/APIRename.txt
