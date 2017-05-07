#!/usr/bin/env python
import os
from conduit import create_app

base_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(base_path, 'config.cfg')
app = create_app(config_path)
