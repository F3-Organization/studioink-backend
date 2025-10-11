from django.db import models

from api.models.artist import ArtistProfile
from api.models.base import BaseModel
from api.models.studio import Studio


class TimeBlockQuerySet(models.QuerySet["TimeBlock"]):
    def has_conflict(
        self,
        artist,
        start_time,
        end_time,
        exclude_timeblock_id: int | None = None,
    ) -> bool:
        qs = self.filter(
            artist=artist,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if exclude_timeblock_id is not None:
            qs = qs.exclude(id=exclude_timeblock_id)
        return qs.exists()


class TimeBlockManager(models.Manager):
    def get_time_block_by_id(self, time_block_id: int) -> "TimeBlock":
        return self.get_queryset().get(id=time_block_id)


class TimeBlock(BaseModel):
    objects: TimeBlockManager | TimeBlockQuerySet = TimeBlockManager.from_queryset(
        TimeBlockQuerySet
    )()

    class BlockType(models.TextChoices):
        BREAK = "BREAK", "Intervalo"
        ART_CREATION = "ART_CREATION", "Criação de Arte"
        DAY_OFF = "DAY_OFF", "Folga"
        OTHER = "OTHER", "Outro"

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="time_blocks",
        verbose_name="Estúdio",
    )
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name="time_blocks",
        verbose_name="Artista",
    )
    start_time = models.DateTimeField(verbose_name="Início do Bloqueio")
    end_time = models.DateTimeField(verbose_name="Fim do Bloqueio")
    block_type = models.CharField(
        max_length=20,
        choices=BlockType.choices,
        default=BlockType.OTHER,
        verbose_name="Tipo de Bloqueio",
    )
    reason = models.TextField(verbose_name="Motivo", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.get_block_type_display()} - {self.start_time.isoformat()}"

    class Meta:
        verbose_name = "Bloqueio de Tempo"
        verbose_name_plural = "Bloqueios de Tempo"
        ordering = ("-start_time",)
