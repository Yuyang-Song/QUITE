# How to remove nested if/else statements when accounting for Error handling
[Link to question](https://stackoverflow.com/questions/32253281/how-to-remove-nested-if-else-statements-when-accounting-for-error-handling)
**Creation Date:** 1440688619
**Score:** 0
**Tags:** python, xml, api, xslt, flask-sqlalchemy
## Question Body
<p>Howdie do,</p>

<p>So I have this API that does the following:</p>

<p>1) It receives a XML request. It first parses that request to ensure the request is in the correct format.</p>

<p>2) If the XML is in the correct format, it checks to ensure that the correct user is authenicating.</p>

<p>3) If authenication is successful, it then retreives a URI from a database that the API will send a get request to.</p>

<p>4) If the response is successful, meaning it's a XML reply, it will use XSLT to transform the request into a format</p>

<p>5) It then adds the request to the database and returns the transformed XML to the user that queried the API</p>

<p>I have error handling involved at each step, but the issue is, I've had to nest 5 if else statements to accomplish this.</p>

<p>I know there has to be a better way to rewrite this error handling logic without so many nested if statements, but I'm not sure how. The subsequent steps rely on the previous to ensure that if any error occurs, it's returned properly to the user.</p>

<p>Below is my main Flask-API that I've created. The second file is a module that I've created which does a lot of the error processing. Those functions return a state(True/False) and the response to the main Flask-API.</p>

<p>Can someone give me some ideas on how to rewrite this API without the nesting? The API works 100% and does what it should for catching errors, but I just know there's a better way</p>

<p>Main API:</p>

<pre><code>@dbConnect.app.route('/services/tracking/getShipmentStatus', methods=['POST'])
def parsexml2():
    parseStatus, returnValues = func.parseNWRequest(request.data, 'SS')

    if parseStatus:
        authStatus, authResponse = func.checkAuthorization(returnValues['bu'], request.headers['Authorization'], 'SS')

        if authStatus:
            getURIStatus, uriResponse = func.getURI('SS')
            if getURIStatus:
                search = {'bu': returnValues['bu'], 'starttime': returnValues['start'], 'endtime': returnValues['end'],
                          'requestid': returnValues['requestid'], 'pagesize': returnValues['page']}

                responseStatus, depascoResponse = func.sendDepascoRequest(uriResponse, search, 'SS')

                if responseStatus:
                    nakedResponse = func.transformXML(depascoResponse.content, 'transformTracking.xsl')

                    # Write Request to db
                    file_name = 'WS_SS_' + returnValues['bu']
                    request_file_size = request.headers['Content-Length']
                    if func.addToDb(file_name, 'text/xml', 'SS.Request', returnValues['bu'], 'Y', request.data,
                                    request_file_size) or func.addToDb(file_name, 'text/xml', 'SS.Result',
                                                                       returnValues['bu'], 'Y', nakedResponse):
                        pass

                    return Response(nakedResponse, mimetype='text/xml')
                else:
                    return Response(depascoResponse, mimetype='text/xml')
            else:
                return Response(uriResponse, mimetype='text/xml')
        else:
            return Response(authResponse, mimetype='text/xml')
    else:
        return Response(returnValues, mimetype='text/xml')
</code></pre>

<p>Imported module functions:</p>

<pre><code>def transformXML(response, xsl):
    xml = ET.tostring(ET.fromstring(response))
    xslt = ET.XSLT(ET.parse(xsl))
    transformedXML = xslt(ET.XML(xml))

    return ET.tostring(transformedXML, pretty_print=True)

def addToDb(filename, mime, docType, customer_code, activeState, document_blob, filesize=None):
    try:
        response = dbConnect.Documents(file_name=filename, mime_type=mime, file_size=filesize, doc_type=docType,
                                       customer_code=customer_code, is_active=activeState, document_blob=document_blob)

        dbConnect.db.session.add(response)
        dbConnect.db.session.commit()
        dbConnect.db.session.close()
    except exc.SQLAlchemyError:
        return False
    else:
        return True

