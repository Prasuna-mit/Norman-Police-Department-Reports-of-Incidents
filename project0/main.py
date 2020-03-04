#importing files
import tempfile
import urllib
import PyPDF2
import urllib.request
import pandas as pd
import argparse
import sqlite3
from sqlite3 import Error


# import project0

# Download the data
def fetchincidents(url):
    # url = "http://normanpd.normanok.gov/filebrowser_download/657/2020-02-28%20Daily%20Incident%20Summary.pdf"
    data = urllib.request.urlopen(url).read()
    return data


# Extract Data
def extractincidents(data):
    fp = tempfile.TemporaryFile()
    fp.write(data)
    fp.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pdfReader.getNumPages()
    dataF = pd.DataFrame(columns=('date/time', 'inc_number', 'inc_location', 'nature', 'incident_ori'))
    for i in range(pdfReader.numPages):
        pages = pdfReader.getPage(i).extractText()
        # pages = Pages.replace('\n',',').split(',')
        if (i == 0):
            pages = pages.split('\n')
            pages = pages[:-2]
            pages = '\n'.join(pages)
            # print(pages)
            # first row removal
        pages = pages.replace(' \n', '_').split('\n')
        pages = pages[:-1]
        n = 5
        Final = [pages[j * n:(j + 1) * n] for j in range((len(pages) + n - 1) // n)]
        dfP = pd.DataFrame(Final, columns=dataF.columns)
        dataF = dataF.append(dfP, ignore_index=True)
    dataF = dataF[1:]
    dataF = dataF[:-1]
    return dataF


# Create Dataase
def createdb():
    # c = conn.cursor()
    sqlite3_conn = None
    try:
        sqlite3_conn = sqlite3.connect('normanpd.db')

        return sqlite3_conn
    except Error as err:
        print(err)
    if sqlite3_conn is not None:
        sqlite3_conn.close()

    c = sqlite3_conn.cursor()
    c.execute('''CREATE TABLE incidents (
    date/time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
    );''')
    sqlite3_conn.commit()


# Insert Data
def populatedb(sqlite3_conn, incidents):
    sqlite3_conn = sqlite3_conn
    # c = db.cursor()
    # c.execute('''CREATE TABLE incidents (
    # date/time TEXT,
    # incident_number TEXT,
    # incident_location TEXT,
    # nature TEXT,
    # incident_ori TEXT
    # );''')
    # db.commit()

    incidents.to_sql('incidents', sqlite3_conn, if_exists='replace', index=False)


# Print Status
def status(db):
    # sqlite3_conn = sqlite3.connect('normanpd.db')
    results = pd.read_sql_query("select nature, count(*) as count from incidents group by nature", db)
    #results= results["nature"] + results["Count(*)"]
    results["period"] = results["nature"] + "|" + results["count"].astype(str)
    #return results["period"]
    print(results)


def main(url):
    # Download data
    data = fetchincidents(url)

    # Extract Data
    incidents = extractincidents(data)

    # Create Dataase
    db = createdb()

    # Insert Data
    populatedb(db, incidents)

    # Print Status
    status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="The arrest summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
