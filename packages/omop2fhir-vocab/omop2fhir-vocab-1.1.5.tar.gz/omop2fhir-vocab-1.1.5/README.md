# OMOP2FHIR-vocab
Convert OMOP vocab to FHIR.

## Prerequisites
* [Python 3.9+](https://www.python.org/downloads/)
* [Java 11+](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html)

## Installation
`pip install omop2fhir-vocab`

## Running
Run: `omop2fhir-vocab OPTIONS`

### CLI
```
omop2fhir-vocab --help
usage: omop2fhir-vocab [-h] -c CONCEPT_CSV_PATH -r CONCEPT_RELATIONSHIP_CSV_PATH [-v VOCABS [VOCABS ...]] [-R RELATIONSHIPS [RELATIONSHIPS ...]] [-o OUT_DIR]
                       [-I]

Convert OMOP vocab to FHIR.

options:
  -h, --help            show this help message and exit
  -c CONCEPT_CSV_PATH, --concept-csv-path CONCEPT_CSV_PATH
                        Path to CSV of OMOP concept table.
  -r CONCEPT_RELATIONSHIP_CSV_PATH, --concept-relationship-csv-path CONCEPT_RELATIONSHIP_CSV_PATH
                        Path to CSV of OMOP concept_relationship table.
  -v VOCABS [VOCABS ...], --vocabs VOCABS [VOCABS ...]
                        Which vocabularies to include in the output? Usage: --vocabs "Procedure Type" "Device Type"
  -R RELATIONSHIPS [RELATIONSHIPS ...], --relationships RELATIONSHIPS [RELATIONSHIPS ...]
                        Which relationship types from the concept_relationship table's relationship_id field to include? Default is "Is a"
                        only. Passing "ALL" includes everything. Usage: --relationships "Is a" "Maps to"
  -o OUT_DIR, --out-dir OUT_DIR
                        Output directory. Defaults to current working directory.
  -V, --vocab-outputs   Create set of artefacts (CodeSystem, ConceptMap) for each vocabulary?
  -C, --combined-outputs
                        Create set of artefacts (CodeSystem, ConceptMap) for all of OMOP vocabulary combined?
  -e, --exclude-vocab-prefix
                        With this flag absent, the identifiers and file names for each vocabulary will be prefixed "OMOP".
  -S, --exclude-code-system
                        Exclude CodeSystem outputs.
  -M, --exclude-concept-map
                        Exclude ConceptMap outputs.
  -H {all,omop2fhir,omop2owl,owl2fhir} [{all,omop2fhir,omop2owl,owl2fhir} ...], --caching {all,omop2fhir,omop2owl,owl2fhir} [{all,omop2fhir,omop2owl,owl2fhir} ...]
                        Warning: Option currently in development. Does not differentiate between different settings (particularly --vocabs
                        and --relationships). It considers all cached files relevant each time you run it using a given --out-dir. So if
                        you want to use caching and also want to change your settings, either (a) clear your --out-dir or (b) use a
                        different --out-dir. Caching options: `all`: Turns on all cache options. `omop2fhir`: Saves any intermediate files
                        at the top level of this pipeline, which basically entails caching of output from omop2owl which is used by
                        owl2fhir. `omop2owl`: Intermediates used by that package, such as robot templates. `owl2fhir`: Intermediates used
                        by that package, such as Obographs JSON.
```
