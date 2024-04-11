from app import db
import sqlalchemy as sa
from sqlalchemy.sql import text
import sqlalchemy.orm as so
import docker
import json

client = docker.from_env()


class Volume(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'<Volume {self.name}>'

    @staticmethod
    def getAll(self):
        return db.session.execute(db.select(Volume)).scalars().all()

    def get_usedin(self):
        return [container for container in
                db.session.execute(db.select(Container).where(Container.id_volume == self.id)).scalars().all()]


class Vorlage(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    version: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False,
                                               index=True)  # 100 is the smallest one, 101 is 1.01 etc
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    vscodeextension: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)  # json of the list
    installcommands: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)  # json of the list

    def toJson(self):
        usedin = [container.id for container in self.get_containers()]
        image_id = self.get_image().id if self.get_image() else None
        existingversions = [vorlage.version for vorlage in
                            db.session.execute(db.select(Vorlage).where(Vorlage.name == self.name)).scalars().all()]

        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "vscodeextension": json.loads(self.vscodeextension),
            "installcommands": json.loads(self.installcommands),
            "usedin": usedin,
            "image_id": image_id,
            "existingversions": existingversions
        }

    @staticmethod
    def get(name, _id, version):
        if not name and not _id and not version:
            return None
        if _id:
            return db.session.execute(db.select(Vorlage).where(Vorlage.id == _id)).scalars().first()
        if not version:
            return db.session.execute(
                db.select(Vorlage).where(Vorlage.name == name).order_by(text("version desc"))).scalars().first()
        return db.session.execute(
            db.select(Vorlage).where(Vorlage.name == name, Vorlage.version == version)).scalars().first()

    def __repr__(self):
        return f'<Vorlage {self.name}>'

    def delete(self):
        for image in db.session.execute(db.select(Image).where(Image.id_vorlage == self.id)).scalars():
            if image.isused():
                return False, f'Vorlage {self.name} is still in use, for example in image {image.name}'
        for image in db.session.execute(db.select(Image).where(Image.id_vorlage == self.id)).scalars():
            image.delete()
        db.session.delete(self)
        db.session.commit()
        return True

    def get_image(self):
        return db.session.execute(db.select(Image).where(Image.id_vorlage == self.id)).scalars().first()

    def get_containers(self):
        return db.session.execute(db.select(Container).join(Image).where(Image.id_vorlage == self.id)).scalars().all()


class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True, unique=True)
    id_vorlage: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Vorlage.id), nullable=False, index=True)
    docker_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True, unique=True)

    def __repr__(self):
        return f'<Image {self.name}>'

    def delete(self):
        if self.isused():
            return False, f'Image {self.name} is still in use'
        db.session.delete(self)
        client.images.remove(self.docker_id)
        db.session.commit()
        return True

    def isused(self):
        return bool(db.session.execute(db.select(Container).where(Container.id_image == self.id)).scalars().first())

    def get_containers(self):
        return db.session.execute(db.select(Container).where(Container.id_image == self.id)).scalars().all()

    def get_vorlage(self):
        return db.session.execute(db.select(Vorlage).where(Vorlage.id == self.id_vorlage)).scalars().first()


class Container(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True, index=True)
    port: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    id_volume: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Volume.id), nullable=False, index=True)
    id_image: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Image.id), nullable=False, index=True)

    def __repr__(self):
        return f'<Container {self.name}>'
