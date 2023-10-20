# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from .sourceitem import SourceItem

@export
class SourceList:
    """
    SoundTouch device SourceList configuration object.
       
    This class contains the attributes and sub-items that represent the
    sources configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._items = []
        
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            if (root.tag == 'sources'):
                for item in root:
                    self.append(SourceItem(root=item))
            else:
                source_item_list = root.find('sources')
                if source_item_list:
                    for item in root.find('sources'):
                        self.append(SourceItem(root=item))


    def __getitem__(self, key) -> SourceItem:
        if isinstance(key, str):
            for item in self:
                if item.Source == key:
                    return item
        else:
            return self._items[key]


    def __iter__(self) -> Iterator:
        return iter(self._items)


    def __len__(self) -> int:
        return len(self._items)


    def append(self, value: SourceItem):
        """
        Append a new `SourceItem` item to the list.
        
        Args:
            value:
                The `SourceItem` object to append.
        """
        self._items.append(value)


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SourceList:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:SourceItem
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
