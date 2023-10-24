"""
Tools for processing ExSourceFiles.
"""
from os import path
import json
import subprocess
from copy import deepcopy
from tempfile import gettempdir
import logging
import yaml

from exsource_tools import utils
from exsource_tools.exsource import ExSource

logging.basicConfig()
LOGGER = logging.getLogger('exsource')
LOGGER.setLevel(logging.INFO)



UNSTAGED = 0
PENDING = 1
SKIPPED = 2
PROCESSED = 3

CONTINUE = 10
SKIP = 11
DELAY = 12
UNCHANGED = 13
UNCHANGED_INCOMPLETE = 14
CHANGED = 15
NEW = 16


def load_exsource_file(filepath):
    """
    Load an exsource file from the inupt filepath. An ExSource object is returned
    """
    file_format = utils.exsource_file_format(filepath, "read")
    with open(filepath, 'r', encoding="utf-8") as file_obj:
        file_content = file_obj.read()
        if file_format == "JSON":
            input_data = json.loads(file_content)
        else:
            #only other option is YAML
            input_data = yaml.safe_load(file_content)
    return ExSource(input_data)


class ExSourceProcessor:
    """
    This class processes the data in the exsource file to create all the ouputs.
    Currently it only works for certain OpenSCAD and FreeCAD exports
    """

    def __init__(self,
                 exsource_def,
                 previous_exsource=None,
                 exsource_out_path=None,
                 headless=False):

        self.headless = headless
        self._exsource = deepcopy(exsource_def)
        self._exsource_prev = previous_exsource
        self._exsource_out_path = exsource_out_path
        self._all_output_files = {output.filepath: UNSTAGED for output in self._exsource.all_output_files}

    def check(self):
        """
        Check which files require exporting
        """
        #TODO use _check_dependencies
        if self._exsource_prev is None:
            print("No exsource-out found.")
            return
        for export_id, export in self._exsource.exports.items():
            if export_id not in self._exsource_prev.exports:
                print(f"Export {export_id} not in previous run.")
            else:
                prev_export = self._exsource_prev.exports[export_id]
                #Always reprocess is dependencies aren't exhaustive
                if export.unchanged_from(prev_export):
                    if prev_export.dependencies_exhaustive:
                        print(f"Export {export_id}: is unchanged, no processing needed")
                    else:
                        print(f"Export {export_id}: is unchanged, however not all dependencies are known")
                else:
                    print(f"Export {export_id}: has changed, any ouput files need regenerating.")

    def make(self):
        """
        Process all exsource exports (if possible)
        """
        self._all_output_files = {output.filepath: PENDING for output in self._exsource.all_output_files}
        iteration = 0
        unprocessed_exports = self._exsource.exports
        while len(unprocessed_exports) > 0:
            #TODO: make less simplistic
            iteration += 1
            if iteration > len(self._exsource.exports):
                raise RuntimeError("Circular dependencies in exsource file")

            unprocessed_exports = self._process_exports(unprocessed_exports)

        outpath = self._exsource_out_path
        if outpath is None:
            outpath = 'exsource-out.yml'
        self._exsource.save(outpath)

    def _process_exports(self, exports_to_process):
        unprocessed_exports = {}

        for export_id, export in exports_to_process.items():
            LOGGER.info("Processing export: %s", export_id)
            app = export.application

            dep_action = self._check_dependencies(export_id, export)

            if dep_action == CONTINUE:
                if app.lower() == "openscad":
                    self._process_openscad(export)
                elif app.lower() == "freecad":
                    self._process_freecad(export)
                else:
                    LOGGER.warning("Skipping %s as no methods available process files with %s",
                                   export_id,
                                   app)
                    for output in export.output_files:
                        self._all_output_files[output.filepath] = SKIPPED
            elif dep_action == SKIP:
                for output in export.output_files:
                    self._all_output_files[output.filepath] = SKIPPED
                LOGGER.warning("Skipping %s it has skipped dependencies", export_id)
            elif dep_action == DELAY:
                unprocessed_exports[export_id] = export
                LOGGER.info("Delaying %s as it has unprocessed dependencies", export_id)
            elif dep_action == UNCHANGED:
                #Move all extra information over if eveything is unchanged since last run.
                new_export = deepcopy(self._exsource_prev.exports[export_id])
                new_export.name = export.name
                new_export.description = export.description
                self._exsource.exports[export_id] = new_export

        return unprocessed_exports

    def _check_dependencies(self, export_id, export):
        """
        action to take based on dependency and source file status
        """
        # Store all hashes of all dependent files (both dependencies and source files)
        # before checking if changed
        if self._exsource_prev is not None:
            if export_id in self._exsource_prev.exports:
                prev_export = self._exsource_prev.exports[export_id]
                #Always reprocess is dependencies aren't exhaustive
                if prev_export.dependencies_exhaustive and export.unchanged_from(prev_export):
                    LOGGER.info("Export %s: is unchanged, no processing needed", export_id)
                    return UNCHANGED
        action = CONTINUE
        for dep in export.dependencies + export.source_files:
            dep.store_hash()
            if dep.filepath in self._all_output_files:
                dep_status = self._all_output_files[dep.filepath]
                if dep_status == SKIPPED:
                    return SKIP
                if dep_status == PENDING:
                    LOGGER.info("Dependent file: %s not yet processed", dep.filepath)
                    action = DELAY
                    #No return here as another dependency might require it be skipped

        return action

    def _process_openscad(self, export):
        #TODO: Tidy up
        assert len(export.output_files) == 1, "OpenSCAD expects only one output"
        output = export.output_files[0]
        assert len(export.source_files) == 1, "Openscad expects only one source file"
        source = export.source_files[0]

        require_x = True if output.filepath.lower().endswith('.png') else False


        params = []
        for parameter in export.parameters:
            if isinstance(export.parameters[parameter], (float, int)):
                par = str(export.parameters[parameter])
            elif isinstance(export.parameters[parameter], bool):
                #ensure lowercase for booleans
                par = str(export.parameters[parameter]).lower()
            elif isinstance(export.parameters[parameter], str):
                par = export.parameters[parameter]
            else:
                LOGGER.warning("Can only process string, numerical or boolean arguments "
                               "for OpenSCAD. Skipping parameter %s", parameter)
                continue
            params.append("-D")
            params.append(f"{parameter}={par}")

        executable = "openscad"

        depfilename = output.filepath + ".d"
        utils.add_directory_if_needed(output.filepath)
        openscad_file_args = ["-d", depfilename, "-o", output.filepath, source.filepath]
        options = utils.split_app_options(export.app_options)
        openscad_args = options + params + openscad_file_args
        try:
            if self.headless and require_x:
                xrvb_args = ['xvfb-run',
                             '--auto-servernum',
                             '--server-args',
                             '-screen 0 1024x768x24']
                args = xrvb_args + [executable] + openscad_args
            else:
                args = [executable] + openscad_args
            ret = subprocess.run(args, check=True, capture_output=True)
            #print std_err as OpenSCAD uses it to print rather than std_out
            std_err = ret.stderr.decode('UTF-8')
            print(std_err)
        except subprocess.CalledProcessError as error:
            std_err = error.stderr.decode('UTF-8')
            raise RuntimeError(f"\n\nOpenSCAD failed create file: {output} with error:\n\n"
                               f"{std_err}") from error
        output.store_hash()
        depsfile = utils.Depsfile(depfilename)
        assert len(depsfile.rules) == 1, "Expecting only one rule in and openscad deps file"
        assert len(depsfile.rules[0].outputs) == 1, "Expecting only one output to be specified in the openscad depsile"
        assert depsfile.rules[0].outputs[0] == output, "depsfile output doens't match expected file"
        for dep in depsfile.rules[0].dependencies:
            if dep not in export.source_files+export.dependencies:
                export.add_dependency(dep, store_hash=True)
        export.mark_dependencies_exhaustive()
        self._all_output_files[output.filepath] = PROCESSED

    def _process_freecad(self, export):
        #TODO: Tidy up

        outputs = export.output_files
        sources = export.source_files
        assert len(sources) == 1, "FreeCAD expects only one source file"
        sourcefile = sources[0].filepath
        assert len(export.app_options) == 0, "Cannot apply options to FreeCAD"
        for parameter in export.parameters:
            LOGGER.info("Cannot process parameters for FreeCAD skipping parameter %s",
                        parameter)
            continue

        for outfile_obj in outputs:
            outfile = outfile_obj.filepath
            utils.add_directory_if_needed(outfile_obj.filepath)
            if outfile.lower().endswith('.stp') or outfile.lower().endswith('.step'):
                macro = (f"doc = FreeCAD.openDocument('{sourcefile}')\n"
                         "body = doc.getObject('Body')\n"
                         f"body.Shape.exportStep('{outfile}')\n")
            elif outfile.lower().endswith('.stl'):
                macro = ("from FreeCAD import Mesh\n"
                         f"doc = FreeCAD.openDocument('{sourcefile}')\n"
                         "body = doc.getObject('Body')\n"
                         f"Mesh.export([body], '{outfile}')\n")
            tmpdir = gettempdir()
            macropath = path.join(tmpdir, "export.FCMacro")
            with open(macropath, 'w', encoding="utf-8") as file_obj:
                file_obj.write(macro)
            subprocess.run(["freecadcmd", macropath], check=True)
            outfile_obj.store_hash()
            self._all_output_files[outfile] = PROCESSED
