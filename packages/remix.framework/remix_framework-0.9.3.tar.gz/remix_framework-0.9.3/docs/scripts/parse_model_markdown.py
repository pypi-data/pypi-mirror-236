"""REMix Model Markdown documentation parser

This script transforms an expected format inside of the GAMS code documentation
into makdown files that can then be loaded in the documentation. You can run
this as a normal python script or import the "compile_markdown_from_model"
function to integrate it with other code.

Anything that comes after a "* //" in the GAMS code will be interpreted as
markdown. This is a project specific script not designed to be reusable with
other GAMS projects.
"""
# %%
import json
from pathlib import Path
import os
import re
from remix.framework.schema.templates import sm
import sys

# Constant value declaration
SOURCE_PATH = "remix/framework/model/source"
DOCUMENTATION_PATH = "docs/documentation/tech-docs/remix.model"
OEO_BASE_IRI = "http://openenergy-platform.org/ontology/oeo/"
MISSING_TERM_TRACKING = "https://github.com/OpenEnergyPlatform/ontology/issues"
BFO_BASE_IRI = "http://purl.obolibrary.org/obo/"
TEX_FILE_PATH = "docs/scripts/remix.tex"
CUSTOM_MAPPINGS_FILE = "docs/scripts/mappings.json"
HEADER = "| Symbol | Name | Title |  Description | Constraints | Type | Unit | Concept |\n"
SEPARATOR =  "| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |\n"
GENERIC = "| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |\n"
TABLE_LENGTH = 8
RENAMES = {
    "postcalc_declaration": "output_reference"
}
schemas = sm.get_schemas("latest")
# %%
def main():
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
        if Path(base_dir).exists():
            compile_markdown_from_model(base_dir)
        else:
            raise ValueError(f"The given directory: {base_dir} does not exists.")
    else:
        compile_markdown_from_model(".")

def compile_markdown_from_model(base_directory):
    source_directory = Path(base_directory).joinpath(SOURCE_PATH).resolve()
    if not source_directory.exists():
        raise ValueError(f"The source directory: {source_directory} does not exist.")
    output_directory = Path(base_directory).joinpath(DOCUMENTATION_PATH).resolve()
    tex_file = Path(base_directory).joinpath(TEX_FILE_PATH).resolve()
    file_list = [os.path.join(root, cur_file)
             for root, dirs, files in os.walk(source_directory)
             for cur_file in files
             if (".gms" in cur_file)]
    target_files = {s: name_target_files(s, source_directory, output_directory) for s in file_list}
    # Construct map of equations
    equations_raw, variables_raw, parameters_raw, symbols_raw, sets_raw = extract_tex_data(tex_file)
    equation_dict = build_equation_dictionary(equations_raw)
    set_table = build_set_table(sets_raw)
    set_input_files_content = build_input_files_content()
    variables_tables = build_variables_tables(variables_raw)
    equation_dict = reformat_equations(equation_dict)
    custom_mappings = load_custom_mappings()
    os.makedirs(output_directory, exist_ok=True)
    readme_list = []
    accounting_buffer = {}
    for gams_file in file_list:
        # Extract data from the .gms files
        md, tables = extract_source_data(gams_file)
        # Construct the markdown file templates
        out_md = "".join([l.strip("\s") for l in md])
        # Construct map of markdowntables
        core_list = [core for core in custom_mappings["modules"].keys() if core in gams_file]
        core = custom_mappings["modules"][core_list[0]] if len(core_list) > 0 else "ANY"
        names_tables = [parse_markdown_table(t, custom_mappings["parameters"], core) for t in tables]
        table_dict = {n:t for n,t in names_tables}
        if "sets.gms" in gams_file:
            table_dict["special_table_sets"] = set_table
            table_dict["special_table_set_input_files"] = set_input_files_content

        variables_pair = get_variables(gams_file, variables_tables)
        if variables_pair[1] is not None:
             table_dict[variables_pair[0]] = variables_pair[1]
        # Construct map of placeholders with default empty value
        all_placeholders = re.findall("\{(.*?)\}", out_md)
        placeholders = {p: "" for p in all_placeholders}
        # Update the placeholders with the table values
        placeholders.update(table_dict)
        # Update the placeholders with the equation values
        this_equations_dict = {k: v for k,v in equation_dict.items() if k in placeholders.keys()}
        placeholders.update(this_equations_dict)
        placeholders.update({"ref": "{ref}"})
        # Use the placeholder map to apply the format into the markdown file
        out_md = out_md.format(**placeholders)
        out_md = out_md.replace("Title: ", "**Title**: ")
        out_md = out_md.replace("Description: ", "**Description**: ")
        # Apply custom parameter mappings
        out_md = find_and_replace_parameter_symbols(out_md, custom_mappings)
        # Hardcode parameter replacement of Incidence Model
        out_md = out_md.replace("incidenceModel_{n, l}  \\neq  0", "\\neg incidence_{n, l}")
        # Find the output path using a map
        out_path = target_files[gams_file]
        # Add md header
        title = " ".join(Path(out_path).stem.split("_")).capitalize()
        out_md = add_header(out_md, title)
        # Write the output file
        out_md = out_md.replace("%curly_open%", "{")
        out_md = out_md.replace("%curly_close%", "}")
        if "accounting_input"in str(out_path):
            accounting_buffer["accounting_input"] = (out_path, out_md)
        elif "accounting_equations"in str(out_path):
            accounting_buffer["accounting_equations"] = (out_path, out_md)
        else:
            status = write_out(out_md,out_path)
            if status == 0:
                print("Parsed: {}".format(gams_file))
                readme_list.append(out_path.name)

    write_accounting(accounting_buffer)

