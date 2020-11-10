from bs4 import BeautifulSoup 
import csv, time, requests

class Constituency:
  def __init__(self):
    self.constit_name = None
    self.constit_num = None
    self.lCand = None
    self.lParty = None
    self.tCand = None
    self.tParty = None
    self.curMargin = None
    self.prevWParty = None
    self.prevMargin = None

  def test_func(self):
    print("Hello, the constituency's name is " + self.constit_name)
    
soups = [None]*25
constituencies = []
for cnt in range(1, 26):
    pageURL = "https://results.eci.gov.in/ACTRENDS2020/statewiseS04" + str(cnt) + ".htm"
    if (cnt!=1):
        time.sleep(2)
    results_html_page = requests.get(pageURL)
    soups[cnt-1] = BeautifulSoup(results_html_page.text, 'html.parser')
    
for cnt in range(1,26):
    relevant_table = soups[cnt-1].find('tbody', attrs = {'id':'ElectionResult'})

    for row in relevant_table.findAll('tr', style=True, recursive=False):
        #print ( row["style"] )
        if row["style"] == "font-size:12px;":
            #print (cnt)
            col = row.findAll('td', recursive=False)
            tempConst = Constituency()
            #print (col[0].text)
            #print (col[1].text)
            #print (col[5].find("table").find("tbody").find("tr").find("td", recursive=False).text )
            tempConst.constit_name = col[0].text
            tempConst.constit_num = col[1].text
            tempConst.lCand = col[2].text
            #tempConst.lParty = col[3].text
            tempConst.lParty = col[3].find("table").find("tbody").find("tr").find("td", recursive=False).text
            tempConst.tCand = col[4].text
            #tempConst.tParty = col[5].text
            tempConst.tParty = col[5].find("table").find("tbody").find("tr").find("td", recursive=False).text
            tempConst.curMargin = col[6].text
            tempConst.prevWParty = col[9].text
            tempConst.prevMargin = col[10].text
            constituencies.append(tempConst)


print ("Number of Constituencies fetched = " + str(len(constituencies)) )

filename = 'E://Android_Development//bihar_result.csv'
with open(filename, 'w', newline='') as f: 
    w = csv.writer(f)
    w.writerow(['Constituency Name','Constituency Number','Leading Candidate', 'Leading Party', 'Trailing Cand', 'Trailing Party', 'Current Margin','Previous Winning Party', 'Previous Margin'])
    for c_obj in constituencies:
        constituency_iterable = [c_obj.constit_name, c_obj.constit_num, c_obj.lCand, c_obj.lParty, c_obj.tCand, c_obj.tParty, c_obj.curMargin, c_obj.prevWParty, c_obj.prevMargin]
        w.writerow(constituency_iterable) 
