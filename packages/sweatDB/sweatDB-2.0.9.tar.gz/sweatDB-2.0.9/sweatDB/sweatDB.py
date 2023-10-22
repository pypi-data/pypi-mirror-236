import datetime
import os
class actions :
    version = "v2.1"
    e = os.path.isfile
    
    def create(db):
        if e(db):
            raise Exception("{db} already exists")
        else:
            open(db).write(f"DATABASE NAME : {db} TIME CREATED : {datetime.datetime.utcnow()} CREATED WITH https://github.com/0xsweat/sweatDB {version}\n")
            
    def delete(ttd,db,item=''):
        if e(name) != True:
            return f"Database : {name} doesn't exist"
        if ttd == "db":
            os.remove(db)
        elif item == '':
            raise Exception('No item specified')
            a = open(db, 'r').read().split("\n")
            open(db, 'w').write("".join([f"{x}\n" for x in a if x.startswith(f'{item} ') == False])[:-1])

    def add(db,name,value):
        if e(db):
            open(db, 'a').write(f'{name} {value}\n')
        else:
            raise Exception(f'Database {db} not found')

    def view(db,option='all',item='',start=1,end=0):
        if e(db) != True:
            raise Exception(f'Database {db} not found')
        elif option == "all":
            c = open(db, 'r').read()
            if start < end and start > 0:
                return ''.join(f'{x}\n' for x in c.split("\n")[start:end])
            else:
                return c
        elif option == "item":
            b = open(db, 'r').read().split("\n")
            for i in range(1,len(b)):
                if b[i].startswith(f'{item} '):
                    return(''.join([f'{x} ' for x in b[i].split(" ")[1:]])[:-1])
            raise Exception(f'{item} not present in {db}')
        elif option == "items":
            return(''.join([f'{x.split(" ")[0]}\n' for x in open(db, 'r').read().split('\n')[1:]])[:-2])
        elif option == "info":
            return(open(db, 'r').read().split("\n")[0])
        elif option == "itemcount":
            return(open(db, 'r').read().count("\n") - 1)

    def edit(db,item,value):
        if e(db) != True:
            return f'Database {db} does not exist'
        b = open(db, 'r').read().split("\n")
        for x in range(len(b)):
            if b[x].startswith(f'{item} '):
                b[x] = f"{item} {newvalue}"
        open(db, 'w').write("".join([f"{x}\n" for x in b])[:-1])
