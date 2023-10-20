# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************
import json
import re
from abc import ABCMeta, abstractmethod
from typing import Union

from ._typing import Any, Callable, Dict, List, MemoryUploadable, Optional, Type
from .convert_utils import fix_special_floats
from .json_encoder import NestedEncoder
from .utils import local_timestamp


class BaseMessage(metaclass=ABCMeta):
    @property
    @abstractmethod
    def type(self):
        pass

    @staticmethod
    def translate_message_class__to_handler_name(class_name):
        """
        This function turns the message class name to the equivalent function in the Message class.
        """
        class_name_splitted = re.findall("[A-Z][^A-Z]*", class_name)
        class_name_splitted_lowered = [word.lower() for word in class_name_splitted]
        method_name = "_".join(class_name_splitted_lowered[:-1])
        return "set_" + method_name

    @classmethod
    def create(cls, context, use_http_messages, **kwargs):
        # type: (Optional[str], bool, Dict[Any, Any]) -> BaseMessage
        if use_http_messages:
            return cls(**kwargs)
        else:
            return cls.create_websocket_message(context, **kwargs)

    @classmethod
    def create_websocket_message(cls, context, **kwargs):
        message = WebSocketMessage(context=context)
        method_name = cls.translate_message_class__to_handler_name(cls.__name__)
        method = getattr(message, method_name)
        method(**kwargs)
        return message

    def repr_json(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if (not key.startswith("_"))
        }

    def repr_json_batch(self):
        """To be defined by subclasses to return JSON dictionary representation to be used for batching"""
        pass

    def to_json(self):
        json_re = json.dumps(
            self.repr_json(), sort_keys=True, indent=4, cls=NestedEncoder
        )
        return json_re

    def non_null_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if (value is not None and not key.startswith("_"))
        }


class CloseMessage(BaseMessage):
    """A special message indicating Streamer to ends and exit"""

    type = "close"

    pass


class UploadFileMessage(BaseMessage):
    type = "file_upload"

    def __init__(
        self,
        file_path: str,
        upload_type: str,
        additional_params: Optional[Dict[str, Optional[Any]]],
        metadata: Optional[Any],
        size: int,
        clean: bool = True,
        critical: bool = False,
        on_asset_upload: Optional[Callable] = None,
        on_failed_asset_upload: Optional[Callable] = None,
    ) -> None:
        self.local_timestamp = local_timestamp()

        self.file_path = file_path
        self.upload_type = upload_type
        self.additional_params = additional_params
        self.metadata = metadata
        self.clean = clean
        self._size = size
        self._critical = critical
        self._on_asset_upload = on_asset_upload
        self._on_failed_asset_upload = on_failed_asset_upload

        # figName is not null and the backend fallback to figure_{FIGURE_NUMBER}
        # if not passed
        if (
            additional_params
            and "fileName" in additional_params
            and additional_params["fileName"] is None
        ):
            raise TypeError("file_name shouldn't be null")

    def non_null_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if (not key.startswith("_"))
        }


class UploadInMemoryMessage(BaseMessage):
    type = "file_upload"

    def __init__(
        self,
        file_like,  # type: MemoryUploadable
        upload_type,  # type: str
        additional_params,  # type: Dict[str, Optional[Any]]
        metadata,  # type: Optional[Any]
        size,  # type: int
        critical=False,  # type: bool
        on_asset_upload=None,  # type: Optional[Callable]
        on_failed_asset_upload=None,  # type: Optional[Callable]
    ):
        # type: (...) -> None
        self.local_timestamp = local_timestamp()

        self.file_like = file_like
        self.upload_type = upload_type
        self.additional_params = additional_params
        self.metadata = metadata
        self._size = size
        self._critical = critical
        self._on_asset_upload = on_asset_upload
        self._on_failed_asset_upload = on_failed_asset_upload

        # figName is not null and the backend fallback to figure_{FIGURE_NUMBER}
        # if not passed
        if (
            additional_params
            and "fileName" in additional_params
            and additional_params["fileName"] is None
        ):
            raise TypeError("file_name shouldn't be null")

    def non_null_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if (not key.startswith("_"))
        }


class RemoteAssetMessage(BaseMessage):
    type = "remote_file"

    def __init__(
        self,
        remote_uri,  # type: Any
        upload_type,  # type: str
        additional_params,  # type: Dict[str, Optional[Any]]
        metadata,  # type: Optional[Dict[str, str]]
        size,  # type: int
        critical=False,  # type: bool
        on_asset_upload=None,
        on_failed_asset_upload=None,
    ):
        # type: (...) -> None
        self.remote_uri = remote_uri
        self.upload_type = upload_type
        self.additional_params = additional_params
        self.metadata = metadata
        self._size = size
        self._critical = critical
        self._on_asset_upload = on_asset_upload
        self._on_failed_asset_upload = on_failed_asset_upload

    def non_null_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if (not key.startswith("_"))
        }