def extract_source_data(source_file: Path):
    """Open source_file and extract the markdown templates [markdown],
    and the raw parameter tables [tables]
    """
    with open(source_file, "r") as f:
        lines = f.readlines()
    chunk = "".join(lines)
    markdown = get_markdown(lines)
    tables = get_tables(chunk)
    return markdown, tables

def get_markdown(string_lines):
    """Look for all the lines containing * // in the file and return them as a list
    """
    markdown = [l for l in string_lines if l.startswith("* //")]
    markdown = [m.replace("* //", "").strip("/s") for m in markdown]
    return markdown

def get_tables(chunk):
    """Find parameter tables based on a regex pattern
    """
    all_tables = re.findall(r'(?s)(\*\s\/\/\s\{table_.*?)(?=/;)', chunk, re.IGNORECASE)
    return all_tables

def parse_markdown_table(raw, mappings, core):
    """Transform the list of parameter strings into a markdown table.
    """
    # Harcoding exception for Links
    if "accounting_indicatorBounds_links" in raw:
        core = "J"
    raw_list = raw.split("\n")
    name = raw_list[0].replace("* //", "").strip().replace("{","").replace("}","")
    elements = [l.strip() for l in raw_list if len(l.strip()) != 0]
    elements = [e for e in elements if re.match(r"\w+\s+\"\w+",e)]
    elements = [re.sub("\s+\"", "|",e).strip(",").split("|") for e in elements]
    elements = [[sub.replace("\"", "").strip(" ") for sub in e if len(sub)>0] for e in elements]
    elements = [[f"${mappings[e[0]]}$"] + e if e[0] in mappings.keys() else [f"${e[0]}$"] + e for e in elements]
    # Regex magic to replace values in the tables
    elements = [[e[0].replace(f"{e[1]}",mappings[f"{e[1]}{core}"])] + e[1:] if f"{e[1]}{core}" in mappings.keys() else [e[0]] + e[1:]  for e in elements]
    # [element.extend(["required"]) if "required:true" in element[-1] else element.extend(["optional"])  for element in elements]
    # Get table domain from schemas
    domain_sets = [f["fields"] for f in schemas.get(name.replace("table_", ""), {"foreignKeys": []}).get("foreignKeys")]
    domain = []
    for ds in domain_sets:
        domain.extend(ds)
    domain = ", ".join(domain)
    REFERENCE = f"({name.lower()})=\n"
    DOMAIN = f"**Domain**: {domain}  "
    table = DOMAIN + "\n" + REFERENCE + HEADER + SEPARATOR

    for element in elements:
        padded = [element[i] if i < len(element) else "---" for i in range(TABLE_LENGTH) ]
        if ":" in padded[-1]:
            code, label = padded[-1].split(":")
            if "OEO_" in code:
                padded[-1] = f"[{label}]({OEO_BASE_IRI}{code})"
            if "BFO_" in code:
                padded[-1] = f"[{label}]({BFO_BASE_IRI}{code})"
            if "MISSING_TERM" in code:
                #padded[-1] = f'<span style="color:red">[{padded[-1]}]({MISSING_TERM_TRACKING})</span>'
                padded[-1] = f'<a href="{MISSING_TERM_TRACKING}" style="color: red; text-decoration: underline;">Missing: {label}</a>'
        padded[3] = padded[3].replace(";", "<br />").strip("<br />")
        padded[3] = padded[3].replace(":", ": ")
        table += GENERIC.format(*padded)
    return name, table

