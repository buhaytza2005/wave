import random
from faker import Faker
from h2o_wave import main, app, Q, ui

fake = Faker()

_id = 0


class Issue:
    def __init__(self, text: str, status: str, progress: float, icon: str, notifications: str):
        global _id
        _id += 1
        self.id = f'I{_id}'
        self.text = text
        self.status = status
        self.views = 0
        self.progress = progress
        self.icon = icon
        self.notifications = notifications


# Create some issues
issues = [
    Issue(
        text=fake.sentence(),
        status=('Closed' if i % 2 == 0 else 'Open'),
        progress=random.random(),
        icon=('BoxCheckmarkSolid' if random.random() > 0.5 else 'BoxMultiplySolid'),
        notifications=('Off' if random.random() > 0.5 else 'On')) for i in range(100)
]

# Create columns for our issue table.
columns = [
    ui.table_column(name='text', label='Issue', searchable=True),
    ui.table_column(name='status', label='Status'),
    ui.table_column(name='notifications', label='Notifications'),
    ui.table_column(name='done', label='Done', cell_type=ui.icon_table_cell_type()),
    ui.table_column(name='views', label='Views'),
    ui.table_column(name='progress', label='Progress', cell_type=ui.progress_table_cell_type()),
]

columns2 = [
    ui.table_column(name='text', label='Issue'),
    ui.table_column(name='status', label='Status'),
    ui.table_column(name='notifications', label='Notifications'),
    ui.table_column(name='done', label='Done', cell_type=ui.icon_table_cell_type()),
    ui.table_column(name='views', label='Views'),
    ui.table_column(name='progress', label='Progress', cell_type=ui.progress_table_cell_type()),
]


@app('/demo')
async def serve(q: Q):
    q.page["meta"] = ui.meta_card(
            box="",
            layouts=[
                ui.layout(
                    breakpoint="xs",
                    zones=[
                        ui.zone("content")
                        ]

                    )
                ]

            )
    q.page['form'] = ui.form_card(box=ui.box('content', height="250px"), items=[
        ui.table(
            name='issues',
            columns=columns,
            rows=[ui.table_row(
                name=issue.id,
                cells=[issue.text, issue.status, issue.notifications, issue.icon, str(issue.views),
                       str(issue.progress)]) for issue in issues],
        )
    ])
    q.page['form2'] = ui.form_card(box=ui.box('content', height="250px"), items=[
        ui.table(
            name='issues2',
            columns=columns,
            rows=[ui.table_row(
                name=issue.id,
                cells=[issue.text, issue.status, issue.notifications, issue.icon, str(issue.views),
                       str(issue.progress)]) for issue in issues],
            groupable=True,
        )
    ])
    q.page['form3'] = ui.form_card(box=ui.box('content', height="250px"), items=[
        ui.table(
            name='issues3',
            columns=columns2,
            rows=[ui.table_row(
                name=issue.id,
                cells=[issue.text, issue.status, issue.notifications, issue.icon, str(issue.views),
                       str(issue.progress)]) for issue in issues],
            groupable=True,
        )
    ])
   
    await q.page.save()