def generateXMLErrorResponse(errorMessage, api):
    E = ElementMaker()
    if api == 'SS':
        GETSHIPMENTSTATUSRESPONSE = E.getShipmentStatusResponse
        GETSHIPMENTSTATUSRESULT = E.getShipmentStatusResult
        OUTCOME = E.outcome
        RESULT = E.result
        ERROR = E.error

        xml_error = GETSHIPMENTSTATUSRESPONSE(
                    GETSHIPMENTSTATUSRESULT(
                        OUTCOME(
                            RESULT('Failure'),
                            ERROR(errorMessage)
                        )
                    )
        )
        return ET.tostring(xml_error, pretty_print=True)

    elif api == 'IS':
        GETINVENTORYSTATUSRESPONSE = E.getInventoryStatusResponse
        GETINVENTORYSTATUSRESULT = E.getInventoryStatusResult
        OUTCOME = E.outcome
        RESULT = E.result
        ERROR = E.error

        xml_error = GETINVENTORYSTATUSRESPONSE(
                    GETINVENTORYSTATUSRESULT(
                        OUTCOME(
                            RESULT('Failure'),
                            ERROR(errorMessage)
                        )
                    )
        )
        return ET.tostring(xml_error, pretty_print=True)

def checkAuthorization(bu, headers, status):
    error = 'Invalid clientCode for account type'
    auth_search = re.search('username="(.*?)"', headers)
    auth_user = auth_search.group(1)

    if auth_user.upper() != "ADMIN":
        if (str(bu).upper() != auth_user.upper()) and status == 'SS':
            return False, Response(generateXMLErrorResponse(error, status), mimetype='text/xml')
        elif (str(bu).upper() != auth_user.upper()) and status == 'IS':
            return False, Response(generateXMLErrorResponse(error, status), mimetype='text/xml')
        else:
            return True, 'User authenticated'
    else:
        return True, 'User authenticated'

def getURI(api):
    try:
        if api == 'SS':
            tracking = dbConnect.db.session.query(dbConnect.AppParam).\
                filter(dbConnect.AppParam.name == 'TRACKING_WEB_SERVICE_URI').first()
            return True, tracking.value
        elif api == 'IS':
            inventory = dbConnect.db.session.query(dbConnect.AppParam).\
                filter(dbConnect.AppParam.name == 'INVENTORY_WEB_SERVICE_URI').first()
            return True, inventory.value
    except exc.OperationalError:
        sendEmail()
        return False, generateXMLErrorResponse('Service Unavailable', api)

def sendEmail():
    msg = MIMEText('Unable to connect to DB')
    msg['Subject'] = "Database server down!"
    msg['From'] = ''
    msg['To'] = ''

    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    return True

def parseNWRequest(nwRequest, api):
    returnValues = {}
    if api == 'SS':
        try:
            xml = xmltodict.parse(nwRequest)
            returnValues['start'] = xml['getShipmentStatus']['getShipmentStatusRequest']['startTime']
            returnValues['end'] = xml['getShipmentStatus']['getShipmentStatusRequest']['endTime']
            if validateDate(returnValues['start'], returnValues['end']):
                returnValues['bu'] = xml['getShipmentStatus']['getShipmentStatusRequest']['clientCode']
                returnValues['page'] = xml['getShipmentStatus']['getShipmentStatusRequest']['pageSize']
                returnValues['requestid'] = xml['getShipmentStatus']['getShipmentStatusRequest']['requestId']
                return True, returnValues
            else:
                return False, generateXMLErrorResponse('Invalid startDate/endDate', api)
        except xmltodict.expat.ExpatError:
            return False, generateXMLErrorResponse('Invalid Formed XML', api)
    elif api == 'IS':
        try:
            xml = xmltodict.parse(request.data)
            returnValues['bu'] = xml['getInventoryStatus']['getInventoryStatusRequest']['clientCode']
            returnValues['facility'] = xml['getInventoryStatus']['getInventoryStatusRequest']['facility']
            return True, returnValues
        except xmltodict.expat.ExpatError:
            return False, generateXMLErrorResponse('Invalid Formed XML', api)

def validateDate(startDate, endDate):
    try:
        datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
        datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return False
    else:
        return True

def sendDepascoRequest(uri, search, api):
    auth=('', '')
    depascoResponse = requests.get(uri, auth=auth, params=search)

    try:
        depascoResponse.raise_for_status()
    except requests.exceptions.HTTPError:
        return False, generateXMLErrorResponse(depascoResponse.content, api)
    else:
        return True, requests.get(uri, auth=auth, params=search)
</code></pre>

<p>******* UPDATE **********
Thanks to the accepted answer, I removed all layers of the nested if statements. I have my functions just raise a custom exception which is handled in the main program.</p>

<pre><code>__author__ = 'jw1050'
from functions import parseNWRequest, checkAuthorization, getURI, sendDepascoRequest, transformXML, addToDb, APIError
from flask import request
from flask import Response
import dbConnect
import lxml.etree as ET
from sqlalchemy import text


