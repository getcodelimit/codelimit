import plotly.express as px

from codelimit.common.SourceFolder import SourceFolder
from codelimit.common.report.ReportReader import ReportReader


def walk_tree(tree: dict[str, SourceFolder], folder_name: str) -> tuple[
    list[str], list[str], list[str], list[int]]:
    ids = []
    names = []
    parents = []
    values = []
    folder = tree[folder_name]
    if folder_name == './':
        folder_name = ''
    for entry in folder.entries:
        if entry.is_folder():
            entry_folder_name = f"{folder_name}{entry.name}"
            ids.append(entry_folder_name)
            names.append(entry.name)
            values.append(sum(tree[entry_folder_name].profile))
            parents.append(folder_name)
            [fi, fn, fp, fv] = walk_tree(tree, entry_folder_name)
            ids.extend(fi)
            names.extend(fn)
            parents.extend(fp)
            values.extend(fv)
        else:
            ids.append(entry.name)
            names.append(entry.name)
            values.append(sum(entry.profile()))
            parents.append(folder_name)
    return ids, names, parents, values


def render_treemap():
    with open('/Users/rob/projects/kepler/NightNurseApp/.codelimit_cache/codelimit.json', 'r') as f:
        json = f.read()
    codebase = ReportReader.from_json(json).codebase
    ids, names, parents, values = walk_tree(codebase.tree, './')
    fig = px.treemap(
        ids=ids,
        names=names,
        parents=parents,
        values=values,
        color=values,
        color_continuous_scale='Bluered',
        # color_discrete_map=
        # maxdepth=3
        # names=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        # parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        # uniformtext=dict(minsize=9, mode='show'),
    )
    fig.show()


if __name__ == "__main__":
    render_treemap()
