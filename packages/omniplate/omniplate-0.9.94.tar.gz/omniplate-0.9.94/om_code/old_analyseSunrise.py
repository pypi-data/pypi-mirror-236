import numpy as np
import om_code.omgenutils as gu


def analyseSunrise(dfd, rcontents, experiment):
    """
    Parse data from an imported Excel file from a Sunrise plate reader.

    Parameters
    --
    dfd: dataframe
        Created by importing the data from a file using Panda's read_excel.
    rcontents: dataframe
        Created by analyseContentsofWells.
    experiment: string
        The name of the experiment.

    Returns
    ------
    rdict: list of dictionaries
        Describes the contents of the plate by experiment, condition, strain,
        time, and well.
    datatypes: list of strings
        Delineates all the types of data in the experiment and is minimally
        ['OD'].
    """
    # extract datatypes
    datatypes = np.array(["OD"], dtype=object)
    # extract times of measurements
    t = (
        gu.rmnans([float(str(ts).split("s")[0]) for ts in dfd.to_numpy()[0]])
        / 3600.0
    )
    # data
    # add to dataframe
    rdict = []
    for index, row in dfd.iterrows():
        if isinstance(row[-1], str) and row[-1][0] in "ABCDEFGH":
            well = row[-1]
            data = row.to_numpy(dtype="float")[:-1]
            if (
                rcontents[well][0] is not None
                and rcontents[well][1] is not None
            ):
                for j in range(len(t)):
                    cons = {
                        "experiment": experiment,
                        "condition": rcontents[well][0],
                        "strain": rcontents[well][1],
                        "time": t[j],
                        "well": well,
                    }
                    dats = {"OD": data[j]}
                    cons.update(dats)
                    rdict.append(cons)
    return rdict, datatypes