@dbConnect.app.route('/services/inventory/getInventoryStatus', methods=['POST'])
def parsexml():
    try:
        returnValues = parseNWRequest(request.data, 'IS')

        checkAuthorization(returnValues['bu'], request.headers['Authorization'], 'IS')

        uri = getURI('IS')
        search = {'bu': returnValues['bu'], 'facility': returnValues['facility']}

        depascoResponse = sendDepascoRequest(uri, search, 'IS')

        s = text("Select sku, allocated from fgw_allocated_sku_count where client_code = :c and fulfillment_location = :t")
        result = dbConnect.db.engine.execute(s, c=returnValues['bu'], t=returnValues['facility']).fetchall()

        root = ET.fromstring(depascoResponse.content)

        for row in result:
            for element in root.iter('Item'):
                xmlSKU = element.find('SKU').text
                if xmlSKU == row[0]:
                    newQonOrder = int(element.find('QuantityOnOrder').text) + row[1]
                    element.find('QuantityOnOrder').text = str(newQonOrder)

                    newQAvailable = int(element.find('QuantityAvailable').text) - newQonOrder
                    element.find('QuantityAvailable').text = str(newQAvailable)

        nakedResponse = transformXML(ET.tostring(root), 'transformInventory.xsl')

        # Write Request to db
        file_name = 'WS_IS_' + returnValues['bu']
        request_file_size = request.headers['Content-Length']
        addToDb('SS', file_name, 'text/xml', 'IS.Req', returnValues['bu'], 'Y', request.data, request_file_size)
        addToDb('SS', file_name, 'text/xml', 'IS.Result', returnValues['bu'], 'Y', nakedResponse)

        return Response(nakedResponse, mimetype='text/xml')
    except APIError as error:
        return Response(error.errorResponse, mimetype='text/xml')


@dbConnect.app.route('/services/tracking/getShipmentStatus', methods=['POST'])
def parsexml2():
    try:
        returnValues = parseNWRequest(request.data, 'SS')

        checkAuthorization(returnValues['bu'], request.headers['Authorization'], 'SS')

        uri = getURI('SS')

        search = {'bu': returnValues['bu'], 'starttime': returnValues['start'], 'endtime': returnValues['end'],
                              'requestid': returnValues['requestid'], 'pagesize': returnValues['page']}
        depascoResponse = sendDepascoRequest(uri, search, 'SS')

        nakedResponse = transformXML(depascoResponse.content, 'transformTracking.xsl')

        # Write Request to db
        file_name = 'WS_SS_' + returnValues['bu']
        request_file_size = request.headers['Content-Length']
        addToDb('SS', file_name, 'text/xml', 'SS.Request', returnValues['bu'], 'Y', request.data, request_file_size)
        addToDb('SS', file_name, 'text/xml', 'SS.Result', returnValues['bu'], 'Y', nakedResponse)

        return Response(nakedResponse, mimetype='text/xml')
    except APIError as error:
        return Response(error.errorResponse, mimetype='text/xml')
if __name__ == '__main__':
    dbConnect.app.run(host='localhost', port=int("5010"), debug=True)
</code></pre>

<p>My custom exception class:</p>

<pre><code>class APIError(Exception):
    def __init__(self, errorResponse):
        self.errorResponse = errorResponse
</code></pre>

<p>An example of a function that raises my custom exception:</p>

<pre><code>def validateDate(startDate, endDate):
    try:
        datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
        datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise APIError(generateXMLErrorResponse('Invalid format for startDate/endDate', 'SS'))
    else:
        return True
</code></pre>

## Answers
### Answer ID: 32253813
<p>Another way is to raise exceptions and handle them. </p>

<pre><code>import myexceptions

try:
   # a complicated hunk of stuff that raises exceptions when 
   # things don't work out. The exceptions can be raised down
   # inside functions, if breaking this lump into functions
   # makes it easier to follow.
except MyExceptionA:
   return Response( ...) # appropriate response for error A
except MyExceptionB
    return Response( ...) # appropriate response for error B
except ...
</code></pre>

### Answer ID: 32253389
<p>I like to leave my methods ASAP, so in your case, it would look like:</p>

<pre><code>if !X:
   return...

if !Y:
   return...

if !Z:
   return...
</code></pre>

<p>though generally, I prefer</p>

<pre><code>if X:
   return...

if Y:
   return...
</code></pre>

