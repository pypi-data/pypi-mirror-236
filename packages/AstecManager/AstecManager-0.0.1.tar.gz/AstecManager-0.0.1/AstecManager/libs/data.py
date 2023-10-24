class Cell:
    id = -1
    t = -1
    mothers = []
    daughters = []

    def __init__(self,id_cell,time_cell):
        self.id = id_cell
        self.t = time_cell
        self.mothers = []
        self.daughters = []

    def add_mother(self,cell):
        #print("mother len before : " + str(len(self.mothers)))
        #print("add mother for cell : "+str(self.t)+","+str(self.id)+" for mother : "+str(cell.t)+","+str(cell.id))
        if self.mothers is None:
            self.mothers = []
        if not cell in self.mothers:
            self.mothers.append(cell)
        #print("mother len after : " + str(len(self.mothers)))
        cell.add_daughter(self)


    def add_daughter(self,cell):
        #print("daughters len before : " + str(len(self.daughters)))
        #print("add daughter for cell : " + str(self.t) + "," + str(self.id) + " for mother : " + str(cell.t) + "," + str(cell.id))
        if self.daughters is None:
            self.daughters = []
        if not cell in self.daughters:
            self.daughters.append(cell)

def is_image(imagepath):
    """
        Returns true if file is a readable image or not

        Parameters
        --------
        path : basestring
            Path to file to test
        Returns
        --------
        boolean
            is file image or not
    """
    import os
    return os.path.isfile(imagepath) and (imagepath.endswith(".mha") or imagepath.endswith(".nii") or imagepath.endswith(".inr") or imagepath.endswith(".mha.gz") or imagepath.endswith(".nii.gz") or imagepath.endswith(".inr.gz"))

def get_id_t(idl):
    """ Return the cell t,id

            Parameters
            ----------
            idl : int
                Cell information id
            Returns
            -------
            t : int
                Cell time point
            id : int
                Cell id
    """
    t=int(int(idl)/(10**4))
    cell_id=int(idl)-int(t)*10**4
    return t,cell_id

def get_longid(t,idc):
    """ Return the cell information id

            Parameters
            ----------
            t : int
                Cell time point
            idc : int
                Cell id

            Returns
            -------
            id : int
                Cell information id format {ttt0iiii}
    """
    if t==0 or  t=="0":
        return idc
    return t*10**4+idc

