import pytz
import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from pytest_factoryboy import register

from django.utils import timezone

from conferences.models import Conference, Topic, Deadline, AudienceLevel, Duration, Ticket
from languages.models import Language
from submissions.models import SubmissionType


@register
class ConferenceFactory(DjangoModelFactory):
    name = factory.Faker('name')
    code = factory.Faker('text', max_nb_chars=10)

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    timezone = pytz.timezone('Europe/Rome')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # if the user specifies active_cfp (for example) we will create a deadline to the conference
        # if the value is True, we will create an active CFP (now is between start and end)
        # if the value is False, we will create a CFP with dates in the past
        specified_deadlines = {}

        for deadline in Deadline.TYPES:
            _type = deadline[0]

            value = kwargs.pop(f'active_{_type}', None)
            specified_deadlines[_type] = value

        instance = super()._create(model_class, *args, **kwargs)

        for _type, value in specified_deadlines.items():
            if value is True:
                instance.deadlines.add(DeadlineFactory(conference=instance, type=_type))
            elif value is False:
                instance.deadlines.add(DeadlineFactory(
                    conference=instance,
                    type=_type,
                    start=timezone.now() - timezone.timedelta(days=10),
                    end=timezone.now() - timezone.timedelta(days=5),
                ))

        return instance

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        """Accepts a list of topic names and adds each topic to the
        Conference allowed submission topics.

        If a topic with that name doesn't exists, a new one is created.

        This fixture makes easier to add allowed topics to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.add(Topic.objects.get_or_create(name=topic)[0])

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        """Accepts a list of language codes and adds each language to the
        Conference allowed languages.

        This fixture makes easier to add allowed languages to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for language_code in extracted:
                self.languages.add(Language.objects.get(code=language_code))

    @factory.post_generation
    def submission_types(self, create, extracted, **kwargs):
        """Accepts a list of submission type names and adds each submission type to the
        Conference allowed submission types.

        If a submission type with that name doesn't exists, a new one is created.

        This fixture makes easier to add allowed submission types to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for submission_type in extracted:
                self.submission_types.add(SubmissionType.objects.get_or_create(name=submission_type)[0])

    @factory.post_generation
    def durations(self, create, extracted, **kwargs):
        """Accepts a list of durations (in minutes) and creates a duration object to the
        Conference allowed durations.

        This fixture makes easier to add durations to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for duration in extracted:
                duration, created = Duration.objects.get_or_create(
                    duration=duration,
                    conference=self,
                    defaults={'name': f'{duration}m'}
                )

                if created:
                    duration.allowed_submission_types.set(SubmissionType.objects.all())

                self.durations.add(duration)

    class Meta:
        model = Conference


@register
class TopicFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Topic
        django_get_or_create = ('name',)


@register
class DeadlineFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    type = factory.fuzzy.FuzzyChoice([deadline[0] for deadline in Deadline.TYPES])

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    class Meta:
        model = Deadline


@register
class AudienceLevelFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = AudienceLevel
        django_get_or_create = ('name', )


@register
class DurationFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = factory.Faker('word')
    duration = factory.Faker('pyint')
    notes = factory.Faker('text')

    class Meta:
        model = Duration


@register
class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket

    conference = factory.SubFactory(ConferenceFactory)

    name = factory.Faker('name')
    description = factory.Faker('paragraphs')
    price = factory.Faker('random_int', min=20, max=300)
    code = factory.Faker('military_ship')

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)
