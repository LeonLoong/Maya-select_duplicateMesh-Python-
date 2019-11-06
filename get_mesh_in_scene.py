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
            ini_dict.update( {name : bbox} )

    dagIterator.next()

def remove_duplicates(input_dict):
	output_dict = {}
	for key,value in input_dict.items():
		if value not in output_dict.values():
			output_dict[key] = value
	return output_dict	

print remove_duplicates(ini_dict)

 