def name_target_files(original_dir, source_directory, output_directory):
    source_name = source_directory.name
    original_path = Path(original_dir)
    parent = original_path.parent.name
    file_name = original_path.name.replace(".gms", ".md")
    new_name = "_".join([parent,file_name]) if parent != source_name else file_name
    stem = Path(new_name).stem
    if stem in RENAMES:
        new_name = new_name.replace(stem, RENAMES[stem])
    target_dir = output_directory.joinpath(new_name)
    return target_dir

def write_out(chunk, filepath):
    if len(chunk) != 0:
        with open(filepath, "w") as fil:
            for line in chunk.split("\n"):
                if (len(line)> 0) and (line[0] != "#"):
                    line = line.strip() + "  \n"
                fil.write(line)
            return 0
    return 1

def extract_tex_data(tex_file):
    with open(tex_file, "r") as file:
        string = file.read()
    sets_raw = re.findall(r'(?s)(\\subsection\*\{Sets\}.*?)(?=.\\end\{tabularx\})', string)
    variables_raw = re.findall(r'(?s)(\\subsection\*\{Variables\}.*?)(?=.\\end\{tabularx\})', string)
    parameters_raw = re.findall(r'(?s)(\\subsection\*\{Parameters\}.*?)(?=.\\end\{tabularx\})', string)
    symbols_raw = re.findall(r'(?s)(\\subsection\*\{Symbols\}.*?)(?=.\\end\{tabularx\})', string)
    equations_raw = re.findall(r'(?s)(\\section\*\{Equation Definitions\}.*?)(?=.\\hrule\s+\n\\bigskip)', string)[0]
    equations_raw = equations_raw.replace("\\textcolor", "\\color")
    equations_raw = re.sub(r"\n\$\s+\\vspace\{5pt\}\n", "\n$\n", equations_raw)
    pattern = r'\\text\{(.*?)\}'
    replacement = r'\1'
    equations_raw = re.sub(pattern, replacement, equations_raw)
    pattern = r'\\texttt\{(.*?)\}'
    replacement = r'\1'
    equations_raw = re.sub(pattern, replacement, equations_raw)
    pattern = r'\\color\{black\}\{(.*?)\}'
    replacement = r'\1'
    equations_raw = re.sub(pattern, replacement, equations_raw)
    return equations_raw, variables_raw, parameters_raw, symbols_raw, sets_raw

def build_equation_dictionary(equations_raw):
    individual_equations = re.findall(r'(?s)(\\subsubsection\*\{\$.*?)(?=.\\subsubsection)', equations_raw)
    # Find the last equation
    last_equation = re.findall(r'(?s)(\\subsubsection\*\{\$Eq\\\_accounting\\\_objective\$\}.*?)(?=.\$\s\\vspace\{5pt\})', equations_raw)
    individual_equations.extend(last_equation)
    return {get_label(eq): get_parsed_equation(eq) for eq in individual_equations}

def build_set_table(sets_raw):
    header = "| Symbol | Name | Domain | Description | \n"
    separator =  "| ------ | ------ | ------ | ------ |\n"
    individual_sets = re.findall(r'(?s)(\n.*?)(?=\\\\)', sets_raw[0])
    individual_sets = [st for st in individual_sets if "&" in st]
    individual_sets = [[element.strip() for element in st.split("&")] for st in individual_sets]
    individual_sets[1][0] = individual_sets[1][0].replace("\\hline \n\\endhead \n", "")
    # Only consider Sets from the set file
    individual_sets = [st for st in individual_sets if st[2] != ""]
    # Get rid of the header
    individual_sets = individual_sets[1:]
    multiple_sets = [i for i in individual_sets if "," in i[0]]
    singles_sets = [i for i in individual_sets if not "," in i[0]]
    new_sets= []
    for u in multiple_sets:
        base = u[1:]
        collection = u[0]
        for c in collection.split(","):
            current = [c.strip()] + base
            singles_sets.append(current)
    for v in singles_sets:
        domain = f"${v[1]}$"
        if "(" in v[0]:
            symbol = v[0].split("(")[0]
            name = v[0].split("(")[1].split(")")[0]
        else:
            symbol = v[0]
            name = v[0]
        stripped = symbol.strip()
        formated= f"${stripped}$"
        new_sets.append([formated, name, domain, v[-1]])
    # Join common symbols
    unique_sets = set([s[0] for s in new_sets])
    out_sets = []
    for u in unique_sets:
        current_set = [n for n in new_sets if n[0] == u][0]
        all_symbols = [n[1] for n in new_sets if n[0] == u]
        if len(all_symbols) > 1:
            symbols = ", ".join(all_symbols)
        else:
            symbols = all_symbols[0]
        current_set[1] = symbols
        out_sets.append(current_set)
    out_sets.sort(key=lambda x: x[0].strip("$"))
    out_sets = ["|"+ "|".join(s) + "| \n" for s in out_sets]
    table = header + separator
    for element in out_sets:
        table += element
    table = table.replace("|*|", "|Universe(*)|")
    return table

