from datetime import date, timedelta
import sys
from takenote.utils.paths import (
    generate_note_folder,
    generate_note_path,
    generate_template_path,
)
from takenote.utils.dates import (
    get_monday,
    get_time_delta_from_options,
    format_header_date,
    get_weeks_delta,
)
from takenote.utils.args import process_args
from subprocess import call


def create_file(note_file, template_path, week: date):
    if not template_path:
        note_file.touch()
    else:
        text = ""
        with open(template_path, "r") as template_file:
            text = template_file.read().replace("HEADER_DATE", format_header_date(week))

        note_file.write_text(text)


def get_path_for_file(week: date, folder_path):
    folder = generate_note_folder(week, folder_path)

    if not folder.exists():
        print(f"Creating folder: {folder}")
        folder.mkdir(parents=True)

    note_path = folder.joinpath(generate_note_path(week))

    return note_path, note_path.exists()


def open_file(folder_path, editor, note_file, workspace=None):
    args = [editor, note_file]
    if workspace:
        args.append(folder_path.joinpath(workspace))

    call(args)


def main(argv):
    options, parser = process_args(argv)
    print(options)

    try:
        delta = get_time_delta_from_options(options)
    except ValueError:
        parser.print_help()
        sys.exit()

    week = get_monday(date.today()) + delta
    template_path = generate_template_path(options.notesFolder, options.template)

    if options.batch is not None:
        for i in range(0, options.batch):
            batch_week = week + get_weeks_delta(i)
            note_path, file_exists = get_path_for_file(batch_week, options.notesFolder)

            if not file_exists:
                print(f"Creating file: {note_path}")
                create_file(note_path, template_path, batch_week)

    note_path, file_exists = get_path_for_file(week, options.notesFolder)

    if not file_exists:
        print(f"Creating file: {note_path}")
        create_file(note_path, template_path, week)

    open_file(options.notesFolder, options.editor, note_path, options.workspace)
