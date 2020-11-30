from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField


class ImageMetadata(EmbeddedDocument):
    author = StringField()
    camera = StringField()
    tags = StringField()


class Image(Document):
    image_id = StringField()
    cropped_picture = StringField()
    full_picture = StringField()
    metadata = EmbeddedDocumentField(ImageMetadata)

    meta = {
        "indexes": [
            {
                "fields": ["$metadata.author", "$metadata.camera", "$metadata.tags"],
                "default_language": "english",
            }
        ]
    }