class OsPackagesMessage(BaseMessage):
    type = "os_packages"

    def __init__(self, os_packages):
        # type: (List[str]) -> None
        self.os_packages = os_packages

    def non_null_dict(self):
        return self.__dict__


class ModelGraphMessage(BaseMessage):
    type = "graph"

    def __init__(self, graph):
        # type: (str) -> None
        self.graph = graph

    def non_null_dict(self):
        return self.__dict__


class SystemDetailsMessage(BaseMessage):
    type = "system_details"

    def __init__(
        self,
        command,  # type: Union[str, List[str]]
        env,  # type: Optional[Dict[str, str]]
        hostname,  # type: str
        ip,  # type: str
        machine,  # type: str
        os_release,  # type: str
        os_type,  # type: str
        os,  # type: str
        pid,  # type: int
        processor,  # type: str
        python_exe,  # type: str
        python_version_verbose,  # type: str
        python_version,  # type: str
        user,  # type: str
    ):
        # type: (...) -> None

        self.command = command
        self.env = env
        self.hostname = hostname
        self.ip = ip
        self.machine = machine
        self.os = os
        self.os_release = os_release
        self.os_type = os_type
        self.pid = pid
        self.processor = processor
        self.python_exe = python_exe
        self.python_version = python_version
        self.python_version_verbose = python_version_verbose
        self.user = user

    def non_null_dict(self):
        return self.__dict__


class CloudDetailsMessage(BaseMessage):
    type = "cloud_details"

    def __init__(
        self,
        provider,  # type: str
        cloud_metadata,  # type: Dict[str, Any]
    ):
        # type: (...) -> None

        self.provider = provider
        self.cloud_metadata = cloud_metadata

    def non_null_dict(self):
        return self.__dict__


class ParameterMessage(BaseMessage):

    """The Message type to encapsulate named parameter value.
    The parameter value can be either float or the list of floats."""

    type = "parameter_msg"
    source_autologger = "auto-logged"
    source_cli = "cli"
    source_manual = "manual"

    def __init__(self, context=None, timestamp=None):
        # type: (Optional[str], Optional[int]) -> None
        if timestamp is None:
            timestamp = local_timestamp()

        self.context = context
        self.local_timestamp = timestamp

        # The following attributes are optional
        self.param = None  # type: Optional[Dict[str, Any]]
        self.params = None  # type: Optional[Dict[str, Any]]

    def set_param(self, name, value, step=None, source=source_autologger):
        # type: (str, Any, Optional[int], str) -> None
        safe_value = fix_special_floats(value)
        self.param = {
            "paramName": name,
            "paramValue": safe_value,
            "step": step,
            "source": source,
        }

    def set_params(self, name, values, step=None, source=source_autologger):
        # type: (str, List[Any], Optional[int], str) -> None
        safe_values = list(map(fix_special_floats, values))
        self.params = {
            "paramName": name,
            "paramValue": safe_values,
            "step": step,
            "source": source,
        }

    def get_param_name(self):
        # type: () -> Optional[str]
        """Returns the name of the parameter associated with this message."""
        if self.param is not None:
            return self.param["paramName"]
        elif self.params is not None:
            return self.params["paramName"]
        else:
            return None

    def get_source(self):
        """Returns the source of the parameter value"""
        param_dict = self._get_param_dict()
        if param_dict is not None:
            return param_dict.get("source")
        return None

    def _get_param_dict(self):
        # type: () -> Optional[Dict[str, Any]]
        if self.param is not None:
            return self.param
        elif self.params is not None:
            return self.params
        else:
            return None

    @classmethod
    def deserialize(cls, message_dict):
        # type: (Type['ParameterMessage'], Dict[str, Any]) -> 'ParameterMessage'
        """Recreate a ParameterMessage from its Dict representation"""
        parameter_message = cls(
            context=message_dict.get("context", None),
            timestamp=message_dict.get("local_timestamp", None),
        )

        if message_dict.get("param", None) is not None:
            parameter_message.set_param(
                message_dict["param"]["paramName"],
                message_dict["param"]["paramValue"],
                step=message_dict["param"]["step"],
                source=message_dict["param"].get(
                    "source", ParameterMessage.source_autologger
                ),
            )
        elif message_dict.get("params", None) is not None:
            parameter_message.set_params(
                message_dict["params"]["paramName"],
                message_dict["params"]["paramValue"],
                step=message_dict["params"]["step"],
                source=message_dict["params"].get(
                    "source", ParameterMessage.source_autologger
                ),
            )
        else:
            # to support an offline experiment generated with SDK version 2.0.12
            # (see test_offline_sender.py#test_backward_compatibility_2_0_12)
            pass

        return parameter_message

    def repr_json_batch(self):
        # type: () -> Dict[str, Any]
        repr_dict = dict()
        param_dict = self._get_param_dict()
        if param_dict is not None:
            repr_dict["parameterName"] = param_dict["paramName"]
            repr_dict["parameterValue"] = param_dict["paramValue"]
            repr_dict["step"] = param_dict["step"]
            repr_dict["source"] = param_dict["source"]

        repr_dict["context"] = self.context
        repr_dict["timestamp"] = self.local_timestamp
        return repr_dict


