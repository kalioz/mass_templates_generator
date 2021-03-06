# Mass template generator

This script allows you to create a lot of files issued from the templates you gave it.
It is useful to generate a lot of fake/anonymised files.

Written in Python to allow a simple interface with Ansible.

## TL;DR :

```bash
python3 main.py \
  --use-memory \
  --output "OUTPUT_FOLDER" \
  --csv-delimiter ";" \
  --csv-quote-char '"' \
  --template-folder "templates" \
  INSTRUCTIONS.csv
```

## Parameters

| Parameter         | Description                                                                                                                  | Default          |
|-------------------|------------------------------------------------------------------------------------------------------------------------------|------------------|
| --use-memory      | Loads the templates in memory. Allows for faster performance, but can be problematic if your templates are on the heavy side | False / Disabled |
| --output          | Output folder where the templates will be written                                                                            | "output"         |
| --csv-delimiter   | Delimiter used by the csv                                                                                                    | ";"              |
| --csv-quote-char  | Quote character used by the csv                                                                                              | '"'              |
| --template-folder | Folder containing the templates                                                                                              | "templates"      |
| __positional__    | CSV file containing the files to creates; see the below section for more information                                         | _N/A_ Required   |

## CSV file format

```csv
destination;template_subfolder;mimetype
test.jpg
test2.jpeg;funny_photos
test3.png;;image/jpg
test4.pdf
```
Only the "destination" part of each line is needeed.
You can specify a subfolder to the template in order to have different categories of templates.
The mimetype will be guessed from the filename, but can be overriden with the 3rd parameter of each line.

folder structure :
```console
.
└───output
└───templates
    │   template.jpg
    │   template.pdf
    │   template.png
    │
    └───funny_photos
            pinguin.jpg
            snow_bear.png
```

with the previous CSV file, the corresponding templates would be used :
```
test.jpg                -> templates/template.jpg
test2.jpeg;funny_photos -> templates/funny_photos/pinguin.jpg
test3.png;;image/jpg    -> templates/template.jpg
test4.pdf               -> templates/template.pdf
```


## Optimisation

You can pass the `--use-memory` switch to load in memory all the templates. This reduce the time spent due to the disk reading, but can be problematic with big file sizes.