def convert_to_table(variables):
    header = "| Symbol | Name | Domain | Description | \n"
    separator =  "| ------ | ------ | ------ |  ------ | \n"
    new_vars = []
    for v in variables:
        domain = f"${v[1]}$"
        if "(" in v[0]:
            symbol = v[0].split("(")[0]
            name = v[0].split("(")[1].split(")")[0]
        else:
            symbol = v[0]
            name = v[0]
        symbol= f"${symbol}$"
        new_vars.append([symbol, name, domain, v[-1]])
    table_elements = ["|"+ "|".join(s) + "| \n" for s in new_vars]
    table = header + separator
    for element in table_elements:
        table += element
    table = table.replace("|*|", "|Universe(*)|")
    return table

def build_variables_tables(variables_raw):
    individual_variables = re.findall(r'(?s)(\n.*?)(?=\\\\)', variables_raw[0])
    individual_variables = [vrs for vrs in individual_variables if "&" in vrs]
    individual_variables = [[element.strip() for element in vrs.split("&")] for vrs in individual_variables]
    individual_variables[1][0] = individual_variables[1][0].replace("\\hline \n\\endhead \n", "")
    # Get rid of the header
    individual_variables = individual_variables[1:]
    # converter variables
    converter_variables = [vrs for vrs in individual_variables if (vrs[0].startswith("conv\\") | vrs[0].startswith("A") | vrs[0].startswith("V") )]
    # storage variables
    storage_variables = [vrs for vrs in individual_variables if (vrs[0].startswith("stor") | vrs[0].startswith("S") | vrs[0].startswith("L") | vrs[0].startswith("M")| vrs[0].startswith("N")| vrs[0].startswith("K"))]
    # transport variables
    transport_variables = [vrs for vrs in individual_variables if (vrs[0].startswith("tran") | vrs[0].startswith("F") | vrs[0].startswith("E")| vrs[0].startswith("D") )]
    # sourcesink variables
    sourcesink_variables = [vrs for vrs in individual_variables if (vrs[0].startswith("sourcesink") | vrs[0].startswith("Q"))]
    # accounting variables
    accounting_variables = [vrs for vrs in individual_variables if (vrs[0].startswith("accounting")| vrs[0].startswith("I") | vrs[0].startswith("J")| vrs[0].startswith("C") | vrs[0].startswith("H") | vrs[0].startswith("R") )]

    output_tables = {
        "special_table_converter_variables": convert_to_table(converter_variables),
        "special_table_storage_variables": convert_to_table(storage_variables),
        "special_table_transport_variables": convert_to_table(transport_variables),
        "special_table_sourcesink_variables": convert_to_table(sourcesink_variables),
        "special_table_input_variables": convert_to_table(accounting_variables),
    }
    return output_tables

def get_variables(name, tables):
    name = Path(name).as_posix()
    table_name = "special_table_{}_variables".format(name.split(".")[0].split("/")[-1])
    table = tables.get(table_name, None)
    return (table_name, table)
def get_label(raw_equation):
    return re.findall(r'(?<=(\\label\{))(.*?)(?=(\}))', raw_equation)[0][1]

def get_parsed_equation(raw_equation):
    TOP = "\n$$\n"
    BOT = "\n$$\n"
    MID = "\n$$\n\n$$\n"
    equation = raw_equation.split("\n$\n")
    start_exclusion = "\\subsubsection*"
    full_exclussion = ["\\hfill", "\\hrule"]
    equation = [section for section in equation if not section.startswith(start_exclusion)]
    equation = [section.strip() for section in equation if section.strip() not in full_exclussion]
    # finetunning large equations
    if any(part in raw_equation for part in ["Eq\\_balance\\_commodities", "Eq\\_accounting\\_indicatorCalc", "Eq_accounting\\_indicatorCalc\\_links"]):
        bottom = equation[1:]
        new = [e + ")  +" for e in equation[0].split(")  + ")]
        new[-1] = new[-1][:-4]
        equation = new
        equation.extend(bottom)
    equation = TOP + MID.join(equation) + BOT
    return equation