class MetricMessage(BaseMessage):
    type = "metric_msg"
    metric_key = "metric"

    """The Message type to encapsulate named metric value."""

    def __init__(self, context=None, timestamp=None):
        # type: (Optional[str], Optional[int]) -> None
        self.context = context
        self.metric = None  # type: Optional[Dict[str, Any]]
        if timestamp is None:
            timestamp = local_timestamp()

        self.local_timestamp = timestamp

    def set_metric(self, name, value, step=None, epoch=None):
        safe_value = fix_special_floats(value)
        self.metric = {
            "metricName": name,
            "metricValue": safe_value,
            "step": step,
            "epoch": epoch,
        }

    @classmethod
    def deserialize(cls, message_dict):
        # type: (Type['MetricMessage'], Dict[str, Any]) -> MetricMessage
        """Recreate a MetricMessage from its Dict representation"""
        metric_message = cls(
            context=message_dict.get("context", None),
            timestamp=message_dict.get("local_timestamp", None),
        )

        if message_dict.get(cls.metric_key, None):
            metric_message.set_metric(
                message_dict[cls.metric_key]["metricName"],
                message_dict[cls.metric_key]["metricValue"],
                step=message_dict[cls.metric_key].get("step", None),
                epoch=message_dict[cls.metric_key].get("epoch", None),
            )
        else:
            raise ValueError("no metric message data found")

        return metric_message

    def repr_json_batch(self):
        # type: () -> Dict[str, Any]
        repr_dict = dict(self.metric)
        repr_dict["context"] = self.context
        repr_dict["timestamp"] = self.local_timestamp
        return repr_dict

    def __str__(self):
        return "MetricMessage: %s" % self.repr_json_batch()


class InstalledPackagesMessage(BaseMessage):
    type = "installed_packages"

    def __init__(self, installed_packages):
        # type: (List[str]) -> None

        self.installed_packages = installed_packages

    def non_null_dict(self):
        return self.__dict__


class LogOtherMessage(BaseMessage):
    type = "log_other"

    def __init__(self, key, value):
        # type: (Any, Any) -> None

        self.key = key
        self.value = value

    def non_null_dict(self):
        return self.__dict__


class RemoteModelMessage(BaseMessage):
    type = "remote_model"

    def __init__(
        self,
        model_name: str,
        remote_assets: List[Dict[str, Optional[str]]],
        on_model_upload: Optional[Callable] = None,
        on_failed_model_upload: Optional[Callable] = None,
    ) -> None:
        self.model_name = model_name
        self.remote_assets = remote_assets
        self.on_model_upload = on_model_upload
        self.on_failed_model_upload = on_failed_model_upload

    def non_null_dict(self):
        return self.__dict__


class RegisterModelMessage(BaseMessage):
    type = "register_model"

    def __init__(
        self,
        experiment_id,
        model_name,
        version,
        workspace,
        registry_name,
        public,
        description,
        comment,
        tags,
        status,
        stages,
        upload_status_observer_callback,
        on_model_register,
        on_failed_model_register,
    ):
        self.experiment_id = experiment_id
        self.model_name = model_name
        self.version = version
        self.workspace = workspace
        self.registry_name = registry_name
        self.public = public
        self.description = description
        self.comment = comment
        self.tags = tags
        self.status = status
        self.stages = stages
        self.upload_status_observer_callback = upload_status_observer_callback
        self.on_model_register = on_model_register
        self.on_failed_model_register = on_failed_model_register

    def non_null_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if key
            not in [
                "upload_status_observer_callback",
                "on_model_register",
                "on_failed_model_register",
            ]
        }


