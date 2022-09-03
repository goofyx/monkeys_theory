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
import sys
import getopt

from rethinkdb import RethinkDB 
from rethinkdb.errors import RqlRuntimeError




def generuj_slowo(dlugosc_slowa):
    return ''.join( random.choice( string.ascii_letters ) for _ in range( dlugosc_slowa ))  

def timestamp_na_data(acctual_time):
    return datetime.datetime.fromtimestamp(acctual_time)

def wynik_do_bazy(slowo):
    monkeys_database = RethinkDB()
    monkeys_connection = monkeys_database.connect('192.168.200.181', 28015)
    try:
        monkeys_database.db("monkeys").table('wyniki').insert({ 'slowo_wylosowane': slowo }).run(monkeys_connection)

#r.table("user").insert({
#    "name": "Michel",
#    "age": 26
#}).run()

    except RqlRuntimeError as err:
        print(err.message)
    finally:
        monkeys_connection.close()



def malpa_proces(nazwa, ilosc_losowan):    
    ilosc_trafien = 0
    czas_trafienia = 0
    zapis_do_bazy = 1        

    czas_staru = time.time()
    print( nazwa, ': zaczął: ', timestamp_na_data(czas_staru) )
    
    for i in range( 1, ilosc_losowan + 1 ):
        slowo_losowanie = generuj_slowo( len( slowo_klucz ) )

        #print(nazwa, ' iteracja: ', i, ' wylosowano: ', slowo_losowanie, ' lower: ', slowo_losowanie.lower())
        if slowo_losowanie.lower() == slowo_klucz.lower():
        #if len(slowo_losowanie) > 1:
            ilosc_trafien += 1
            czas_trafienia = time.time()
            print( nazwa,
                    ' Trafienia czas: ', timestamp_na_data(czas_trafienia), 
                    ' iteracja: ', i, 
                    ' numer trafienia: ', ilosc_trafien,
                    ' słowo: ', slowo_losowanie)  
            
            #zapis do bazy
            if zapis_do_bazy == 1 :
                wynik_do_bazy(slowo_losowanie)      

        time.sleep(0)

    czas_konca = time.time()

    print( nazwa,
        ' Start: ', timestamp_na_data(czas_staru), 
        ' koniec:', timestamp_na_data(czas_konca), 
        ' ilość trafień: ', ilosc_trafien,
        ' Czas trwanie: ', czas_konca - czas_staru )



slowo_klucz = 'krzys'
ilosc_malp = 8
ilosc_losowan = 9999999999 #12000000
#ilosc_trafien = 0
malpy = []

if __name__ == '__main__':    
    program_start = time.time()
    print( 'Program START: ', timestamp_na_data( program_start ) )
    
    for proces_id in range( 1, ilosc_malp + 1 ):   
        nazwa_watku = 'Proces_' + str(proces_id)
        malpa = mp.Process( target=malpa_proces, args=(nazwa_watku,ilosc_losowan) )
        malpy.append( malpa )
        malpa.start()

    for malpa in malpy:
        malpa.join()
    
    program_koniec = time.time()   
    print( ' Start: ', timestamp_na_data(program_start), 
           ' koniec:', timestamp_na_data(program_koniec), 
           ' Czas trwanie: ', program_koniec - program_start )