def reformat_equations(equation_dict):
    new_dict = {}
    for k in equation_dict.keys():
        new_dict[k] = f"""({k})={reformat_equation(equation_dict[k])}"""
    return new_dict


def reformat_equation(equation):
    # (?s)(\[.*?\])(?=.)
    equation_noconditions = re.sub(r'(?s)(\[.*?)(?=.\])*\]', "", equation)
    equation_fixminus2 = re.sub(r'--', "-", equation_noconditions)
    return equation_fixminus2

def add_header(md, title):
    head = """---
title: {}
lang: en-UK
---

(remix_model_{}_label)=
""".format(title, title.lower().replace(" ", "_"))
    out_md = head + md if len(md) != 0 else md
    return out_md

def write_readme(file_list, output_directory):
    HEAD = """---
title: Technical Documentation
lang: en-UK
---

# Technical Documentation

## Table of contents
"""
    outfile= HEAD
    TEMPLATE = "\n[{0}]({1}.md)\n"
    for file in file_list:
        display_name = Path(file).stem
        outfile += TEMPLATE.format(" ".join(display_name.split("_")).capitalize(), display_name.lower())
    write_out(outfile, os.path.join(output_directory,"README.md"))

def build_input_files_content():
    resources = sm.get_resources()
    sets = {sc:it for sc, it in resources.items() if "set_" in sc}
    content= ""
    for cnt in sets.values():
        name = cnt["name"]
        HEADER3 = f"### {name}\n"
        title = cnt["title"]
        TITLE = f"**Title**: {title}  \n"
        description = cnt["description"]
        DESCRIPTION = f"**Description**: {description}  \n"
        set_markdown = HEADER3 + TITLE + DESCRIPTION
        content += set_markdown
    return content

def find_and_replace_parameter_symbols(markdown_file, all_mappings):
    # This is currently broken, only works for converter, have to implement something that considers all of  the
    # Modules!!
    mappings = all_mappings["parameters"]
    parameter_variables = re.findall(r'(?s)(Parameter\\\_[A-Z]\_{.*?)(?=\})', markdown_file)
    parameter_variables = [p + "}" for p in parameter_variables]
    type = {p: p.split("_")[1] for p in parameter_variables}
    all_indexes =  {p:[i.strip() for i in p.split("{")[-1].replace("}", "").split(",")] for p in parameter_variables}
    parameter_name = { p: i[-1] for p,i in all_indexes.items()}
    indexes_noname = { p: i[:-1]  for p,i in all_indexes.items()}
    replaced_names = {p: (mappings[i] if i in mappings.keys() else i) for p,i in parameter_name.items()}
    replaced_names = {p: (mappings[i + type[p]] if i + type[p] in mappings.keys() else i) for p,i in replaced_names.items()}
    replacer = {p: replaced_names[p] + "_{" + ", ".join(indexes_noname[p]).strip() + "}" for p in parameter_variables}
    for k, v in replacer.items():
        # Harcode boolean variable replacement
        if f"{k}  =  1" in markdown_file:
            markdown_file = markdown_file.replace(f"{k}  =  1",v)
        if f"{k}  =  0" in markdown_file:
            markdown_file = markdown_file.replace(f"{k}  =  0",f"\\neg {v}")

        markdown_file = markdown_file.replace(k,v)
    return markdown_file

def write_accounting(accounting_buffer):
    new_str = f"{accounting_buffer['accounting_input'][0]}"
    new_name = Path(new_str.replace("accounting_input", "accounting"))
    new_md = accounting_buffer["accounting_input"][1] + accounting_buffer["accounting_equations"][1]
    new_md = new_md.replace("# accounting_input", "# accounting")
    new_md = new_md.replace("# accounting_equations", "")
    new_md = new_md.replace("(remix_model_accounting_equations_label)=", "")
    write_out(new_md, new_name)

def load_custom_mappings():
    with open(CUSTOM_MAPPINGS_FILE, "r") as file:
        mappings = json.load(file)
    return mappings
if __name__=="__main__":
    main()
