import os
import json
import psutil
import tempfile
import requests
import posixpath
import contextlib

from typing import Dict, Optional, Any

from .entities import experiment, run
from .error.value_error import HaiqvValueError
from .utils.common import get_millis, key_subset_split
from .utils.files import guess_mime_type


# Run
def create_run(exp_name: str, run_name: str, client_ip: str) -> run.Run:
    data = {
        'exp_name': exp_name,
        'run_name': run_name,
        'client_ip': client_ip
    }

    run_info = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})

    if run_info.status_code == 200:
        return run.Run(id=run_info.json()['run_id'], name=run_name)
    else:
        raise HaiqvValueError(run_info.text)


def update_run(
        run_id: str,
        status: Optional[str] = None,
        is_end: Optional[bool] = False,
) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run/update?run_id={run_id}&status={status}&is_end={is_end}')

    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Parameter
def log_param(run_id: str, key: str, value: Any) -> None:
    data = [
        {
            key: str(value)
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_params(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Metric
def log_metric(run_id: str, key: str, value: float, step: int) -> None:
    data = [
        {
            'key': key,
            'value': str(value),
            'step': step
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_metrics(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Artifact
def log_artifact(run_id: str, local_file: str, artifact_path: str) -> None:
    filename = os.path.basename(local_file)
    mime = guess_mime_type(filename)
    with open(local_file, 'rb') as f:
        res = requests.post(
            f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run/set-artifacts?run_id={run_id}&artifact_path={artifact_path}',
            files={'local_file': (filename, f, mime)}
        )
        if res.status_code != 200:
            raise HaiqvValueError(res)


# Requirements
def log_requirements(run_id: str, text: str, requirement_file: str) -> None:
    with _log_artifact_helper(run_id, requirement_file) as tmp_path:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(text)


# metadata
def log_dataset_metadata(run_id: str, name: str, path: str, desc: str = None):
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/metadata-dataset?run_id={run_id}&name={name}&path={path}&description={desc}',
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def findVolumeInfo(path):
    disk_partitions = psutil.disk_partitions(all=True)
    target_volumename = None
    target_device = None
    target_mountpoint = ""
    for partition in disk_partitions:
        find_mountpoint = partition.mountpoint + "/"
        if find_mountpoint in path and len(find_mountpoint) > len(target_mountpoint):
            target_device = partition.device
            target_mountpoint = find_mountpoint
    if target_device is not None:
        target_device_info = target_device.split("/")
        if len(target_device_info) > 0:
            target_volumename = target_device_info[1]
    return target_volumename, target_mountpoint


def log_model_metadata(run_id: str, name: str, path: str, step: int, metric: Optional[dict] = None):
    # todo
    abs_path = os.path.abspath(path)
    volume_name, mount_path = findVolumeInfo(abs_path)
    volume_path = None
    if volume_name is not None:
        volume_path = abs_path.replace(mount_path, "")
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/metadata-model?run_id={run_id}&name={name}&path={path}&step={step}&volume_name={volume_name}&volume_path={volume_path}',
                        data=json.dumps(metric),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


@contextlib.contextmanager
def _log_artifact_helper(run_id, artifact_file):
    norm_path = posixpath.normpath(artifact_file)
    filename = posixpath.basename(norm_path)
    artifact_dir = posixpath.dirname(norm_path)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, filename)
        yield tmp_path
        log_artifact(run_id, tmp_path, artifact_dir)

