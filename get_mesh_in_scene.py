import maya.OpenMaya as om

def doIt():
    # get the active selection list
    mSelectionList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(mSelectionList)
    om.MGlobal.clearSelectionList()
    dagIterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    
    # if nothing is selected
    if (mSelectionList.length() == 0):
    	# add all mesh type from scene to selectionList
    	while not dagIterator.isDone():
    		# avoiding intermediate objects
    		mfnDagNode =om.MFnDagNode(dagIterator.currentItem())
    		if not mfnDagNode.isIntermediateObject():
    		    mSelectionList.add(dagIterator.fullPathName())
    		dagIterator.next()
    
    
		# if mesh found in scene
		if mSelectionList.length() is not 0:
		    iterateFn(mSelectionList)
		else:
		    om.MGlobal.displayInfo("No Mesh present in the scene !!")
    
	# if user has selected a group of mesh
	else: 
		selDagPath = om.MDagPath()
		childSelList = om.MSelectionList()

		for i in range(mSelectionList.length()): 
			mSelectionList.getDagPath(i, selDagPath)

			# select all children shapes
			dagIterator.reset(selDagPath, om.MItDag.kDepthFirst, om.MFn.kMesh)
			while not dagIterator.isDone():
				# avoiding intermediate objects
				mfnDagNode = om.MFnDagNode(dagIterator.currentItem())
				if not mfnDagNode.isIntermediateObject():
				    childSelList.add(dagIterator.fullPathName())

				dagIterator.next()

		iterateFn(childSelList)

###################################################################################
### This function iterates through the selectionList passed to it.		           ###
### Compares every dagPath with everyother by feeding them to checkDoubleMesh() ###
###################################################################################

def iterateFn(selList):
	value = 0

	# iterate through selection list and pass pairs to checkDoubleMesh() function

	for i in range(selList.length()):
	    for j in range(i + 1, selList.length()):
	        dagPath1 = om.MDagPath()
	        dagPath2 = om.MDagPath()
	        selList.getDagPath(i, dagPath1)
	        selList.getDagPath(j, dagPath2)
	        
	        #if both dagpaths points to mesh type, check for doubleMesh
	        if (dagPath1.apiType() == om.MFn.kMesh and dagPath2.apiType() == om.MFn.kMesh):
	            value = checkDoubleMesh(dagPath1, dagPath2)
	        
	        if value == 1:
	            # select both the transform nodes
	            dagPathStringArray1 = []
	            dagPathStringArray2 = [] 
	            dagPathStringArray1.append(dagPath1.fullPathName().split('|'))
	            dagPathStringArray2.append(dagPath2.fullPathName().split('|'))
	            for dagPathString in dagPathStringArray1:
	                for object in dagPathString:
	                    try:
	                        om.MGlobal.selectByName(object)
	                    except:
	                        pass
	            for dagPathString in dagPathStringArray2:
	                for object in dagPathString:
	                    try:
	                        om.MGlobal.selectByName(object)
	                    except:
	                        pass

            	finalSelList = om.MSelectionList()
            	om.MGlobal.getActiveSelectionList(finalSelList)
            
            	if finalSelList.length() == 0:
            	    om.MGlobal.displayInfo("No Duplicates found")
	    
#################################################################################
### This function creates two bounding boxes for the dagPaths passed.	         ###
### Checks if the bounding boxes are at exact same position with a tolerance  ###
#################################################################################

def checkDoubleMesh(dagPath1, dagPath2):
    # tolerance value
    tol = 0.01
    
    ###################################
    ## Make the first worldspace bbox #
    ###################################
    
    dagFn1 = om.MFnDagNode(dagPath1)
    bbox1 = om.MBoundingBox(dagFn1.boundingBox())
    
    # get worldspace points
    min1 = om.MPoint(bbox1.min()) * dagPath1.exclusiveMatrix()
    max1 = om.MPoint(bbox1.max()) * dagPath1.exclusiveMatrix()
    
    # make a worldspace bounding box
    bBoxWorld1 = om.MBoundingBox(min1, max1)
    
    #####################################
    ## Make the second worldspace bbox ##
    #####################################
    
    dagFn2 = om.MFnDagNode(dagPath2)
    bbox2 = om.MBoundingBox(dagFn2.boundingBox())
    
    #get worldspace points
    min2 = om.MPoint(bbox2.min()) * dagPath2.exclusiveMatrix()
    max2 = om.MPoint(bbox2.max()) * dagPath2.exclusiveMatrix()
    
    # make a worldspace bounding box
    bBoxWorld2 = om.MBoundingBox(min2, max2)
    
    # compare the bounding boxes to identify double mesh cases
    if (min1.isEquivalent(min2, tol) and max1.isEquivalent(max2, tol)):
        om.MGlobal.displayInfo("Duplicate Mesh detected")
        om.MGlobal.displayInfo(dagPath1.fullPathName())
        om.MGlobal.displayInfo(dagPath2.fullPathName())
        return 1
    else:
        return 0

import time
start_time = time.time()
doIt()
print("--- %s seconds ---" % (time.time() - start_time))
