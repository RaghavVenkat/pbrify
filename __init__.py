# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "pbrify",
    "author" : "Raghav Venkat",
    "description" : "Quick PBR node setup creator",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "Properties > Material > Quick PBR Generator: PBRify",
    "warning" : "",
    "category" : "Material",
    "support": "COMMUNITY",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
}

import bpy
from . pbrPanel import PbrifyInterface
from . pbrOp import PbrifyCreate

classes = (PbrifyCreate, PbrifyInterface)

register, unregister = bpy.utils.register_classes_factory(classes)  