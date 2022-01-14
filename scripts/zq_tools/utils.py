import pymel.core as pm



def getMeshElementVertices(mesh,vtxs):

    indices = list(vtxs)
    #print vtxs
    for v in vtxs:
        cIndices = mesh.vtx[v].connectedVertices().indices()

        indices.extend(cIndices)
    indices = set(indices)
    
    #print(vtxs,indices)
    if indices == vtxs:
        return indices
    else:
        return getMeshElementVertices(mesh,indices)

def fix_BindPos():
    for jnt in pm.ls(type='joint'):
        jnt.rotateOrder.unlock()
        jnt.rotateOrder.set(0)
        wm = jnt.worldMatrix.get()
        if pm.objExists(jnt+'.bindPose'):
            jnt.bindPose.set(wm)

    bps = pm.ls(type = 'dagPose')
    pm.delete(bps)
    jnts = pm.ls(type = 'joint')
    pm.dagPose(jnts , save = 1 , name = 'bindPose')
    for i in pm.ls(type="skinCluster"):

        pm.PyNode("bindPose").message.connect(i.bindPose)
    jntMatrixs = [None for i in jnts]

    skinClusters = pm.ls(type="skinCluster")
    for i in pm.ls(type="skinCluster"):

        for index in range(len(i.bindPreMatrix.elements())):
            jnt = i.matrix[index].listConnections()[0]
            jntMatrixs[jnts.index(jnt)] = i.bindPreMatrix[index].get().inverse()


    noSkinJnts = []
    for i in jnts:
        if not i.listConnections(type="skinCluster"):
            noSkinJnts.append(i)
    noSkinJnts.sort(key=lambda x:len(x.getAllParents()))
    for j in noSkinJnts:

        localMatrix = j.getMatrix()
        parentJnt = j.getParent()
        pIndex = jnts.index(parentJnt)
        parentMatrix = jntMatrixs[pIndex]
        newPreMatrix = localMatrix * jntMatrixs[pIndex]
        j.worldMatrix.connect(skinClusters[0].matrix[skinClusters[0].bindPreMatrix.numElements()])
        skinClusters[0].bindPreMatrix[skinClusters[0].bindPreMatrix.numElements()].set(newPreMatrix.inverse())
        jntMatrixs[jnts.index(j)] = newPreMatrix