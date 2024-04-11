from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class Volume(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True, index=True)

    containers: so.WriteOnlyMapped["Container"] = so.relationship(back_populates="volume")

    def __repr__(self):
        return f'<Volume {self.name}>'


class Vorlage(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    version: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False,
                                               index=True)  # 100 is the smalles one, 101 is 1.01 etc
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    vscodeextension: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)  # json of the list
    installcommands: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)  # json of the list

    images: so.WriteOnlyMapped["Image"] = so.relationship(back_populates="vorlage")

    def __repr__(self):
        return f'<Vorlage {self.name}>'


class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    version: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, index=True)
    id_vorlage: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Vorlage.id), nullable=False, index=True)
    docker_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)

    containers: so.WriteOnlyMapped["Container"] = so.relationship(back_populates="image")
    vorlage: so.Mapped[Vorlage] = so.relationship(back_populates="images")

    def __repr__(self):
        return f'<Image {self.name}>'


class Container(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True, index=True)
    port: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    id_volume: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Volume.id), nullable=False, index=True)
    id_image: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Image.id), nullable=False, index=True)

    volume: so.Mapped[Volume] = so.relationship(back_populates="containers")
    image: so.Mapped[Image] = so.relationship(back_populates="containers")

    def __repr__(self):
        return f'<Container {self.name}>'
