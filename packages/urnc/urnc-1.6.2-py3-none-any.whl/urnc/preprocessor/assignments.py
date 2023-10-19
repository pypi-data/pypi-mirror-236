import inspect
import re
from nbconvert.preprocessors.base import Preprocessor

import urnc.preprocessor.util as util
from urnc.preprocessor.util import Keywords

import urnc.logger as log


def replace_local_link(cell):
    if cell.cell_type != "markdown":
        return
    if not re.search(Keywords.ASSIGNMENT_LINK, cell.source, re.IGNORECASE):
        return
    log.dbg("Detected Link to assignment.")
    cell.source = re.sub(Keywords.ASSIGNMENT_REPLACE,
                         "#a-", cell.source, re.IGNORECASE)


class ProcessAssignments(Preprocessor):
    def preprocess(self, notebook, resources):
        for cell in notebook.cells:
            replace_local_link(cell)
            if util.has_tag(cell, util.Tags.ASSIGNMENT_START):
                eid = cell.metadata.assignment_id
                html = f"""
                    <a class="anchor" name="a-{eid}"></a>
                    <h3>   ✎    Assignment {eid}</h3>
                """
                clean = inspect.cleandoc(html)
                cell.source = re.sub(
                    Keywords.ASSIGNMENT_START, clean, cell.source, 1)
        return notebook, resources
