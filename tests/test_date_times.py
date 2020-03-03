#importing main function from project0
#testcase 1
import pytest 
from project0 import main
url = 'http://normanpd.normanok.gov/filebrowser_download/657/2020-02-28%20Daily%20Incident%20Summary.pdf'

def test_fetchincidents():

    var = main.fetchincidents(url)
    assert str(type(var)) == "<class 'bytes'>"




#testcase-2 for extractincidents
def test_extractincidents():
   # url = 'http://normanpd.normanok.gov/filebrowser_download/657/2020-02-28%20Daily%20Incident%#20Summary.pdf'
    var1  = main.fetchincidents(url)
    table = main.extractincidents(var1)
    assert len(table.columns) == 5 
    assert table.iloc[17][4] == "14005"


#Testcase-3 for database

def test_connection():
    var1  = main.fetchincidents(url)
    table = main.extractincidents(var1)
    db=main.createdb()
    # assert con = main.populate(db,table)
    assert db  is not None
    

#Test case-4
def test_populatedb():
    var2  = main.fetchincidents(url)
    table = main.extractincidents(var2)
    db=main.createdb()
    c = db.cursor()
    main.populatedb(db,table)
    check_data = "select count(*) from incidents"
    assert c.execute(check_data).fetchall()[0][0] == 373


#
def test_status():
    db=main.createdb()
    var3 = main.status(db)
    assert var3.iloc[0] == "Abdominal Pains/Problems|2"



