from firebase_admin import initialize_app
from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from google.cloud import vision

set_global_options(max_instances=10)
initialize_app()


@https_fn.on_request()
def generate_hashtags(request: https_fn.Request):
    body = request.get_json(silent=True)
    data = body.get("data", body)
    image_url = data.get("imageUrl")

    hashtags = extract_hashtags_from_image(image_url)

    return {
        "imageUrl": image_url,
        "hashtags": hashtags,
    }


def extract_hashtags_from_image(image_url: str) -> list[str]:
    client = vision.ImageAnnotatorClient(transport="rest")

    image = vision.Image()
    image.source.image_uri = image_url

    response = client.label_detection(image=image, max_results=5)

    hashtags = []

    for label in response.label_annotations:
        hashtags.append(f"#{label.description.replace(' ', '')}")

    return hashtags
