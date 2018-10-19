import pytz
import factory

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from conferences.models import Conference


@register
class ConferenceFactory(DjangoModelFactory):
    class Meta:
        model = Conference

    name = factory.Faker('name')
    slug = factory.Faker('slug')
    code = factory.Faker('text', max_nb_chars=10)

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    voting_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    voting_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    refund_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    refund_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    cfp_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    cfp_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)
