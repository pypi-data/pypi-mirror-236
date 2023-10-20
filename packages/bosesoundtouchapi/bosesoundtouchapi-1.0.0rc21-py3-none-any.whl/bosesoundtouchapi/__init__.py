# include the README.md file for pdoc documentation generation.
"""
.. include:: ../README.md

_________________

<details>
  <summary>View Change Log</summary>
.. include:: ../CHANGELOG.md
</details>
"""

# our package imports.
from bosesoundtouchapi.soundtouchclient import SoundTouchClient
from bosesoundtouchapi.soundtouchdevice import SoundTouchDevice
from bosesoundtouchapi.soundtouchexception import SoundTouchException
from bosesoundtouchapi.soundtouchkeys import SoundTouchKeys
from bosesoundtouchapi.soundtouchmessage import SoundTouchMessage
from bosesoundtouchapi.soundtouchnotifycategorys import SoundTouchNotifyCategorys
from bosesoundtouchapi.soundtouchsources import SoundTouchSources

# all classes to import when "import *" is specified.
__all__ = [
    'SoundTouchClient',
    'SoundTouchDevice',
    'SoundTouchException',
    'SoundTouchKeys',
    'SoundTouchMessage',
    'SoundTouchNotifyCategorys',
    'SoundTouchSources',
]
