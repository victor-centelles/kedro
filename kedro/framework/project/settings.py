# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module provides settings of a Kedro project."""
from importlib import import_module
from typing import Dict, NamedTuple, Tuple

from kedro.framework.project.metadata import ProjectMetadata


class ProjectSettings(NamedTuple):
    """Structure holding project settings configured in `settings.py`"""

    disable_hooks_for_plugins: Tuple[str, ...] = ()
    hooks: Tuple[str, ...] = ()
    session_store: Dict[str, str] = {}


def _get_project_settings(project_metadata: ProjectMetadata) -> ProjectSettings:
    source_dir = project_metadata.source_dir
    package_name = project_metadata.package_name
    settings_path = source_dir / package_name / "settings.py"

    if settings_path.is_file():
        module = import_module(f"{package_name}.settings")
        project_settings = {
            "disable_hooks_for_plugins": tuple(
                getattr(module, "DISABLE_HOOKS_FOR_PLUGINS", ())
            ),
            "hooks": tuple(getattr(module, "HOOKS", ())),
            "session_store": getattr(module, "SESSION_STORE", {}),
        }
        return ProjectSettings(**project_settings)

    return ProjectSettings()  # default settings