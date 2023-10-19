# -*- coding: utf-8 -*-
import json
import logging
import sys

import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.models import Dataset
from arkindex_worker.worker import BaseWorker
from arkindex_worker.worker.dataset import DatasetMixin, DatasetState

PROCESS_ID = "cafecafe-cafe-cafe-cafe-cafecafecafe"


@pytest.fixture
def default_dataset():
    return {
        "id": "dataset_id",
        "name": "My dataset",
        "description": "A super dataset built by me",
        "sets": ["set_1", "set_2", "set_3"],
        "state": DatasetState.Open,
        "corpus_id": "corpus_id",
        "creator": "creator@teklia.com",
        "task_id": "task_id",
        "created": "2000-01-01T00:00:00Z",
        "updated": "2000-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_dataset_worker(monkeypatch, default_dataset):
    class DatasetWorker(BaseWorker, DatasetMixin):
        """
        This class is needed to run tests in the context of a dataset worker
        """

    monkeypatch.setattr(sys, "argv", ["worker"])
    dataset_worker = DatasetWorker()
    dataset_worker.args = dataset_worker.parser.parse_args()
    dataset_worker.process_information = {"id": PROCESS_ID}
    dataset_worker.dataset = Dataset(default_dataset)

    return dataset_worker


def test_list_process_datasets_readonly_error(mock_dataset_worker):
    # Set worker in read_only mode
    mock_dataset_worker.worker_run_id = None
    assert mock_dataset_worker.is_read_only

    with pytest.raises(AssertionError) as e:
        mock_dataset_worker.list_process_datasets()
    assert str(e.value) == "This helper is not available in read-only mode."


def test_list_process_datasets_api_error(responses, mock_dataset_worker):
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/",
        status=500,
    )

    with pytest.raises(
        Exception, match="Stopping pagination as data will be incomplete"
    ):
        next(mock_dataset_worker.list_process_datasets())

    assert len(responses.calls) == 5
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        # The API call is retried 5 times
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
    ]


def test_list_process_datasets(
    responses,
    mock_dataset_worker,
):
    expected_results = [
        {
            "id": "dataset_1",
            "name": "Dataset 1",
            "description": "My first great dataset",
            "sets": ["train", "val", "test"],
            "state": "open",
            "corpus_id": "corpus_id",
            "creator": "test@teklia.com",
            "task_id": "task_id_1",
        },
        {
            "id": "dataset_2",
            "name": "Dataset 2",
            "description": "My second great dataset",
            "sets": ["train", "val"],
            "state": "complete",
            "corpus_id": "corpus_id",
            "creator": "test@teklia.com",
            "task_id": "task_id_2",
        },
        {
            "id": "dataset_3",
            "name": "Dataset 3 (TRASHME)",
            "description": "My third dataset, in error",
            "sets": ["nonsense", "random set"],
            "state": "error",
            "corpus_id": "corpus_id",
            "creator": "test@teklia.com",
            "task_id": "task_id_3",
        },
    ]
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/",
        status=200,
        json={
            "count": 3,
            "next": None,
            "results": expected_results,
        },
    )

    for idx, dataset in enumerate(mock_dataset_worker.list_process_datasets()):
        assert isinstance(dataset, Dataset)
        assert dataset == expected_results[idx]

    assert len(responses.calls) == 1
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        ("GET", f"http://testserver/api/v1/process/{PROCESS_ID}/datasets/"),
    ]


@pytest.mark.parametrize(
    "payload, error",
    (
        # Dataset
        (
            {"dataset": None},
            "dataset shouldn't be null and should be a Dataset",
        ),
        (
            {"dataset": "not Dataset type"},
            "dataset shouldn't be null and should be a Dataset",
        ),
    ),
)
def test_list_dataset_elements_wrong_param_dataset(mock_dataset_worker, payload, error):
    with pytest.raises(AssertionError) as e:
        mock_dataset_worker.list_dataset_elements(**payload)
    assert str(e.value) == error


def test_list_dataset_elements_api_error(responses, mock_dataset_worker):
    dataset = mock_dataset_worker.dataset
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/datasets/{dataset.id}/elements/",
        status=500,
    )

    with pytest.raises(
        Exception, match="Stopping pagination as data will be incomplete"
    ):
        next(mock_dataset_worker.list_dataset_elements(dataset=dataset))

    assert len(responses.calls) == 5
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        # The API call is retried 5 times
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
    ]