class FileNameMessage(BaseMessage):
    type = "file_name"

    def __init__(self, file_name):
        # type: (str) -> None

        self.file_name = file_name

    def non_null_dict(self):
        return self.__dict__


class HtmlMessage(BaseMessage):
    type = "html"

    def __init__(
        self,
        html,  # type: str
    ):
        # type: (...) -> None

        self.html = html

    def non_null_dict(self):
        return self.__dict__


class HtmlOverrideMessage(BaseMessage):
    type = "htmlOverride"

    def __init__(self, htmlOverride):
        # type: (str) -> None

        self.htmlOverride = htmlOverride

    def non_null_dict(self):
        return self.__dict__


class GpuStaticInfoMessage(BaseMessage):
    type = "gpu_static_info"

    def __init__(self, gpu_static_info):
        # type: (List[Dict[str, Any]]) -> None

        self.gpu_static_info = gpu_static_info

    def non_null_dict(self):
        return self.__dict__


class GitMetadataMessage(BaseMessage):
    type = "git_metadata"

    def __init__(self, git_metadata):
        # type: (Dict[str, Any]) -> None

        self.git_metadata = git_metadata

    def non_null_dict(self):
        return self.__dict__


class SystemInfoMessage(BaseMessage):
    type = "system_info"

    def __init__(self, key, value):
        # type: (str, Any) -> None

        self.system_info = {
            "key": key,
            "value": value,
        }

    def non_null_dict(self):
        return self.__dict__


class LogDependencyMessage(BaseMessage):
    type = "log_dependency"

    def __init__(self, name, version, timestamp=None):
        # type: (Any, Any, int) -> None
        self.name = name
        self.version = version

        if timestamp is None:
            timestamp = local_timestamp()
        self.local_timestamp = timestamp


class StandardOutputMessage(BaseMessage):
    type = "standard_output"

    def __init__(self, output, stderr=False, context=None, timestamp=None):
        # type: (str, bool, str, int) -> None
        self.output = output
        self.stderr = stderr
        self.context = context

        if timestamp is None:
            timestamp = local_timestamp()
        self.local_timestamp = timestamp

    @classmethod
    def create(cls, context, use_http_messages, **kwargs):
        # type: (Optional[str], bool, Dict[Any, Any]) -> BaseMessage
        if use_http_messages:
            kwargs["context"] = context
            return StandardOutputMessage(**kwargs)
        else:
            return cls.create_websocket_message(context, **kwargs)

    @classmethod
    def deserialize(cls, message_dict):
        # type: (Type['StandardOutputMessage'], Dict[str, Any]) -> StandardOutputMessage
        """Recreate a StandardOutputMessage from its Dict representation"""
        stdout_message = cls(
            output=message_dict.get("output", None),
            stderr=message_dict.get("stderr", None),
            context=message_dict.get("context", None),
            timestamp=message_dict.get("local_timestamp", None),
        )
        return stdout_message


