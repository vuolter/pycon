import datetime
import sqlite3
import pytz

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from conferences.models import Conference, Duration, Topic
from submissions.models import Submission, SubmissionType
from languages.models import Language
from schedule.models import ScheduleItem, Room


class Command(BaseCommand):
    help = 'Imports the schedule from the old website'

    def add_arguments(self, parser):
        parser.add_argument('conference_code', type=str)
        parser.add_argument('db', type=str)

    def handle(self, *args, **options):
        db_path = options['db']

        conference_code = options['conference_code']

        talks_ids = []
        events_ids = []

        events = {}
        talks = {}

        rome_tz = pytz.timezone('Europe/Rome')
        utc_tz = pytz.utc
        user_model = get_user_model()

        conference, _ = Conference.objects.get_or_create(
            code=conference_code,
            defaults={
                'name': 'PyCon 9',
                'timezone': rome_tz,
            }
        )

        Room.objects.filter(conference=conference).delete()
        Topic.objects.filter(conference=conference).delete()
        ScheduleItem.objects.filter(conference=conference).delete()
        Submission.objects.filter(conference=conference).delete()
        Duration.objects.filter(conference=conference).delete()

        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()

            cursor.execute(f'SELECT event.id, start_time, custom, talk_id, abstract, duration, schedule.date FROM conference_event AS event LEFT JOIN conference_schedule AS schedule ON schedule.id = event.schedule_id WHERE conference = "{conference_code}"')

            for event in cursor:
                events_ids.append(str(event[0]))
                talk_id = event[3]

                events[event[0]] = {
                    'id': event[0],
                    'start_time': event[1],
                    'custom': event[2],
                    'talk_id': talk_id,
                    'abstract': event[4],
                    'duration': event[5],
                    'schedule_date': event[6]
                }

                if talk_id:
                    talks_ids.append(str(talk_id))

            talks_ids_as_str = ','.join(talks_ids)
            events_ids_as_str = ','.join(events_ids)

            cursor.execute(f'SELECT id, title, duration, language, level, type, qa_duration FROM conference_talk WHERE id IN ({talks_ids_as_str})')

            for talk in cursor:
                duration = int(talk[2])
                qa_duration = int(talk[6])
                total_duration = duration + qa_duration

                duration_obj = Duration.objects.get_or_create(
                    conference=conference,
                    duration=total_duration,
                    defaults={
                        'name': f'{duration} minutes + {qa_duration} Q/A',
                        'notes': '',
                    }
                )[0]

                language = talk[3]

                talks[talk[0]] = {
                    'id': talk[0],
                    'title': talk[1],
                    'duration': duration,
                    'qa_duration': qa_duration,
                    'duration_obj': duration_obj,
                    'language': language,
                    'language_obj': Language.objects.get(code=language),
                    'level': talk[4],
                    'type': talk[5],
                    'total_duration': total_duration,
                }

            cursor.execute(f'SELECT object_id, language, content, body FROM conference_multilingualcontent WHERE object_id in ({talks_ids_as_str}) AND content = "abstracts"')

            for abstract in cursor:
                object_id = abstract[0]
                talk = talks[object_id]

                if abstract[1] != talk['language']:
                    continue

                talk['abstract'] = abstract[3].strip()

            cursor.execute(f'SELECT id, track_id, event_id FROM conference_eventtrack WHERE event_id IN ({events_ids_as_str})')

            tracks_ids = []
            tracks = {}

            for mapping in cursor:
                event_id = mapping[2]

                if 'tracks' not in events[event_id]:
                    events[event_id]['tracks'] = []

                tracks_ids.append(str(mapping[1]))
                events[event_id]['tracks'].append(mapping[1])

            tracks_ids_as_str = ','.join(tracks_ids)

            cursor.execute(f'SELECT id, title, track, schedule_id FROM conference_track WHERE id IN ({tracks_ids_as_str})')

            for track in cursor:
                track_id = track[0]
                track_title = track[1]

                topic_obj = Topic.objects.get_or_create(name=track_title)[0]
                room_obj = Room.objects.get_or_create(conference=conference, name=track_title)[0]

                tracks[track_id] = {
                    'id': track_id,
                    'title': track_title,
                    'track': track[2],
                    'schedule_id': track[3],
                    'topic_obj': topic_obj,
                    'room_obj': room_obj,
                }


            cursor.close()

        talk_type = SubmissionType.objects.get_or_create(name='Talk')[0]
        interactive_type = SubmissionType.objects.get_or_create(name='Interactive')[0]
        training_type = SubmissionType.objects.get_or_create(name='Training')[0]
        poster_type = SubmissionType.objects.get_or_create(name='Poster session')[0]
        helphesk_type = SubmissionType.objects.get_or_create(name='Help desk')[0]

        # TALK_TYPE = (
        #     ('s', 'Talk'),
        #     ('i', 'Interactive'),
        #     ('t', 'Training'),
        #     ('p', 'Poster session'),
        #     ('h', 'Help desk'),
        # )

        old_site_to_obj = {
            's': talk_type,
            'i': interactive_type,
            't': training_type,
            'p': poster_type,
            'h': helphesk_type
        }

        for event in events.values():
            schedule_date = datetime.datetime.strptime(event['schedule_date'], '%Y-%m-%d')
            event_start = datetime.datetime.strptime(event['start_time'], '%H:%M:%S').time()

            start_date = datetime.datetime.combine(schedule_date, event_start)
            start_date = utc_tz.normalize(utc_tz.localize(start_date))

            if event['talk_id']:
                duration = event['duration'] if event['duration'] else talk['duration_obj'].duration
                end_date = start_date + datetime.timedelta(seconds=duration * 60)

                talk = talks[event['talk_id']]

                submission = Submission.objects.create(
                    conference=conference,
                    title=talk['title'],
                    abstract=talk.get('abstract', ''),
                    duration=talk['duration_obj'],
                    language=talk['language_obj'],
                    speaker_id=1,
                    topic_id=tracks[events[event_id]['tracks'][0]]['topic_obj'].id if 'tracks' in events[event_id] and len(events[event_id]['tracks']) > 0 else 1,
                    type=old_site_to_obj[talk['type']],
                )

                schedule = ScheduleItem.objects.create(
                    conference=conference,
                    type=ScheduleItem.TYPES.submission,
                    submission=submission,
                    start=start_date,
                    end=end_date,
                )
            else:
                end_date = start_date + datetime.timedelta(seconds=event['duration'] * 60)

                # other!
                schedule = ScheduleItem.objects.create(
                    conference=conference,
                    title=event['custom'],
                    description=event['abstract'],
                    type=ScheduleItem.TYPES.custom,
                    start=start_date,
                    end=end_date,
                )

            if 'tracks' in event:
                for track_id in event['tracks']:
                    track = tracks[track_id]
                    schedule.rooms.add(track['room_obj'])

                schedule.save()
