import maya.api.OpenMaya as newOM
import maya.OpenMaya as oldOM
import pymel.core as pm

#selectionList  = newOM.MGlobal.getActiveSelectionList()
mObject_list = newOM.MSelectionList()

dagIterator = newOM.MItDag( newOM.MItDag.kDepthFirst, newOM.MFn.kMesh )

mSelectionList = oldOM.MSelectionList()
selDagPath = oldOM.MDagPath()
childSelList = oldOM.MSelectionList()


# This reference to the MFnDagNode function set will be needed
# to obtain information about the DAG objects.
dagNodeFn = newOM.MFnDagNode()

# empty dictionary 
ini_dict = {} 

# Traverse the scene.
while not dagIterator.isDone():
    # Obtain the current item.
    dagObject = dagIterator.currentItem()
            
    # Make our MFnDagNode function set operate on the current DAG object.
    dagNodeFn.setObject( dagObject )
                       
    # Extract the DAG object's name.
    name = dagNodeFn.name()
    
    mSelectionList.add(dagIterator.fullPathName())
    
    if dagObject.apiType() == newOM.MFn.kMesh:
        mfn_mesh = newOM.MFnMesh( dagObject )
        
        dag = newOM.MFnDagNode( dagObject )
        bbox = dag.boundingBox
        min = newOM.MPoint(bbox.min) * newOM.MDagPath().exclusiveMatrix()
        max = newOM.MPoint(bbox.max) * newOM.MDagPath().exclusiveMatrix()
        #print name, bbox, min, max
        ini_dict.update( {name : str(bbox)} ) 

            
    # Iterate to the next item.
    dagIterator.next()

dagPath = oldOM.MDagPath()
tol = 0.01
for i in range( mSelectionList.length()):
    mSelectionList.getDagPath(i, dagPath)
    if dagPath.apiType() == oldOM.MFn.kMesh:
        dagFn = oldOM.MFnDagNode(dagPath)
        bbox = oldOM.MBoundingBox(dagFn.boundingBox())
        min = oldOM.MPoint(bbox.min()) * dagPath.exclusiveMatrix()
        max = oldOM.MPoint(bbox.max()) * dagPath.exclusiveMatrix()
        bBoxWorld = oldOM.MBoundingBox(min, max)
        om.MGlobal.displayInfo(dagPath.fullPathName())


# finding duplicate values 
# from dictionary 
# using a naive approach 
rev_dict = {} 
  
for key, value in ini_dict.items(): 
    rev_dict.setdefault(value, set()).add(key) 
      
result = [key for key, values in rev_dict.items() if len(values) > 1] 
  
# printing result 
#print("duplicate values", str(result)) 
