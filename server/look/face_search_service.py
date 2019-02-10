import boto3
from typing import Tuple


class FaceSearchService:
    def __init__(self,
                 collectionId: str,
                 faceMatchThreshold: int = 95,
                 maxFaces: int = 2) -> None:
        self.client = boto3.client('rekognition')
        self.collectionId = collectionId
        self.faceMatchThreshold = faceMatchThreshold
        self.maxFaces = maxFaces

    def search(self, image: str) -> Tuple[str, bool]:
        response = self.client.search_faces_by_image(
            CollectionId=self.collectionId,
            FaceMatchThreshold=self.faceMatchThreshold,
            Image={"Bytes": image},
            MaxFaces=self.maxFaces)
        if len(response["FaceMatches"]) == 1:
            return (response["FaceMatches"][0]["Face"]["FaceId"], True)

        return ("", False)
