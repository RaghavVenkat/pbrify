# MIT License
# 
# Copyright (c) 2019 Raghav Venkat
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Addon Description
bl_info = {
    "name" : "pbrify",
    "author" : "Raghav Venkat",
    "description" : "Quick PBR Node Setup Generator for Blender Cycles and EEVEE Engine",
    "blender" : (2, 80, 0),
    "version" : (1 , 1, 0),
    "location" : "Properties > Material > Quick PBR Generator: PBRify",
    "warning" : "",
    "category" : "Material",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/RaghavVenkat/pbrify",
    "tracker_url": "https://github.com/RaghavVenkat/pbrify/issues"
}

import bpy
from . pbrPanel import PbrifyInterface
from . pbrOp import PbrifyCreate

classes = (PbrifyCreate, PbrifyInterface)

register, unregister = bpy.utils.register_classes_factory(classes)  
