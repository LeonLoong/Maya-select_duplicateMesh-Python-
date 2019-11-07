import maya.api.OpenMaya as om
import pymel.core as pm
from itertools import chain 

dagIterator = om.MItDag( om.MItDag.kDepthFirst, om.MFn.kInvalid  )

# This reference to the MFnDagNode function set will be needed
# to obtain information about the DAG objects.
dagNodeFn = om.MFnDagNode()

# empty dictionary 
ini_dict = {} 

# Traverse the scene.
while not dagIterator.isDone():
    # Obtain the current item.
    dagObject = dagIterator.currentItem()
            
    # Make our MFnDagNode function set operate on the current DAG object.
    dagNodeFn.setObject( dagObject  )
                       
    # Extract the DAG object's name.
    name = dagNodeFn.name()
    
    if dagObject.apiType() == om.MFn.kTransform:
        dag = om.MFnDagNode( dagObject )
        bbox = dag.boundingBox
        min = om.MPoint(bbox.min) * om.MDagPath().exclusiveMatrix()
        max = om.MPoint(bbox.max) * om.MDagPath().exclusiveMatrix()
        ini_dict.update( {name : str( min ) + str( max )} ) 

            
    # Iterate to the next item.
    dagIterator.next()

# finding duplicate values 
# from dictionary using set 
rev_dict = {} 
for key, value in ini_dict.items(): 
    rev_dict.setdefault(value, set()).add(key) 
  
  
result = set(chain.from_iterable( values for key, values in rev_dict.items() if len(values) > 1)) 
  
# Iterating using for loop 
for key in result: 
    cmds.select( key, add = True ) 
