import logging
import os, sys
from tkinter import *

from jumplists import JumpList, JumpListItemLink
from jumplists.jumplist import JumpListCustomCategory


def main():
    logger.info("args: %s", sys.argv)
    jump_list = JumpList()

    custom_category = JumpListCustomCategory("Example")

    args = []

    if not getattr(sys, 'frozen', False):
        args.append(__file__)

    link1 = JumpListItemLink("Test item", sys.executable,
                                     args + ["test\" test"])
    link1.working_directory = os.getcwd()
    custom_category.add_item(link1)
    custom_category.visible = True

    jump_list.add_category(custom_category)
    jump_list.update()

    window = Tk()
    window.title("Example window")
    lbl = Label(window, text="Example Label")
    lbl.grid(column=0, row=0)
    window.mainloop()


if __name__ == '__main__':
    logger = logging.getLogger('jumplist_example')
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    main()
