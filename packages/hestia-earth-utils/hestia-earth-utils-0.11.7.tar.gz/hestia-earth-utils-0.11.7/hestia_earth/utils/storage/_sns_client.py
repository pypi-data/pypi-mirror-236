_sns_client = None


# improves speed for connecting on subsequent calls
def _get_sns_client():
    global _sns_client
    import boto3
    _sns_client = boto3.session.Session().client('sns') if _sns_client is None else _sns_client
    return _sns_client
