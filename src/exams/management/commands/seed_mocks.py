from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from exams.models import Exam, ExamCategory, MockTest, Option, Passage, Plan, Question, Section
from exams.seed_data import ibps_po_prelims_free_1 as data

CATALOGUE = [
    ('Banking', 'banking', 'IBPS, SBI and RRB officer & clerk exams', [
        ('IBPS PO', 'IBPS Probationary Officer', 'ibps-po'),
        ('SBI PO', 'SBI Probationary Officer', 'sbi-po'),
        ('IBPS Clerk', 'IBPS Clerk', 'ibps-clerk'),
        ('SBI Clerk', 'SBI Junior Associate', 'sbi-clerk'),
        ('IBPS RRB PO', 'IBPS RRB Officer Scale I', 'ibps-rrb-po'),
    ]),
    ('Insurance', 'insurance', 'LIC, NIACL and other insurer recruitments', [
        ('LIC AAO', 'LIC Assistant Administrative Officer', 'lic-aao'),
        ('NIACL AO', 'NIACL Administrative Officer', 'niacl-ao'),
        ('LIC ADO', 'LIC Apprentice Development Officer', 'lic-ado'),
    ]),
    ('Regulatory Bodies', 'regulatory', 'RBI, SEBI, NABARD and SIDBI Grade A/B', [
        ('RBI Grade B', 'RBI Grade B Officer', 'rbi-grade-b'),
        ('SEBI Grade A', 'SEBI Grade A Officer', 'sebi-grade-a'),
        ('NABARD Grade A', 'NABARD Grade A Officer', 'nabard-grade-a'),
    ]),
    ('Government Exams', 'government', 'SSC, Railways and state-level exams', [
        ('SSC CGL', 'SSC Combined Graduate Level', 'ssc-cgl'),
        ('SSC CHSL', 'SSC Combined Higher Secondary Level', 'ssc-chsl'),
        ('RRB NTPC', 'Railways Non-Technical Popular Categories', 'rrb-ntpc'),
    ]),
]


class Command(BaseCommand):
    help = 'Seed exam catalogue and the IBPS PO Prelims free mock.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Rebuild the free mock questions (deletes responses of existing attempts).',
        )

    @transaction.atomic
    def handle(self, *args, reset=False, **options):
        for c_order, (c_name, c_slug, tagline, exams) in enumerate(CATALOGUE, start=1):
            category, _ = ExamCategory.objects.update_or_create(
                slug=c_slug, defaults={'name': c_name, 'tagline': tagline, 'order': c_order},
            )
            for e_order, (short, name, slug) in enumerate(exams, start=1):
                Exam.objects.update_or_create(slug=slug, defaults={
                    'category': category, 'short_name': short, 'name': name, 'order': e_order,
                })

        exam = Exam.objects.get(slug=data.MOCK['exam']['slug'])
        exam.conducting_body = data.MOCK['exam']['conducting_body']
        exam.is_live = True
        exam.save()

        mock, created = MockTest.objects.get_or_create(slug=data.MOCK['slug'], defaults={
            'exam': exam, 'title': data.MOCK['title'], 'stage': data.MOCK['stage'],
            'is_free': True, 'is_published': True, 'order': 1,
        })
        if mock.sections.exists() and not reset:
            self.stdout.write('Free mock already seeded (use --reset to rebuild).')
        else:
            mock.sections.all().delete()
            self._load_sections(mock)
            self.stdout.write(self.style.SUCCESS(f'Seeded {mock.total_questions} questions.'))

        for n in range(2, data.PRO_MOCKS + 2):
            pro, _ = MockTest.objects.get_or_create(slug=f'ibps-po-prelims-mock-{n}', defaults={
                'exam': exam, 'title': f'IBPS PO Prelims · Mock {n}', 'stage': 'Prelims',
                'is_free': False, 'is_published': True, 'order': n,
            })
            if not pro.sections.exists():
                for s_order, s in enumerate(data.SECTIONS, start=1):
                    Section.objects.create(
                        mock=pro, name=s['name'], order=s_order, duration_minutes=s['minutes'],
                    )

        Plan.objects.update_or_create(exam=exam, name=data.PLAN['name'], defaults={
            'price_inr': data.PLAN['price_inr'], 'mrp_inr': data.PLAN['mrp_inr'],
            'features': data.PLAN['features'],
        })

    def _load_sections(self, mock):
        number = 0
        for s_order, s in enumerate(data.SECTIONS, start=1):
            section = Section.objects.create(
                mock=mock, name=s['name'], order=s_order, duration_minutes=s['minutes'],
            )
            order = 0
            for group in s['groups']:
                passage = None
                if group.get('directions'):
                    passage = Passage.objects.create(
                        section=section, directions=group['directions'],
                        body=group.get('body', '').strip(), layout=group.get('layout', 'inline'),
                    )
                for item in group['questions']:
                    order += 1
                    number += 1
                    if not 0 <= item['answer'] < len(item['options']):
                        raise CommandError(f'Question {number}: answer index out of range')
                    question = Question.objects.create(
                        section=section, passage=passage, order=order, text=item['text'],
                        explanation=item['explanation'], topic=group['topic'],
                    )
                    Option.objects.bulk_create(
                        Option(question=question, order=i, text=text, is_correct=i == item['answer'])
                        for i, text in enumerate(item['options'])
                    )
