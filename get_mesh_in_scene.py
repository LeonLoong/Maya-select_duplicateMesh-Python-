import maya.api.OpenMaya as om
import pymel.core as pm
from itertools import chain 

selectionList  = om.MGlobal.getActiveSelectionList()
dagIterator = om.MItDag( om.MItDag.kDepthFirst, om.MFn.kInvalid )
dagNodeFn = om.MFnDagNode()
# empty dictionary 
ini_dict = {} 

while not dagIterator.isDone():
    #dagObject = om.MFnDagNode(dagIterator.currentItem())
    dagObject = dagIterator.currentItem()
            
    # Make our MFnDagNode function set operate on the current DAG object.
    dagNodeFn.setObject( dagObject )
                       
    # Extract the DAG object's name.
    name = dagNodeFn.name()
   
    

    if dagObject.apiTypeStr == "kTransform":
        if cmds.ls(name, dag = True, type = ['mesh','nurbsSurface']):
            dag = om.MFnDagNode( dagObject )
            bbox = dag.boundingBox
            #min = om.MPoint(bbox.min) * om.MDagPath().exclusiveMatrix()
            #max = om.MPoint(bbox.max) * om.MDagPath().exclusiveMatrix()
            ini_dict.update( {name : str(bbox)} )
            
    dagIterator.next()

# finding duplicate values 
# from dictionary 
# using a naive approach 
rev_dict = {} 
  
for key, value in ini_dict.items(): 
    rev_dict.setdefault(value, set()).add(key) 
      
result = [key for key, values in rev_dict.items() 
                              if len(values) > 1] 
  
# printing result 
print("duplicate values", str(result)) 