class WebSocketMessage(BaseMessage):
    """
    A bean used to send messages to the server over websockets.
    """

    type = "ws_msg"

    def __init__(self, context=None):
        self.local_timestamp = local_timestamp()

        # The following attributes are optional
        self.graph = None
        self.code = None
        self.stdout = None
        self.stderr = None
        self.fileName = None
        self.env_details = None
        self.html = None
        self.htmlOverride = None
        self.installed_packages = None
        self.os_packages = None
        self.log_other = None
        self.gpu_static_info = None
        self.git_meta = None
        self.log_dependency = None
        self.log_system_info = None
        self.context = context

    def set_log_other(self, key, value):
        self.log_other = {"key": key, "val": value}

    def set_log_dependency(self, name, version, timestamp=None):
        self.log_dependency = {"name": name, "version": version}
        if timestamp is not None:
            self.local_timestamp = timestamp

    def set_system_info(self, key, value):
        self.log_system_info = {"key": key, "value": value}

    def set_installed_packages(self, installed_packages):
        self.installed_packages = installed_packages

    def set_html(self, html):
        self.html = html

    def set_html_override(self, htmlOverride):
        self.htmlOverride = htmlOverride

    def set_code(self, code):
        self.code = code

    def set_standard_output(self, output, stderr=False, context=None, timestamp=None):
        self.stdout = output
        self.stderr = stderr
        if context is not None:
            self.context = context
        if timestamp is not None:
            self.local_timestamp = timestamp

    def set_file_name(self, file_name):
        self.fileName = file_name

    def set_gpu_static_info(self, gpu_static_info):
        self.gpu_static_info = gpu_static_info

    def set_git_metadata(self, git_metadata):
        self.git_meta = git_metadata

    def set_model_graph(self, graph):
        self.graph = graph

    def set_os_packages(self, os_packages):
        self.os_packages = os_packages

    def set_system_details(
        self,
        command,
        env,
        hostname,
        ip,
        machine,
        os_release,
        os_type,
        os,
        pid,
        processor,
        python_exe,
        python_version_verbose,
        python_version,
        user,
    ):
        self.env_details = {
            "command": command,
            "env": env,
            "hostname": hostname,
            "ip": ip,
            "machine": machine,
            "os_release": os_release,
            "os_type": os_type,
            "os": os,
            "pid": pid,
            "processor": processor,
            "python_exe": python_exe,
            "python_version_verbose": python_version_verbose,
            "python_version": python_version,
            "user": user,
        }

    def to_http_message(
        self,
    ) -> Union[
        LogOtherMessage,
        LogDependencyMessage,
        SystemInfoMessage,
        InstalledPackagesMessage,
        HtmlMessage,
        HtmlOverrideMessage,
        StandardOutputMessage,
        FileNameMessage,
        GpuStaticInfoMessage,
        GitMetadataMessage,
        ModelGraphMessage,
        OsPackagesMessage,
        SystemDetailsMessage,
    ]:
        """Converts this message into appropriate message supported by HTTP endpoint"""
        if self.log_other is not None:
            return LogOtherMessage(
                key=self.log_other["key"], value=self.log_other["val"]
            )
        elif self.log_dependency is not None:
            return LogDependencyMessage(
                name=self.log_dependency["name"],
                version=self.log_dependency["version"],
                timestamp=self.local_timestamp,
            )
        elif self.log_system_info is not None:
            return SystemInfoMessage(
                key=self.log_system_info["key"], value=self.log_system_info["value"]
            )
        elif self.installed_packages is not None:
            return InstalledPackagesMessage(installed_packages=self.installed_packages)
        elif self.html is not None:
            return HtmlMessage(html=self.html)
        elif self.htmlOverride is not None:
            return HtmlOverrideMessage(htmlOverride=self.htmlOverride)
        elif self.stdout is not None:
            return StandardOutputMessage(
                output=self.stdout,
                stderr=self.stderr,
                context=self.context,
                timestamp=self.local_timestamp,
            )
        elif self.fileName is not None:
            return FileNameMessage(file_name=self.fileName)
        elif self.gpu_static_info is not None:
            return GpuStaticInfoMessage(gpu_static_info=self.gpu_static_info)
        elif self.git_meta is not None:
            return GitMetadataMessage(git_metadata=self.git_meta)
        elif self.graph is not None:
            return ModelGraphMessage(graph=self.graph)
        elif self.os_packages is not None:
            return OsPackagesMessage(os_packages=self.os_packages)
        elif self.env_details is not None:
            return SystemDetailsMessage(
                command=self.env_details["command"],
                env=self.env_details["env"],
                hostname=self.env_details["hostname"],
                ip=self.env_details["ip"],
                machine=self.env_details["machine"],
                os_release=self.env_details["os_release"],
                os_type=self.env_details["os_type"],
                os=self.env_details["os"],
                pid=self.env_details["pid"],
                processor=self.env_details["processor"],
                python_exe=self.env_details["python_exe"],
                python_version_verbose=self.env_details["python_version_verbose"],
                python_version=self.env_details["python_version"],
                user=self.env_details["user"],
            )
        else:
            raise ValueError(
                "can not convert to HTTP message format, message: %r" % self
            )

    @classmethod
    def deserialize(cls, message_dict):
        # type: (Type['WebSocketMessage'], Dict[str, Any]) -> WebSocketMessage
        ws_message = cls(
            context=message_dict.get("context", None),
        )
        # copy values
        for k, v in message_dict.items():
            ws_message.__dict__[k] = v

        return ws_message

    @classmethod
    def deserialize_to_http(cls, message_dict):
        ws_message = WebSocketMessage.deserialize(message_dict)
        return ws_message.to_http_message()

    def __repr__(self):
        filtered_dict = [(key, value) for key, value in self.__dict__.items() if value]
        string = ", ".join("%r=%r" % item for item in filtered_dict)
        return "Message(%s)" % string

    def __str__(self):
        return self.to_json()

    def __len__(self):
        return len(self.to_json())

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.__dict__ == other.__dict__
