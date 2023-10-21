
# Introduction 

TPES is system which can plan and estimate tasks given workflow diagrams


# Usage 

get specific diagram details

    tpes read --workflow diagram.bpmn

Get all information for given element given id 

    tpes show --id <element-id> --workflow diagram.bpmn

Get all element ids linked from given element

    tpes next --id <element-id> --workflow diagram.bpmn

# Process instances

Everything is done by creating process instance:

    tpes start --instance path/to/instance.json --workflow path/to/process.bpmn


Every process definition contains:

* Start node 
* flow nodes 
* task nodes
* itermediate nodes
* reusable node
* end node 

# Process states 

To get process state:

    tpes state --instance path/to/instance.json

to continue planning for next states up until next stopping point 

    tpes follow --save --instance path/to/instance.json

To print all tasks which have to be done from this state up until next stopping state

    tpes todo --instance path/to/instance.json

in order to group them by 1 hour slots
    
    tpes todo --instance path/to/instance.json --group-by 1h


# Process management with its children 

All processes can be recognized if their children are in the same directory as current instance of process 

If current state of instance is reusable node, we can start subprocess 

    tpes start --parent-instance path/to/instance.json --instance path/to/new/instance.json 

# Reusables

every reusable node has to contain attribute:

* `path` with relative path from root of this directory 
* `repeat` - number of times to repeat this process - can be complex expression with parameter value from start OR can be * which means user will be asked
* I - values provided for input I  - has to be expression (so strings are inside quotes) OR can be * meaning user will be asked for every instance 

# Start nodes 

every start node contains attribute:


for every input I the following metadata can be defined:

* `IInputDescription` - description of input I 
* `IInputDefault` - default value of input I 

# Task nodes

every task contains attributes:

* `time` - estimated time in hours - can be complex expression with parameter value used from start

# End node

End nodes specify the following attributes:

* `deliverable` - Description of required the ending deliverable produced by process

# Data objects

for data objects, custom destination path can be defined with attribute:

* `destination`

# Script behaviour

intermediate nodes will stop the process until certain conditions are satisfied. Every intermediate node has to have capturing and sending parts. When planning, script will create new file describing instance of each process currently in progress 
and will track its status on what is the last node of process (start node, intermediate node or finished). Script keeps 
database of running instances. 

All reusables will be marked with "Plan" tasks where user will have to manually create these instances. 

When we arrive to reusable, until this instance is not finished, we cannot continue parent process with tasks after reusable.

on XOR and OR node, we stop and also create "plan next steps task" task 

on parallel node, we add all tasks recursively 

on message end node, we add task to send message to certain stakeholders 

on send message intermediate node, we add task to send message 

Every week script is run to check all instances that need periodic checking for messages and timers for intermediate nodes

every reusable process instance has parent of process instance which called it

on End node of instance of reusable, we add "plan" step to continue parent process manually.

If there is data object associated with particular task, mention it in org task in brackets e.g. "Pack stuff (with Checklist)"

Every data object has to be created from jinja template (if exists, otherwise from original file template) and copied
to aproprirate "Documents" section for particular process.

For instance, Travel/Checklist.org will be copied to Documents/Travel/Paris 2020/Checklist.org

for data objects, custom destination path can be defined with attribute:

* `destination`

and then document is copied to `<destination>/<instance name>/<document name>`


# Expressions 

* `instance` - evaluates to the name of current instance 
* `lineCount(path)` - number of lines in text file 
* `document(name)`  - returns full path to given document for given instance 
* `shell(command)` - evaluates to the output of executed command
* `concat(str1, str2, ...)` - concatenate strings
* `expression` - evaluate numeric expression
* `csvField(path, field, column)` - evaluates to value in `data[i][j]` such that `data[i][0] == field` and `data[0][j] == column`
* `input(inputName)` - evaluates to value given as `inputName` metadata parameter to this process or empty string if null

# Periodic processes 

Periodic processes are defined in `<project>/<subproject><Weekly|Monthly|Quarterly|Yearly>` 

all periodic processes start with timer 

# Subproject processes 

All other processes for project are defined in `<project>/<subproject>/Process` directory and they have aproprirate 
start node and this can be:

* message start - message from stakeholder received
* signal - created by other process, signals have to match 


All these processes either end with signal or with message to specific stakeholder 


# Creating TODO items and formats 

When we start certain workflow, we can have list of already traversed nodes by `follow` method
by using `todo` command like this 

    tpes todo --instance <instance-path>

We can even format this TODO list with `--format <FORMAT>` in several ways:

* `orgmode` - items are shown as ORG MODE TODO items 
* `orgmode+` - items are shown as ORG MODE TODO items where each item has added parent names to its item title 
* `jira` - outputs CSV table with `Summary` and `Time` columns

Items can be grouped as well with `--group-by-hours` option to make multiple items as one (titles separated with comma)

For instance, to export your stes as Jira tickets one can use:

    tpes todo --instance myinstance.json --format jira > tickets.csv

and then `tickets.csv` can be used to import tickets to Jira 

