from enum import Enum

from win32com.shell import shell
import pythoncom

from .jumplistitem import AbstractJumpListItem


class JumpListCategoryType(Enum):
    CUSTOM = 0
    TASK = 1
    RECENT = 2
    FREQUENT = 3


class JumpListCategory(object):
    def __init__(self):
        self.type = JumpListCategoryType.TASK
        self.items = []  # type: [AbstractJumpListItem]
        self._visible = False

    def get_category(self):
        collection = pythoncom.CoCreateInstance(
            shell.CLSID_EnumerableObjectCollection,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IObjectCollection)
        for i in self.items:
            collection.AddObject(i.get_link())

        return collection

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible

    def add_item(self, item):
        self.items.append(item)


class JumpListCustomCategory(JumpListCategory):
    def __init__(self, title):
        super().__init__()
        self.type = JumpListCategoryType.CUSTOM
        self.title = title


class JumpList(object):
    def __init__(self):
        self._jumplist = pythoncom.CoCreateInstance(
            shell.CLSID_DestinationList,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_ICustomDestinationList)

        self._tasks = JumpListCategory()
        self.custom = []  # type: [JumpListCustomCategory]

    @property
    def tasks(self) -> JumpListCategory:
        return self._tasks

    def update(self) -> None:
        self._jumplist.BeginList()

        if self._tasks.visible and self._tasks.items:
            self._jumplist.AddUserTasks(self._tasks.get_category())

        for category in self.custom:  # type: JumpListCustomCategory
            if category.visible and category.items:
                self._jumplist.AppendCategory(category.title, category.get_category())
        self._jumplist.CommitList()

    def delete_list(self):
        self._jumplist.DeleteList()

    def add_category(self, category):
        self.custom.append(category)
