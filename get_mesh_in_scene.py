import maya.api.OpenMaya as om
import pymel.core as pm

selectionList  = om.MGlobal.getActiveSelectionList()
dagIterator = om.MItDag( om.MItDag.kDepthFirst, om.MFn.kInvalid )
dagNodeFn = om.MFnDagNode()

while( not dagIterator.isDone() ):
    #dagObject = om.MFnDagNode(dagIterator.currentItem())
    dagObject = dagIterator.currentItem()
            
    # Make our MFnDagNode function set operate on the current DAG object.
    dagNodeFn.setObject( dagObject )
                       
    # Extract the DAG object's name.
    name = dagNodeFn.name()
    
    if dagObject.apiTypeStr == "kMesh":
        print name

    dagIterator.next()
        
  