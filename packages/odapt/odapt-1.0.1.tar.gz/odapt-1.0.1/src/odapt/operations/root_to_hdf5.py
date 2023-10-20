import h5py
import awkward as ak
import uproot
from skhep_testdata import data_path

def root_to_hdf5(read_path, write_path, *, compression=None,):

    # Check out_file suffix - if root ask did you want hdf5_to_root or something?

    out_file = h5py.File(write_path, "w")

    # tree.mktree("tree", branch_types=type(dset), ) # Fix type obv
    in_file = uproot.open(read_path)
    keys = in_file.keys(recursive=True) #recursive false?
    print(in_file[keys[0]].classname)
    # for key in in_file.iterkeys():
    #     
    for key in keys:
        if in_file[key].classname == 'TTree':
            group = out_file.create_group(key)
            dset = group.create_dataset(key, chunks=True)
            for branch in in_file[key].iterate(step_size="100 MB"):
                # dset = group.create_dataset(key, data=branch, chunks=True) #Branch.member('fName') for name?
                dset.write_direct()
        # out_file.create_dataset("chunked", key, [array for array in in_file[key].iterate(step_size="100 MB")], chunks=True, maxshape=(None, None))

# f = h5py.File("/Users/zobil/Documents/odapt/tests/samples/mytestfile.hdf5", "w")
# dset = f.create_dataset("mydataset", (100,), dtype='i')

root_to_hdf5(data_path("uproot-simple.root"), "/Users/zobil/Documents/odapt/tests/samples/mytestfile.hdf5")

