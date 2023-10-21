# external package imports.
from threading import Thread
from websocket import WebSocketApp
from xml.etree import ElementTree as xmltree

# our package imports.
from bosesoundtouchapi.bstutils import export
from bosesoundtouchapi.soundtouchdevice import SoundTouchDevice
from bosesoundtouchapi.soundtouchnotifycategorys import SoundTouchNotifyCategorys


# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SILevel, SISession
from smartinspectpython.sisourceid import SISourceId
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)


class _SoundTouchWebSocketThread(Thread):
    """
    A small utility class wrapping the WebSocketApp::run_forever() method in an
    extra Thread.
    """

    def __init__(self, ws:WebSocketApp) -> None:
        """
        Args:
            ws (WebSocketApp):
                A websocket client, that receives notifications from the Bose device.
        """
        super().__init__()
        self.wsocket = ws


    def run(self) -> None:
        """
        Starts the event loop for WebSocket framework.
        """
        self.wsocket.run_forever()


@export
class SoundTouchWebSocket:
    """
    A wrapper class to use the notification system provided by SoundTouch devices.

    In order to react to a message, there is a listener system. You can add
    functions as listener objects. The connection url is defined as follows:
    'ws://{Host}:{Port}/'.  Port 8080 is used by default.

    This class can be used in two ways. First, the object can open a
    connection through the `StartNotification` method and secondly, the with-statement
    can be used to create an instance.
    
    You must first check the device capabilities prior to using the support notifications
    functionality; if the device does not support it, then it's not going to work!
    To do this, fetch the device's capabilities and check for a `IsWebSocketApiProxyCapable = True`
    value.  If true, then the device supports sending notifications; if false, it does not.
    
    For more information and code samples refer to `bosesoundtouchapi.soundtouchclient.GetCapabilities`
    method.

    <details>
        <summary>Sample Code</summary>
    ```python
    .. include:: ../../docs/include/samplecode/SoundTouchWebSocket/_ClassInit.py
    ```
    </details>
    """
    
    def __init__(self, device:SoundTouchDevice, port:int=8080) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            device (SoundTouchDevice):
                A SoundTouchDevice instance containing the host ip-address.
            port (int):
                The port the Bose WebAPI socket is posting notifications on.  
                Default is 8080.
        
        """
        self._CachedListeners:dict = {}
        self._Device:SoundTouchDevice = device
        self._Port:int = int(port)
        self._Thread = None
        self._WebsocketClient:WebSocketApp = None


    def __enter__(self) -> 'SoundTouchWebSocket':
        self.StartNotification()
        return self


    def __exit__(self, etype, value, traceback) -> None:
        self.StopNotification()


    @property
    def Device(self) -> SoundTouchDevice:
        """ A SoundTouchDevice instance containing the host ip-address. """
        return self._Device


    def _OnError(self, wsClient, error):
        """
        Event raised by the web socket event listener when a socket error has occurred.
        
        Args:
            wsClient (WebSocketApp):
                Event sender.
            error (bytes):
                Event argument, in the form of socket error details.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogSource(SILevel.Verbose, "SoundTouch web socket event listener OnError event: '%s' - %s" % ("error", error), error, SISourceId.Xml)

        self.NotifyListeners('error', error)


    def _OnPacket(self, wsClient, message:bytes):
        """
        Event raised by the web socket event listener when a packet is received from
        the monitored Bose SoundTouch device.
        
        Args:
            wsClient (WebSocketApp):
                Event sender.
            message (bytes):
                Event argument, in the form of an xml-formatted message.
        """
        root = xmltree.fromstring(message)
        
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogSource(SILevel.Verbose, "SoundTouch web socket event listener OnPacket event: '%s' - %s" % (root.tag, message), message, SISourceId.Xml)

        # the SoundTouch device can send different types of notification packets, which
        # need to be processed differently.
        # Examples: "userActivityUpdate", "updates", etc.

        # is this an "updates" packet?
        if root.tag == 'updates':
            
            # "updates" messages will consist of child nodes that denote the type of update; like so:
            # <updates deviceID="9070658C9D4A">
            #   <connectionStateUpdated state="NETWORK_WIFI_CONNECTED" up="true" signal="GOOD_SIGNAL" />
            # </updates>

            # process all update child nodes (there could be multiple).
            for update in root:
                if (update.tag):
                    self.NotifyListeners(update.tag, update)

        else:

            # for all other messages, we will just process the root node; like so:
            # <SoundTouchSdkInfo serverVersion="4" serverBuild="trunk r46330 v4 epdbuild hepdswbld04" />
            # <userActivityUpdate deviceID="9070658C9D4A" />

            # process the root node (there is only one).
            self.NotifyListeners(root.tag, root)


    def AddListener(self, category:SoundTouchNotifyCategorys, listener) -> bool:
        """
        Adds a listener provided here to the given category.

        Since there are different types of events, the category-string can be used
        to add a listener to a specific notification category. The listener must take
        only one argument: xml.etree.ElementTree.Element.

        Args:
            category (SoundTouchNotifyCategorys):
                The category this listener should be added to.  
                Use one of the pre-defined SoundTouchNotifyCategorys values to receive 
                updates for that category (e.g. "volumeUpdated", "nowPlayingUpdated", etc).
                Use SoundTouchNotifyCategorys.Error to receive notifications for WebSocket errors.  
                Use SoundTouchNotifyCategorys.ALL to receive notifications for any type of update event.
            listener (object):
                A simple listener method which takes the XML-Element as a passed argument.
        
        Returns:
            True if the listener was added successfully; otherwise, False.
            
        Please refer to the `bosesoundtouchapi.soundtouchnotifycategories.SoundTouchNotifyCategorys`
        class for more details on what events are raised and why / when they happen.
        """
        if (not category) or (not listener):
            return False
        
        # convert category argument to string.
        category = SoundTouchNotifyCategorys.toString(category)

        # add the listener to the category list of listeners.
        if category in self._CachedListeners:
            self._CachedListeners[category].append(listener)
        else:
            self._CachedListeners[category] = [listener]
        return True


    def GetListenerGroup(self, category:str) -> list: # list[function]
        """
        Searches for a specific category in the registered ones.

        This method is a convenient method to return all listeners that were added
        to a specific context.

        Args:
            category (str):
                The category, which has to be one of the SoundTouchNotifyCategorys values.
                    
        Returns:
            A list containing all listeners linked to the given category.
        """
        if not category:
            return []
        return self._CachedListeners[category]


    def NotifyListeners(self, category: str, event: xmltree.Element) -> None:
        """
        Notifies all listeners that were stored in the given context.

        The name of each context is defined to be the tag element of the update
        XML-Element.

        Args:
            category (str):
                The category of which listeners should be notified from.
            event (xmltree.Element):
                The event represents an XML-Element with event.tag == category.
        """
        category = str(category)

        # are listeners defined for ANY category?  if so, then notify them.
        if ('*' in self._CachedListeners):
            for listener in self.GetListenerGroup('*'):
                if (event != None):
                    eventEncoded = xmltree.tostring(event, encoding="unicode")
                    _logsi.LogSource(SILevel.Verbose, "SoundTouch device status update NOTIFY (*): '%s'" % (category), eventEncoded, SISourceId.Xml)
                listener(event)
            return
            
        # are listeners defined for the specified category?  if so, then notify them.
        if (category in self._CachedListeners):
            for listener in self.GetListenerGroup(category):
                if (event != None):
                    eventEncoded = xmltree.tostring(event, encoding="unicode")
                    _logsi.LogSource(SILevel.Verbose, "SoundTouch device status update NOTIFY: '%s'" % (category), eventEncoded, SISourceId.Xml)
                listener(event)
            return
        
        return


    def RemoveListener(self, category:SoundTouchNotifyCategorys, listener) -> bool:
        """
        Removes a listener from the given category.

        Args:
            category (str):
                The category this listener should be removed from.  
                Use one of the pre-defined SoundTouchNotifyCategorys values to receive 
                updates for that category (e.g. "volumeUpdated", "nowPlayingUpdated", etc).
            listener (object):
                A simple listener method which takes the XML-Element as a passed argument.
        
        Returns:
            True if the listener was removed successfully; otherwise, False.
        """
        if not category or not listener: 
            return False
        
        # convert category argument to string.
        category = SoundTouchNotifyCategorys.toString(category)

        # remove the listener from the category list of listeners.
        if category not in self._CachedListeners: 
            listeners: list = self._CachedListeners[category]
            for ls in listeners:
                if ls == listener:
                    listeners.remove(ls)
                    return True
        return False


    def StartNotification(self) -> None:
        """
        Creates and starts a web socket event loop thread that listens for notifications 
        from the SoundTouch device.
        
        Only one web socket event loop thread will be started for the device.
        """
        if self._WebsocketClient is None:

            wsUrl = 'ws://%s:%d/' % (self._Device.Host, self._Port)
            _logsi.LogVerbose("Creating SoundTouch web socket client (%s)." % (wsUrl))
            
            self._WebsocketClient = WebSocketApp(
                    wsUrl,
                    on_message=self._OnPacket,
                    on_error=self._OnError,
                    subprotocols=['gabbo']
            )
            
            _logsi.LogVerbose("Starting SoundTouch web socket event listener thread.")
            self._Thread = _SoundTouchWebSocketThread(self._WebsocketClient)
            self._Thread.name = 'SoundTouchWebSocketEventThread'
            self._Thread.start()


    def StopNotification(self) -> None:
        """
        Stops the web socket event loop thread, if one was previously started using 
        the `StartNotification` method.
        
        This method does nothing if the event loop thread was not started.
        """
        if self._WebsocketClient != None:
            _logsi.LogVerbose("Stopping SoundTouch web socket event listener thread.")
            self._WebsocketClient.close()
            self._WebsocketClient = None
