"""Search the web from your website."""

import collections
import random
import re
import sqlite3
import string

import black
import easyuri
import eng_to_ipa
import nltk
import pint
import pronouncing
import requests
import typesense
import web
import webagt
import webint_owner
import wn
import youtube_search
from RestrictedPython import (
    compile_restricted,
    limited_builtins,
    safe_builtins,
    utility_builtins,
)
from RestrictedPython.Eval import (
    default_guarded_getattr,
    default_guarded_getitem,
    default_guarded_getiter,
)
from RestrictedPython.PrintCollector import PrintCollector

app = web.application(__name__, prefix="search")
client = typesense.Client(
    {
        "nodes": [
            {
                "host": "localhost",
                "port": "8108",
                "protocol": "http",
            }
        ],
        "api_key": "hpAnnsIdJse2NejW8RFKKRZ8z2lfhRjWCNtWWvwNFWXTyB1Y",
        "connection_timeout_seconds": 2,
    }
)
ureg = pint.UnitRegistry()
books_schema = {
    "name": "books",
    "fields": [
        {"name": "title", "type": "string"},
        {"name": "authors", "type": "string[]", "facet": True},
        {"name": "publication_year", "type": "int32", "facet": True},
        {"name": "ratings_count", "type": "int32"},
        {"name": "average_rating", "type": "float"},
    ],
    "default_sorting_field": "ratings_count",
}
# client.collections.create(books_schema)
# with open("/tmp/books.jsonl") as jsonl_file:
#     client.collections["books"].documents.import_(jsonl_file.read().encode("utf-8"))


@app.wrap
def linkify_head(handler, main_app):
    """Ensure OpenSearch document is referenced from homepage."""
    yield
    if web.tx.request.uri.path == "":
        web.add_rel_links(
            search=(
                "/search/opensearch.xml",
                {
                    "type": "application/opensearchdescription+xml",
                    "title": "Angelo Gladding",
                },
            )
        )


def search_youtube(query):
    return youtube_search.YoutubeSearch(query, max_results=10).to_dict()


IW_HANDLE_RE = r"^@(?P<domain>[\w.]+)$"
AP_HANDLE_RE = r"^@(?P<user>[\w.]+)@(?P<domain>[\w.]+)$"


def iw_lookup(handle):
    match = re.match(IW_HANDLE_RE, handle)
    if match is None:
        return
    (domain,) = match.groups()
    return webagt.get(domain).card


def ap_lookup(handle):
    match = re.match(AP_HANDLE_RE, handle)
    if match is None:
        return
    user, domain = match.groups()
    for link in requests.get(
        f"https://{domain}/.well-known/webfinger?resource=acct:{user}@{domain}",
        headers={"Accept": "application/activity+json"},
    ).json()["links"]:
        if link["rel"] == "self":
            identity_url = link["href"]
            break
    else:
        return
    return webint_owner.ap_request(identity_url)


