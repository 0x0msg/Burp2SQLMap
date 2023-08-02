from burp import IBurpExtender, IContextMenuFactory, IContextMenuInvocation
from javax.swing import JMenuItem

try:
    from urllib import request as urllib_request
except ImportError:
    # For Jython, fall back to Java URLConnection
    from java.net import URL, HttpURLConnection

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("Burp2SQLMap")

        # Register ourselves as a context menu factory for Proxy and Repeater
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        menu_items = []
        context = invocation.getInvocationContext()
        if context == IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST or context == IContextMenuInvocation.CONTEXT_MESSAGE_VIEWER_REQUEST:
            menu_item = JMenuItem("Send Request to Local Server", actionPerformed=lambda x, inv=invocation: self.send_request_to_server(inv))
            menu_items.append(menu_item)
        return menu_items

    def send_request_to_server(self, invocation):
        http_traffic = invocation.getSelectedMessages()
        if not http_traffic:
            return

        request = http_traffic[0].getRequest()
        request_data = self._helpers.bytesToString(request)
        self.send_http_request_to_server(request_data)

    def send_http_request_to_server(self, raw_request):
        url = "http://localhost:8888"  # Change the server address and port to match the running server
        try:
            if 'urllib_request' in globals():
                # Use urllib (for CPython)
                req = urllib_request.Request(url, data=raw_request.encode('utf-8'))
                response = urllib_request.urlopen(req)
                print("Server Response:")
                print(response.read().decode('utf-8'))
            else:
                # Use Java URLConnection (for Jython)
                java_url = URL(url)
                conn = java_url.openConnection()
                conn.setRequestMethod("POST")
                conn.setDoOutput(True)
                conn.getOutputStream().write(raw_request.encode('utf-8'))

                response = conn.getInputStream()
                print("Server Response:")
                print(response.read().decode('utf-8'))
        except Exception as e:
            print("Error sending request to server:", e)

if __name__ == '__main__':
    pass  # Burp Suite will execute the code when loaded as an extension
