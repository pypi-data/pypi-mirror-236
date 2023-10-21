from extractzip.model import Lang, Text

lang = Lang(
    en=Text(
        base_path_error="No 'base_path' is set in config.yaml or it is not a directory.",
        config_error="No course '{course_name}' defined.",
        course_error="No {zip_type.name} in course '{course_name}' defined.",
        file_error="The {zip_type.name} doesn't exist (yet).",
        zip_file_error="The {zip_type.name} has not a valid zip file.",
        already_exists_text="The {zip_type.name} are already extracted.",
        input_text="Enter the password:",
        bad_password="Bad passwort!\nRerun the cell and enter the correct password!",
        success_text="The {zip_type.name} has been successfully extracted.",
    ),
    de=Text(
        base_path_error="In config.yaml ist kein 'base_path' festgelegt oder es ist kein Verzeichnis.",
        config_error="Kurse '{course_name}' ist nicht definiert.",
        course_error="Kein(e) {zip_type.name} im Kurs '{course_name}' definiert.",
        file_error="{zip_type.name} existiert (noch) nicht.",
        zip_file_error="{zip_type.name} hat keine gültige zip Datei.",
        already_exists_text="{zip_type.name} sind bereits entpackt.",
        input_text="Geben Sie das Passwort ein:",
        bad_password="Das Passwort stimmt nicht!\nFühren Sie die Zelle erneut aus und geben Sie das richtige Passwort ein!",
        success_text="{zip_type.name} wurde erfolgreich entpackt.",
    ),
)
