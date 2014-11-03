import webbrowser

global dataAsList

dataAsList = [['country','Female labor participation rate']]



from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus, quote   
import json

# This function retrieves life expectancy at birth (SP.DYN.LE00.IN)
# for three countries (USA, Brazil, Afghanistan) for the years
# 2000 and 2001
#
# It constructs this URL:
# http://api.worldbank.org/countries/usa%3Bbra%3Bafg/indicators/SP.DYN.LE00.IN?date=2000%3A2001&format=json
# You can copy/paste the above URL into a browser address bar and see the results there.
# They are reasonably readable.


def queryworldbank():
    global results

    # Construct data retrieval URL
    urlbase = "http://api.worldbank.org/countries/"
    countries = quote_plus("usa;bra;afg;chn;ind;zaf;mdg;dom;fra;gha;idn;ita;pak")
    query = "/indicators/SL.TLF.CACT.FE.ZS?"
    args = urlencode({'format': "json",
                      'date': "2010:2010",
                      'per_page' : 100})
    url = urlbase+countries+query+args
    #print('url',url)

    
    
    wbresult = urlopen(url).read()
    wbresult = wbresult.decode('utf-8')
    jsonresult = json.loads(wbresult)
    pageinfo = jsonresult[0]
    print("The World Bank query yielded {} results on {} page(s)".format(pageinfo['total'], pageinfo['pages']))
    results = jsonresult[1]

    
    return(results)
    
    




geochartHTMLpart1 = '''<html>
<head>
  <script type='text/javascript' src='https://www.google.com/jsapi'></script>
  <script type='text/javascript'>
   google.load('visualization', '1', {'packages': ['geomap']});
   google.setOnLoadCallback(drawMap);

    function drawMap() {
      var data = google.visualization.arrayToDataTable(
    '''

geocharHTMLpart3 = '''
        );

      var options = {};
      options['dataMode'] = 'regions';

      var container = document.getElementById('map_canvas');
      var geomap = new google.visualization.GeoMap(container);
      geomap.draw(data, options);
  };
  </script>
</head>

<body>
  <div id='map_canvas'></div>
</body>

</html>'''

def createData(additionalCountry, value):
    global dataAsList
    dataAsList.append([additionalCountry,value])
    #print(dataAsList)
    
    return(str(dataAsList))
          
def writeGeoChartHTML():
    global results
    global valueList
    global countryID
    global dataAsList
    of = open("geochart.html", 'w')

    dataList = []
    dataString1 = ''

    for i in range(len(results)):
        createData(countryID[i], valueList[i])
    #print(dataList)
    #print(dataString1)
    html = geochartHTMLpart1 + str(dataAsList) + geocharHTMLpart3
    #print(html)
    of.write(html)
    of.close()

def MakeChart():
    global results
    global valueList 
    global countryID
    valueList = []
    countryID = []
    queryworldbank()
    for i in range(len(results)):
        tempResult = results[i]
        valueList.append(tempResult['value'])
    #print(valueList)
    for i in range(len(results)):
        tempResult2 = results[i]
        tempResult3 = tempResult2['country']
        finalTempResult = tempResult3['id']
        countryID.append(finalTempResult)
    writeGeoChartHTML()
    showwebfile('geochart.html')
    
   
    
# path goes here

urlbase = "file:///Users/username/"

# E.g. showwebfile("geochart2.html")
def showwebfile(filename):
    webbrowser.open(urlbase + filename)








