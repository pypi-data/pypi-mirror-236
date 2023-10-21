import json
from hestia_earth.utils.tools import current_time_ms

from .storage._s3_client import _load_from_bucket, _upload_to_bucket
from .storage._sns_client import _get_sns_client

PROGRESS_EXT = '.progress'


def upload_json(bucket_name: str, file_key: str, body):
    return _upload_to_bucket(bucket_name, file_key, json.dumps(body, indent=2, ensure_ascii=False).encode('utf8'))


def _to_file_progress(filepath: str):
    return filepath.replace('.csv', PROGRESS_EXT).replace('.json', PROGRESS_EXT).replace('.hestia', PROGRESS_EXT)


def _write_result(bucket_name: str, file_key: str, step: str, start: int, content: dict):
    filepath = _to_file_progress(file_key)

    # try to read existing progress to update the time per step
    try:
        data = json.loads(_load_from_bucket(bucket_name, filepath))
    except Exception:
        data = {}

    return upload_json(bucket_name, filepath, {
        'step': step,
        'time': {
            **(data.get('time', {}) if isinstance(data.get('time', {}), dict) else {}),
            step: current_time_ms() - start
        },
        **content
    })


def handle_error(
    bucket_name: str, file_key: str, step: str, start: int,
    err: str = '', stack: str = '', errors=[], warnings=[]
):
    return _write_result(bucket_name, file_key, step, start, {
        'success': False,
        'error': {
            'message': err,
            'stack': stack,
            'errors': errors,
            'warnings': warnings
        }
    })


def handle_success(bucket_name: str, file_key: str, step: str, start: int):
    return _write_result(bucket_name, file_key, step, start, {
        'success': True
    })


def publish_result(topic_arn: str, bucket_name: str, file_key: str, filepath: str, step: str, success: bool):
    return _get_sns_client().publish(
        TopicArn=topic_arn,
        Message=json.dumps({
            'bucket': bucket_name,
            'key': file_key,
            'filepath': filepath
        }, indent=2),
        MessageAttributes={
            'functionName': {
                'DataType': 'String',
                'StringValue': step + ('Done' if success else 'Error')
            }
        }
    )
