import datetime
import glob
import os
import uuid
import warnings
import zipfile

import numpy as np

from pyjaniml.janiml_schema import ExperimentStepSchema

try:
    import brukeropusreader
except ImportError:
    HAS_BRUKEROPUSREADER = False
else:
    HAS_BRUKEROPUSREADER = True

from pyjaniml.janiml import (
    Category,
    Device,
    ExperimentStep,
    Infrastructure,
    Method,
    Parameter,
    Result,
    Series,
    SeriesSet,
)


def warn_missing_brukeropusreader_lib():
    warnings.warn(
        "The brukeropusreader library is required to use this converter. "
        "Install it with `python -m pip install 'pyjaniml[opus]'`."
    )


NUMBER_OF_POINTS = 3885
FIRST_X_VALUE = 7490.215058363770367578
LAST_X_VALUE = 0
RESULTION = 1.928479675170899909631


class Converter:
    def from_opus_file(self, path_to_file):
        if not HAS_BRUKEROPUSREADER:
            warn_missing_brukeropusreader_lib()
            return

        # extract all data from file
        opus_data = brukeropusreader.read_file(path_to_file)
        spectra = opus_data["AB"]
        sample_origin = opus_data["Sample"]
        instrument = opus_data["Instrument"]
        parameters = opus_data["AB Data Parameter"]
        serial_number_and_device_type = instrument["INS"]
        serial_number = serial_number_and_device_type.split(".")[5]
        device_type = serial_number_and_device_type.split(".")[2]
        date = parameters["DAT"].split("/")
        time = parameters["TIM"].split(" ")[0].split(".")[0]
        timestamp = f"{date[2]}-{date[1]}-{date[0]}T{time}"

        # construct a new experiment step from it
        new_experiment_step_id = uuid.uuid4()
        experiment_step = ExperimentStep(
            "MIRA EWA Measurement", experimentStepID=new_experiment_step_id
        )
        experiment_step.sourceDataLocation = instrument["INS"]

        infrastructure = Infrastructure(Timestamp=datetime.datetime.fromisoformat(timestamp))
        experiment_step.Infrastructure = infrastructure
        device = Device(
            name="MIRA",
            manufacturer="CLADE",
            deviceIdentifier=device_type,
            serialNumber=serial_number,
        )
        method = Method("MIRA EWA Measurement", Device=device)
        method.Categories = []
        experiment_step.Method = method

        parameters["RES"] = (parameters["FXV"] - parameters["LXV"]) / (parameters["NPT"] - 1)

        current_wavenumbers = list(
            np.arange(
                start=parameters["FXV"],
                stop=parameters["LXV"] - parameters["RES"],
                step=-parameters["RES"],
            )
        )
        spectra, wavenumbers_filled, FXV = self.spectra_fill(
            spectra,
            current_wavenumbers,
            parameters["FXV"],
            parameters["RES"],
            FIRST_X_VALUE,
            LAST_X_VALUE,
        )

        spectra_series = Series("AB", "Float64", seriesID="AB", IndividualValueSets=[spectra])

        wavenumbers = Series(
            "wavenumbers",
            "Float64",
            seriesID="wavenumbers",
            AutoIncrementedValueSets=[{"startValue": FXV, "increment": -parameters["RES"]}],
        )

        series_set = SeriesSet("ABSpectrum", parameters["NPT"], [spectra_series, wavenumbers])
        result = Result("EWA_1", series_set)
        sample_parameter = Parameter("NAM", sample_origin["NAM"])
        sample_origin = Category("SampleOrigin", Parameters=[sample_parameter])
        result.Categories = [sample_origin]
        experiment_step.Results = [result]
        experiment_step.Categories = []

        return experiment_step

    def from_opus_binary(self, data):
        if not HAS_BRUKEROPUSREADER:
            warn_missing_brukeropusreader_lib()
            return

        meta_data = brukeropusreader.parse_meta(data)
        opus_data = brukeropusreader.parse_data(data, meta_data)
        return opus_data

    def spectra_fill(self, data, wavenumbers, FXV, RES, TargetFXV=None, TargetLXV=None):
        data = np.array([data])

        TargetLXV = wavenumbers[-1] + round((TargetLXV - wavenumbers[-1]) / RES) * RES
        NPT = round((TargetFXV - TargetLXV) / RES) + 1
        TargetFXV = TargetLXV + RES * (NPT - 1)

        FXV = TargetFXV
        LXV = TargetLXV

        Datadat = np.zeros((data.shape[0], NPT))
        Datadat[:] = NPT
        target_wavenumbers = list(np.arange(start=FXV, stop=LXV - RES, step=-RES))
        wavenumbers_round = [round(x, 3) for x in wavenumbers]
        new_wavenumbers_idx = [
            idx for idx, x in enumerate(target_wavenumbers) if round(x, 3) in wavenumbers_round
        ]
        Datadat[:, new_wavenumbers_idx] = data.tolist()[0]
        data = Datadat.tolist()[0]
        return data, wavenumbers, FXV

    def convert_folder_and_zip(self, folder_path, name_zip="sphere_import"):
        converter = Converter()
        zip_directory = os.path.join(folder_path, f"{name_zip}_{uuid.uuid4()}.zip")
        opus_directory = glob.glob(os.path.join(folder_path, "*.0"))
        with zipfile.ZipFile(zip_directory, "w") as outfile:
            for filename in opus_directory:
                janiml = converter.from_opus_file(filename)
                json_string = ExperimentStepSchema().dumps(janiml)
                outfile.writestr(os.path.basename(filename) + ".json", json_string)
