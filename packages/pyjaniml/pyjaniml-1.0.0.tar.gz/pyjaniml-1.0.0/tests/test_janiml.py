import json
import uuid
from pathlib import Path

import pytest
from marshmallow import ValidationError

from pyjaniml.janiml import ExperimentStep
from pyjaniml.janiml_schema import ExperimentStepSchema

FIXTURE_DIR = Path(__file__).resolve().parent / "test_files"


@pytest.mark.parametrize("file", [FIXTURE_DIR / "ExperimentStep.json"])
def test_experiment_step(file):
    with file.open() as jsonfile:
        data = json.load(jsonfile)
        exp_from_dict = ExperimentStepSchema().load(data)
        exp_from_json = ExperimentStepSchema().loads(json.dumps(data))

        json_first = ExperimentStepSchema().dumps(exp_from_dict)
        json_second = ExperimentStepSchema().dumps(exp_from_json)
        assert json_first == json_second

        dict_first = ExperimentStepSchema().dump(exp_from_dict)
        dict_second = ExperimentStepSchema().dump(exp_from_json)
        assert dict_first == dict_second


@pytest.mark.parametrize("file", [FIXTURE_DIR / "ExperimentStepStringSpectra.json"])
def test_invalid_experiment_step(file):
    """
    ``IndividualValueSets`` must be of type ``List[List[float]]`` otherwise we
    will get a ``ValidationError``.
    """
    with file.open() as jsonfile:
        data = json.load(jsonfile)
        with pytest.raises(ValidationError):
            ExperimentStepSchema().load(data)


@pytest.mark.parametrize(
    "janiml_template",
    (
        {
            "name": "Simple QSIM Analysis Template",
            "experimentStepID": str(uuid.uuid4()),
            "comment": "Lorem ipsum dolor",
        },
        {
            "name": "Simple QSIM Analysis Template",
            "experimentStepID": str(uuid.uuid4()),
            "templateUsed": "Lorem ipsum dolor",
        },
        {
            "name": "Simple QSIM Analysis Template",
            "experimentStepID": str(uuid.uuid4()),
            "TagSet": {"step": "#1", "filter": "some"},
        },
    ),
)
def test_experiment_loads(janiml_template):
    experiment_step = ExperimentStepSchema()
    obj = experiment_step.loads(json_data=json.dumps(janiml_template))
    assert isinstance(obj, ExperimentStep)
    for key in janiml_template.keys():
        assert hasattr(obj, key)
