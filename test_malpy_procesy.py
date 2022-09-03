#''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
#''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
#''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

from concurrent.futures import process
import string
import random
import time
import datetime
import multiprocessing as mp
import os



def generuj_slowo(dlugosc_slowa):
    return ''.join( random.choice( string.ascii_letters ) for _ in range( dlugosc_slowa ))  

def malpa_proces(nazwa, ilosc_losowan):    
    ilosc_trafien = 0

    czas_staru = time.time()
    print( nazwa, ': zaczął: ', datetime.datetime.fromtimestamp(czas_staru) )
    
    for i in range( 1, ilosc_losowan + 1 ):
        slowo_losowanie = generuj_slowo( len( slowo_klucz ) )

        #print(nazwa, ' iteracja: ', i, ' wylosowano: ', slowo_losowanie, ' lower: ', slowo_losowanie.lower())
        if slowo_losowanie.lower() == slowo_klucz.lower():
            ilosc_trafien += 1
            print( nazwa,
                    ' Trafienia czas: ', datetime.datetime.fromtimestamp(time.time()), 
                    ' iteracja: ', i, 
                    ' numer trafienia: ', ilosc_trafien,
                    ' słowo: ', slowo_losowanie)   

        time.sleep(0)

    czas_konca = time.time()
    print( nazwa,
        ' Start: ', datetime.datetime.fromtimestamp(czas_staru), 
        ' koniec:', datetime.datetime.fromtimestamp(czas_konca), 
        ' ilość trafień: ', ilosc_trafien,
        ' Czas trwanie: ', czas_konca - czas_staru )



slowo_klucz = 'goofyx'
ilosc_malp = 8
ilosc_losowan = 120000000
#ilosc_trafien = 0
malpy = []

if __name__ == '__main__':    
    program_start = time.time()
    print( 'Program START: ', datetime.datetime.fromtimestamp( program_start ) )
    
    for proces_id in range( 1, ilosc_malp + 1 ):   
        nazwa_watku = 'Proces_' + str(proces_id)
        malpa = mp.Process( target=malpa_proces, args=(nazwa_watku,ilosc_losowan) )
        malpy.append( malpa )
        malpa.start()

    for malpa in malpy:
        malpa.join()
    
    program_koniec = time.time()   
    print( ' Start: ', datetime.datetime.fromtimestamp(program_start), 
           ' koniec:', datetime.datetime.fromtimestamp(program_koniec), 
           ' Czas trwanie: ', program_koniec - program_start )

