import os
from collections import OrderedDict

from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from pattern_library import get_base_lookup_dir

# TODO: Decide if we need these to be configurable
pattern_types = ['atoms', 'molecules', 'organisms', 'templates', 'pages']
pattern_template_suffix = '.html'


def get_pattern_templates():
    templates = OrderedDict()

    base_lookup_dir = get_base_lookup_dir()
    lookup_dir = os.path.join(base_lookup_dir, 'patterns')

    for pattern_type in pattern_types:
        # We can't use defaultdict here, because Django templates
        # can't handle it properly: Django will try to resolve `templates.items`
        # as `templates['items']` not as `templates.items()`
        templates.setdefault(pattern_type, {})
        pattern_type_path = os.path.join(lookup_dir, pattern_type)

        for root, dirs, files in os.walk(pattern_type_path):
            # Do not allow patters to sit directly underneath the pattern_type_path dir
            if root == pattern_type_path:
                continue

            # Ignore folders without files
            if not files:
                continue

            pattern_subtype = os.path.relpath(root, pattern_type_path)
            templates[pattern_type].setdefault(pattern_subtype, [])

            for current_file in files:
                pattern_path = os.path.join(root, current_file)
                pattern_path = os.path.relpath(pattern_path, base_lookup_dir)

                # Include only templates ending with pattern template suffix
                if pattern_path.endswith(pattern_template_suffix):
                    try:
                        templates[pattern_type][pattern_subtype].append(
                            get_template(pattern_path)
                        )
                    except TemplateDoesNotExist:
                        pass

    return templates