import jinja2


def string_to_html_file(html_string, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_string)


def create_html(path_template, info, path_css=""):

    name_template_index = path_template[0].split("/")[-1]
    path_template_index = path_template[0].replace(name_template_index, "")

    name_template_card = path_template[1].split("/")[-1]
    path_template_card = path_template[1].replace(name_template_card, "")

    env_card = jinja2.Environment(loader=jinja2.FileSystemLoader(path_template_card))
    template_card = env_card.get_template(name_template_card)
    html_card = template_card.render(info)

    env_index = jinja2.Environment(loader=jinja2.FileSystemLoader(path_template_index))
    template_index = env_index.get_template(name_template_index)
    html_index = template_index.render({"card": html_card})

    # print("***********************************************")
    # print(html_index)
    # print("***********************************************")
    output_file = "output.html"
    string_to_html_file(html_index, output_file)


if __name__ == "__main__":

    info = {"card": "templates/cardRotulo.html"}
    path_template = ["templates/index.html", "templates/cardRotulo.html"]
    path_css = "templates/styles.css"
    create_html(path_template, info, path_css)
