from hamal_utils.code.s3_utils.session import aws_session


class CustomS3Resource:
    def __init__(self):
        self._base_s3_resources = aws_session.resource('s3')

    def __getattr__(self, attr):
        if hasattr(self._base_s3_resources, attr):
            return getattr(self._base_s3_resources, attr)

        return super().__getattribute__(attr)
