import pytz

from pytest import mark

from django.utils import timezone


@mark.django_db
def test_get_conference_info(conference, ticket_factory, graphql_client):
    ticket = ticket_factory(conference=conference)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                id
                code
                name
                tickets {
                    id
                    name
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp
    assert {
        'id': str(conference.id),
        'code': conference.code,
        'name': conference.name,
        'tickets': [
            {
                'id': str(ticket.id),
                'name': ticket.name,
            },
        ],
    } == resp['data']['conference']


@mark.django_db
def test_get_conference_deadlines_ordered_by_start_date(graphql_client, conference_factory, deadline_factory):
    now = timezone.now()

    conference = conference_factory(timezone=pytz.timezone('America/Los_Angeles'))

    deadline_voting = deadline_factory(
        start=now - timezone.timedelta(days=20),
        end=now - timezone.timedelta(days=15),
        conference=conference,
        type='voting'
    )

    deadline_cfp = deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type='cfp'
    )

    deadline_refund = deadline_factory(
        start=now - timezone.timedelta(days=14),
        end=now - timezone.timedelta(days=10),
        conference=conference,
        type='refund'
    )

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                start
                end
                timezone
                deadlines {
                    start
                    end
                    type
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert resp['data']['conference']['timezone'] == 'America/Los_Angeles'

    assert resp['data']['conference']['start'] == conference.start.isoformat()
    assert resp['data']['conference']['end'] == conference.end.isoformat()

    assert {
        'start': deadline_voting.start.isoformat(),
        'end': deadline_voting.end.isoformat(),
        'type': 'VOTING'
    } == resp['data']['conference']['deadlines'][0]

    assert {
        'start': deadline_refund.start.isoformat(),
        'end': deadline_refund.end.isoformat(),
        'type': 'REFUND'
    } == resp['data']['conference']['deadlines'][1]

    assert {
        'start': deadline_cfp.start.isoformat(),
        'end': deadline_cfp.end.isoformat(),
        'type': 'CFP'
    } == resp['data']['conference']['deadlines'][2]


@mark.django_db
def test_get_not_existent_conference_info(conference, graphql_client):
    resp = graphql_client.query(
        """
        {
            conference(code: "random-conference-code") {
                name
            }
        }
        """,
    )

    assert 'errors' in resp
    assert resp["errors"][0]["message"] == "Conference matching query does not exist."


@mark.django_db
def test_query_conference_audience_levels(graphql_client, conference, audience_level_factory):
    level1 = audience_level_factory()
    level2 = audience_level_factory()
    level3 = audience_level_factory()

    conference.audience_levels.add(level1, level2, level3)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                audienceLevels {
                    id
                    name
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp

    assert {
        'name': level1.name,
        'id': str(level1.id)
    } in resp['data']['conference']['audienceLevels']

    assert {
        'name': level2.name,
        'id': str(level2.id)
    } in resp['data']['conference']['audienceLevels']

    assert {
        'name': level3.name,
        'id': str(level3.id)
    } in resp['data']['conference']['audienceLevels']


@mark.django_db
def test_query_conference_topics(graphql_client, conference, topic_factory):
    topic1 = topic_factory()
    topic2 = topic_factory()
    topic3 = topic_factory()

    conference.topics.add(topic1, topic2, topic3)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                topics {
                    id
                    name
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp

    assert {
        'name': topic1.name,
        'id': str(topic1.id)
    } in resp['data']['conference']['topics']

    assert {
        'name': topic2.name,
        'id': str(topic2.id)
    } in resp['data']['conference']['topics']

    assert {
        'name': topic3.name,
        'id': str(topic3.id)
    } in resp['data']['conference']['topics']


@mark.django_db
def test_query_conference_languages(graphql_client, conference, language):
    lang_it = language('it')
    lang_en = language('en')

    conference.languages.add(lang_en, lang_it)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                languages {
                    id
                    name
                    code
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp

    assert {
        'name': lang_it.name,
        'code': lang_it.code,
        'id': str(lang_it.id)
    } in resp['data']['conference']['languages']

    assert {
        'name': lang_en.name,
        'code': lang_en.code,
        'id': str(lang_en.id)
    } in resp['data']['conference']['languages']



@mark.django_db
def test_get_conference_durations(graphql_client, duration_factory, submission_type_factory):
    talk_type = submission_type_factory(name='talk')
    tutorial_type = submission_type_factory(name='tutorial')

    d1 = duration_factory()
    d1.allowed_submission_types.add(talk_type)
    d2 = duration_factory(conference=d1.conference)
    d2.allowed_submission_types.add(tutorial_type)

    conference = d1.conference

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                durations {
                    id
                    name
                    duration
                    notes
                    allowedSubmissionTypes {
                        id
                        name
                    }
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp
    assert {
        'id': str(d1.id),
        'name': d1.name,
        'duration': d1.duration,
        'notes': d1.notes,
        'allowedSubmissionTypes': [
            {'id': str(talk_type.id), 'name': talk_type.name}
        ]
    } in resp['data']['conference']['durations']

    assert {
        'id': str(d2.id),
        'name': d2.name,
        'duration': d2.duration,
        'notes': d2.notes,
        'allowedSubmissionTypes': [
            {'id': str(tutorial_type.id), 'name': tutorial_type.name}
        ]
    } in resp['data']['conference']['durations']
