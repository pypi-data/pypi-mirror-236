import os
from tpes.expression import ASK_INPUT
import easy_widgets
from tpes.environment import Environment
from typing import Callable
from easy_widgets.MenuBox import MenuBox
from tpes.data.instance import Instance
from tpes.data.node import WorkflowNode
from tpes.instance_management import InstanceFactory, InstanceStateMachine, JSONInstanceWriter, TransitionRequest
from easy_widgets import Application, Menu, MessageBox

class AbstractResolveWizzard:
    def show_dialog(self, msg: str):
        raise NotImplementedError()
    def select_multiple(self, msg, items, f: Callable[[list[int]], None]) -> list[int]:
        raise NotImplementedError()
    def select_one(self, msg, items, f: Callable[[int], None]):
        raise NotImplementedError()
    def yesno(self, msg, f_yes, f_no):
        raise NotImplementedError()
    def text(msg: str, callback: Callable[[str], None]):
        raise NotImplementedError()

def create_child(name: str, instance: Instance, state: WorkflowNode):
    env = Environment()
    workflow  = env.find_workflow(instance.evaluate(state, "path"))
    factory = InstanceFactory(workflow, name, {}, instance)
    childInstance:Instance = factory.parse()
    childInstance.parent = instance
    childInstance.path = "%s.json" % name 
    writer = JSONInstanceWriter()
    writer.write(childInstance)
    for do in childInstance.workflow.data_objects:
        print("Producing " + do.title)
        env.produce_document(instance, do.title)
    return childInstance 

def resolve(sm: InstanceStateMachine, state: WorkflowNode, ui: AbstractResolveWizzard) -> Instance:
    transition = sm.next(state)
    sm.instance.states = [s for s in sm.instance.states if s != state]
    if transition.request == TransitionRequest.CREATE_CHILD_INSTANCES:
        s = ("Create child instances and then continue.")
        s += ("\nDo you want to create child? (type name of instance) or leave empty to continue or type \"x\" to cancel")
        def _ans(ans):
            print("Evaluation of repeat: %s", sm.instance.evaluate(state, "repeat"))
            if ans == "" or (sm.instance.evaluate(state, "repeat") != ASK_INPUT and sm.instance.evaluate(state, "repeat") in [0, 1]):
                print("adding new states")
                sm.instance.states.extend(transition.new_states)
            else:
                print("adding existing state")
                sm.instance.states.append(state)
            if ans != "":
                if ans != "x":
                    return create_child(ans, sm.instance, state)
                else:
                    return None
        ui.text(s, _ans)
    elif transition.request == TransitionRequest.SELECT_ONE:
        msg = ("Select one of the following next states:")
        ui.select_one(msg, [s.title for s in transition.new_states], lambda answer: sm.instance.states.append(transition.new_states[answer]))
    elif transition.request == TransitionRequest.SELECT_SUNSET:
        msg = ("Select subset of the following tasks:")
        ui.select_multiple(msg, [s.title for s in transition.new_states], lambda answers: [sm.instance.states.append(transition.new_states[x]) for x in answers])
    else:
        msg = ("Manual intervention required.")
        msg += ("\nEnter IDs of nodes in workflow you want to replace this node with.")
        def f(answer):
            answer = [transition.new_states[k].id for k in answer]
            for a in answer:
                sm.instance.states.append(sm.instance.workflow.find_node(a))
        ui.select_multiple(msg, [s.title for s in transition.new_states], f)
    return sm.instance

class CursesResolveWizzard(AbstractResolveWizzard):
    def show_dialog(self, msg: str):
        raise NotImplementedError()
    def select_multiple(self, msg, items) -> list[int]:
        raise NotImplementedError()
    def select_one(self, msg, items) -> int:
        raise NotImplementedError()


class CLIResolveWizzard(AbstractResolveWizzard):
    def show_dialog(self, msg: str):
        print(msg)
        print("Press return to continue.")
        input(">> ")
    def select_multiple(self, msg, items, f):
        print(msg)
        print("Enter numbers of items you want to select.")
        for i, item in enumerate(items):
            print("%d - %s" % (i+1, item))
        answer = str(input(">> "))
        f([int(x) - 1 for x in answer.split(" ")])
    def select_one(self, msg, items, f):
        print(msg)
        for i, item in enumerate(items):
            print("%d - %s" % (i+1, item))
        f(int(input("Select one nuber >> ")) - 1)
    def yesno(self, msg, yes, no):
        print(msg)    
        ans = str(input("(y/n)>> "))
        if ans == "y":
            yes()
        else:
            no()
    def text(self, msg, callback):
        print(msg)    
        ans = str(input(">> "))
        callback(ans)
class TUIResolveWizzard:
    def __init__(self, cb) -> None:
        self.cb = cb 
    def show_dialog(self, msg: str):
        MessageBox("", msg).exec()
    def select_multiple(self, msg, items, h) -> list[int]:
        selected = [] 
        menu = MenuBox(msg)
        for i, item in enumerate(items):
            def f(btn, p):
                selected.append(p[0])
                menu.exec()
            menu.addOption(item, f, params=[i])
        menu.addOption("Finish", lambda b, p: [h(selected), self.cb()])
        menu.exec()
    def select_one(self, msg, items, h) -> int:
        menu = MenuBox("")
        for i, item in enumerate(items):
            def f(btn, p):
                h(p[0])
                self.cb()
            menu.addOption(item, f, params=[i])
        menu.exec()
    def yesno(self, msg, y,n):
        menu = MenuBox(msg)
        menu.addOption("Yes", lambda b, p: [y(), self.cb()])
        menu.addOption("No", lambda b, p: [n(), self.cb()])
        menu.exec()
    def text(self, msg, callback):
        dialog = easy_widgets.TextInput(msg, lambda ans: [callback(ans), self.cb()])
        dialog.show()