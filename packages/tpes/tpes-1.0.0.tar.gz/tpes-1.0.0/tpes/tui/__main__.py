
from tpes.data.instance import Instance
from tpes.instance_management import JSONInstanceWriter
from easy_widgets.MenuBox import MenuBox
from tpes.ui import TUIResolveWizzard, resolve
from easy_widgets import Application, Menu, MessageBox
import sys 
from tpes.command_executor import CommandExecutor, get_instance_state_machine
Application.init()

output = ""
def print_now(s):
    global output
    output += "\n" + s 
    Application.exit()

def main():
    global output
    instance = sys.argv[1]
    executor = CommandExecutor()
    states = executor.state(instance).items 
    sm = get_instance_state_machine(instance)
    resolution_menu = Menu("Resolve instance")
    menu = Menu("Select operation with instance")
    def cb():
        writer = JSONInstanceWriter()
        writer.write(sm.instance)
        menu.show()
    for state in states:
        resolution_menu.addOption("%s: %s" % (state.id, state.title), lambda btn, p: resolve(sm, p[0], TUIResolveWizzard(cb)), params=[state])
    menu.addOption("Follow", lambda btn, p: executor.follow(instance, save=True))
    menu.addOption("Resolve", lambda btn, p: resolution_menu.show())
    menu.addOption("TODO", lambda btn, p: print_now(executor.todo(instance)))
    menu.addOption("Show state", lambda btn, p: MessageBox(
        "State for instance", 
        "\n".join([x.title for x in executor.state(instance).items])).exec())
    menu.addOption("Exit", lambda btn, p: Application.exit())
    menu.show()

    Application.run()
    print(output)
if __name__ == "__main__":
    main()