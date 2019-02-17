from flask import current_app
import click
from flask.cli import FlaskGroup
import boto3

from look import create_app
from look.model import db, User, Face


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
    pass


@cli.command("init-db")
def init_db() -> None:
    db.init_app(current_app)
    db.drop_all()
    db.create_all()
    click.echo("Initialized Database")


@cli.group()
def user():
    pass


@user.command("add")
@click.argument("email")
@click.argument("password")
def add_user(email: str, password: str) -> None:
    db.init_app(current_app)
    user = User(email=email, password=password, faces=[])
    db.session.add(user)
    db.session.commit()
    click.echo("Created User")


@cli.group()
def face():
    pass


@face.command("add")
@click.argument("email")
@click.argument("path")
@click.option("--collection-id", default="look", help='Collection ID')
@click.option(
    "--only-id/--no-only-id",
    default=False,
    help="If set, it does not send image data")
def add_face(email: str, path: str, collection_id: str, only_id: bool) -> None:
    db.init_app(current_app)
    if not only_id:
        with open(path, "rb") as f:
            client = boto3.client('rekognition')
            response = client.index_faces(
                CollectionId=collection_id,
                Image={'Bytes': f.read()},
                MaxFaces=1,
            )

        assert len(response["FaceRecords"]) == 1

    user = User.query.filter_by(email=email).first()
    if only_id:
        face = Face(face_id=path)
    else:
        face = Face(face_id=response["FaceRecords"][0]["Face"]["FaceId"])
    user.faces.append(face)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Added face")


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        click.echo(e)
