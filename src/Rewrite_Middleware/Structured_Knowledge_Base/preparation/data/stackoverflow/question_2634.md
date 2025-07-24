# Using PyQt for Front End Web Development
[Link to question](https://stackoverflow.com/questions/43765286/using-pyqt-for-front-end-web-development)
**Creation Date:** 1493828257
**Score:** 17
**Tags:** python, python-2.7, qt, pyqt, pyqt4
## Question Body
<p>I have written a single-script (i.e. <em>full-stack</em>) GUI in PyQT which queries an SQL database, performs some functions with the query outputs and then displays these outputs graphically in a <code>QtGui.QApplication</code>. However, I have decided that I would like to convert this into a Web application that I can host on a local server. </p>

<p>Running the code in <a href="https://wiki.python.org/moin/PyQt/Embedding%20Widgets%20in%20Web%20Pages" rel="noreferrer">this</a> tutorial produces something similar to what I am after but it runs in the Python launcher rather than on a web page. What I want to do - to prevent me from having to rewrite all of the graphical widgets in another web-based framework - is to separate the script into a back-end which deals with querying the database and using the query results and a front-end written with PyQt and HTML (as in the linked tutorial) containing PyQt widgets <strong>embedded</strong> into an HTML script which I can run as a website. Is this possible?</p>

<p>If it is possible to do this, how would I go about writing it (for instance, how would you change the code in the linked tutorial) such that it can be run from a browser/hosted on a server rather than run as an application? There may be some technical blunders in this question as my understanding of web development is limited. Any help will be appreciated.</p>

<p>For ease of answering, here is the joined code from the linked tutorial:</p>

<pre><code>import sys
from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

html = \
"""&lt;html&gt;
&lt;head&gt;
&lt;title&gt;Python Web Plugin Test&lt;/title&gt;
&lt;/head&gt;

&lt;body&gt;
&lt;h1&gt;Python Web Plugin Test&lt;/h1&gt;
&lt;object type="x-pyqt/widget" width="200" height="200"&gt;&lt;/object&gt;
&lt;p&gt;This is a Web plugin written in Python.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
"""

class WebWidget(QWidget):

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.black)
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
        painter.setBrush(Qt.red)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.width()/4, self.height()/4,
                         self.width()/2, self.height()/2)
        painter.end()

    def sizeHint(self):
        return QSize(100, 100)

class WebPluginFactory(QWebPluginFactory):

    def __init__(self, parent = None):
        QWebPluginFactory.__init__(self, parent)

    def create(self, mimeType, url, names, values):
        if mimeType == "x-pyqt/widget":
            return WebWidget()

    def plugins(self):
        plugin = QWebPluginFactory.Plugin()
        plugin.name = "PyQt Widget"
        plugin.description = "An example Web plugin written with PyQt."
        mimeType = QWebPluginFactory.MimeType()
        mimeType.name = "x-pyqt/widget"
        mimeType.description = "PyQt widget"
        mimeType.fileExtensions = []
        plugin.mimeTypes = [mimeType]
        print "plugins"
        return [plugin]

if __name__ == "__main__":

    app = QApplication(sys.argv)
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)
    view = QWebView()
    factory = WebPluginFactory()
    view.page().setPluginFactory(factory)
    view.setHtml(html)
    view.show()
    sys.exit(app.exec_())
</code></pre>