@app.control("")
class Search:
    """Search everything."""

    def get(self):
        """Return an index of data sources."""
        try:
            form = web.form("q")
        except web.BadRequest:
            return app.view.index()
        query = form.q

        conversion = None
        units = {
            # length
            "fm": ("femtometer", "femtometer", "femtometers"),
            "pm": ("picometer", "picometer", "picometers"),
            "nm": ("nanometer", "nanometer", "nanometers"),
            "μm": ("micron", "micron", "microns"),
            "mm": ("millimeter", "millimeter", "millimeters"),
            "cm": ("centimeter", "centimeter", "centimeters"),
            "dm": ("decimeter", "decimeter", "decimeters"),
            "m": ("meter", "meter", "meters"),
            "dam": ("decameter", "decameter", "decameters"),
            "hm": ("hectometer", "hectometer", "hectometers"),
            "km": ("kilometer", "kilometer", "kilometers"),
            "au": ("astronomical unit", "astronomical unit", "astronomical units"),
            "ly": ("light year", "light year", "light years"),
            "pc": ("parsec", "parsec", "parsecs"),
            "mil": ("mil", "mil", "mils"),
            "in": ("inch", "inch", "inches"),
            "ft": ("foot", "foot", "feet"),
            "yd": ("yard", "yard", "yards"),
            "mi": ("mile", "mile", "miles"),
            # temperature
            "f": ("fahrenheit", "°F"),
            "c": ("celsius", "°C"),
            "k": ("kelvin", "°K"),
            # area
            r"sq\ in": ("square inch", "square inch", "square inches"),
            r"sq\ ft": ("square foot", "square foot", "square feet"),
            r"sq\ yd": ("square yard", "square yard", "square yards"),
            r"sq\ mi": ("square mile", "square mile", "square miles"),
            "acre": ("acre", "acre", "acres"),
            "hectare": ("hectare", "hectare", "hectares"),
            # volume
            r"cu\ in": ("cubic inch", "cubic inch", "cubic inches"),
            r"cu\ ft": ("cubic foot", "cubic foot", "cubic feet"),
            r"cu\ yd": ("cubic yard", "cubic yard", "cubic yards"),
            r"cu\ cm": ("cubic centimeter", "cubic centimeter", "cubic centimeter"),
            "μl": ("microliter", "microliter", "microliters"),
            "l": ("liter", "liter", "liters"),
            "gal": ("gallon", "gallon", "gallons"),
            "qt": ("quart", "quart", "quarts"),
            "pt": ("pint", "pint", "pints"),
            "cup": ("cup", "cup", "cups"),
            "fl oz": ("fluid ounce", "fluid ounce", "fluid ounces"),
            "tbls": ("tablespoon", "tablespoon", "tablespoons"),
            "tspn": ("teaspoon", "teaspoon", "teaspoons"),
            # weight
            "μg": ("microgram", "microgram", "micrograms"),
            "mg": ("milligram", "milligram", "millagrams"),
            "g": ("gram", "gram", "grams"),
            "kg": ("kilogram", "kilogram", "kilograms"),
            "ct": ("carat", "carat", "carats"),
            "oz": ("ounce", "ounce", "ounces"),
            "lb": ("pound", "pound", "pounds"),
            "tn": ("short ton", "short ton", "short tons"),
            "t": ("metric ton", "metric ton", "metric tons"),
            "lt": ("long ton", "long ton", "long tons"),
            # time
            "as": ("attosecond", "attosecond", "attoseconds"),
            "fs": ("femtosecond", "femtosecond", "femtoseconds"),
            "ps": ("picosecond", "picosecond", "picoseconds"),
            "ns": ("nanosecond", "nanosecond", "nanoseconds"),
            "sh": ("shake", "shake", "shakes"),
            "μs": ("microsecond", "microsecond", "microseconds"),
            "ms": ("millisecond", "millisecond", "milliseconds"),
            "s": ("second", "second", "seconds"),
            "min": ("minute", "minute", "minutes"),
            "h": ("hour", "hour", "hours"),
            "d": ("day", "day", "days"),
            "wk": ("week", "week", "weeks"),
            "fn": ("fortnight", "fortnight", "fortnights"),
            "mo": ("month", "month", "months"),
            "yr": ("year", "year", "years"),
            "dec": ("decade", "decade", "decades"),
            "cen": ("century", "century", "centuries"),
            "ml": ("millennium", "millennium", "millennia"),
            # data
            "bit": ("bit", "bit", "bits"),
            "kb": ("kilobit", "kilobit", "kilobits"),
            "Mb": ("megabit", "megabit", "megabits"),
            "Gb": ("gigabit", "gigabit", "gigabits"),
            "Tb": ("terabit", "terabit", "terabits"),
            "Pb": ("petabit", "petabit", "petabit"),
            "Eb": ("exabit", "exabit", "exabit"),
            "byte": ("byte", "bytes", "bytes"),
            "kB": ("kilobyte", "kilobyte", "kilobytes"),
            "MB": ("megabyte", "megabyte", "megabytes"),
            "GB": ("gigabyte", "gigabyte", "gigabytes"),
            "TB": ("terabyte", "terabyte", "terabytes"),
            "PB": ("petabyte", "petabyte", "petabytes"),
            "EB": ("exabyte", "exabyte", "exabytes"),
            # speed
            "kph": ("kilometer per hour", "kilometer/hour", "kilometers/hour"),
            "kps": ("kilometer per second", "kilometer/second", "kilometers/second"),
            "mph": ("mile per hour", "mile/hour", "miles/hour"),
        }
        if match := re.match(
            rf"""^(?P<quantity>[\d.]+)(?P<from>({'|'.join(units)}))
                 \ to\ (?P<to>({'|'.join(units)}))$""",
            query,
            re.VERBOSE,
        ):
            matches = match.groupdict()
            from_quantity = float(matches["quantity"])
            from_sig = len(matches["quantity"].partition(".")[2])
            from_unit = units[matches["from"].replace(" ", r"\ ")]
            to_unit = units[matches["to"].replace(" ", r"\ ")]
            to_quantity = ureg.convert(
                float(from_quantity),
                getattr(ureg, from_unit[0].replace(" ", "_")),
                getattr(ureg, to_unit[0].replace(" ", "_")),
            )
            output_from_unit = from_unit[1]
            if len(from_unit) == 3 and from_quantity != 1:
                output_from_unit = from_unit[2]
            output_to_unit = to_unit[1]
            if len(to_unit) == 3 and to_quantity != 1:
                output_to_unit = to_unit[2]
            conversion = (
                f"{round(from_quantity, from_sig):n} {output_from_unit}",
                f"{round(to_quantity, from_sig):n} {output_to_unit}",
            )

        iw_profile = iw_lookup(query)
        ap_profile = ap_lookup(query)

        builtins = dict(safe_builtins)
        builtins.update(**limited_builtins)
        builtins.update(**utility_builtins)
        env = {
            "__builtins__": builtins,
            "_getiter_": default_guarded_getiter,
            "_getattr_": default_guarded_getattr,
            "_getitem_": default_guarded_getitem,
        }
        secret = "".join(random.choices(string.ascii_lowercase, k=20))
        try:
            formatted_query = black.format_str(query, mode=black.mode.Mode()).rstrip()
        except black.parsing.InvalidInput:
            formatted_query = None
        try:
            exec(compile_restricted(f"{secret} = {query}", "<string>", "exec"), env)
        except Exception as err:
            result = None
        else:
            result = env[secret]

        if re.match(r"^[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]$", query):
            raise web.SeeOther(f"/player/{query}")
        if query.startswith("!"):
            bang, _, query = query[1:].partition(" ")
            match bang:
                case "yt":
                    return app.view.youtube_results(query, search_youtube(query))
                case "imdb":
                    web.tx.response.headers["Referrer-Policy"] = "no-referrer"
                    url = easyuri.parse("https://www.imdb.com/find/")
                    url["q"] = query
                    raise web.SeeOther(url)
                case "ud":
                    web.tx.response.headers["Referrer-Policy"] = "no-referrer"
                    url = easyuri.parse("https://www.urbandictionary.com/define.php")
                    url["term"] = query
                    raise web.SeeOther(url)

        nltk.download("wordnet")
        word = query
        snow = nltk.stem.SnowballStemmer("english")
        stem = snow.stem(query)
        ipa_pronunciation = None
        cmu_pronunciation = None
        definition = None
        rhymes = []
        try:
            en = wn.Wordnet("oewn:2022")
        except (sqlite3.OperationalError, wn.Error):
            pass  # TODO download Open English WordNet `python -m wn download oewn:2022`
        else:
            try:
                definition = en.synsets(query)[0].definition()
            except IndexError:
                try:
                    definition = en.synsets(stem)[0].definition()
                except IndexError:
                    pass
        if definition:
            ipa_pronunciation = eng_to_ipa.convert(query)
            try:
                cmu_pronunciation = pronouncing.phones_for_word(query)[0]
            except IndexError:
                pass
            rhymes = pronouncing.rhymes(query)

        web_results = [
            (
                webagt.uri(webagt.uri(result.element.attrib["href"])["uddg"][0]),
                result.element.text if result.element.text is not None else "",
            )
            for result in webagt.get(
                f"https://html.duckduckgo.com/html?q={query}"
            ).dom.select(".result__a")
        ]

        code_projects = collections.Counter()
        code_files = collections.defaultdict(list)
        for code_project, code_file in web.application("webint_code").model.search(
            query
        ):
            code_projects[code_project] += 1
            code_files[code_project].append(code_file)

        # books = client.collections["books"].documents.search(
        #     {
        #         "q": query,
        #         "query_by": "authors,title",
        #         "sort_by": "ratings_count:desc",
        #     }
        # )
        books = {}

        return app.view.results(
            query,
            # scope,
            conversion,
            iw_profile,
            ap_profile,
            formatted_query,
            result,
            ipa_pronunciation,
            cmu_pronunciation,
            definition,
            rhymes,
            web_results,
            code_projects,
            code_files,
            books,
        )


@app.control("opensearch.xml")
class OpenSearch:
    """"""

    def get(self):
        web.header("Content-Type", "application/xml; charset=utf-8")
        return bytes(str(app.view.opensearch()), "utf-8")


@app.control("collections")
class Collections:
    """"""

    def get(self):
        return app.view.collections(client.collections.retrieve())
