import shlex
from enum import Enum

from win32com.shell import shell
from win32com.propsys import propsys, pscon
import pythoncom


def cmd_escape(x: str):
    # return x.replace('\\', '\\\\').replace('"', '\\"').replace(' ', '\\ ')
    # return x.replace('"', '\\"').replace(' ', '\\ ')
    return '"'+x.replace('"', '\\"')+'"'


class JumpListItemType(Enum):
    UNKNOWN = 0
    LINK = 1
    DESTINATION = 2
    SEPARATOR = 3


class AbstractJumpListItem(object):
    def __init__(self):
        self.type = JumpListItemType.UNKNOWN
        pass

    def get_item(self):
        raise NotImplemented


class JumpListItemLink(AbstractJumpListItem):
    def __init__(self, title, command=None, command_args=None, icon=None, icon_index=0):
        super().__init__()
        self.type = JumpListItemType.LINK
        if command_args is None:
            command_args = []
        self.title = title
        self.command = command
        self.command_args = command_args
        self.icon = icon
        self.icon_index = icon_index
        self._working_directory = None

    @property
    def working_directory(self):
        return self._working_directory

    @working_directory.setter
    def working_directory(self, path):
        self._working_directory = path

    def get_link(self):
        link = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

        link.SetPath(self.command)
        if self.command_args:
            args = ' '.join(map(cmd_escape, self.command_args))
            link.SetArguments(args)

        if self._working_directory:
            link.SetWorkingDirectory(self._working_directory)

        if self.icon:
            link.SetIconLocation(self.icon, self.icon_index)

        properties = link.QueryInterface(propsys.IID_IPropertyStore)
        properties.SetValue(pscon.PKEY_Title, propsys.PROPVARIANTType(self.title))
        properties.Commit()
        return link


class JumpListItemSeparator(AbstractJumpListItem):
    def __init__(self):
        super().__init__()
        self.type = JumpListItemType.SEPARATOR

    def get_link(self):
        link = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

        properties = link.QueryInterface(propsys.IID_IPropertyStore)
        properties.SetValue(pscon.PKEY_AppUserModel_IsDestListSeparator, propsys.PROPVARIANTType(True))
        properties.Commit()
        return link
