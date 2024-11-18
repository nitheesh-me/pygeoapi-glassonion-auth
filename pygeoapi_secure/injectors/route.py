import fnmatch
from typing import Callable, Optional, Set
from flask import Flask


def apply_decorator_on_views(app: Flask, decorator: Callable, include: Optional[Set[str]] = None):
    include_patterns = set()
    exclude_patterns = set()

    if include:
        for pattern in include:
            if pattern.startswith('!'):
                exclude_patterns.add(pattern[1:])
            else:
                include_patterns.add(pattern)

    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint
        if include_patterns and not any(fnmatch.fnmatch(endpoint, pattern) for pattern in include_patterns):
            continue
        if exclude_patterns and any(fnmatch.fnmatch(endpoint, pattern) for pattern in exclude_patterns):
            continue
        view_func = app.view_functions[endpoint]
        app.view_functions[endpoint] = decorator(view_func)