def test_list_dataset_elements(
    responses,
    mock_dataset_worker,
):
    dataset = mock_dataset_worker.dataset

    expected_results = [
        {
            "set": "set_1",
            "element": {
                "id": "0000",
                "type": "page",
                "name": "Test",
                "corpus": {},
                "thumbnail_url": None,
                "zone": {},
                "best_classes": None,
                "has_children": None,
                "worker_version_id": None,
                "worker_run_id": None,
            },
        },
        {
            "set": "set_1",
            "element": {
                "id": "1111",
                "type": "page",
                "name": "Test 2",
                "corpus": {},
                "thumbnail_url": None,
                "zone": {},
                "best_classes": None,
                "has_children": None,
                "worker_version_id": None,
                "worker_run_id": None,
            },
        },
        {
            "set": "set_2",
            "element": {
                "id": "2222",
                "type": "page",
                "name": "Test 3",
                "corpus": {},
                "thumbnail_url": None,
                "zone": {},
                "best_classes": None,
                "has_children": None,
                "worker_version_id": None,
                "worker_run_id": None,
            },
        },
        {
            "set": "set_3",
            "element": {
                "id": "3333",
                "type": "page",
                "name": "Test 4",
                "corpus": {},
                "thumbnail_url": None,
                "zone": {},
                "best_classes": None,
                "has_children": None,
                "worker_version_id": None,
                "worker_run_id": None,
            },
        },
    ]
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/datasets/{dataset.id}/elements/",
        status=200,
        json={
            "count": 4,
            "next": None,
            "results": expected_results,
        },
    )

    for idx, element in enumerate(
        mock_dataset_worker.list_dataset_elements(dataset=dataset)
    ):
        assert element == (
            expected_results[idx]["set"],
            expected_results[idx]["element"],
        )

    assert len(responses.calls) == 1
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        ("GET", f"http://testserver/api/v1/datasets/{dataset.id}/elements/"),
    ]


@pytest.mark.parametrize(
    "payload, error",
    (
        # Dataset
        (
            {"dataset": None},
            "dataset shouldn't be null and should be a Dataset",
        ),
        (
            {"dataset": "not dataset type"},
            "dataset shouldn't be null and should be a Dataset",
        ),
    ),
)
def test_update_dataset_state_wrong_param_dataset(mock_dataset_worker, payload, error):
    api_payload = {
        "dataset": mock_dataset_worker.dataset,
        "state": DatasetState.Building,
        **payload,
    }

    with pytest.raises(AssertionError) as e:
        mock_dataset_worker.update_dataset_state(**api_payload)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "payload, error",
    (
        # DatasetState
        (
            {"state": None},
            "state shouldn't be null and should be a str from DatasetState",
        ),
        (
            {"state": "not dataset type"},
            "state shouldn't be null and should be a str from DatasetState",
        ),
    ),
)
def test_update_dataset_state_wrong_param_state(mock_dataset_worker, payload, error):
    api_payload = {
        "dataset": mock_dataset_worker.dataset,
        "state": DatasetState.Building,
        **payload,
    }

    with pytest.raises(AssertionError) as e:
        mock_dataset_worker.update_dataset_state(**api_payload)
    assert str(e.value) == error


def test_update_dataset_state_readonly_error(caplog, mock_dataset_worker):
    # Set worker in read_only mode
    mock_dataset_worker.worker_run_id = None
    assert mock_dataset_worker.is_read_only

    api_payload = {
        "dataset": mock_dataset_worker.dataset,
        "state": DatasetState.Building,
    }

    assert not mock_dataset_worker.update_dataset_state(**api_payload)
    assert [(level, message) for _, level, message in caplog.record_tuples] == [
        (
            logging.WARNING,
            "Cannot update dataset as this worker is in read-only mode",
        ),
    ]


def test_update_dataset_state_api_error(responses, mock_dataset_worker):
    dataset = mock_dataset_worker.dataset
    responses.add(
        responses.PATCH,
        f"http://testserver/api/v1/datasets/{dataset.id}/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_dataset_worker.update_dataset_state(
            dataset=dataset,
            state=DatasetState.Building,
        )

    assert len(responses.calls) == 5
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        # We retry 5 times the API call
        ("PATCH", f"http://testserver/api/v1/datasets/{dataset.id}/"),
        ("PATCH", f"http://testserver/api/v1/datasets/{dataset.id}/"),
        ("PATCH", f"http://testserver/api/v1/datasets/{dataset.id}/"),
        ("PATCH", f"http://testserver/api/v1/datasets/{dataset.id}/"),
        ("PATCH", f"http://testserver/api/v1/datasets/{dataset.id}/"),
    ]


def test_update_dataset_state(
    responses,
    mock_dataset_worker,
    default_dataset,
):
    dataset = mock_dataset_worker.dataset

    dataset_response = {
        "name": "My dataset",
        "description": "A super dataset built by me",
        "sets": ["set_1", "set_2", "set_3"],
        "state": DatasetState.Building.value,
    }
    responses.add(
        responses.PATCH,
        f"http://testserver/api/v1/datasets/{dataset.id}/",
        status=200,
        json=dataset_response,
    )

    updated_dataset = mock_dataset_worker.update_dataset_state(
        dataset=dataset,
        state=DatasetState.Building,
    )

    assert len(responses.calls) == 1
    assert [(call.request.method, call.request.url) for call in responses.calls] == [
        (
            "PATCH",
            f"http://testserver/api/v1/datasets/{dataset.id}/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "state": DatasetState.Building.value
    }
    assert updated_dataset == Dataset(**{**default_dataset, **dataset_response})
