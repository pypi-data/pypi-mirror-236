from functools import wraps
from typing import Optional
from yaml import safe_load
import json


class inject_config:
    def __init__(self, config: object, first: Optional[bool] = True, use_kwarg: Optional[str] = None):
        """initializes the decorator

        Parameters
        ----------
        config : object
            configuration object to inject into function
        first : Optional[bool], optional
            inject config as first argument. if false as last argument, by default True
        use_kwarg : Optional[str], optional
            If specified, injects the config-object as a kwarg with the key specified in use_kwarg
            this overrides the "first" parameter, by default None
        """
        self._config = config
        self._first = first
        self._use_kwarg = use_kwarg

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._first and not self._use_kwarg:
                args = (self._config,) + args
            elif not self._use_kwarg:
                args = args + (self._config,)
            else:
                kwargs[self._use_kwarg] = self._config
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def from_json(cls, file: str, first: Optional[bool] = True, use_kwarg: Optional[str] = None):
        """inject config specified in a json_file

        Parameters
        ----------
        file : str
            path of json config file
        first : Optional[bool], optional
            inject config as first argument. if false as last argument, by default True
        use_kwarg : Optional[str], optional
            If specified, injects the config-object as a kwarg with the key specified in use_kwarg
            this overrides the "first" parameter, by default None
        """
        with open(file, "r", encoding="utf-8") as f:
            dict_ = json.loads(f.read())
        return cls(dict_, first, use_kwarg)

    @classmethod
    def from_yaml(cls, file: str, first: Optional[bool] = True, use_kwarg: Optional[str] = None):
        """inject config specified in a yaml-file

        Parameters
        ----------
        file : str
            path of json config file
        first : Optional[bool], optional
            inject config as first argument. if false as last argument, by default True
        use_kwarg : Optional[str], optional
            If specified, injects the config-object as a kwarg with the key specified in use_kwarg
            this overrides the "first" parameter, by default None
        """
        with open(file, "r", encoding="utf-8") as f:
            dict_ = safe_load(f)
        return cls(dict_, first, use_kwarg)

    @classmethod
    def from_loader(
        cls,
        loader: object,
        first: Optional[bool] = True,
        use_kwarg: Optional[str] = None,
        loader_args: Optional[tuple] = None,
        loader_kwargs: Optional[dict] = None,
    ):
        """inject config with custom loader object

        Parameters
        ----------
        loader : object
            Callable returning injected config-object
        first : Optional[bool], optional
            inject config as first argument. if false as last argument, by default True
        use_kwarg : Optional[str], optional
            If specified, injects the config-object as a kwarg with the key specified in use_kwarg
            this overrides the "first" parameter, by default None
        kwargs: any
            kwargs that get passed through to the loader
        """
        loader_kwargs = {} if not loader_kwargs else loader_kwargs
        loader_args = tuple() if not loader_args else loader_args
        return cls(loader(*loader_args, **loader_kwargs), first, use_kwarg)
