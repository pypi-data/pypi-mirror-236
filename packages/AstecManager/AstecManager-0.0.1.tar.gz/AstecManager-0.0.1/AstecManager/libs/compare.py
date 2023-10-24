import os
import AstecManager.libs.analyze as astec_analyze

from AstecManager.libs.analyze import plotminmaxleaves,plotminmaxleaves_post


def apply_analysis(list_lineage,list_noms,folder_out,embryo_name,mincells_test,maxcells_test,begin,end,path="",is_post=False,ref_lineage=None,data_path=None):
    print("-> Compute of the cell count plot")
    astec_analyze.generate_compare(list_noms, list_lineage, folder_out=folder_out, embryo_name=embryo_name,ref_lineage_path=ref_lineage,data_path=data_path)

    folder_exp = folder_out

    print("-> compute all min max leaves in for ")

    begin_temp = begin
    end_temp = end
    if is_post:
        plotminmaxleaves_post(list_lineage[0], list_noms[0], begin_temp, end_temp,folder_out,data_path=None)
    else :
        plotminmaxleaves(list_lineage, list_noms, begin_temp, end_temp,embryo_name,folder_out,data_path=None)

    os.system("cd " + folder_exp + ' && `for f in *.py; do python3 "$f"; done`')
    os.system("cd "+ folder_out + ' && rm generate_cell_count_multiples_.py')

