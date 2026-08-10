
mkdir templates 
python3 scaffold.py user username password country_id:reference phone email
python3 scaffold.py country name
python3 scaffold.py domtom name
python3 scaffold.py domtomhaslanguage domtom_id:references language_id:references
python3 scaffold.py language name short_name
python3 scaffold.py word from_language_id:references to_language_id:references to word translation
python3 scaffold.py sentence from_language_id:references to_language_id:references content translation
