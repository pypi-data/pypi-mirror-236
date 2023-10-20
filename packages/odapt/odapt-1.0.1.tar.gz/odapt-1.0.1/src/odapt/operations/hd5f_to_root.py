import h5py
import awkward as ak
import uproot

def hdf5_to_root(read_path, write_path, *, chunk_shape=True, compression=None,):
    f = h5py.File(read_path, 'r') # 'r' for read only, file must exist (it's the default though)
    keys = [key for key in f.keys()] # keys may or not be for groups
    # print([key for key in f.keys()])
    file = uproot.recreate(write_path)
    # tree.mktree("tree", branch_types=type(dset), ) # Fix type obv
    for key in keys:
        if type(f[key]) == type: #group or whatever...
            for s in dset.iter_chunks():
                if key == keys[0]:
                    file[keys[0]] = ak.Array(s)
                file[key].extend(ak.Array(s))

f = h5py.File("/Users/zobil/Documents/odapt/tests/samples/mytestfile.hdf5", "w")
dset = f.create_dataset("mydataset", (100,), dtype='i')

hdf5_to_root("/Users/zobil/Documents/odapt/tests/samples/mytestfile.hdf5", "/Users/zobil/Documents/odapt/tests/samples/destination.root")



# When writing with Uproot, every time you call uproot.WritableTree.extend,
# you create a new TBasket (for all TBranches, so you create a new cluster).
# You can use extend inside of iterate to resize TBaskets from an input 
# file to an output file.

