from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
#from twisted.internet import task, defer
from twisted.internet.defer import Deferred
import collections

from DBPool import dbpool

import json
import datetime


class Instruction(dict):
    """An Instruction is an unordered collection of name and value pairs
    (a dict).

    Default values are provided in this class.

    """
    
    def underwrite(self, name, value):
        """Provides a value if name doesn't already exist."""
        if name in self:
            # Name already exists in the dict, do nothing
            pass
        else:
            # Name doesn't exist, add it
            self[name] = value

    def underwriteDefaults(self):
        """Specifies the default values of every parameter."""
        self.underwrite("FillLevel",50)
        self.underwrite("FillLevelHysteresis",5)
        self.underwrite("StartLevel",40)
        self.underwrite("StartLevelHysteresis",5)

    def __init__(self, *args, **kw):
        super(Instruction, self).__init__(args, kw)
        self.underwriteDefaults()
        self.instructionID = None

    def __init__(self):
        """Creates an empty instruction."""
        super(Instruction, self).__init__()
        self.underwriteDefaults()
        self.instructionID = None
    
    def execute(self):
        """Executes the instruction by setting the parameter values inside the PLC."""

    def insert(self, programID=None):
        def insertIntoDatabase(cursor):
            cursor.execute("INSERT INTO Instructions (ProgramID,FillLevel,FillLevelHysteresis,StartLevel,StartLevelHysteresis) VALUES (?,?,?,?,?)", (programID, self["FillLevel"], self["FillLevelHysteresis"], self["StartLevel"], self["StartLevelHysteresis"]))
            return cursor.lastrowid

        return dbpool.runInteraction(insertIntoDatabase)

    def markAsQueued
        

    def save(self, programID=None):
        """Saves the instruction to the database.  Returns the instruction ID."""
        


    def load(self, instructionID):
        """Loads the instruction from the database."""
        

testInstruction = Instruction()
testInstruction["FillLevel"] = 60


class Program(list):
    """A Program is an ordered collection of Instructions (a list)."""

    def __init__(self):
        self.programID = None

    def execute(self):
        """Executes the set of instructions.  Waits between instructions until
        the PLC is ready to accept the next instruction.

        If the programID is set, the database's queued flag is also
        managed during execution.

        """
        
    def save(self):
        """Saves program to the database."""
        self.programID = None # FIXME

    def load(self):
        """Loads program from the database."""
        self.programID = None # FIXME


class Butler(Resource):
    """The Butler receives Programs, queues Programs into the database,
    takes queued programs and sends them to the PLC, and starts up an
    observer to gather data regularly from the PLC.

    Further, if there are running instructions, the Butler regularly
    checks to see if the PLC is finished and awaiting the next (queued)
    instruction.

    """

    isLeaf = True

    def render_POST(self, request):
        print "Received POST request for Butler"
        request.setHeader("Content-Type","application/json");

        def printResult(data):
            print "data:",data

        d = testInstruction.insert()
        d.addCallback(printResult)

        return NOT_DONE_YET

    def render_GET(self, request):
        self.render_POST(request)

