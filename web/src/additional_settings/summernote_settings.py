SUMMERNOTE_THEME = 'bs4'


SUMMERNOTE_CONFIG = {
    'iframe': True,
    'empty': ('<p><br/></p>', '<p><br></p>'),
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '480',
        'lang': None,
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview']],
        ],
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',

        },
        'attachment_absolute_uri': True,
        'attachment_require_authentication': True,
        # 'attachment_model': 'main.models.Attachment',
        # 'attachment_upload_to': '%Y-%m-%dT',
    }
}
