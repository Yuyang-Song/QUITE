from gpt import GPT
import json
import textwrap
result = []
gpt = GPT()
prompt = textwrap.dedent(
    f"""
<mission>
You are a professional DBA. Your task is to generate queries with 
a high number of join orders, long execution times, but returning a limited number of rows. You could make some redundent operations in the query to increase the execution time.
Additionally, the queries should have significant optimization potential through query rewriting. For example:

1. A high number of AND conditions in the FROM clause that should be moved to the WHERE clause
2. Nested and repeatedly used subqueries
3. Constant not folding
4. Predicate that could be pushdowned 


Below is the schema and data statistics of the database.
<data_statistics>:
'table: aka_name, rows: 901337', 'table: aka_title, rows: 361378', 'table: cast_info, rows: 36243321', 'table: char_name, rows: 3139793', 'table: comp_cast_type, rows: 3', 'table: company_name, rows: 234996', 'table: company_type, rows: 3', 'table: complete_cast, rows: 135085', 'table: info_type, rows: 112', 'table: keyword, rows: 134169', 'table: kind_type, rows: 6', 'table: link_type, rows: 17', 'table: movie_companies, rows: 2609128', 'table: movie_info_idx, rows: 1380034', 'table: movie_keyword, rows: 4523929', 'table: movie_link, rows: 29996', 'table: name, rows: 4167490', 'table: role_type, rows: 11', 'table: title, rows: 2527968', 'table: movie_info, rows: 14711167', 'table: person_info, rows: 2827456'
<schema>：
CREATE TABLE aka_name (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    name character varying,
    imdb_index character varying(3),
    name_pcode_cf character varying(11),
    name_pcode_nf character varying(11),
    surname_pcode character varying(11),
    md5sum character varying(65)
);

CREATE TABLE aka_title (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    title character varying,
    imdb_index character varying(4),
    kind_id integer NOT NULL,
    production_year integer,
    phonetic_code character varying(5),
    episode_of_id integer,
    season_nr integer,
    episode_nr integer,
    note character varying(72),
    md5sum character varying(32)
);

CREATE TABLE cast_info (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    movie_id integer NOT NULL,
    person_role_id integer,
    note character varying,
    nr_order integer,
    role_id integer NOT NULL
);

CREATE TABLE char_name (
    id integer NOT NULL PRIMARY KEY,
    name character varying NOT NULL,
    imdb_index character varying(2),
    imdb_id integer,
    name_pcode_nf character varying(5),
    surname_pcode character varying(5),
    md5sum character varying(32)
);

CREATE TABLE comp_cast_type (
    id integer NOT NULL PRIMARY KEY,
    kind character varying(32) NOT NULL
);

CREATE TABLE company_name (
    id integer NOT NULL PRIMARY KEY,
    name character varying NOT NULL,
    country_code character varying(6),
    imdb_id integer,
    name_pcode_nf character varying(5),
    name_pcode_sf character varying(5),
    md5sum character varying(32)
);

CREATE TABLE company_type (
    id integer NOT NULL PRIMARY KEY,
    kind character varying(32)
);

CREATE TABLE complete_cast (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer,
    subject_id integer NOT NULL,
    status_id integer NOT NULL
);

CREATE TABLE info_type (
    id integer NOT NULL PRIMARY KEY,
    info character varying(32) NOT NULL
);

CREATE TABLE keyword (
    id integer NOT NULL PRIMARY KEY,
    keyword character varying NOT NULL,
    phonetic_code character varying(5)
);

CREATE TABLE kind_type (
    id integer NOT NULL PRIMARY KEY,
    kind character varying(15)
);

CREATE TABLE link_type (
    id integer NOT NULL PRIMARY KEY,
    link character varying(32) NOT NULL
);

CREATE TABLE movie_companies (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    company_id integer NOT NULL,
    company_type_id integer NOT NULL,
    note character varying
);

CREATE TABLE movie_info_idx (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info character varying NOT NULL,
    note character varying(1)
);

CREATE TABLE movie_keyword (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    keyword_id integer NOT NULL
);

CREATE TABLE movie_link (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    linked_movie_id integer NOT NULL,
    link_type_id integer NOT NULL
);

CREATE TABLE name (
    id integer NOT NULL PRIMARY KEY,
    name character varying NOT NULL,
    imdb_index character varying(9),
    imdb_id integer,
    gender character varying(1),
    name_pcode_cf character varying(5),
    name_pcode_nf character varying(5),
    surname_pcode character varying(5),
    md5sum character varying(32)
);

CREATE TABLE role_type (
    id integer NOT NULL PRIMARY KEY,
    role character varying(32) NOT NULL
);

CREATE TABLE title (
    id integer NOT NULL PRIMARY KEY,
    title character varying NOT NULL,
    imdb_index character varying(5),
    kind_id integer NOT NULL,
    production_year integer,
    imdb_id integer,
    phonetic_code character varying(5),
    episode_of_id integer,
    season_nr integer,
    episode_nr integer,
    series_years character varying(49),
    md5sum character varying(32)
);

CREATE TABLE movie_info (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info character varying NOT NULL,
    note character varying
);

CREATE TABLE person_info (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info character varying NOT NULL,
    note character varying
);

You should return the answer in json format as below:
{{
    "query": //
}}
    """
)
ans = []
MAX_LOOP = 10
money = 0.0
for i in range (MAX_LOOP):
    result = gpt.get_GPT_response(prompt,  json_format=True)
    money += float(gpt.calc_money(prompt, result))
    query = result["query"]
    # explain = result["explain"]
    tmp = {
        "id": i,
        "query": query,
    }
    ans.append(tmp)

with open("result.json", "w") as f:
    json.dump(ans, f, indent=4)

print(f"Total cost: {money} USD")